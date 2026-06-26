#!/usr/bin/env python3
"""
Sync self-improving agent metrics to unified memory lake.
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

SOURCE_DIR = Path.home() / ".openclaw" / "agents"
TARGET_DIR = Path(__file__).parent.parent / "memory" / "sources" / "self-improving"
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


def sync_self_improving():
    """Sync self-improving metrics."""
    if not SOURCE_DIR.exists():
        print(f"Source dir not found: {SOURCE_DIR}")
        return

    last_sync = get_last_sync_time()
    synced_count = 0

    for metrics_file in SOURCE_DIR.rglob("metrics.json"):
        mtime = metrics_file.stat().st_mtime
        if mtime > last_sync:
            agent_name = metrics_file.parent.name
            dest = TARGET_DIR / f"{agent_name}_metrics.json"
            with open(metrics_file) as src:
                data = json.load(src)
                data["_synced_at"] = datetime.now().isoformat()
                with open(dest, "w") as dst:
                    json.dump(data, dst, indent=2)
            synced_count += 1

    save_sync_time()
    print(f"Synced {synced_count} self-improving metrics files")
