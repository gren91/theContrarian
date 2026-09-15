#!/usr/bin/env python3
"""
Daily site update script for The Contrarian
Updates publication date on all pages and pushes to GitHub
"""
import os
import subprocess
from datetime import datetime
from pathlib import Path
import re

# Configuration
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
FILES = ["index.html", "rates.html", "crypto.html"]

def get_formatted_date():
    """Get today's date in format: 'September 13, 2026'"""
    return datetime.now().strftime("%B %d, %Y")

def update_html_files():
    """Update publication date in all HTML files"""
    today = get_formatted_date()
    updated_count = 0
    
    for filename in FILES:
        filepath = os.path.join(REPO_PATH, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠ File not found: {filepath}")
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update date pattern (matches various date formats in the file)
            # Looking for: "Published: [DATE]" or "Date: [DATE]" etc.
            original_content = content
            
            # Pattern 1: <p class="date">...</p>
            content = re.sub(
                r'(<p[^>]*class="date"[^>]*>)[^<]+(</p>)',
                rf'\1{today}\2',
                content
            )
            
            # Pattern 2: September XX, 2026 anywhere in the file
            content = re.sub(
                r'(September|October|November|December|January|February|March|April|May|June|July|August)\s+\d{1,2},\s+\d{4}',
                today,
                content
            )
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Updated: {filename}")
                updated_count += 1
            else:
                print(f"~ No changes needed: {filename}")
        
        except Exception as e:
            print(f"✗ Error updating {filename}: {e}")
    
    return updated_count > 0

def git_push():
    """Commit and push changes to GitHub"""
    try:
        os.chdir(REPO_PATH)
        
        # Check if there are changes
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if not result.stdout.strip():
            print("~ No changes to commit")
            return True
        
        # Add all changes
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit with timestamp
        today = get_formatted_date()
        commit_msg = f"Daily update: {today}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # Push to GitHub
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print(f"✓ Pushed to GitHub: {commit_msg}")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"✗ Git error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def main():
    """Main execution"""
    print(f"\n{'='*50}")
    print(f"The Contrarian - Daily Update Script")
    print(f"Running at: {datetime.now()}")
    print(f"{'='*50}\n")
    
    # Update HTML files
    if update_html_files():
        # Push to GitHub if changes were made
        git_push()
    
    print(f"\n{'='*50}")
    print("Update complete!")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
