#!/usr/bin/env python3
import json
import os
from datetime import datetime

SCRAPER_DIR = os.path.expanduser("~/.openclaw/workspace/memory/scraper")
OUTPUT_DIR = os.path.join(SCRAPER_DIR, "output")
JOBS_FILE = os.path.join(SCRAPER_DIR, "jobs.json")

def ensure_dirs():
    os.makedirs(SCRAPER_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_jobs():
    ensure_dirs()
    if not os.path.exists(JOBS_FILE):
        return {
            "metadata": {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            },
            "jobs": {}
        }
    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_jobs(data):
    ensure_dirs()
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    tmp = JOBS_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, JOBS_FILE)
