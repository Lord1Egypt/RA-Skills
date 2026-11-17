"""Progress event data model emitted by the skill during execution.

Defines :class:`ProgressEvent`, the payload reported by
``ProgressReporter.report`` at each stage transition. The event sequence is
determined by the processing mode (see requirements R11.1–R11.6):

- ``subtitle_and_dubbing``: ``parsing → translating → tts → muxing → done``
- ``subtitle_only``:        ``parsing → translating → muxing → done``

Corresponds to requirement R11.1 and the "Data Models > ProgressEvent"
section of the design document.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

ProgressStage = Literal["parsing", "translating", "tts", "muxing", "done"]
"""Closed set of stages a progress event may report."""


@dataclass(frozen=True)
class ProgressEvent:
    """A single progress update emitted during skill execution.

    Attributes:
        stage: Lifecycle stage this event belongs to. Must be one of
            ``parsing``, ``translating``, ``tts``, ``muxing``, or ``done``.
        message: Human-readable description of the event.
        completed: Optional count of completed units in this stage; paired
            with ``total``. Used for translate/TTS per-entry progress.
            Must be monotonically non-decreasing within a stage.
        total: Optional total unit count in this stage; paired with
            ``completed``.
        extra: Optional bag for stage-specific metadata. The terminal
            ``done`` event typically carries output paths here.
    """

    stage: ProgressStage
    message: str
    completed: int | None = None
    total: int | None = None
    extra: dict[str, Any] | None = None


__all__ = ["ProgressEvent", "ProgressStage"]
