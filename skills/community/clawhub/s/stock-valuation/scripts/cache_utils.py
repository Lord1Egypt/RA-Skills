#!/usr/bin/env python3
"""File-based cache utilities for stock valuation data. TTL: 4h fundamentals, 1h prices."""
import argparse
import hashlib
import json
import os
import sys
import time

CACHE_DIR = "/tmp/stock_valuation_cache"

# TTL in seconds
TTL = {
    "fundamentals": 4 * 3600,  # 4 hours
    "prices": 1 * 3600,        # 1 hour
    "default": 2 * 3600,       # 2 hours
}


def _ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)


def _cache_path(key):
    safe_key = hashlib.sha256(key.encode()).hexdigest()[:16]
    # Also keep a readable prefix
    prefix = key.replace("/", "_").replace(":", "_")[:40]
    return os.path.join(CACHE_DIR, f"{prefix}_{safe_key}.json")


def _get_ttl(category):
    return TTL.get(category, TTL["default"])


def cache_get(key, category="default"):
    """Retrieve a cached value. Returns None if missing or expired."""
    path = _cache_path(key)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            entry = json.load(f)
        ttl = _get_ttl(category)
        if time.time() - entry.get("timestamp", 0) > ttl:
            os.remove(path)
            return None
        return entry.get("data")
    except (json.JSONDecodeError, OSError):
        return None


def cache_set(key, data, category="default"):
    """Store a value in the cache."""
    _ensure_cache_dir()
    path = _cache_path(key)
    entry = {
        "key": key,
        "category": category,
        "timestamp": time.time(),
        "data": data,
    }
    with open(path, "w") as f:
        json.dump(entry, f)
    return path


def cache_clear(key=None):
    """Clear a specific key or the entire cache."""
    if key:
        path = _cache_path(key)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
    else:
        count = 0
        if os.path.exists(CACHE_DIR):
            for f in os.listdir(CACHE_DIR):
                fp = os.path.join(CACHE_DIR, f)
                if os.path.isfile(fp):
                    os.remove(fp)
                    count += 1
        return count


def cache_stats():
    """Return cache statistics."""
    if not os.path.exists(CACHE_DIR):
        return {"entries": 0, "size_bytes": 0}
    entries = 0
    total_size = 0
    expired = 0
    for f in os.listdir(CACHE_DIR):
        fp = os.path.join(CACHE_DIR, f)
        if os.path.isfile(fp):
            entries += 1
            total_size += os.path.getsize(fp)
            try:
                with open(fp, "r") as fh:
                    entry = json.load(fh)
                cat = entry.get("category", "default")
                ttl = _get_ttl(cat)
                if time.time() - entry.get("timestamp", 0) > ttl:
                    expired += 1
            except (json.JSONDecodeError, OSError):
                expired += 1
    return {"entries": entries, "expired": expired, "size_bytes": total_size}


def main():
    parser = argparse.ArgumentParser(description="Cache utilities for stock valuation data.")
    sub = parser.add_subparsers(dest="command", help="Cache command")

    get_p = sub.add_parser("get", help="Get a cached value")
    get_p.add_argument("key", help="Cache key")
    get_p.add_argument("--category", default="default", help="Cache category (fundamentals/prices/default)")

    set_p = sub.add_parser("set", help="Set a cache value (reads JSON from stdin)")
    set_p.add_argument("key", help="Cache key")
    set_p.add_argument("--category", default="default", help="Cache category (fundamentals/prices/default)")

    clear_p = sub.add_parser("clear", help="Clear cache")
    clear_p.add_argument("--key", default=None, help="Specific key to clear (omit for all)")

    sub.add_parser("stats", help="Show cache statistics")

    args = parser.parse_args()

    if args.command == "get":
        result = cache_get(args.key, args.category)
        if result is None:
            print(json.dumps({"hit": False, "key": args.key}))
        else:
            print(json.dumps({"hit": True, "key": args.key, "data": result}, default=str))

    elif args.command == "set":
        raw = sys.stdin.read().strip()
        if not raw:
            print("ERROR: No data on stdin", file=sys.stderr)
            sys.exit(1)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print("ERROR: Invalid JSON on stdin", file=sys.stderr)
            sys.exit(1)
        path = cache_set(args.key, data, args.category)
        print(json.dumps({"stored": True, "key": args.key, "path": path}))

    elif args.command == "clear":
        result = cache_clear(args.key)
        if args.key:
            print(json.dumps({"cleared": result, "key": args.key}))
        else:
            print(json.dumps({"cleared": True, "entries_removed": result}))

    elif args.command == "stats":
        print(json.dumps(cache_stats(), indent=2))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
