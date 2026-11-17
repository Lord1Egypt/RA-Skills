"""总工视角的施工平面布置候选生成器（v0.7.0）。

输入：base-map、周边环境 site-context、项目需求、reader 塔吊（可选）。
输出：A/B/C 三套结构化布置候选（cad-site-facility/v1 行），以及假设、指标与评分。

边界：
- 只生成“可讨论的候选”，不是审批图；所有设施 source=auto-layout、confidence=candidate。
- 不替代塔吊选型、临电计算、消防审查、管线探测和现场踏勘。
- 场地不规则时用外接矩形/内缩环近似，必须在 assumptions 中写明。
"""
from __future__ import annotations

import bisect
import itertools
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from .context import geometry_blocked, point_blocked
from .taxonomy import FACILITIES, STAGE_NAMES, meta

SCHEMA = "cad-site-facility/v1"
REQ_SCHEMA = "site-layout-requirements/v1"
UNIT_TO_MM = {"mm": 1.0, "cm": 10.0, "m": 1000.0}

STAGE_ALL = ("earthwork", "structure", "finish")
STAGE_STRUCT = ("structure", "finish")
STAGE_STRUCT_ONLY = ("structure",)
STAGE_EARTH = ("earthwork",)

# 加工区拆分后的类别集合（含旧通用类，兼容历史输入）
PROCESSING = ("processing_zone", "steel_processing", "wood_processing", "mortar_processing")

# 0.7.0 生活区：宿舍/食堂/淋浴/晾晒均属人员密集临建，塔吊回转范围内不得布置。
# worker_living_zone 是包含食堂/淋浴/晾晒的“生活区包络”，其本身没有独立建筑轮廓；
# 与 siteplan 规则 6 一致按形心避开塔吊，边缘净距必须在塔吊选型后复核。
LIVING_CATEGORIES = (
    "staff_dormitory", "worker_living_zone", "canteen", "toilet_shower",
    "drying_area", "temporary_dormitory", "temporary_building",
)
CRANE_SENSITIVE = ("site_office",) + LIVING_CATEGORIES
QUIET_GENERATOR = ("site_office",) + LIVING_CATEGORIES
CENTROID_CRANE_CATEGORIES = ("worker_living_zone", "staff_dormitory")

# 单个设施自动选址的确定性搜索预算（候选点数，不按墙钟时间，保证同输入同结果）。
# 真实大场地（约 474 m x 189 m，2 m 网格）单个设施约 2 万个候选；
# 12 万可覆盖三档尺寸仍不收敛的异常情况，同时避免无解时无限扫描。
MAX_PLACEMENT_CANDIDATES = 120_000
# 生活区子块组合搜索预算：按候选矩形计数，保证同输入同结果且不会无限扫描。
MAX_LIVING_SEARCH_NODES = 1_200_000
MAX_LIVING_COMBO_NODES = 40_000


class GeneratorError(Exception):
    exit_code = 2


class GeneratorUnitError(GeneratorError):
    exit_code = 4


def _f(value: Any, label: str) -> float:
    if isinstance(value, bool):
        raise GeneratorError(f"{label} 必须是数字")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise GeneratorError(f"{label} 必须是数字，收到 {value!r}") from exc
    if not math.isfinite(number):
        raise GeneratorError(f"{label} 必须是有限数字")
    return number


def _dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _point_segment(p: Sequence[float], a: Sequence[float], b: Sequence[float]) -> float:
    dx, dy = b[0] - a[0], b[1] - a[1]
    if abs(dx) < 1e-12 and abs(dy) < 1e-12:
        return _dist(p, a)
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return _dist(p, (a[0] + t * dx, a[1] + t * dy))


def _polyline_distance(p: Sequence[float], points: Sequence[Sequence[float]]) -> float:
    if len(points) == 1:
        return _dist(p, points[0])
    return min(_point_segment(p, points[i], points[i + 1]) for i in range(len(points) - 1))


def _nearest_point_on_polyline(p: Sequence[float], points: Sequence[Sequence[float]]) -> Sequence[float]:
    """返回折线上距 p 最近的点，用于大门接入环道；不能只连最近转角。"""
    best: Optional[Tuple[float, Sequence[float]]] = None
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        if abs(dx) < 1e-12 and abs(dy) < 1e-12:
            q = a
        else:
            t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
            q = (a[0] + t * dx, a[1] + t * dy)
        d = _dist(p, q)
        if best is None or d < best[0]:
            best = (d, q)
    return best[1] if best else points[0]


def _oriented_rect(center: Sequence[float], length: float, width: float,
                   angle_rad: float) -> List[Tuple[float, float]]:
    """按长轴方向生成长方形四角（逆时针），用于顺路/顺围挡布置。"""
    ux, uy = math.cos(angle_rad), math.sin(angle_rad)
    vx, vy = -uy, ux
    hl, hw = length / 2.0, width / 2.0
    cx, cy = center
    return [(cx - ux * hl - vx * hw, cy - uy * hl - vy * hw),
            (cx + ux * hl - vx * hw, cy + uy * hl - vy * hw),
            (cx + ux * hl + vx * hw, cy + uy * hl + vy * hw),
            (cx - ux * hl + vx * hw, cy - uy * hl + vy * hw)]


def _project_on_closed_polyline(p: Sequence[float],
                                points: Sequence[Sequence[float]]
                                ) -> Tuple[int, float, Tuple[float, float], float]:
    """返回 (段号, 段内参数 t, 投影点, 距离)；points 不重复首点。"""
    best: Optional[Tuple[int, float, Tuple[float, float], float]] = None
    n = len(points)
    for i in range(n):
        a, b = points[i], points[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        if abs(dx) < 1e-12 and abs(dy) < 1e-12:
            q, t = a, 0.0
        else:
            t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy)
                             / (dx * dx + dy * dy)))
            q = (a[0] + t * dx, a[1] + t * dy)
        d = _dist(p, q)
        if best is None or d < best[3]:
            best = (i, t, (float(q[0]), float(q[1])), d)
    return best  # type: ignore[return-value]


def _walk_closed_polyline(points: Sequence[Sequence[float]], seg: int, t: float,
                          distance: float, forward: bool
                          ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """沿闭合折线走 distance，返回 (落点, 该处前进方向单位向量)。"""
    n = len(points)
    remaining = max(0.0, float(distance))
    i, u = seg, t
    for _ in range(n * 2 + 2):
        a, b = points[i], points[(i + 1) % n]
        seg_len = _dist(a, b)
        if seg_len <= 1e-9:
            i = (i + 1) % n if forward else (i - 1) % n
            u = 0.0 if forward else 1.0
            continue
        avail = (1.0 - u) * seg_len if forward else u * seg_len
        if remaining <= avail + 1e-9:
            du = (remaining / seg_len) * (1.0 if forward else -1.0)
            u2 = min(1.0, max(0.0, u + du))
            point = (a[0] + (b[0] - a[0]) * u2, a[1] + (b[1] - a[1]) * u2)
            dx, dy = (b[0] - a[0], b[1] - a[1])
            if not forward:
                dx, dy = -dx, -dy
            norm = math.hypot(dx, dy) or 1.0
            return point, (dx / norm, dy / norm)
        remaining -= avail
        if forward:
            i, u = (i + 1) % n, 0.0
        else:
            i, u = (i - 1) % n, 1.0
    a, b = points[i], points[(i + 1) % n]
    dx, dy = b[0] - a[0], b[1] - a[1]
    norm = math.hypot(dx, dy) or 1.0
    return (float(a[0]), float(a[1])), (dx / norm, dy / norm)


def _point_in_polygon(p: Sequence[float], poly: Sequence[Sequence[float]]) -> bool:
    if len(poly) < 3:
        return False
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i][0], poly[i][1]
        xj, yj = poly[j][0], poly[j][1]
        if (yi > p[1]) != (yj > p[1]) and p[0] < (xj - xi) * (p[1] - yi) / ((yj - yi) or 1e-12) + xi:
            inside = not inside
        j = i
    return inside


def _bbox(points: Sequence[Sequence[float]]) -> Tuple[float, float, float, float]:
    xs = [float(p[0]) for p in points]
    ys = [float(p[1]) for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def _poly_length(points: Sequence[Sequence[float]], closed: bool = False) -> float:
    total = sum(_dist(points[i], points[i + 1]) for i in range(len(points) - 1))
    if closed and len(points) > 2:
        total += _dist(points[-1], points[0])
    return total


def _road_key(row: Dict[str, Any]) -> Tuple[Any, ...]:
    """道路几何指纹：坐标取 0.1 mm，供长度去重（消防车道与临时主路共线时只算一次）。"""
    geom = row.get("geometry") or {}
    pts = geom.get("points_mm") or []
    return (bool(geom.get("closed")), tuple((round(float(p[0]), 1), round(float(p[1]), 1))
                                            for p in pts))


def _unique_road_length_m(rows: Sequence[Dict[str, Any]]) -> Dict[str, float]:
    """按物理几何去重统计道路长度；同一几何被临时道路+消防车道共用只计一次。"""
    seen: set = set()
    by_category: Dict[str, float] = {}
    for row in rows:
        category = row.get("category")
        if category not in ("temporary_road", "fire_access", "permanent_road"):
            continue
        key = _road_key(row)
        if key in seen:
            continue
        seen.add(key)
        geom = row["geometry"]
        length = _poly_length(geom["points_mm"], geom.get("closed", False)) / 1000.0
        by_category[category] = round(by_category.get(category, 0.0) + length, 1)
    total = round(sum(by_category.values()), 1)
    return {"total": total, "by_category": by_category}


def _point_at(points: Sequence[Sequence[float]], station_mm: float, closed: bool = False) -> Tuple[float, float]:
    pts = list(points)
    if closed and pts and _dist(pts[0], pts[-1]) > 1e-6:
        pts.append(pts[0])
    remain = max(0.0, station_mm)
    for i in range(len(pts) - 1):
        seg = _dist(pts[i], pts[i + 1])
        if remain <= seg or i == len(pts) - 2:
            ratio = 0.0 if seg <= 1e-9 else min(1.0, remain / seg)
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * ratio,
                    pts[i][1] + (pts[i + 1][1] - pts[i][1]) * ratio)
        remain -= seg
    return tuple(pts[-1])


def _rect_polygon(rect: Sequence[float]) -> List[Tuple[float, float]]:
    x0, y0, x1, y1 = rect
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _rect_points(rect: Sequence[float]) -> List[Tuple[float, float]]:
    x0, y0, x1, y1 = rect
    return [(x0, y0), ((x0 + x1) / 2, y0), (x1, y0), (x1, (y0 + y1) / 2),
            (x1, y1), ((x0 + x1) / 2, y1), (x0, y1), (x0, (y0 + y1) / 2)]


def _rect_rect_gap(a: Sequence[float], b: Sequence[float]) -> float:
    dx = max(b[0] - a[2], a[0] - b[2], 0.0)
    dy = max(b[1] - a[3], a[1] - b[3], 0.0)
    return math.hypot(dx, dy)


def _rect_distance_to_point(rect: Sequence[float], p: Sequence[float]) -> float:
    dx = max(rect[0] - p[0], 0.0, p[0] - rect[2])
    dy = max(rect[1] - p[1], 0.0, p[1] - rect[3])
    return math.hypot(dx, dy)


def _signed_area(points: Sequence[Sequence[float]]) -> float:
    total = 0.0
    for i in range(len(points)):
        a = points[i]
        b = points[(i + 1) % len(points)]
        total += a[0] * b[1] - b[0] * a[1]
    return total / 2.0


def _proper_cross(a: Sequence[float], b: Sequence[float],
                  c: Sequence[float], d: Sequence[float]) -> bool:
    """严格相交（不算共享端点/共线接触），用于内缩多边形自交校验。"""

    def orient(p, q, r):
        value = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        if abs(value) < 1e-9:
            return 0
        return 1 if value > 0 else -1

    o1, o2 = orient(a, b, c), orient(a, b, d)
    o3, o4 = orient(c, d, a), orient(c, d, b)
    return o1 * o2 < 0 and o3 * o4 < 0


def _polyline_self_intersects(points: Sequence[Sequence[float]]) -> bool:
    n = len(points)
    if n < 4:
        return False
    for i in range(n):
        a, b = points[i], points[(i + 1) % n]
        for j in range(i + 1, n):
            if j == i or (j + 1) % n == i or (i + 1) % n == j:
                continue
            c, d = points[j], points[(j + 1) % n]
            if _proper_cross(a, b, c, d):
                return True
    return False


def _rdp(points: Sequence[Sequence[float]], tol_mm: float) -> List[Tuple[float, float]]:
    """Douglas-Peucker 简化（开折线）。"""
    if len(points) < 3:
        return [(float(p[0]), float(p[1])) for p in points]
    a = (float(points[0][0]), float(points[0][1]))
    b = (float(points[-1][0]), float(points[-1][1]))
    index = -1
    best = tol_mm
    for i in range(1, len(points) - 1):
        d = _point_segment((float(points[i][0]), float(points[i][1])), a, b)
        if d > best:
            index, best = i, d
    if index < 0:
        return [a, b]
    left = _rdp(points[:index + 1], tol_mm)
    right = _rdp(points[index:], tol_mm)
    return left[:-1] + right


def _simplify_closed(points: Sequence[Sequence[float]], tol_mm: float) -> List[Tuple[float, float]]:
    """闭合折线简化：用相距最远的两个点切环，避免简化后起点处出现假尖角。"""
    pts = [(float(p[0]), float(p[1])) for p in points]
    if len(pts) >= 2 and _dist(pts[0], pts[-1]) <= 1e-6:
        pts.pop()
    if len(pts) < 4:
        return pts
    far_index = max(range(len(pts)), key=lambda i: _dist(pts[0], pts[i]))
    first = _rdp(pts[:far_index + 1], tol_mm)
    second = _rdp(pts[far_index:] + [pts[0]], tol_mm)
    merged = first[:-1] + second[:-1]
    return merged


def _inset_once(points: Sequence[Sequence[float]], offset_mm: float,
                tol_mm: float) -> Optional[List[Tuple[float, float]]]:
    """单次内缩：先按 tol_mm 简化，再逐边内向平移求斜接角。"""
    pts: List[Tuple[float, float]] = []
    for item in _simplify_closed(points, tol_mm):
        q = (float(item[0]), float(item[1]))
        if not pts or _dist(q, pts[-1]) > 1.0:
            pts.append(q)
    if len(pts) >= 2 and _dist(pts[0], pts[-1]) <= 1.0:
        pts.pop()
    if len(pts) < 3 or offset_mm <= 0:
        return None
    area = _signed_area(pts)
    if abs(area) < 1e-9:
        return None
    sign = 1.0 if area > 0 else -1.0
    normals: List[Tuple[float, float]] = []
    dirs: List[Tuple[float, float]] = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        length = _dist(a, b)
        if length <= 1e-9:
            return None
        ux, uy = (b[0] - a[0]) / length, (b[1] - a[1]) / length
        dirs.append((ux, uy))
        # CCW 多边形的内法线是左转 90°：(-uy, ux)；顺时针取反
        normals.append((-uy * sign, ux * sign))
    result: List[Tuple[float, float]] = []
    for i in range(len(pts)):
        a = pts[i]
        u_prev = dirs[i - 1]
        u_cur = dirs[i]
        n_prev = normals[i - 1]
        n_cur = normals[i]
        p_prev = (a[0] + n_prev[0] * offset_mm, a[1] + n_prev[1] * offset_mm)
        p_cur = (a[0] + n_cur[0] * offset_mm, a[1] + n_cur[1] * offset_mm)
        den = u_prev[0] * u_cur[1] - u_prev[1] * u_cur[0]
        if abs(den) < 1e-9:
            result.append(((p_prev[0] + p_cur[0]) / 2.0, (p_prev[1] + p_cur[1]) / 2.0))
            continue
        t = ((p_cur[0] - p_prev[0]) * u_cur[1] - (p_cur[1] - p_prev[1]) * u_cur[0]) / den
        result.append((p_prev[0] + u_prev[0] * t, p_prev[1] + u_prev[1] * t))
    # 落界校验：每个顶点必须仍在红线内，且内缩后不能自交
    for q in result:
        if not _point_in_polygon(q, pts):
            return None
    cleaned: List[Tuple[float, float]] = []
    for q in result:
        if not cleaned or _dist(q, cleaned[-1]) > 500.0:
            cleaned.append(q)
    if len(cleaned) < 3:
        return None
    if _polyline_self_intersects(cleaned):
        return None
    # 面积必须变小但仍是同一量级，防止退化成细缝
    if _signed_area(cleaned) * sign <= 0:
        return None
    return [(round(q[0], 3), round(q[1], 3)) for q in cleaned]


def _fillet_closed(points: Sequence[Sequence[float]], radius_mm: float = 12000.0,
                   step_deg: float = 15.0) -> List[Tuple[float, float]]:
    """给闭合折线的凸角倒圆，避免红线直角被原样当成道路直角。

    只处理凸角；凹角倒圆会侵出红线，保持原样交给规则报警。半径按相邻
    边长度自动折减，保证切点不越过邻近顶点。
    """
    pts = [(float(p[0]), float(p[1])) for p in points]
    n = len(pts)
    if n < 3 or radius_mm <= 0:
        return pts
    area2 = sum(pts[i][0] * pts[(i + 1) % n][1]
                - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    orient = 1.0 if area2 > 0 else -1.0
    result: List[Tuple[float, float]] = []
    for i in range(n):
        cur = pts[i]
        prev = pts[i - 1]
        nxt = pts[(i + 1) % n]
        v1 = (prev[0] - cur[0], prev[1] - cur[1])
        v2 = (nxt[0] - cur[0], nxt[1] - cur[1])
        l1, l2 = math.hypot(*v1), math.hypot(*v2)
        if l1 < 1e-6 or l2 < 1e-6:
            result.append(cur)
            continue
        u1 = (v1[0] / l1, v1[1] / l1)
        u2 = (v2[0] / l2, v2[1] / l2)
        cross = u1[0] * u2[1] - u1[1] * u2[0]
        dot = max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1]))
        turn = math.atan2(cross, dot)          # 有符号转角，逆时针为正
        # 以“指向相邻顶点”的两个向量计算转角：CCW 多边形的凸角为右转
        # （turn<0），CW 为左转；两者都满足 orient*turn<0。原实现方向写反，
        # 会把所有凸角当凹角跳过，导致环道仍是硬折线。
        if orient * turn >= -math.radians(5.0) or abs(turn) > math.radians(175.0):
            result.append(cur)
            continue
        half = (math.pi - abs(turn)) / 2.0      # 内角一半
        if half <= math.radians(1.0):
            result.append(cur)
            continue
        t = radius_mm / math.tan(half)
        t_max = 0.45 * min(l1, l2)
        if t > t_max:
            t = t_max
        r_eff = t * math.tan(half)
        if r_eff < 1000.0:
            result.append(cur)
            continue
        p1 = (cur[0] + u1[0] * t, cur[1] + u1[1] * t)
        p2 = (cur[0] + u2[0] * t, cur[1] + u2[1] * t)
        bis = (u1[0] + u2[0], u1[1] + u2[1])
        bl = math.hypot(*bis)
        if bl < 1e-9:
            result.append(cur)
            continue
        bis = (bis[0] / bl, bis[1] / bl)
        center = (cur[0] + bis[0] * (r_eff / math.sin(half)),
                  cur[1] + bis[1] * (r_eff / math.sin(half)))
        a1 = math.atan2(p1[1] - center[1], p1[0] - center[0])
        a2 = math.atan2(p2[1] - center[1], p2[0] - center[0])
        raw = math.atan2(math.sin(a2 - a1), math.cos(a2 - a1))
        sweep = math.pi - abs(turn)
        if abs(raw) > sweep + 1e-6:
            raw = math.copysign(sweep, raw if abs(raw) > 1e-9 else -orient)
        steps = max(2, int(math.degrees(abs(raw)) / step_deg) + 1)
        result.append((round(p1[0], 3), round(p1[1], 3)))
        for k in range(1, steps):
            a = a1 + raw * k / steps
            result.append((round(center[0] + r_eff * math.cos(a), 3),
                           round(center[1] + r_eff * math.sin(a), 3)))
        result.append((round(p2[0], 3), round(p2[1], 3)))
    cleaned: List[Tuple[float, float]] = []
    for q in result:
        if not cleaned or _dist(q, cleaned[-1]) > 200.0:
            cleaned.append(q)
    if len(cleaned) >= 2 and _dist(cleaned[0], cleaned[-1]) <= 200.0:
        cleaned.pop()
    return cleaned


def _trim_short_ring_edges(ring: Sequence[Sequence[float]],
                           boundary: Sequence[Sequence[float]],
                           max_edge_mm: float = 15000.0) -> List[Tuple[float, float]]:
    """去掉红线内缩环上的碎边/小凸起，而不是把每个碎折点都当道路折角。

    真实红线常由几百个短线段组成，局部小台阶会让 R3 把相邻三点误算成
    小半径转弯。按周长 1% 设定短边阈值（4~15 m），逐个删除相邻短边
    最短的顶点；每次删除都要仍落在原红线内、不自交、面积不明显缩小。
    """
    pts = [(float(p[0]), float(p[1])) for p in ring]
    if len(pts) < 5:
        return pts
    perimeter = _poly_length(pts, closed=True)
    limit = max(4000.0, min(float(max_edge_mm), perimeter * 0.01))
    area0 = abs(_signed_area(pts))
    changed = True
    while changed and len(pts) > 4:
        changed = False
        shortest: Optional[Tuple[float, int]] = None
        for i in range(len(pts)):
            edge = min(_dist(pts[i - 1], pts[i]), _dist(pts[i], pts[(i + 1) % len(pts)]))
            if edge < limit and (shortest is None or edge < shortest[0]):
                shortest = (edge, i)
        if shortest is None:
            break
        candidate = pts[:shortest[1]] + pts[shortest[1] + 1:]
        if len(candidate) < 4 or _polyline_self_intersects(candidate):
            continue
        if not _ring_stays_inside(candidate, boundary):
            continue
        if abs(_signed_area(candidate)) < area0 * 0.5:
            continue
        pts = candidate
        changed = True
    return [(round(q[0], 3), round(q[1], 3)) for q in pts]


def _ring_stays_inside(ring: Sequence[Sequence[float]],
                       boundary: Sequence[Sequence[float]]) -> bool:
    """按 10 m 采样校验内缩环每个点都还在真实红线内（防简化把环甩出去）。"""
    pts = [(float(q[0]), float(q[1])) for q in boundary]
    for i, a in enumerate(ring):
        b = ring[(i + 1) % len(ring)]
        if not _point_in_polygon(a, pts):
            return False
        seg = _dist(a, b)
        steps = max(1, int(seg // 10_000.0))
        for k in range(1, steps + 1):
            t = k / float(steps)
            q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            if not _point_in_polygon(q, pts):
                return False
    return True


def _inset_polygon(points: Sequence[Sequence[float]],
                   offset_mm: float) -> Optional[List[Tuple[float, float]]]:
    """把红线多边形按 offset_mm 向内偏移，返回验证过的闭合环（不含重复首点）。

    用于非矩形/斜置红线：外接矩形内缩会把环道和设施甩到红线外。
    简化容差从 5 m 逐级收紧，任一档通过“真实红线内 + 不自交 + 转角不过碎”即采用。
    """
    # 真实红线常按 3~5 m 碎段给出；5 m 容差会把平缓弧线简化成上百米长弦，
    # 6 m 宽道路再内缩 4 m 时会压到红线/围挡边。逐级收紧到 0.5 m，保证环道贴界。
    for tol in (200.0, 500.0, 800.0, 1500.0, 3000.0, 5000.0):
        ring = _inset_once(points, offset_mm, tol)
        if not ring:
            continue
        if not _ring_stays_inside(ring, points):
            continue
        return ring
    return None


def _nearest_on_boundary(p: Sequence[float], boundary: Sequence[Sequence[float]]) -> Tuple[float, float]:
    pts = [(float(q[0]), float(q[1])) for q in boundary]
    if len(pts) >= 2 and _dist(pts[0], pts[-1]) > 1e-6:
        pts.append(pts[0])
    return tuple(_nearest_point_on_polyline(p, pts))


PROFILES: Dict[str, Dict[str, Any]] = {
    "compact": {
        "key": "A", "name": "A 紧凑经济型", "tag": "省地、省道路、一次投入低",
        "road_width_m": 3.5, "lanes": 1, "inset_m": 7.0, "margin_m": 3.0,
        "hydrants": 6, "gates": ["S"], "gate_offset_m": 0.0,
        "sizes_m": {
            "processing_zone": (16, 9), "steel_processing": (12, 7),
            "wood_processing": (8, 5), "mortar_processing": (6, 4),
            "material_yard": (9, 7),
            "site_office": (10, 6), "temporary_dormitory": (10, 6),
            # 0.7.0 生活区：员工宿舍与工人生活区分设；食堂/卫生间/晾晒为生活区子块
            "staff_dormitory": (10, 6), "worker_living_zone": (24, 15),
            "canteen": (6, 4), "toilet_shower": (4, 3), "drying_area": (5, 4),
            "parking": (14, 7), "distribution_room": (5, 4),
            "transformer": (3, 2.5), "fire_pump_room": (4, 3),
            "fire_water_tank": (5, 3),
            "waste_pool": (4, 3), "wheel_wash": (5, 3), "weighbridge": (12, 4.6),
            "safety_podium": (5, 3), "temporary_building": (8, 4),
        },
        "prefs": {
            "processing_zone": (0.76, 0.24), "steel_processing": (0.78, 0.22),
            "wood_processing": (0.64, 0.30), "mortar_processing": (0.80, 0.40),
            "material_yard": (0.88, 0.28),
            "site_office": (0.14, 0.30), "temporary_dormitory": (0.14, 0.62),
            "staff_dormitory": (0.26, 0.18), "worker_living_zone": (0.16, 0.74),
            "canteen": (0.20, 0.78), "toilet_shower": (0.20, 0.50),
            "drying_area": (0.20, 0.22),
            "parking": (0.24, 0.18), "distribution_room": (0.12, 0.20),
            "transformer": (0.20, 0.18), "fire_pump_room": (0.88, 0.62),
            "fire_water_tank": (0.80, 0.66),
            "waste_pool": (0.90, 0.16), "wheel_wash": (0.62, 0.16),
            "weighbridge": (0.58, 0.10),
            "safety_podium": (0.42, 0.18), "temporary_building": (0.24, 0.48),
        },
        "weights": {"cost": 0.22, "constructability": 0.18, "safety": 0.14,
                    "fire": 0.12, "traffic": 0.12, "environment": 0.08,
                    "schedule": 0.08, "reviewability": 0.06},
        "note": "单车道 3.5m，靠会车点解决；生活区压到最小，适合场地紧、工期短。",
    },
    "balanced": {
        "key": "B", "name": "B 均衡推荐型", "tag": "安全、成本、可实施性折中",
        "road_width_m": 4.5, "lanes": 1, "inset_m": 8.0, "margin_m": 4.0,
        "hydrants": 6, "gates": ["S", "W"], "gate_offset_m": 8.0,
        "sizes_m": {
            "processing_zone": (18, 10), "steel_processing": (14, 8),
            "wood_processing": (8, 5), "mortar_processing": (7, 4),
            "material_yard": (10, 7),
            "site_office": (12, 7), "temporary_dormitory": (12, 7),
            # 0.7.0 生活区基准尺寸；场地不足时按 85%/70%/60%/50% 降级并写入说明
            "staff_dormitory": (12, 7), "worker_living_zone": (28, 18),
            "canteen": (8, 5), "toilet_shower": (5, 3.5), "drying_area": (6, 4),
            "parking": (16, 8), "distribution_room": (6, 5),
            "transformer": (3.5, 3), "fire_pump_room": (5, 3.5),
            "fire_water_tank": (6, 4),
            "waste_pool": (5, 4), "wheel_wash": (6, 4), "weighbridge": (14, 4.8),
            "safety_podium": (6, 4), "temporary_building": (9, 5),
        },
        "prefs": {
            "processing_zone": (0.78, 0.24), "steel_processing": (0.80, 0.22),
            "wood_processing": (0.64, 0.32), "mortar_processing": (0.80, 0.42),
            "material_yard": (0.88, 0.26),
            "site_office": (0.16, 0.28), "temporary_dormitory": (0.16, 0.62),
            "staff_dormitory": (0.28, 0.18), "worker_living_zone": (0.16, 0.74),
            "canteen": (0.20, 0.78), "toilet_shower": (0.20, 0.50),
            "drying_area": (0.20, 0.22),
            "parking": (0.26, 0.18), "distribution_room": (0.12, 0.22),
            "transformer": (0.20, 0.20), "fire_pump_room": (0.88, 0.62),
            "fire_water_tank": (0.80, 0.66),
            "waste_pool": (0.90, 0.16), "wheel_wash": (0.62, 0.16),
            "weighbridge": (0.58, 0.10),
            "safety_podium": (0.42, 0.16), "temporary_building": (0.26, 0.48),
        },
        "weights": {"cost": 0.14, "constructability": 0.16, "safety": 0.18,
                    "fire": 0.15, "traffic": 0.14, "environment": 0.10,
                    "schedule": 0.08, "reviewability": 0.05},
        "note": "4.5m 单车道 + 南/西双出入口 + 六消火栓，作为默认比选基线。",
    },
    "safe": {
        "key": "C", "name": "C 安全文明型", "tag": "双车道、宽间距、便于检查和观摩",
        "road_width_m": 6.0, "lanes": 2, "inset_m": 4.0, "margin_m": 3.0,
        "hydrants": 8, "gates": ["S", "W"], "gate_offset_m": 12.0,
        "sizes_m": {
            "processing_zone": (20, 11), "steel_processing": (16, 9),
            "wood_processing": (10, 6), "mortar_processing": (8, 5),
            "material_yard": (12, 8),
            "site_office": (14, 8), "temporary_dormitory": (14, 8),
            # 0.7.0 生活区基准尺寸；场地不足时按 85%/70%/60%/50% 降级并写入说明
            "staff_dormitory": (14, 8), "worker_living_zone": (32, 20),
            "canteen": (9, 6), "toilet_shower": (6, 4), "drying_area": (7, 5),
            "parking": (18, 9), "distribution_room": (7, 5),
            "transformer": (5, 4), "fire_pump_room": (6, 4),
            "fire_water_tank": (8, 5),
            "waste_pool": (6, 4), "wheel_wash": (7, 4), "weighbridge": (16, 5.0),
            "safety_podium": (7, 4), "temporary_building": (10, 5),
        },
        "prefs": {
            "processing_zone": (0.82, 0.55), "steel_processing": (0.82, 0.22),
            "wood_processing": (0.64, 0.34), "mortar_processing": (0.82, 0.44),
            "material_yard": (0.84, 0.30),
            "site_office": (0.14, 0.28), "temporary_dormitory": (0.16, 0.62),
            "staff_dormitory": (0.26, 0.18), "worker_living_zone": (0.16, 0.74),
            "canteen": (0.20, 0.78), "toilet_shower": (0.20, 0.50),
            "drying_area": (0.20, 0.22),
            "parking": (0.26, 0.18), "distribution_room": (0.12, 0.22),
            "transformer": (0.20, 0.20), "fire_pump_room": (0.88, 0.62),
            "fire_water_tank": (0.80, 0.66),
            "waste_pool": (0.90, 0.16), "wheel_wash": (0.62, 0.16),
            "weighbridge": (0.58, 0.10),
            "safety_podium": (0.42, 0.16), "temporary_building": (0.26, 0.48),
        },
        "weights": {"cost": 0.07, "constructability": 0.13, "safety": 0.23,
                    "fire": 0.18, "traffic": 0.16, "environment": 0.12,
                    "schedule": 0.06, "reviewability": 0.05},
        "note": "6m 双车道、4m 环道中心退距、8 消火栓；成本高，但适合检查、观摩和高层项目。",
    },
}


def load_requirements(path: str | Path | None) -> Dict[str, Any]:
    if not path:
        return {"schema": REQ_SCHEMA, "project": "", "preferences": {}, "assumptions": []}
    file = Path(path).expanduser()
    if not file.is_file():
        raise GeneratorError(f"找不到需求文件：{file}")
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GeneratorError(f"需求文件不是合法 JSON：{file}：{exc}") from exc
    if not isinstance(data, dict):
        raise GeneratorError("需求文件顶层必须是对象")
    schema = str(data.get("schema") or REQ_SCHEMA)
    if schema != REQ_SCHEMA:
        raise GeneratorError(f"需求文件 schema={schema!r}；只接受 {REQ_SCHEMA}")
    data["_path"] = str(file.resolve())
    data["_sha256"] = __import__("hashlib").sha256(file.read_bytes()).hexdigest()
    return data


def _req_points(raw: Any, label: str, factor: float) -> List[Tuple[float, float]]:
    if not isinstance(raw, list) or len(raw) < 3:
        raise GeneratorError(f"{label} 必须是至少 3 点的数组")
    points = []
    for i, item in enumerate(raw):
        if isinstance(item, dict):
            item = [item.get("x"), item.get("y")]
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            raise GeneratorError(f"{label}[{i}] 必须是 [x, y]")
        points.append((_f(item[0], label) * factor, _f(item[1], label) * factor))
    return points


def _req_unit(data: Dict[str, Any]) -> float:
    raw = data.get("coord_unit")
    text = str(raw or "").strip().lower()
    if not text:
        return 1.0
    if text not in UNIT_TO_MM:
        raise GeneratorUnitError("requirements.coord_unit 只接受 mm/cm/m")
    return UNIT_TO_MM[text]


def _building_from(base_map: Dict[str, Any], requirements: Dict[str, Any],
                   bbox: Sequence[float], assumptions: List[str],
                   ) -> Tuple[Tuple[float, float, float, float], str]:
    """返回 (外接矩形 mm, 来源)。来源：requirements / base_map / assumed。

    assumed 表示底图与需求都没给主体轮廓，这里按场地中部 42%×32% 矩形兜底。
    该兜底只能用于“看功能”的草案；generate_layout 默认拒绝在 assumed 上出 A/B/C，
    否则塔吊覆盖、施工电梯贴边、道路避让全都建立在一栋假楼上。
    """
    x0, y0, x1, y1 = bbox
    if not str(requirements.get("coord_unit") or "").strip():
        assumptions.append("requirements 未声明 coord_unit，按 mm 解释建筑轮廓；请补单位后复核。")
    factor = _req_unit(requirements)
    raw = None
    building = requirements.get("building")
    if isinstance(building, dict):
        raw = building.get("footprint") or building.get("points")
    if raw is None and isinstance(requirements.get("building_footprints"), list):
        first = requirements["building_footprints"][0]
        if isinstance(first, dict):
            raw = first.get("footprint") or first.get("points")
    if raw is not None:
        if not str(requirements.get("coord_unit") or "").strip():
            assumptions.append("需求文件 building.footprint 未声明 coord_unit，按 mm 解释；请补单位。")
        points = _req_points(raw, "building.footprint", factor)
        bx0, by0, bx1, by1 = _bbox(points)
        return (bx0, by0, bx1, by1), "requirements"
    candidate = None
    if isinstance(base_map.get("buildings"), list) and base_map["buildings"]:
        first = base_map["buildings"][0]
        if isinstance(first, dict):
            candidate = first.get("footprint") or first.get("points")
    if candidate is None:
        candidate = base_map.get("structure_outline")
    if isinstance(candidate, list) and len(candidate) >= 3:
        pts = [(float(item[0]), float(item[1])) for item in candidate]
        bx0, by0, bx1, by1 = _bbox(pts)
        return (bx0, by0, bx1, by1), "base_map"
    width = (x1 - x0) * 0.42
    depth = (y1 - y0) * 0.32
    cx = (x0 + x1) / 2
    cy = y0 + (y1 - y0) * 0.58
    assumptions.append("未提供拟建主体轮廓，按场地中部 42%×32% 的矩形假定，仅用于布置草案；施工前必须用建筑总平面图替换。")
    return (cx - width / 2, cy - depth / 2, cx + width / 2, cy + depth / 2), "assumed"


def _interior_bbox(boundary: Sequence[Sequence[float]], margin_mm: float) -> Tuple[float, float, float, float]:
    x0, y0, x1, y1 = _bbox(boundary)
    return x0 + margin_mm, y0 + margin_mm, x1 - margin_mm, y1 - margin_mm


class _BoundaryIndex:
    """红线几何加速索引：只改计算方式，不改判定语义。

    判定仍是“矩形四角都在红线内，且四角距边界 >= margin”。
    - 外接矩形快速拒绝：绝大多数远离场地或出界的候选一次比较就淘汰；
    - 扫描线交点缓存：同一行 y 的四角包含判断只算一次交点表；
    - 边段分桶：距离只算邻近边段，不再每次遍历全部 100+ 个红线点。
    """

    CELL_MM = 10_000.0
    INDEX_MARGIN_MM = 8_000.0

    def __init__(self, points: Sequence[Sequence[float]]) -> None:
        self.points = [(float(p[0]), float(p[1])) for p in points]
        self.bbox = _bbox(self.points) if self.points else (0.0, 0.0, 0.0, 0.0)
        self.segments = ([(self.points[i], self.points[(i + 1) % len(self.points)])
                          for i in range(len(self.points))] if self.points else [])
        self.grid: Dict[Tuple[int, int], List[int]] = {}
        self._crossings: Dict[float, List[float]] = {}
        self._build_grid()

    def _key(self, x: float, y: float) -> Tuple[int, int]:
        return (int(math.floor((x - self.bbox[0]) / self.CELL_MM)),
                int(math.floor((y - self.bbox[1]) / self.CELL_MM)))

    def _build_grid(self) -> None:
        margin = self.INDEX_MARGIN_MM
        for index, (a, b) in enumerate(self.segments):
            x_lo, x_hi = min(a[0], b[0]) - margin, max(a[0], b[0]) + margin
            y_lo, y_hi = min(a[1], b[1]) - margin, max(a[1], b[1]) + margin
            ix0 = int(math.floor((x_lo - self.bbox[0]) / self.CELL_MM))
            ix1 = int(math.floor((x_hi - self.bbox[0]) / self.CELL_MM))
            iy0 = int(math.floor((y_lo - self.bbox[1]) / self.CELL_MM))
            iy1 = int(math.floor((y_hi - self.bbox[1]) / self.CELL_MM))
            for ix in range(ix0, ix1 + 1):
                for iy in range(iy0, iy1 + 1):
                    self.grid.setdefault((ix, iy), []).append(index)

    def _row_crossings(self, y: float) -> List[float]:
        key = round(y, 6)
        xs = self._crossings.get(key)
        if xs is None:
            xs = []
            for a, b in self.segments:
                yi, yj = a[1], b[1]
                if (yi > y) != (yj > y):
                    xs.append((b[0] - a[0]) * (y - yi) / (yj - yi) + a[0])
            xs.sort()
            self._crossings[key] = xs
        return xs

    def contains(self, point: Sequence[float]) -> bool:
        x, y = float(point[0]), float(point[1])
        bx0, by0, bx1, by1 = self.bbox
        if not self.points or x < bx0 or x > bx1 or y < by0 or y > by1:
            return False
        xs = self._row_crossings(y)
        # 与原 _point_in_polygon 一致：统计交点 x 严格大于待判点 x 的个数，奇数在内
        return (len(xs) - bisect.bisect_right(xs, x)) % 2 == 1

    def distance(self, point: Sequence[float]) -> float:
        if not self.segments:
            return float("inf")
        candidates = self.grid.get(self._key(float(point[0]), float(point[1])))
        if not candidates:
            return float("inf")
        return min(_point_segment(point, *self.segments[index]) for index in candidates)

    def inside_rect(self, rect: Sequence[float], margin_mm: float) -> bool:
        if not self.points:
            return True
        x0, y0, x1, y1 = (float(v) for v in rect)
        bx0, by0, bx1, by1 = self.bbox
        if (x0 < bx0 + margin_mm or y0 < by0 + margin_mm
                or x1 > bx1 - margin_mm or y1 > by1 - margin_mm):
            return False
        for p in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
            if not self.contains(p):
                return False
            if margin_mm <= 0:
                continue
            if margin_mm > self.INDEX_MARGIN_MM:
                # 超过索引覆盖半径时退回全量边段，保证不因索引漏判
                if min(_point_segment(p, *seg) for seg in self.segments) < margin_mm:
                    return False
            elif self.distance(p) < margin_mm:
                return False
        return True


def _inside(rect: Sequence[float], boundary: Sequence[Sequence[float]], margin_mm: float) -> bool:
    """兼容入口：外部只有偶尔调用；内部热路径使用 _Layout.boundary_index。"""
    if not boundary:
        return True
    return _BoundaryIndex(boundary).inside_rect(rect, margin_mm)


def _segment_crosses_rect(a: Sequence[float], b: Sequence[float],
                          rect: Sequence[float]) -> bool:
    """Liang-Barsky：线段是否穿过矩形（含完全在内）。"""
    xmin, ymin, xmax, ymax = rect
    dx, dy = b[0] - a[0], b[1] - a[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, a[0] - xmin), (dx, xmax - a[0]),
                 (-dy, a[1] - ymin), (dy, ymax - a[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return False
            continue
        r = q / p
        if p < 0:
            if r > t1:
                return False
            t0 = max(t0, r)
        else:
            if r < t0:
                return False
            t1 = min(t1, r)
    return t0 <= t1


def _hits_road(rect: Sequence[float], roads: Sequence[Dict[str, Any]], gap_mm: float) -> bool:
    """按道路带宽向外扩 gap 后做线段—矩形相交；防止矩形横跨道路带却四角都远离中线。"""
    for road in roads:
        points = list(road["geometry"]["points_mm"])
        # 闭合环道最后一段（末点→首点）不在 points 数组里；漏掉它会让设施
        # 压在西/北侧环路上却通过初筛，随后规则 24 才报“道路穿越生活区”。
        geom = road.get("geometry") or {}
        if geom.get("closed") and len(points) > 2 and _dist(points[0], points[-1]) > 1e-6:
            points.append(points[0])
        half = float(road.get("width_mm") or 4000.0) / 2.0
        pad = half + gap_mm
        expanded = (rect[0] - pad, rect[1] - pad, rect[2] + pad, rect[3] + pad)
        for i in range(len(points) - 1):
            if _segment_crosses_rect(points[i], points[i + 1], expanded):
                return True
    return False


def _hits_placed(rect: Sequence[float], placed: Sequence[Dict[str, Any]], gap_mm: float) -> bool:
    for item in placed:
        need = max(gap_mm, float(item.get("gap_mm") or 0.0))
        if _rect_rect_gap(rect, item["rect"]) < need - 1e-6:
            return True
    return False


def _crane_blocked(rect: Sequence[float], category: str, cranes: Sequence[Dict[str, Any]],
                   margin_mm: float = 2000.0) -> bool:
    """人员密集临建与塔吊回转半径的初筛。

    办公/旧临建按矩形最近边判定，偏保守；生活区包络与员工宿舍按形心判定，
    与 siteplan 规则 6 保持同一口径，避免“生成时按最近边永远放不下、校核时
    又按形心通过”的自相矛盾。形心通过不等于边缘安全，必须在塔吊选型后复核。
    """
    if category not in CRANE_SENSITIVE:
        return False
    if category in CENTROID_CRANE_CATEGORIES:
        point = ((rect[0] + rect[2]) / 2.0, (rect[1] + rect[3]) / 2.0)
    else:
        point = None
    for crane in cranes:
        center = crane.get("center_mm")
        jib = crane.get("jib_mm")
        if not center or not jib:
            continue
        if point is not None:
            # 形心口径与规则 6 完全一致，不再额外加 2m 余量；
            # 否则生活区包络在常规场地永远无法落位。
            hit = _dist(point, center) <= float(jib)
        else:
            hit = _rect_distance_to_point(rect, center) <= float(jib) + margin_mm
        if hit:
            return True
    return False


def _gap_ok(rect: Sequence[float], category: str, placed: Sequence[Dict[str, Any]],
            params: Dict[str, float]) -> bool:
    center = ((rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2)
    for item in placed:
        other = item["category"]
        other_center = ((item["rect"][0] + item["rect"][2]) / 2,
                        (item["rect"][1] + item["rect"][3]) / 2)
        distance = _dist(center, other_center)
        if category in PROCESSING and other in QUIET_GENERATOR:
            if distance < params["processing_separation_m"] * 1000.0:
                return False
        if other in PROCESSING and category in QUIET_GENERATOR:
            if distance < params["processing_separation_m"] * 1000.0:
                return False
        if category == "waste_pool" and other in QUIET_GENERATOR:
            if distance < params["waste_separation_m"] * 1000.0:
                return False
        if other == "waste_pool" and category in QUIET_GENERATOR:
            if distance < params["waste_separation_m"] * 1000.0:
                return False
        # 员工宿舍与工人生活区之间留 3m 边净距，避免宿舍门窗正对生活区喧闹面。
        if {category, other} == {"staff_dormitory", "worker_living_zone"}:
            if _rect_rect_gap(rect, item["rect"]) < params["living_separation_min_m"] * 1000.0:
                return False
        # 变压器按“最近边净距”避让人员区和可燃堆场；中心距会在大体块下
        # 虚报安全（例如 9m 长临建中心距 12m，边缘只剩 7.5m）。
        living = QUIET_GENERATOR
        combustible = ("wood_processing", "material_yard")
        if category == "transformer" and other in living:
            if _rect_rect_gap(rect, item["rect"]) < params["transformer_to_living_min_m"] * 1000.0:
                return False
        if other == "transformer" and category in living:
            if _rect_rect_gap(rect, item["rect"]) < params["transformer_to_living_min_m"] * 1000.0:
                return False
        if category == "transformer" and other in combustible:
            if _rect_rect_gap(rect, item["rect"]) < params["transformer_to_combustible_min_m"] * 1000.0:
                return False
        if other == "transformer" and category in combustible:
            if _rect_rect_gap(rect, item["rect"]) < params["transformer_to_combustible_min_m"] * 1000.0:
                return False
    return True


def _make_area(fid: str, category: str, name: str, rect: Sequence[float],
               stages: Sequence[str], attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    info = meta(category)
    return {
        "id": fid, "category": category, "category_name": info["zh"], "name": name,
        "geometry": {"type": "area", "points_mm": _rect_polygon(rect), "closed": True},
        "width_mm": None, "active_stages": list(stages), "source": "auto-layout",
        "confidence": "candidate", "evidence": [], "attrs": attrs or {}, "raw_status": "candidate",
    }


def _make_area_poly(fid: str, category: str, name: str,
                    points: Sequence[Sequence[float]], stages: Sequence[str],
                    attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """任意多边形区域设施（顺红线/顺道路的长条设施用）。"""
    info = meta(category)
    return {
        "id": fid, "category": category, "category_name": info["zh"], "name": name,
        "geometry": {"type": "area",
                     "points_mm": [(float(p[0]), float(p[1])) for p in points],
                     "closed": True},
        "width_mm": None, "active_stages": list(stages), "source": "auto-layout",
        "confidence": "candidate", "evidence": [], "attrs": attrs or {}, "raw_status": "candidate",
    }


def _make_point(fid: str, category: str, name: str, point: Sequence[float],
                stages: Sequence[str], attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    info = meta(category)
    return {
        "id": fid, "category": category, "category_name": info["zh"], "name": name,
        "geometry": {"type": "point", "points_mm": [(float(point[0]), float(point[1]))], "closed": False},
        "width_mm": None, "active_stages": list(stages), "source": "auto-layout",
        "confidence": "candidate", "evidence": [], "attrs": attrs or {}, "raw_status": "candidate",
    }


def _make_line(fid: str, category: str, name: str, points: Sequence[Sequence[float]],
               stages: Sequence[str], width_m: Optional[float] = None,
               closed: bool = False, attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    info = meta(category)
    return {
        "id": fid, "category": category, "category_name": info["zh"], "name": name,
        "geometry": {"type": "line", "points_mm": [(float(p[0]), float(p[1])) for p in points],
                     "closed": bool(closed)},
        "width_mm": None if width_m is None else float(width_m) * 1000.0,
        "active_stages": list(stages), "source": "auto-layout",
        "confidence": "candidate", "evidence": [], "attrs": attrs or {}, "raw_status": "candidate",
    }


def _default_params() -> Dict[str, float]:
    # 与 siteplan.DEFAULT_PARAMS 的分项隔离经验值保持一致，避免生成后自检自相矛盾
    return {"processing_separation_m": 12.0, "waste_separation_m": 22.0,
            "notice_to_gate_m": 45.0, "parking_to_gate_m": 60.0,
            "steel_processing_separation_m": 10.0,
            "wood_processing_separation_m": 12.0,
            "mortar_processing_separation_m": 15.0,
            "wood_to_power_min_m": 15.0,
            "transformer_to_living_min_m": 10.0,
            "transformer_to_combustible_min_m": 10.0,
            # 0.7.0 生活区（与 siteplan.DEFAULT_PARAMS 同步）
            "living_to_processing_min_m": 20.0,
            "living_to_worksite_min_m": 10.0,
            "office_to_gate_max_m": 50.0,
            "living_fire_lane_max_m": 30.0,
            "living_separation_min_m": 3.0}


class _Layout:
    def __init__(self, base_map: Dict[str, Any], context: Dict[str, Any],
                 requirements: Dict[str, Any], cranes: Sequence[Dict[str, Any]],
                 profile: Dict[str, Any], allow_assumed_building: bool = False) -> None:
        self.allow_assumed_building = bool(allow_assumed_building)
        self.building_source = ""
        self.base_map = base_map
        self.context = context
        self.requirements = requirements
        self.profile = profile
        self.assumptions: List[str] = list(requirements.get("assumptions") or [])
        self.assumptions += list(context.get("warnings") or [])
        boundary = base_map.get("redline") or context.get("boundary") or []
        if isinstance(boundary, list) and len(boundary) >= 3:
            self.boundary = [(float(p[0]), float(p[1])) for p in boundary]
        else:
            ext = base_map.get("extents_mm") or [0, 0, 100000, 60000]
            self.boundary = [(ext[0], ext[1]), (ext[2], ext[1]), (ext[2], ext[3]), (ext[0], ext[3])]
            self.assumptions.append("底图无闭合红线，按 extents 矩形假定场地边界。")
        if len(self.boundary) != 4:
            self.assumptions.append("红线不是矩形：环道按红线内缩生成；凹口、弧段与门位仍需人工复核。")
        self.ring_source = ""
        self.bbox = _bbox(self.boundary)
        self.boundary_index = _BoundaryIndex(self.boundary)
        self.params = _default_params()
        self.cranes = list(cranes)
        self.facilities: List[Dict[str, Any]] = []
        self.placed: List[Dict[str, Any]] = []
        self.roads: List[Dict[str, Any]] = []
        self.ring: List[Tuple[float, float]] = []
        self.gate_access: List[List[Tuple[float, float]]] = []
        self.gate_used: int = 0
        self.metrics: Dict[str, Any] = {}

    def _factor(self) -> float:
        return _req_unit(self.requirements)

    def _size(self, category: str) -> Tuple[float, float]:
        return self.profile["sizes_m"][category]

    def _try_sizes(self, category: str) -> List[Tuple[float, float]]:
        base = self._size(category)
        variants = [base, (max(4.0, base[0] * 0.85), max(3.0, base[1] * 0.85)),
                    (max(3.5, base[0] * 0.7), max(2.5, base[1] * 0.7))]
        if category in ("worker_living_zone", "staff_dormitory"):
            # 生活区受红线、环道、主体和塔吊多重夹逼，允许继续降级；
            # 降级结果必须写入 attrs.note 与 assumptions，不能静默。
            variants += [(max(3.5, base[0] * 0.6), max(3.0, base[1] * 0.6)),
                         (max(3.5, base[0] * 0.5), max(3.0, base[1] * 0.5)),
                         (max(3.0, base[0] * 0.4), max(2.5, base[1] * 0.4))]
        seen = set()
        result = []
        for item in variants:
            key = (round(item[0], 2), round(item[1], 2))
            if key not in seen:
                result.append(item)
                seen.add(key)
        return result

    def _score_position(self, rect: Sequence[float], category: str,
                        preferred: Sequence[float], gate_points: Sequence[Sequence[float]]) -> float:
        cx, cy = (rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2
        x0, y0, x1, y1 = self.bbox
        width, height = max(1.0, x1 - x0), max(1.0, y1 - y0)
        pref = (x0 + preferred[0] * width, y0 + preferred[1] * height)
        score = 2.4 * (_dist((cx, cy), pref) / max(width, height))
        if category in ("notice_board", "safety_podium", "parking", "wheel_wash"):
            if gate_points:
                score += 0.7 * (min(_dist((cx, cy), g) for g in gate_points) / max(width, height))
        if category == "site_office" and gate_points:
            # 办公区要接待、考勤和应急集合，权重高于一般设施，优先贴最近出入口。
            score += 1.0 * (min(_dist((cx, cy), g) for g in gate_points) / max(width, height))
        if category in ("worker_living_zone", "staff_dormitory"):
            # 生活区优先靠西/北侧围挡，为后续“上风向待确认”留出调整余地；
            # 这里只做候选排序，不把西/北侧说成已证明的上风向。
            score += 0.25 * ((y1 - cy) / height + (cx - x0) / width * 0.0)
        if category in PROCESSING:
            score += 0.5 * (min(_dist((cx, cy), (p[0], p[1])) for p in self.building_poly) / max(width, height))
        if category == "material_yard":
            procs = [item for item in self.placed if item["category"] in PROCESSING]
            if procs:
                pc = min((((item["rect"][0] + item["rect"][2]) / 2,
                           (item["rect"][1] + item["rect"][3]) / 2) for item in procs),
                         key=lambda q: _dist((cx, cy), q))
                score += 0.7 * (abs(_dist((cx, cy), pc) - 12000.0) / 12000.0)
        return score

    def _hard_ok(self, rect: Sequence[float], category: str, gate_points: Sequence[Sequence[float]]) -> bool:
        if not self.boundary_index.inside_rect(rect, self.profile["margin_m"] * 1000.0):
            return False
        center = ((rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2)
        # 距离大门的门限是廉价约束，先挡掉远离大门的候选，避免做道路/已放设施检查
        if category in ("notice_board", "safety_podium", "wheel_wash") and gate_points:
            if min(_dist(center, g) for g in gate_points) > self.params["notice_to_gate_m"] * 1000.0:
                return False
        if category == "parking" and gate_points:
            if min(_dist(center, g) for g in gate_points) > self.params["parking_to_gate_m"] * 1000.0:
                return False
        if category not in ("tower_crane",) and _rect_rect_gap(rect, self.building_rect) < 1500.0:
            return False
        if _hits_placed(rect, self.placed, 1500.0):
            return False
        if _hits_road(rect, self.roads, 1500.0):
            return False
        if geometry_blocked({"type": "area", "points_mm": _rect_polygon(rect), "closed": True},
                            self.context, category):
            return False
        if _crane_blocked(rect, category, self.cranes):
            return False
        if not _gap_ok(rect, category, self.placed, self.params):
            return False
        return True

    def place_area(self, category: str, name: str, fid: str, stages: Sequence[str],
                   preferred: Optional[Sequence[float]] = None,
                   gate_points: Sequence[Sequence[float]] = (),
                   attrs_extra: Optional[Dict[str, Any]] = None,
                   note: str = "") -> Tuple[float, float, float, float]:
        if preferred is None:
            preferred = self.profile["prefs"][category]
        x0, y0, x1, y1 = self.bbox
        margin = self.profile["margin_m"] * 1000.0
        best: Optional[Tuple[float, Dict[str, Any]]] = None
        step = 2000.0
        tried = 0
        exhausted = False
        for w_m, d_m in self._try_sizes(category):
            w, d = w_m * 1000.0, d_m * 1000.0
            if w > (x1 - x0) - 2 * margin or d > (y1 - y0) - 2 * margin:
                continue
            y = y0 + margin + d / 2
            while y <= y1 - margin - d / 2 + 1e-6:
                x = x0 + margin + w / 2
                while x <= x1 - margin - w / 2 + 1e-6:
                    tried += 1
                    if tried > MAX_PLACEMENT_CANDIDATES:
                        exhausted = True
                        break
                    rect = (x - w / 2, y - d / 2, x + w / 2, y + d / 2)
                    if self._hard_ok(rect, category, gate_points):
                        score = self._score_position(rect, category, preferred, gate_points)
                        if best is None or score < best[0] - 1e-9:
                            best = (score, {"rect": rect, "size": (w, d)})
                    x += step
                if exhausted:
                    break
                y += step
            if exhausted or best is not None:
                break
        if best is None:
            reason = (
                f"自动选址已尝试 {tried} 个候选（预算 {MAX_PLACEMENT_CANDIDATES}）仍未找到可行位置，"
                "已停止以避免无限扫描"
                if exhausted else
                f"无法为 {meta(category)['zh']} 找到满足边界/道路/塔吊/周边约束的位置"
            )
            raise GeneratorError(
                reason + "；请缩小设施尺寸、放宽场地或人工指定位置"
            )
        rect = best[1]["rect"]
        attrs: Dict[str, Any] = {"scheme": self.profile["key"],
                                 "assumption": "自动候选位置，需项目确认"}
        if attrs_extra:
            attrs.update(attrs_extra)
        base_w, base_d = self._size(category)
        used_w, used_d = best[1]["size"][0] / 1000.0, best[1]["size"][1] / 1000.0
        if category in ("worker_living_zone", "staff_dormitory") and (
                used_w < base_w - 0.05 or used_d < base_d - 0.05):
            size_note = (
                "受红线/环道/主体/塔吊夹逼，{} 基准 {:.1f}×{:.1f} m 降级为 "
                "{:.1f}×{:.1f} m（{:.0f} m²）；只是候选示意，实际面积必须按人数、"
                "床位数和消防疏散重新选址确认。".format(
                    meta(category)["zh"], base_w, base_d, used_w, used_d, used_w * used_d))
            attrs["size_degraded"] = True
            attrs["size_note"] = size_note
            attrs["note"] = (attrs.get("note", "") + "；" + size_note).strip("；")
            if size_note not in self.assumptions:
                self.assumptions.append(size_note)
        if note:
            attrs["note"] = (attrs.get("note", "") + "；" + note).strip("；")
        self.facilities.append(_make_area(fid, category, name, rect, stages, attrs))
        self.placed.append({"category": category, "rect": rect, "gap_mm": 1500.0})
        return tuple(rect)

    def place_living_children(self, parent_rect: Sequence[float], parent_id: str,
                              specs: Sequence[Dict[str, Any]], stages: Sequence[str],
                              gap_mm: float = 800.0) -> Dict[str, Tuple[float, float, float, float]]:
        """在生活区包络内整体布置食堂/卫生间/晾晒子块（0.7.0）。

        与逐个子块贪心不同：这里把三块尺寸组合放在一起搜索。组合先按
        “最差一块的保持比例”排序，再在固定尺寸下做带面积剪枝的回溯；
        前面的子块放不下时回退，允许缩小先前子块，避免食堂先占大块后
        卫生间无位可放。子块不进入全局 placed（父包络已占位），只与本地
        siblings 检查净距；所有子块角点必须完全落在父区域内，形心避开
        塔吊回转半径（与 siteplan 规则 6 同一口径）。
        """
        px0, py0, px1, py1 = parent_rect
        inset = 600.0
        step = 250.0
        avail_w = max(0.0, (px1 - px0) - 2.0 * inset)
        avail_d = max(0.0, (py1 - py0) - 2.0 * inset)
        if avail_w < 3000.0 or avail_d < 2500.0:
            raise GeneratorError(
                "工人生活区 {} 内部可用尺寸仅 {:.1f}×{:.1f} m，无法容纳食堂/卫生间/晾晒；"
                "请扩大生活区包络或人工指定子块位置".format(
                    parent_id, avail_w / 1000.0, avail_d / 1000.0))

        base_sizes = {spec["category"]: self._size(spec["category"]) for spec in specs}
        option_map: Dict[str, List[Tuple[float, float, float]]] = {}
        for spec in specs:
            category = spec["category"]
            base_w, base_d = base_sizes[category]
            options: List[Tuple[float, float, float]] = []
            seen = set()
            # 逐级尝试 85%/70%/60%/50%，保留最小可用尺寸；降级会写入 attrs 与 assumptions。
            for factor in (1.0, 0.85, 0.7, 0.6, 0.5):
                w = min(max(2.0, base_w * factor) * 1000.0, avail_w)
                d = min(max(1.5, base_d * factor) * 1000.0, avail_d)
                if w < 1800.0 or d < 1200.0:
                    continue
                key = (round(w), round(d))
                if key in seen:
                    continue
                seen.add(key)
                options.append((w, d, factor))
            if not options:
                raise GeneratorError(
                    "工人生活区 {} 内部空间不足，无法为 {} 生成候选尺寸".format(
                        parent_id, meta(category)["zh"]))
            option_map[category] = options

        combos: List[Tuple[Tuple[Tuple[float, float, float], ...], Tuple[float, float, float]]] = []
        for combo in itertools.product(*(option_map[spec["category"]] for spec in specs)):
            scales = []
            area = 0.0
            for spec, (w, d, _factor) in zip(specs, combo):
                base_w, base_d = base_sizes[spec["category"]]
                scales.append(min(w / (base_w * 1000.0), d / (base_d * 1000.0)))
                area += w * d
            # 先保证“最差一块”不至于被压得太小，再比总面积；同分时保持输入顺序。
            score = (round(min(scales), 4), round(sum(scales), 4), round(area, 1))
            combos.append((combo, score))
        combos.sort(key=lambda item: item[1], reverse=True)

        order = sorted(specs, key=lambda spec: -(
            base_sizes[spec["category"]][0] * base_sizes[spec["category"]][1]))

        def _candidate_centers(spec: Dict[str, Any], w: float, d: float) -> List[Tuple[float, float]]:
            preferred = spec["preferred"]
            pref_x = px0 + float(preferred[0]) * (px1 - px0)
            pref_y = py0 + float(preferred[1]) * (py1 - py0)
            x_min, x_max = px0 + inset + w / 2.0, px1 - inset - w / 2.0
            y_min, y_max = py0 + inset + d / 2.0, py1 - inset - d / 2.0
            if x_max < x_min - 1e-6 or y_max < y_min - 1e-6:
                return []
            xs: List[float] = []
            x = x_min
            while x <= x_max + 1e-6:
                xs.append(x)
                x += step
            if x_max - xs[-1] > 1e-6:
                xs.append(x_max)
            ys: List[float] = []
            y = y_min
            while y <= y_max + 1e-6:
                ys.append(y)
                y += step
            if y_max - ys[-1] > 1e-6:
                ys.append(y_max)
            points = [(x, y) for y in ys for x in xs]
            points.sort(key=lambda p: (round(_dist(p, (pref_x, pref_y)), 2), p[1], p[0]))
            return points

        attempts = 0
        chosen_gap = gap_mm
        solution: Optional[Dict[str, Tuple[float, float, float, float]]] = None
        for gap in (gap_mm, 600.0, 500.0):
            if gap > gap_mm + 1e-6:
                continue
            chosen_gap = gap
            for combo, _score in combos:
                dims = {spec["category"]: (w, d, factor)
                        for spec, (w, d, factor) in zip(specs, combo)}
                total_area = sum(w * d for w, d, _factor in dims.values())
                if total_area > avail_w * avail_d + 1.0:
                    continue
                placed_local: List[Tuple[float, float, float, float]] = []
                combo_attempts = 0
                combo_exhausted = False

                def _search(index: int, free_area: float) -> bool:
                    nonlocal attempts, combo_attempts, combo_exhausted
                    if index == len(order):
                        return True
                    spec = order[index]
                    category = spec["category"]
                    w, d, _factor = dims[category]
                    remaining = sum(dims[item["category"]][0] * dims[item["category"]][1]
                                    for item in order[index:])
                    if remaining > free_area + 1.0:
                        return False
                    for x, y in _candidate_centers(spec, w, d):
                        attempts += 1
                        combo_attempts += 1
                        if attempts > MAX_LIVING_SEARCH_NODES or combo_attempts > MAX_LIVING_COMBO_NODES:
                            combo_exhausted = True
                            return False
                        rect = (x - w / 2.0, y - d / 2.0, x + w / 2.0, y + d / 2.0)
                        if not all(px0 + 1.0 <= cx <= px1 - 1.0
                                   and py0 + 1.0 <= cy <= py1 - 1.0
                                   for cx, cy in ((rect[0], rect[1]), (rect[2], rect[1]),
                                                  (rect[2], rect[3]), (rect[0], rect[3]))):
                            continue
                        if any(_rect_rect_gap(rect, other) < gap - 1e-6
                               for other in placed_local):
                            continue
                        center = ((rect[0] + rect[2]) / 2.0, (rect[1] + rect[3]) / 2.0)
                        blocked = False
                        for crane in self.cranes:
                            if (crane.get("center_mm") and crane.get("jib_mm")
                                    and _dist(center, crane["center_mm"]) <= float(crane["jib_mm"])):
                                blocked = True
                                break
                        if blocked:
                            continue
                        placed_local.append(rect)
                        if _search(index + 1, free_area - w * d):
                            return True
                        placed_local.pop()
                    return False

                if _search(0, avail_w * avail_d):
                    solution = {order[i]["category"]: placed_local[i]
                                for i in range(len(order))}
                    break
                if attempts > MAX_LIVING_SEARCH_NODES:
                    break
            if solution is not None or attempts > MAX_LIVING_SEARCH_NODES:
                break
        if solution is None:
            raise GeneratorError(
                "无法在工人生活区 {} 内同时布置食堂/卫生间/晾晒（组合搜索尝试 {} 个候选）；"
                "请扩大生活区包络、减少子项或人工指定子块位置".format(parent_id, attempts))

        if chosen_gap < gap_mm - 1e-6:
            gap_note = ("生活区子块净距按 {:.1f} m 候选布置（默认 {:.1f} m）；"
                        "实际净距须按消防、通行与使用要求复核。").format(
                            chosen_gap / 1000.0, gap_mm / 1000.0)
            if gap_note not in self.assumptions:
                self.assumptions.append(gap_note)

        result: Dict[str, Tuple[float, float, float, float]] = {}
        for spec in specs:
            category = spec["category"]
            rect = solution[category]
            result[category] = rect
            used_w = (rect[2] - rect[0]) / 1000.0
            used_d = (rect[3] - rect[1]) / 1000.0
            base_w, base_d = base_sizes[category]
            attrs: Dict[str, Any] = {
                "scheme": self.profile["key"],
                "assumption": "生活区内部子块自动候选位置，需项目确认",
                "parent_id": parent_id,
                "parent_name": "工人生活区",
                "inside_parent": True,
            }
            if used_w < base_w - 0.05 or used_d < base_d - 0.05:
                ratio = min(used_w / base_w, used_d / base_d)
                note = ("{} 放入 {} 时由 {:.1f}×{:.1f} m 收缩为 {:.1f}×{:.1f} m"
                        "（约为基准的 {:.0f}%）；面积与间距仅作候选示意，"
                        "须按人数、床位数与使用需求复核。").format(
                            meta(category)["zh"], parent_id, base_w, base_d,
                            used_w, used_d, ratio * 100.0)
                attrs["size_degraded"] = True
                attrs["size_note"] = note
                if note not in self.assumptions:
                    self.assumptions.append(note)
            self.facilities.append(_make_area(
                spec["fid"], category, spec["name"], rect, stages, attrs))
        return result

    def place_point_near(self, category: str, name: str, fid: str, stages: Sequence[str],
                         anchor: Sequence[float], radius_m: float = 8.0,
                         gate_points: Sequence[Sequence[float]] = ()) -> Tuple[float, float]:
        x0, y0, x1, y1 = self.bbox
        best: Optional[Tuple[float, Tuple[float, float]]] = None
        step = 1000.0
        ax, ay = anchor
        for attempt in range(4):
            r = radius_m * 1000.0 * (attempt + 1)
            y = max(y0, ay - r)
            while y <= min(y1, ay + r) + 1e-6:
                x = max(x0, ax - r)
                while x <= min(x1, ax + r) + 1e-6:
                    p = (x, y)
                    box = (x - 600, y - 600, x + 600, y + 600)
                    if (self.boundary_index.contains(p)
                            and not _point_in_polygon(p, self.building_poly)
                            and not _hits_road(box, self.roads, 1000.0)
                            and not _hits_placed(box, self.placed, 1200.0)):
                        if not point_blocked(p, self.context, category, 500.0):
                            score = _dist(p, anchor)
                            if best is None or score < best[0]:
                                best = (score, p)
                    x += step
                y += step
            if best is not None:
                break
        if best is None:
            raise GeneratorError(f"无法为 {meta(category)['zh']} 找到合适点位")
        p = best[1]
        self.facilities.append(_make_point(fid, category, name, p, stages,
                                           {"scheme": self.profile["key"],
                                            "assumption": "自动候选位置，需项目确认"}))
        return p

    def place_wheel_wash(self, gates: Sequence[Sequence[float]]) -> Tuple[float, float, float, float]:
        """洗车台跨出入口接入道路布置：遍历所有大门，选第一条能落界的接入段。

        车辆进出必过，不再放到路边空地。斜交门位、红线内收过紧时，第一个门
        可能放不下；此时应尝试后续大门，而不是让整套方案失败。
        """
        if not gates or not self.gate_access:
            raise GeneratorError("无大门/接入道路，无法布置洗车台")
        attempts: List[str] = []
        chosen: Optional[Tuple[int, float, float, float, List[Tuple[float, float]],
                                Tuple[float, float, float, float]]] = None
        for gate_index, access in enumerate(self.gate_access):
            a, b = access
            seg = _dist(a, b)
            if seg < 3600.0:
                attempts.append("大门 {} 接入段 {:.1f} m 不足 3.6 m".format(
                    gate_index + 1, seg / 1000.0))
                continue
            ux, uy = (b[0] - a[0]) / seg, (b[1] - a[1]) / seg
            angle = math.atan2(uy, ux)
            # 洗车台顺路：长度取 12 m 与接入段余量的较小值；小于 6 m 时标注专项确认。
            length = max(3200.0, min(12000.0, seg - 300.0))
            width = 5000.0
            center = (a[0] + ux * (length / 2.0 + 400.0),
                      a[1] + uy * (length / 2.0 + 400.0))
            pts = _oriented_rect(center, length, width, angle)
            rect = (min(p[0] for p in pts), min(p[1] for p in pts),
                    max(p[0] for p in pts), max(p[1] for p in pts))
            # 洗车台就在大门口跨接入道路，允许贴围挡/红线布置，但不允许出红线。
            if not all(self.boundary_index.contains(p) for p in pts):
                attempts.append("大门 {} 洗车台出红线".format(gate_index + 1))
                continue
            if _rect_rect_gap(rect, self.building_rect) < 500.0:
                attempts.append("大门 {} 洗车台距主体不足 0.5 m".format(gate_index + 1))
                continue
            if _hits_placed(rect, self.placed, 1000.0):
                attempts.append("大门 {} 洗车台与已放设施重叠".format(gate_index + 1))
                continue
            if geometry_blocked({"type": "area", "points_mm": pts, "closed": True},
                                self.context, "wheel_wash"):
                attempts.append("大门 {} 洗车台落在周边硬约束缓冲区".format(gate_index + 1))
                continue
            chosen = (gate_index, seg, length, width, pts, rect)
            break
        if chosen is None:
            raise GeneratorError(
                "所有大门接入段均无法布置洗车台：{}；请加大道路内缩或人工指定".format(
                    "；".join(attempts) if attempts else "无可用接入道路"))
        gate_index, seg, length, width, pts, rect = chosen
        self.gate_used = gate_index
        self.facilities.append(_make_area_poly(
            "A-WASH-01", "wheel_wash", "洗车台/沉淀池", pts, STAGE_ALL,
            {"scheme": self.profile["key"], "layout": "drive-through",
             "on_access_road": True, "drive_through_m": round(length / 1000.0, 1),
             "pad_width_m": round(width / 1000.0, 1),
             "short_pad": bool(length < 6000.0), "gate_index": gate_index + 1,
             "gate_count": len(gates),
             "main_gate_assumption": bool(len(gates) > 1),
             "assumption": "洗车台顺接入道路跨路布置，沉淀池与排水坡度需现场确认"
                           + ("；接入段较短，洗车台长度不足 6 m，需专项确认" if length < 6000.0 else "")
                           + ("；多门时按可布置的第一条重车接入道路选址（本次为第 {} 个大门），需现场确认".format(gate_index + 1) if len(gates) > 1 else "")}))
        self.placed.append({"category": "wheel_wash", "rect": rect, "gap_mm": 1000.0})
        return rect

    def place_weighbridge(self, gates: Sequence[Sequence[float]]) -> Tuple[float, float, float, float]:
        """地磅贴近出入口主环路布置：平台顺行车方向，落点写回距大门距离。"""
        if not gates or not self.gate_access or not self.ring:
            raise GeneratorError("无大门/环道，无法布置地磅")
        gate_index = min(self.gate_used, len(gates) - 1)
        gate = gates[gate_index]
        junction = self.gate_access[gate_index][1]
        seg, t, _q, _d = _project_on_closed_polyline(junction, self.ring)
        length = self.profile["sizes_m"]["weighbridge"][0] * 1000.0
        width = self.profile["sizes_m"]["weighbridge"][1] * 1000.0
        half = length / 2.0
        candidates: List[Tuple[float, Tuple[float, float], List[Tuple[float, float]], float]] = []
        for forward in (True, False):
            for dist_m in (half / 1000.0 + 3.0, half / 1000.0 + 6.0,
                           half / 1000.0 + 10.0, half / 1000.0 + 15.0,
                           half / 1000.0 + 21.0):
                point, direction = _walk_closed_polyline(
                    self.ring, seg, t, dist_m * 1000.0, forward)
                angle = math.atan2(direction[1], direction[0])
                pts = _oriented_rect(point, length, width, angle)
                # 平台必须整段落在同一条环道直段上，避免地磅跨转角
                p1, _ = _walk_closed_polyline(self.ring, seg, t,
                                              (dist_m * 1000.0 - half), forward)
                p2, _ = _walk_closed_polyline(self.ring, seg, t,
                                              (dist_m * 1000.0 + half), forward)
                if (_project_on_closed_polyline(p1, self.ring)[0] != seg
                        or _project_on_closed_polyline(p2, self.ring)[0] != seg):
                    continue
                rect = (min(p[0] for p in pts), min(p[1] for p in pts),
                        max(p[0] for p in pts), max(p[1] for p in pts))
                if not all(self.boundary_index.contains(p)
                           and self.boundary_index.distance(p) >= 1000.0 for p in pts):
                    continue
                if _rect_rect_gap(rect, self.building_rect) < 1500.0:
                    continue
                if _hits_placed(rect, self.placed, 1500.0):
                    continue
                if geometry_blocked({"type": "area", "points_mm": pts, "closed": True},
                                    self.context, "weighbridge"):
                    continue
                score = _dist(point, gate)
                candidates.append((score, point, pts, dist_m))
                break
        if not candidates:
            raise GeneratorError(
                "地磅无法贴近大门主环路布置；请检查环道宽度、主体退距或人工指定位置")
        _score, point, pts, dist_m = min(candidates, key=lambda item: item[0])
        rect = (min(p[0] for p in pts), min(p[1] for p in pts),
                max(p[0] for p in pts), max(p[1] for p in pts))
        self.facilities.append(_make_area_poly(
            "A-WEIGH-01", "weighbridge", "地磅", pts, STAGE_ALL,
            {"scheme": self.profile["key"], "layout": "on_main_road",
             "platform_m": [round(length / 1000.0, 1), 3.0],
             "footprint_m": [round(length / 1000.0, 1), round(width / 1000.0, 1)],
             "capacity_t": 100, "distance_to_gate_m": round(_dist(point, gate) / 1000.0, 1),
             "gate_index": gate_index + 1, "gate_count": len(gates),
             "main_gate_assumption": bool(len(gates) > 1),
             "assumption": "地磅按 100 t、3 m 宽平台占位；型号、基础、排水、检定与超限车绕行需专项确认"
                           + ("；地磅与洗车台同用第 {} 个大门，需现场确认主重车出入口".format(gate_index + 1) if len(gates) > 1 else "")}))
        self.placed.append({"category": "weighbridge", "rect": rect, "gap_mm": 1500.0})
        return rect

    def place_notice_board(self, gate_points: Sequence[Sequence[float]]) -> List[Tuple[float, float]]:
        """九牌一图沿大门侧围挡/红线直线排布 9 块，板面朝向场地内侧。

        优先贴围挡内侧的窄条带布置；若接入道路/洗车台占用门口，则沿围挡
        向两侧滑动，而不是把九块板缩成一个点或硬塞进道路。
        """
        if not gate_points:
            raise GeneratorError("无大门，无法定位九牌一图")
        gate = gate_points[0]
        # 红线在真实总图里常被拆成 3~5 m 的碎段，不能只拿“最近一段”当板长。
        # 先投影到大门所在红线，再沿折线累积走位，用局部切线方向放 11 m 直排板。
        seg, t, _proj, _proj_d = _project_on_closed_polyline(gate, self.boundary)
        # 板厚按 0.15 m 表达（9 块 1.2 m 宽板 + 0.2 m 端部余量，总长 11.0 m）。
        # 围挡内侧常只有 1 m 左右硬化带，九牌多为挂板/窄基础，不能按 0.3 m 厚占位。
        board_count = 9
        panel_width = 1200.0
        length = board_count * panel_width + 200.0
        depth = 150.0
        candidates: List[Tuple[float, List[Tuple[float, float]], float, float]] = []
        for forward in (True, False):
            # along_clear 是板端到大门中心的净距；接入道路/洗车台一般占据门口
            # 3~5 m，故从 3 m 开始逐级向外滑。
            for along_clear in (3000.0, 5000.0, 8000.0, 12000.0,
                                16000.0, 20000.0, 26000.0):
                run_center, direction = _walk_closed_polyline(
                    self.boundary, seg, t, along_clear + length / 2.0, forward)
                ux, uy = direction
                angle = math.atan2(uy, ux)
                for normal_sign in (1.0, -1.0):
                    nx, ny = -uy * normal_sign, ux * normal_sign
                    probe = (run_center[0] + nx * 800.0, run_center[1] + ny * 800.0)
                    if not self.boundary_index.contains(probe):
                        continue
                    for offset_mm in (300.0, 450.0, 650.0, 800.0, 1100.0, 1600.0):
                        center = (run_center[0] + nx * offset_mm,
                                  run_center[1] + ny * offset_mm)
                        if _dist(center, gate) > self.params["notice_to_gate_m"] * 1000.0:
                            continue
                        pts = _oriented_rect(center, length, depth, angle)
                        if not all(self.boundary_index.contains(p)
                                   and self.boundary_index.distance(p) >= 150.0 for p in pts):
                            continue
                        rect = (min(p[0] for p in pts), min(p[1] for p in pts),
                                max(p[0] for p in pts), max(p[1] for p in pts))
                        if _rect_rect_gap(rect, self.building_rect) < 800.0:
                            continue
                        if _hits_placed(rect, self.placed, 800.0):
                            continue
                        # 九牌允许贴道路边布置，只要求不压道路实体，不再额外留 0.6 m。
                        if _hits_road(rect, self.roads, 100.0):
                            continue
                        if geometry_blocked({"type": "area", "points_mm": pts, "closed": True},
                                            self.context, "notice_board"):
                            continue
                        score = _dist(center, gate) + 0.15 * offset_mm
                        candidates.append((score, pts, offset_mm, along_clear))
        if not candidates:
            raise GeneratorError(
                "九牌一图无法沿大门侧围挡直线排布；请检查大门位置、围挡长度或人工指定")
        _score, pts, offset_mm, along_clear = min(candidates, key=lambda item: item[0])
        center = (sum(p[0] for p in pts) / 4.0, sum(p[1] for p in pts) / 4.0)
        self.facilities.append(_make_area_poly(
            "A-NOTICE-01", "notice_board", "九牌一图", pts, STAGE_ALL,
            {"scheme": self.profile["key"], "layout": "linear",
             "board_count": board_count, "panel_width_m": 1.2, "panel_height_m": 2.4,
             "total_length_m": round(length / 1000.0, 1),
             "distance_to_gate_m": round(_dist(center, gate) / 1000.0, 1),
             "offset_from_fence_m": round(offset_mm / 1000.0, 2),
             "along_gate_m": round(along_clear / 1000.0, 1),
             "facing": "site_internal",
             "assumption": "九牌一图按 9 块 1.2 m 宽板直线排布；板面朝向大门/主路，需现场确认"}))
        self.placed.append({"category": "notice_board",
                            "rect": (min(p[0] for p in pts), min(p[1] for p in pts),
                                     max(p[0] for p in pts), max(p[1] for p in pts)),
                            "gap_mm": 800.0})
        return [(float(p[0]), float(p[1])) for p in pts]

    def _ring_polyline(self, extra_inset_mm: float = 0.0) -> List[Tuple[float, float]]:
        """环道中线：优先按真实红线内缩，失败才退回外接矩形内缩。"""
        inset = self.profile["inset_m"] * 1000.0 + extra_inset_mm
        if len(self.boundary) >= 3:
            ring = _inset_polygon(self.boundary, inset)
            if ring:
                self.ring_source = "redline-inset-cleaned"
                # 真实红线的小台阶不能原样当成道路硬折角；先删碎边，再交给
                # R3 校核。倒圆只用于外接矩形回退，避免短边倒圆反而产生小半径。
                return _trim_short_ring_edges(ring, self.boundary)
        x0, y0, x1, y1 = self.bbox
        self.ring_source = "bbox-inset"
        self.assumptions.append("红线内缩失败，环道按外接矩形内缩近似；非矩形场地必须人工复核环道是否落界。")
        return _fillet_closed([(x0 + inset, y0 + inset), (x1 - inset, y0 + inset),
                               (x1 - inset, y1 - inset), (x0 + inset, y1 - inset)], 12000.0)

    def add_roads(self, gate_points: List[Tuple[float, float]]) -> None:
        ring = self._ring_polyline()
        self.ring = list(ring)
        self.gate_access = []
        width = self.profile["road_width_m"]
        length_m = _poly_length(ring, closed=True) / 1000.0
        bays = []
        if self.profile["lanes"] == 1:
            station = 60.0
            while station < length_m - 10.0:
                bays.append({"station_m": round(station, 1)})
                station += 60.0
        ring_attrs = {"lanes": self.profile["lanes"], "passing_bays": bays,
                      "scheme": self.profile["key"]}
        self.roads.append(_make_line("A-ROAD-RING", "temporary_road", "环形临时主路",
                                     ring, STAGE_ALL, width, True, ring_attrs))
        fire_attrs = {"lanes": self.profile["lanes"], "passing_bays": bays,
                      "fire_lane": True, "shared_with": "A-ROAD-RING",
                      "scheme": self.profile["key"]}
        self.roads.append(_make_line("A-FIRE-RING", "fire_access", "环形消防车道",
                                     ring, STAGE_ALL, max(4.0, width), True, fire_attrs))

        for index, gate in enumerate(gate_points):
            nearest = _nearest_point_on_polyline(gate, ring)
            access = [gate, nearest]
            self.gate_access.append(access)
            attrs = {"lanes": self.profile["lanes"], "turnaround": True,
                     "turnaround_area_m": 225.0, "gate": index + 1}
            self.roads.append(_make_line(f"A-ROAD-GATE-{index + 1}", "temporary_road",
                                         f"大门 {index + 1} 连接道路", access,
                                         STAGE_ALL, width, False, attrs))

        # 周边既有道路：作为永久道路输入，便于校核永临结合
        for index, road in enumerate(self.context.get("existing_roads") or []):
            self.roads.append(_make_line(f"A-PERM-{index + 1:02d}", "permanent_road",
                                         road.get("name") or "既有/永久道路",
                                         road["geometry"]["points_mm"], STAGE_ALL,
                                         float(road.get("width_m") or 7.0), False,
                                         {"source": "site-context"}))

    def add_gates(self) -> List[Tuple[float, float]]:
        x0, y0, x1, y1 = self.bbox
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        gates: List[Tuple[float, float]] = []
        req_gates = self.requirements.get("gates")
        sides = self.profile["gates"]
        if isinstance(req_gates, list) and req_gates:
            sides = []
            for item in req_gates:
                if isinstance(item, dict):
                    if item.get("x_m") is not None and item.get("y_m") is not None:
                        gates.append((float(item["x_m"]) * 1000.0, float(item["y_m"]) * 1000.0))
                        continue
                    sides.append(str(item.get("side") or "S").upper())
                else:
                    sides.append(str(item).upper())
        offset = self.profile["gate_offset_m"] * 1000.0
        for index, side in enumerate(sides):
            side = str(side).upper()[:1]
            delta = offset * (1 if index % 2 == 0 else -1)
            if side == "S":
                target = (cx + delta, y0)
            elif side == "N":
                target = (cx - delta, y1)
            elif side == "W":
                target = (x0, cy + delta)
            elif side == "E":
                target = (x1, cy - delta)
            else:
                continue
            # 门必须落在围挡/红线上：把“某侧中点”投影到真实红线，
            # 避免斜置场地仍把门画在外接矩形边（红线外几十米）。
            gates.append(_nearest_on_boundary(target, self.boundary))
        # 去重并确保在边界附近
        unique: List[Tuple[float, float]] = []
        for gate in gates:
            if all(_dist(gate, item) > 3000.0 for item in unique):
                unique.append(gate)
        for index, gate in enumerate(unique):
            self.facilities.append(_make_point(f"A-GATE-{index + 1:02d}", "site_access",
                                               f"大门 {index + 1}", gate, STAGE_ALL,
                                               {"scheme": self.profile["key"]}))
        return unique

    def add_hoarding(self) -> None:
        pts = list(self.boundary) + [self.boundary[0]]
        self.facilities.append(_make_line("A-HOARD", "hoarding", "施工围挡", pts,
                                          STAGE_ALL, None, True, {"scheme": self.profile["key"]}))

    def add_power_and_water(self, gate_points: Sequence[Sequence[float]],
                            power_rect: Sequence[float], processing_rect: Optional[Sequence[float]]) -> None:
        pcx = (power_rect[0] + power_rect[2]) / 2
        pcy = (power_rect[1] + power_rect[3]) / 2
        box = self.place_point_near("primary_distribution_box", "一级配电箱", "A-BOX-01",
                                    STAGE_ALL, (pcx + 3000, pcy), 4.0, gate_points)
        # 临电干线：箱变 -> 加工区/塔吊/施工电梯
        targets = []
        if processing_rect:
            targets.append(((processing_rect[0] + processing_rect[2]) / 2,
                            (processing_rect[1] + processing_rect[3]) / 2))
        for crane in self.cranes:
            if crane.get("center_mm"):
                targets.append(tuple(crane["center_mm"]))
        for index, target in enumerate(targets):
            self.facilities.append(_make_line(f"A-POWER-{index + 1:02d}", "temporary_power",
                                              f"一级箱至用电点 {index + 1}", [box, target],
                                              STAGE_ALL, None, False,
                                              {"scheme": self.profile["key"]}))
        # 临时给水沿环道内侧，消防干管单独一根
        water = self._ring_polyline(1500.0)
        water = list(water) + [water[0]]
        self.facilities.append(_make_line("A-WATER-RING", "temporary_water", "临时给水环管",
                                          water, STAGE_ALL, None, True,
                                          {"scheme": self.profile["key"]}))
        self.facilities.append(_make_line("A-FIREWATER-RING", "fire_water", "临时消防干管",
                                          water, STAGE_ALL, None, True,
                                          {"scheme": self.profile["key"]}))

    def add_hydrants(self, gate_points: Sequence[Sequence[float]]) -> None:
        ring = next(row for row in self.roads if row["id"] == "A-ROAD-RING")
        points = ring["geometry"]["points_mm"]
        length = _poly_length(points, closed=True)
        # GB 50720：消火栓间距不应大于 120 m；按 110 m 目标排布留 10 m 余量，
        # 大场地必须加密，不能沿用方案画像里的固定个数。
        target_mm = 110_000.0
        count = max(int(self.profile["hydrants"]), int(math.ceil(length / target_mm)))
        spacing = length / 1000.0 / count
        for i in range(count):
            station = length * (i + 0.5) / count
            p = _point_at(points, station, closed=True)
            if len(self.boundary) >= 3 and not _point_in_polygon(p, self.boundary):
                p = _nearest_point_on_polyline(p, [tuple(q) for q in self.boundary] +
                                               [tuple(self.boundary[0])])
            self.facilities.append(_make_point(f"A-HYD-{i + 1:02d}", "fire_hydrant",
                                               f"消火栓 {i + 1}", p, STAGE_ALL,
                                               {"scheme": self.profile["key"],
                                                "spacing_target_m": round(spacing, 1),
                                                "max_spacing_m": 120.0}))

    def add_crane(self) -> List[Dict[str, Any]]:
        if self.cranes:
            return list(self.cranes)
        bx0, by0, bx1, by1 = self.building_rect
        cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
        half_diag_m = math.hypot(bx1 - bx0, by1 - by0) / 2.0 / 1000.0
        jib_m = max(25.0, half_diag_m + 3.0)
        crane = {
            "id": "TC-01", "model": "自动布置草案（未选型）",
            "center_mm": [cx, cy], "jib_mm": jib_m * 1000.0,
            "rotation_deg": 0.0, "source": "auto-layout",
            # 塔吊随主体结构安装、主体封顶后拆除；土石方与装饰阶段不应默认出现
            "active_stages": ["structure"],
        }
        self.cranes = [crane]
        self.assumptions.append("未提供塔吊识图/选型，按建筑外接圆半径+3m 假定一台塔吊，仅用于检查覆盖与临建避让；必须做选型、基础、附着和群塔验算。")
        return [crane]

    def build(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
        self.building_rect, self.building_source = _building_from(
            self.base_map, self.requirements, self.bbox, self.assumptions
        )
        if self.building_source == "assumed" and not self.allow_assumed_building:
            raise GeneratorError(
                "底图与需求都没有主体建筑轮廓，自动布置会按场地中部 42%×32% 的假定矩形出 A/B/C，"
                "塔吊覆盖、施工电梯贴边、道路避让都会跟着错。请任选其一后再跑：\n"
                "  1) 让 reader 契约带上建筑外轮廓层（cad_site_geometry 的 site_geometry 出现 building 类图层）；\n"
                "  2) prepare_site.py 加 --building-layer \"0-建筑-屋顶-外轮廓\" 指定图层；\n"
                "  3) requirements 里写 building.footprint（含 coord_unit）；\n"
                "  4) 只想看功能草案时显式加 --allow-assumed-building，输出会标 building_source=assumed。"
            )
        self.building_poly = _rect_polygon(self.building_rect)
        gates = self.add_gates()
        self.add_roads(gates)
        self.add_hoarding()
        cranes = self.add_crane()
        # 施工电梯与主体关系最刚性，先占靠主体南/东侧的合法带；
        # 否则后期生活区/宣讲台等设施可能把贴边位置全部挤掉。
        self.place_elevator()

        # 出入口服务带先落位：洗车台跨接入道路、地磅贴主环路靠大门；
        # 后续设施看到它们后会自动避让，避免“洗车台放到路边空地上”。
        self.place_wheel_wash(gates)
        self.place_weighbridge(gates)

        # 加工区/堆场放在塔吊覆盖内、靠近大门；生活办公放上风向并避开回转半径
        # 0.6.0 加工区拆分：钢筋只进主体；木工/砂浆进主体+装饰；通用 processing_zone 不再生成
        proc = self.place_area("steel_processing", "钢筋加工区", "A-STEEL-01",
                               STAGE_STRUCT_ONLY, gate_points=gates)
        self.place_area("wood_processing", "木工加工区", "A-WOOD-01", STAGE_STRUCT,
                        gate_points=gates)
        self.place_area("mortar_processing", "砂浆/砌体加工区", "A-MORTAR-01", STAGE_STRUCT,
                        gate_points=gates)
        self.place_area("material_yard", "材料堆场", "A-MAT-01", STAGE_STRUCT,
                        gate_points=gates)
        # 办公/宿舍/临建先落位：变压器必须按 10m 安全距离避让人员区，
        # 若先放变压器再放生活设施，安全距离只能事后报警而不能自动避让。
        self.place_area("site_office", "办公区", "A-OFFICE-01", STAGE_ALL, gate_points=gates)
        living = self.place_area(
            "worker_living_zone", "工人生活区", "A-LIVING-01", STAGE_ALL,
            gate_points=gates,
            attrs_extra={"evacuation_exits": 2,
                         "evacuation_note": "候选证据：按不少于 2 个疏散口示意，待消防疏散专项确认"},
            note="生活区包络仅作候选，待风玫瑰、人数、床位数与消防疏散专项确认")
        # 三块整体搜索：食堂/卫生间/晾晒的尺寸组合一起比选，避免贪心先占大块。
        self.place_living_children(
            living, "A-LIVING-01", (
                {"category": "canteen", "name": "生活区食堂", "fid": "A-CANTEEN-01",
                 "preferred": (0.72, 0.76)},
                {"category": "toilet_shower", "name": "生活区卫生间/淋浴间", "fid": "A-TOILET-01",
                 "preferred": (0.22, 0.22)},
                {"category": "drying_area", "name": "生活区晾晒区", "fid": "A-DRYING-01",
                 "preferred": (0.78, 0.20)},
            ), STAGE_ALL)
        self.place_area(
            "staff_dormitory", "员工宿舍区", "A-STAFFDORM-01", STAGE_ALL,
            gate_points=gates,
            attrs_extra={"evacuation_exits": 2,
                         "evacuation_note": "候选证据：按不少于 2 个疏散口示意，待消防疏散专项确认"},
            note="候选证据，待消防疏散专项确认")
        power = self.place_area("distribution_room", "配电室", "A-PWR-01", STAGE_ALL,
                                gate_points=gates)
        # 0.6.0 新增：变压器靠近配电室；消防泵房/水池成组并靠近消防车道
        x0, y0, x1, y1 = self.bbox
        pcx = (power[0] + power[2]) / 2
        pcy = (power[1] + power[3]) / 2
        self.place_area("transformer", "变压器/箱变", "A-TRANS-01", STAGE_ALL,
                        preferred=((pcx - x0) / max(1.0, x1 - x0) + 0.06,
                                   (pcy - y0) / max(1.0, y1 - y0) + 0.06),
                        gate_points=gates)
        tank = self.place_area("fire_water_tank", "消防水池", "A-FIRETANK-01", STAGE_ALL,
                               gate_points=gates)
        tcx = (tank[0] + tank[2]) / 2
        tcy = (tank[1] + tank[3]) / 2
        self.place_area("fire_pump_room", "消防泵房", "A-FIREPUMP-01", STAGE_ALL,
                        preferred=((tcx - x0) / max(1.0, x1 - x0) + 0.04,
                                   (tcy - y0) / max(1.0, y1 - y0) + 0.04),
                        gate_points=gates)
        self.place_area("parking", "停车场", "A-PARK-01", STAGE_ALL, gate_points=gates)
        self.place_area("safety_podium", "安全宣讲台", "A-PODIUM-01", STAGE_ALL,
                        gate_points=gates)
        self.place_area("waste_pool", "垃圾池", "A-WASTE-01", STAGE_ALL,
                        gate_points=gates)
        # 九牌一图：长条区域，靠近主大门，走与区域设施同样的硬约束检查
        self.place_notice_board(gates)

        self.add_power_and_water(gates, power, proc)
        self.add_hydrants(gates)
        self.add_drainage()

        # 指标
        area_m2 = abs(sum(self.boundary[i][0] * self.boundary[(i + 1) % len(self.boundary)][1]
                          - self.boundary[(i + 1) % len(self.boundary)][0] * self.boundary[i][1]
                          for i in range(len(self.boundary)))) / 2.0 / 1e6
        road_stats = _unique_road_length_m(self.facilities + self.roads)
        road_len = road_stats["total"]
        facility_area = 0.0
        for row in self.facilities:
            if row["geometry"]["type"] == "area":
                pts = row["geometry"]["points_mm"]
                facility_area += abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1]
                                         - pts[(i + 1) % len(pts)][0] * pts[i][1]
                                         for i in range(len(pts)))) / 2.0 / 1e6
        self.metrics = {
            "site_area_m2": round(area_m2, 1),
            "road_length_m": round(road_len, 1),
            "road_length_by_category_m": road_stats["by_category"],
            "facility_area_m2": round(facility_area, 1),
            "facility_area_ratio": round(facility_area / area_m2, 3) if area_m2 else None,
            "gates": len(gates),
            "hydrants": len([r for r in self.facilities if r["category"] == "fire_hydrant"]),
            "road_width_m": self.profile["road_width_m"],
            "lanes": self.profile["lanes"],
        }
        return self.facilities + self.roads, cranes, {
            "scheme": self.profile["key"], "profile": self.profile,
            "assumptions": self.assumptions, "metrics": self.metrics,
            "building_rect_mm": [round(v, 1) for v in self.building_rect],
            "building_source": self.building_source,
        }

    def add_drainage(self) -> None:
        """环沟沿临时道路内侧闭合；加一段洗车池/沉淀池排水接入（全阶段保留）。"""
        ring = self._ring_polyline(-1500.0)
        ring = list(ring) + [ring[0]]
        self.facilities.append(_make_line(
            "A-DITCH-01", "drainage_ditch", "排水沟（环沟）", ring, STAGE_ALL, None, True,
            {"scheme": self.profile["key"], "assumption": "沿道路内侧环沟，坡度与排放口需现场确认"}))
        wash = next((row for row in self.facilities if row["category"] == "wheel_wash"), None)
        if wash:
            pts = wash["geometry"]["points_mm"]
            wc = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
            nearest = _nearest_point_on_polyline(wc, ring)
            self.facilities.append(_make_line(
                "A-DITCH-02", "drainage_ditch", "洗车池排水接入", [wc, nearest], STAGE_ALL,
                None, False, {"scheme": self.profile["key"], "discharge": "wheel_wash"}))

    def place_elevator(self) -> None:
        bx0, by0, bx1, by1 = self.building_rect
        candidates = [
            (bx0 + (bx1 - bx0) * 0.25 - 3000, by0 - 4500, bx0 + (bx1 - bx0) * 0.25 + 3000, by0 - 500),
            (bx1 + 500, by0 + (by1 - by0) * 0.3 - 2500, bx1 + 6000, by0 + (by1 - by0) * 0.3 + 2500),
            (bx0 - 6000, by0 + (by1 - by0) * 0.3 - 2500, bx0 - 500, by0 + (by1 - by0) * 0.3 + 2500),
            (bx0 + (bx1 - bx0) * 0.75 - 3000, by1 + 500, bx0 + (bx1 - bx0) * 0.75 + 3000, by1 + 4500),
        ]
        for rect in candidates:
            if self.boundary_index.inside_rect(rect, self.profile["margin_m"] * 1000.0) \
                    and not _hits_road(rect, self.roads, 1000.0) \
                    and not _hits_placed(rect, self.placed, 500.0) \
                    and not geometry_blocked({"type": "area", "points_mm": _rect_polygon(rect), "closed": True},
                                             self.context, "construction_elevator"):
                self.facilities.append(_make_area("A-LIFT-01", "construction_elevator",
                                                  "施工电梯", rect, STAGE_STRUCT,
                                                  {"scheme": self.profile["key"]}))
                self.placed.append({"category": "construction_elevator", "rect": rect, "gap_mm": 500.0})
                return
        raise GeneratorError("施工电梯无法贴靠主体布置；请检查道路与建筑轮廓")


def generate_layout(base_map: Dict[str, Any], context: Dict[str, Any],
                    requirements: Dict[str, Any], cranes: Sequence[Dict[str, Any]],
                    scheme: str, allow_assumed_building: bool = False) -> Dict[str, Any]:
    if scheme not in PROFILES:
        raise GeneratorError(f"未知方案 {scheme!r}；只接受 {list(PROFILES)}")
    profile = PROFILES[scheme]
    layout = _Layout(base_map, context, requirements, cranes, profile,
                     allow_assumed_building=allow_assumed_building)
    facilities, generated_cranes, meta_info = layout.build()
    return {
        "schema": SCHEMA,
        "project": str(requirements.get("project") or base_map.get("project") or ""),
        "coord_unit": "mm",
        "scheme": scheme,
        "scheme_name": profile["name"],
        "facilities": facilities,
        "cranes": generated_cranes,
        "assumptions": meta_info["assumptions"],
        "metrics": meta_info["metrics"],
        "profile": profile,
        "building_rect_mm": meta_info["building_rect_mm"],
        "building_source": meta_info.get("building_source") or "",
        "source": {
            "base_map": base_map.get("source_file") or "",
            "base_map_sha256": base_map.get("source_sha256") or "",
            "context": context.get("source_path") or "",
            "requirements": requirements.get("_path") or "",
            "requirements_sha256": requirements.get("_sha256") or "",
        },
        "final_check": False,
        "boundary": "自动布置候选；设施位置为候选（candidate），不是确认位置，不替代审批。",
    }


def render_generated_markdown(result: Dict[str, Any]) -> str:
    lines = ["# 自动布置候选：{}".format(result["scheme_name"]), "",
             "> 所有设施为 candidate；必须经项目技术负责人逐项确认。", "",
             "## 指标", ""]
    for key, value in result["metrics"].items():
        lines.append("- {}：{}".format(key, value))
    lines += ["", "## 假设与边界", ""]
    for item in result["assumptions"]:
        lines.append("- {}".format(item))
    lines += ["", "## 设施清单", "", "| ID | 类别 | 名称 | 阶段 |", "|---|---|---|---|"]
    for row in result["facilities"]:
        lines.append("| {} | {} | {} | {} |".format(
            row["id"], row["category_name"], row["name"], ",".join(row["active_stages"])))
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 方案评分与比选（v0.5）
#
# 分数是“内部比选参考分”，不是评标分、报价或安全评级。
# 硬约束 fail 一票否决；分数只在没有硬伤或需要说明代价时使用。
# ---------------------------------------------------------------------------

DIMENSIONS: List[Tuple[str, str]] = [
    ("cost", "成本"), ("constructability", "可施工性"), ("safety", "安全"),
    ("fire", "消防"), ("traffic", "交通"), ("environment", "环保"),
    ("schedule", "工期"), ("reviewability", "可审查性"),
]

# 与 review_panel.ROLES 保持一致；这里只用于算分，不重复出意见。
_ROLE_CHECKS: Dict[str, List[str]] = {
    "chief": ["1", "2", "4", "11", "13", "14", "R1", "R2", "R3", "R4"],
    "safety": ["6", "7", "14", "R2", "R3"],
    "fire": ["3", "4", "5", "15", "R1", "R3", "R4"],
    "civil": ["8", "9", "10", "R1"],
}


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, value))


def _index(checks: Sequence[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {str(item.get("id")): item for item in checks}


def _check_score(index: Dict[str, Dict[str, Any]], ids: Sequence[str],
                 fail_penalty: float = 45.0, manual_penalty: float = 12.0) -> Tuple[float, Dict[str, Any]]:
    present = [index[cid] for cid in ids if cid in index]
    fails = [item for item in present if item.get("status") == "fail"]
    manual = [item for item in present if item.get("status") == "manual"]
    score = _clamp(100.0 - fail_penalty * len(fails) - manual_penalty * len(manual))
    return score, {"checks": len(present), "fail": len(fails), "manual": len(manual),
                   "failed_names": [item.get("name") for item in fails],
                   "manual_names": [item.get("name") for item in manual]}


_STATUS_RANK = {"pass": 0, "manual": 1, "fail": 2}


def _stage_map(value: Any) -> Dict[str, Dict[str, Any]]:
    """兼容单阶段对象和 {stage: 校核结果} 两种输入。"""
    if not isinstance(value, dict):
        return {}
    if "checks" in value or "summary" in value:
        return {"_": value}
    return {str(k): v for k, v in value.items() if isinstance(v, dict)}


def _merge_checks(groups: Sequence[Tuple[str, Sequence[Dict[str, Any]]]]) -> List[Dict[str, Any]]:
    """按检查 id 合并多阶段结果，取最不利状态（fail > manual > pass）。"""
    merged: Dict[str, Dict[str, Any]] = {}
    for stage, checks in groups:
        for check in checks or []:
            cid = str(check.get("id"))
            item = dict(check)
            item["stage"] = stage
            item["stages"] = [stage]
            prev = merged.get(cid)
            if prev is None:
                merged[cid] = item
                continue
            prev["stages"].append(stage)
            if _STATUS_RANK.get(item.get("status"), 0) > _STATUS_RANK.get(prev.get("status"), 0):
                keep_stages = prev["stages"]
                item["stages"] = keep_stages
                merged[cid] = item
    return list(merged.values())


def evaluate_scheme(result: Dict[str, Any],
                    models: Any,
                    roads: Any,
                    contexts: Any = None,
                    stages: Optional[Sequence[str]] = None) -> Dict[str, Any]:
    """按 8 个维度给一套候选打分，汇总全部阶段的硬伤与待办。

    输入 models/roads/contexts 可以是单阶段结果，也可以是 {stage: 结果}；
    三阶段时按“任一阶段 fail 即硬伤、人工项取并集、分数取最不利”处理。
    """
    model_map = _stage_map(models)
    road_map = _stage_map(roads)
    context_map = _stage_map(contexts) if contexts is not None else {}
    stage_names = list(stages or model_map.keys())
    stage_keys = [key for key in stage_names if key in model_map]
    if not stage_keys:
        stage_keys = list(model_map.keys())

    groups: List[Tuple[str, Sequence[Dict[str, Any]]]] = []
    for stage in stage_keys:
        label = STAGE_NAMES.get(stage, stage) if stage != "_" else ""
        model = model_map.get(stage) or {}
        road = road_map.get(stage) or {}
        ctx = context_map.get(stage) or {}
        for source, checks in (("规则", model.get("checks") or []),
                               ("道路", road.get("checks") or []),
                               ("周边", ctx.get("checks") or [])):
            tagged = []
            for check in checks:
                item = dict(check)
                item["name"] = "{}{}".format(source, item.get("name") or item.get("id"))
                tagged.append(item)
            groups.append((stage, tagged))
    merged = _merge_checks(groups)
    index = {str(item.get("id")): item for item in merged}

    metrics = result.get("metrics") or {}
    assumptions = list(result.get("assumptions") or [])
    profile = result.get("profile") or {}
    weights = profile.get("weights") or {key: 1.0 / len(DIMENSIONS) for key, _ in DIMENSIONS}

    width = float(metrics.get("road_width_m") or 4.0)
    length = float(metrics.get("road_length_m") or 0.0)
    ratio = float(metrics.get("facility_area_ratio") or 0.0) * 100.0
    gates = int(metrics.get("gates") or 1)
    hydrants = int(metrics.get("hydrants") or 0)
    area = float(metrics.get("site_area_m2") or 0.0)
    # 用场地等效周长做道路长度基准，避免大场地被固定 160 m 阈值一刀切
    perimeter_ref = 4.0 * math.sqrt(area) if area > 0 else 320.0
    cost = _clamp(100.0
                  - max(0.0, width - 3.5) * 9.0
                  - max(0.0, length - perimeter_ref) * 0.06
                  - max(0.0, ratio - 10.0) * 1.6
                  - max(0, gates - 1) * 4.0)

    construct, construct_detail = _check_score(index, ["1", "2", "4", "13"],
                                               fail_penalty=35.0, manual_penalty=8.0)
    construct = _clamp(construct - 5.0 * len(assumptions))

    safety, safety_detail = _check_score(index, _ROLE_CHECKS["safety"])
    fire, fire_detail = _check_score(index, _ROLE_CHECKS["fire"])
    env, env_detail = _check_score(index, _ROLE_CHECKS["civil"])
    traffic, traffic_detail = _check_score(index, ["R1", "R2", "R3", "R4", "3"])
    if not (model_map.get(stage_keys[0]) or {}).get("counts", {}).get("by_category", {}).get(
            "temporary_road"):
        traffic = _clamp(traffic - 12.0)

    all_checks = list(index.values())
    fails = [item for item in all_checks if item.get("status") == "fail"]
    manuals = [item for item in all_checks if item.get("status") == "manual"]
    schedule = _clamp(100.0 - max(0.0, width - 3.5) * 10.0
                      - max(0, gates - 1) * 3.0
                      - 8.0 * len(fails) - 3.0 * len(manuals))
    reviewability = _clamp(100.0 - 6.0 * len(assumptions)
                           - 4.0 * len(manuals) - 10.0 * len(fails))

    scores = {"cost": round(cost, 1), "constructability": round(construct, 1),
              "safety": round(safety, 1), "fire": round(fire, 1),
              "traffic": round(traffic, 1), "environment": round(env, 1),
              "schedule": round(schedule, 1), "reviewability": round(reviewability, 1)}
    total = sum(scores[key] * float(weights.get(key, 0.0)) for key, _ in DIMENSIONS)

    hard: List[str] = []
    stage_summary: Dict[str, Dict[str, Any]] = {}
    for stage in stage_keys:
        label = STAGE_NAMES.get(stage, stage) if stage != "_" else ""
        model = model_map.get(stage) or {}
        road = road_map.get(stage) or {}
        ctx = context_map.get(stage) or {}
        stage_summary[stage] = {
            "rules_fail": int((model.get("summary") or {}).get("fail") or 0),
            "rules_manual": int((model.get("summary") or {}).get("manual") or 0),
            "road_fail": int((road.get("summary") or {}).get("fail") or 0),
            "road_manual": int((road.get("summary") or {}).get("manual") or 0),
            "context_fail": int((ctx.get("summary") or {}).get("fail") or 0),
        }
        prefix = label + "：" if label else ""
        model_fail = [item for item in model.get("checks") or [] if item.get("status") == "fail"]
        if model_fail:
            hard.append(prefix + "规则校核 fail：{}".format("、".join(
                str(item.get("name") or item.get("id")) for item in model_fail)))
        road_fail = [item for item in road.get("checks") or [] if item.get("status") == "fail"]
        if road_fail:
            hard.append(prefix + "道路校核 fail：{}".format("、".join(
                str(item.get("name") or item.get("id")) for item in road_fail)))
        ctx_fail = [item for item in ctx.get("checks") or [] if item.get("status") == "fail"]
        if ctx_fail:
            hard.append(prefix + "周边硬约束 fail：{}".format("、".join(
                str(item.get("name") or item.get("id")) for item in ctx_fail)))

    manual_actions = []
    for item in manuals:
        action = str(item.get("action") or "").strip()
        name = str(item.get("name") or item.get("id"))
        stage_tag = ""
        if stage_keys and stage_keys[0] != "_":
            span = [STAGE_NAMES.get(st, st) for st in item.get("stages") or []]
            stage_tag = "（{}）".format("、".join(span)) if span else ""
        manual_actions.append("{}{}{}".format(name, stage_tag,
                                             "：" + action if action else ""))
    for stage in stage_keys:
        ctx = context_map.get(stage) or {}
        if (ctx.get("summary") or {}).get("review"):
            label = STAGE_NAMES.get(stage, stage) if stage != "_" else ""
            manual_actions.append("{}周边软约束 review，需专项评估".format(
                label + "：" if label else ""))

    if hard:
        verdict = "不推荐（存在硬伤）"
    elif manual_actions:
        verdict = "可讨论（需补人工确认项）"
    else:
        verdict = "可推荐为基线"

    detail = {"constructability": construct_detail, "safety": safety_detail,
              "fire": fire_detail, "environment": env_detail, "traffic": traffic_detail}
    return {
        "scheme": result.get("scheme"),
        "scheme_name": result.get("scheme_name"),
        "tag": (result.get("profile") or {}).get("tag", ""),
        "scores": scores,
        "weights": {key: float(weights.get(key, 0.0)) for key, _ in DIMENSIONS},
        "total": round(total, 1),
        "verdict": verdict,
        "hard_finds": hard,
        "manual_actions": manual_actions[:12],
        "manual_total": len(manual_actions),
        "metrics": metrics,
        "assumptions": assumptions,
        "detail": detail,
        "hydrants": hydrants,
        "evaluated_stages": stage_keys if stage_keys != ["_"] else [],
        "stage_summary": stage_summary,
        "final_check": False,
        "boundary": "评分为内部比选参考，不是评标分、报价或安全评级；硬约束以规则/周边/道路校核为准。",
    }


def compare_schemes(evaluations: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """汇总多方案：排序、推荐、适用条件。"""
    rows = sorted(evaluations, key=lambda item: item["total"], reverse=True)
    usable = [item for item in rows if not item["hard_finds"]]
    recommended = None
    if usable:
        best = usable[0]
        # 5 分以内优先均衡型，避免为了小数点牺牲可实施性
        for item in usable:
            if item["scheme"] == "balanced" and best["total"] - item["total"] <= 5.0:
                best = item
        recommended = {"scheme": best["scheme"], "scheme_name": best["scheme_name"],
                       "total": best["total"], "reason": ""}
        reasons = []
        if best["scheme"] == "balanced":
            reasons.append("综合分靠前且安全/成本折中")
        else:
            reasons.append("综合分最高")
        if best["hard_finds"]:
            reasons.append("但仍有硬伤，需先解决")
        elif best["manual_actions"]:
            reasons.append("需补齐 {} 项人工确认".format(len(best["manual_actions"])))
        recommended["reason"] = "；".join(reasons)
    return {
        "schema": "site-scheme-comparison/v1",
        "generated_at": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds"),
        "rows": rows,
        "recommended": recommended,
        "usable": len(usable),
        "final_check": False,
        "boundary": "方案比选是内部决策参考；推荐不等于审批通过，硬约束必须先闭环。",
    }


def render_comparison_markdown(comparison: Dict[str, Any]) -> str:
    lines = ["# 平面布置方案比选", "",
             "> 分数为内部参考分（0-100），不是评标分、报价或安全评级；硬约束 fail 一票否决。", ""]
    header = "| 方案 | 结论 | 综合 | " + " | ".join(name for _key, name in DIMENSIONS) + " |"
    lines += [header, "|" + "---|" * (3 + len(DIMENSIONS))]
    for row in comparison["rows"]:
        scores = row["scores"]
        lines.append("| {} | {} | {} | {} |".format(
            row["scheme_name"], row["verdict"], row["total"],
            " | ".join(str(scores[key]) for key, _name in DIMENSIONS)))
    lines.append("")
    if comparison.get("recommended"):
        rec = comparison["recommended"]
        lines += ["## 推荐", "",
                  "**{}（{}）**：{}".format(rec["scheme_name"], rec["total"], rec["reason"]), ""]
    else:
        lines += ["## 推荐", "", "三套方案均有硬伤，暂不推荐；先解决硬约束再比选。", ""]
    for row in comparison["rows"]:
        lines += ["## {}".format(row["scheme_name"]), "",
                  "- 定位：{}".format(row.get("tag") or "—"),
                  "- 结论：{}".format(row["verdict"]),
                  "- 指标：道路 {road_width_m} m × {road_length_m} m，临建占地 {facility_area_ratio}，"
                  "大门 {gates} 个，消火栓 {hydrants} 个".format(**row["metrics"]),
                  ""]
        if row["hard_finds"]:
            lines.append("- 硬伤：")
            lines += ["  - {}".format(item) for item in row["hard_finds"]]
        if row["manual_actions"]:
            lines.append("- 待人工：")
            lines += ["  - {}".format(item) for item in row["manual_actions"]]
        if not row["hard_finds"] and not row["manual_actions"]:
            lines.append("- 无硬伤、无待人工项（仍需项目确认与审批）")
        lines.append("")
    lines += ["## 边界", "", comparison["boundary"], ""]
    return "\n".join(lines)
