"""ffmpeg ``atempo`` filter helpers for audio time-scaling.

The ``atempo`` filter changes audio playback tempo without affecting pitch.
A single ``atempo`` instance only accepts rates in the closed interval
``[0.5, 2.0]``; to reach rates outside that range, the filter has to be
*chained* so the product of per-stage rates equals the target.

This module provides two pure helpers:

* :func:`build_atempo_chain` — decomposes a positive ``rate`` into an
  ``atempo=a,atempo=b,…`` filter-graph string where each per-stage factor
  lies in ``[0.5, 2.0]``.
* :func:`apply_atempo` — shells out to ``ffmpeg`` to apply the filter
  chain to a raw audio byte stream and returns the resulting bytes.

Corresponds to requirements R8.3 and R8.4 (audio time-scaling in the
alignment stage) and the "音频对齐算法" / "变速实现 (ffmpeg)" sections
of the design document.
"""

from __future__ import annotations

import math
import subprocess
import tempfile
from pathlib import Path

# ``atempo``'s per-stage range as documented by ffmpeg. Values outside this
# interval require a chained filter.
_ATEMPO_MIN: float = 0.5
_ATEMPO_MAX: float = 2.0

# Floating-point slack used when deciding whether a rate is already "in
# range". Without it a rate produced by arithmetic like ``3.0 / 1.5`` can
# drift slightly above 2.0 and cause an unneeded extra stage.
_EPS: float = 1e-9


def build_atempo_chain(rate: float) -> str:
    """Return an ``atempo=…,atempo=…`` filter graph for ``rate``.

    Decomposes ``rate`` into a sequence of per-stage factors, each in
    ``[0.5, 2.0]``, whose product equals ``rate`` (within floating-point
    precision). The returned string is ready to hand to ffmpeg's
    ``-filter:a`` option.

    Examples::

        build_atempo_chain(1.0)   -> "atempo=1.0"
        build_atempo_chain(1.5)   -> "atempo=1.5"
        build_atempo_chain(3.0)   -> "atempo=2.0,atempo=1.5"
        build_atempo_chain(0.25)  -> "atempo=0.5,atempo=0.5"

    Args:
        rate: Desired overall tempo multiplier. Must be strictly positive.

    Returns:
        A comma-separated chain of ``atempo=<factor>`` stages. When
        ``rate`` already lies in ``[0.5, 2.0]`` the chain is a single
        stage.

    Raises:
        ValueError: If ``rate`` is not strictly positive or is not finite.
    """
    if not math.isfinite(rate) or rate <= 0.0:
        raise ValueError(f"atempo rate must be a positive finite number; got {rate!r}")

    stages: list[float] = []
    remaining = float(rate)

    # Speed-up path: repeatedly pull out factors of 2.0 until the residual
    # fits in the single-stage range. One extra stage at the end carries
    # whatever is left (which by construction satisfies 1.0 <= x <= 2.0).
    while remaining > _ATEMPO_MAX + _EPS:
        stages.append(_ATEMPO_MAX)
        remaining /= _ATEMPO_MAX

    # Slow-down path: symmetric to the speed-up path with factors of 0.5.
    while remaining < _ATEMPO_MIN - _EPS:
        stages.append(_ATEMPO_MIN)
        remaining /= _ATEMPO_MIN

    # The residual is now inside the per-stage range; emit it as the final
    # (or only) stage. Clamp defensively in case accumulated FP error
    # nudged us a hair outside the nominal bounds.
    residual = min(_ATEMPO_MAX, max(_ATEMPO_MIN, remaining))
    stages.append(residual)

    return ",".join(f"atempo={stage}" for stage in stages)


def apply_atempo(audio_bytes: bytes, rate: float) -> bytes:
    """Apply an atempo filter chain to ``audio_bytes`` via ffmpeg.

    Writes ``audio_bytes`` to a temporary file, shells out to ``ffmpeg``
    with the filter graph produced by :func:`build_atempo_chain`, and
    reads the resulting WAV bytes back. Temporary files are cleaned up
    on both success and error paths.

    Args:
        audio_bytes: Source audio bytes. Any format ffmpeg can auto-detect
            works (e.g. WAV); the output is always WAV.
        rate: Overall tempo multiplier (>0). ``1.0`` is a no-op.

    Returns:
        Time-scaled audio bytes in WAV container format.

    Raises:
        ValueError: If ``rate`` is not strictly positive / finite.
        RuntimeError: If the ``ffmpeg`` subprocess fails; the captured
            stderr is included in the message to aid debugging.
    """
    filter_chain = build_atempo_chain(rate)

    # NamedTemporaryFile with ``delete=False`` so we can close the handle
    # before ffmpeg opens the path (Windows-friendly, and avoids the
    # "file in use" hazard on POSIX when ffmpeg seeks).
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as src:
        src.write(audio_bytes)
        src_path = Path(src.name)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as dst:
        dst_path = Path(dst.name)

    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-i",
                str(src_path),
                "-filter:a",
                filter_chain,
                str(dst_path),
            ],
            capture_output=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                "ffmpeg atempo failed: "
                f"rate={rate!r} chain={filter_chain!r} "
                f"stderr={result.stderr.decode('utf-8', errors='replace')}"
            )
        return dst_path.read_bytes()
    finally:
        # Best-effort cleanup; ignore errors from files that were never
        # created (e.g. if ffmpeg exited before writing the output).
        for path in (src_path, dst_path):
            try:
                path.unlink()
            except FileNotFoundError:
                pass


__all__ = ["build_atempo_chain", "apply_atempo"]
