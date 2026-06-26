#!/usr/bin/env python3
import json
import os
from datetime import datetime

READER_DIR = os.path.expanduser("~/.openclaw/workspace/memory/reader")
HISTORY_FILE = os.path.join(READER_DIR, "history.json")

def ensure_dir():
    os.makedirs(READER_DIR, exist_ok=True)

def load_history():
    ensure_dir()
    if not os.path.exists(HISTORY_FILE):
        return {
            "metadata": {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            },
            "sessions": []
        }
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(data):
    ensure_dir()
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    tmp = HISTORY_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, HISTORY_FILE)
