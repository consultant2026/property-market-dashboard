#!/usr/bin/env python3
"""
Weekly automation script:
1. Run data collection
2. Generate static dashboard
3. Commit and push to GitHub

Run this weekly to update the dashboard.
"""

import subprocess
import sys
from datetime import datetime

def run_command(cmd, description):
    """Run a command and print output."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def main():
    """Main automation workflow."""
    print("=" * 60)
    print("Weekly Dashboard Update and Deployment")
    print("=" * 60)
    
    # Step 1: Run data collection
    print("\n" + "=" * 60)
    print("Step 1: Collecting auction data")
    print("=" * 60)
    if not run_command("./update_auction_data.sh", "Running data collection script"):
        print("Warning: Data collection failed, but continuing with existing data...")
    
    # Step 2: Generate static dashboard
    print("\n" + "=" * 60)
    print("Step 2: Generating static dashboard")
    print("=" * 60)
    if not run_command("python3 generate_static_dashboard.py", "Generating dashboard HTML"):
        print("Error: Failed to generate dashboard")
        sys.exit(1)
    
    # Step 3: Commit and push to GitHub
    print("\n" + "=" * 60)
    print("Step 3: Deploying to GitHub")
    print("=" * 60)
    
    # Check if docs/index.html exists
    if not run_command("test -f docs/index.html", "Checking for generated HTML"):
        print("Error: docs/index.html not found")
        sys.exit(1)
    
    # Add to git
    if not run_command("git add docs/index.html", "Adding HTML to git"):
        print("Error: Failed to add file to git")
        sys.exit(1)
    
    # Commit with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_message = f"Update dashboard - {timestamp}"
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        print("Warning: No changes to commit or commit failed")
    
    # Push to GitHub
    if not run_command("git push origin main", "Pushing to GitHub"):
        print("Error: Failed to push to GitHub")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ Deployment complete!")
    print("=" * 60)
    print("\nYour dashboard will be available at:")
    print("https://YOUR_USERNAME.github.io/YOUR_REPO/")
    print("\nIt may take 1-2 minutes for GitHub Pages to update.")

if __name__ == '__main__':
    main()
