"""Simple in-memory per-IP sliding window rate limiter (stdlib only)."""

from __future__ import annotations

import threading
import time
from collections import defaultdict


class RateLimiter:
    """Sliding window rate limiter.

    Args:
        max_requests: Maximum requests allowed in the window.
        window_seconds: Window size in seconds.
    """

    def __init__(self, max_requests: int = 10, window_seconds: float = 60.0, max_keys: int = 4096) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.max_keys = max_keys
        self._requests: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def is_allowed(self, key: str) -> bool:
        """Return True if the request is allowed, False if rate limited."""
        now = time.monotonic()
        cutoff = now - self.window_seconds

        with self._lock:
            # Use .get so merely reading an unknown key doesn't create an entry.
            timestamps = [t for t in self._requests.get(key, ()) if t > cutoff]

            if len(timestamps) >= self.max_requests:
                self._requests[key] = timestamps
                return False

            timestamps.append(now)
            self._requests[key] = timestamps
            # Opportunistically drop keys whose entries have all expired so the
            # map stays bounded when many distinct client IPs are seen.
            if len(self._requests) > self.max_keys:
                self._evict_stale(cutoff)
            return True

    def _evict_stale(self, cutoff: float) -> None:
        stale = [k for k, ts in self._requests.items() if not any(t > cutoff for t in ts)]
        for k in stale:
            del self._requests[k]

    def reset(self) -> None:
        """Clear all tracking data (useful for testing)."""
        with self._lock:
            self._requests.clear()


# Shared limiter for draft generation endpoints
draft_limiter = RateLimiter(max_requests=10, window_seconds=60.0)


RATE_LIMIT_RESPONSE = {"detail": "Rate limit exceeded. Max 10 drafts/minute."}
