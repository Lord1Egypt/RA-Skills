#!/usr/bin/env python3
"""Tushare Pro client factory and retry proxy."""

from __future__ import annotations

import os
import time
from typing import Any, Callable, Dict, Optional

try:
    import tushare as ts
except ImportError as exc:
    raise RuntimeError("Missing dependency: install tushare before using this fetcher.") from exc


def get_tushare_token() -> str:
    """Read TUSHARE_TOKEN from the environment or cwd/.env."""
    token = os.environ.get("TUSHARE_TOKEN", "").strip()
    if token:
        return token

    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        return ""

    with open(env_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            if key.strip() == "TUSHARE_TOKEN":
                return value.strip().strip('"').strip("'")
    return ""


def get_tushare_pro(token: Optional[str] = None):
    """Create a Tushare Pro client."""
    resolved_token = token or get_tushare_token()
    if not resolved_token:
        raise RuntimeError("Missing TUSHARE_TOKEN. Set it in the environment or cwd/.env.")
    return ts.pro_api(resolved_token)


class _TushareProxy:
    """Lightweight retry wrapper around Tushare Pro API.

    Intercepts every method call on the underlying ``pro`` object and adds
    exponential-backoff retry for transient errors (timeout, connection reset,
    rate-limit).  Auth and parameter errors are never retried.
    """

    def __init__(self, pro: Any, *, attempts: int = 2, backoff: float = 1.0):
        self._pro = pro
        self._attempts = attempts
        self._backoff = backoff
        self._cache: Dict[str, Callable] = {}

    @staticmethod
    def _is_retriable(exc: Exception) -> bool:
        msg = str(exc).lower()
        # Auth / parameter / permission errors — never retry
        if any(k in msg for k in ("invalid", "unauthorized", "token", "param", "argument", "no data", "permission")):
            return False
        # Transient network / server errors — retry
        return any(k in msg for k in (
            "timeout", "timed out", "connection", "reset", "refused",
            "too many requests", "rate limit", "quota", "503", "502", "504",
            "temporary", "unavailable", "busy",
        ))

    def __getattr__(self, name: str) -> Callable:
        if name not in self._cache:
            original = getattr(self._pro, name)

            def wrapper(*args: Any, **kwargs: Any) -> Any:
                last_exc: Optional[Exception] = None
                for i in range(self._attempts):
                    try:
                        return original(*args, **kwargs)
                    except Exception as exc:
                        last_exc = exc
                        if not self._is_retriable(exc):
                            raise
                        if i < self._attempts - 1:
                            time.sleep(self._backoff * (2 ** i))
                raise last_exc or RuntimeError(f"Tushare {name} failed after {self._attempts} attempts")

            self._cache[name] = wrapper
        return self._cache[name]
