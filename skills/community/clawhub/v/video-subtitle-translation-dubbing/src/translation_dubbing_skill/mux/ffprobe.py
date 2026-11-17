"""Lightweight ``ffprobe`` wrapper used by the muxer and property tests.

The OpenClaw runtime ships with a real ``ffmpeg``/``ffprobe`` toolchain;
the skill invokes ``ffprobe`` to introspect the streams, dispositions and
tags of a muxed output. Tests use the same helper to assert on output
video structure (P17–P20 and P27–P29).

The module exposes a single public function :func:`probe_streams`. It
shells out to ``ffprobe -v error -show_streams -show_format -of json``
and returns the parsed JSON payload as a ``dict`` with keys
``streams`` (list[dict]) and ``format`` (dict).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


def probe_streams(path: Path | str) -> dict[str, Any]:
    """Return ffprobe's JSON metadata for ``path``.

    Args:
        path: Path to the media file. Coerced to ``str`` for the CLI.

    Returns:
        Parsed ffprobe JSON with at least the top-level keys ``streams``
        (a list) and ``format`` (a dict). Each stream dict contains the
        standard ffprobe fields (``codec_type``, ``codec_name``,
        ``width``, ``height``, ``avg_frame_rate``, ...), plus
        ``disposition`` (dict of 0/1 flags) and ``tags`` (dict of string
        metadata including ``language``).

    Raises:
        RuntimeError: If ``ffprobe`` exits non-zero. The stderr of the
            subprocess is embedded in the message for debugging.
        json.JSONDecodeError: If ``ffprobe`` prints non-JSON on stdout
            (should not happen with ``-of json`` but surfaced so callers
            can observe pathological toolchains).
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "ffprobe failed: "
            f"path={str(path)!r} "
            f"stderr={result.stderr.decode('utf-8', errors='replace')}"
        )
    payload = json.loads(result.stdout.decode("utf-8", errors="replace"))
    # Ensure the canonical shape even when a container has no streams /
    # format entries, so callers can always iterate ``payload["streams"]``.
    payload.setdefault("streams", [])
    payload.setdefault("format", {})
    return payload


__all__ = ["probe_streams"]
