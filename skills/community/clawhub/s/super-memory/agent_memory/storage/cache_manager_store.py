from __future__ import annotations

import os
import time
import threading
import logging
from collections import OrderedDict

logger = logging.getLogger(__name__)


class StoreCacheManager:
    _MAX_CACHE_SIZE = 10000

    def __init__(
        self,
        db_path: str,
        cache_max_size: int = None,
        cache_ttl_seconds: int = 300,
        cache_version_check_interval: float = 5.0,
    ):
        self._db_path = db_path
        self._cache_version_path = db_path + ".cache_ver"
        self._query_cache: OrderedDict = OrderedDict()
        self._cache_max_size = cache_max_size if cache_max_size is not None else self._MAX_CACHE_SIZE
        self._cache_ttl_seconds = cache_ttl_seconds
        self._thread_lock = threading.Lock()
        self._cache_hits = 0
        self._cache_misses = 0
        self._stats = {"reads": 0, "writes": 0, "cache_hits": 0, "cache_misses": 0}
        self._local_cache_version = 0
        self._cache_version_check_interval = cache_version_check_interval
        self._last_cache_version_check = 0.0

    @property
    def stats(self) -> dict:
        return self._stats

    def invalidate_cache(self, key_prefix: str = None):
        with self._thread_lock:
            if key_prefix:
                keys_to_remove = [k for k in self._query_cache if k.startswith(key_prefix)]
                for k in keys_to_remove:
                    del self._query_cache[k]
            else:
                self._query_cache.clear()
        try:
            ver = 0
            if os.path.exists(self._cache_version_path):
                try:
                    with open(self._cache_version_path, "r") as f:
                        ver = int(f.read().strip())
                except (ValueError, IOError) as e:
                    logger.debug("store: cache version read: %s", e)
            ver += 1
            tmp_path = self._cache_version_path + ".tmp"
            with open(tmp_path, "w") as f:
                f.write(str(ver))
            os.replace(tmp_path, self._cache_version_path)
            self._local_cache_version = ver
        except Exception as e:
            logger.warning("store: %s", e)

    def cache_get(self, key: str):
        try:
            now = time.monotonic()
            if now - self._last_cache_version_check >= self._cache_version_check_interval:
                self._last_cache_version_check = now
                if os.path.exists(self._cache_version_path):
                    with open(self._cache_version_path, "r") as f:
                        remote_ver = int(f.read().strip())
                    if remote_ver > self._local_cache_version:
                        with self._thread_lock:
                            self._query_cache.clear()
                        self._local_cache_version = remote_ver
        except Exception as e:
            logger.warning("store: %s", e)
        with self._thread_lock:
            self._stats["reads"] += 1
            item = self._query_cache.get(key)
            if item is None:
                self._stats["cache_misses"] += 1
                self._cache_misses += 1
                return None
            if not isinstance(item, tuple):
                self._stats["cache_hits"] += 1
                self._cache_hits += 1
                return item
            value, expire_at = item
            if expire_at and time.monotonic() > expire_at:
                del self._query_cache[key]
                self._stats["cache_misses"] += 1
                self._cache_misses += 1
                return None
            self._query_cache.move_to_end(key)
            self._stats["cache_hits"] += 1
            self._cache_hits += 1
            return value

    def cache_set(self, key: str, value, ttl_seconds: int = None):
        with self._thread_lock:
            if key not in self._query_cache and len(self._query_cache) >= self._cache_max_size:
                self._evict_expired()
                if len(self._query_cache) >= self._cache_max_size:
                    keys_to_remove = list(self._query_cache.keys())[:self._cache_max_size // 5]
                    for k in keys_to_remove:
                        del self._query_cache[k]
            ttl = ttl_seconds if ttl_seconds is not None else self._cache_ttl_seconds
            expire_at = time.monotonic() + ttl if ttl else None
            self._query_cache[key] = (value, expire_at)
            self._query_cache.move_to_end(key)

    def _evict_expired(self):
        now = time.monotonic()
        expired = [k for k, (_, exp) in self._query_cache.items() if exp and now > exp]
        for k in expired:
            del self._query_cache[k]

    def increment_writes(self):
        self._stats["writes"] += 1

    def get_io_stats(self, has_fts: bool, max_memories: int) -> dict:
        with self._thread_lock:
            stats = dict(self._stats)
        total = stats["reads"] + stats["cache_misses"]
        stats["cache_hit_rate"] = stats["cache_hits"] / total if total > 0 else 0
        stats["has_fts"] = has_fts
        stats["max_memories"] = max_memories
        stats["cache_size"] = len(self._query_cache)
        stats["cache_max_size"] = self._cache_max_size
        stats["cache_hits_direct"] = self._cache_hits
        stats["cache_misses_direct"] = self._cache_misses
        return stats
