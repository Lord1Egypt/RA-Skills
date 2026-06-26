#!/usr/bin/env python3
import json
import os
from datetime import datetime

TODO_DIR = os.path.expanduser("~/.openclaw/workspace/memory/todo")
ITEMS_FILE = os.path.join(TODO_DIR, "items.json")
STATS_FILE = os.path.join(TODO_DIR, "stats.json")
ARCHIVE_FILE = os.path.join(TODO_DIR, "archive.json")

def ensure_dir():
    os.makedirs(TODO_DIR, exist_ok=True)

def _safe_load(path, default):
    ensure_dir()
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default

def _atomic_save(path, data):
    ensure_dir()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def load_items():
    return _safe_load(ITEMS_FILE, {
        "metadata": {
            "version": "3.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "items": {}
    })

def save_items(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(ITEMS_FILE, data)

def load_stats():
    return _safe_load(STATS_FILE, {
        "total_items_created": 0,
        "total_items_completed": 0,
        "total_items_archived": 0,
        "total_projects_created": 0,
        "total_commitments_fulfilled": 0,
        "total_weight_released": 0,
        "total_minutes_completed": 0,
        "last_daily_sync_at": None,
        "last_weekly_review_at": None
    })

def save_stats(data):
    _atomic_save(STATS_FILE, data)

def load_archive():
    return _safe_load(ARCHIVE_FILE, {
        "metadata": {
            "version": "3.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "items": {}
    })

def save_archive(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(ARCHIVE_FILE, data)
