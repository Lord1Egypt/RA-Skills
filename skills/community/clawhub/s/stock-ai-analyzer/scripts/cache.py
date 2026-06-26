#!/usr/bin/env python3
"""Simple file-based JSON cache with TTL support."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Optional


class JsonTTLCache:
    """Simple file-based JSON cache with TTL support."""

    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        return self.root / f"{hashlib.sha256(key.encode()).hexdigest()}.json"

    def get(self, key: str, ttl_seconds: int) -> Optional[Any]:
        path = self._path(key)
        if not path.exists():
            return None
        if time.time() - path.stat().st_mtime > ttl_seconds:
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None

    def set(self, key: str, value: Any) -> Any:
        path = self._path(key)
        path.write_text(json.dumps(value, ensure_ascii=False, default=str), encoding="utf-8")
        return value
