#!/usr/bin/env python3
import json
import os
from datetime import datetime

VERIFIER_DIR = os.path.expanduser("~/.openclaw/workspace/memory/verifier")
CASES_FILE = os.path.join(VERIFIER_DIR, "cases.json")

def write_json_if_missing(path, payload):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(VERIFIER_DIR, exist_ok=True)
    write_json_if_missing(CASES_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "cases": {}
    })
    print("✓ Verifier storage initialized")
    print(f"  {CASES_FILE}")

if __name__ == "__main__":
    main()
