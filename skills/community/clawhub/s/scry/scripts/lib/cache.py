"""File-based caching for SCRY skill."""

import hashlib
import json
import os
import time
from typing import Any, Dict, Optional

CACHE_DIR = os.path.expanduser("~/.cache/scry")
CACHE_TTL = 24 * 3600  # 24 hours


def _cache_key(topic: str, from_date: str, to_date: str, sources: str = "") -> str:
    raw = f"{topic}|{from_date}|{to_date}|{sources}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _cache_path(key: str) -> str:
    return os.path.join(CACHE_DIR, f"{key}.json")


def load_cache(topic: str, from_date: str, to_date: str, sources: str = "") -> Optional[Dict[str, Any]]:
    key = _cache_key(topic, from_date, to_date, sources)
    path = _cache_path(key)
    if not os.path.isfile(path):
        return None
    try:
        mtime = os.path.getmtime(path)
        age = time.time() - mtime
        if age > CACHE_TTL:
            return None
        with open(path) as f:
            data = json.load(f)
        data["_cache_age_hours"] = round(age / 3600, 1)
        return data
    except (json.JSONDecodeError, OSError):
        return None


def save_cache(topic: str, from_date: str, to_date: str, data: Dict[str, Any], sources: str = "") -> None:
    key = _cache_key(topic, from_date, to_date, sources)
    path = _cache_path(key)
    os.makedirs(CACHE_DIR, exist_ok=True)
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except OSError:
        pass
