"""Audio clip data model produced by the TTS engine.

Defines :class:`AudioClip`, the unit of work exchanged between the TTS engine
and the audio aligner. Each clip corresponds to a non-empty subtitle entry
and carries the synthesized audio bytes together with its measured duration.

Corresponds to requirement R6.2 and the "Data Models > AudioClip" section of
the design document.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AudioClip:
    """An immutable synthesized audio clip tied to a subtitle entry.

    Attributes:
        entry_index: Matches :attr:`SubtitleEntry.index` of the source entry.
        start_ms: Subtitle window start in milliseconds (inclusive).
        end_ms: Subtitle window end in milliseconds (exclusive).
        audio: Raw audio bytes as returned by the TTS provider (typically
            WAV or PCM).
        duration_ms: Measured duration of ``audio`` in milliseconds.
            Non-negative; enforced by the TTS engine's contract check.
    """

    entry_index: int
    start_ms: int
    end_ms: int
    audio: bytes
    duration_ms: int


__all__ = ["AudioClip"]
