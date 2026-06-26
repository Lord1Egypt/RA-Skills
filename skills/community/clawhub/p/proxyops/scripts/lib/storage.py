#!/usr/bin/env python3
import json
import os
from datetime import datetime

PROXY_DIR = os.path.expanduser("~/.openclaw/workspace/memory/proxy")
PROXIES_FILE = os.path.join(PROXY_DIR, "proxies.json")
SESSIONS_FILE = os.path.join(PROXY_DIR, "sessions.json")
STATS_FILE = os.path.join(PROXY_DIR, "stats.json")

def ensure_dir():
    os.makedirs(PROXY_DIR, exist_ok=True)

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

def load_proxies():
    now = datetime.now().isoformat()
    return _safe_load(PROXIES_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": now,
            "last_updated": now
        },
        "proxies": {}
    })

def save_proxies(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(PROXIES_FILE, data)

def load_sessions():
    now = datetime.now().isoformat()
    return _safe_load(SESSIONS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": now,
            "last_updated": now
        },
        "sessions": {}
    })

def save_sessions(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(SESSIONS_FILE, data)

def load_stats():
    return _safe_load(STATS_FILE, {
        "total_proxies": 0,
        "active_proxies": 0,
        "inactive_proxies": 0,
        "expired_proxies": 0,
        "last_scored_at": None
    })

def save_stats(data):
    _atomic_save(STATS_FILE, data)
