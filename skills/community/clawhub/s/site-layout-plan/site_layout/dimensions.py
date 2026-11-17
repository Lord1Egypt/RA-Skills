"""关键尺寸标注与角点坐标表（纯几何，无 I/O）。

S2 出图内核的三类派生数据：
1. 关键尺寸：设施净距、道路宽度、消防车道宽度、塔吊回转半径、施工电梯距结构边。
2. 坐标表：红线角点 + 主要设施定位点，输出 CSV 与图内表格。
3. 指北针/比例尺的元数据（实际绘制在 stage_draw）。

本模块只做候选与证据，不判合规；任何一项几何不足都返回 skipped 原因，
由自检降级为 manual，绝不静默省略。
"""
from __future__ import annotations

import math
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

Point = Tuple[float, float]

KIND_NAMES: Dict[str, str] = {
    "facility_clearance": "设施间净距",
    "road_width": "道路宽度",
    "fire_lane_width": "消防车道宽度",
    "crane_radius": "塔吊回转半径",
    "elevator_offset": "施工电梯距结构边",
}
KIND_ORDER: Tuple[str, ...] = (
    "facility_clearance", "road_width", "fire_lane_width",
    "crane_radius", "elevator_offset",
)

# 设施净距的优先配对：生活/办公/加工/堆场/临建之间最需要交代的净距。
CLEARANCE_PAIRS: Tuple[Tuple[str, str], ...] = (
    # 0.7.0 生活区优先配对：先标生活区与加工区/堆场、宿舍与配套、
    # 办公区与大门；旧临时宿舍/临建配对保留在表末兼容历史数据。
    ("worker_living_zone", "steel_processing"),
    ("worker_living_zone", "wood_processing"),
    ("worker_living_zone", "mortar_processing"),
    ("worker_living_zone", "processing_zone"),
    ("worker_living_zone", "material_yard"),
    ("staff_dormitory", "canteen"),
    ("staff_dormitory", "toilet_shower"),
    ("site_office", "site_access"),
    ("staff_dormitory", "worker_living_zone"),
    ("temporary_dormitory", "site_office"),
    ("temporary_dormitory", "steel_processing"),
    ("temporary_dormitory", "wood_processing"),
    ("temporary_dormitory", "mortar_processing"),
    # processing_zone 为 0.5/旧数据通用类；仍保留，避免 S2 五类标注回归
    ("temporary_dormitory", "processing_zone"),
    ("temporary_dormitory", "material_yard"),
    ("site_office", "steel_processing"),
    ("site_office", "wood_processing"),
    ("site_office", "mortar_processing"),
    ("site_office", "processing_zone"),
    ("site_office", "material_yard"),
    ("temporary_building", "steel_processing"),
    ("temporary_building", "wood_processing"),
    ("temporary_building", "mortar_processing"),
    ("temporary_building", "processing_zone"),
    ("temporary_dormitory", "waste_pool"),
    ("site_office", "waste_pool"),
)
MAX_CLEARANCE_DIMS = 4
MIN_CLEARANCE_MM = 100.0
# 只标“场地内真正有参考价值”的近邻净距；300m 级的长线会横穿整张图，
# 既不可读也不代表规范控制距离，超过阈值直接不生成标注。
MAX_CLEARANCE_MM = 60_000.0

ROAD_CATEGORY_KIND: Dict[str, str] = {
    "temporary_road": "road_width",
    "permanent_road": "road_width",
    "fire_access": "fire_lane_width",
}
ROAD_LABEL: Dict[str, str] = {
    "temporary_road": "临时道路",
    "permanent_road": "永久道路",
    "fire_access": "消防车道",
}

COORD_FACILITY_CATEGORIES: Tuple[str, ...] = (
    "site_access",
    "primary_distribution_box",
    "fire_hydrant",
    "construction_elevator",
    "processing_zone",
    "steel_processing",
    "wood_processing",
    "mortar_processing",
    "material_yard",
    "temporary_dormitory",
    "site_office",
    "staff_dormitory",
    "worker_living_zone",
    "canteen",
    "toilet_shower",
    "drying_area",
    "distribution_room",
    "transformer",
    "fire_pump_room",
    "fire_water_tank",
    "notice_board",
    "wheel_wash",
    "weighbridge",
)
COORD_TYPE_NAMES: Dict[str, str] = {
    "tower_crane": "塔吊中心",
    "primary_distribution_box": "一级配电箱",
    "fire_hydrant": "消火栓",
    "construction_elevator": "施工电梯",
    "site_access": "大门/出入口",
    "processing_zone": "加工区",
    "steel_processing": "钢筋加工区",
    "wood_processing": "木工加工区",
    "mortar_processing": "砂浆加工区",
    "material_yard": "材料堆场",
    "transformer": "变压器",
    "fire_pump_room": "消防泵房",
    "fire_water_tank": "消防水池",
    "temporary_dormitory": "临时宿舍",
    "site_office": "办公区",
    "staff_dormitory": "员工宿舍区",
    "worker_living_zone": "工人生活区",
    "canteen": "食堂",
    "toilet_shower": "卫生间/淋浴间",
    "drying_area": "晾晒区",
    "distribution_room": "配电室",
    "notice_board": "九牌一图",
    "wheel_wash": "洗车台",
    "weighbridge": "地磅",
}


# ---------- 基础几何 ----------

def _dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.hypot(float(a[0]) - float(b[0]), float(a[1]) - float(b[1]))


def _unit(a: Sequence[float], b: Sequence[float]) -> Optional[Point]:
    dx = float(b[0]) - float(a[0])
    dy = float(b[1]) - float(a[1])
    length = math.hypot(dx, dy)
    if length <= 1e-9:
        return None
    return dx / length, dy / length


def _closest_on_segment(p: Sequence[float], a: Sequence[float],
                        b: Sequence[float]) -> Tuple[float, Point]:
    ax, ay = float(a[0]), float(a[1])
    bx, by = float(b[0]), float(b[1])
    px, py = float(p[0]), float(p[1])
    dx, dy = bx - ax, by - ay
    denom = dx * dx + dy * dy
    if denom <= 1e-12:
        point = (ax, ay)
        return _dist(p, point), point
    t = ((px - ax) * dx + (py - ay) * dy) / denom
    t = max(0.0, min(1.0, t))
    point = (ax + t * dx, ay + t * dy)
    return _dist(p, point), point


def _ring(points: Sequence[Sequence[float]]) -> List[Point]:
    pts = [(float(p[0]), float(p[1])) for p in points]
    if len(pts) >= 2 and _dist(pts[0], pts[-1]) <= 1e-6:
        pts = pts[:-1]
    return pts


def _edges(points: Sequence[Sequence[float]]) -> Iterable[Tuple[Point, Point]]:
    pts = _ring(points)
    for index in range(len(pts)):
        yield pts[index], pts[(index + 1) % len(pts)] if len(pts) > 1 else pts[index]


def _polyline_edges(points: Sequence[Sequence[float]]) -> Iterable[Tuple[Point, Point]]:
    pts = [(float(p[0]), float(p[1])) for p in points]
    for index in range(len(pts) - 1):
        yield pts[index], pts[index + 1]


def _segment_distance(a1: Point, a2: Point, b1: Point,
                      b2: Point) -> Tuple[float, Point, Point]:
    """两线段最小距离；返回距离与分别落在两线段上的最近点。"""
    best: Optional[Tuple[float, Point, Point]] = None
    for point, start, end in ((a1, b1, b2), (a2, b1, b2),
                              (b1, a1, a2), (b2, a1, a2)):
        distance, closest = _closest_on_segment(point, start, end)
        on_a = point in (a1, a2)
        pair = (distance, point, closest) if on_a else (distance, closest, point)
        if best is None or pair[0] < best[0]:
            best = pair
    return best or (float("inf"), a1, b1)


def polygon_distance(a: Sequence[Sequence[float]],
                     b: Sequence[Sequence[float]]) -> Tuple[float, Point, Point]:
    """两个闭合多边形边界的最小距离及最近点。"""
    best: Optional[Tuple[float, Point, Point]] = None
    for a1, a2 in _edges(a):
        for b1, b2 in _edges(b):
            candidate = _segment_distance(a1, a2, b1, b2)
            if best is None or candidate[0] < best[0]:
                best = candidate
    return best or (float("inf"), (0.0, 0.0), (0.0, 0.0))


def _point_in_polygon(point: Point, polygon: Sequence[Sequence[float]]) -> bool:
    pts = [(float(p[0]), float(p[1])) for p in polygon]
    if len(pts) < 3:
        return False
    inside = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > point[1]) != (yj > point[1]) and \
                point[0] < (xj - xi) * (point[1] - yi) / ((yj - yi) or 1e-12) + xi:
            inside = not inside
        j = i
    return inside


def _point_polygon_distance(point: Point,
                            polygon: Sequence[Sequence[float]]) -> Tuple[float, Point, Point]:
    if _point_in_polygon(point, polygon):
        return 0.0, point, point
    best: Optional[Tuple[float, Point, Point]] = None
    for a, b in _edges(polygon):
        distance, closest = _closest_on_segment(point, a, b)
        if best is None or distance < best[0]:
            best = (distance, point, closest)
    return best or (float("inf"), point, point)


def row_distance(row_a: Dict[str, Any], row_b: Dict[str, Any]) -> Tuple[float, Point, Point]:
    """设施行间最小边界距离：区域—区域、区域—点、点—点。

    尺寸标注只需要最近边净距，不把中心距冒充净距。线状设施不参与
    净距配对；道路宽度另有 road_width/fire_lane_width 标注。
    """
    type_a = row_a["geometry"]["type"]
    type_b = row_b["geometry"]["type"]
    points_a = row_a["geometry"]["points_mm"]
    points_b = row_b["geometry"]["points_mm"]
    if type_a == "area" and type_b == "area":
        return polygon_distance(points_a, points_b)
    if type_a == "area" and type_b == "point":
        return _point_polygon_distance((float(points_b[0][0]), float(points_b[0][1])), points_a)
    if type_a == "point" and type_b == "area":
        distance, p1, p2 = _point_polygon_distance(
            (float(points_a[0][0]), float(points_a[0][1])), points_b)
        return distance, p1, p2
    if type_a == "point" and type_b == "point":
        p1 = (float(points_a[0][0]), float(points_a[0][1]))
        p2 = (float(points_b[0][0]), float(points_b[0][1]))
        return _dist(p1, p2), p1, p2
    # 兜底：用质心距离，但不把该值当作净距用于图面标注。
    c1 = _row_centroid(row_a) or (0.0, 0.0)
    c2 = _row_centroid(row_b) or (0.0, 0.0)
    return _dist(c1, c2), c1, c2


def _row_centroid(row: Dict[str, Any]) -> Optional[Point]:
    pts = row["geometry"]["points_mm"]
    if not pts:
        return None
    if len(pts) == 1:
        return float(pts[0][0]), float(pts[0][1])
    if row["geometry"]["type"] == "area" and len(pts) >= 3:
        signed = sum(
            pts[i][0] * pts[(i + 1) % len(pts)][1]
            - pts[(i + 1) % len(pts)][0] * pts[i][1]
            for i in range(len(pts))
        ) / 2.0
        if abs(signed) > 1e-9:
            cx = sum(
                (pts[i][0] + pts[(i + 1) % len(pts)][0])
                * (pts[i][0] * pts[(i + 1) % len(pts)][1]
                   - pts[(i + 1) % len(pts)][0] * pts[i][1])
                for i in range(len(pts))
            ) / (6.0 * signed)
            cy = sum(
                (pts[i][1] + pts[(i + 1) % len(pts)][1])
                * (pts[i][0] * pts[(i + 1) % len(pts)][1]
                   - pts[(i + 1) % len(pts)][0] * pts[i][1])
                for i in range(len(pts))
            ) / (6.0 * signed)
            return cx, cy
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def _polyline_midpoint(points: Sequence[Sequence[float]]) -> Optional[Point]:
    pts = [(float(p[0]), float(p[1])) for p in points]
    if not pts:
        return None
    if len(pts) == 1:
        return pts[0]
    segments = [(_dist(pts[i], pts[i + 1]), pts[i], pts[i + 1])
                for i in range(len(pts) - 1)]
    total = sum(item[0] for item in segments)
    if total <= 1e-9:
        return pts[0]
    target = total / 2.0
    walked = 0.0
    for length, a, b in segments:
        if walked + length >= target:
            ratio = (target - walked) / length
            return a[0] + (b[0] - a[0]) * ratio, a[1] + (b[1] - a[1]) * ratio
        walked += length
    return pts[-1]


def _longest_segment(points: Sequence[Sequence[float]]) -> Optional[Tuple[Point, Point, Point]]:
    """返回最长线段的 (起点, 终点, 中点)。"""
    best: Optional[Tuple[float, Point, Point]] = None
    for a, b in _polyline_edges(points):
        length = _dist(a, b)
        if best is None or length > best[0]:
            best = (length, a, b)
    if best is None or best[0] <= 1e-9:
        return None
    _length, a, b = best
    return a, b, ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)


# ---------- 结构边 ----------

def structure_edges(base_map: Dict[str, Any]) -> List[Tuple[Point, Point]]:
    """读取主体结构边：优先 structure_outline，其次 site_geometry 的建筑类线段。

    没有结构数据时返回空表，由调用方把「施工电梯距结构边」降级为 blocked，
    不拿红线或围挡冒充结构边。
    """
    edges: List[Tuple[Point, Point]] = []
    outline = base_map.get("structure_outline")
    if isinstance(outline, list) and len(outline) >= 3:
        try:
            edges.extend(_edges(outline))
        except (TypeError, ValueError, IndexError):
            pass
    for item in base_map.get("structures") or []:
        if not isinstance(item, dict):
            continue
        points = item.get("points") or item.get("outline") or []
        if isinstance(points, list) and len(points) >= 3:
            try:
                edges.extend(_edges(points))
            except (TypeError, ValueError, IndexError):
                continue
    keywords = ("主体", "结构", "building", "structure", "拟建")
    for row in base_map.get("site_geometry") or []:
        if not isinstance(row, dict) or row.get("category") in ("site_boundary", "road"):
            continue
        category = str(row.get("category") or "").lower()
        if not any(word in category for word in keywords):
            continue
        geom = row.get("geometry")
        if isinstance(geom, list) and len(geom) >= 4:
            edges.append(((float(geom[0]), float(geom[1])),
                          (float(geom[2]), float(geom[3]))))
    return edges


# ---------- 标注候选 ----------

def _offset_distance(p1: Point, p2: Point, centroid: Point, value: float) -> float:
    direction = _unit(p1, p2)
    if direction is None:
        return value
    normal = (-direction[1], direction[0])
    mid = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)
    toward = (centroid[0] - mid[0]) * normal[0] + (centroid[1] - mid[1]) * normal[1]
    return -value if toward > 0 else value


def _clearance_specs(model: Dict[str, Any], text_h: float,
                     skipped: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = model.get("facilities") or []
    by_category: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        if row["geometry"]["type"] in ("area", "point"):
            by_category.setdefault(row["category"], []).append(row)
    specs: List[Dict[str, Any]] = []
    covered_pairs: set = set()
    for category_a, category_b in CLEARANCE_PAIRS:
        if len(specs) >= MAX_CLEARANCE_DIMS:
            break
        pair_key = tuple(sorted((category_a, category_b)))
        if pair_key in covered_pairs:
            continue
        best: Optional[Tuple[float, Point, Point, Dict[str, Any], Dict[str, Any]]] = None
        for row_a in by_category.get(category_a, []):
            for row_b in by_category.get(category_b, []):
                distance, p1, p2 = row_distance(row_a, row_b)
                if distance <= MIN_CLEARANCE_MM or distance > MAX_CLEARANCE_MM:
                    continue
                if best is None or distance < best[0]:
                    best = (distance, p1, p2, row_a, row_b)
        if best is None:
            continue
        distance, p1, p2, row_a, row_b = best
        center_a = _row_centroid(row_a) or p1
        center_b = _row_centroid(row_b) or p2
        centroid = ((center_a[0] + center_b[0]) / 2.0, (center_a[1] + center_b[1]) / 2.0)
        offset = _offset_distance(p1, p2, centroid, text_h * 1.6)
        specs.append({
            "kind": "facility_clearance",
            "text": "净距 {:.2f}m".format(distance / 1000.0),
            "p1": [round(p1[0], 3), round(p1[1], 3)],
            "p2": [round(p2[0], 3), round(p2[1], 3)],
            "offset": round(offset, 3),
            "value_mm": round(distance, 3),
            "refs": [row_a["id"], row_b["id"]],
            "label": "{}↔{}".format(row_a["category_name"], row_b["category_name"]),
        })
        covered_pairs.add(pair_key)
    if not by_category:
        skipped.append({"kind": "facility_clearance", "reason": "无区域/点设施，无法计算净距",
                        "refs": []})
    expected = [pair for pair in CLEARANCE_PAIRS
                if pair[0] in by_category and pair[1] in by_category]
    if by_category and not expected:
        skipped.append({"kind": "facility_clearance",
                        "reason": "现有区域/点设施不在优先配对表内，未自动补净距",
                        "refs": []})
    elif by_category and not specs:
        skipped.append({"kind": "facility_clearance",
                        "reason": "优先配对设施净距均大于 {:.0f}m，图面不画跨场长线".format(
                            MAX_CLEARANCE_MM / 1000.0),
                        "refs": []})
    return specs


def _road_specs(model: Dict[str, Any], text_h: float,
                skipped: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    specs: List[Dict[str, Any]] = []
    for category, kind in ROAD_CATEGORY_KIND.items():
        candidates = [row for row in model.get("facilities") or []
                      if row["category"] == category and row["geometry"]["type"] == "line"]
        if not candidates:
            continue
        drawn = False
        for row in candidates:
            width = row.get("width_mm")
            if not width:
                continue
            segment = _longest_segment(row["geometry"]["points_mm"])
            if segment is None:
                continue
            a, b, mid = segment
            direction = _unit(a, b)
            if direction is None:
                continue
            normal = (-direction[1], direction[0])
            half = width / 2.0
            p1 = (mid[0] - normal[0] * half, mid[1] - normal[1] * half)
            p2 = (mid[0] + normal[0] * half, mid[1] + normal[1] * half)
            specs.append({
                "kind": kind,
                "text": "{}宽{:.2f}m".format(ROAD_LABEL[category], width / 1000.0),
                "p1": [round(p1[0], 3), round(p1[1], 3)],
                "p2": [round(p2[0], 3), round(p2[1], 3)],
                "offset": round(text_h * 1.2, 3),
                "value_mm": round(float(width), 3),
                "refs": [row["id"]],
                "label": ROAD_LABEL[category],
            })
            drawn = True
            break
        if not drawn:
            skipped.append({"kind": kind, "reason": "{}缺宽度，无法标注".format(ROAD_LABEL[category]),
                            "refs": [row["id"] for row in candidates]})
    return specs


def _crane_specs(model: Dict[str, Any], text_h: float,
                 skipped: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    specs: List[Dict[str, Any]] = []
    angles = (135.0, 45.0, 225.0, 315.0, 100.0, 260.0)
    for index, crane in enumerate(model.get("cranes") or []):
        radius = crane.get("jib_mm")
        if not radius:
            skipped.append({"kind": "crane_radius",
                            "reason": "塔吊 {} 缺臂长".format(crane.get("id")), "refs": [crane.get("id")]})
            continue
        cx, cy = crane["center_mm"]
        angle = math.radians(angles[index % len(angles)])
        p2 = (cx + float(radius) * math.cos(angle), cy + float(radius) * math.sin(angle))
        specs.append({
            "kind": "crane_radius",
            "text": "R={:.2f}m".format(float(radius) / 1000.0),
            "p1": [round(cx, 3), round(cy, 3)],
            "p2": [round(p2[0], 3), round(p2[1], 3)],
            "offset": round(text_h * 1.0, 3),
            "value_mm": round(float(radius), 3),
            "refs": [crane.get("id") or "crane"],
            "label": "塔吊回转半径",
        })
    return specs


def _elevator_specs(model: Dict[str, Any], base_map: Dict[str, Any], text_h: float,
                    skipped: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    elevators = [row for row in model.get("facilities") or []
                 if row["category"] == "construction_elevator"]
    if not elevators:
        return []
    edges = structure_edges(base_map)
    if not edges:
        skipped.append({"kind": "elevator_offset",
                        "reason": "输入缺主体结构轮廓，施工电梯距结构边无法标注",
                        "refs": [row["id"] for row in elevators]})
        return []
    specs: List[Dict[str, Any]] = []
    row = elevators[0]
    midpoint = _polyline_midpoint(row["geometry"]["points_mm"])
    if midpoint is None:
        skipped.append({"kind": "elevator_offset", "reason": "施工电梯几何为空",
                        "refs": [row["id"]]})
        return []
    best: Optional[Tuple[float, Point]] = None
    for a, b in edges:
        distance, point = _closest_on_segment(midpoint, a, b)
        if best is None or distance < best[0]:
            best = (distance, point)
    if best is None or best[0] <= 1.0:
        skipped.append({"kind": "elevator_offset", "reason": "施工电梯与结构边重合，净距为 0",
                        "refs": [row["id"]]})
        return []
    distance, point = best
    # 电梯净距通常只有 2~5m，而图块与文字都远大于这个间距；若把尺寸线
    # 贴着电梯画，文字必然压住吊笼/导轨。按制图习惯把尺寸线整体外移，
    # 延长线仍指回电梯与结构边，文字落在外侧空白区。
    offset = max(text_h * 4.8, 12000.0)
    specs.append({
        "kind": "elevator_offset",
        "text": "距结构边 {:.2f}m".format(distance / 1000.0),
        "p1": [round(midpoint[0], 3), round(midpoint[1], 3)],
        "p2": [round(point[0], 3), round(point[1], 3)],
        "offset": round(offset, 3),
        "value_mm": round(distance, 3),
        "refs": [row["id"]],
        "label": "施工电梯距结构边",
    })
    for extra in elevators[1:]:
        skipped.append({"kind": "elevator_offset",
                        "reason": "仅标注首个施工电梯，{} 需人工补充".format(extra["id"]),
                        "refs": [extra["id"]]})
    return specs


def build_dimension_specs(model: Dict[str, Any], base_map: Dict[str, Any],
                          text_h: float) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """返回 (标注候选, 跳过原因)。任何异常都变成 skip，不向上抛。"""
    skipped: List[Dict[str, Any]] = []
    specs: List[Dict[str, Any]] = []
    builders = (
        lambda: _clearance_specs(model, text_h, skipped),
        lambda: _road_specs(model, text_h, skipped),
        lambda: _crane_specs(model, text_h, skipped),
        lambda: _elevator_specs(model, base_map, text_h, skipped),
    )
    for build in builders:
        try:
            specs.extend(build())
        except Exception as exc:  # 标注失败必须留痕，不静默省略
            skipped.append({"kind": "unknown", "reason": "标注生成异常: {}".format(exc), "refs": []})
    specs.sort(key=lambda item: KIND_ORDER.index(item["kind"])
               if item["kind"] in KIND_ORDER else 99)
    return specs, skipped


def applicable_kinds(model: Dict[str, Any], base_map: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """返回 (数据上可标注的类型, 有设施但缺数据而 blocked 的类型)。"""
    rows = model.get("facilities") or []
    categories = {row["category"] for row in rows}
    applicable: List[str] = []
    blocked: List[str] = []
    if any(row["geometry"]["type"] == "area" for row in rows):
        applicable.append("facility_clearance")
    road_cats = {"temporary_road", "permanent_road"} & categories
    if road_cats:
        applicable.append("road_width")
    if "fire_access" in categories:
        applicable.append("fire_lane_width")
    if any(crane.get("jib_mm") for crane in model.get("cranes") or []):
        applicable.append("crane_radius")
    if "construction_elevator" in categories:
        if structure_edges(base_map):
            applicable.append("elevator_offset")
        else:
            blocked.append("elevator_offset")
    return applicable, blocked


# ---------- 坐标表 ----------

# 图内表只放关键点：红线弧段/短边会把上百个点塞进图纸，导致横向挤压；
# 全量点仍在 coordinates-<stage>.csv 中，图内表只做定位索引。
COORD_TABLE_LIMIT = 40

_COORD_PRIORITY: Dict[str, int] = {
    "tower_crane": 10,
    "site_access": 20,
    "construction_elevator": 30,
    "primary_distribution_box": 35,
    "distribution_room": 40,
    "transformer": 45,
    "fire_pump_room": 50,
    "fire_water_tank": 55,
    "fire_hydrant": 60,
    "processing_zone": 70,
    "steel_processing": 71,
    "wood_processing": 72,
    "mortar_processing": 73,
    "material_yard": 74,
    "temporary_dormitory": 80,
    "site_office": 81,
    "staff_dormitory": 78,
    "worker_living_zone": 79,
    "canteen": 82,
    "toilet_shower": 83,
    "drying_area": 84,
    "notice_board": 85,
    "wheel_wash": 86,
    "weighbridge": 87,
}
_REDLINE_PRIORITY = 90
# 主图只标这些“定位控制点”；消火栓、红线弧段点等仍在坐标表/CSV 中，
# 避免几十个蓝色编号把主体轮廓和设施图元压住。
_COORD_MAP_CATEGORIES = {
    "site_access", "construction_elevator", "primary_distribution_box",
    "distribution_room", "transformer", "fire_pump_room", "fire_water_tank",
}


def redline_key_indices(points: Sequence[Sequence[float]],
                        angle_tol_deg: float = 8.0) -> List[int]:
    """筛出表内需要的红线角点：只保留转角明显的点（弧段由 CSV 全量给出）。"""
    n = len(points)
    if n <= 8:
        return list(range(n))
    keep: List[int] = [0]
    for i in range(n):
        a, b, c = points[i - 1], points[i], points[(i + 1) % n]
        v1 = (b[0] - a[0], b[1] - a[1])
        v2 = (c[0] - b[0], c[1] - b[1])
        n1 = math.hypot(v1[0], v1[1])
        n2 = math.hypot(v2[0], v2[1])
        if n1 < 1e-9 or n2 < 1e-9:
            keep.append(i)
            continue
        dot = max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))
        if math.degrees(math.acos(dot)) >= angle_tol_deg:
            keep.append(i)
    keep = sorted(set(keep))
    if len(keep) < 4:
        step = max(1, n // 8)
        keep = sorted(set(keep) | set(range(0, n, step)))
    return keep


def build_coordinate_rows(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    redline = _ring(model.get("redline") or [])
    key_indices = set(redline_key_indices(redline))
    for index, point in enumerate(redline, start=1):
        rows.append({
            "id": "RL-{:02d}".format(index),
            "type": "红线角点",
            "name": "红线角点 {:02d}".format(index),
            "x_m": round(float(point[0]) / 1000.0, 3),
            "y_m": round(float(point[1]) / 1000.0, 3),
            "note": "用地红线",
            "table": (index - 1) in key_indices,
            "map": False,
            "priority": _REDLINE_PRIORITY,
        })
    for index, crane in enumerate(model.get("cranes") or [], start=1):
        cx, cy = crane["center_mm"]
        rows.append({
            "id": "TC-{:02d}".format(index),
            "type": "塔吊中心",
            "name": "{} {}".format(crane.get("id") or "TC", crane.get("model") or "").strip(),
            "x_m": round(float(cx) / 1000.0, 3),
            "y_m": round(float(cy) / 1000.0, 3),
            "note": "臂长 {}m".format(round(float(crane.get("jib_mm") or 0) / 1000.0, 2)),
            "table": True,
            "map": True,
            "priority": _COORD_PRIORITY["tower_crane"],
        })
    facilities = sorted(model.get("facilities") or [], key=lambda row: row["id"])
    for row in facilities:
        if row["category"] not in COORD_FACILITY_CATEGORIES:
            continue
        points = row["geometry"]["points_mm"]
        if not points:
            continue
        if row["geometry"]["type"] == "point":
            point = (float(points[0][0]), float(points[0][1]))
        elif row["geometry"]["type"] == "line":
            point = _polyline_midpoint(points)
        else:
            point = _row_centroid(row)
        if point is None:
            continue
        rows.append({
            "id": row["id"],
            "type": COORD_TYPE_NAMES.get(row["category"], row["category_name"]),
            "name": (row.get("name") or row["category_name"])[:16],
            "x_m": round(point[0] / 1000.0, 3),
            "y_m": round(point[1] / 1000.0, 3),
            "note": "设施定位点",
            "table": row["category"] in _COORD_PRIORITY,
            "map": row["category"] in _COORD_MAP_CATEGORIES,
            "priority": _COORD_PRIORITY.get(row["category"], 95),
        })
    return rows


def select_table_rows(rows: Sequence[Dict[str, Any]],
                      limit: int = COORD_TABLE_LIMIT) -> List[Dict[str, Any]]:
    """图内关键点：按优先级截断；全量点始终保留在 CSV。"""
    picked = [row for row in rows if row.get("table")]
    if not picked:
        picked = list(rows)
    picked.sort(key=lambda row: (int(row.get("priority") or 99), str(row["id"])))
    return picked[:max(1, int(limit))]
