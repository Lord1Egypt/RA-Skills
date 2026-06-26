"""Console compatibility helpers for CLI scripts."""

from __future__ import annotations

import sys


def configure_stdio(encoding: str = "utf-8") -> None:
    """Prefer UTF-8 output on Windows consoles and replace unsupported glyphs."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not reconfigure:
            continue
        try:
            reconfigure(encoding=encoding, errors="replace")
        except Exception:
            pass


configure_stdio()
