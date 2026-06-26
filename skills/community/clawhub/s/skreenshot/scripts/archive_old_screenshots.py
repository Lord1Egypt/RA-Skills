#!/usr/bin/env python3
"""
Archive old screenshots to organized folders.

Usage:
    python archive_old_screenshots.py [--days N] [--dry-run]

Moves screenshots older than N days from Desktop to Pictures/Screenshots/
organized by date.

Examples:
    python archive_old_screenshots.py --days 7
    python archive_old_screenshots.py --days 30 --dry-run
"""

import os
import re
import sys
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def get_screenshot_date(filepath):
    """Extract date from filename or use mtime."""
    filename = os.path.basename(filepath)
    match = re.search(r'Screenshot (\d{4})-(\d{2})-(\d{2})', filename)
    if match:
        return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    
    # Fallback to modification time
    mtime = os.path.getmtime(filepath)
    return datetime.fromtimestamp(mtime)

def archive_screenshots(source_dir, dest_base, days_old=30, dry_run=False):
    """Move old screenshots to dated archive folders."""
    
    source_dir = os.path.expanduser(source_dir)
    dest_base = os.path.expanduser(dest_base)
    
    # Find screenshots
    screenshots = [f for f in os.listdir(source_dir)
                   if f.startswith('Screenshot') and f.endswith('.png')]
    
    if not screenshots:
        print(f"No screenshots found in {source_dir}")
        return
    
    cutoff_date = datetime.now() - timedelta(days=days_old)
    moved = 0
    skipped = 0
    
    for filename in screenshots:
        filepath = os.path.join(source_dir, filename)
        screenshot_date = get_screenshot_date(filepath)
        
        if screenshot_date >= cutoff_date:
            # Recent, skip
            skipped += 1
            continue
        
        # Create dated folder: YYYY/MM/
        year_folder = os.path.join(dest_base, str(screenshot_date.year))
        month_folder = os.path.join(year_folder, f"{screenshot_date.month:02d}")
        
        if dry_run:
            print(f"[DRY] {filename} ({screenshot_date.date()}) → {month_folder}/")
        else:
            os.makedirs(month_folder, exist_ok=True)
            dest_path = os.path.join(month_folder, filename)
            if os.path.exists(dest_path):
                print(f"[SKIP] {filename} already exists in archive")
                skipped += 1
            else:
                shutil.move(filepath, dest_path)
                print(f"[MOVED] {filename} → {month_folder}/")
                moved += 1
    
    print(f"\nSummary: {moved} moved, {skipped} skipped (recent)")

def main():
    args = sys.argv[1:]
    
    days_old = 30
    dry_run = False
    
    i = 0
    while i < len(args):
        if args[i] == '--days' and i + 1 < len(args):
            days_old = int(args[i + 1])
            i += 2
        elif args[i] == '--dry-run':
            dry_run = True
            i += 1
        else:
            i += 1
    
    source = '~/Desktop'
    dest = '~/Pictures/Screenshots'
    
    print(f"Archiving screenshots older than {days_old} days")
    print(f"Source: {source}")
    print(f"Destination: {dest}")
    if dry_run:
        print("[DRY RUN - no files will be moved]\n")
    
    archive_screenshots(source, dest, days_old=days_old, dry_run=dry_run)

if __name__ == '__main__':
    main()
