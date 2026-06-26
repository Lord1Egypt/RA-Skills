#!/usr/bin/env python3
"""
Sync Claude Code JSONL logs to unified memory lake.
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

SOURCE_DIR = Path.home() / ".claude" / "projects"
TARGET_DIR = Path(__file__).parent.parent / "memory" / "sources" / "claude-code"
STATE_FILE = TARGET_DIR / ".sync_state.json"


def get_last_sync_time():
    """Get last sync timestamp."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f).get("last_sync", 0)
    return 0


def save_sync_time():
    """Save current sync timestamp."""
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"last_sync": datetime.now().timestamp()}, f)


def sync_claude_code():
    """Sync Claude Code JSONL files."""
    if not SOURCE_DIR.exists():
        print(f"Source dir not found: {SOURCE_DIR}")
        return

    last_sync = get_last_sync_time()
    synced_count = 0

    for project_dir in SOURCE_DIR.rglob("sessions/*.jsonl"):
        mtime = project_dir.stat().st_mtime
        if mtime > last_sync:
            dest = TARGET_DIR / project_dir.name
            shutil.copy2(project_dir, dest)
            synced_count += 1

    save_sync_time()
    print(f"Synced {synced_count} Claude Code JSONL files")


if __name__ == "__main__":
    sync_claude_code()
