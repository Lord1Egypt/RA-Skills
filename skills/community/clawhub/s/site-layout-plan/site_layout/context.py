"""周边环境约束（site-context/v1）：高压线、住宅、河道、市政管线、既有道路/建筑。

本模块只做确定性的距离与缓冲区判断，不代替管线探测、产权协调和现场踏勘。
坐标统一为 mm；上下文文件必须声明 coord_unit，缺单位直接报错，不猜。
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

SCHEMA = "site-context/v1"
UNIT_TO_MM = {"mm": 1.0, "cm": 10.0, "m": 1000.0}

LIVING = {"temporary_dormitory", "site_office", "temporary_building",
          "staff_dormitory", "worker_living_zone", "canteen",
          "toilet_shower", "drying_area"}

# 经验/规范混合默认值。项目必须按当地规定、产权单位要求和专项方案复核。
DEFAULTS: Dict[str, Dict[str, Any]] = {
    "high_voltage": {
        "buffer_m": 8.0, "severity": "hard",
        "affects": ["living", "tower_crane", "temporary_dormitory", "site_office",
                    "temporary_building", "processing_zone", "steel_processing",
                    "wood_processing", "mortar_processing", "material_yard",
                    "transformer", "fire_pump_room", "fire_water_tank",
                    "parking", "fire_hydrant", "safety_podium"],
        "basis": "经验", "note": "按电压等级、导线类型和当地供电部门要求复核；塔吊回转不得侵入",
    },
    "residential": {
        "buffer_m": 10.0, "severity": "hard",
        "affects": ["living", "temporary_dormitory", "site_office", "temporary_building",
                    "processing_zone", "steel_processing", "wood_processing",
                    "mortar_processing", "transformer", "waste_pool", "safety_podium"],
        "basis": "经验", "note": "噪声、粉尘、光污染和日照影响需专项评估",
    },
    "river": {
        "buffer_m": 15.0, "severity": "hard",
        "affects": ["living", "temporary_dormitory", "site_office", "temporary_building",
                    "processing_zone", "steel_processing", "wood_processing",
                    "mortar_processing", "material_yard", "waste_pool", "wheel_wash",
                    "transformer", "fire_water_tank", "fire_pump_room",
                    "drainage_ditch"],
        "basis": "经验", "note": "按河道蓝线、防洪和环保要求复核；不得向河道排水",
    },
    "municipal_pipeline": {
        "buffer_m": 3.0, "severity": "hard", "affects": ["all"],
        "basis": "经验", "note": "管线种类多，必须查产权单位图纸并现场探挖；3 m 仅为占位默认值",
    },
    "existing_building": {
        "buffer_m": 3.0, "severity": "hard", "affects": ["all"],
        "basis": "经验", "note": "既有建筑基础、沉降和消防间距需专项复核",
    },
    "sensitive_receptor": {
        "buffer_m": 20.0, "severity": "soft",
        "affects": ["living", "temporary_dormitory", "site_office", "processing_zone",
                    "steel_processing", "wood_processing", "mortar_processing",
                    "waste_pool"],
        "basis": "经验", "note": "学校、医院、居民等敏感点，按环评与投诉风险复核",
    },
    "flood": {
        "buffer_m": 0.0, "severity": "soft", "affects": ["all"],
        "basis": "经验", "note": "低洼地、汇水方向需结合竖向设计复核",
    },
}

ALIASES = {
    "powerline": "high_voltage", "power_line": "high_voltage", "highvoltage": "high_voltage",
    "house": "residential", "neighbor_building": "residential",
    "watercourse": "river", "canal": "river",
    "pipeline": "municipal_pipeline", "utility": "municipal_pipeline",
    "building": "existing_building", "existing": "existing_building",
    "school": "sensitive_receptor", "hospital": "sensitive_receptor",
}


class ContextError(Exception):
    exit_code = 2


class ContextUnitError(ContextError):
    exit_code = 4


def _f(value: Any, label: str) -> float:
    if isinstance(value, bool):
        raise ContextError(f"{label} 必须是数字")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ContextError(f"{label} 必须是数字，收到 {value!r}") from exc
    if not math.isfinite(number):
        raise ContextError(f"{label} 必须是有限数字")
    return number


def _pt(value: Any, label: str) -> Tuple[float, float]:
    if isinstance(value, dict):
        value = [value.get("x"), value.get("y")]
    if not isinstance(value, (list, tuple)) or len(value) < 2:
        raise ContextError(f"{label} 必须是 [x, y]")
    return _f(value[0], f"{label}[0]"), _f(value[1], f"{label}[1]")


def _dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _point_segment(p: Sequence[float], a: Sequence[float], b: Sequence[float]) -> float:
    dx, dy = b[0] - a[0], b[1] - a[1]
    if abs(dx) < 1e-12 and abs(dy) < 1e-12:
        return _dist(p, a)
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return _dist(p, (a[0] + t * dx, a[1] + t * dy))


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


def _segments_cross(a1, a2, b1, b2) -> bool:
    def orient(p, q, r):
        value = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        if abs(value) < 1e-9:
            return 0
        return 1 if value > 0 else -1
    return (orient(a1, a2, b1) != orient(a1, a2, b2)
            and orient(b1, b2, a1) != orient(b1, b2, a2))


def _polyline_distance(p: Sequence[float], points: Sequence[Sequence[float]]) -> float:
    if len(points) == 1:
        return _dist(p, points[0])
    return min(_point_segment(p, points[i], points[i + 1]) for i in range(len(points) - 1))


def _geometry_distance(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    ap, bp = a["points_mm"], b["points_mm"]
    if not ap or not bp:
        return float("inf")
    if a["type"] == "point":
        if b["type"] == "area" and _point_in_polygon(ap[0], bp):
            return 0.0
        if b["type"] == "area":
            return min(_point_segment(ap[0], bp[i], bp[(i + 1) % len(bp)]) for i in range(len(bp)))
        return _polyline_distance(ap[0], bp)
    if b["type"] == "point":
        return _geometry_distance(b, a)
    # 面/线对线/面：先看边相交，再看顶点距离
    if a["type"] == "area":
        pa = list(ap) + [ap[0]]
    else:
        pa = ap
    if b["type"] == "area":
        pb = list(bp) + [bp[0]]
    else:
        pb = bp
    for i in range(len(pa) - 1):
        for j in range(len(pb) - 1):
            if _segments_cross(pa[i], pa[i + 1], pb[j], pb[j + 1]):
                return 0.0
    best = min((_polyline_distance(p, bp) for p in ap), default=float("inf"))
    best = min(best, min((_polyline_distance(p, ap) for p in bp), default=float("inf")))
    if a["type"] == "area" and any(_point_in_polygon(p, ap) for p in bp):
        return 0.0
    if b["type"] == "area" and any(_point_in_polygon(p, bp) for p in ap):
        return 0.0
    return best


def _canonical_type(value: Any) -> str:
    key = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    return ALIASES.get(key, key)


def _normalize_geometry(raw: Any, factor: float, label: str) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raise ContextError(f"{label} 必须是对象")
    kind = str(raw.get("type") or "").strip().lower()
    if kind in ("point", "insert", "xy"):
        value = raw.get("xy") or raw.get("point") or raw.get("insert")
        if value is None:
            points = raw.get("points")
            if isinstance(points, list) and len(points) == 1:
                value = points[0]
        p = _pt(value, label)
        return {"type": "point", "points_mm": [(p[0] * factor, p[1] * factor)], "closed": False}
    points = raw.get("points") or raw.get("vertices") or raw.get("polyline")
    if points is None and isinstance(raw.get("bbox"), list) and len(raw["bbox"]) == 4:
        x0, y0, x1, y1 = (_f(v, f"{label}.bbox") for v in raw["bbox"])
        points = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]
    if not isinstance(points, list) or not points:
        raise ContextError(f"{label} 缺 points/xy/bbox")
    pts = [_pt(p, f"{label}.points[{i}]") for i, p in enumerate(points)]
    if len(pts) >= 2 and _dist(pts[0], pts[-1]) <= 1e-6:
        pts = pts[:-1]
    geo_type = "area" if (kind in ("polygon", "area", "rect") or len(pts) >= 3 and raw.get("closed")) else (
        "line" if len(pts) > 1 else "point")
    return {"type": geo_type,
            "points_mm": [(p[0] * factor, p[1] * factor) for p in pts],
            "closed": geo_type == "area"}


def _declared_unit(data: Dict[str, Any]) -> Tuple[str, float]:
    raw = data.get("coord_unit") or data.get("unit") or data.get("units")
    text = str(raw or "").strip().lower()
    if isinstance(raw, dict):
        text = str(raw.get("drawing_unit") or raw.get("unit") or "").strip().lower()
    if text not in UNIT_TO_MM:
        raise ContextUnitError(
            "site-context 必须显式声明 coord_unit=mm/cm/m；"
            "周边管线、高压线距离不能靠猜单位"
        )
    return text, UNIT_TO_MM[text]


def _affects_for(kind: str, raw: Dict[str, Any]) -> List[str]:
    value = raw.get("affects")
    if isinstance(value, list) and value:
        return [str(v) for v in value]
    return list(DEFAULTS.get(kind, {}).get("affects") or ["all"])


def load_context(path: str | Path | None, base_map: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    warnings: List[str] = []
    if path:
        file = Path(path).expanduser()
        if not file.is_file():
            raise ContextError(f"找不到周边环境文件：{file}")
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ContextError(f"周边环境文件不是合法 JSON：{file}：{exc}") from exc
        if not isinstance(data, dict):
            raise ContextError("周边环境文件顶层必须是对象")
        if str(data.get("schema") or "") != SCHEMA:
            raise ContextError(f"周边环境 schema={data.get('schema')!r}；只接受 {SCHEMA}")
        unit, factor = _declared_unit(data)
        source_path: Optional[str] = str(file.resolve())
    else:
        data = {}
        unit, factor = "mm", 1.0
        source_path = None
        warnings.append("未提供 site-context，周边环境按“未调查”处理；高压线、河道、管线必须现场踏勘补充")

    boundary_raw = data.get("boundary")
    boundary: List[List[float]] = []
    if isinstance(boundary_raw, list) and len(boundary_raw) >= 3:
        boundary = [[_f(p[0], "boundary") * factor, _f(p[1], "boundary") * factor]
                    for p in boundary_raw if isinstance(p, (list, tuple)) and len(p) >= 2]
    elif base_map and isinstance(base_map.get("redline"), list):
        boundary = [[float(p[0]), float(p[1])] for p in base_map["redline"]]

    constraints: List[Dict[str, Any]] = []
    for index, raw in enumerate(data.get("constraints") or []):
        if not isinstance(raw, dict):
            continue
        kind = _canonical_type(raw.get("type") or raw.get("kind"))
        defaults = DEFAULTS.get(kind, {})
        buffer_m = raw.get("buffer_m", raw.get("setback_m", defaults.get("buffer_m", 0.0)))
        buffer_m = _f(buffer_m or 0.0, f"constraints[{index}].buffer_m")
        geometry = _normalize_geometry(raw.get("geometry") or raw, factor, f"constraints[{index}]")
        constraints.append({
            "id": str(raw.get("id") or f"C-{index + 1:02d}"),
            "type": kind,
            "name": str(raw.get("name") or kind),
            "geometry": geometry,
            "buffer_mm": buffer_m * 1000.0,
            "severity": str(raw.get("severity") or defaults.get("severity") or "hard"),
            "affects": _affects_for(kind, raw),
            "basis": str(raw.get("basis") or defaults.get("basis") or "经验"),
            "voltage_kv": raw.get("voltage_kv"),
            "note": str(raw.get("note") or defaults.get("note") or ""),
            "status": str(raw.get("status") or "confirmed"),
        })

    existing_roads: List[Dict[str, Any]] = []
    for index, raw in enumerate(data.get("existing_roads") or []):
        if not isinstance(raw, dict):
            continue
        existing_roads.append({
            "id": str(raw.get("id") or f"ER-{index + 1:02d}"),
            "name": str(raw.get("name") or "既有道路"),
            "geometry": _normalize_geometry(raw.get("geometry") or raw, factor, f"existing_roads[{index}]"),
            "width_m": _f(raw.get("width_m") or 7.0, f"existing_roads[{index}].width_m"),
        })

    return {
        "schema": SCHEMA,
        "project": str(data.get("project") or (base_map or {}).get("project") or ""),
        "coord_unit": "mm",
        "source_unit": unit,
        "boundary": boundary,
        "constraints": constraints,
        "existing_roads": existing_roads,
        "wind": data.get("wind") if isinstance(data.get("wind"), dict) else {},
        "north_angle_deg": data.get("north_angle_deg"),
        "source_path": source_path,
        "warnings": warnings,
        "final_check": False,
    }


def _category_affected(category: str, constraint: Dict[str, Any]) -> bool:
    # 既有道路、围挡、相邻地貌本身是周边条件，不再拿它们去撞周边缓冲
    if category in ("permanent_road", "hoarding", "site_boundary_neighbor"):
        return False
    affects = constraint.get("affects") or ["all"]
    if "all" in affects:
        return True
    if "living" in affects and category in LIVING:
        return True
    return category in affects


def check_context(facilities: Sequence[Dict[str, Any]], cranes: Sequence[Dict[str, Any]],
                  context: Dict[str, Any]) -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    constraints = context.get("constraints") or []
    for index, constraint in enumerate(constraints):
        hits: List[Dict[str, Any]] = []
        for row in facilities:
            category = str(row.get("category") or "")
            if not _category_affected(category, constraint):
                continue
            distance = _geometry_distance(row["geometry"], constraint["geometry"])
            if distance < constraint["buffer_mm"] - 1.0:
                hits.append({
                    "facility": row.get("id"), "category": category,
                    "distance_m": round(distance / 1000.0, 2),
                    "required_m": round(constraint["buffer_mm"] / 1000.0, 2),
                })
        # 塔吊回转半径是三维作业面，平面距离要扣掉臂长
        if constraint.get("type") == "high_voltage" and "tower_crane" in (constraint.get("affects") or []):
            for crane in cranes:
                center = crane.get("center_mm")
                jib = crane.get("jib_mm")
                if not center:
                    continue
                distance = _polyline_distance(center, constraint["geometry"]["points_mm"])
                clear = distance - float(jib or 0.0)
                if clear < constraint["buffer_mm"] - 1.0:
                    hits.append({
                        "facility": crane.get("id"), "category": "tower_crane_jib",
                        "distance_m": round(clear / 1000.0, 2),
                        "required_m": round(constraint["buffer_mm"] / 1000.0, 2),
                        "note": "按塔吊回转外缘至高压线净距计算",
                    })
        status = "pass"
        if hits:
            status = "fail" if constraint.get("severity") == "hard" else "review"
        checks.append({
            "id": f"C{index + 1}",
            "name": f"周边约束：{constraint.get('name')}",
            "type": constraint.get("type"),
            "status": status,
            "basis": constraint.get("basis"),
            "severity": constraint.get("severity"),
            "message": ("{} 项设施进入 {} m 缓冲/净距".format(len(hits), round(constraint["buffer_mm"] / 1000.0, 1))
                        if hits else "未发现设施进入缓冲/净距"),
            "evidence": {
                "constraint_id": constraint.get("id"),
                "buffer_m": round(constraint["buffer_mm"] / 1000.0, 2),
                "hits": hits,
                "note": constraint.get("note"),
            },
        })
    summary = {"pass": 0, "review": 0, "fail": 0}
    for check in checks:
        summary[check["status"]] += 1
    return {
        "schema": "site-context-check/v1",
        "constraints": len(constraints),
        "checks": checks,
        "summary": summary,
        "final_check": False,
        "boundary": "周边距离为平面净距代理，未含高差、埋深、管线走向和产权边界；必须现场踏勘与产权单位复核。",
    }


def point_blocked(point: Sequence[float], context: Dict[str, Any], category: str,
                  extra_mm: float = 0.0) -> Optional[Dict[str, Any]]:
    for constraint in context.get("constraints") or []:
        if not _category_affected(category, constraint):
            continue
        distance = _polyline_distance(point, constraint["geometry"]["points_mm"])
        if constraint["geometry"]["type"] == "area" and _point_in_polygon(point, constraint["geometry"]["points_mm"]):
            distance = 0.0
        if distance < constraint["buffer_mm"] + extra_mm:
            return constraint
    return None


def geometry_blocked(geometry: Dict[str, Any], context: Dict[str, Any], category: str,
                     extra_mm: float = 0.0) -> Optional[Dict[str, Any]]:
    for constraint in context.get("constraints") or []:
        if not _category_affected(category, constraint):
            continue
        distance = _geometry_distance(geometry, constraint["geometry"])
        if distance < constraint["buffer_mm"] + extra_mm:
            return constraint
    return None


def render_context_markdown(result: Dict[str, Any]) -> str:
    lines = ["# 周边环境约束校核", "",
             "> 只做平面净距代理；不含高差、埋深、管线走向与产权边界，必须现场踏勘复核。", ""]
    if not result["checks"]:
        lines += ["未提供周边约束。高压线、住宅、河道、市政管线必须补调查。", ""]
    for check in result["checks"]:
        lines += [f"## {check['id']} {check['name']}（{check['status']}）", "",
                  check["message"], "",
                  "依据：{}　缓冲：{} m".format(check.get("basis"), check["evidence"].get("buffer_m")), ""]
        if check["evidence"].get("hits"):
            lines += ["命中设施："]
            for hit in check["evidence"]["hits"]:
                lines.append("- {}（{}）：{:.2f} m".format(hit["facility"], hit["category"], hit["distance_m"]))
            lines.append("")
    lines += ["## 汇总", "",
              "- pass：{pass}　review：{review}　fail：{fail}".format(**result["summary"]), ""]
    return "\n".join(lines)
