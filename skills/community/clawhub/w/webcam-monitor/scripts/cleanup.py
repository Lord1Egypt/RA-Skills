#!/usr/bin/env python3.10
"""
Snapshot Cleanup - Deletes snapshots older than 1 hour
Can be run manually or as a cron job
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta

SNAPSHOT_DIR = Path.home() / ".openclaw" / "workspace" / "camera" / "snapshots"
LOG_FILE = Path.home() / ".openclaw" / "workspace" / "camera" / "cleanup.log"

# Config
MAX_AGE_HOURS = 1  # Delete snapshots older than this many hours

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

def cleanup_old_snapshots():
    """Delete snapshots older than MAX_AGE_HOURS"""
    if not SNAPSHOT_DIR.exists():
        log(f"Snapshot directory not found: {SNAPSHOT_DIR}")
        return 0
    
    cutoff_time = datetime.now() - timedelta(hours=MAX_AGE_HOURS)
    deleted_count = 0
    total_size_freed = 0
    
    log(f"Cleaning up snapshots older than {MAX_AGE_HOURS} hour(s)...")
    log(f"Cutoff time: {cutoff_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    for image_file in SNAPSHOT_DIR.glob("*.jpg"):
        try:
            # Get file modification time
            mtime = datetime.fromtimestamp(image_file.stat().st_mtime)
            
            if mtime < cutoff_time:
                file_size = image_file.stat().st_size
                image_file.unlink()  # Delete the file
                deleted_count += 1
                total_size_freed += file_size
                log(f"  Deleted: {image_file.name} (age: {datetime.now() - mtime})")
        except Exception as e:
            log(f"  Error deleting {image_file.name}: {e}")
    
    # Summary
    remaining = len(list(SNAPSHOT_DIR.glob("*.jpg")))
    log(f"Cleanup complete: {deleted_count} deleted, {remaining} remaining")
    if total_size_freed > 0:
        log(f"Space freed: {total_size_freed / (1024*1024):.2f} MB")
    
    return deleted_count

def main():
    log("=" * 50)
    log("Snapshot Cleanup Started")
    log("=" * 50)
    
    count = cleanup_old_snapshots()
    
    log(f"Done. Deleted {count} old snapshot(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())