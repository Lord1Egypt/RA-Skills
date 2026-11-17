#!/usr/bin/env python3
"""Classic black-and-white Chen ER diagram via matplotlib (Graphviz-like fallback).

Layout goals:
- Generous spacing (not cramped)
- Adaptive radius / entity gap by attribute count
- Optional max_attrs: keep PK + FK + first N other fields when too many
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon

_ASSETS = Path(__file__).resolve().parent.parent / "assets"

_CJK_CANDIDATES = [
    _ASSETS / "NotoSansSC-Regular.otf",
    _ASSETS / "NotoSansCJKsc-Regular.otf",
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
    Path("/usr/share/fonts/truetype/arphic/uming.ttc"),
    Path("C:/Windows/Fonts/msyh.ttc"),
    Path("C:/Windows/Fonts/simhei.ttf"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/Library/Fonts/Arial Unicode.ttf"),
    _ASSETS / "DejaVuSans.ttf",
]


def _setup_font() -> None:
    chosen = None
    for fp in _CJK_CANDIDATES:
        try:
            if fp.is_file():
                font_manager.fontManager.addfont(str(fp))
                chosen = font_manager.FontProperties(fname=str(fp)).get_name()
                break
        except Exception:
            continue
    families = [chosen] if chosen else []
    families += [
        "Noto Sans CJK SC", "Microsoft YaHei", "SimHei",
        "PingFang SC", "WenQuanYi Micro Hei", "DejaVu Sans",
    ]
    plt.rcParams["font.sans-serif"] = [f for f in families if f]
    plt.rcParams["axes.unicode_minus"] = False


def _ell_size(label: str) -> tuple[float, float]:
    """Ellipse width/height from label length (roomy)."""
    n = max(len(label), 2)
    w = max(1.35, 0.28 * n + 0.55)
    h = 0.70 if n <= 12 else 0.85
    return w, h


def _trim_attrs(items: list[dict], max_attrs: int | None) -> list[dict]:
    """Keep all PK/FK; fill remaining slots with other fields. None = keep all."""
    if max_attrs is None or max_attrs <= 0 or len(items) <= max_attrs:
        return items
    pks = [x for x in items if x["is_pk"]]
    fks = [x for x in items if x["is_fk"] and not x["is_pk"]]
    others = [x for x in items if not x["is_pk"] and not x["is_fk"]]
    kept = pks + fks
    room = max(max_attrs - len(kept), 0)
    kept += others[:room]
    # stable-ish order: PK, FK, others
    kept.sort(key=lambda s: (0 if s["is_pk"] else (1 if s["is_fk"] else 2), s["name"]))
    return kept


def _fan_positions(cx: float, cy: float, items: list[dict], prefer_up: bool) -> None:
    """Place attribute ellipses around entity with enough clearance."""
    k = len(items)
    if k == 0:
        return

    # Radius grows with count so labels don't collide
    radius = 2.6 + 0.22 * max(k - 4, 0)
    radius = min(radius, 5.5)

    if k == 1:
        angles = [90.0 if prefer_up else -90.0]
    elif k <= 6:
        # upper or lower arc
        if prefer_up:
            start, end = 25.0, 155.0
        else:
            start, end = -155.0, -25.0
        angles = [start + i * (end - start) / (k - 1) for i in range(k)]
    else:
        # full circle for many attrs
        angles = [90.0 + i * (360.0 / k) for i in range(k)]
        radius = max(radius, 3.2 + 0.15 * k)

    for i, it in enumerate(items):
        ang = math.radians(angles[i])
        it["x"] = cx + radius * math.cos(ang)
        it["y"] = cy + radius * math.sin(ang)
        it["w"], it["h"] = _ell_size(it["label"])


def layout_model(model: dict, max_attrs: int | None = 12):
    entities = model.get("entities") or {}
    rels = model.get("relationships") or []
    e_names = list(entities.keys())
    n = len(e_names)
    if n == 0:
        return {}, [], [], []

    # Pre-count attrs for spacing
    attr_counts = {}
    for name, meta in entities.items():
        attr_counts[name] = len(meta.get("attributes") or [])

    max_ac = max(attr_counts.values()) if attr_counts else 0
    # Entity gap grows with attribute density
    base_gap_x = 7.5 + min(max_ac, 10) * 0.35
    base_gap_y = 8.5 + min(max_ac, 10) * 0.4

    ent_centers = {}
    if n == 1:
        ent_centers[e_names[0]] = (0.0, 0.0)
    elif n == 2:
        top, bottom = e_names[0], e_names[1]
        for rel in rels:
            if rel["from"] in e_names and rel["to"] in e_names:
                top, bottom = rel["from"], rel["to"]
                break
        ent_centers[top] = (0.0, base_gap_y / 2)
        ent_centers[bottom] = (0.0, -base_gap_y / 2)
    else:
        # grid-ish: up to 3 per row
        cols = min(3, n)
        rows = math.ceil(n / cols)
        for i, name in enumerate(e_names):
            r, c = divmod(i, cols)
            cx = (c - (cols - 1) / 2) * base_gap_x
            cy = ((rows - 1) / 2 - r) * base_gap_y
            ent_centers[name] = (cx, cy)

    attrs = []
    for name, meta in entities.items():
        cx, cy = ent_centers[name]
        raw = meta.get("attributes") or []
        items = []
        for attr in raw:
            if isinstance(attr, str):
                aname, ainfo = attr, {}
            elif isinstance(attr, dict):
                aname = next(iter(attr.keys()))
                ainfo = attr[aname] if isinstance(attr[aname], dict) else {}
            else:
                continue
            label = ainfo.get("comment") or aname
            is_pk = bool(ainfo.get("pk") or ainfo.get("primary_key"))
            is_fk = bool(ainfo.get("fk") or ainfo.get("foreign_key"))
            items.append({
                "ent": name, "name": aname, "label": label,
                "is_pk": is_pk, "is_fk": is_fk,
            })
        items.sort(key=lambda s: (0 if s["is_pk"] else (1 if s["is_fk"] else 2), s["name"]))
        items = _trim_attrs(items, max_attrs)

        # Prefer attributes on the outer side (top entity → up, bottom → down)
        prefer_up = True
        if n == 2:
            prefer_up = cy > 0
        _fan_positions(cx, cy, items, prefer_up=prefer_up)
        attrs.extend(items)

    diamonds, edges = [], []
    for rel in rels:
        frm, to = rel["from"], rel["to"]
        if frm not in ent_centers or to not in ent_centers:
            continue
        x1, y1 = ent_centers[frm]
        x2, y2 = ent_centers[to]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        diamonds.append({"frm": frm, "to": to, "cx": mx, "cy": my, "label": "(关联)"})
        edges.append({"x1": x2, "y1": y2, "x2": mx, "y2": my, "label": "N"})
        edges.append({"x1": mx, "y1": my, "x2": x1, "y2": y1, "label": "1"})

    for a in attrs:
        ex, ey = ent_centers[a["ent"]]
        edges.append({"x1": ex, "y1": ey, "x2": a["x"], "y2": a["y"], "label": ""})

    return ent_centers, attrs, diamonds, edges


def render(
    model: dict,
    out_path: Path,
    watermark: str | None = "yanleaf.com",
    max_attrs: int | None = 12,
) -> Path:
    _setup_font()
    ent_centers, attrs, diamonds, edges = layout_model(model, max_attrs=max_attrs)
    entities = model.get("entities") or {}

    xs = [c[0] for c in ent_centers.values()] or [0.0]
    ys = [c[1] for c in ent_centers.values()] or [0.0]
    for a in attrs:
        xs += [a["x"] - a["w"] / 2, a["x"] + a["w"] / 2]
        ys += [a["y"] - a["h"] / 2, a["y"] + a["h"] / 2]
    for d in diamonds:
        xs.append(d["cx"]); ys.append(d["cy"])

    pad = 2.4
    xmin, xmax = min(xs) - pad, max(xs) + pad
    ymin, ymax = min(ys) - pad, max(ys) + pad
    span_x, span_y = max(xmax - xmin, 4), max(ymax - ymin, 4)

    # Larger canvas, still readable dpi
    fig_w = min(max(8.0, span_x * 1.15), 22.0)
    fig_h = min(max(8.0, span_y * 1.15), 22.0)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for e in edges:
        ax.plot([e["x1"], e["x2"]], [e["y1"], e["y2"]],
                color="#222", linewidth=1.0, zorder=1)
        if e.get("label"):
            mx = (e["x1"] + e["x2"]) / 2
            my = (e["y1"] + e["y2"]) / 2
            ax.text(mx + 0.22, my, e["label"], fontsize=11,
                    color="#111", ha="left", va="center", zorder=4)

    for a in attrs:
        ax.add_patch(Ellipse(
            (a["x"], a["y"]), a["w"], a["h"],
            facecolor="white", edgecolor="#111", linewidth=1.3, zorder=2,
        ))
        ax.text(a["x"], a["y"] + (0.02 if a["is_pk"] else 0), a["label"],
                ha="center", va="center", fontsize=10, color="#111", zorder=3)
        if a["is_pk"]:
            tw = min(a["w"] * 0.5, 0.20 * len(a["label"]))
            ax.plot([a["x"] - tw / 2, a["x"] + tw / 2],
                    [a["y"] - 0.16, a["y"] - 0.16],
                    color="#111", linewidth=0.9, zorder=3)

    for d in diamonds:
        w, h = 1.5, 0.95
        pts = [
            (d["cx"], d["cy"] + h / 2), (d["cx"] + w / 2, d["cy"]),
            (d["cx"], d["cy"] - h / 2), (d["cx"] - w / 2, d["cy"]),
        ]
        ax.add_patch(Polygon(
            pts, closed=True, facecolor="white", edgecolor="#111",
            linewidth=1.5, zorder=2,
        ))
        ax.text(d["cx"], d["cy"], d["label"], ha="center", va="center",
                fontsize=10, color="#111", zorder=3)

    for name, meta in entities.items():
        cx, cy = ent_centers[name]
        comment = meta.get("comment") or ""
        label = comment if comment else name
        w = max(1.8, 0.40 * len(label) + 1.0)
        h = 0.85
        ax.add_patch(FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="square,pad=0.02",
            facecolor="white", edgecolor="#111", linewidth=2.0, zorder=2,
        ))
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=12, fontweight="bold", color="#111", zorder=3)

    if watermark:
        ax.text(0.99, 0.01, watermark, transform=ax.transAxes,
                ha="right", va="bottom", fontsize=8, color="#999999")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout(pad=0.5)
    plt.savefig(out_path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: render_chen.py <model.json> <out.png> [watermark] [max_attrs]")
        return 2
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    watermark = sys.argv[3] if len(sys.argv) > 3 else "yanleaf.com"
    if str(watermark).lower() in ("none", "null", "off", ""):
        watermark = None
    max_attrs = 12
    if len(sys.argv) > 4:
        max_attrs = int(sys.argv[4])  # 0 = unlimited
        if max_attrs <= 0:
            max_attrs = None
    raw = json.loads(src.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        from generate_erd import normalize_model
        model = normalize_model(raw)
    elif isinstance(raw, dict) and "entities" in raw:
        model = raw
    else:
        print("Unsupported model format", file=sys.stderr)
        return 1
    print(f"[OK] PNG → {render(model, out, watermark=watermark, max_attrs=max_attrs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
