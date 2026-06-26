#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

GRID_X = 120
GRID_Y = 80
PADDING = 40
FONT_FAMILY = "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

NODE_STYLES = {
    "service": {"fill": "#ffffff", "stroke": "#1f2937", "text": "#111827"},
    "llm": {"fill": "#ffffff", "stroke": "#0f172a", "text": "#0f172a"},
    "agent": {"fill": "#f8fafc", "stroke": "#0f172a", "text": "#0f172a"},
    "memory": {"fill": "#f8fafc", "stroke": "#14532d", "text": "#14532d"},
}

EDGE_STYLES = {
    "primary-data": {"stroke": "#2563eb", "dash": None, "label_fill": "#dbeafe", "label_text": "#1d4ed8"},
    "memory-write": {"stroke": "#16a34a", "dash": "10 8", "label_fill": "#dcfce7", "label_text": "#166534"},
    "control": {"stroke": "#475569", "dash": "6 6", "label_fill": "#e2e8f0", "label_text": "#334155"},
}


def snap(value, grid):
    return round(value / grid) * grid


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def text_width(text, font_size):
    return max(36, int(len(text) * font_size * 0.58))


def node_box(node):
    title = node["label"]
    subtitle = node.get("subtitle", "")
    width = max(180, text_width(title, 18) + 48, text_width(subtitle, 13) + 48 if subtitle else 0)
    height = 76 if subtitle else 56
    return width, height


def position_nodes(nodes):
    placed = {}
    for node in nodes:
        x = snap(node.get("x", 0), GRID_X)
        y = snap(node.get("y", 0), GRID_Y)
        width, height = node_box(node)
        placed[node["id"]] = {**node, "x": x, "y": y, "width": width, "height": height}
    return placed


def anchor(node, side):
    x = node["x"]
    y = node["y"]
    w = node["width"]
    h = node["height"]
    if side == "left":
        return x - w / 2, y
    if side == "right":
        return x + w / 2, y
    if side == "top":
        return x, y - h / 2
    return x, y + h / 2


def choose_sides(source, target):
    dx = target["x"] - source["x"]
    dy = target["y"] - source["y"]
    if abs(dx) >= abs(dy):
        return ("right", "left") if dx >= 0 else ("left", "right")
    return ("bottom", "top") if dy >= 0 else ("top", "bottom")


def clean_points(points):
    cleaned = [points[0]]
    for point in points[1:]:
        if point != cleaned[-1]:
            cleaned.append(point)

    final = [cleaned[0]]
    for point in cleaned[1:]:
        if len(final) >= 2:
            ax, ay = final[-2]
            bx, by = final[-1]
            cx, cy = point
            if (ax == bx == cx) or (ay == by == cy):
                final[-1] = point
                continue
        final.append(point)
    return final


def orthogonal_points(source, target, edge=None):
    edge = edge or {}
    source_side = edge.get("source_side")
    target_side = edge.get("target_side")
    if not source_side or not target_side:
        auto_source, auto_target = choose_sides(source, target)
        source_side = source_side or auto_source
        target_side = target_side or auto_target

    sx, sy = anchor(source, source_side)
    tx, ty = anchor(target, target_side)
    points = [(sx, sy)]

    via = edge.get("via", [])
    if via:
        for point in via:
            points.append((snap(point["x"], GRID_X), snap(point["y"], GRID_Y)))
    elif source_side in ("left", "right"):
        dogleg = snap((sx + tx) / 2, GRID_X)
        points.extend([(dogleg, sy), (dogleg, ty)])
    else:
        dogleg = snap((sy + ty) / 2, GRID_Y)
        points.extend([(sx, dogleg), (tx, dogleg)])

    points.append((tx, ty))
    return clean_points(points)


def path_d(points):
    return " ".join([f"M {points[0][0]:.1f} {points[0][1]:.1f}"] + [f"L {x:.1f} {y:.1f}" for x, y in points[1:]])


def segment_midpoint(points, index=None):
    segments = list(zip(points, points[1:]))
    if not segments:
        return points[0]
    if index is not None:
        index = max(0, min(index, len(segments) - 1))
        a, b = segments[index]
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    max_len = -1
    best = (points[0][0], points[0][1])
    for a, b in segments:
        length = abs(b[0] - a[0]) + abs(b[1] - a[1])
        if length > max_len:
            max_len = length
            best = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    return best


def arrow_head(a, b, size=9):
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    left = (b[0] - size * math.cos(angle) + size * 0.6 * math.sin(angle),
            b[1] - size * math.sin(angle) - size * 0.6 * math.cos(angle))
    right = (b[0] - size * math.cos(angle) - size * 0.6 * math.sin(angle),
             b[1] - size * math.sin(angle) + size * 0.6 * math.cos(angle))
    return left, b, right


def render_node(node):
    style = NODE_STYLES.get(node.get("kind", "service"), NODE_STYLES["service"])
    x = node["x"]
    y = node["y"]
    w = node["width"]
    h = node["height"]
    left = x - w / 2
    top = y - h / 2
    shape_parts = []
    label_parts = []
    kind = node.get("kind", "service")

    if kind == "llm":
        shape_parts.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" rx="16" fill="{style["fill"]}" stroke="{style["stroke"]}" stroke-width="2"/>')
        shape_parts.append(f'<rect x="{left+6:.1f}" y="{top+6:.1f}" width="{w-12:.1f}" height="{h-12:.1f}" rx="12" fill="none" stroke="{style["stroke"]}" stroke-width="1.5"/>')
    elif kind == "agent":
        cut = min(22, w * 0.14)
        points = [
            (left + cut, top), (left + w - cut, top), (left + w, y),
            (left + w - cut, top + h), (left + cut, top + h), (left, y)
        ]
        points_str = " ".join(f"{px:.1f},{py:.1f}" for px, py in points)
        shape_parts.append(f'<polygon points="{points_str}" fill="{style["fill"]}" stroke="{style["stroke"]}" stroke-width="2"/>')
    elif kind == "memory":
        rx = w / 2
        ry = 12
        cx = x
        top_y = top + ry
        bottom_y = top + h - ry
        shape_parts.append(f'<path d="M {left:.1f} {top_y:.1f} A {rx:.1f} {ry:.1f} 0 0 1 {left+w:.1f} {top_y:.1f} L {left+w:.1f} {bottom_y:.1f} A {rx:.1f} {ry:.1f} 0 0 1 {left:.1f} {bottom_y:.1f} Z" fill="{style["fill"]}" stroke="{style["stroke"]}" stroke-width="2"/>')
        shape_parts.append(f'<ellipse cx="{cx:.1f}" cy="{top_y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{style["fill"]}" stroke="{style["stroke"]}" stroke-width="2"/>')
        shape_parts.append(f'<path d="M {left:.1f} {bottom_y:.1f} A {rx:.1f} {ry:.1f} 0 0 0 {left+w:.1f} {bottom_y:.1f}" fill="none" stroke="{style["stroke"]}" stroke-width="2"/>')
    else:
        shape_parts.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="{style["fill"]}" stroke="{style["stroke"]}" stroke-width="2"/>')

    label_parts.append(f'<text x="{x:.1f}" y="{y - (4 if node.get("subtitle") else -6):.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="18" font-weight="600" fill="{style["text"]}">{escape(node["label"])}</text>')
    if node.get("subtitle"):
        label_parts.append(f'<text x="{x:.1f}" y="{y + 18:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="13" font-weight="500" fill="#475569">{escape(node["subtitle"])}</text>')
    return "\n".join(shape_parts), "\n".join(label_parts)


def render_edge(edge, nodes):
    source = nodes[edge["from"]]
    target = nodes[edge["to"]]
    points = orthogonal_points(source, target, edge)
    style = EDGE_STYLES.get(edge.get("kind", "control"), EDGE_STYLES["control"])
    edge_parts = []
    label_parts = []
    dash = f' stroke-dasharray="{style["dash"]}"' if style["dash"] else ""
    edge_parts.append(f'<path d="{path_d(points)}" fill="none" stroke="{style["stroke"]}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"{dash}/>')
    left, tip, right = arrow_head(points[-2], points[-1])
    edge_parts.append(f'<polygon points="{left[0]:.1f},{left[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} {right[0]:.1f},{right[1]:.1f}" fill="{style["stroke"]}"/>')
    if edge.get("label"):
        lx, ly = segment_midpoint(points, edge.get("label_segment"))
        dx, dy = edge.get("label_offset", [0, 0])
        lx += dx
        ly += dy
        label = edge["label"]
        width = text_width(label, 12) + 18
        height = 24
        label_parts.append(f'<rect x="{lx - width/2:.1f}" y="{ly - height/2:.1f}" width="{width:.1f}" height="{height:.1f}" rx="6" fill="{style["label_fill"]}" stroke="#ffffff" stroke-width="2"/>')
        label_parts.append(f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="12" font-weight="600" fill="{style["label_text"]}">{escape(label)}</text>')
    return "\n".join(edge_parts), "\n".join(label_parts)


def render(data):
    nodes = position_nodes(data["nodes"])
    xs = [n["x"] for n in nodes.values()]
    ys = [n["y"] for n in nodes.values()]
    widths = [n["width"] for n in nodes.values()]
    heights = [n["height"] for n in nodes.values()]
    min_x = min(x - w / 2 for x, w in zip(xs, widths)) - PADDING
    max_x = max(x + w / 2 for x, w in zip(xs, widths)) + PADDING
    min_y = min(y - h / 2 for y, h in zip(ys, heights)) - PADDING
    max_y = max(y + h / 2 for y, h in zip(ys, heights)) + PADDING
    width = max_x - min_x
    height = max_y - min_y

    edge_shapes = []
    edge_labels = []
    for edge in data.get("edges", []):
        shape_svg, label_svg = render_edge(edge, nodes)
        edge_shapes.append(shape_svg)
        if label_svg:
            edge_labels.append(label_svg)

    node_shapes = []
    node_labels = []
    for node in nodes.values():
        shape_svg, label_svg = render_node(node)
        node_shapes.append(shape_svg)
        if label_svg:
            node_labels.append(label_svg)

    title = escape(data.get("title", "Architecture"))
    edge_shapes_svg = indent("\n".join(edge_shapes), 4)
    node_shapes_svg = indent("\n".join(node_shapes), 4)
    labels_svg = indent("\n".join(edge_labels + node_labels), 4)

    show_grid = data.get("show_grid", False)
    grid_svg = ""
    if show_grid:
        grid_svg = f'\n  <rect x="{min_x:.1f}" y="{min_y:.1f}" width="{width:.1f}" height="{height:.1f}" fill="url(#grid)" opacity="0.85"/>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.1f}" height="{height:.1f}" viewBox="{min_x:.1f} {min_y:.1f} {width:.1f} {height:.1f}" role="img" aria-label="{title}">
  <defs>
    <pattern id="grid" width="{GRID_X}" height="{GRID_Y}" patternUnits="userSpaceOnUse">
      <path d="M {GRID_X} 0 L 0 0 0 {GRID_Y}" fill="none" stroke="#e5e7eb" stroke-width="1"/>
    </pattern>
  </defs>
  <rect x="{min_x:.1f}" y="{min_y:.1f}" width="{width:.1f}" height="{height:.1f}" fill="#f8fafc"/>{grid_svg}
  <g id="arrows">
{edge_shapes_svg}
  </g>
  <g id="nodes">
{node_shapes_svg}
  </g>
  <g id="labels">
{labels_svg}
  </g>
</svg>
'''


def indent(text, spaces):
    prefix = " " * spaces
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def main():
    parser = argparse.ArgumentParser(description="Render architecture JSON to SVG")
    parser.add_argument("input", help="Path to architecture JSON")
    parser.add_argument("output", help="Path to output SVG")
    args = parser.parse_args()

    data = load(args.input)
    svg = render(data)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
