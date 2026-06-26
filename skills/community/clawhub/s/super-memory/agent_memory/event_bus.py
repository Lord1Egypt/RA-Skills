"""
event_bus.py - Streaming Memory Event Bus (V12)

Provides a lightweight, thread-safe pub/sub event bus for the agent memory
system with SSE-ready output.

Core components:
  - MemoryEventBus   → async pub/sub with asyncio.Queue-based fanout
  - EventSubscriber  → dataclass pairing a callback with an optional filter
  - SSEAdapter       → wraps MemoryEventBus events as Server-Sent Events

Event types:
  memory.created    • memory.updated   • memory.deleted
  memory.recalled   • alert.sentiment  • team.shared

Event format:
  {"id": uuid4, "type": str, "tenant_id": str, "data": dict, "timestamp": float}

Usage:
  bus = MemoryEventBus()
  await bus.subscribe("memory.created", my_callback)
  await bus.emit("memory.created", {"content": "hello"}, tenant_id="t1")
  async for event in bus.stream_events(["memory.created", "memory.updated"]):
      print(event)

  sse = SSEAdapter(bus)
  async for line in sse.events_to_sse(["alert.sentiment"]):
      print(line)  # "event: alert.sentiment\\ndata: {...}\\n\\n"
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Union

logger = logging.getLogger(__name__)

_EVENT_TYPES: frozenset = frozenset({
    "memory.created",
    "memory.updated",
    "memory.deleted",
    "memory.recalled",
    "alert.sentiment",
    "team.shared",
})

_DEFAULT_MAX_QUEUE = 4096


# ═══════════════════════════════════════════════════════════
# EventSubscriber
# ═══════════════════════════════════════════════════════════

@dataclass
class EventSubscriber:
    callback: Callable[..., Any]
    filter: Optional[Callable[[dict], bool]] = None


# ═══════════════════════════════════════════════════════════
# MemoryEventBus
# ═══════════════════════════════════════════════════════════

class MemoryEventBus:
    """
    Async, thread-safe memory event bus.

    Events are emitted onto an asyncio.Queue and fanned out to registered
    subscribers by a single background dispatch loop.  Each subscriber
    receives a copy of every matching event via its own private queue or
    callback invocation.

    Parameters
    ----------
    max_queue_size : int
        Maximum number of pending events before emit blocks (default 4096).
    """

    def __init__(self, max_queue_size: int = _DEFAULT_MAX_QUEUE):
        self._max_queue_size = max_queue_size
        self._queue: Optional[asyncio.Queue] = None
        self._dispatch_task: Optional[asyncio.Task] = None
        self._running = False
        self._subscribers: Dict[str, List[EventSubscriber]] = {
            et: [] for et in _EVENT_TYPES
        }
        self._stream_queues: List[asyncio.Queue] = []
        self._started = False

    # ── lifecycle ─────────────────────────────────────────

    async def _ensure_started(self) -> None:
        if self._started:
            return
        self._started = True
        self._running = True
        self._queue = asyncio.Queue(maxsize=self._max_queue_size)
        self._dispatch_task = asyncio.create_task(self._dispatch_loop())
        logger.debug("MemoryEventBus dispatch loop started")

    async def close(self) -> None:
        self._running = False
        if self._queue is not None:
            try:
                self._queue.put_nowait(None)
            except asyncio.QueueFull as e:
                logger.debug("event_bus: close queue full: %s", e)
        if self._dispatch_task is not None:
            self._dispatch_task.cancel()
            try:
                await self._dispatch_task
            except asyncio.CancelledError as e:
                logger.debug("event_bus: dispatch task cancelled: %s", e)
            self._dispatch_task = None
        for q in self._stream_queues:
            try:
                q.put_nowait(_SENTINEL)
            except asyncio.QueueFull as e:
                logger.debug("event_bus: stream queue full on close: %s", e)
        self._stream_queues.clear()
        self._subscribers = {et: [] for et in _EVENT_TYPES}
        self._started = False
        logger.debug("MemoryEventBus closed")

    # ── emit ──────────────────────────────────────────────

    async def emit(
        self,
        event_type: str,
        data: dict,
        tenant_id: Optional[str] = None,
    ) -> None:
        if event_type not in _EVENT_TYPES:
            logger.warning("Unknown event type %r — ignored", event_type)
            return

        await self._ensure_started()

        event: dict = {
            "id": uuid.uuid4().hex,
            "type": event_type,
            "tenant_id": tenant_id,
            "data": data,
            "timestamp": time.time(),
        }

        try:
            await self._queue.put(event)
        except asyncio.QueueFull:
            logger.error("Event bus queue full — dropping event type=%r", event_type)

    # ── subscribe / unsubscribe ──────────────────────────

    async def subscribe(
        self,
        event_type: str,
        callback: Callable[..., Any],
    ) -> None:
        if event_type not in _EVENT_TYPES:
            raise ValueError(f"Unknown event type: {event_type}")

        await self._ensure_started()

        subscriber = EventSubscriber(callback=callback)
        self._subscribers[event_type].append(subscriber)
        logger.debug("Subscriber registered for %r (total=%d)", event_type, len(self._subscribers[event_type]))

    async def unsubscribe(
        self,
        event_type: str,
        callback: Callable[..., Any],
    ) -> None:
        if event_type not in _EVENT_TYPES:
            raise ValueError(f"Unknown event type: {event_type}")

        subs = self._subscribers.get(event_type, [])
        self._subscribers[event_type] = [
            s for s in subs if s.callback is not callback
        ]
        logger.debug("Subscriber removed for %r (remaining=%d)", event_type, len(self._subscribers[event_type]))

    # ── stream_events ────────────────────────────────────

    async def stream_events(
        self,
        event_types: Optional[List[str]] = None,
    ) -> Any:
        """
        Async generator yielding events as they arrive.

        Parameters
        ----------
        event_types : list[str] or None
            Whitelist of event types to stream.  ``None`` or empty
            means *all* known event types.

        Yields
        ------
        dict
            Event payloads matching the filter.
        """
        await self._ensure_started()

        allowed: frozenset
        if event_types:
            invalid = set(event_types) - _EVENT_TYPES
            if invalid:
                logger.warning("Unknown event type(s) in stream filter: %s", invalid)
            allowed = frozenset(event_types) & _EVENT_TYPES
            if not allowed:
                return
        else:
            allowed = _EVENT_TYPES

        queue: asyncio.Queue = asyncio.Queue(maxsize=self._max_queue_size)
        self._stream_queues.append(queue)

        try:
            while True:
                item = await queue.get()
                if item is _SENTINEL:
                    break
                if isinstance(item, dict):
                    if item["type"] in allowed:
                        yield item
        finally:
            try:
                self._stream_queues.remove(queue)
            except ValueError as e:
                logger.debug("event_bus: stream queue remove: %s", e)

    # ── dispatch loop ────────────────────────────────────

    async def _dispatch_loop(self) -> None:
        queue = self._queue
        if queue is None:
            return

        while self._running:
            try:
                event = await queue.get()
            except asyncio.CancelledError:
                break

            if event is None:
                break

            if not isinstance(event, dict):
                continue

            event_type = event.get("type", "")
            subs = self._subscribers.get(event_type, [])

            for sub in subs:
                try:
                    if sub.filter is not None and not sub.filter(event):
                        continue
                    result = sub.callback(event)
                    if asyncio.iscoroutine(result) or asyncio.isfuture(result):
                        asyncio.create_task(self._safe_invoke(result))
                except Exception:
                    logger.exception("Subscriber callback failed for %r", event_type)

            for sq in self._stream_queues:
                try:
                    sq.put_nowait(event)
                except asyncio.QueueFull:
                    logger.warning("Stream subscriber queue full — dropping event type=%r", event_type)

        logger.debug("MemoryEventBus dispatch loop exited")

    @staticmethod
    async def _safe_invoke(coro) -> None:
        try:
            await coro
        except Exception:
            logger.exception("Async subscriber callback failed")


_SENTINEL = object()


# ═══════════════════════════════════════════════════════════
# SSEAdapter
# ═══════════════════════════════════════════════════════════

class SSEAdapter:
    """
    Converts MemoryEventBus events to Server-Sent Events (SSE) format.

    Parameters
    ----------
    bus : MemoryEventBus
        The event bus to wrap.
    """

    def __init__(self, bus: MemoryEventBus):
        self._bus = bus

    async def events_to_sse(
        self,
        event_types: Optional[List[str]] = None,
    ) -> Any:
        """
        Async generator yielding SSE-formatted strings.

        Each yielded string follows the SSE wire format::

            event: {type}
            data: {json}
            <blank line>

        Parameters
        ----------
        event_types : list[str] or None
            Event types to stream (pass-through to ``bus.stream_events``).

        Yields
        ------
        str
            SSE-formatted event string.
        """
        async for event in self._bus.stream_events(event_types=event_types):
            event_type = event.get("type", "message")
            payload = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
            yield f"event: {event_type}\ndata: {payload}\n\n"