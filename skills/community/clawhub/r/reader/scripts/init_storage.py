#!/usr/bin/env python3
import json
import os
from datetime import datetime

READER_DIR = os.path.expanduser("~/.openclaw/workspace/memory/reader")
HISTORY_FILE = os.path.join(READER_DIR, "history.json")

def write_json_if_missing(path, payload):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(READER_DIR, exist_ok=True)
    write_json_if_missing(HISTORY_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "sessions": []
    })
    print("✓ Reader storage initialized")
    print(f"  {HISTORY_FILE}")

if __name__ == "__main__":
    main()
