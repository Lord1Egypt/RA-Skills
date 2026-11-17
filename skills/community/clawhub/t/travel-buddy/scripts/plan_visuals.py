#!/usr/bin/env python3
"""Inline SVG figures drawn from the plan's own numbers.

Why these and not decoration. The delivered page is 96KB of text with zero images and zero
figures, and the things hardest to see in it are the things a traveller most needs to judge:
whether a day is a tight cluster or spread across a city, which day is the heavy one for their
legs, where the money went, and how packed each day is. All four are already IN the plan as
numbers. Nothing had to be researched, licensed, downloaded or invented to draw them -- which is
also why they are separate from the photo tier: a figure derived from the plan cannot be wrong
about the trip in a way the plan is not already wrong, and it costs no network and no bytes.

Every figure here obeys the same four rules, and the first is a scar:

1. **Scale, never truncate.** The route diagram used to be a horizontal SVG needing ~720px to stay
   legible, so on a phone it silently showed the first two stops of the day and looked complete.
   Everything here uses a viewBox with no minimum width, so a narrow screen shrinks the figure
   instead of cropping it.
2. **Degrade to nothing, never to a lie.** A figure with no data returns "" and the page simply
   has one less figure. An axis with invented numbers would be worse than an absent chart.
3. **No renderer-owned English.** Callers pass their own labels, because validate_trip_html.py
   fails any non-English page carrying renderer English -- and an SVG's text nodes are exactly as
   visible as a paragraph's.
4. **Print and screen-reader safe.** Figures carry a title and text alternatives, and use stroke
   plus shape rather than colour alone to distinguish series.
"""

from __future__ import annotations

import html
import math
import re
import urllib.parse

# Amap documents lon,lat; Google, Apple and OpenStreetMap read lat,lon. Same table as
# check_plan_consistency.LON_FIRST_HOSTS, and it matters here for the same reason it mattered
# there: reading one dialect as the other moves a point thousands of kilometres, which in this
# file would silently draw a day's stops as a meaningless scatter rather than fail loudly.
LON_FIRST_HOSTS = ("amap.com", "gaode.com")


def _esc(value: object) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def _lon_first(url: str) -> bool:
    host = urllib.parse.urlparse(url or "").netloc.casefold()
    return any(h in host for h in LON_FIRST_HOSTS)


def _pair(raw: str, lon_first: bool) -> tuple[float, float] | None:
    # Split on a literal comma AFTER unquoting. The first version wrote the separator as the
    # character class [,%2C], meaning "any of , % 2 C" -- so it also split inside the number, and
    # 38.345200 became 38.345 followed by 00. Every longitude came out as 0.0 and every day map
    # would have been drawn along the Greenwich meridian. Caught by reading the extracted
    # coordinates rather than by the figure failing to render: it rendered perfectly.
    parts = [p for p in urllib.parse.unquote(str(raw or "")).strip().split(",") if p.strip()]
    if len(parts) < 2:
        return None
    try:
        first, second = float(parts[0]), float(parts[1])
    except ValueError:
        return None
    lat, lon = (second, first) if lon_first else (first, second)
    if abs(lat) > 90 or abs(lon) > 180:
        return None
    return lat, lon


def stop_coordinates(route: dict) -> list[tuple[str, float, float]]:
    """Every stop of a day as (name, lat, lon), read out of the segment map links.

    Derived rather than added to the contract, because the coordinates are already there: each
    segment's map URL carries its two endpoints, and the endpoint rule in check_plan_consistency
    already forces them to be real coordinates rather than labels. A new required field would be
    one more thing to fill in and one more thing to get wrong.
    """
    stops = [str(s) for s in (route.get("stops_in_order") or []) if s]
    points: dict[int, tuple[float, float]] = {}
    for index, segment in enumerate(route.get("segments") or []):
        if not isinstance(segment, dict):
            continue
        url = str(segment.get("verified_map_url") or "")
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        lon_first = _lon_first(url)
        start = query.get("origin") or query.get("from") or query.get("saddr")
        end = query.get("destination") or query.get("to") or query.get("daddr")
        if start:
            point = _pair(start[0], lon_first)
            if point:
                points.setdefault(index, point)
        if end:
            point = _pair(end[0], lon_first)
            if point:
                points.setdefault(index + 1, point)
    return [(stops[i] if i < len(stops) else f"{i + 1}", lat, lon)
            for i, (lat, lon) in sorted(points.items())]


def day_map(route: dict, title: str, caption: str,
            span_label: str = "straight-line span") -> str:
    """The day's stops at their true relative positions, in visit order.

    The page already lists the stop names in order. What a list cannot show is the shape of the
    day -- whether everything sits within a few hundred metres or the afternoon is a trek across
    town -- and that shape is what decides whether a plan is comfortable. It is drawn from the
    same coordinates the map buttons use, so it cannot disagree with them.

    Longitude is scaled by cos(latitude) so the picture is not stretched east-west; at 38 degrees
    a degree of longitude is 79% of a degree of latitude, and ignoring that would make a
    north-south day look like a diagonal one.
    """
    points = stop_coordinates(route)
    if len(points) < 2:
        return ""
    lats = [p[1] for p in points]
    # Longitudes are unwrapped relative to the first stop before anything is drawn. Without this a
    # day that crosses the 180th meridian -- Fiji, Kiribati, Chukotka, the Chatham Islands -- puts
    # 178.06 and -179.90 at opposite ends of the figure although they are 215 km apart, while the
    # distance caption stays correct because haversine does not care. Measured: two adjacent stops
    # landed 261px apart on a 320px drawing. The map rendered perfectly and was inside out, which
    # is the only kind of wrong this file can produce silently.
    lons = []
    for _, _, lon in points:
        if lons:
            while lon - lons[0] > 180:
                lon -= 360
            while lon - lons[0] < -180:
                lon += 360
        lons.append(lon)
    points = [(name, lat, lon) for (name, lat, _), lon in zip(points, lons)]
    mid_lat = sum(lats) / len(lats)
    stretch = max(math.cos(math.radians(mid_lat)), 0.05)
    xs = [lon * stretch for lon in lons]
    span_x = max(max(xs) - min(xs), 1e-9)
    span_y = max(max(lats) - min(lats), 1e-9)
    # One scale for both axes keeps the drawing proportional; the smaller span gets padded rather
    # than stretched, so a day along one street reads as a line and not as a square.
    scale = max(span_x, span_y)
    pad = 14.0
    width, height = 320.0, 200.0
    inner_w, inner_h = width - 2 * pad, height - 2 * pad

    def place(lat: float, lon: float) -> tuple[float, float]:
        x = pad + inner_w / 2 + ((lon * stretch) - (min(xs) + span_x / 2)) / scale * inner_w * 0.9
        y = pad + inner_h / 2 - (lat - (min(lats) + span_y / 2)) / scale * inner_h * 0.9
        return x, y

    placed = [(name, *place(lat, lon)) for name, lat, lon in points]
    path = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}"
                    for i, (_, x, y) in enumerate(placed))
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" class="pv-stop"/>'
        f'<text x="{x:.1f}" y="{y + 3.4:.1f}" class="pv-stop-n">{i}</text>'
        for i, (_, x, y) in enumerate(placed, 1))
    # Distance between the two furthest stops, so the figure carries a number and not only a shape.
    furthest = max(
        _haversine(a[1], a[2], b[1], b[2]) for a in points for b in points) if len(points) > 1 else 0
    legend = ", ".join(f"{i}. {name}" for i, (name, _, _) in enumerate(points, 1))
    return (
        f'<figure class="pv-figure pv-map"><svg viewBox="0 0 {width:.0f} {height:.0f}" '
        f'role="img" aria-label="{_esc(title)}: {_esc(legend)}" preserveAspectRatio="xMidYMid meet">'
        f'<title>{_esc(title)}</title>'
        f'<path d="{path}" class="pv-route"/>{dots}</svg>'
        f'<figcaption>{_esc(caption)} · {_esc(span_label)} {furthest:.1f} km</figcaption></figure>')


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return 6371.0 * 2 * math.asin(math.sqrt(a))


def walking_bars(rows: list[tuple[str, float]], cap: float | None,
                 title: str, caption: str, cap_label: str) -> str:
    """Minutes on foot per day, against the traveller's stated ceiling.

    This is the safety-relevant one. A stated walking limit is the constraint whose violation
    strands somebody rather than disappointing them, and a plan once shipped its heaviest day
    labelled as its lightest. The numbers are already computed and already checked; what was
    missing was the one glance that makes "day 3 is nearly double the rest" obvious without
    reading five day cards and adding up.
    """
    # Rows are unpacked defensively rather than trusted. Today every caller builds them inline so
    # a malformed row cannot reach here, but this file's neighbours all hold to the same rule:
    # malformed input produces a finding or an empty figure, never a traceback, because an
    # operator who sees a stack trace learns nothing and stops running the thing.
    rows = [(str(row[0]), float(row[1])) for row in rows
            if isinstance(row, (list, tuple)) and len(row) == 2
            and isinstance(row[1], (int, float)) and not isinstance(row[1], bool)]
    if not rows:
        return ""
    peak = max([value for _, value in rows] + ([cap] if cap else []) + [1.0])
    bar_h, gap = 22.0, 8.0
    width = 320.0
    label_w = 58.0
    height = len(rows) * (bar_h + gap) + 16
    bars = []
    for index, (label, value) in enumerate(rows):
        y = index * (bar_h + gap) + 4
        length = (width - label_w - 42) * (value / peak)
        over = cap is not None and value > cap
        bars.append(
            f'<text x="0" y="{y + bar_h * 0.7:.1f}" class="pv-axis">{_esc(label)}</text>'
            f'<rect x="{label_w}" y="{y:.1f}" width="{max(length, 1):.1f}" height="{bar_h:.1f}" '
            f'rx="4" class="pv-bar{" pv-over" if over else ""}"/>'
            f'<text x="{label_w + max(length, 1) + 6:.1f}" y="{y + bar_h * 0.7:.1f}" '
            f'class="pv-val">{value:.0f}</text>')
    rule = ""
    if cap:
        x = label_w + (width - label_w - 42) * (cap / peak)
        rule = (f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{height - 12:.1f}" class="pv-cap"/>'
                f'<text x="{x:.1f}" y="{height - 2:.1f}" class="pv-axis pv-cap-label">'
                f'{_esc(cap_label)}</text>')
    alt = "; ".join(f"{label} {value:.0f}" for label, value in rows)
    return (f'<figure class="pv-figure pv-bars"><svg viewBox="0 0 {width:.0f} {height:.0f}" '
            f'role="img" aria-label="{_esc(title)}: {_esc(alt)}" preserveAspectRatio="xMidYMid meet">'
            f'<title>{_esc(title)}</title>{"".join(bars)}{rule}</svg>'
            f'<figcaption>{_esc(caption)}</figcaption></figure>')


def budget_bar(rows: list[tuple[str, float]], total: float, cap: float | None,
               title: str, caption: str) -> str:
    """Where the money went, as one proportional strip.

    The breakdown table is exact and hard to read at a glance; this answers "is this a flights
    trip or a hotel trip" in one look, and shows the headroom against a stated cap -- the number
    a traveller actually acts on.
    """
    rows = [(str(row[0]), float(row[1])) for row in rows
            if isinstance(row, (list, tuple)) and len(row) == 2
            and isinstance(row[1], (int, float)) and not isinstance(row[1], bool) and row[1]]
    if not rows or total <= 0:
        return ""
    width, height = 320.0, 46.0
    x = 0.0
    blocks, keys = [], []
    for index, (label, value) in enumerate(rows):
        span = width * (value / total)
        blocks.append(f'<rect x="{x:.1f}" y="0" width="{max(span, 0.6):.1f}" height="20" '
                      f'class="pv-seg pv-seg-{index % 6}"/>')
        keys.append(f'<span class="pv-key pv-key-{index % 6}">{_esc(label)} {value:.0f}</span>')
        x += span
    headroom = ""
    if cap and cap > 0:
        share = min(total / cap, 1.0)
        headroom = (f'<rect x="0" y="28" width="{width:.0f}" height="8" rx="4" class="pv-cap-track"/>'
                    f'<rect x="0" y="28" width="{width * share:.1f}" height="8" rx="4" '
                    f'class="pv-cap-fill{" pv-over" if total > cap else ""}"/>')
    alt = "; ".join(f"{label} {value:.0f}" for label, value in rows)
    return (f'<figure class="pv-figure pv-budget"><svg viewBox="0 0 {width:.0f} {height:.0f}" '
            f'role="img" aria-label="{_esc(title)}: {_esc(alt)}" preserveAspectRatio="none">'
            f'<title>{_esc(title)}</title>{"".join(blocks)}{headroom}</svg>'
            f'<div class="pv-keys">{"".join(keys)}</div>'
            f'<figcaption>{_esc(caption)}</figcaption></figure>')


def _minutes(value: object) -> int | None:
    match = re.match(r"^\s*(\d{1,2})[:：](\d{2})", str(value or ""))
    if not match:
        return None
    hour, minute = int(match.group(1)), int(match.group(2))
    return hour * 60 + minute if 0 <= hour < 24 and 0 <= minute < 60 else None


def day_timeline(entries: list[tuple[str, object, str]], title: str, caption: str) -> str:
    """When the day's fixed points fall, on one clock line.

    A list of times reads as a sequence; the same times on an axis read as a shape, and the shape
    is what shows a four-hour hole after lunch or three things stacked into one morning. Entries
    that carry no clock time are counted in the caption rather than placed, because putting a
    flexible item at an invented hour would be the chart telling a story the plan does not.
    """
    day_start, day_end = 7 * 60, 23 * 60
    placed = [(str(row[0]), _minutes(row[1]), str(row[2])) for row in entries
              if isinstance(row, (list, tuple)) and len(row) == 3]
    timed = [(kind, minute, label) for kind, minute, label in placed if minute is not None]
    if not timed:
        return ""
    width, height = 320.0, 44.0
    def x_of(minute: int) -> float:
        return max(0.0, min(1.0, (minute - day_start) / (day_end - day_start))) * (width - 8) + 4
    ticks = "".join(
        f'<line x1="{x_of(h * 60):.1f}" y1="14" x2="{x_of(h * 60):.1f}" y2="20" class="pv-tick"/>'
        f'<text x="{x_of(h * 60):.1f}" y="32" class="pv-axis pv-tick-label">{h}</text>'
        for h in range(8, 23, 3))
    marks = "".join(
        f'<circle cx="{x_of(minute):.1f}" cy="10" r="5" class="pv-mark pv-mark-{_esc(kind)}">'
        f'<title>{_esc(label)}</title></circle>'
        for kind, minute, label in timed)
    untimed = len(placed) - len(timed)
    tail = f" · +{untimed}" if untimed else ""
    alt = "; ".join(f"{label} {minute // 60:02d}:{minute % 60:02d}" for _, minute, label in timed)
    return (f'<figure class="pv-figure pv-timeline"><svg viewBox="0 0 {width:.0f} {height:.0f}" '
            f'role="img" aria-label="{_esc(title)}: {_esc(alt)}" preserveAspectRatio="xMidYMid meet">'
            f'<title>{_esc(title)}</title>'
            f'<line x1="4" y1="10" x2="{width - 4:.0f}" y2="10" class="pv-rail"/>{ticks}{marks}</svg>'
            f'<figcaption>{_esc(caption)}{tail}</figcaption></figure>')


# Kept beside the figures rather than in the page's main stylesheet, so a change to a figure and
# the change to its styling are one edit. Colour never carries meaning alone: the over-cap state
# is a different fill AND a dashed rule, and the budget keys repeat their label as text.
VISUAL_CSS = (
    ".pv-figure{margin:14px 0 0;padding:0}"
    ".pv-figure svg{display:block;width:100%;height:auto;max-width:420px}"
    ".pv-figure figcaption{color:var(--muted);font-size:.84rem;margin-top:4px}"
    ".pv-route{fill:none;stroke:var(--accent);stroke-width:2.5;stroke-linejoin:round;"
    "stroke-linecap:round;stroke-dasharray:5 4}"
    ".pv-stop{fill:var(--accent);stroke:#fff;stroke-width:2}"
    ".pv-stop-n{fill:#fff;font-size:9px;font-weight:800;text-anchor:middle}"
    ".pv-axis{fill:var(--muted);font-size:10px}"
    ".pv-val{fill:var(--ink);font-size:10px;font-weight:700}"
    ".pv-bar{fill:var(--accent)}"
    ".pv-bar.pv-over{fill:var(--warn)}"
    ".pv-cap{stroke:var(--warn);stroke-width:1.5;stroke-dasharray:3 3}"
    ".pv-cap-label{text-anchor:middle;fill:var(--warn)}"
    ".pv-seg{stroke:#fff;stroke-width:1}"
    ".pv-seg-0{fill:#0b6e69}.pv-seg-1{fill:#3f8f8a}.pv-seg-2{fill:#6fb0aa}"
    ".pv-seg-3{fill:#9dcbc6}.pv-seg-4{fill:#c6e2df}.pv-seg-5{fill:#e4f4f1}"
    ".pv-cap-track{fill:var(--line)}.pv-cap-fill{fill:var(--accent)}"
    ".pv-cap-fill.pv-over{fill:var(--warn)}"
    ".pv-keys{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:6px}"
    ".pv-key{font-size:.78rem;color:var(--muted);display:inline-flex;align-items:center;gap:4px}"
    ".pv-key::before{content:'';width:9px;height:9px;border-radius:2px;background:currentColor}"
    ".pv-key-0::before{background:#0b6e69}.pv-key-1::before{background:#3f8f8a}"
    ".pv-key-2::before{background:#6fb0aa}.pv-key-3::before{background:#9dcbc6}"
    ".pv-key-4::before{background:#c6e2df}.pv-key-5::before{background:#e4f4f1}"
    ".pv-rail{stroke:var(--line);stroke-width:2}"
    ".pv-tick{stroke:var(--line);stroke-width:1}"
    ".pv-tick-label{text-anchor:middle}"
    ".pv-mark{fill:var(--accent);stroke:#fff;stroke-width:1.5}"
    ".pv-mark-meal{fill:var(--warn)}"
    "@media print{.pv-figure svg{max-width:320px}}"
)
