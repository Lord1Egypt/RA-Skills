#!/usr/bin/env python3
"""
Rename screenshots with smart patterns.

Usage:
    python rename_screenshots.py [directory] [--tags tag1,tag2] [--dry-run]

Examples:
    python rename_screenshots.py ~/Desktop --tags work,bug
    python rename_screenshots.py --dry-run
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

def parse_screenshot_filename(filename):
    """Extract date/time from default screenshot name."""
    # Pattern: Screenshot YYYY-MM-DD at HH.MM.SS.png
    match = re.search(r'Screenshot (\d{4}-\d{2}-\d{2}) at (\d{2})\.(\d{2})\.(\d{2})', filename)
    if match:
        date_str = match.group(1)
        time_str = f"{match.group(2)}:{match.group(3)}:{match.group(4)}"
        return date_str, time_str
    return None, None

def rename_screenshot(filepath, tags=None, dry_run=False):
    """Generate new filename with optional tags."""
    filename = os.path.basename(filepath)
    date_str, time_str = parse_screenshot_filename(filename)
    
    if not date_str:
        # Use file modification date as fallback
        mtime = os.path.getmtime(filepath)
        date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        time_str = datetime.fromtimestamp(mtime).strftime('%H:%M:%S')
    
    # Build new name
    base_name = f"{date_str}_{time_str.replace(':', '-')}"
    if tags:
        base_name += f"_{'+'.join(tags)}"
    
    new_filename = f"{base_name}.png"
    return new_filename

def main():
    args = sys.argv[1:]
    
    # Parse args
    directory = None
    tags = None
    dry_run = False
    
    i = 0
    while i < len(args):
        if args[i] == '--tags' and i + 1 < len(args):
            tags = args[i + 1].split(',')
            i += 2
        elif args[i] == '--dry-run':
            dry_run = True
            i += 1
        elif not args[i].startswith('--'):
            directory = args[i]
            i += 1
        else:
            i += 1
    
    # Default directory
    if not directory:
        directory = os.path.expanduser('~/Desktop')
    
    directory = os.path.expanduser(directory)
    
    # Find screenshots
    screenshots = [f for f in os.listdir(directory) 
                   if f.startswith('Screenshot') and f.endswith('.png')]
    
    if not screenshots:
        print(f"No screenshots found in {directory}")
        return
    
    print(f"Found {len(screenshots)} screenshots in {directory}\n")
    
    for filename in screenshots:
        filepath = os.path.join(directory, filename)
        new_name = rename_screenshot(filepath, tags=tags)
        
        if dry_run:
            print(f"[DRY] {filename} → {new_name}")
        else:
            new_path = os.path.join(directory, new_name)
            if os.path.exists(new_path):
                print(f"[SKIP] {new_name} already exists")
            else:
                os.rename(filepath, new_path)
                print(f"[RENAMED] {filename} → {new_name}")

if __name__ == '__main__':
    main()
