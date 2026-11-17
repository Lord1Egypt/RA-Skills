"""Small, bounded SVG vocabulary for printable primary-school visual tasks."""

from __future__ import annotations

import html
import math


EXTENDED_TYPES = {"shape_collection", "clock", "number_line", "grid", "polygon"}
SUPPORTED_GEOMETRY = {"rectangle", "composite_rect", *EXTENDED_TYPES}


def number(value: object, name: str, low: float, high: float) -> float:
    if type(value) not in {int, float} or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name} must be a finite number in [{low}, {high}]")
    return float(value)


def integer(value: object, name: str, low: int, high: int) -> int:
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer")
    return int(number(value, name, low, high))


def validate_geometry(spec: dict) -> None:
    if not isinstance(spec, dict) or spec.get("type") not in SUPPORTED_GEOMETRY:
        raise ValueError("unsupported geometry_spec type")
    if "answer_detail" in spec:
        raise ValueError("geometry_spec must not contain answer_detail")
    width = number(spec.get("canvas_width", 320), "canvas_width", 100, 1600)
    height = number(spec.get("canvas_height", 180), "canvas_height", 80, 1600)
    kind = spec["type"]
    if kind == "shape_collection":
        shapes = spec.get("shapes")
        if not isinstance(shapes, list) or not 1 <= len(shapes) <= 40:
            raise ValueError("shape_collection requires 1..40 shapes")
        for shape in shapes:
            if not isinstance(shape, dict) or shape.get("kind") not in {"circle", "triangle", "square", "rectangle"}:
                raise ValueError("shape kind must be circle, triangle, square or rectangle")
            x = number(shape.get("x"), "shape.x", 2, width - 2)
            y = number(shape.get("y"), "shape.y", 2, height - 2)
            w = number(shape.get("width", 30), "shape.width", 4, width)
            h = number(shape.get("height", 30), "shape.height", 4, height)
            if x + w > width - 2 or y + h > height - 2:
                raise ValueError("shape extends outside canvas")
            if shape["kind"] in {"circle", "square"} and w != h:
                raise ValueError("circle and square require equal width and height")
    elif kind == "clock":
        integer(spec.get("hour"), "hour", 0, 23)
        integer(spec.get("minute", 0), "minute", 0, 59)
        if width < 180 or height < 180:
            raise ValueError("clock canvas must be at least 180 x 180")
    elif kind == "number_line":
        start = integer(spec.get("start", 0), "start", -1000, 1000)
        end = integer(spec.get("end", 10), "end", -1000, 1000)
        step = integer(spec.get("step", 1), "step", 1, 100)
        if end <= start or (end - start) % step or (end - start) // step > 20:
            raise ValueError("number line needs 1..20 equal intervals")
        ticks = list(range(start, end + 1, step))
        hidden = spec.get("hidden_values", [])
        if not isinstance(hidden, list) or any(type(v) is not int or v not in ticks for v in hidden):
            raise ValueError("hidden_values must be number-line tick values")
    elif kind == "grid":
        rows = integer(spec.get("rows", 5), "rows", 1, 12)
        cols = integer(spec.get("cols", 5), "cols", 1, 12)
        cells = spec.get("shaded_cells", [])
        if not isinstance(cells, list) or len(cells) > rows * cols:
            raise ValueError("invalid shaded_cells")
        seen = set()
        for cell in cells:
            if not isinstance(cell, list) or len(cell) != 2:
                raise ValueError("shaded cell must be [row, col]")
            row = integer(cell[0], "row", 0, rows - 1)
            col = integer(cell[1], "col", 0, cols - 1)
            if (row, col) in seen:
                raise ValueError("duplicate shaded cell")
            seen.add((row, col))
    elif kind == "polygon":
        points = spec.get("points")
        if not isinstance(points, list) or not 3 <= len(points) <= 20:
            raise ValueError("polygon requires 3..20 points")
        for point in points:
            if not isinstance(point, list) or len(point) != 2:
                raise ValueError("polygon point must be [x, y]")
            number(point[0], "point.x", 2, width - 2)
            number(point[1], "point.y", 2, height - 2)


def render_extended_geometry(spec: dict) -> str:
    validate_geometry(spec)
    width, height = spec.get("canvas_width", 320), spec.get("canvas_height", 180)
    elements = []

    def tag(name: str, **attrs: object) -> str:
        attributes = " ".join(f'{key.replace("_", "-")}="{html.escape(str(value), quote=True)}"' for key, value in attrs.items())
        return f"<{name} {attributes}/>"

    def label(x: float, y: float, value: object, size: int = 14) -> str:
        return f'<text x="{x:g}" y="{y:g}" font-size="{size}" text-anchor="middle" fill="#111" stroke="none">{html.escape(str(value))}</text>'

    kind = spec["type"]
    if kind == "shape_collection":
        for shape in spec["shapes"]:
            x, y, w, h = shape["x"], shape["y"], shape.get("width", 30), shape.get("height", 30)
            if shape["kind"] == "circle":
                elements.append(tag("circle", cx=x + w / 2, cy=y + h / 2, r=w / 2))
            elif shape["kind"] == "triangle":
                elements.append(tag("polygon", points=f"{x + w / 2},{y} {x + w},{y + h} {x},{y + h}"))
            else:
                elements.append(tag("rect", x=x, y=y, width=w, height=h))
    elif kind == "clock":
        cx, cy, radius = width / 2, height / 2, min(width, height) / 2 - 12
        elements.append(tag("circle", cx=cx, cy=cy, r=radius))
        for tick in range(60):
            angle = tick * math.pi / 30
            inner = radius - (8 if tick % 5 == 0 else 3)
            elements.append(tag("line", x1=cx + inner * math.sin(angle), y1=cy - inner * math.cos(angle),
                                x2=cx + radius * math.sin(angle), y2=cy - radius * math.cos(angle)))
        for digit in range(1, 13):
            angle = digit * math.pi / 6
            elements.append(label(cx + (radius - 22) * math.sin(angle), cy - (radius - 22) * math.cos(angle) + 5, digit))
        minute = spec.get("minute", 0)
        for angle, length, thickness in [((spec["hour"] % 12 + minute / 60) * math.pi / 6, radius * .48, 4),
                                          (minute * math.pi / 30, radius * .72, 2)]:
            elements.append(tag("line", x1=cx, y1=cy, x2=cx + length * math.sin(angle),
                                y2=cy - length * math.cos(angle), stroke_width=thickness))
        elements.append(tag("circle", cx=cx, cy=cy, r=3, fill="#111"))
    elif kind == "number_line":
        start, end, step = spec.get("start", 0), spec.get("end", 10), spec.get("step", 1)
        y = height / 2
        elements.append(tag("line", x1=20, y1=y, x2=width - 20, y2=y))
        for value in range(start, end + 1, step):
            x = 25 + (width - 50) * (value - start) / (end - start)
            elements.append(tag("line", x1=x, y1=y - 6, x2=x, y2=y + 6))
            elements.append(label(x, y + 25, "□" if value in spec.get("hidden_values", []) else value))
    elif kind == "grid":
        rows, cols = spec.get("rows", 5), spec.get("cols", 5)
        size = min((width - 30) / cols, (height - 30) / rows)
        left, top = (width - cols * size) / 2, (height - rows * size) / 2
        for row, col in spec.get("shaded_cells", []):
            elements.append(tag("rect", x=left + col * size, y=top + row * size, width=size, height=size, fill="#b0b0b0", stroke="none"))
        for row in range(rows + 1):
            elements.append(tag("line", x1=left, y1=top + row * size, x2=left + cols * size, y2=top + row * size))
        for col in range(cols + 1):
            elements.append(tag("line", x1=left + col * size, y1=top, x2=left + col * size, y2=top + rows * size))
    elif kind == "polygon":
        elements.append(tag("polygon", points=" ".join(f"{x},{y}" for x, y in spec["points"])))
    else:
        raise ValueError(f"not an extended geometry type: {kind}")
    # No hidden numeric answers in aria labels or data attributes.
    return (f'<svg class="geometry-diagram" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            'role="img" aria-label="题目图形" fill="none" stroke="#111" stroke-width="1.5">'
            + "".join(elements) + "</svg>")
