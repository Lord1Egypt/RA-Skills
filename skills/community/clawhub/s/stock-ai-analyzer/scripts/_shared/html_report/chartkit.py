"""Loader for the shared chart-kit JavaScript.

The kit (``chartkit.js``) defines ``window.CK`` — the SVG/DOM primitives and
small generic chart components that hooks share (metric cards, horizontal bars,
tooltips, cards, legends, heading finders).
The builder injects it once per page, right after the base UI script and
before any ChartHook IIFE, so hooks can drop their private copies.
"""

from __future__ import annotations

from importlib import resources


def chartkit_js() -> str:
    return (resources.files(__package__) / "chartkit.js").read_text(encoding="utf-8")
