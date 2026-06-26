#!/usr/bin/env python3
import json
import os
from datetime import datetime

SCRAPER_DIR = os.path.expanduser("~/.openclaw/workspace/memory/scraper")
OUTPUT_DIR = os.path.join(SCRAPER_DIR, "output")
JOBS_FILE = os.path.join(SCRAPER_DIR, "jobs.json")

def write_json_if_missing(path, payload):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(SCRAPER_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    write_json_if_missing(JOBS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "jobs": {}
    })

    print("✓ Scraper storage initialized")
    print(f"  {JOBS_FILE}")
    print(f"  {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
