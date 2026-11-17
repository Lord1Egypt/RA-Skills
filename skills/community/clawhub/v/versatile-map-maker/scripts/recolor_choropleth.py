#!/usr/bin/env python3
"""Recolor SVG map regions from id -> value JSON."""
import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import extract_paths, svg_bbox

QUALITATIVE = ["#4C72B0", "#F28E2B", "#59A14F", "#E15759", "#76B7B2",
               "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC"]
SEQUENTIAL = {
    "YlOrRd": ["#ffffcc", "#ffeda0", "#fed976", "#feb24c", "#fd8d3c", "#f03b20", "#bd0026"],
    "Blues": ["#eff3ff", "#bdd7e7", "#6baed6", "#3182bd", "#08519c"],
    "Greens": ["#edf8e9", "#bae4b3", "#74c476", "#31a354", "#006d2c"],
    "Greys": ["#f7f7f7", "#cccccc", "#969696", "#636363", "#252525"],
    "Viridis": ["#440154", "#414487", "#2a788e", "#22a884", "#7ad151", "#fde725"],
    "viridis": ["#440154", "#414487", "#2a788e", "#22a884", "#7ad151", "#fde725"],
}
DEFAULT_STYLE = {
    "font_family": "Arial, sans-serif",
    "neutral_fill": "#EDEAE3",
    "neutral_stroke": "#B9B3A6",
    "title_fill": "#1a1a1a",
    "subtitle_fill": "#555555",
    "legend_fill": "#333333",
    "qualitative": QUALITATIVE,
}


def load_style(path):
    style = dict(DEFAULT_STYLE)
    if path:
        style.update(json.loads(Path(path).read_text(encoding="utf-8")))
    return style


def set_path_style(svg, region_ids_colors, style):
    def repl(m):
        tag = m.group(0)
        id_m = re.search(r'id="([^"]+)"', tag)
        if not id_m:
            return tag
        rid = id_m.group(1)
        fill = region_ids_colors.get(rid, style["neutral_fill"])
        tag = re.sub(r'fill="[^"]*"', f'fill="{fill}"', tag) if 'fill="' in tag else tag[:-1] + f' fill="{fill}">'
        stroke = "#7a7a7a" if rid in region_ids_colors else style["neutral_stroke"]
        tag = re.sub(r'stroke="[^"]*"', f'stroke="{stroke}"', tag) if 'stroke="' in tag else tag[:-1] + f' stroke="{stroke}">'
        return tag
    return re.sub(r'<path\b[^>]*>', repl, svg)


def hex_to_rgb(color):
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, int(round(c)))):02x}" for c in rgb)


def interp_palette(colors, t):
    colors = [hex_to_rgb(c) for c in colors]
    if t <= 0:
        return rgb_to_hex(colors[0])
    if t >= 1:
        return rgb_to_hex(colors[-1])
    pos = t * (len(colors) - 1)
    i = int(pos)
    frac = pos - i
    return rgb_to_hex(tuple(colors[i][j] + (colors[i + 1][j] - colors[i][j]) * frac for j in range(3)))


def build_legend_numeric(cmap_name, vmin, vmax, label, x, y, style):
    palette = SEQUENTIAL.get(cmap_name, SEQUENTIAL["YlOrRd"])
    stops = "\n".join(
        f'<stop offset="{t*100:.0f}%" stop-color="{interp_palette(palette, t)}"/>'
        for t in [i / 10 for i in range(11)]
    )
    font = html.escape(style["font_family"])
    return f'''
<defs><linearGradient id="legendGrad" x1="0%" y1="0%" x2="100%" y2="0%">{stops}</linearGradient></defs>
<g transform="translate({x},{y})">
  <text x="0" y="-6" font-family="{font}" font-size="11" fill="{style["legend_fill"]}">{html.escape(label)}</text>
  <rect x="0" y="0" width="300" height="14" fill="url(#legendGrad)" stroke="#888" stroke-width="0.5"/>
  <text x="0" y="28" font-family="{font}" font-size="10" fill="{style["legend_fill"]}">{vmin:.3g}</text>
  <text x="285" y="28" font-family="{font}" font-size="10" fill="{style["legend_fill"]}">{vmax:.3g}</text>
</g>'''


def build_legend_categorical(categories, colors, x, y, style):
    font = html.escape(style["font_family"])
    rows = []
    for i, (cat, col) in enumerate(zip(categories, colors)):
        ry = i * 20
        rows.append(f'<rect x="0" y="{ry}" width="14" height="14" fill="{col}" stroke="#888" stroke-width="0.5"/>')
        rows.append(f'<text x="20" y="{ry+12}" font-family="{font}" font-size="11" fill="{style["legend_fill"]}">{html.escape(str(cat))}</text>')
    return f'<g transform="translate({x},{y})">' + "\n".join(rows) + "</g>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("in_svg")
    ap.add_argument("data_json")
    ap.add_argument("out_svg")
    ap.add_argument("--title", default="")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--legend-label", default="Value")
    ap.add_argument("--cmap", default="YlOrRd")
    ap.add_argument("--style", help="Optional JSON file with colors/font settings")
    ap.add_argument("--missing-fill", help="Override fill for regions missing data")
    args = ap.parse_args()

    style = load_style(args.style)
    if args.missing_fill:
        style["neutral_fill"] = args.missing_fill

    svg = Path(args.in_svg).read_text(encoding="utf-8")
    data = json.loads(Path(args.data_json).read_text(encoding="utf-8"))
    present_ids = {pid for pid, _ in extract_paths(svg)}
    missing = [k for k in data if k not in present_ids]
    if missing:
        print(f"Warning: {len(missing)} id(s) in data.json do not match SVG paths: {missing[:10]}", file=sys.stderr)
    data = {k: v for k, v in data.items() if k in present_ids}
    if not data:
        print("No data ids matched the SVG region ids.", file=sys.stderr)
        sys.exit(1)

    values = list(data.values())
    is_numeric = all(isinstance(v, (int, float)) for v in values)
    if is_numeric:
        vmin, vmax = min(values), max(values)
        palette = SEQUENTIAL.get(args.cmap, SEQUENTIAL["YlOrRd"])
        span = (vmax - vmin) or 1.0
        colors = {k: interp_palette(palette, (v - vmin) / span) for k, v in data.items()}
    else:
        cats = sorted(set(values), key=lambda x: str(x))
        palette = {c: style["qualitative"][i % len(style["qualitative"])] for i, c in enumerate(cats)}
        colors = {k: palette[v] for k, v in data.items()}

    new_svg = set_path_style(svg, colors, style)
    minx, maxx, miny, maxy = svg_bbox(svg)
    header, footer, pad = 70, 110, 10

    if is_numeric:
        legend_svg = build_legend_numeric(args.cmap, vmin, vmax, args.legend_label, minx, maxy + 20, style)
    else:
        legend_svg = build_legend_categorical(cats, [palette[c] for c in cats], minx, maxy + 20, style)

    font = html.escape(style["font_family"])
    extras = f'''
<g id="title-block">
  <text x="{minx}" y="{miny - header + 28}" font-family="{font}" font-size="20" font-weight="bold" fill="{style["title_fill"]}">{html.escape(args.title)}</text>
  <text x="{minx}" y="{miny - header + 48}" font-family="{font}" font-size="12" fill="{style["subtitle_fill"]}">{html.escape(args.subtitle)}</text>
</g>
{legend_svg}
'''
    new_svg = new_svg.rsplit("</svg>", 1)[0] + extras + "\n</svg>"
    vb = f'{minx - pad} {miny - header} {(maxx - minx) + 2*pad} {(maxy - miny) + header + footer}'
    if "viewBox=" in new_svg:
        new_svg = re.sub(r'viewBox="[^"]*"', f'viewBox="{vb}"', new_svg, count=1)
    else:
        new_svg = re.sub(r'(<svg\b)', rf'\1 viewBox="{vb}"', new_svg, count=1)

    Path(args.out_svg).write_text(new_svg, encoding="utf-8")
    print(f"Wrote {args.out_svg} ({'numeric' if is_numeric else 'categorical'}, {len(data)} regions colored)")


if __name__ == "__main__":
    main()
