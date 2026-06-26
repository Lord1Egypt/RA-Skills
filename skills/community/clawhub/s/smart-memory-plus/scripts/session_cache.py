#!/usr/bin/env python3
"""
session_cache.py — Session-scoped temporary memory cache.
Safe alternative to shell-based session_cache.sh (no shell injection).
Usage:
  session_cache.py set <key> <value>
  session_cache.py get <key>
  session_cache.py list
  session_cache.py remove <key>
  session_cache.py clear
"""

import json
import os
import re
import sys
from pathlib import Path

SESSION_ID = os.environ.get("OPENCLAW_SESSION_ID", "default")
SAFE_ID = re.sub(r"[^a-zA-Z0-9_-]", "", SESSION_ID) or "default"
CACHE_FILE = Path(f"/tmp/openclaw-session-cache-{SAFE_ID}.json")

# Sensitive patterns — refuse to cache
SENSITIVE_PATTERNS = [
    re.compile(r"(?:password|passwd|pwd)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"(?:api[_-]?key|token|secret|bearer)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"clh_[A-Za-z0-9]{30,}", re.IGNORECASE),
    re.compile(r"sk-[A-Za-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"ghp_[A-Za-z0-9]{30,}", re.IGNORECASE),
]


def check_sensitive(text: str) -> str | None:
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(text):
            return f"Refused: matches sensitive pattern"
    return None


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_cache(data: dict):
    CACHE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_set(key: str, value: str):
    err = check_sensitive(value)
    if err:
        print(err)
        return
    data = load_cache()
    data[key] = value
    save_cache(data)
    print(f"Set: {key} = {value}")


def cmd_get(key: str):
    data = load_cache()
    print(data.get(key, ""))


def cmd_list():
    data = load_cache()
    if not data:
        print("(empty)")
    else:
        for k, v in data.items():
            print(f"{k}: {v}")


def cmd_remove(key: str):
    data = load_cache()
    data.pop(key, None)
    save_cache(data)
    print(f"Removed: {key}")


def cmd_clear():
    save_cache({})
    print("Cache cleared.")


def main():
    if len(sys.argv) < 2:
        print("Usage: session_cache.py {set|get|list|remove|clear} [key] [value]")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "set" and len(args) >= 2:
        cmd_set(args[0], " ".join(args[1:]))
    elif cmd == "get" and len(args) >= 1:
        cmd_get(args[0])
    elif cmd == "list":
        cmd_list()
    elif cmd == "remove" and len(args) >= 1:
        cmd_remove(args[0])
    elif cmd == "clear":
        cmd_clear()
    else:
        print("Usage: session_cache.py {set|get|list|remove|clear} [key] [value]")
        sys.exit(1)


if __name__ == "__main__":
    main()
