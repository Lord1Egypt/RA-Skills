"""Rasterise a DXF file (lines, circles, arcs, polylines, splines, dimension blocks) to PNG.

Used to preview drawings from the file that was actually written. Text is not
drawn (no font renderer); dimension values are reported in the JSON instead.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

Seg = Tuple[float, float, float, float]


def _pairs(text: str) -> List[Tuple[str, str]]:
    lines = [ln.strip() for ln in text.splitlines()]
    return list(zip(lines[0::2], lines[1::2]))


def _sections(text: str) -> Dict[str, List[Tuple[str, Dict[str, List[str]]]]]:
    out: Dict[str, List[Any]] = {}
    current = None
    pairs = _pairs(text)
    for (code, value), nxt in zip(pairs, pairs[1:] + [("", "")]):
        if code == "0" and value == "SECTION":
            current = nxt[1]
            out[current] = []
            continue
        if code == "0" and value == "ENDSEC":
            current = None
            continue
        if current is None or (code == "2" and not out[current]):
            continue
        if code == "0":
            out[current].append((value, {}))
        elif out[current]:
            out[current][-1][1].setdefault(code, []).append(value)
    return out


def _arc(cx: float, cy: float, r: float, a0: float, a1: float, n: int = 48) -> List[Seg]:
    sweep = (a1 - a0) % 360 or 360
    pts = [
        (cx + r * math.cos(math.radians(a0 + sweep * k / n)), cy + r * math.sin(math.radians(a0 + sweep * k / n)))
        for k in range(n + 1)
    ]
    return [(*pts[k], *pts[k + 1]) for k in range(n)]


def _segments(ents: List[Any]) -> List[Seg]:
    segs: List[Seg] = []
    for kind, g in ents:
        try:
            f = lambda c, i=0, g=g: float(g[c][i])  # noqa: E731
            if kind == "LINE":
                segs.append((f("10"), f("20"), f("11"), f("21")))
            elif kind == "CIRCLE":
                segs += _arc(f("10"), f("20"), f("40"), 0, 360)
            elif kind == "ARC":
                segs += _arc(f("10"), f("20"), f("40"), f("50"), f("51"))
            elif kind in ("LWPOLYLINE", "SPLINE"):
                xs, ys = [float(v) for v in g.get("10", [])], [float(v) for v in g.get("20", [])]
                segs += [(xs[k], ys[k], xs[k + 1], ys[k + 1]) for k in range(min(len(xs), len(ys)) - 1)]
        except (KeyError, ValueError, IndexError):
            continue
    return segs


def segments(text: str) -> Tuple[List[Seg], List[Seg]]:
    """(geometry segments, dimension segments) of a DXF file."""
    sec = _sections(text)
    blocks: Dict[str, List[Any]] = {}
    name = None
    for kind, g in sec.get("BLOCKS", []):
        if kind == "BLOCK":
            name = (g.get("2") or [""])[0]
            blocks[name] = []
        elif kind == "ENDBLK":
            name = None
        elif name is not None:
            blocks[name].append((kind, g))
    geo: List[Any] = []
    dims: List[Seg] = []
    for kind, g in sec.get("ENTITIES", []):
        if kind == "DIMENSION":
            dims += _segments(blocks.get((g.get("2") or [""])[0], []))
        else:
            geo.append((kind, g))
    return _segments(geo), dims


def render_png(text: str, path: str, sheet: Tuple[float, float], px_per_mm: float = 3.0) -> Dict[str, int]:
    import numpy as np

    from .ops.render import _png

    w, h = int(sheet[0] * px_per_mm), int(sheet[1] * px_per_mm)
    img = np.full((h, w, 3), 255, np.uint8)

    def draw(segs: List[Seg], color: Tuple[int, int, int]) -> None:
        for x0, y0, x1, y1 in segs:
            n = int(max(abs(x1 - x0), abs(y1 - y0)) * px_per_mm) + 2
            t = np.linspace(0, 1, n)
            xs = ((x0 + (x1 - x0) * t) * px_per_mm).astype(int)
            ys = (h - 1 - (y0 + (y1 - y0) * t) * px_per_mm).astype(int)
            ok = (xs >= 0) & (xs < w) & (ys >= 0) & (ys < h)
            img[ys[ok], xs[ok]] = color

    geo, dims = segments(text)
    draw(
        [
            (0, 0, sheet[0], 0),
            (sheet[0], 0, sheet[0], sheet[1]),
            (sheet[0], sheet[1], 0, sheet[1]),
            (0, sheet[1], 0, 0),
        ],
        (150, 150, 150),
    )
    draw(dims, (30, 90, 220))
    draw(geo, (0, 0, 0))
    _png(path, img)
    return {"geometry_segments": len(geo), "dimension_segments": len(dims)}
