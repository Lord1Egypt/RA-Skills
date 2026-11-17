"""2D profile shapes -> line/arc/circle segments (pure Python).

Agents describe profiles with simple shapes instead of constrained sketches:

    {"rect": [x0, y0, x1, y1], "corner_radius": 3}
    {"circle": [cx, cy], "radius": 2.5}
    {"slot": [[x1, y1], [x2, y2]], "radius": 3}
    {"polygon": [[x, y], ...], "corner_radius": 2}          # or "radii": [r per corner]
    {"spline": [[x, y], ...]}                                # smooth closed curve through the points
    {"path": [[x, y], {"arc_to": [x, y], "center": [cx, cy], "clockwise": false},
              {"spline_to": [x, y], "through": [[x, y], ...], "start_tangent": [dx, dy], "end_tangent": [dx, dy]},
              [x, y], ...]}

Each shape is a closed loop. Loops inside other loops become holes when
extruded or revolved. Coordinates are in the profile plane.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

Point = Tuple[float, float]
# ("line", p0, p1) | ("arc", p0, pmid, p1) | ("circle", center, radius)
# | ("spline", (points...), periodic, start_tangent | None, end_tangent | None)  (interpolating B-spline)
Segment = Tuple[Any, ...]

KINDS = ("rect", "circle", "slot", "polygon", "spline", "path")
EXTRA_KEYS = {
    "rect": ("corner_radius",),
    "circle": ("radius",),
    "slot": ("radius",),
    "polygon": ("corner_radius", "radii"),
    "spline": (),
    "path": (),
}
TOL = 1e-6


class ProfileError(ValueError):
    pass


def _num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _pt(v: Any, what: str) -> Point:
    if not (isinstance(v, list) and len(v) == 2 and all(_num(c) for c in v)):
        raise ProfileError(f"{what} must be [x, y]")
    return (float(v[0]), float(v[1]))


def _sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1])


def _len(v: Point) -> float:
    return math.hypot(v[0], v[1])


def _unit(v: Point) -> Point:
    n = _len(v)
    return (v[0] / n, v[1] / n)


def _cross(a: Point, b: Point) -> float:
    return a[0] * b[1] - a[1] * b[0]


def _signed_area(pts: Sequence[Point]) -> float:
    return 0.5 * sum(_cross(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))


# ------------------------------------------------------------------ expressions

# Shapes whose numbers may be '=expression' strings: they are built with one named dimension per number,
# which an expression can drive (see ops/sketch.py). Other shapes have no such one-to-one dimensions.
EXPR_KINDS = ("rect", "circle", "slot")
EXPR_HINT = (
    "'=expression' values are supported in the numbers of rect, circle and slot shapes "
    "(and their radius / corner_radius) of extrude and revolve profiles"
)


def is_expr(v: Any) -> bool:
    return isinstance(v, str) and v.startswith("=") and len(v.strip()) > 1


def _any_expr(v: Any) -> bool:
    if isinstance(v, dict):
        return any(_any_expr(x) for x in v.values())
    if isinstance(v, list):
        return any(_any_expr(x) for x in v)
    return is_expr(v)


def has_expressions(shapes: Any) -> bool:
    return _any_expr(shapes)


def resolve(shapes: Any, evaluate: Any) -> Any:
    """Copy of ``shapes`` with the supported '=expression' numbers replaced by ``evaluate(expression)``."""

    def val(v: Any) -> Any:
        return evaluate(v) if is_expr(v) else v

    out = []
    for shape in shapes if isinstance(shapes, list) else []:
        if not isinstance(shape, dict):
            out.append(shape)
            continue
        new = dict(shape)
        kind = next((k for k in EXPR_KINDS if k in shape), None)
        if kind in ("rect", "circle") and isinstance(shape[kind], list):
            new[kind] = [val(c) for c in shape[kind]]
        elif kind == "slot" and isinstance(shape[kind], list):
            new[kind] = [[val(c) for c in pt] if isinstance(pt, list) else pt for pt in shape[kind]]
        if kind is not None:
            for key in ("radius", "corner_radius"):
                if key in new:
                    new[key] = val(new[key])
        out.append(new)
    return out


def check_expressions(shapes: Any) -> None:
    """Static check of shapes that contain expressions: they may only stand where ``resolve`` replaces them.
    Shapes without expressions get the full geometric check; the others get it when they are built."""
    if not isinstance(shapes, list) or not shapes:
        raise ProfileError("'shapes' must be a non-empty list")
    placeholders = resolve(shapes, lambda e: 1.0)
    for i, (shape, plain) in enumerate(zip(shapes, placeholders)):
        if not _any_expr(shape):
            shape_segments(shape, i)
        elif _any_expr(plain):
            raise ProfileError(f"shapes[{i}]: {EXPR_HINT}")
        else:
            kind = next(k for k in EXPR_KINDS if k in shape)
            extra = set(shape) - {kind} - set(EXTRA_KEYS[kind])
            if extra or sum(1 for k in KINDS if k in shape) != 1:
                raise ProfileError(f"shapes[{i}]: unknown keys {sorted(extra)} for '{kind}'")


# ------------------------------------------------------------------ splines


def closed_spline_derivatives(pts: Sequence[Point]) -> Tuple[List[float], List[Point]]:
    """Chord-length parameters and first derivatives of the closed C2 cubic spline through ``pts``.

    OCC's own periodic interpolation is not symmetric about its seam (the first point), which shows as a
    bulge or kink there; passing it these exact derivatives removes the dependence on the seam.
    """
    n = len(pts)
    h = [_len(_sub(pts[(i + 1) % n], pts[i])) for i in range(n)]  # segment i: pts[i] -> pts[i+1]
    params = [0.0]
    for x in h[:-1]:
        params.append(params[-1] + x)
    # Unknown derivatives D_i. Continuity of the 2nd derivative at point i (segments i-1 and i):
    #   h_i D_{i-1} + 2 (h_{i-1} + h_i) D_i + h_{i-1} D_{i+1}
    #     = 3 (h_i (P_i - P_{i-1}) / h_{i-1} + h_{i-1} (P_{i+1} - P_i) / h_i)
    a = [[0.0] * n for _ in range(n)]
    rhs = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        hp, hi = h[i - 1], h[i]
        a[i][(i - 1) % n] += hi
        a[i][i] += 2 * (hp + hi)
        a[i][(i + 1) % n] += hp
        for k in range(2):
            rhs[i][k] = 3 * (hi * (pts[i][k] - pts[i - 1][k]) / hp + hp * (pts[(i + 1) % n][k] - pts[i][k]) / hi)
    for c in range(n):  # Gaussian elimination; the matrix is diagonally dominant
        piv = a[c][c]
        for r in range(c + 1, n):
            f = a[r][c] / piv
            if f:
                for k in range(c, n):
                    a[r][k] -= f * a[c][k]
                rhs[r][0] -= f * rhs[c][0]
                rhs[r][1] -= f * rhs[c][1]
    d: List[List[float]] = [[0.0, 0.0] for _ in range(n)]
    for r in range(n - 1, -1, -1):
        for k in range(2):
            d[r][k] = (rhs[r][k] - sum(a[r][j] * d[j][k] for j in range(r + 1, n))) / a[r][r]
    return params, [(x, y) for x, y in d]


# ------------------------------------------------------------------ shapes


def _rounded_polygon(pts: List[Point], radii: List[float], label: str) -> List[Segment]:
    n = len(pts)
    if n < 3:
        raise ProfileError(f"{label}: needs at least 3 corners")
    for i in range(n):
        if _len(_sub(pts[(i + 1) % n], pts[i])) < TOL:
            raise ProfileError(f"{label}: corners {i} and {(i + 1) % n} coincide")
    if abs(_signed_area(pts)) < TOL:
        raise ProfileError(f"{label}: corners are collinear (zero area)")
    setback = [0.0] * n  # distance from corner i to its tangent points
    arcs: List[Optional[Segment]] = [None] * n
    t_in: List[Point] = list(pts)  # tangent point on the edge arriving at corner i
    t_out: List[Point] = list(pts)  # tangent point on the edge leaving corner i
    for i in range(n):
        r = radii[i]
        if r <= 0:
            continue
        p, prev, nxt = pts[i], pts[i - 1], pts[(i + 1) % n]
        u1, u2 = _unit(_sub(prev, p)), _unit(_sub(nxt, p))
        theta = math.acos(max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1])))  # angle between edges
        if theta < 1e-6 or abs(theta - math.pi) < 1e-6:
            raise ProfileError(f"{label}: corner {i} is straight or degenerate and cannot be rounded")
        d = r / math.tan(theta / 2)
        setback[i] = d
        a = (p[0] + u1[0] * d, p[1] + u1[1] * d)
        b = (p[0] + u2[0] * d, p[1] + u2[1] * d)
        bis = _unit((u1[0] + u2[0], u1[1] + u2[1]))
        h = r / math.sin(theta / 2)
        c = (p[0] + bis[0] * h, p[1] + bis[1] * h)
        mdir = _unit(_sub(p, c))
        arcs[i] = ("arc", a, (c[0] + mdir[0] * r, c[1] + mdir[1] * r), b)
        t_in[i], t_out[i] = a, b
    for i in range(n):
        j = (i + 1) % n
        edge = _len(_sub(pts[j], pts[i]))
        if setback[i] + setback[j] > edge + 1e-9:
            raise ProfileError(
                f"{label}: corner radii too large for edge {i}-{j} "
                f"(length {edge:.4g}, the roundings need {setback[i] + setback[j]:.4g})"
            )
    segs: List[Segment] = []
    for i in range(n):
        if arcs[i] is not None:
            segs.append(arcs[i])
        start, end = t_out[i], t_in[(i + 1) % n]
        if _len(_sub(end, start)) > TOL:
            segs.append(("line", start, end))
    return segs


def _arc_mid(start: Point, end: Point, center: Point, clockwise: bool, label: str) -> Point:
    r0, r1 = _len(_sub(start, center)), _len(_sub(end, center))
    if r0 < TOL:
        raise ProfileError(f"{label}: arc start coincides with its center")
    if abs(r0 - r1) > 1e-4 * max(1.0, r0):
        raise ProfileError(
            f"{label}: arc start and end are at different distances from the center ({r0:.4g} vs {r1:.4g})"
        )
    a0 = math.atan2(start[1] - center[1], start[0] - center[0])
    a1 = math.atan2(end[1] - center[1], end[0] - center[0])
    sweep = (a1 - a0) % (2 * math.pi)
    if clockwise:
        sweep -= 2 * math.pi
    if abs(sweep) < 1e-9 or abs(abs(sweep) - 2 * math.pi) < 1e-9:
        raise ProfileError(f"{label}: arc start and end coincide; use a circle for a full circle")
    am = a0 + sweep / 2
    return (center[0] + r0 * math.cos(am), center[1] + r0 * math.sin(am))


def _tangent(v: Any, what: str) -> Point:
    t = _pt(v, what)
    if _len(t) < TOL:
        raise ProfileError(f"{what} must not be [0, 0]")
    return t


def _distinct(pts: List[Point], label: str, closed: bool) -> None:
    n = len(pts)
    for i in range(n if closed else n - 1):
        if _len(_sub(pts[(i + 1) % n], pts[i])) < TOL:
            raise ProfileError(f"{label}: spline points {i} and {(i + 1) % n} coincide")


def _spline_to(cur: Point, it: Dict[str, Any], label: str) -> Segment:
    bad = set(it) - {"spline_to", "through", "start_tangent", "end_tangent"}
    if bad:
        raise ProfileError(
            f"{label}: unknown keys {sorted(bad)} for spline_to; allowed: through, start_tangent, end_tangent"
        )
    end = _pt(it["spline_to"], f"{label}.spline_to")
    through = it.get("through", [])
    if not isinstance(through, list):
        raise ProfileError(f"{label}.through must be a list of [x, y] points")
    pts = [cur] + [_pt(q, f"{label}.through[{i}]") for i, q in enumerate(through)] + [end]
    t0 = _tangent(it["start_tangent"], f"{label}.start_tangent") if "start_tangent" in it else None
    t1 = _tangent(it["end_tangent"], f"{label}.end_tangent") if "end_tangent" in it else None
    if len(pts) == 2 and t0 is None and t1 is None:
        raise ProfileError(f"{label}: a spline_to needs 'through' points or tangents; otherwise use a straight [x, y]")
    _distinct(pts, label, closed=False)
    return ("spline", tuple(pts), False, t0, t1)


def _path(items: Any, label: str) -> List[Segment]:
    if not isinstance(items, list) or len(items) < 2:
        raise ProfileError(f"{label}: 'path' needs a start point and at least 2 more entries")
    start = _pt(items[0], f"{label}: path[0]")
    segs: List[Segment] = []
    cur = start
    for k, it in enumerate(items[1:], start=1):
        if isinstance(it, list):
            p = _pt(it, f"{label}: path[{k}]")
            if _len(_sub(p, cur)) < TOL:
                raise ProfileError(f"{label}: path[{k}] repeats the previous point")
            segs.append(("line", cur, p))
            cur = p
        elif isinstance(it, dict) and "arc_to" in it:
            bad = set(it) - {"arc_to", "center", "clockwise"}
            if bad or "center" not in it:
                raise ProfileError(
                    f'{label}: path[{k}] arc must be {{"arc_to": [x, y], "center": [x, y], "clockwise": false}}'
                )
            p = _pt(it["arc_to"], f"{label}: path[{k}].arc_to")
            c = _pt(it["center"], f"{label}: path[{k}].center")
            cw = it.get("clockwise", False)
            if not isinstance(cw, bool):
                raise ProfileError(f"{label}: path[{k}].clockwise must be true or false")
            segs.append(("arc", cur, _arc_mid(cur, p, c, cw, f"{label}: path[{k}]"), p))
            cur = p
        elif isinstance(it, dict) and "spline_to" in it:
            segs.append(_spline_to(cur, it, f"{label}: path[{k}]"))
            cur = segs[-1][1][-1]
        else:
            raise ProfileError(f"{label}: path[{k}] must be [x, y] (line to), an arc_to or a spline_to object")
    if _len(_sub(cur, start)) > TOL:
        segs.append(("line", cur, start))  # close
    if all(s[0] == "line" for s in segs) and len(segs) < 3:
        raise ProfileError(f"{label}: path does not enclose an area")
    return segs


def shape_segments(shape: Any, index: int) -> List[Segment]:
    label = f"shapes[{index}]"
    if _any_expr(shape):
        raise ProfileError(f"{label}: {EXPR_HINT}")
    if not isinstance(shape, dict):
        raise ProfileError(f'{label} must be an object such as {{"rect": [0, 0, 40, 20]}}')
    kinds = [k for k in KINDS if k in shape]
    if len(kinds) != 1:
        raise ProfileError(f"{label} must have exactly one of {list(KINDS)}")
    kind = kinds[0]
    extra = set(shape) - {kind} - set(EXTRA_KEYS[kind])
    if extra:
        raise ProfileError(f"{label}: unknown keys {sorted(extra)} for '{kind}'; allowed: {list(EXTRA_KEYS[kind])}")
    val = shape[kind]

    def radius(key: str, required: bool) -> float:
        r = shape.get(key, 0 if not required else None)
        if r is None:
            raise ProfileError(f"{label}: '{kind}' needs '{key}'")
        if not _num(r) or r < 0 or (required and r == 0):
            raise ProfileError(f"{label}: '{key}' must be a {'positive' if required else 'non-negative'} number")
        return float(r)

    if kind == "circle":
        return [("circle", _pt(val, f"{label}.circle"), radius("radius", True))]
    if kind == "rect":
        if not (isinstance(val, list) and len(val) == 4 and all(_num(c) for c in val)):
            raise ProfileError(f"{label}: rect must be [x_min, y_min, x_max, y_max]")
        x0, y0, x1, y1 = (float(c) for c in val)
        if x1 - x0 <= TOL or y1 - y0 <= TOL:
            raise ProfileError(f"{label}: rect needs x_max > x_min and y_max > y_min")
        r = radius("corner_radius", False)
        if 2 * r > min(x1 - x0, y1 - y0) + 1e-9:
            raise ProfileError(
                f"{label}: corner_radius {r} is more than half the smaller side ({min(x1 - x0, y1 - y0):.4g})"
            )
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        return _rounded_polygon(pts, [r] * 4, label)
    if kind == "slot":
        if not (isinstance(val, list) and len(val) == 2):
            raise ProfileError(f"{label}: slot must be [[x1, y1], [x2, y2]] (centers of the two ends)")
        p1, p2 = _pt(val[0], f"{label}.slot[0]"), _pt(val[1], f"{label}.slot[1]")
        r = radius("radius", True)
        if _len(_sub(p2, p1)) < TOL:
            raise ProfileError(f"{label}: slot end centers coincide; use a circle")
        u = _unit(_sub(p2, p1))
        n = (-u[1], u[0])
        a1 = (p1[0] - n[0] * r, p1[1] - n[1] * r)
        a2 = (p2[0] - n[0] * r, p2[1] - n[1] * r)
        b2 = (p2[0] + n[0] * r, p2[1] + n[1] * r)
        b1 = (p1[0] + n[0] * r, p1[1] + n[1] * r)
        cap2 = (p2[0] + u[0] * r, p2[1] + u[1] * r)
        cap1 = (p1[0] - u[0] * r, p1[1] - u[1] * r)
        return [("line", a1, a2), ("arc", a2, cap2, b2), ("line", b2, b1), ("arc", b1, cap1, a1)]
    if kind == "polygon":
        if not isinstance(val, list) or len(val) < 3:
            raise ProfileError(f"{label}: polygon needs at least 3 points")
        pts = [_pt(p, f"{label}.polygon[{i}]") for i, p in enumerate(val)]
        if "radii" in shape:
            radii = shape["radii"]
            if "corner_radius" in shape:
                raise ProfileError(f"{label}: give 'corner_radius' or 'radii', not both")
            if not (isinstance(radii, list) and len(radii) == len(pts) and all(_num(r) and r >= 0 for r in radii)):
                raise ProfileError(f"{label}: 'radii' must list one non-negative radius per corner ({len(pts)})")
            radii = [float(r) for r in radii]
        else:
            radii = [radius("corner_radius", False)] * len(pts)
        return _rounded_polygon(pts, radii, label)
    if kind == "spline":
        if not isinstance(val, list) or len(val) < 3:
            raise ProfileError(f"{label}: spline needs at least 3 points")
        pts = [_pt(q, f"{label}.spline[{i}]") for i, q in enumerate(val)]
        if len(pts) > 3 and _len(_sub(pts[-1], pts[0])) < TOL:
            pts = pts[:-1]  # closing point repeated: the spline closes by itself
        _distinct(pts, label, closed=True)
        if abs(_signed_area(pts)) < TOL:
            raise ProfileError(f"{label}: spline points are collinear (zero area)")
        return [("spline", tuple(pts), True, None, None)]
    return _path(val, label)


def all_segments(shapes: Any) -> List[List[Segment]]:
    """Validate a 'shapes' list and return one segment loop per shape."""
    if not isinstance(shapes, list) or not shapes:
        raise ProfileError("'shapes' must be a non-empty list")
    return [shape_segments(s, i) for i, s in enumerate(shapes)]
