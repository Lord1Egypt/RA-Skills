"""
state_bus.py — Sigrid's Internal State Event Bus
=================================================

Adapted from OpenClaw's clawlite bus system (bus/events.py + bus/queue.py).
Provides typed, in-process async message passing between all Ørlög modules.

This is the Bifröst of the system — every module publishes and subscribes
through the bus, keeping them decoupled and independently testable.

Event taxonomy:
  InboundEvent  — user message arriving into the skill
  OutboundEvent — Sigrid's response leaving the skill
  StateEvent    — internal state change (bio tick, wyrd update, etc.)
"""

from __future__ import annotations

import asyncio
import hashlib
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from time import monotonic
from typing import Any, AsyncIterator, Dict, List, Optional


# ─── Timestamp & ID helpers ───────────────────────────────────────────────────

def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id() -> str:
    return str(uuid.uuid4())


# ─── Event dataclasses ────────────────────────────────────────────────────────

@dataclass(slots=True)
class InboundEvent:
    """A user message arriving at Sigrid's hall — the stranger at the gate."""

    channel: str                          # "openclaw" | "terminal" | "api"
    session_id: str
    user_id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_now)
    envelope_version: int = 1
    correlation_id: str = field(default_factory=_new_id)


@dataclass(slots=True)
class OutboundEvent:
    """Sigrid's response going back to the user — the völva speaks."""

    channel: str
    session_id: str
    target: str                           # user_id or channel target
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    attempt: int = 1
    max_attempts: int = 3
    retryable: bool = True
    dead_lettered: bool = False
    dead_letter_reason: str = ""
    last_error: str = ""
    created_at: str = field(default_factory=_utc_now)
    envelope_version: int = 1
    correlation_id: str = field(default_factory=_new_id)


@dataclass(slots=True)
class StateEvent:
    """An internal state change published by any Ørlög module.

    Verdandi weaves new threads — the bus broadcasts the change to all who listen.
    """

    source_module: str                    # "bio_engine" | "wyrd_matrix" | etc.
    event_type: str                       # "bio_tick" | "mood_update" | "sleep_enter" | etc.
    payload: dict[str, Any] = field(default_factory=dict)
    session_id: str = ""
    created_at: str = field(default_factory=_utc_now)
    correlation_id: str = field(default_factory=_new_id)


# ─── Bus constants ────────────────────────────────────────────────────────────

_WILDCARD = "*"
DEFAULT_QUEUE_MAXSIZE = 1000
DEFAULT_SUBSCRIBER_QUEUE_MAXSIZE = 256
DEFAULT_STOP_EVENT_TTL_S = 6 * 60 * 60  # 6 hours


class BusFullError(Exception):
    """Raised when the bus queue is at capacity and nowait=True is set."""


# ─── Main bus ─────────────────────────────────────────────────────────────────

class StateBus:
    """Lightweight in-process async message bus — the Bifröst between all modules.

    Carries:
      - InboundEvent  : user → Sigrid
      - OutboundEvent : Sigrid → user
      - StateEvent    : internal module → module (bio, wyrd, memory, etc.)

    All queues are bounded; dropped messages are counted, never silently lost.
    Dead-letter queue captures failed outbound events for retry.
    """

    def __init__(
        self,
        maxsize: int = DEFAULT_QUEUE_MAXSIZE,
        subscriber_queue_maxsize: int = DEFAULT_SUBSCRIBER_QUEUE_MAXSIZE,
        stop_event_ttl_s: float = DEFAULT_STOP_EVENT_TTL_S,
    ) -> None:
        self._inbound: asyncio.Queue[InboundEvent] = asyncio.Queue(maxsize=maxsize)
        self._outbound: asyncio.Queue[OutboundEvent] = asyncio.Queue(maxsize=maxsize)
        self._dead_letter: asyncio.Queue[OutboundEvent] = asyncio.Queue(maxsize=maxsize)
        self._state: asyncio.Queue[StateEvent] = asyncio.Queue(maxsize=maxsize)

        # Topic subscriptions: channel name → list of per-subscriber queues
        self._inbound_topics: dict[str, list[asyncio.Queue[InboundEvent]]] = defaultdict(list)
        # State event topic subscriptions: event_type → subscriber queues
        self._state_topics: dict[str, list[asyncio.Queue[StateEvent]]] = defaultdict(list)

        self._subscriber_queue_maxsize = max(1, int(subscriber_queue_maxsize))
        self._dead_letter_events: deque[OutboundEvent] = deque()
        self._stop_event_ttl_s = max(0.01, float(stop_event_ttl_s))
        self._stop_events: dict[str, tuple[asyncio.Event, float]] = {}
        self._outbound_created_at: deque[str] = deque()

        # Telemetry counters — Huginn's tally of all traffic
        self._inbound_subscriber_dropped = 0   # fan-out drops to slow inbound subscribers
        self._state_subscriber_dropped = 0     # fan-out drops to slow state subscribers
        self._inbound_published = 0
        self._outbound_enqueued = 0
        self._outbound_dropped = 0
        self._state_published = 0
        self._state_dropped = 0
        self._dead_letter_enqueued = 0

    # ─── Inbound (user → skill) ───────────────────────────────────────────────

    async def publish_inbound(self, event: InboundEvent, *, nowait: bool = False) -> None:
        """Publish a user message into the skill. Fans out to topic subscribers."""
        if nowait:
            try:
                self._inbound.put_nowait(event)
            except asyncio.QueueFull as exc:
                raise BusFullError("inbound queue is full") from exc
        else:
            await self._inbound.put(event)

        self._inbound_published += 1

        # Fan out to channel-specific and wildcard topic subscribers
        for queue in tuple(self._inbound_topics.get(event.channel, ())):
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                self._inbound_subscriber_dropped += 1
                import logging as _log
                _log.getLogger(__name__).warning(
                    "StateBus backpressure: inbound subscriber queue full "
                    "(channel=%r, total_dropped=%d) — event skipped",
                    event.channel, self._inbound_subscriber_dropped,
                )
        for queue in tuple(self._inbound_topics.get(_WILDCARD, ())):
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                self._inbound_subscriber_dropped += 1
                import logging as _log
                _log.getLogger(__name__).warning(
                    "StateBus backpressure: wildcard inbound subscriber queue full "
                    "(total_dropped=%d) — event skipped",
                    self._inbound_subscriber_dropped,
                )

    async def next_inbound(self) -> InboundEvent:
        """Await the next inbound event from the main queue."""
        return await self._inbound.get()

    async def subscribe_inbound(self, channel: str) -> AsyncIterator[InboundEvent]:
        """Async generator yielding inbound events for a specific channel."""
        queue: asyncio.Queue[InboundEvent] = asyncio.Queue(
            maxsize=self._subscriber_queue_maxsize
        )
        self._inbound_topics[channel].append(queue)
        try:
            while True:
                yield await queue.get()
        finally:
            try:
                self._inbound_topics[channel].remove(queue)
            except ValueError:
                pass

    # ─── Outbound (skill → user) ──────────────────────────────────────────────

    async def publish_outbound(self, event: OutboundEvent) -> None:
        """Enqueue an outbound response. Drops silently if full (counted)."""
        try:
            self._outbound.put_nowait(event)
            self._outbound_created_at.append(str(event.created_at))
            self._outbound_enqueued += 1
        except asyncio.QueueFull:
            self._outbound_dropped += 1

    async def next_outbound(self) -> OutboundEvent:
        """Await the next outbound event."""
        event = await self._outbound.get()
        if self._outbound_created_at:
            self._outbound_created_at.popleft()
        return event

    # ─── Dead-letter queue ────────────────────────────────────────────────────

    async def publish_dead_letter(self, event: OutboundEvent) -> None:
        """Send a failed outbound event to the Vargr Ledger (dead-letter queue)."""
        await self._dead_letter.put(event)
        self._dead_letter_events.append(event)
        self._dead_letter_enqueued += 1

    def dead_letter_snapshot(self) -> list[OutboundEvent]:
        """Return a copy of all dead-letter events for inspection."""
        return list(self._dead_letter_events)

    # ─── State events (module → module) ──────────────────────────────────────

    async def publish_state(self, event: StateEvent, *, nowait: bool = False) -> None:
        """Publish an internal state change. Fan out to event_type subscribers."""
        if nowait:
            try:
                self._state.put_nowait(event)
            except asyncio.QueueFull:
                self._state_dropped += 1
                return
        else:
            await self._state.put(event)
        self._state_published += 1

        # Fan out to type-specific and wildcard state subscribers
        for queue in tuple(self._state_topics.get(event.event_type, ())):
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                self._state_subscriber_dropped += 1
                import logging as _log
                _log.getLogger(__name__).warning(
                    "StateBus backpressure: state subscriber queue full "
                    "(event_type=%r, total_dropped=%d) — event skipped",
                    event.event_type, self._state_subscriber_dropped,
                )
        for queue in tuple(self._state_topics.get(_WILDCARD, ())):
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                self._state_subscriber_dropped += 1
                import logging as _log
                _log.getLogger(__name__).warning(
                    "StateBus backpressure: wildcard state subscriber queue full "
                    "(total_dropped=%d) — event skipped",
                    self._state_subscriber_dropped,
                )

    async def next_state(self) -> StateEvent:
        """Await the next state event from the main queue."""
        return await self._state.get()

    async def subscribe_state(self, event_type: str) -> AsyncIterator[StateEvent]:
        """Async generator yielding state events of a given type (or '*' for all)."""
        queue: asyncio.Queue[StateEvent] = asyncio.Queue(
            maxsize=self._subscriber_queue_maxsize
        )
        self._state_topics[event_type].append(queue)
        try:
            while True:
                yield await queue.get()
        finally:
            try:
                self._state_topics[event_type].remove(queue)
            except ValueError:
                pass

    # ─── Session stop signals ─────────────────────────────────────────────────

    def _prune_stop_events(self) -> None:
        """Remove expired stop signals — the old watch relieves itself."""
        cutoff = monotonic() - self._stop_event_ttl_s
        stale = [
            sid for sid, (_, touched) in self._stop_events.items() if touched < cutoff
        ]
        for sid in stale:
            self._stop_events.pop(sid, None)

    def stop_event(self, session_id: str) -> asyncio.Event:
        """Get (or create) the stop signal for a session."""
        self._prune_stop_events()
        sid = str(session_id or "").strip()
        if not sid:
            return asyncio.Event()
        entry = self._stop_events.get(sid)
        if entry is None:
            evt = asyncio.Event()
        else:
            evt = entry[0]
        self._stop_events[sid] = (evt, monotonic())
        return evt

    def request_stop(self, session_id: str) -> bool:
        """Signal a session to stop gracefully — Skuld cuts the thread."""
        sid = str(session_id or "").strip()
        if not sid:
            return False
        evt = self.stop_event(sid)
        evt.set()
        self._stop_events[sid] = (evt, monotonic())
        return True

    def clear_stop(self, session_id: str) -> None:
        """Clear a session stop signal — the thread is renewed."""
        sid = str(session_id or "").strip()
        if not sid:
            return
        entry = self._stop_events.pop(sid, None)
        if entry is not None:
            entry[0].clear()

    # ─── Lifecycle ────────────────────────────────────────────────────────────

    async def connect(self) -> None:
        """No-op for in-process bus; exists for interface compatibility."""
        return None

    async def close(self) -> None:
        """Gracefully shut down the bus — Bifröst retracts."""
        import logging as _log
        # Signal all active sessions to stop — Skuld severs every thread
        for evt, _ in self._stop_events.values():
            evt.set()
        # Clear subscriber registrations — fan-out ceases; generators' finally
        # blocks will remove their own queue references as they unwind
        self._inbound_topics.clear()
        self._state_topics.clear()
        _log.getLogger(__name__).info(
            "StateBus closed — %d session(s) signalled, subscriber topics cleared.",
            len(self._stop_events),
        )

    # ─── Telemetry ────────────────────────────────────────────────────────────

    def stats(self) -> dict[str, Any]:
        """Return bus telemetry — Odin's ravens report on all nine worlds."""
        self._prune_stop_events()
        return {
            "inbound_size": self._inbound.qsize(),
            "inbound_published": self._inbound_published,
            "outbound_size": self._outbound.qsize(),
            "outbound_enqueued": self._outbound_enqueued,
            "outbound_dropped": self._outbound_dropped,
            "state_size": self._state.qsize(),
            "state_published": self._state_published,
            "state_dropped": self._state_dropped,
            "inbound_subscriber_dropped": self._inbound_subscriber_dropped,
            "state_subscriber_dropped": self._state_subscriber_dropped,
            "dead_letter_size": self._dead_letter.qsize(),
            "dead_letter_enqueued": self._dead_letter_enqueued,
            "inbound_topic_count": sum(
                len(v) for v in self._inbound_topics.values()
            ),
            "state_topic_count": sum(
                len(v) for v in self._state_topics.values()
            ),
            "stop_sessions": len(self._stop_events),
        }


# ─── Singleton accessor ────────────────────────────────────────────────────────

_BUS: Optional[StateBus] = None


def get_bus() -> StateBus:
    """Return the global StateBus, initialising it on first call."""
    global _BUS
    if _BUS is None:
        _BUS = StateBus()
    return _BUS


def init_bus(
    maxsize: int = DEFAULT_QUEUE_MAXSIZE,
    subscriber_queue_maxsize: int = DEFAULT_SUBSCRIBER_QUEUE_MAXSIZE,
) -> StateBus:
    """Create and register a fresh StateBus (call once at startup)."""
    global _BUS
    _BUS = StateBus(maxsize=maxsize, subscriber_queue_maxsize=subscriber_queue_maxsize)
    return _BUS
