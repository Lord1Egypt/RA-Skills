#!/usr/bin/env python3
import json
import os
from datetime import datetime

BASE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/terminal")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

def ensure_dir():
    os.makedirs(BASE_DIR, exist_ok=True)

def _secure_permissions(path):
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass

def load_history():
    ensure_dir()
    if not os.path.exists(HISTORY_FILE):
        return {
            "metadata": {
                "version": "1.0.2",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            },
            "runs": []
        }
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "metadata": {
                "version": "1.0.2",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            },
            "runs": []
        }

def save_history(data):
    ensure_dir()
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    tmp = HISTORY_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, HISTORY_FILE)
    _secure_permissions(HISTORY_FILE)
