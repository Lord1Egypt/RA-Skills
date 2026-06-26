#!/usr/bin/env python3
import json
import os
from datetime import datetime

PROXY_DIR = os.path.expanduser("~/.openclaw/workspace/memory/proxy")
PROXIES_FILE = os.path.join(PROXY_DIR, "proxies.json")
SESSIONS_FILE = os.path.join(PROXY_DIR, "sessions.json")
STATS_FILE = os.path.join(PROXY_DIR, "stats.json")

def write_json_if_missing(path, payload):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

def main():
    now = datetime.now().isoformat()
    os.makedirs(PROXY_DIR, exist_ok=True)

    write_json_if_missing(PROXIES_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": now,
            "last_updated": now
        },
        "proxies": {}
    })

    write_json_if_missing(SESSIONS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": now,
            "last_updated": now
        },
        "sessions": {}
    })

    write_json_if_missing(STATS_FILE, {
        "total_proxies": 0,
        "active_proxies": 0,
        "inactive_proxies": 0,
        "expired_proxies": 0,
        "last_scored_at": None
    })

    print("✓ Proxy storage initialized")
    print(f"  {PROXIES_FILE}")
    print(f"  {SESSIONS_FILE}")
    print(f"  {STATS_FILE}")

if __name__ == "__main__":
    main()
