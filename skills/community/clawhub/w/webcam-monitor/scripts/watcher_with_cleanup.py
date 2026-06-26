#!/usr/bin/env python3.10
"""
Snapshot Watcher with Auto-Cleanup
Watches for new snapshots AND automatically deletes old ones
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta

SNAPSHOT_DIR = Path.home() / ".openclaw" / "workspace" / "camera" / "snapshots"
QUEUE_DIR = Path.home() / ".openclaw" / "workspace" / "camera" / "analysis_queue"
LOG_FILE = Path.home() / ".openclaw" / "workspace" / "camera" / "watcher.log"

# Config
MAX_AGE_HOURS = 1  # Delete snapshots older than this
CLEANUP_INTERVAL = 300  # Check for old files every 5 minutes (300 seconds)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

def cleanup_old_files():
    """Delete snapshots and queue files older than MAX_AGE_HOURS"""
    cutoff_time = datetime.now() - timedelta(hours=MAX_AGE_HOURS)
    deleted_snapshots = 0
    deleted_queue = 0
    
    # Clean up old snapshots
    for image_file in SNAPSHOT_DIR.glob("*.jpg"):
        try:
            mtime = datetime.fromtimestamp(image_file.stat().st_mtime)
            if mtime < cutoff_time:
                image_file.unlink()
                deleted_snapshots += 1
        except Exception as e:
            log(f"  Error deleting {image_file.name}: {e}")
    
    # Clean up old queue files
    for queue_file in QUEUE_DIR.glob("*.txt"):
        try:
            mtime = datetime.fromtimestamp(queue_file.stat().st_mtime)
            if mtime < cutoff_time:
                queue_file.unlink()
                deleted_queue += 1
        except Exception as e:
            log(f"  Error deleting queue file {queue_file.name}: {e}")
    
    if deleted_snapshots > 0 or deleted_queue > 0:
        remaining_snapshots = len(list(SNAPSHOT_DIR.glob("*.jpg")))
        remaining_queue = len(list(QUEUE_DIR.glob("*.txt")))
        log(f"🧹 Auto-cleanup: {deleted_snapshots} snapshot(s), {deleted_queue} queue file(s) deleted")
        log(f"   Remaining: {remaining_snapshots} snapshots, {remaining_queue} queue files")
    
    return deleted_snapshots + deleted_queue

def queue_for_analysis(image_path):
    """Queue image for analysis"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    queue_file = QUEUE_DIR / f"analyze_{timestamp}_{image_path.stem}.txt"
    
    with open(queue_file, "w") as f:
        f.write(str(image_path))
    
    log(f"   → Queued: {queue_file.name}")
    log(f"   → Person: Jade OR Sarah (home office/living room, cat tree)")
    return queue_file

def watch_snapshots():
    """Watch for new snapshots with auto-cleanup"""
    log(f"👁️  Watching: {SNAPSHOT_DIR}")
    log(f"🧹 Auto-cleanup: Deletes snapshots and queue files older than {MAX_AGE_HOURS} hour(s)")
    log("Press Ctrl+C to stop\n")
    
    known_files = set(f.name for f in SNAPSHOT_DIR.glob("*.jpg"))
    log(f"Found {len(known_files)} existing snapshots")
    
    last_cleanup = time.time()
    
    try:
        while True:
            time.sleep(2)
            
            # Check for new snapshots
            current_files = set(f.name for f in SNAPSHOT_DIR.glob("*.jpg"))
            new_files = current_files - known_files
            
            for filename in sorted(new_files):
                image_path = SNAPSHOT_DIR / filename
                time.sleep(0.5)
                
                if image_path.exists() and image_path.stat().st_size > 1000:
                    log(f"📸 NEW: {filename}")
                    queue_for_analysis(image_path)
            
            known_files = current_files
            
            # Periodic cleanup
            if time.time() - last_cleanup > CLEANUP_INTERVAL:
                cleanup_old_files()
                last_cleanup = time.time()
                # Refresh known files after cleanup
                known_files = set(f.name for f in SNAPSHOT_DIR.glob("*.jpg"))
            
    except KeyboardInterrupt:
        log("\n👋 Watcher stopped")

def main():
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    
    log("=" * 60)
    log("📷 Motion Watcher + Auto-Cleanup")
    log(f"Deletes snapshots older than {MAX_AGE_HOURS} hour(s)")
    log("=" * 60)
    
    watch_snapshots()
    return 0

if __name__ == "__main__":
    sys.exit(main())