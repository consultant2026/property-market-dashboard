# Auction Market Dashboard

A static HTML dashboard displaying Australian auction market data for Sydney, Melbourne, Brisbane, Adelaide, and Canberra.

## Architecture

This project uses a **local data + remote display** architecture:
- **Data collection**: Runs locally on your laptop
- **Data storage**: Raw data files stay on your laptop
- **Dashboard generation**: Static HTML with embedded data
- **Hosting**: GitHub Pages (free, static hosting)

## Weekly Workflow

1. **Run data collection** (on your laptop):
   ```bash
   ./update_auction_data.sh
   ```

2. **Generate static dashboard** (on your laptop):
   ```bash
   python3 generate_static_dashboard.py
   ```
   This creates `docs/index.html` with all data embedded as JSON.

3. **Push to GitHub** (on your laptop):
   ```bash
   git add docs/index.html
   git commit -m "Update dashboard - [date]"
   git push origin main
   ```

4. **View dashboard**: Your friends can see it at `https://yourusername.github.io/your-repo/`

## Initial Setup

### 1. Create GitHub Repository

```bash
git init
git add .gitignore generate_static_dashboard.py README.md
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select **Deploy from a branch**
4. Select **main** branch and **/docs** folder
5. Click **Save**

Your dashboard will be available at: `https://YOUR_USERNAME.github.io/YOUR_REPO/`

### 3. First Deployment

1. Run data collection (if you have data):
   ```bash
   ./update_auction_data.sh
   ```

2. Generate the static dashboard:
   ```bash
   python3 generate_static_dashboard.py
   ```

3. Push to GitHub:
   ```bash
   git add docs/index.html
   git commit -m "Initial dashboard deployment"
   git push origin main
   ```

## Files in This Repository

- `generate_static_dashboard.py` - Script to generate static HTML from local data
- `docs/index.html` - Generated dashboard (only this file is pushed to GitHub)
- `.gitignore` - Excludes data files and scripts from GitHub

## Files NOT in Repository (Stay Local)

- All data collection scripts (`collect_*.py`, `process_*.py`, etc.)
- All data files (`auction_history/`, `auction_metrics/`, etc.)
- All shell scripts (`*.sh`)
- Flask applications (`dashboard_*/`, `app.py`)

## Customization

Edit `generate_static_dashboard.py` to:
- Change data file paths
- Adjust data processing logic
- Modify chart styling
- Add/remove cities

## Benefits

- **Free hosting** via GitHub Pages
- **No server** needed
- **Data privacy** - raw data stays on your laptop
- **Simple workflow** - just run one script weekly
- **Fast loading** - static HTML with embedded data
- **Version control** - track dashboard changes via Git

## Troubleshooting

### Dashboard not updating
- Make sure you're pushing `docs/index.html` to GitHub
- Check GitHub Pages deployment status in repository settings
- Wait 1-2 minutes for GitHub Pages to rebuild

### Data not loading
- Verify data files exist in `auction_history/` directory
- Check column names in your CSV files match the script expectations
- Run `generate_static_dashboard.py` locally and check console output

### GitHub Pages 404 error
- Ensure GitHub Pages is enabled and pointing to `/docs` folder
- Check that `docs/index.html` exists in your repository
- Verify the branch name matches (usually `main`)
