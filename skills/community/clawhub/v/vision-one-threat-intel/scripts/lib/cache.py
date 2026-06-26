"""Simple file-based session cache to avoid redundant API calls."""

import hashlib
import json
import os
import time

CACHE_DIR = os.path.join(os.environ.get("TMPDIR", "/tmp"), "v1ti_cache")
DEFAULT_TTL = 300  # 5 minutes


class SessionCache:
    def __init__(self, ttl=DEFAULT_TTL):
        self.ttl = ttl
        os.makedirs(CACHE_DIR, exist_ok=True)

    def _key_path(self, key):
        h = hashlib.sha256(key.encode()).hexdigest()[:16]
        return os.path.join(CACHE_DIR, f"{h}.json")

    def _make_key(self, endpoint, params):
        parts = [endpoint]
        if params:
            for k in sorted(params):
                parts.append(f"{k}={params[k]}")
        return "|".join(parts)

    def get(self, endpoint, params=None):
        key = self._make_key(endpoint, params)
        path = self._key_path(key)
        try:
            with open(path) as f:
                entry = json.load(f)
            if time.time() - entry["ts"] < self.ttl:
                return entry["data"]
            os.unlink(path)
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass
        return None

    def set(self, endpoint, params, data):
        key = self._make_key(endpoint, params)
        path = self._key_path(key)
        with open(path, "w") as f:
            json.dump({"ts": time.time(), "data": data}, f)

    def clear(self):
        try:
            for fname in os.listdir(CACHE_DIR):
                os.unlink(os.path.join(CACHE_DIR, fname))
        except FileNotFoundError:
            pass
