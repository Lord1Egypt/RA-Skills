#!/usr/bin/env python3
"""
Score cache — persists last known results for all tracked teams.
Used by ticker.py and live_monitor.py.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

CACHE_FILE = Path(__file__).parent.parent / ".score_cache.json"


def load_cache() -> dict:
    """Load full cache from disk."""
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except Exception:
            return {}
    return {}


def save_cache(cache: dict):
    """Write cache to disk."""
    CACHE_FILE.write_text(json.dumps(cache, indent=2))


def write_to_cache(team_key: str, result: str, source: str = "web_search"):
    """Store a result in the cache (creates or updates entry)."""
    cache = load_cache()
    now = datetime.now(timezone.utc)
    cache[team_key] = {
        "last_result": result,
        "match_date": now.strftime("%Y-%m-%d"),
        "source": source,
        "cached_at": now.isoformat(),
    }
    save_cache(cache)


def read_from_cache(team_key: str) -> dict | None:
    """Get cached entry for a team, or None if not cached."""
    return load_cache().get(team_key)


def format_cached_result(team_key: str) -> str:
    """Return a human-readable 'Last result: …' string, or empty string if no cache."""
    entry = read_from_cache(team_key)
    if not entry:
        return ""
    result = entry.get("last_result", "")
    date_str = entry.get("match_date", "")
    if date_str:
        try:
            date_label = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.")
        except ValueError:
            date_label = date_str
        return f"Last result: {result} ({date_label})"
    return f"Last result: {result}"
