#!/usr/bin/env python3
"""
savemaintenance backup manager — archive snapshot of memory state.

Usage:
  python3 snapshot.py                 # Full snapshot (conversation log + index + topic map)
  python3 snapshot.py list            # List available backups
  python3 snapshot.py restore <tag>   # Restore from a backup tag
"""

import json
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace")).resolve()
SAVED_DIR = Path(os.path.expanduser("~/.openclaw/workspace/saved"))
PROJECT_DIR = Path(os.path.expanduser("~/.openclaw/workspace/savemaintenance"))
BACKUP_DIR = PROJECT_DIR / "backups"
SNAPSHOT_DIR = PROJECT_DIR / "snapshots"
FTS5_DB = Path("/dev/shm/memory-index.db")
CONV_LOG = SAVED_DIR / "conversation-log.md"
TOPIC_PATH = SAVED_DIR / "topic-index.json"
STUB_PATH = WORKSPACE / "stub-index.md"
INDEX_SCRIPT = SAVED_DIR / "memory-index.py"

def timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")

def take_snapshot(tag=None):
    """Snapshot the current state of the memory system."""
    tag = tag or timestamp()
    snap_dir = SNAPSHOT_DIR / tag
    snap_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Taking snapshot: {tag}")
    
    # conversation-log.md
    if CONV_LOG.exists():
        shutil.copy2(CONV_LOG, snap_dir / "conversation-log.md")
        print(f"  ✓ conversation-log.md ({CONV_LOG.stat().st_size:,} bytes)")
    
    # topic-index.json
    if TOPIC_PATH.exists():
        shutil.copy2(TOPIC_PATH, snap_dir / "topic-index.json")
        print(f"  ✓ topic-index.json ({TOPIC_PATH.stat().st_size:,} bytes)")
    
    # stub-index.md
    if STUB_PATH.exists():
        shutil.copy2(STUB_PATH, snap_dir / "stub-index.md")
        print(f"  ✓ stub-index.md ({STUB_PATH.stat().st_size:,} bytes)")
    
    # FTS5 DB
    if FTS5_DB.exists():
        db_dest = snap_dir / "memory-index.db"
        shutil.copy2(FTS5_DB, db_dest)
        print(f"  ✓ memory-index.db ({FTS5_DB.stat().st_size:,} bytes)")
    
    # File manifest
    manifest = {}
    if SAVED_DIR.exists():
        files = sorted(SAVED_DIR.iterdir())
        manifest = {
            f.name: {"size": f.stat().st_size, "mtime": datetime.fromtimestamp(f.stat().st_mtime).isoformat()}
            for f in files if f.is_file()
        }
    
    (snap_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"  ✓ manifest.json ({len(manifest)} files)")
    
    print(f"\nSnapshot saved to: {snap_dir}")


def list_snapshots():
    """List available snapshots."""
    if not SNAPSHOT_DIR.exists():
        print("No snapshots found.")
        return
    
    snapshots = sorted(SNAPSHOT_DIR.iterdir())
    if not snapshots:
        print("No snapshots found.")
        return
    
    print(f"Snapshots ({len(snapshots)}):")
    for s in snapshots:
        if s.is_dir():
            conv_log = s / "conversation-log.md"
            manifest = s / "manifest.json"
            count = ""
            if manifest.exists():
                try:
                    m = json.loads(manifest.read_text())
                    count = f" ({len(m)} files)"
                except:
                    pass
            size = ""
            if conv_log.exists():
                size = f" [{conv_log.stat().st_size:,}b]"
            print(f"  {s.name}{size}{count}")


def has_command(cmd):
    """Check if a command exists."""
    return subprocess.run(["which", cmd], capture_output=True).returncode == 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_snapshots()
    elif len(sys.argv) > 2 and sys.argv[1] == "take":
        take_snapshot(sys.argv[2] if len(sys.argv) > 2 else None)
    elif len(sys.argv) > 1 and sys.argv[1] == "take":
        take_snapshot()
    else:
        # Default: take snapshot with timestamp
        take_snapshot()
