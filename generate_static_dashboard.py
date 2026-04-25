#!/usr/bin/env python3
"""
Generate static HTML dashboard with embedded data for GitHub Pages.
Run this weekly after collecting new auction data.
"""

import pandas as pd
import json
from datetime import datetime
import os

# City configurations
CITIES = {
    'sydney': 'Sydney',
    'melbourne': 'Melbourne',
    'brisbane': 'Brisbane',
    'adelaide': 'Adelaide',
    'canberra': 'Canberra'
}

def load_city_data(city):
    """Load auction metrics data for a specific city."""
    # Read from auction_metrics/metrics/ folder
    data_path = f'auction_metrics/metrics/{city}_metrics.csv'
    
    if not os.path.exists(data_path):
        print(f"Warning: Data file not found for {city}: {data_path}")
        return None
    
    try:
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        print(f"Error loading data for {city}: {e}")
        return None

def process_data_for_city(df, city):
    """Process data for a city into the format expected by the dashboard."""
    if df is None or df.empty:
        return None
    
    # Convert date column
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        dates = df['Date'].dt.strftime('%Y-%m-%d').tolist()
    else:
        dates = []
    
    # Extract data from metrics CSV
    # CSV columns: Date, Auctions scheduled, RealTrend, Market Tightness, UnSold Auctions, Median Price ($)
    scheduled = df.get('Auctions scheduled', []).tolist()
    realtrend = df.get('RealTrend', []).tolist()
    market_tightness = df.get('Market Tightness', []).tolist()
    unsold_percent = df.get('UnSold Auctions', []).tolist()
    
    # Calculate 8-week moving average for RealTrend
    realtrend_ma = pd.Series(realtrend).rolling(window=8, min_periods=1).mean().tolist()
    
    data = {
        'city': city,
        'city_display': CITIES.get(city, city),
        'dates': dates,
        'realtrend': realtrend,
        'realtrend_ma': realtrend_ma,
        'scheduled': scheduled,
        'market_tightness': market_tightness,
        'unsold_percent': unsold_percent,
        'last_updated': datetime.now().isoformat()
    }
    
    return data

def generate_html_with_data(all_city_data):
    """Generate the complete HTML file with embedded data."""
    
    # Convert data to JSON string
    data_json = json.dumps(all_city_data, indent=2)
    
    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <title>Property Market Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px;
            background-color: #f5f7fa;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .charts-container {{
            display: flex;
            flex-direction: column;
            gap: 40px;
        }}
        .city-chart {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        .city-chart h2 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .page-header {{
            text-align: center;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
        }}
        .page-header h1 {{
            margin: 0 0 5px 0;
            color: #2c3e50;
        }}
        .last-updated {{ 
            color: #777; 
            font-size: 14px;
            margin: 0;
        }}
        .time-range-buttons {{
            display: flex;
            justify-content: center;
            gap: 8px;
            margin: 15px 0;
            flex-wrap: wrap;
        }}
        .time-range-btn {{
            padding: 6px 12px;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }}
        .time-range-btn:hover {{
            background-color: #e9ecef;
        }}
        .time-range-btn.active {{
            background-color: #007bff;
            color: white;
            border-color: #007bff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="page-header">
            <h1>Property Market Dashboard</h1>
            <div id="last-updated" class="last-updated">Loading...</div>
            <div class="time-range-buttons">
                <button class="time-range-btn active" data-months="3">3 Months</button>
                <button class="time-range-btn" data-months="6">6 Months</button>
                <button class="time-range-btn" data-months="12">1 Year</button>
                <button class="time-range-btn" data-months="24">2 Years</button>
                <button class="time-range-btn" data-months="36">3 Years</button>
                <button class="time-range-btn" data-months="48">4 Years</button>
                <button class="time-range-btn" data-months="0">All Time</button>
            </div>
        </div>
        <div class="charts-container">
            <div class="city-chart">
                <h2>Sydney</h2>
                <div id="chart-sydney" style="height: 500px;"></div>
            </div>
            <div class="city-chart">
                <h2>Melbourne</h2>
                <div id="chart-melbourne" style="height: 500px;"></div>
            </div>
            <div class="city-chart">
                <h2>Brisbane</h2>
                <div id="chart-brisbane" style="height: 500px;"></div>
            </div>
            <div class="city-chart">
                <h2>Adelaide</h2>
                <div id="chart-adelaide" style="height: 500px;"></div>
            </div>
            <div class="city-chart">
                <h2>Canberra</h2>
                <div id="chart-canberra" style="height: 500px;"></div>
            </div>
        </div>
    </div>
    
    <script>
        // Embedded data
        const EMBEDDED_DATA = {data_json};
        
        const CITIES = {{
            'sydney': 'Sydney',
            'melbourne': 'Melbourne',
            'brisbane': 'Brisbane',
            'adelaide': 'Adelaide',
            'canberra': 'Canberra'
        }};
        
        let currentTimeRange = 6;
        let cityDataCache = {{}};
        let globalLatestDate = null;
        
        function processData(dates, values) {{
            if (!values || !dates || !Array.isArray(values) || !Array.isArray(dates)) {{
                return {{dates: [], values: []}};
            }}
            
            const result = [];
            for (let i = 0; i < Math.min(dates.length, values.length); i++) {{
                if (dates[i] && values[i] !== null && values[i] !== undefined) {{
                    result.push({{
                        date: dates[i],
                        value: values[i]
                    }});
                }}
            }}
            
            result.sort((a, b) => new Date(a.date) - new Date(b.date));
            
            return {{
                dates: result.map(item => item.date),
                values: result.map(item => item.value)
            }};
        }}
        
        function filterDataByDateRange(data, months) {{
            if (months === 0) return data;
            
            const cutoffDate = new Date();
            cutoffDate.setMonth(cutoffDate.getMonth() - months);
            
            const filteredDates = [];
            const filteredValues = {{}};
            
            Object.keys(data).forEach(key => {{
                if (key === 'dates' || key === 'city' || key === 'city_display' || key === 'last_updated') {{
                    return;
                }}
                
                if (Array.isArray(data[key])) {{
                    filteredValues[key] = [];
                }}
            }});
            
            data.dates.forEach((dateStr, index) => {{
                const date = new Date(dateStr);
                if (date >= cutoffDate) {{
                    filteredDates.push(dateStr);
                    Object.keys(filteredValues).forEach(key => {{
                        if (data[key] && data[key][index] !== undefined) {{
                            filteredValues[key].push(data[key][index]);
                        }}
                    }});
                }}
            }});
            
            return {{
                ...data,
                dates: filteredDates,
                ...filteredValues
            }};
        }}
        
        function formatDate(dateString) {{
            if (!dateString) return 'N/A';
            const date = new Date(dateString);
            if (isNaN(date)) return 'N/A';
            
            const day = date.getDate();
            const month = date.toLocaleString('default', {{ month: 'short' }});
            const year = date.getFullYear();
            
            return `${{day}} ${{month}} ${{year}}`;
        }}
        
        function updateGlobalLatestDate() {{
            let latest = null;
            Object.keys(cityDataCache).forEach(city => {{
                const data = cityDataCache[city];
                if (data && data.dates && data.dates.length > 0) {{
                    const date = new Date(data.dates[0]);
                    if (!latest || date > latest) {{
                        latest = date;
                    }}
                }}
            }});
            globalLatestDate = latest;
        }}
        
        function updateLastUpdated(timestamp) {{
            const lastUpdatedElement = document.getElementById('last-updated');
            if (lastUpdatedElement) {{
                lastUpdatedElement.textContent = timestamp || 'Loading...';
            }}
        }}
        
        function createVolumeChartForCity(city, data, latestDate = '') {{
            const cityName = CITIES[city] || 'City';
            const chartContainer = document.getElementById(`chart-${{city}}`);
            if (!chartContainer) return;
            
            const processedRealtrend = processData(data.dates, data.realtrend);
            const processedRealtrendMA = processData(data.dates, data.realtrend_ma);
            
            const sortedDates = processedRealtrend.dates;
            
            const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            const dateLabels = [];
            const dateValues = [];
            let lastMonth = -1;
            let lastYear = -1;
            
            sortedDates.forEach((dateStr, index) => {{
                const date = new Date(dateStr);
                const month = date.getMonth();
                const year = date.getFullYear();
                
                if (month !== lastMonth || year !== lastYear) {{
                    dateLabels.push(`${{monthNames[month]}} ${{year}}`);
                    dateValues.push(dateStr);
                    lastMonth = month;
                    lastYear = year;
                }} else {{
                    dateLabels.push('');
                    dateValues.push(dateStr);
                }}
            }});
            
            const totalPoints = dateValues.length;
            const defaultRange = [0, totalPoints - 1];
            
            const xAxis = {{
                tickvals: dateValues,
                ticktext: dateLabels,
                type: 'category',
                title: 'Date',
                showgrid: true,
                gridcolor: '#f0f0f0',
                rangeslider: {{
                    visible: true,
                    thickness: 0.05,
                    bgcolor: 'rgba(150,150,150,0.2)'
                }},
                tickangle: -45,
                tickfont: {{ size: 10 }},
                autorange: false,
                range: defaultRange,
                categoryorder: 'array',
                categoryarray: dateValues
            }};
            
            const formatTooltipDate = (dateStr) => {{
                if (!dateStr) return '';
                const date = new Date(dateStr);
                if (isNaN(date)) return '';
                
                const day = date.getDate();
                const month = date.toLocaleString('default', {{ month: 'short' }});
                const year = date.getFullYear();
                
                return `${{day}} ${{month}} ${{year}}`;
            }};
            
            const hoverText = processedRealtrend.dates.map((date, i) => {{
                const dateStr = formatTooltipDate(date);
                const trend = (processedRealtrend.values[i] * 100).toFixed(1);
                return `Date: ${{dateStr}}<br>Demand Trend: ${{trend}}%`;
            }});
            
            const trace1 = {{
                x: processedRealtrend.dates,
                y: processedRealtrend.values,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Demand Trend',
                line: {{
                    color: '#00008B',
                    width: 2,
                    shape: 'spline',
                    smoothing: 0.6
                }},
                marker: {{
                    color: '#00008B',
                    size: 6
                }},
                hovertemplate: '%{{customdata}}<extra></extra>',
                customdata: hoverText
            }};
            
            const trace2 = {{
                x: processedRealtrendMA.dates,
                y: processedRealtrendMA.values,
                type: 'scatter',
                mode: 'lines',
                name: '8-Week MA',
                line: {{
                    color: 'orange',
                    width: 2,
                    dash: 'dash'
                }},
                hovertemplate: '%{{customdata}}<extra></extra>',
                customdata: hoverText
            }};
            
            const referenceLines = [];
            
            if (city === 'sydney') {{
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.8, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.8, line: {{color: '#FF6B6B', width: 1.5, dash: 'solid'}}}});
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.45, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.45, line: {{color: '#7EC8E3', width: 1.5, dash: 'solid'}}}});
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.625, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.625, line: {{color: '#D3D3D3', width: 1, dash: 'dash'}}}});
            }} else if (city === 'melbourne') {{
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.75, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.75, line: {{color: '#FF6B6B', width: 1.5, dash: 'solid'}}}});
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.35, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.35, line: {{color: '#7EC8E3', width: 1.5, dash: 'solid'}}}});
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.55, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.55, line: {{color: '#D3D3D3', width: 1, dash: 'dash'}}}});
            }} else if (city === 'brisbane') {{
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.7, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.7, line: {{color: '#FF6B6B', width: 1.5, dash: 'solid'}}}});
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.25, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.25, line: {{color: '#7EC8E3', width: 1.5, dash: 'solid'}}}});
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.475, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.475, line: {{color: '#D3D3D3', width: 1, dash: 'dash'}}}});
            }} else if (city === 'adelaide') {{
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.85, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.85, line: {{color: '#FF6B6B', width: 1.5, dash: 'solid'}}}});
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.25, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.25, line: {{color: '#7EC8E3', width: 1.5, dash: 'solid'}}}});
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.55, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.55, line: {{color: '#D3D3D3', width: 1, dash: 'dash'}}}});
            }} else if (city === 'canberra') {{
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.95, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.95, line: {{color: '#FF6B6B', width: 1.5, dash: 'solid'}}}});
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.35, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.35, line: {{color: '#7EC8E3', width: 1.5, dash: 'solid'}}}});
                referenceLines.push({{type: 'line', x0: processedRealtrend.dates[0], y0: 0.65, x1: processedRealtrend.dates[processedRealtrend.dates.length - 1], y1: 0.65, line: {{color: '#D3D3D3', width: 1, dash: 'dash'}}}});
            }}
            
            const layout = {{
                title: {{ text: `${{cityName}} - Demand Trend`, font: {{ size: 16, color: '#2c3e50' }}, x: 0.5, xanchor: 'center', y: 0.99 }},
                shapes: referenceLines,
                margin: {{ t: 50, l: 60, r: 60, b: 100 }},
                height: 500,
                hovermode: 'x unified',
                xaxis: xAxis,
                yaxis: {{
                    title: 'Demand Trend',
                    side: 'left',
                    showgrid: true,
                    zeroline: true,
                    zerolinecolor: 'rgba(0,0,0,0.1)'
                }},
                legend: {{ x: 0, y: 1.1, orientation: 'h', bgcolor: 'rgba(255,255,255,0.8)' }},
                showlegend: true,
                plot_bgcolor: 'rgba(0,0,0,0)',
                paper_bgcolor: 'rgba(0,0,0,0)'
            }};
            
            const config = {{
                responsive: true,
                displayModeBar: true,
                scrollZoom: true,
                displaylogo: false
            }};
            
            Plotly.newPlot(`chart-${{city}}`, [trace1, trace2], layout, config);
        }}
        
        function loadData() {{
            console.log('Loading embedded data...');
            
            // Cache all embedded data
            EMBEDDED_DATA.forEach(cityData => {{
                if (cityData && cityData.city) {{
                    cityDataCache[cityData.city] = cityData;
                }}
            }});
            
            updateGlobalLatestDate();
            
            // Display all cities
            Object.keys(CITIES).forEach(city => {{
                const data = cityDataCache[city];
                if (data && data.dates && data.dates.length > 0) {{
                    const filteredData = filterDataByDateRange(data, currentTimeRange);
                    const latestDate = globalLatestDate ? formatDate(globalLatestDate) : 'N/A';
                    createVolumeChartForCity(city, filteredData, latestDate);
                }}
            }});
            
            if (globalLatestDate) {{
                const options = {{ year: 'numeric', month: 'long', day: 'numeric' }};
                updateLastUpdated('Latest data point: ' + globalLatestDate.toLocaleDateString('en-AU', options));
            }}
        }}
        
        // Time range button handlers
        document.querySelectorAll('.time-range-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.time-range-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentTimeRange = parseInt(this.dataset.months);
                loadData();
            }});
        }});
        
        // Load data on page load
        loadData();
    </script>
</body>
</html>"""
    
    return html_template

def main():
    """Main function to generate the static dashboard."""
    print("Generating static dashboard...")
    
    # Load data for all cities
    all_city_data = []
    for city in CITIES.keys():
        print(f"Loading data for {city}...")
        df = load_city_data(city)
        if df is not None:
            processed_data = process_data_for_city(df, city)
            if processed_data:
                all_city_data.append(processed_data)
                print(f"  Loaded {len(processed_data['dates'])} data points")
        else:
            print(f"  No data available for {city}")
    
    if not all_city_data:
        print("Error: No data loaded for any city")
        return
    
    # Generate HTML
    html_content = generate_html_with_data(all_city_data)
    
    # Save to docs directory for GitHub Pages
    output_dir = 'docs'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'index.html')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Static dashboard generated: {output_file}")
    print(f"Total cities with data: {len(all_city_data)}")
    print("\nNext steps:")
    print("1. Commit and push the docs/index.html file to GitHub")
    print("2. Enable GitHub Pages on your repository")
    print("3. Select 'docs' folder as the source")

if __name__ == '__main__':
    main()
