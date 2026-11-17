"""Progress reporting facade for the translation-dubbing skill.

The skill reports lifecycle progress through :class:`ProgressReporter`,
which is a thin dispatcher that forwards :class:`ProgressEvent` values to
a caller-supplied callback. The OpenClaw runtime bridges this callback to
whatever downstream transport it prefers (SSE, WebSocket, log sink, ...).

For testing we expose :class:`InMemoryReporter`, which simply accumulates
every reported event into a list. Tests assert monotonic ``completed``
values, stage orderings, and so on by inspecting the captured sequence.

Design mapping: design §"进度反馈器 (Progress_Reporter)";
requirements R11.1–R11.6.
"""

from __future__ import annotations

from typing import Callable

from translation_dubbing_skill.models.progress_event import ProgressEvent

# Public alias describing the shape of a reporter callback: a one-way sink
# that consumes a ProgressEvent and returns nothing. Kept as a module-level
# type so both the reporter and its users may reference it without coupling
# to ``typing.Callable`` spelling conventions.
ProgressCallback = Callable[[ProgressEvent], None]


class ProgressReporter:
    """Dispatch :class:`ProgressEvent` values to a caller-supplied callback.

    The reporter itself holds no state beyond the callback reference. It
    deliberately does not buffer, filter, or serialize events — that is the
    callback's responsibility. This keeps the skill pipeline decoupled from
    the OpenClaw runtime transport (SSE, WebSocket, in-memory capture in
    tests, ...).
    """

    __slots__ = ("_callback",)

    def __init__(self, callback: ProgressCallback) -> None:
        """Wrap a callback so each call to :meth:`report` forwards to it.

        Args:
            callback: A callable accepting a :class:`ProgressEvent`. The
                skill guarantees at-most-one event is in flight at a time
                (events are emitted sequentially from the coordinating
                entry point), so the callback need not be thread-safe.
        """
        self._callback = callback

    def report(self, event: ProgressEvent) -> None:
        """Forward ``event`` to the wrapped callback.

        Args:
            event: The progress event to dispatch.
        """
        self._callback(event)


class InMemoryReporter(ProgressReporter):
    """A :class:`ProgressReporter` that records every event into a list.

    Intended for tests that need to assert over the event sequence:
    monotonic ``completed``, presence/absence of a ``tts`` stage event
    depending on processing mode, and so on.

    Attributes:
        events: List of every :class:`ProgressEvent` reported, in the
            order :meth:`report` was invoked.
    """

    __slots__ = ("events",)

    def __init__(self) -> None:
        """Initialize the reporter with an empty event buffer."""
        self.events: list[ProgressEvent] = []
        super().__init__(self.events.append)


__all__ = ["ProgressReporter", "InMemoryReporter", "ProgressCallback"]
