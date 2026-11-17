"""Audio alignment: place TTS clips onto a silent base track.

This module implements the :class:`AudioAligner` described in the design
document ("音频对齐算法"). It is only invoked in ``subtitle_and_dubbing``
mode (R8.7); callers in ``subtitle_only`` mode never construct it.

Algorithm
---------

Given a sorted list of :class:`AudioClip` s and the total ``video_duration_ms``,
build an output track of exactly ``video_duration_ms`` milliseconds:

1. Start with a silent base track of length ``video_duration_ms`` (R8.1, R8.5).
2. Walk clips in ``start_ms`` order; for each clip:

   * ``target_start = max(entry.start_ms, prev_end)`` — never start earlier
     than the subtitle entry says (R8.2) and never overlap the previously
     placed clip (R8.4).
   * ``available = entry.end_ms - target_start``.
   * If ``available <= 0`` the window is already consumed by a prior clip;
     skip placement (the slot stays silent).
   * If ``clip.duration_ms <= available`` place the raw clip at
     ``target_start``.
   * Otherwise compute ``rate = clip.duration_ms / available``, atempo the
     clip to fit, and truncate if the result still overshoots (R8.3, R8.4).

3. Trim/pad the final concatenation to exactly ``video_duration_ms`` so
   that INV4 (``|output.duration - video_duration_ms| <= 100``) holds by
   construction (R8.6).

Invariants (INV1–INV4)
----------------------

* **INV1** — no overlap:            ``placed[i].start >= placed[i-1].end``
* **INV2** — start not earlier than subtitle start: ``placed[i].start >= entry.start_ms``
* **INV3** — within window:         ``placed[i].end   <= entry.end_ms``
* **INV4** — duration match:        ``|output.duration - video_duration_ms| <= 100``

The aligner accepts an injected ``atempo_fn`` so callers (in particular
property tests) can avoid shelling out to ffmpeg; the default delegates
to :func:`translation_dubbing_skill.align.atempo.apply_atempo`.
"""

from __future__ import annotations

import tempfile
from io import BytesIO
from pathlib import Path
from typing import Callable, Iterable, Protocol

from pydub import AudioSegment

from translation_dubbing_skill.align.atempo import apply_atempo
from translation_dubbing_skill.models.audio_clip import AudioClip

#: Callable signature for the pluggable time-scaling primitive.
#:
#: Takes raw audio bytes and a positive speed multiplier, returns the
#: time-scaled audio as bytes. The default implementation shells out to
#: ffmpeg via :func:`apply_atempo`; tests inject a pure-Python stub that
#: re-encodes a shorter silence so they can run without ffmpeg.
AtempoFn = Callable[[bytes, float], bytes]


class _Placement(Protocol):
    """Structural placement record used for INV1/INV2/INV3 checks."""

    entry_index: int
    start_ms: int
    end_ms: int


class AudioAligner:
    """Place synthesized audio clips on a silent base track.

    Args:
        atempo_fn: Time-scaling primitive. Defaults to the ffmpeg-backed
            :func:`translation_dubbing_skill.align.atempo.apply_atempo`;
            tests pass a pure-Python stub to keep runs hermetic.
    """

    def __init__(self, atempo_fn: AtempoFn | None = None) -> None:
        self._atempo_fn: AtempoFn = atempo_fn if atempo_fn is not None else apply_atempo

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def align(self, clips: Iterable[AudioClip], video_duration_ms: int) -> Path:
        """Build the aligned Chinese audio track.

        Args:
            clips: Iterable of :class:`AudioClip` s. Clips are sorted
                internally by ``start_ms`` so the caller need not pre-sort.
            video_duration_ms: Target track length in milliseconds. Must
                be non-negative.

        Returns:
            Path to a WAV file on disk containing the aligned track. The
            file is created via :func:`tempfile.NamedTemporaryFile` with
            ``delete=False``; the caller is responsible for its lifecycle.

        Raises:
            ValueError: If ``video_duration_ms`` is negative.
        """
        if video_duration_ms < 0:
            raise ValueError(
                f"video_duration_ms must be non-negative; got {video_duration_ms!r}"
            )

        sorted_clips = sorted(clips, key=lambda c: c.start_ms)

        # The silent base track guarantees INV4 by construction: the final
        # output is built by overlaying clips onto this fixed-length base,
        # so its duration never exceeds ``video_duration_ms``.
        track = AudioSegment.silent(duration=video_duration_ms)

        prev_end_ms = 0
        for clip in sorted_clips:
            placement = self._place_one(clip, prev_end_ms)
            if placement is None:
                # No room to place this clip; base track stays silent in
                # the corresponding window (R8.5).
                continue

            placed_segment, placed_start_ms, placed_duration_ms = placement

            # ``overlay`` replaces the samples at ``position`` with the
            # overlay's samples (after mixing). For our use-case we want
            # *replacement*, so we attenuate the base by -∞ dB in the
            # window. pydub's simpler approach: slice & concatenate.
            track = _replace_window(
                track,
                placed_segment,
                placed_start_ms,
                placed_duration_ms,
            )
            prev_end_ms = placed_start_ms + placed_duration_ms

        # Snap the final length to exactly ``video_duration_ms``. The
        # silent base track is already exactly that length; ``_replace_window``
        # preserves length, but we guard against pydub implementation
        # drift (e.g. sample-rate rounding at segment boundaries).
        if len(track) != video_duration_ms:
            if len(track) > video_duration_ms:
                track = track[:video_duration_ms]
            else:
                track = track + AudioSegment.silent(
                    duration=video_duration_ms - len(track)
                )

        out_path = _new_wav_path()
        # Export via an in-memory buffer and write the bytes ourselves.
        # ``AudioSegment.export`` accepts a path but (as of pydub 0.25)
        # leaves the underlying file descriptor open on return, which
        # trips ``ResourceWarning`` under strict warning configurations.
        buffer = BytesIO()
        track.export(buffer, format="wav")
        out_path.write_bytes(buffer.getvalue())
        return out_path

    # ------------------------------------------------------------------
    # Placement helpers
    # ------------------------------------------------------------------

    def _place_one(
        self,
        clip: AudioClip,
        prev_end_ms: int,
    ) -> tuple[AudioSegment, int, int] | None:
        """Decide how to place a single clip.

        Returns the placed ``AudioSegment``, its start in milliseconds,
        and its actual duration in milliseconds. Returns ``None`` if the
        window is already consumed by a prior clip (INV1 enforcement via
        ``target_start``).
        """
        target_start = max(clip.start_ms, prev_end_ms)
        available = clip.end_ms - target_start
        if available <= 0:
            # Window fully absorbed by the previous clip. R8.4 allows us
            # to truncate to zero length (i.e. drop the clip).
            return None

        source = AudioSegment.from_file(BytesIO(clip.audio), format="wav")
        # Peak-normalize non-silent clips to maintain consistent loudness across synthesized TTS clips
        if len(source) > 0 and getattr(source, "max_dBFS", float("-inf")) > float("-inf"):
            try:
                source = source.normalize()
            except Exception:
                pass

        # ``duration_ms`` on the clip is the provider-reported duration;
        # fall back to the measured duration if they disagree so the
        # rate calculation stays faithful to what we actually have in
        # memory.
        measured = len(source)
        duration_ms = max(clip.duration_ms, 0) if clip.duration_ms > 0 else measured

        if duration_ms <= available:
            segment = source
            # Trim any decoder-tail so the placed segment never exceeds
            # the available window (INV3).
            if len(segment) > available:
                segment = segment[:available]
            if len(segment) >= 20:
                segment = segment.fade_in(10).fade_out(10)
            placed_duration = len(segment)
            return segment, target_start, placed_duration

        # Speed check: if we need to speed up, but the calculated rate is extremely close to 1.0
        # (e.g. less than 1.01 or accumulating FP error), we can avoid scaling.
        rate = duration_ms / available
        if abs(rate - 1.0) < 0.005:
            segment = source[:available]
            if len(segment) >= 20:
                segment = segment.fade_in(10).fade_out(10)
            placed_duration = len(segment)
            return segment, target_start, placed_duration

        # Need to speed up. rate > 1 compresses playback length.
        sped_bytes = self._atempo_fn(clip.audio, rate)
        sped = AudioSegment.from_file(BytesIO(sped_bytes), format="wav")
        if len(sped) > available:
            # atempo's output length is subject to its own rounding; truncate
            # to honour INV3 (R8.3 fallback).
            sped = sped[:available]
        if len(sped) >= 20:
            sped = sped.fade_in(10).fade_out(10)
        placed_duration = len(sped)
        return sped, target_start, placed_duration


# ---------------------------------------------------------------------------
# Module-level utilities
# ---------------------------------------------------------------------------


def _replace_window(
    base: AudioSegment,
    insert: AudioSegment,
    start_ms: int,
    duration_ms: int,
) -> AudioSegment:
    """Return ``base`` with ``[start, start+duration)`` replaced by ``insert``.

    ``insert`` is expected to be exactly ``duration_ms`` long; shorter
    inserts are padded with silence to keep the overall length invariant.
    Longer inserts are truncated.
    """
    if duration_ms <= 0:
        return base

    # Normalise insert length so slicing arithmetic below is straightforward.
    if len(insert) > duration_ms:
        insert = insert[:duration_ms]
    elif len(insert) < duration_ms:
        insert = insert + AudioSegment.silent(duration=duration_ms - len(insert))

    head = base[:start_ms]
    tail = base[start_ms + duration_ms :]
    return head + insert + tail


def _new_wav_path() -> Path:
    """Allocate a fresh ``.wav`` path via :mod:`tempfile`.

    The file is created (so callers can rely on its existence) but left
    empty; ``AudioSegment.export`` will overwrite it. ``delete=False``
    ensures the file survives the ``with`` block so ffmpeg downstream
    can open it.
    """
    handle = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    handle.close()
    return Path(handle.name)


__all__ = ["AudioAligner", "AtempoFn"]
