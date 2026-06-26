"""Async wrapper for RecallEngine.

⚠️ ARCHITECTURE NOTE: This module wraps synchronous SQLite operations
with asyncio's run_in_executor(). It is NOT true async I/O.

Implications:
- GIL contention: SQLite operations still block the event loop's thread pool
- Connection model: Each thread pool worker creates its own SQLite connection
- Transaction isolation: Operations in different thread pool workers CANNOT
  share transactions. Methods that require shared transactions will NOT work
  correctly in async mode.
- Performance: This provides concurrency (other coroutines can run while
  waiting for SQLite), but NOT parallelism (SQLite is still single-writer).

For true async I/O with SQLite, use aiosqlite.
For high-concurrency production workloads, consider PostgreSQL with asyncpg.

Recommended usage:
- FastAPI endpoints: Use this wrapper for non-blocking API responses
- Background tasks: Use synchronous RecallEngine directly (no event loop needed)
- High concurrency: Use PostgreSQL backend with asyncpg
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import re
import threading
import time
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from typing import Any, AsyncIterator, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class RecallMetrics:
    """Latency, throughput, and cache tracking for the async recall engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self.total_searches: int = 0
        self._latency_samples: List[float] = []
        self._max_samples = 10_000
        self.cache_hits: int = 0
        self.cache_misses: int = 0

    def record(self, latency_ms: float, cache_hit: bool = False):
        with self._lock:
            self.total_searches += 1
            self._latency_samples.append(latency_ms)
            if len(self._latency_samples) > self._max_samples:
                self._latency_samples = self._latency_samples[-self._max_samples:]
            if cache_hit:
                self.cache_hits += 1
            else:
                self.cache_misses += 1

    @property
    def avg_latency_ms(self) -> float:
        with self._lock:
            if not self._latency_samples:
                return 0.0
            return round(sum(self._latency_samples) / len(self._latency_samples), 4)

    def _percentile(self, pct: float) -> float:
        with self._lock:
            if not self._latency_samples:
                return 0.0
            sorted_samples = sorted(self._latency_samples)
            idx = int(len(sorted_samples) * pct)
            if idx >= len(sorted_samples):
                idx = len(sorted_samples) - 1
            return round(sorted_samples[idx], 4)

    @property
    def p50_latency_ms(self) -> float:
        return self._percentile(0.50)

    @property
    def p95_latency_ms(self) -> float:
        return self._percentile(0.95)

    @property
    def p99_latency_ms(self) -> float:
        return self._percentile(0.99)

    @property
    def cache_hit_ratio(self) -> float:
        with self._lock:
            total = self.cache_hits + self.cache_misses
            if total == 0:
                return 0.0
            return round(self.cache_hits / total, 4)

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "total_searches": self.total_searches,
                "avg_latency_ms": self.avg_latency_ms,
                "p50_latency_ms": self.p50_latency_ms,
                "p95_latency_ms": self.p95_latency_ms,
                "p99_latency_ms": self.p99_latency_ms,
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "cache_hit_ratio": self.cache_hit_ratio,
                "sample_count": len(self._latency_samples),
            }

    def reset(self):
        with self._lock:
            self.total_searches = 0
            self._latency_samples.clear()
            self.cache_hits = 0
            self.cache_misses = 0


class RecallCache:
    """TTL-based in-memory LRU cache for frequent recall queries."""

    def __init__(self, max_size: int = 128, default_ttl: int = 60):
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._lock = threading.Lock()
        self._store: OrderedDict[str, Tuple[float, Any]] = OrderedDict()

    def _make_key(self, query: str, top_k: int, filters: dict) -> str:
        raw = json.dumps(
            {"q": query, "k": top_k, "f": filters},
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, query_hash: str) -> Optional[Any]:
        with self._lock:
            entry = self._store.get(query_hash)
            if entry is None:
                return None
            expires_at, value = entry
            if time.monotonic() > expires_at:
                del self._store[query_hash]
                return None
            self._store.move_to_end(query_hash)
            return value

    def set(self, query_hash: str, results: Any, ttl_seconds: Optional[int] = None):
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        expires_at = time.monotonic() + ttl
        with self._lock:
            if query_hash in self._store:
                del self._store[query_hash]
            self._store[query_hash] = (expires_at, results)
            self._store.move_to_end(query_hash)
            self._evict_lru()

    def invalidate(self, pattern: str):
        compiled = re.compile(pattern)
        with self._lock:
            keys_to_delete = [k for k in self._store if compiled.search(k)]
            for k in keys_to_delete:
                del self._store[k]

    def clear(self):
        with self._lock:
            self._store.clear()

    def _evict_lru(self):
        while len(self._store) > self._max_size:
            self._store.popitem(last=False)

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._store)


class AsyncRecallEngine:
    """Async wrapper around RecallEngine with streaming, metrics, and caching.

    Uses ``asyncio`` + ``ThreadPoolExecutor`` to run blocking recall
    operations asynchronously.  Compatible with Python 3.7+.

    Parameters
    ----------
    recall_engine : recall.RecallEngine
        An already-configured recall engine instance.
    min_workers : int
        Minimum number of threads kept warm in the pool (default 2).
    max_workers : int
        Maximum number of threads the pool may grow to (default 8).
    async_store : AsyncMemoryStore, optional
        If passed, used for direct database queries through the async layer.
    enable_cache : bool
        Whether to enable the TTL-based result cache (default True).
    cache_max_size : int
        Maximum number of cached results (default 128).
    cache_ttl : int
        Default cache TTL in seconds (default 60).

    Examples
    --------
    >>> from recall import RecallEngine
    >>> engine = RecallEngine(store, encoder, embedding_store=emb)
    >>> async with AsyncRecallEngine(engine, enable_cache=True) as rec:
    ...     results = await rec.search("hello world", top_k=10)
    ...     async for item in rec.search_stream("hello world", top_k=5):
    ...         print(item)
    ...     print(rec.metrics.snapshot())
    """

    def __init__(
        self,
        recall_engine,
        min_workers: int = 2,
        max_workers: int = 8,
        async_store = None,
        enable_cache: bool = True,
        cache_max_size: int = 128,
        cache_ttl: int = 60,
    ):
        self._engine = recall_engine
        self._async_store = async_store
        self._min_workers = max(1, int(min_workers))
        self._max_workers = max(self._min_workers, int(max_workers))
        self._executor: Optional[ThreadPoolExecutor] = None
        self._closed = False

        self._metrics = RecallMetrics()
        self._cache = RecallCache(max_size=cache_max_size, default_ttl=cache_ttl) if enable_cache else None

        self._stream_delay: float = 0.02  # seconds between streamed results

    @property
    def engine(self):
        return self._engine

    @property
    def metrics(self) -> RecallMetrics:
        return self._metrics

    @property
    def closed(self) -> bool:
        return self._closed

    # ── internal helpers ─────────────────────────────────────────────────

    def _ensure_executor(self):
        if self._closed:
            raise RuntimeError("AsyncRecallEngine is closed")
        if self._executor is None:
            self._executor = ThreadPoolExecutor(max_workers=self._max_workers)
            for _ in range(self._min_workers):
                self._executor.submit(lambda: None)

    async def _run_async(self, fn, *args, **kwargs):
        self._ensure_executor()
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self._executor,
            lambda: fn(*args, **kwargs),
        )

    @staticmethod
    def _to_score_results(recall_output: dict, query: str) -> List[dict]:
        items = []
        for mem in recall_output.get("primary", []):
            item = dict(mem)
            item["_score"] = mem.get("_rank_score", mem.get("_rrf_score", 0))
            item["_query"] = query
            item["_mode"] = recall_output.get("search_mode", "unknown")
            item["_intent"] = recall_output.get("intent", "general")
            items.append(item)
        return items

    @staticmethod
    def _build_recall_kwargs(
        query: str,
        top_k: int,
        filters: dict,
        agent_id: Optional[str] = None,
    ) -> dict:
        kwargs: Dict[str, Any] = {
            "query": query,
            "limit": top_k,
        }
        field_map = {
            "time_from": "time_from",
            "time_to": "time_to",
            "person_id": "person_id",
            "nature_code": "nature_code",
            "topic_path": "topic_path",
            "tool_id": "tool_id",
            "knowledge_id": "knowledge_id",
            "importance": "importance",
            "keyword": "keyword",
            "significance": "significance",
            "team_id": "team_id",
        }
        for src, dst in field_map.items():
            if src in filters:
                kwargs[dst] = filters[src]
        if agent_id:
            kwargs["query_agent_id"] = agent_id
        elif "query_agent_id" in filters:
            kwargs["query_agent_id"] = filters["query_agent_id"]
        return kwargs

    # ── public search methods ────────────────────────────────────────────

    async def search(
        self,
        query: str,
        top_k: int = 10,
        **filters,
    ) -> List[dict]:
        cache_hit = False
        cache_key = None

        if self._cache:
            cache_key = self._cache._make_key(query, top_k, filters)
            cached = self._cache.get(cache_key)
            if cached is not None:
                cache_hit = True
                self._metrics.record(0.0, cache_hit=True)
                return cached

        start = time.perf_counter_ns()
        kwargs = self._build_recall_kwargs(query, top_k, filters)

        if self._async_store and hasattr(self._engine, "store"):
            try:
                store_query_results = await self._async_store.query(
                    keyword=query,
                    limit=top_k,
                    **{k: v for k, v in filters.items()
                       if k in ("time_from", "time_to", "person_id", "importance")},
                )
                scored = []
                for mem in store_query_results:
                    item = dict(mem)
                    item["_score"] = 0.5
                    item["_query"] = query
                    item["_mode"] = "async_store_fallback"
                    item["_intent"] = "general"
                    scored.append(item)
                if scored:
                    elapsed = (time.perf_counter_ns() - start) / 1_000_000
                    self._metrics.record(elapsed, cache_hit=False)
                    if self._cache and cache_key:
                        self._cache.set(cache_key, scored)
                    return scored
            except Exception:
                logger.debug("Async store fallback failed, using recall engine", exc_info=True)

        output = await self._run_async(
            self._engine.recall,
            **kwargs,
        )
        results = self._to_score_results(output, query)
        elapsed = (time.perf_counter_ns() - start) / 1_000_000
        self._metrics.record(elapsed, cache_hit=False)

        if self._cache and cache_key:
            self._cache.set(cache_key, results)

        return results

    async def search_stream(
        self,
        query: str,
        top_k: int = 10,
        **filters,
    ) -> AsyncIterator[dict]:
        results = await self.search(query, top_k=top_k, **filters)
        for i, item in enumerate(results):
            item["_stream_index"] = i
            item["_stream_total"] = len(results)
            yield item
            if i < len(results) - 1:
                await asyncio.sleep(self._stream_delay)

    async def multi_search(
        self,
        queries: List[str],
        top_k: int = 10,
        **filters,
    ) -> Dict[str, List[dict]]:
        tasks = {
            q: self.search(q, top_k=top_k, **filters)
            for q in queries
        }
        gathered = await asyncio.gather(*tasks.values(), return_exceptions=True)
        result: Dict[str, List[dict]] = {}
        for (query,), output in zip(tasks.items(), gathered):
            if isinstance(output, Exception):
                logger.warning("multi_search: query '%s' failed: %s", query, output)
                result[query] = []
            else:
                result[query] = output
        return result

    async def batch_recall(
        self,
        agent_id: str,
        queries: List[str],
        top_k: int = 10,
        **filters,
    ) -> Dict[str, List[dict]]:
        filters_with_agent = dict(filters)
        filters_with_agent["query_agent_id"] = agent_id

        tasks = {
            q: self.search(q, top_k=top_k, **filters_with_agent)
            for q in queries
        }
        gathered = await asyncio.gather(*tasks.values(), return_exceptions=True)
        result: Dict[str, List[dict]] = {}
        for (query,), output in zip(tasks.items(), gathered):
            if isinstance(output, Exception):
                logger.warning("batch_recall: query '%s' failed: %s", query, output)
                result[query] = []
            else:
                result[query] = output
        return result

    # ── health / close ───────────────────────────────────────────────────

    async def health_check(self) -> Dict[str, Any]:
        try:
            stats = self._engine.get_stats() if hasattr(self._engine, "get_stats") else {}
            metrics = self._metrics.snapshot()
            return {
                "status": "ok",
                "engine_type": type(self._engine).__name__,
                "cache_enabled": self._cache is not None,
                "cache_size": self._cache.size if self._cache else 0,
                "engine_stats": stats,
                "metrics": metrics,
                "closed": self._closed,
            }
        except Exception as exc:
            logger.error("Health check failed: %s", exc)
            return {"status": "error", "error": str(exc)}

    async def close(self):
        if self._closed:
            return
        self._closed = True
        if self._executor is not None:
            self._executor.shutdown(wait=True)
            self._executor = None
        if self._cache:
            self._cache.clear()

    # ── context manager ──────────────────────────────────────────────────

    async def __aenter__(self):
        self._ensure_executor()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False