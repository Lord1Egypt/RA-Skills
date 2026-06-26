#!/usr/bin/env python3
"""
Way Back - Cleanup Old Snapshots
Usage: python cleanup.py [--dry-run]
"""
import os
import sys
import time
from pathlib import Path

OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
SNAPSHOT_DIR = os.path.join(OPENCLAW_DIR, "snapshots")

# Config
MAX_COUNT = 50
RETENTION_DAYS = 7

def cleanup(dry_run=False):
    """Cleanup old snapshots"""
    print("🧹 Cleaning up old snapshots...")
    
    if not os.path.exists(SNAPSHOT_DIR):
        print("📭 No snapshots to clean up")
        return
    
    now = time.time()
    cutoff_time = now - (RETENTION_DAYS * 24 * 60 * 60)
    
    # Get all snapshots
    snapshots = []
    for item in os.listdir(SNAPSHOT_DIR):
        if item.startswith("v") and ("_full" in item or "_inc" in item):
            path = os.path.join(SNAPSHOT_DIR, item)
            if os.path.isdir(path):
                mtime = os.path.getmtime(path)
                snapshots.append((item, mtime))
    
    # Delete by age
    for snap, mtime in snapshots:
        if mtime < cutoff_time:
            print(f"  🗑️ Deleting old: {snap}")
            if not dry_run:
                import shutil
                shutil.rmtree(os.path.join(SNAPSHOT_DIR, snap))
    
    # Delete by count
    snapshots.sort(key=lambda x: int(x[0].split("_")[0].replace("v", "")))
    total = len(snapshots)
    
    if total > MAX_COUNT:
        excess = total - MAX_COUNT
        print(f"  📉 Deleting {excess} excess snapshots (max: {MAX_COUNT})")
        
        for snap, _ in snapshots[:excess]:
            print(f"  🗑️ Deleting: {snap}")
            if not dry_run:
                import shutil
                shutil.rmtree(os.path.join(SNAPSHOT_DIR, snap))
    
    print("✅ Cleanup complete")

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    cleanup(dry_run)
