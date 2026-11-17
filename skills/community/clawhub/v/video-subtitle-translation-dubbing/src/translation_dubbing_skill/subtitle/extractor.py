"""Extract the embedded English subtitle track from a video file.

This module provides :func:`extract_from_video`, which shells out to
``ffmpeg`` to pull the first stream tagged with ``language=eng`` out of
the container and emit it as SRT on stdout.

Design notes
------------

- We invoke ``ffmpeg`` once with
  ``-map 0:s:m:language:eng -c:s srt -f srt -``. The ``-map`` selector
  chooses the first subtitle stream whose ``language`` metadata tag is
  ``eng``; if none exists, ``ffmpeg`` fails with a non-zero exit code.
- ``-c:s srt`` re-encodes whatever the source codec is (``mov_text``,
  ``webvtt``, ``subrip``, ...) to plain SubRip so the caller always sees
  a consistent SRT payload. The returned format literal is therefore
  always ``"srt"``.
- ``ffmpeg`` is invoked with ``-y`` (overwrite) for safety even though we
  stream to stdout; ``-nostdin`` guarantees we never block on a prompt.
- Any failure — missing track, invalid container, ``ffmpeg`` not on
  PATH, timeout — is normalized to :class:`NoEnglishSubtitleError`
  carrying the video path and (when available) the tail of the ``ffmpeg``
  stderr for operator debugging.

Corresponds to requirements R2.6 and R2.7.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Final, Literal

from translation_dubbing_skill.errors import NoEnglishSubtitleError

# Only include the tail of ``ffmpeg`` stderr in error context so we don't
# carry multi-megabyte log dumps through the error chain.
_STDERR_TAIL_CHARS: Final[int] = 2_000

# Hard cap on the extraction subprocess so a pathological input cannot
# wedge the skill run indefinitely. Five minutes is generous even for
# long-form content since we're only streaming subtitles, not video.
_EXTRACT_TIMEOUT_SECONDS: Final[float] = 300.0


def _tail(text: str, limit: int = _STDERR_TAIL_CHARS) -> str:
    """Return the trailing ``limit`` characters of ``text`` for error context."""
    if len(text) <= limit:
        return text
    return text[-limit:]


def extract_from_video(
    video_path: Path,
) -> tuple[str, Literal["srt", "vtt"]]:
    """Extract the embedded English subtitle track from ``video_path``.

    Args:
        video_path: Path to the input video file.

    Returns:
        A ``(text, format)`` pair. ``text`` is the subtitle content encoded
        as UTF-8 SRT; ``format`` is always the literal ``"srt"`` because
        ``ffmpeg`` is asked to normalize whatever source codec the track
        uses into SubRip.

    Raises:
        NoEnglishSubtitleError: the container carries no English subtitle
            stream, ``ffmpeg`` is not available on PATH, the subprocess
            timed out, or the extraction otherwise failed. The error's
            ``context`` includes ``video_path`` and a bounded tail of the
            ``ffmpeg`` stderr output when one was captured.
    """
    candidate_maps = ["0:s:m:language:eng", "0:s:m:language:en", "0:s:0"]
    last_completed: subprocess.CompletedProcess[bytes] | None = None

    for sub_map in candidate_maps:
        cmd = [
            "ffmpeg",
            "-y",
            "-nostdin",
            "-i",
            str(video_path),
            "-map",
            sub_map,
            "-c:s",
            "srt",
            "-f",
            "srt",
            "-",
        ]

        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                check=False,
                timeout=_EXTRACT_TIMEOUT_SECONDS,
            )
        except FileNotFoundError as exc:
            # ``ffmpeg`` binary missing from PATH — surface as a normal
            # "no english subtitle" failure so the skill entry can tell the
            # caller to provide an external subtitle file.
            raise NoEnglishSubtitleError(
                "ffmpeg executable not found while extracting English subtitle",
                context={
                    "video_path": str(video_path),
                    "reason_detail": str(exc),
                },
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise NoEnglishSubtitleError(
                "ffmpeg timed out while extracting English subtitle",
                context={
                    "video_path": str(video_path),
                    "timeout_seconds": _EXTRACT_TIMEOUT_SECONDS,
                },
            ) from exc

        last_completed = completed
        if completed.returncode == 0 and completed.stdout:
            break

    assert last_completed is not None
    completed = last_completed
    if completed.returncode != 0 or not completed.stdout:
        stderr_text = (
            completed.stderr.decode("utf-8", errors="replace")
            if completed.stderr
            else ""
        )
        raise NoEnglishSubtitleError(
            "no English subtitle track could be extracted from video",
            context={
                "video_path": str(video_path),
                "returncode": completed.returncode,
                "stderr_tail": _tail(stderr_text),
            },
        )

    text = completed.stdout.decode("utf-8", errors="replace")
    return text, "srt"


__all__ = ["extract_from_video"]
