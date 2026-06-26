#!/usr/bin/env python3
import json
import os
from datetime import datetime

VERIFIER_DIR = os.path.expanduser("~/.openclaw/workspace/memory/verifier")
CASES_FILE = os.path.join(VERIFIER_DIR, "cases.json")

def ensure_dir():
    os.makedirs(VERIFIER_DIR, exist_ok=True)

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

def load_cases():
    return _safe_load(CASES_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "cases": {}
    })

def save_cases(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(CASES_FILE, data)
