#!/usr/bin/env python3
"""Draw polygon, line, and point overlays on an SVG base map."""
import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import svg_bbox

NEUTRAL_FILL = "#EDEAE3"
NEUTRAL_STROKE = "#B9B3A6"
BOUNDARY_FILL = "#C0392B"
BOUNDARY_STROKE = "#7B241C"


def to_px(coef_x, coef_y, lon, lat):
    ax, bx, cx = coef_x
    ay, by, cy = coef_y
    return ax * lon + bx * lat + cx, ay * lon + by * lat + cy


def normalize_features(raw):
    if isinstance(raw, dict) and "features" in raw:
        return raw["features"]
    if isinstance(raw, list) and raw and isinstance(raw[0], list) and raw[0] and isinstance(raw[0][0], (int, float)):
        return [{"type": "polygon", "coordinates": [raw]}]
    if isinstance(raw, list):
        return [{"type": "polygon", "coordinates": raw}]
    raise ValueError("Unsupported boundary JSON format")


def path_from_coords(coords, coef_x, coef_y, close):
    pts_px = [to_px(coef_x, coef_y, lon, lat) for lon, lat in coords]
    if not pts_px:
        return ""
    suffix = " Z" if close else ""
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts_px) + suffix


def recolor_neutral(svg):
    def repl(m):
        tag = m.group(0)
        tag = re.sub(r'fill="[^"]*"', f'fill="{NEUTRAL_FILL}"', tag) if 'fill="' in tag else tag[:-1] + f' fill="{NEUTRAL_FILL}">'
        tag = re.sub(r'stroke="[^"]*"', f'stroke="{NEUTRAL_STROKE}"', tag) if 'stroke="' in tag else tag[:-1] + f' stroke="{NEUTRAL_STROKE}">'
        return tag
    return re.sub(r'<path\b[^>]*>', repl, svg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("in_svg")
    ap.add_argument("transform_json")
    ap.add_argument("boundary_json")
    ap.add_argument("out_svg")
    ap.add_argument("--title", default="")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--legend-inside", default="Inside the boundary")
    ap.add_argument("--legend-outside", default="Outside the boundary")
    ap.add_argument("--note", default="")
    ap.add_argument("--mark", action="append", default=[])
    args = ap.parse_args()

    svg = Path(args.in_svg).read_text(encoding="utf-8")
    t = json.loads(Path(args.transform_json).read_text(encoding="utf-8"))
    features = normalize_features(json.loads(Path(args.boundary_json).read_text(encoding="utf-8")))
    new_svg = recolor_neutral(svg)
    minx, maxx, miny, maxy = svg_bbox(svg)

    overlay_svg = []
    labels_svg = []
    for feat in features:
        ftype = feat.get("type", "polygon").lower()
        dash = ' stroke-dasharray="6 4"' if feat.get("dash") else ""
        label = feat.get("label")
        if ftype == "point":
            lon, lat = feat["coordinates"]
            mx, my = to_px(t["coef_x"], t["coef_y"], float(lon), float(lat))
            overlay_svg.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="3.8" fill="{BOUNDARY_STROKE}" stroke="#4A140F" stroke-width="0.7"/>')
            if label:
                labels_svg.append(f'<text x="{mx+8:.1f}" y="{my+4:.1f}" font-family="Arial, sans-serif" font-size="11" fill="#3a2a1a">{html.escape(str(label))}</text>')
            continue
        rings = feat.get("coordinates", [])
        if ftype == "line":
            rings = [rings]
        for ring in rings:
            d = path_from_coords(ring, t["coef_x"], t["coef_y"], ftype == "polygon")
            if not d:
                continue
            fill = BOUNDARY_FILL if ftype == "polygon" else "none"
            fill_opacity = ' fill-opacity="0.30"' if ftype == "polygon" else ""
            overlay_svg.append(
                f'<path d="{d}" fill="{fill}"{fill_opacity} stroke="{BOUNDARY_STROKE}" '
                f'stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"{dash}/>'
            )

    markers_svg = []
    for spec in args.mark:
        lon_s, lat_s, label = spec.split(",", 2)
        mx, my = to_px(t["coef_x"], t["coef_y"], float(lon_s), float(lat_s))
        markers_svg.append(
            f'<path d="M {mx:.1f},{my-7:.1f} l1.8,4.2 4.6,0.4 -3.5,3 1.1,4.4 '
            f'-3.9,-2.5 -3.9,2.5 1.1,-4.4 -3.5,-3 4.6,-0.4 Z" '
            f'fill="{BOUNDARY_STROKE}" stroke="#4A140F" stroke-width="0.5"/>'
            f'<text x="{mx+9:.1f}" y="{my+4:.1f}" font-family="Georgia, serif" '
            f'font-size="12" font-weight="bold" fill="#3a2a1a">{html.escape(label)}</text>'
        )

    header, footer, pad = 70, 130, 10
    legend_y = maxy + 20
    note_svg = (
        f'<text x="{minx}" y="{legend_y+58}" font-family="Georgia, serif" font-size="9" '
        f'fill="#8a7a6a">{html.escape(args.note)}</text>' if args.note else ""
    )
    extras = f'''
<g id="title-block">
  <text x="{minx}" y="{miny - header + 28}" font-family="Georgia, serif" font-size="21" font-weight="bold" fill="#2b2118">{html.escape(args.title)}</text>
  <text x="{minx}" y="{miny - header + 48}" font-family="Georgia, serif" font-size="12" fill="#5a4a3a">{html.escape(args.subtitle)}</text>
</g>
{"".join(overlay_svg)}
{"".join(labels_svg)}
{"".join(markers_svg)}
<g id="legend" transform="translate({minx},{legend_y})">
  <rect x="0" y="0" width="16" height="16" fill="{BOUNDARY_FILL}" fill-opacity="0.30" stroke="{BOUNDARY_STROKE}" stroke-width="2"/>
  <text x="22" y="13" font-family="Georgia, serif" font-size="12" fill="#2b2118">{html.escape(args.legend_inside)}</text>
  <rect x="0" y="24" width="16" height="16" fill="{NEUTRAL_FILL}" stroke="{NEUTRAL_STROKE}" stroke-width="1"/>
  <text x="22" y="37" font-family="Georgia, serif" font-size="12" fill="#2b2118">{html.escape(args.legend_outside)}</text>
</g>
{note_svg}
'''
    new_svg = new_svg.rsplit("</svg>", 1)[0] + extras + "\n</svg>"
    vb = f'{minx - pad} {miny - header} {(maxx - minx) + 2*pad} {(maxy - miny) + header + footer}'
    if "viewBox=" in new_svg:
        new_svg = re.sub(r'viewBox="[^"]*"', f'viewBox="{vb}"', new_svg, count=1)
    else:
        new_svg = re.sub(r'(<svg\b)', rf'\1 viewBox="{vb}"', new_svg, count=1)
    Path(args.out_svg).write_text(new_svg, encoding="utf-8")
    print(f"Wrote {args.out_svg} ({len(features)} overlay feature(s))")


if __name__ == "__main__":
    main()

