"""Async wrapper for MemoryStore.

⚠️ ARCHITECTURE NOTE: This module wraps synchronous SQLite operations
with asyncio's run_in_executor(). It is NOT true async I/O.

Implications:
- GIL contention: SQLite operations still block the event loop's thread pool
- Connection model: Each thread pool worker creates its own SQLite connection
- Transaction isolation: Operations in different thread pool workers CANNOT
  share transactions. Methods like insert_memory_in_txn() that require shared
  transactions will NOT work correctly in async mode.
- Performance: This provides concurrency (other coroutines can run while
  waiting for SQLite), but NOT parallelism (SQLite is still single-writer).

For true async I/O with SQLite, use aiosqlite.
For high-concurrency production workloads, consider PostgreSQL with asyncpg.

Recommended usage:
- FastAPI endpoints: Use this wrapper for non-blocking API responses
- Background tasks: Use synchronous MemoryStore directly (no event loop needed)
- High concurrency: Use PostgreSQL backend with asyncpg
"""
from __future__ import annotations

import asyncio
import logging
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

from .storage.base import AbstractMemoryStore

logger = logging.getLogger(__name__)


class AsyncMemoryStore:
    """Async wrapper around any AbstractMemoryStore implementation.

    Uses ``asyncio`` event loop + ``ThreadPoolExecutor`` to run blocking DB
    operations asynchronously.  Compatible with Python 3.7+.

    Parameters
    ----------
    store : AbstractMemoryStore
        An already-configured store instance (e.g. ``SqliteMemoryStore``).
    min_workers : int
        Minimum number of threads kept warm in the pool (default 2).
    max_workers : int
        Maximum number of threads the pool may grow to (default 8).

    Examples
    --------
    >>> from storage.sqlite_store import SqliteMemoryStore
    >>> store = SqliteMemoryStore("memory.db")
    >>> async with AsyncMemoryStore(store, min_workers=2, max_workers=8) as astore:
    ...     await astore.insert_memory(...)
    ...     results = await astore.query(keyword="hello")
    ...     print(astore.metrics)
    """

    def __init__(
        self,
        store: AbstractMemoryStore,
        min_workers: int = 2,
        max_workers: int = 8,
    ):
        if not isinstance(store, AbstractMemoryStore):
            raise TypeError(
                f"store must be an AbstractMemoryStore instance, got {type(store).__name__}"
            )
        self._store = store
        self._min_workers = max(1, int(min_workers))
        self._max_workers = max(self._min_workers, int(max_workers))
        self._executor: Optional[ThreadPoolExecutor] = None
        self._closed = False

        self._metrics_lock = threading.Lock()
        self._total_ops: int = 0
        self._total_latency_ns: int = 0
        self._op_counts: Dict[str, int] = {}

    # ── public properties ────────────────────────────────────────────────

    @property
    def store(self) -> AbstractMemoryStore:
        return self._store

    @property
    def metrics(self) -> Dict[str, Any]:
        with self._metrics_lock:
            avg_latency_ms = (
                (self._total_latency_ns / self._total_ops / 1_000_000)
                if self._total_ops > 0
                else 0.0
            )
            return {
                "total_ops": self._total_ops,
                "avg_latency_ms": round(avg_latency_ms, 4),
                "op_counts": dict(self._op_counts),
                "pool_utilization": self._pool_utilization(),
                "closed": self._closed,
            }

    @property
    def closed(self) -> bool:
        return self._closed

    # ── internal helpers ─────────────────────────────────────────────────

    def _ensure_executor(self):
        if self._closed:
            raise RuntimeError("AsyncMemoryStore is closed")
        if self._executor is None:
            self._executor = ThreadPoolExecutor(max_workers=self._max_workers)
            for _ in range(self._min_workers):
                self._executor.submit(lambda: None)

    def _pool_utilization(self) -> float:
        if self._executor is None:
            return 0.0
        try:
            qsize = self._executor._work_queue.qsize()
        except (AttributeError, RuntimeError):
            qsize = -1
        if qsize < 0:
            return 0.0
        return round(min(1.0, qsize / self._max_workers), 4)

    async def _run_async(self, op_name: str, fn, *args, **kwargs):
        self._ensure_executor()
        loop = asyncio.get_running_loop()
        start = time.perf_counter_ns()
        try:
            result = await loop.run_in_executor(
                self._executor,
                lambda: fn(*args, **kwargs)
            )
            return result
        finally:
            elapsed = time.perf_counter_ns() - start
            with self._metrics_lock:
                self._total_ops += 1
                self._total_latency_ns += elapsed
                self._op_counts[op_name] = self._op_counts.get(op_name, 0) + 1

    # ── async CRUD ───────────────────────────────────────────────────────

    async def insert_memory(
        self,
        memory_id: str,
        time_id: str,
        time_ts: int,
        person_id: str,
        nature_id: str,
        content: str,
        content_hash: str,
        topics: List[str],
        tools: List[str],
        knowledge_types: List[str],
        importance: str,
        valence: float,
        arousal: float,
        dominance: float,
        significance: str,
        confidence: float,
        primary_emotions: str,
        compound_emotions: str,
        owner_agent_id: str,
        visibility: str,
        **kwargs,
    ) -> str:
        return await self._run_async(
            "insert_memory",
            self._store.insert_memory,
            memory_id, time_id, time_ts, person_id, nature_id,
            content, content_hash, topics, tools, knowledge_types,
            importance, valence, arousal, dominance, significance,
            confidence, primary_emotions, compound_emotions,
            owner_agent_id, visibility, **kwargs,
        )

    async def get_memory(self, memory_id: str) -> Optional[dict]:
        return await self._run_async(
            "get_memory", self._store.get_memory, memory_id,
        )

    async def update_memory(self, memory_id: str, **fields):
        return await self._run_async(
            "update_memory", self._store.update_memory, memory_id, **fields,
        )

    async def delete_memory(self, memory_id: str, soft: bool = True):
        return await self._run_async(
            "delete_memory", self._store.delete_memory, memory_id, soft,
        )

    async def query(
        self,
        time_from: int = None,
        time_to: int = None,
        person_id: str = None,
        nature_id: str = None,
        topic_path: str = None,
        tool_id: str = None,
        knowledge_id: str = None,
        importance: str = None,
        keyword: str = None,
        significance: str = None,
        limit: int = 20,
        offset: int = 0,
        owner_agent_id: str = None,
        visibility: str = None,
    ) -> List[dict]:
        return await self._run_async(
            "query",
            self._store.query,
            time_from, time_to, person_id, nature_id,
            topic_path, tool_id, knowledge_id, importance,
            keyword, significance, limit, offset,
            owner_agent_id, visibility,
        )

    async def count(self) -> int:
        return await self._run_async(
            "count", self._store.count,
        )

    async def create_link(
        self,
        source_id: str,
        target_id: str,
        link_type: str,
        weight: float = 1.0,
        reason: str = "",
    ):
        return await self._run_async(
            "create_link",
            self._store.create_link,
            source_id, target_id, link_type, weight, reason,
        )

    async def get_linked(
        self, memory_id: str, link_type: str = None
    ) -> List[dict]:
        return await self._run_async(
            "get_linked", self._store.get_linked, memory_id, link_type,
        )

    async def insert_memory_in_txn(self, content, memory_id=None, **kwargs):
        """Insert memory within a shared transaction.

        ⚠️ WARNING: This method does NOT work correctly in async mode because
        each call may execute in a different thread pool worker, which has its
        own SQLite connection. Transactions cannot be shared across connections.

        Use insert_memory() instead for async contexts.
        """
        logger.warning(
            "insert_memory_in_txn() called in async mode — "
            "transaction isolation may be compromised. Use insert_memory() instead."
        )
        return await self._run_async("insert_memory_in_txn", self._store.insert_memory_in_txn, content, memory_id, **kwargs)

    async def create_indexes(self):
        return await self._run_async(
            "create_indexes", self._store.create_indexes,
        )

    # ── batch / high-throughput ──────────────────────────────────────────

    async def batch_insert(self, records: List[Dict[str, Any]]) -> List[Any]:
        tasks = [self.insert_memory(**record) for record in records]
        return await asyncio.gather(*tasks, return_exceptions=True)

    # ── health / close ───────────────────────────────────────────────────

    async def health_check(self) -> Dict[str, Any]:
        try:
            count_val = await self._run_async("health_check", self._store.count)
            return {"status": "ok", "memory_count": count_val}
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
        try:
            self._store.close()
        except Exception:
            logger.debug("Underlying store close raised (ignored)", exc_info=True)

    # ── context manager ──────────────────────────────────────────────────

    async def __aenter__(self):
        self._ensure_executor()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False