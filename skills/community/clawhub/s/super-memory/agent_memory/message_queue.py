"""
message_queue.py - Distributed Message Queue & Worker Module (V12)

Async message bus + worker pool for processing memory operations.
Supports publish/subscribe, configurable concurrency, retry with DLQ,
and graceful shutdown with drain.

Worker topics:
  - memory.ingest    →  IngestWorker (write to store)
  - memory.index     →  IndexWorker (update search indexes)
  - memory.archive   →  ArchiverWorker (move cold data)
  - memory.notify    →  NotificationWorker (fire webhooks)

Usage:
    from message_queue import MessageQueueManager

    mqm = MessageQueueManager()
    await mqm.start_all()

    # publish a message
    await mqm.bus.publish("memory.ingest", msg)

    # check stats
    stats = mqm.get_worker_stats()
    health = mqm.health_check()

    await mqm.stop_all()
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

_DLQ_TOPIC = ".dlq"
_CLEANUP_INTERVAL = 300
_MAX_RETRIES = 3
_RETRY_BASE_DELAY = 1.0
_IDLE_QUEUE_TTL = 600


@dataclass
class WorkerStats:
    topic: str
    worker_type: str
    active_workers: int = 0
    total_processed: int = 0
    total_failed: int = 0
    total_retried: int = 0
    dlq_depth: int = 0
    queue_depth: int = 0
    started_at: float = 0.0
    last_processed_at: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        uptime = time.time() - self.started_at if self.started_at > 0 else 0
        return {
            "topic": self.topic,
            "worker_type": self.worker_type,
            "active_workers": self.active_workers,
            "total_processed": self.total_processed,
            "total_failed": self.total_failed,
            "total_retried": self.total_retried,
            "dlq_depth": self.dlq_depth,
            "queue_depth": self.queue_depth,
            "uptime_seconds": round(uptime, 2),
            "last_processed_at": self.last_processed_at,
        }


def _make_message(
    msg_type: str,
    tenant_id: str,
    payload: Dict[str, Any],
    parent_id: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "id": uuid.uuid4().hex,
        "type": msg_type,
        "tenant_id": tenant_id,
        "payload": payload,
        "timestamp": int(time.time()),
        "parent_id": parent_id,
        "retry_count": 0,
    }


class MessageBus(ABC):
    """Abstract interface for a topic-based message bus."""

    @abstractmethod
    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def subscribe(self, topic: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        ...

    @abstractmethod
    async def unsubscribe(self, topic: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...


class InMemoryMessageBus(MessageBus):
    """Thread-safe in-memory message bus backed by asyncio.Queue per topic.

    Features:
      - Configurable per-topic max queue size (backpressure)
      - Auto-cleanup of idle queues after TTL
      - DLQ routing for failed messages
      - Async generator consume() for worker drain loops
    """

    def __init__(self, max_queue_size: int = 4096) -> None:
        self._max_queue_size = max_queue_size
        self._queues: Dict[str, asyncio.Queue] = {}
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], Awaitable[None]]]] = defaultdict(list)
        self._last_active: Dict[str, float] = {}
        self._cleanup_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()
        self._closed = False

    async def _ensure_topic(self, topic: str) -> asyncio.Queue:
        if topic not in self._queues:
            self._queues[topic] = asyncio.Queue(maxsize=self._max_queue_size)
        self._last_active[topic] = time.time()
        return self._queues[topic]

    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        if self._closed:
            raise RuntimeError("MessageBus is closed")
        q = await self._ensure_topic(topic)
        try:
            q.put_nowait(message)
        except asyncio.QueueFull:
            logger.warning("Queue full for topic '%s', dropping message %s", topic, message.get("id"))
        logger.debug("Published message %s to topic '%s'", message.get("id"), topic)

    async def subscribe(self, topic: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        async with self._lock:
            if callback not in self._subscribers[topic]:
                self._subscribers[topic].append(callback)
                logger.debug("Subscribed callback to topic '%s'", topic)

    async def unsubscribe(self, topic: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        async with self._lock:
            subs = self._subscribers[topic]
            if callback in subs:
                subs.remove(callback)
                logger.debug("Unsubscribed callback from topic '%s'", topic)

    async def consume(self, topic: str, stop_event: Optional[asyncio.Event] = None) -> Any:
        """Async generator yielding messages from *topic*.

        Yields each message as it arrives. The generator exits when:
          - The bus is closed and the queue is drained, OR
          - *stop_event* is set.
        """
        q = await self._ensure_topic(topic)
        while True:
            if stop_event is not None and stop_event.is_set():
                return
            if self._closed:
                if q.empty():
                    return
            try:
                msg = await asyncio.wait_for(q.get(), timeout=0.5)
                yield msg
            except asyncio.TimeoutError:
                continue

    async def _cleanup_idle_queues(self) -> None:
        """Periodic cleanup of queues that have been idle beyond TTL."""
        while not self._closed:
            await asyncio.sleep(_CLEANUP_INTERVAL)
            now = time.time()
            async with self._lock:
                stale = [
                    t
                    for t in list(self._queues.keys())
                    if t not in self._subscribers or not self._subscribers[t]
                ]
                for topic in stale:
                    last = self._last_active.get(topic, now)
                    if now - last > _IDLE_QUEUE_TTL:
                        q = self._queues.get(topic)
                        if q is not None and q.empty():
                            del self._queues[topic]
                            self._last_active.pop(topic, None)
                            logger.debug("Cleaned up idle queue for topic '%s'", topic)

    async def queue_depth(self, topic: str) -> int:
        q = self._queues.get(topic)
        if q is None:
            return 0
        return q.qsize()

    async def close(self) -> None:
        self._closed = True
        if self._cleanup_task is not None:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            self._cleanup_task = None
        self._subscribers.clear()
        self._queues.clear()
        self._last_active.clear()
        logger.info("MessageBus closed")

    async def start_cleanup(self) -> None:
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_idle_queues())


class _RetryManager:
    """Per-message retry state with exponential backoff."""

    def __init__(self, base_delay: float = _RETRY_BASE_DELAY, max_retries: int = _MAX_RETRIES) -> None:
        self._base_delay = base_delay
        self._max_retries = max_retries

    def next_delay(self, retry_count: int) -> float:
        return self._base_delay * (2 ** retry_count)

    def should_retry(self, retry_count: int) -> bool:
        return retry_count < self._max_retries


class MemoryWorker(ABC):
    """Base async worker that drains a topic and processes messages.

    Subclass and implement ``_process()``.
    """

    def __init__(
        self,
        bus: InMemoryMessageBus,
        topic: str,
        concurrency: int = 2,
        worker_type: str = "generic",
        retry_manager: Optional[_RetryManager] = None,
    ) -> None:
        self._bus = bus
        self._topic = topic
        self._concurrency = max(1, concurrency)
        self._worker_type = worker_type
        self._retry = retry_manager or _RetryManager()
        self._tasks: List[asyncio.Task] = []
        self._running = False
        self._drain_event = asyncio.Event()
        self._stats = WorkerStats(topic=topic, worker_type=worker_type)
        self._started_at: float = 0.0

    # ------------------------------------------------------------------
    #  Public API
    # ------------------------------------------------------------------

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._drain_event.clear()
        self._started_at = time.time()
        self._stats.started_at = self._started_at
        for i in range(self._concurrency):
            task = asyncio.create_task(self._drain_loop(i))
            self._tasks.append(task)
        await self._bus.start_cleanup()
        logger.info(
            "Worker '%s' started on topic '%s' (concurrency=%d)",
            self._worker_type, self._topic, self._concurrency,
        )

    async def stop(self, drain: bool = True) -> None:
        if not self._running:
            return
        self._running = False
        self._drain_event.set()
        if not drain:
            for task in self._tasks:
                task.cancel()
        if self._tasks:
            gathered = asyncio.gather(*self._tasks, return_exceptions=True)
            try:
                await asyncio.wait_for(gathered, timeout=30.0)
            except asyncio.TimeoutError:
                logger.warning(
                    "Worker '%s' drain timeout — cancelling remaining tasks", self._worker_type
                )
                for task in self._tasks:
                    task.cancel()
        self._tasks.clear()
        logger.info("Worker '%s' stopped on topic '%s'", self._worker_type, self._topic)

    def status(self) -> Dict[str, Any]:
        return self._stats.to_dict()

    # ------------------------------------------------------------------
    #  Subclass contract
    # ------------------------------------------------------------------

    @abstractmethod
    async def _process(self, message: Dict[str, Any]) -> None:
        ...

    # ------------------------------------------------------------------
    #  Internal
    # ------------------------------------------------------------------

    async def _drain_loop(self, worker_id: int) -> None:
        self._stats.active_workers += 1
        try:
            async for msg in self._bus.consume(self._topic, stop_event=self._drain_event):
                q = self._bus._queues.get(self._topic)
                self._stats.queue_depth = q.qsize() if q else 0
                await self._handle_message(msg)
        except asyncio.CancelledError:
            pass
        finally:
            self._stats.active_workers -= 1

    async def _handle_message(self, message: Dict[str, Any]) -> None:
        try:
            await self._process(message)
            self._stats.total_processed += 1
            self._stats.last_processed_at = time.time()
        except Exception:
            retry_count = message.get("retry_count", 0)
            if self._retry.should_retry(retry_count):
                message["retry_count"] = retry_count + 1
                delay = self._retry.next_delay(retry_count)
                logger.debug(
                    "Retrying message %s (attempt %d/%d, delay %.1fs)",
                    message.get("id"), message["retry_count"], _MAX_RETRIES, delay,
                )
                self._stats.total_retried += 1
                await asyncio.sleep(delay)
                await self._bus.publish(self._topic, message)
            else:
                logger.error(
                    "Message %s exhausted retries (%d) — routing to DLQ",
                    message.get("id"), _MAX_RETRIES,
                )
                self._stats.total_failed += 1
                await self._bus.publish(_DLQ_TOPIC, message)

    def _update_queue_depth(self, depth: int) -> None:
        self._stats.queue_depth = depth


class IngestWorker(MemoryWorker):
    """Worker that listens on *memory.ingest* and writes to the memory store."""

    def __init__(
        self,
        bus: InMemoryMessageBus,
        store: Optional[Any] = None,
        concurrency: int = 2,
        retry_manager: Optional[_RetryManager] = None,
    ) -> None:
        super().__init__(bus, "memory.ingest", concurrency, "ingest", retry_manager)
        self._store = store

    async def _process(self, message: Dict[str, Any]) -> None:
        payload = message.get("payload", {})
        if self._store is not None:
            if hasattr(self._store, "store"):
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    self._store.store,
                    payload.get("session_id", "default"),
                    payload.get("data", {}),
                )
            else:
                logger.debug("IngestWorker: store interface not available, message %s acknowledged", message.get("id"))
        else:
            logger.debug("IngestWorker: no store configured, message %s acknowledged", message.get("id"))


class IndexWorker(MemoryWorker):
    """Worker that listens on *memory.index* and updates search indexes."""

    def __init__(
        self,
        bus: InMemoryMessageBus,
        index_registry: Optional[Any] = None,
        concurrency: int = 2,
        retry_manager: Optional[_RetryManager] = None,
    ) -> None:
        super().__init__(bus, "memory.index", concurrency, "index", retry_manager)
        self._index_registry = index_registry

    async def _process(self, message: Dict[str, Any]) -> None:
        payload = message.get("payload", {})
        if self._index_registry is not None:
            index_fn = getattr(self._index_registry, "update_index", None)
            if index_fn is not None:
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    index_fn,
                    payload.get("document_id", message.get("id")),
                    payload.get("content", ""),
                    payload.get("metadata", {}),
                )
            else:
                logger.debug("IndexWorker: update_index not found, message %s acknowledged", message.get("id"))
        else:
            logger.debug("IndexWorker: no index_registry configured, message %s acknowledged", message.get("id"))


class ArchiverWorker(MemoryWorker):
    """Worker that listens on *memory.archive* and moves cold data."""

    def __init__(
        self,
        bus: InMemoryMessageBus,
        archiver: Optional[Any] = None,
        concurrency: int = 1,
        retry_manager: Optional[_RetryManager] = None,
    ) -> None:
        super().__init__(bus, "memory.archive", concurrency, "archiver", retry_manager)
        self._archiver = archiver

    async def _process(self, message: Dict[str, Any]) -> None:
        payload = message.get("payload", {})
        if self._archiver is not None:
            archive_fn = getattr(self._archiver, "archive", None)
            if archive_fn is not None:
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    archive_fn,
                    payload.get("record_ids", []),
                    payload.get("tier", "cold"),
                )
            else:
                logger.debug("ArchiverWorker: archive not found, message %s acknowledged", message.get("id"))
        else:
            logger.debug("ArchiverWorker: no archiver configured, message %s acknowledged", message.get("id"))


class NotificationWorker(MemoryWorker):
    """Worker that listens on *memory.notify* and fires webhooks."""

    def __init__(
        self,
        bus: InMemoryMessageBus,
        webhook_urls: Optional[List[str]] = None,
        concurrency: int = 1,
        retry_manager: Optional[_RetryManager] = None,
    ) -> None:
        super().__init__(bus, "memory.notify", concurrency, "notification", retry_manager)
        self._webhook_urls = webhook_urls or []

    async def _process(self, message: Dict[str, Any]) -> None:
        payload = message.get("payload", {})
        if self._webhook_urls:
            import urllib.request

            body = json.dumps({
                "event": "memory.notify",
                "message_id": message.get("id"),
                "tenant_id": message.get("tenant_id"),
                "payload": payload,
            }).encode("utf-8")
            for url in self._webhook_urls:
                req = urllib.request.Request(
                    url, data=body, headers={"Content-Type": "application/json"}, method="POST"
                )
                try:
                    await asyncio.wait_for(
                        asyncio.get_event_loop().run_in_executor(
                            None, lambda r=req: urllib.request.urlopen(r, timeout=30)
                        ),
                        timeout=35,
                    )
                except asyncio.TimeoutError:
                    logger.warning("NotificationWorker: webhook to %s timed out", url)
                except Exception as exc:
                    logger.warning("NotificationWorker: webhook to %s failed: %s", url, exc)
        logger.debug("NotificationWorker: processed message %s (urls=%d)", message.get("id"), len(self._webhook_urls))


class MessageQueueManager:
    """Central orchestrator managing the message bus and worker pool.

    Provides:
      - start_all() / stop_all() lifecycle
      - Per-worker metrics via get_worker_stats()
      - Health check suitable for serving over HTTP
    """

    def __init__(
        self,
        max_queue_size: int = 4096,
        worker_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._bus = InMemoryMessageBus(max_queue_size=max_queue_size)
        self._config = worker_config or {}
        self._workers: Dict[str, MemoryWorker] = {}
        self._started = False

    # ------------------------------------------------------------------
    #  Lifecycle
    # ------------------------------------------------------------------

    async def start_all(self) -> None:
        if self._started:
            return
        await self._bus.start_cleanup()

        ingest_concurrency = self._config.get("ingest_concurrency", 2)
        index_concurrency = self._config.get("index_concurrency", 2)
        archive_concurrency = self._config.get("archive_concurrency", 1)
        notify_concurrency = self._config.get("notify_concurrency", 1)

        ingest_store = self._config.get("store")
        index_registry = self._config.get("index_registry")
        archiver = self._config.get("archiver")
        webhook_urls = self._config.get("webhook_urls", [])

        self._workers["ingest"] = IngestWorker(
            self._bus, store=ingest_store, concurrency=ingest_concurrency
        )
        self._workers["index"] = IndexWorker(
            self._bus, index_registry=index_registry, concurrency=index_concurrency
        )
        self._workers["archive"] = ArchiverWorker(
            self._bus, archiver=archiver, concurrency=archive_concurrency
        )
        self._workers["notification"] = NotificationWorker(
            self._bus, webhook_urls=webhook_urls, concurrency=notify_concurrency
        )

        for name, worker in self._workers.items():
            await worker.start()

        self._started = True
        logger.info("MessageQueueManager started with %d workers", len(self._workers))

    async def stop_all(self, drain: bool = True) -> None:
        if not self._started:
            return
        for name, worker in self._workers.items():
            await worker.stop(drain=drain)
        await self._bus.close()
        self._started = False
        logger.info("MessageQueueManager stopped")

    # ------------------------------------------------------------------
    #  Push helpers
    # ------------------------------------------------------------------

    async def push_ingest(self, tenant_id: str, payload: Dict[str, Any]) -> str:
        msg = _make_message("ingest", tenant_id, payload)
        await self._bus.publish("memory.ingest", msg)
        return msg["id"]

    async def push_index(self, tenant_id: str, payload: Dict[str, Any]) -> str:
        msg = _make_message("index", tenant_id, payload)
        await self._bus.publish("memory.index", msg)
        return msg["id"]

    async def push_archive(self, tenant_id: str, payload: Dict[str, Any]) -> str:
        msg = _make_message("archive", tenant_id, payload)
        await self._bus.publish("memory.archive", msg)
        return msg["id"]

    async def push_notify(self, tenant_id: str, payload: Dict[str, Any]) -> str:
        msg = _make_message("notify", tenant_id, payload)
        await self._bus.publish("memory.notify", msg)
        return msg["id"]

    # ------------------------------------------------------------------
    #  Introspection
    # ------------------------------------------------------------------

    @property
    def bus(self) -> InMemoryMessageBus:
        return self._bus

    def get_worker_stats(self) -> Dict[str, Any]:
        stats: Dict[str, Any] = {}
        for name, worker in self._workers.items():
            ws = worker.status()
            stats[name] = ws
        dlq_q = self._bus._queues.get(_DLQ_TOPIC)
        stats["_dlq"] = {
            "queue_depth": dlq_q.qsize() if dlq_q else 0,
        }
        return stats

    def health_check(self) -> Dict[str, Any]:
        workers_healthy = all(
            w._running for w in self._workers.values()
        ) if self._started else False
        dlq_q = self._bus._queues.get(_DLQ_TOPIC)
        return {
            "status": "healthy" if workers_healthy else "degraded",
            "started": self._started,
            "workers": {name: w._running for name, w in self._workers.items()},
            "dlq_depth": dlq_q.qsize() if dlq_q else 0,
            "timestamp": int(time.time()),
        }


# ------------------------------------------------------------------
#  Global singleton
# ------------------------------------------------------------------

_message_queue_manager: Optional[MessageQueueManager] = None


def get_message_queue_manager(config: Optional[Dict[str, Any]] = None) -> MessageQueueManager:
    global _message_queue_manager
    if _message_queue_manager is None:
        _message_queue_manager = MessageQueueManager(worker_config=config or {})
    return _message_queue_manager