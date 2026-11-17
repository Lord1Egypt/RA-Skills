"""施工平面布置：分阶段场地模型 + 确定性规则校核。

定位
----
本模块只做"把已识别的证据组织成某阶段的布置模型，并跑可复算的规则"，
不做布置方案自动生成、不选型、不替代施工组织设计审批。

硬规则：
- 坐标统一 mm；单位依据来自 base-map（prepare_site 已留痕），设施文件必须声明单位。
- 阶段只有 earthwork / structure / finish 三个，设施用 active_stages 声明生效阶段。
- 缺证据的规则给 manual，不补 0、不猜位置；几何冲突与硬性缺失给 fail。
- final_check 恒为 false；出图必带 DRAFT。
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from .taxonomy import (
    FACILITIES, REQUIRED_BY_STAGE, STAGE_NAMES, STAGE_ORDER, STAGES,
    canonical, is_known, meta,
)

MODEL_SCHEMA = "site-stage-layout/v1"
FACILITY_SCHEMA = "cad-site-facility/v1"
UNIT_TO_MM = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "ft": 304.8}

# 加工区 0.6.0 拆分（processing_zone 为旧数据通用类，保留兼容）
PROCESSING_CATEGORIES: Tuple[str, ...] = (
    "processing_zone", "steel_processing", "wood_processing", "mortar_processing",
)
# 0.7.0 生活区：员工宿舍与工人生活区分设；工人生活区内再放食堂、卫生间/淋浴、
# 晾晒区子块。旧 temporary_dormitory/temporary_building 仅保留兼容读取。
LIVING_CATEGORIES: Tuple[str, ...] = (
    "staff_dormitory", "worker_living_zone", "canteen", "toilet_shower",
    "drying_area", "temporary_dormitory", "temporary_building",
)
LIVING_ZONE_CATEGORIES: Tuple[str, ...] = (
    "staff_dormitory", "worker_living_zone", "temporary_dormitory", "temporary_building",
)
QUIET_CATEGORIES: Tuple[str, ...] = ("site_office",) + LIVING_CATEGORIES

DEFAULT_PARAMS: Dict[str, float] = {
    "fire_lane_min_width_m": 4.0,
    "road_min_width_m": 3.5,
    "temporary_road_default_width_m": 4.0,
    "hydrant_max_spacing_m": 120.0,
    "hydrant_max_radius_m": 150.0,
    "box_to_room_max_m": 30.0,
    "box_to_load_max_m": 50.0,
    "processing_separation_m": 10.0,
    "waste_separation_m": 20.0,
    "notice_to_gate_m": 50.0,
    "road_overlap_sample_m": 5.0,
    "road_overlap_tolerance_m": 1.5,
    "road_overlap_min_ratio": 0.3,
    "connect_tolerance_m": 2.0,
    "road_dual_min_width_m": 6.0,
    "passing_bay_interval_m": 100.0,
    "turning_radius_min_m": 9.0,
    "fire_turning_radius_min_m": 12.0,
    "dead_end_turnaround_min_m": 12.0,
    # 0.6.0 加工区拆分后的分项隔离距离（经验值，可按项目覆盖）
    "steel_processing_separation_m": 10.0,
    "wood_processing_separation_m": 12.0,
    "mortar_processing_separation_m": 15.0,
    "wood_to_power_min_m": 15.0,
    # 0.6.0 新增设施
    "pump_to_tank_max_m": 30.0,
    "pump_to_fire_lane_max_m": 30.0,
    "transformer_to_living_min_m": 10.0,
    "transformer_to_combustible_min_m": 10.0,
    "drainage_connect_tolerance_m": 2.0,
    # 0.6.7 出入口服务带：洗车台/地磅贴大门主路
    "wash_to_gate_max_m": 30.0,
    "wash_to_road_max_m": 8.0,
    "weighbridge_to_gate_max_m": 60.0,
    "weighbridge_to_road_max_m": 10.0,
    # 0.7.0 生活区与作业面分离、办公靠门、消防可达、宿舍分区间距
    "living_to_processing_min_m": 20.0,
    "living_to_worksite_min_m": 10.0,
    "office_to_gate_max_m": 50.0,
    "living_fire_lane_max_m": 30.0,
    "living_separation_min_m": 3.0,
}


class SitePlanError(Exception):
    """输入/单位/字段错误（CLI exit 2 或 4）。"""

    exit_code = 2


class UnitError(SitePlanError):
    exit_code = 4


# ------------------------------------------------------------------ 几何
def _f(value: Any, label: str) -> float:
    if isinstance(value, bool):
        raise SitePlanError(f"{label} 必须是数字，收到布尔值")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise SitePlanError(f"{label} 必须是数字，收到 {value!r}") from exc
    if not math.isfinite(number):
        raise SitePlanError(f"{label} 必须是有限数字，收到 {value!r}")
    return number


def _pt(value: Any, label: str) -> Tuple[float, float]:
    if isinstance(value, dict):
        value = [value.get("x"), value.get("y")]
    if not isinstance(value, (list, tuple)) or len(value) < 2:
        raise SitePlanError(f"{label} 必须是 [x, y]")
    return _f(value[0], f"{label}[0]"), _f(value[1], f"{label}[1]")


def _dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _point_segment_distance(p: Sequence[float], a: Sequence[float], b: Sequence[float]) -> float:
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    dx, dy = bx - ax, by - ay
    if abs(dx) < 1e-12 and abs(dy) < 1e-12:
        return _dist(p, a)
    t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return _dist(p, (ax + t * dx, ay + t * dy))


def polygon_area_mm2(points: Sequence[Sequence[float]]) -> float:
    if len(points) < 3:
        return 0.0
    return abs(sum(
        points[i][0] * points[(i + 1) % len(points)][1]
        - points[(i + 1) % len(points)][0] * points[i][1]
        for i in range(len(points))
    ) / 2.0)


def polyline_length_mm(points: Sequence[Sequence[float]]) -> float:
    return sum(_dist(points[i], points[i + 1]) for i in range(len(points) - 1))


def point_in_polygon(p: Sequence[float], polygon: Sequence[Sequence[float]],
                     tolerance_mm: float = 1.0) -> bool:
    if len(polygon) < 3:
        return False
    for i, a in enumerate(polygon):
        b = polygon[(i + 1) % len(polygon)]
        if _point_segment_distance(p, a, b) <= tolerance_mm:
            return True
    x, y = p[0], p[1]
    inside = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i][0], polygon[i][1]
        xj, yj = polygon[j][0], polygon[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            inside = not inside
        j = i
    return inside


def _bbox(points: Sequence[Sequence[float]]) -> Tuple[float, float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def _sample_polyline(points: Sequence[Sequence[float]], step_mm: float) -> List[Tuple[float, float]]:
    samples: List[Tuple[float, float]] = []
    if len(points) < 2 or step_mm <= 0:
        return samples
    carry = 0.0
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        length = _dist(a, b)
        if length <= 1e-9:
            continue
        t = carry
        while t < length:
            ratio = t / length
            samples.append((a[0] + (b[0] - a[0]) * ratio, a[1] + (b[1] - a[1]) * ratio))
            t += step_mm
        carry = t - length
    return samples


def _segments_cross(a1, a2, b1, b2) -> bool:
    def orient(p, q, r):
        value = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        if abs(value) < 1e-9:
            return 0
        return 1 if value > 0 else -1

    o1 = orient(a1, a2, b1)
    o2 = orient(a1, a2, b2)
    o3 = orient(b1, b2, a1)
    o4 = orient(b1, b2, a2)
    return o1 != o2 and o3 != o4


def _polylines_intersect(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> bool:
    for i in range(len(a) - 1):
        for j in range(len(b) - 1):
            if _segments_cross(a[i], a[i + 1], b[j], b[j + 1]):
                return True
    return False


# ------------------------------------------------------------------ 输入
def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: str | Path, label: str) -> Tuple[Dict[str, Any], str]:
    file = Path(path).expanduser()
    if not file.is_file():
        raise SitePlanError(f"找不到 {label}：{file}")
    raw = file.read_bytes()
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SitePlanError(f"{label} 不是合法 JSON：{file}：{exc}") from exc
    if not isinstance(data, dict):
        raise SitePlanError(f"{label} 顶层必须是对象：{file}")
    return data, _sha256_bytes(raw)


def _declared_unit(data: Dict[str, Any]) -> Tuple[str, str]:
    for key in ("coord_unit", "unit", "units", "drawing_unit"):
        value = data.get(key)
        if isinstance(value, dict):
            value = value.get("drawing_unit") or value.get("unit")
        text = str(value or "").strip().lower()
        if text:
            return text, f"top:{key}"
    audit = data.get("scale_unit_audit")
    if isinstance(audit, list):
        values: List[str] = []
        for row in audit:
            if isinstance(row, dict):
                for key in ("units", "unit", "drawing_unit"):
                    raw = row.get(key)
                    if isinstance(raw, list):
                        values.extend(str(v).strip().lower() for v in raw if str(v).strip())
                    elif str(raw or "").strip():
                        values.append(str(raw).strip().lower())
        unique = sorted(set(values))
        if len(unique) == 1:
            return unique[0], "scale_unit_audit"
        if len(unique) > 1:
            raise UnitError(f"设施文件单位冲突：{unique}；先统一单位，不挑一个看起来对的")
    return "", "missing"


def _unit_factor(data: Dict[str, Any], label: str) -> Tuple[str, float]:
    unit, basis = _declared_unit(data)
    if not unit:
        raise UnitError(f"{label} 未声明坐标单位（coord_unit/unit）；请补 mm 或 m，禁止猜倍数")
    if unit not in UNIT_TO_MM:
        raise UnitError(f"{label} 单位 {unit!r} 不支持；只接受 mm/cm/m/ft")
    return unit, UNIT_TO_MM[unit]


def _stage_list(raw: Any, label: str) -> List[str]:
    if raw in (None, ""):
        return list(STAGES)
    if isinstance(raw, str):
        raw = [item.strip() for item in raw.split(",") if item.strip()]
    if not isinstance(raw, list):
        raise SitePlanError(f"{label}.active_stages 必须是数组或逗号分隔字符串")
    out: List[str] = []
    for item in raw:
        key = str(item).strip().lower()
        if key not in STAGE_ORDER:
            raise SitePlanError(f"{label}.active_stages 含未知阶段 {item!r}；只接受 {list(STAGES)}")
        if key not in out:
            out.append(key)
    return out


def _normalize_geometry(raw: Any, factor: float, label: str) -> Dict[str, Any]:
    """把多种写法归一为 {type, points_mm, closed}。"""
    geom = raw
    if isinstance(raw, dict) and "geometry" in raw:
        geom = raw.get("geometry")
    if isinstance(geom, dict):
        kind = str(geom.get("type") or "").strip().lower()
        if kind in ("point", "insert", "xy"):
            value = geom.get("xy") or geom.get("point") or geom.get("insert")
            legacy = geom.get("points_mm") or geom.get("points")
            if value is None and isinstance(legacy, list) and len(legacy) == 1:
                value = legacy[0]
            point = _pt(value, label)
            return {"type": "point", "points_mm": [(point[0] * factor, point[1] * factor)], "closed": False}
        points_raw = (geom.get("points") or geom.get("vertices") or geom.get("polyline")
                      or geom.get("points_mm"))
        if points_raw is None and isinstance(geom.get("bbox"), list):
            bbox = geom["bbox"]
            if len(bbox) == 4:
                x0, y0, x1, y1 = (_f(v, f"{label}.bbox") for v in bbox)
                points_raw = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]
        if points_raw is None:
            raise SitePlanError(f"{label}.geometry 缺 points/xy/bbox")
        closed = kind in ("polygon", "area", "rect") or bool(geom.get("closed"))
        if kind in ("polyline", "line", "path", "route"):
            # 闭合多段线可以是"环形消防车道"，仍然是线状设施，不能当区域
            geo_type = "line"
        elif len(points_raw) > 1:
            geo_type = "area"
        else:
            geo_type = "point"
    else:
        points_raw = geom
        if not isinstance(points_raw, list) or not points_raw:
            raise SitePlanError(f"{label}.geometry 必须是非空数组或对象")
        closed = len(points_raw) >= 3
        geo_type = "area" if closed else ("line" if len(points_raw) > 1 else "point")
    points = [_pt(item, f"{label}.geometry[{i}]") for i, item in enumerate(points_raw)]
    if len(points) >= 2 and _dist(points[0], points[-1]) <= 1e-6:
        points = points[:-1]
        closed = len(points) >= 3
    points_mm = [(x * factor, y * factor) for x, y in points]
    if geo_type == "point" and len(points_mm) != 1:
        geo_type = "line"
    return {"type": geo_type, "points_mm": points_mm, "closed": closed}


def load_facilities(path: str | Path) -> Tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    data, sha = load_json(path, "设施文件")
    schema = str(data.get("schema") or "")
    if schema not in (FACILITY_SCHEMA, "site-facilities/v1", "cad-site-facility/v1"):
        raise SitePlanError(
            f"设施文件 schema={schema!r}；只接受 {FACILITY_SCHEMA} 或 site-facilities/v1"
        )
    unit, factor = _unit_factor(data, "设施文件")
    rows = data.get("facilities")
    if not isinstance(rows, list):
        raise SitePlanError("设施文件 facilities 必须是数组")
    facilities: List[Dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(rows):
        if not isinstance(raw, dict):
            raise SitePlanError(f"facilities[{index}] 必须是对象")
        fid = str(raw.get("id") or raw.get("facility_id") or "").strip()
        if not fid:
            fid = "F-{:03d}".format(index + 1)
        if fid in seen:
            raise SitePlanError(f"设施 id 重复：{fid}")
        seen.add(fid)
        category = canonical(raw.get("category") or raw.get("type"))
        if not is_known(category):
            raise SitePlanError(
                f"{fid}.category={raw.get('category')!r} 未收录；请用 taxonomy 中的分类或补别名"
            )
        info = meta(category)
        geometry = _normalize_geometry(raw.get("geometry") or raw.get("insert_xy"), factor, fid)
        stages = _stage_list(raw.get("active_stages", raw.get("stages")), fid)
        width_m = raw.get("width_m")
        width_mm = None
        if raw.get("width_mm") is not None:
            width_mm = _f(raw.get("width_mm"), f"{fid}.width_mm")
        elif width_m is not None:
            width_mm = _f(width_m, f"{fid}.width_m") * 1000.0
        if width_mm is not None and width_mm <= 0:
            raise SitePlanError(f"{fid}.width_m(width_mm) 必须大于 0")
        status = str(raw.get("status") or raw.get("confidence") or "candidate")
        facilities.append({
            "id": fid,
            "category": category,
            "category_name": info["zh"],
            "name": str(raw.get("name") or info["zh"]),
            "geometry": geometry,
            "width_mm": width_mm,
            "active_stages": stages,
            "source": str(raw.get("source") or "unknown"),
            "confidence": status,
            "evidence": raw.get("evidence") if isinstance(raw.get("evidence"), list) else [],
            "attrs": raw.get("attrs") if isinstance(raw.get("attrs"), dict) else {},
            "raw_status": str(raw.get("status") or ""),
        })
    contract = data.get("contract") if isinstance(data.get("contract"), dict) else {}
    source = {
        "facilities_path": str(Path(path).expanduser().resolve()),
        "facilities_sha256": sha,
        "facilities_unit": unit,
        "facilities_unit_basis": _declared_unit(data)[1],
        "contract_id": str(contract.get("contract_id") or data.get("contract_id") or ""),
        "source_sha256": str(contract.get("source_sha256") or data.get("source_sha256") or ""),
        "reader_version": str(contract.get("reader_version") or ""),
    }
    return facilities, source, data


def _coordinate_margin(extents: Sequence[float]) -> float:
    """允许塔吊略在红线外的余量；不同原点的坐标会差几个数量级，不会被放过。"""
    width = abs(float(extents[2]) - float(extents[0]))
    height = abs(float(extents[3]) - float(extents[1]))
    return max(50_000.0, 0.25 * max(width, height))


def _inside_extents(point: Sequence[float], extents: Sequence[float], margin: float) -> bool:
    return (
        float(extents[0]) - margin <= float(point[0]) <= float(extents[2]) + margin
        and float(extents[1]) - margin <= float(point[1]) <= float(extents[3]) + margin
    )


def load_cranes(
    paths: Optional[Sequence[str]],
    base_extents: Optional[Sequence[float]] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """加载塔吊正式候选。

    只有 center_status=insert_point 才进入正式检查；circle_center / review /
    unavailable 一律写 review，不冒充回转中心。给了 base_extents 时再做坐标
    同源闸门：塔吊中心落在底图范围 + 余量之外，判 different_source，拒绝正式
    覆盖（常见于塔吊图与总图不同原点，单位都写 m 也不能直接叠加）。
    """
    cranes: List[Dict[str, Any]] = []
    sources: List[Dict[str, Any]] = []
    gate_extents = list(base_extents) if isinstance(base_extents, (list, tuple)) and len(base_extents) >= 4 else None
    margin = _coordinate_margin(gate_extents) if gate_extents else None
    for path in paths or []:
        data, sha = load_json(path, "塔吊识图文件")
        rows = data.get("crane_layout") or data.get("cranes") or data.get("towers")
        if not isinstance(rows, list):
            raise SitePlanError(f"塔吊文件缺 crane_layout[]：{path}")
        contract = data.get("contract") if isinstance(data.get("contract"), dict) else {}
        units = data.get("units") if isinstance(data.get("units"), dict) else {}
        basis = str(units.get("basis") or "")
        reviews: List[Dict[str, Any]] = []
        accepted = 0
        rejected = 0
        for index, raw in enumerate(rows):
            if not isinstance(raw, dict):
                continue
            crane_id = str(raw.get("crane_id") or raw.get("id") or f"TC-{index + 1}")
            center = raw.get("center_xy_m")
            status = str(raw.get("center_status") or "")
            if not isinstance(center, (list, tuple)) or len(center) < 2:
                reviews.append({
                    "crane_id": crane_id,
                    "model": str(raw.get("model") or ""),
                    "center_status": status or "missing",
                    "reason": "missing_center",
                    "candidate_only": True,
                })
                continue
            if status != "insert_point":
                reviews.append({
                    "crane_id": crane_id,
                    "model": str(raw.get("model") or ""),
                    "center_status": status or "missing",
                    "center_xy_m": [float(center[0]), float(center[1])],
                    "reason": "center_not_insert_point",
                    "candidate_only": True,
                })
                continue
            if basis and basis != "explicit":
                raise UnitError(
                    f"{path} 的 units.basis={basis!r}：reader 未确认单位，不能把 center_xy_m 当已确认米制"
                )
            center_mm = [float(center[0]) * 1000.0, float(center[1]) * 1000.0]
            if gate_extents is not None and not _inside_extents(center_mm, gate_extents, float(margin or 0.0)):
                rejected += 1
                reviews.append({
                    "crane_id": crane_id,
                    "model": str(raw.get("model") or ""),
                    "center_status": status,
                    "center_xy_m": [float(center[0]), float(center[1])],
                    "reason": "different_source",
                    "message": "塔吊坐标不在底图范围及余量内，疑似与总图不同原点；拒绝正式覆盖，只留复核",
                    "candidate_only": True,
                })
                continue
            accepted += 1
            jib = raw.get("jib_length_m") or raw.get("jib_m")
            cranes.append({
                "id": crane_id,
                "model": str(raw.get("model") or ""),
                "center_mm": center_mm,
                "jib_mm": float(jib) * 1000.0 if jib not in (None, "") else None,
                "rotation_deg": raw.get("rotation_deg"),
                # 塔吊默认只服务主体结构阶段；如项目需跨阶段使用，在输入里显式写 active_stages
                "active_stages": _stage_list(raw.get("active_stages", raw.get("stages")),
                                             crane_id) if raw.get("active_stages") is not None
                else ["structure"],
                "source": str(path),
            })
        if gate_extents is None:
            gate_status = "not_checked"
        elif rejected and not accepted:
            gate_status = "different_source"
        elif rejected:
            gate_status = "partial_different_source"
        else:
            gate_status = "same_source"
        sources.append({
            "path": str(Path(path).expanduser().resolve()),
            "sha256": sha,
            "contract_id": str(contract.get("contract_id") or data.get("contract_id") or ""),
            "source_sha256": str(contract.get("source_sha256") or data.get("source_sha256") or ""),
            "coordinate_gate": {
                "status": gate_status,
                "base_extents_mm": gate_extents,
                "margin_mm": round(float(margin), 3) if margin is not None else None,
                "accepted": accepted,
                "rejected": rejected,
            },
            "reviews": reviews,
        })
    return cranes, sources


def load_base_map(path: str | Path) -> Tuple[Dict[str, Any], str]:
    data, sha = load_json(path, "底图 base-map")
    schema = str(data.get("schema") or "")
    if schema != "site-layout-base-map/v1":
        raise SitePlanError(f"底图 schema={schema!r}；请先跑 prepare_site.py 生成 site-layout-base-map/v1")
    if str(data.get("coord_unit") or "") != "mm":
        raise UnitError("底图 coord_unit 必须是 mm；请重跑 prepare_site.py")
    return data, sha


# ------------------------------------------------------------------ 组装
def build_stage_model(
    base_map: Dict[str, Any],
    facilities: List[Dict[str, Any]],
    cranes: List[Dict[str, Any]],
    stage: str,
    *,
    project: str = "",
    params: Optional[Dict[str, float]] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if stage not in STAGE_ORDER:
        raise SitePlanError(f"未知阶段 {stage!r}；只接受 {list(STAGES)}")
    p = dict(DEFAULT_PARAMS)
    if params:
        for key, value in params.items():
            if key in p:
                p[key] = _f(value, f"rule_params.{key}")
    redline = base_map.get("redline")
    redline_pts: List[Tuple[float, float]] = []
    if isinstance(redline, list) and len(redline) >= 3:
        redline_pts = [_pt(item, "base_map.redline") for item in redline]
    active: List[Dict[str, Any]] = []
    inactive: List[Dict[str, Any]] = []
    for item in facilities:
        row = dict(item)
        row["active"] = stage in item["active_stages"]
        (active if row["active"] else inactive).append(row)
    active_cranes = [dict(item) for item in cranes
                     if stage in (item.get("active_stages") or STAGES)]
    inactive_cranes = [dict(item) for item in cranes
                       if stage not in (item.get("active_stages") or STAGES)]
    model = {
        "schema": MODEL_SCHEMA,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "stage": stage,
        "stage_name": STAGE_NAMES[stage],
        "project": project or str(base_map.get("project") or ""),
        "coord_unit": "mm",
        "redline": [[round(x, 3), round(y, 3)] for x, y in redline_pts],
        "redline_closed": bool(base_map.get("redline_closed")),
        "redline_area_m2": base_map.get("redline_area_m2"),
        "extents_mm": base_map.get("extents_mm"),
        "structure_outline": base_map.get("structure_outline") or [],
        "wind": (context or {}).get("wind") or base_map.get("wind") or {},
        "facilities": active,
        "inactive_facilities": inactive,
        "cranes": active_cranes,
        "inactive_cranes": inactive_cranes,
        "rule_params": p,
        "checks": [],
        "warnings": [],
        "final_check": False,
    }
    model["checks"] = run_checks(model)
    summary = {"pass": 0, "fail": 0, "manual": 0}
    for check in model["checks"]:
        summary[check["status"]] += 1
    model["summary"] = summary
    model["counts"] = {
        "all": len(facilities),
        "active": len(active),
        "inactive": len(inactive),
        "by_category": _count_categories(active),
    }
    return model


def _count_categories(rows: Iterable[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row["category"]] = counts.get(row["category"], 0) + 1
    return dict(sorted(counts.items()))


def _check(cid: int, name: str, status: str, basis: str, message: str,
           evidence: Optional[Dict[str, Any]] = None, source: str = "") -> Dict[str, Any]:
    return {
        "id": cid,
        "name": name,
        "status": status,
        "basis": basis,
        "source": source,
        "message": message,
        "evidence": evidence or {},
        "final_check": False,
    }


def _centroid(row: Dict[str, Any]) -> Optional[Tuple[float, float]]:
    points = row["geometry"]["points_mm"]
    if not points:
        return None
    if row["geometry"]["type"] == "point":
        return points[0]
    if row["geometry"]["type"] == "area" and len(points) >= 3:
        # 工程坐标常达 5e8/4e9 级，直接做叉积会出现大数相消，重心可偏移数千米。
        # 先平移到首点邻域做面积/重心，再平移回原坐标。
        ox, oy = points[0][0], points[0][1]
        local = [(x - ox, y - oy) for x, y in points]
        signed = sum(
            local[i][0] * local[(i + 1) % len(local)][1]
            - local[(i + 1) % len(local)][0] * local[i][1]
            for i in range(len(local))
        ) / 2.0
        if abs(signed) > 1e-9:
            cx = sum(
                (local[i][0] + local[(i + 1) % len(local)][0])
                * (local[i][0] * local[(i + 1) % len(local)][1]
                   - local[(i + 1) % len(local)][0] * local[i][1])
                for i in range(len(local))
            ) / (6.0 * signed)
            cy = sum(
                (local[i][1] + local[(i + 1) % len(local)][1])
                * (local[i][0] * local[(i + 1) % len(local)][1]
                   - local[(i + 1) % len(local)][0] * local[i][1])
                for i in range(len(local))
            ) / (6.0 * signed)
            return cx + ox, cy + oy
    return (sum(p[0] for p in points) / len(points), sum(p[1] for p in points) / len(points))


def _by_category(rows: Sequence[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
    return [row for row in rows if row["category"] == category]


def _by_categories(rows: Sequence[Dict[str, Any]],
                   categories: Sequence[str]) -> List[Dict[str, Any]]:
    wanted = set(categories)
    return [row for row in rows if row["category"] in wanted]


def _segment_segment_distance_mm(a1: Sequence[float], a2: Sequence[float],
                                 b1: Sequence[float], b2: Sequence[float]) -> float:
    if _segments_cross(a1, a2, b1, b2):
        return 0.0
    return min(
        _point_segment_distance(a1, b1, b2),
        _point_segment_distance(a2, b1, b2),
        _point_segment_distance(b1, a1, a2),
        _point_segment_distance(b2, a1, a2),
    )


def _polygon_distance_mm(poly_a: Sequence[Sequence[float]],
                         poly_b: Sequence[Sequence[float]]) -> float:
    """两个多边形的最小边界距离；相交或包含返回 0。"""
    if len(poly_a) < 3 or len(poly_b) < 3:
        return float("inf")
    if point_in_polygon(poly_a[0], poly_b, 1.0) or point_in_polygon(poly_b[0], poly_a, 1.0):
        return 0.0
    best = float("inf")
    for i in range(len(poly_a)):
        a1 = poly_a[i]
        a2 = poly_a[(i + 1) % len(poly_a)]
        for j in range(len(poly_b)):
            b1 = poly_b[j]
            b2 = poly_b[(j + 1) % len(poly_b)]
            best = min(best, _segment_segment_distance_mm(a1, a2, b1, b2))
    return best


def _row_polygon(row: Dict[str, Any]) -> List[Tuple[float, float]]:
    return [(float(p[0]), float(p[1])) for p in row["geometry"]["points_mm"]]


def _row_distance_mm(row_a: Dict[str, Any], row_b: Dict[str, Any]) -> float:
    """区域/点行间最小距离；点按极短线段处理，避免中心距冒充净距。"""
    poly_a = _row_polygon(row_a)
    poly_b = _row_polygon(row_b)
    if row_a["geometry"]["type"] == "point" and row_b["geometry"]["type"] == "point":
        return _dist(poly_a[0], poly_b[0])
    if row_a["geometry"]["type"] == "point":
        return min(_point_segment_distance(poly_a[0], poly_b[i], poly_b[(i + 1) % len(poly_b)])
                   for i in range(len(poly_b))) if len(poly_b) >= 2 else _dist(poly_a[0], poly_b[0])
    if row_b["geometry"]["type"] == "point":
        return min(_point_segment_distance(poly_b[0], poly_a[i], poly_a[(i + 1) % len(poly_a)])
                   for i in range(len(poly_a))) if len(poly_a) >= 2 else _dist(poly_b[0], poly_a[0])
    return _polygon_distance_mm(poly_a, poly_b)


def _polygon_inside(inner: Sequence[Sequence[float]],
                    outer: Sequence[Sequence[float]]) -> bool:
    return bool(inner) and all(point_in_polygon(p, outer, 5.0) for p in inner)


def _line_crosses_polygon(line: Sequence[Sequence[float]],
                          polygon: Sequence[Sequence[float]]) -> bool:
    if len(line) < 2 or len(polygon) < 3:
        return False
    for i in range(len(line) - 1):
        a, b = line[i], line[i + 1]
        if point_in_polygon(a, polygon, 1.0) or point_in_polygon(b, polygon, 1.0):
            return True
        for j in range(len(polygon)):
            c = polygon[j]
            d = polygon[(j + 1) % len(polygon)]
            if _segments_cross(a, b, c, d):
                return True
    return False


def _point_polygon_distance_mm(point: Sequence[float],
                               polygon: Sequence[Sequence[float]]) -> float:
    if point_in_polygon(point, polygon, 1.0):
        return 0.0
    return min((_point_segment_distance(point, polygon[i], polygon[(i + 1) % len(polygon)])
                for i in range(len(polygon))), default=float("inf"))


def _line_polygon_distance_mm(line: Sequence[Sequence[float]],
                              polygon: Sequence[Sequence[float]]) -> float:
    if _line_crosses_polygon(line, polygon):
        return 0.0
    best = float("inf")
    for i in range(len(line) - 1):
        a1, a2 = line[i], line[i + 1]
        for j in range(len(polygon)):
            b1 = polygon[j]
            b2 = polygon[(j + 1) % len(polygon)]
            best = min(best, _segment_segment_distance_mm(a1, a2, b1, b2))
    return best


def _wind_evidence(model: Dict[str, Any]) -> Dict[str, Any]:
    wind = model.get("wind")
    return wind if isinstance(wind, dict) else {}


def _checks_site_and_roads(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    """用地红线、设施落界与道路宽度/连通（规则 1-4）。"""
    checks: List[Dict[str, Any]] = []
    p = model["rule_params"]
    rows = model["facilities"]
    redline = model["redline"]
    # 1 红线闭合
    checks.append(_check(
        1, "用地红线闭合", "pass" if model["redline_closed"] else "fail", "规范",
        "红线闭合，面积 {:.1f} m²".format(model.get("redline_area_m2") or 0.0)
        if model["redline_closed"] else "红线未闭合，不能作为用地边界出正式布置图",
        {"redline_closed": model["redline_closed"],
         "redline_area_m2": model.get("redline_area_m2"),
         "vertices": len(redline)},
    ))
    # 2 设施锚点在红线内
    if redline:
        outside = []
        for row in rows:
            if row["category"] in ("site_boundary_neighbor", "permanent_road"):
                continue
            center = _centroid(row)
            if center and not point_in_polygon(center, redline, 50.0):
                outside.append({"id": row["id"], "category": row["category"],
                                "center_mm": [round(center[0], 3), round(center[1], 3)]})
        checks.append(_check(
            2, "设施锚点位于红线内", "fail" if outside else "pass", "规范",
            "{} 个设施锚点在红线外".format(len(outside)) if outside else "全部设施锚点位于红线内",
            {"outside_count": len(outside), "outside": outside[:20],
             "tested": len(rows) - len(_by_category(rows, "site_boundary_neighbor"))},
        ))
    else:
        checks.append(_check(2, "设施锚点位于红线内", "manual", "规范",
                             "底图没有红线，无法判断设施是否在用地内", {}))
    # 3 车道宽度
    narrow = []
    tested = 0
    for row in rows:
        if row["category"] not in ("temporary_road", "fire_access", "permanent_road"):
            continue
        width = row["width_mm"]
        if width is None and row["category"] == "temporary_road":
            width = p["temporary_road_default_width_m"] * 1000.0
        if width is None:
            continue
        tested += 1
        limit = p["fire_lane_min_width_m"] if row["category"] == "fire_access" else p["road_min_width_m"]
        if width < limit * 1000.0 - 1e-6:
            narrow.append({"id": row["id"], "category": row["category"],
                           "width_m": round(width / 1000.0, 3), "min_m": limit})
    checks.append(_check(
        3, "道路/消防车道宽度", "fail" if narrow else ("pass" if tested else "manual"), "规范",
        "{} 条道路宽度不足".format(len(narrow)) if narrow else
        ("宽度均满足（临时道路未标宽度按 {} m 计）".format(p["temporary_road_default_width_m"])
         if tested else "设施文件未提供道路宽度，无法校核"),
        {"tested": tested, "narrow": narrow,
         "fire_lane_min_m": p["fire_lane_min_width_m"],
         "road_min_m": p["road_min_width_m"],
         "default_temporary_m": p["temporary_road_default_width_m"]},
        "GB 50720 施工现场临时建筑物技术规范（消防车道净宽不小于 4 m，净高不小于 4 m；净高需现场复核）",
    ))
    # 4 消防车道连通：端点 2 m 内串接，且至少一条与出入口相连
    lane_rows = _by_category(rows, "fire_access") + _by_category(rows, "temporary_road")
    components = _components(lane_rows, p["connect_tolerance_m"] * 1000.0)
    gates = _by_category(rows, "site_access")
    gate_linked = False
    for comp in components:
        comp_points = [pt for row in comp for pt in row["geometry"]["points_mm"]]
        for gate in gates:
            gate_pt = _centroid(gate)
            if gate_pt and any(_dist(gate_pt, pt) <= p["connect_tolerance_m"] * 1000.0 * 5
                               for pt in comp_points):
                gate_linked = True
        if len(comp) >= 2:
            pass
    status = "fail" if (lane_rows and gates and not gate_linked) else ("manual" if not gates else "pass")
    checks.append(_check(
        4, "临时道路/消防车道连通", status, "规范",
        "道路未与出入口连通" if status == "fail" else
        ("缺出入口，无法判断连通" if status == "manual" else
         "道路分 {} 段，已与出入口连通（按端点 2 m 容差）".format(len(components))),
        {"segments": len(lane_rows), "components": len(components),
         "gate_linked": gate_linked,
         "component_sizes": [len(c) for c in components],
         "tolerance_m": p["connect_tolerance_m"]},
        "GB 50720；消防车道应环形或与外部道路连通",
    ))
    return checks

def _checks_fire_and_crane(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    """消防与塔吊安全距离（规则 5-6）。"""
    checks: List[Dict[str, Any]] = []
    p = model["rule_params"]
    rows = model["facilities"]
    redline = model["redline"]
    # 5 消火栓间距与保护半径（以场地四角作最不利点代理）
    hydrants = _by_category(rows, "fire_hydrant")
    spacing = []
    centers = [(row, _centroid(row)) for row in hydrants]
    centers = [(row, c) for row, c in centers if c]
    if len(centers) >= 2:
        # 只比较环向相邻点：环形布置的对角消火栓直线距离天然超过 120 m，
        # 旧算法把任意两点都比一遍，大场地必然误判 fail。
        cx = sum(c[0] for _, c in centers) / len(centers)
        cy = sum(c[1] for _, c in centers) / len(centers)
        ordered = sorted(centers, key=lambda item: math.atan2(item[1][1] - cy, item[1][0] - cx))
        for i in range(len(ordered)):
            row_a, a = ordered[i]
            row_b, b = ordered[(i + 1) % len(ordered)]
            spacing.append((_dist(a, b) / 1000.0, row_a["id"], row_b["id"]))
    far = []
    if hydrants and model.get("extents_mm"):
        x0, y0, x1, y1 = model["extents_mm"]
        corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for corner in corners:
            best = min((_dist(_centroid(h), corner) / 1000.0 for h in hydrants if _centroid(h)),
                       default=None)
            far.append({"corner_mm": [round(corner[0], 1), round(corner[1], 1)],
                        "nearest_m": None if best is None else round(best, 1)})
    spacing_bad = [item for item in spacing if item[0] > p["hydrant_max_spacing_m"]]
    radius_bad = [item for item in far if item["nearest_m"] is None
                  or item["nearest_m"] > p["hydrant_max_radius_m"]]
    if not hydrants:
        status5 = "manual"
        msg5 = "未识别/未提供消火栓，无法校核间距与保护半径"
    elif spacing_bad or radius_bad:
        status5 = "fail"
        msg5 = "消火栓间距或保护半径超限"
    else:
        status5 = "pass"
        msg5 = "消火栓间距 ≤ {} m，场地四角均在 {} m 内".format(
            p["hydrant_max_spacing_m"], p["hydrant_max_radius_m"])
    checks.append(_check(
        5, "消火栓间距与保护半径", status5, "规范", msg5,
        {"hydrants": [h["id"] for h in hydrants], "pairs": len(spacing),
         "max_spacing_m": round(max((s[0] for s in spacing), default=0.0), 1),
         "spacing_over": spacing_bad, "corner_distances": far,
         "radius_over": radius_bad,
         "spacing_method": "环向相邻点（绕场地质心极角排序），非任意两点直线距离",
         "limits_m": {"spacing": p["hydrant_max_spacing_m"], "radius": p["hydrant_max_radius_m"]},
         "note": "以用地四角作最不利点代理；实际应按在建工程最远点复核"},
        "GB 50720：消火栓间距不应大于 120 m，保护半径不应大于 150 m",
    ))
    # 6 宿舍/办公/加工区是否落在塔吊回转半径内
    risky = []
    for row in rows:
        # 加工区常主动布置在塔吊覆盖内（便于吊运），不属于"人员密集临建"；
        # 这里只校核宿舍、办公与食堂等固定人员停留场所。
        if row["category"] not in QUIET_CATEGORIES:
            continue
        center = _centroid(row)
        if not center:
            continue
        for crane in model["cranes"]:
            if not crane.get("jib_mm"):
                continue
            distance = _dist(center, crane["center_mm"])
            if distance <= crane["jib_mm"]:
                risky.append({"facility": row["id"], "category": row["category"],
                              "crane": crane["id"],
                              "distance_m": round(distance / 1000.0, 1),
                              "jib_m": round(crane["jib_mm"] / 1000.0, 1)})
    if not model["cranes"] and model.get("inactive_cranes"):
        status6, msg6 = "pass", "本阶段塔吊已退出（active_stages 不含本阶段），不适用"
    elif not model["cranes"]:
        status6, msg6 = "manual", "未提供塔吊识图结果，无法判断临建是否在回转半径内"
    elif risky:
        status6, msg6 = "fail", "{} 处人员密集临建落在塔吊回转半径内".format(len(risky))
    else:
        status6, msg6 = "pass", "宿舍、办公区、食堂等临建均不在塔吊回转半径内"
    checks.append(_check(
        6, "宿舍/办公避开塔吊回转范围", status6, "规范", msg6,
        {"risky": risky, "cranes": [c["id"] for c in model["cranes"]]},
        "JGJ 59 建筑施工安全检查标准：塔吊回转范围内不得设置宿舍等人员密集临建",
    ))
    return checks

def _checks_power_and_processing(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    """临电距离与加工区通用隔离（规则 7-8）。"""
    checks: List[Dict[str, Any]] = []
    p = model["rule_params"]
    rows = model["facilities"]
    redline = model["redline"]
    # 7 配电室/一级箱距离
    rooms = _by_category(rows, "distribution_room")
    boxes = _by_category(rows, "primary_distribution_box")
    loads = [r for r in rows if r["category"] in
             PROCESSING_CATEGORIES + ("tower_crane", "construction_elevator")]
    room_box_far, box_load_far = [], []
    for box in boxes:
        b = _centroid(box)
        if not b:
            continue
        if rooms:
            nearest = min((_dist(b, _centroid(r)) / 1000.0 for r in rooms if _centroid(r)),
                          default=None)
            if nearest is not None and nearest > p["box_to_room_max_m"]:
                room_box_far.append({"box": box["id"], "nearest_room_m": round(nearest, 1)})
        if loads:
            nearest = min((_dist(b, _centroid(r)) / 1000.0 for r in loads if _centroid(r)),
                          default=None)
            if nearest is not None and nearest > p["box_to_load_max_m"]:
                box_load_far.append({"box": box["id"], "nearest_load_m": round(nearest, 1)})
    if not boxes:
        status7, msg7 = "manual", "未提供一级配电箱，无法校核供电距离"
    elif room_box_far or box_load_far:
        status7, msg7 = "manual", "一级箱距离超经验值，需电气专业复核压降与线路敷设"
    else:
        status7, msg7 = "pass", "一级箱至配电室 ≤ {} m、至用电区 ≤ {} m（经验值）".format(
            p["box_to_room_max_m"], p["box_to_load_max_m"])
    checks.append(_check(
        7, "配电室/一级箱供电距离", status7, "经验", msg7,
        {"boxes": [b["id"] for b in boxes], "rooms": [r["id"] for r in rooms],
         "room_far": room_box_far, "load_far": box_load_far,
         "limits_m": {"box_to_room": p["box_to_room_max_m"],
                      "box_to_load": p["box_to_load_max_m"]}},
        "经验值，非规范强制；最终以临电专项方案与电压损失计算为准",
    ))
    # 8 加工区与办公/宿舍分离
    work = [row for row in rows if row["category"] in PROCESSING_CATEGORIES]
    quiet = _by_categories(rows, QUIET_CATEGORIES)
    too_close = []
    for w in work:
        wc = _centroid(w)
        for q in quiet:
            qc = _centroid(q)
            if wc and qc:
                distance = _dist(wc, qc) / 1000.0
                if distance < p["processing_separation_m"]:
                    too_close.append({"processing": w["id"], "quiet": q["id"],
                                      "distance_m": round(distance, 1)})
    required_categories = set(REQUIRED_BY_STAGE.get(model["stage"], ()))
    if not work and not (set(PROCESSING_CATEGORIES) & required_categories):
        status8, msg8 = "pass", "本阶段未设加工区，不适用"
    elif not work or not quiet:
        status8, msg8 = "manual", "缺加工区或办公/宿舍，无法判断噪声与粉尘隔离"
    elif too_close:
        status8, msg8 = "manual", "加工区与办公/宿舍距离小于 {} m，需复核噪声粉尘影响".format(
            p["processing_separation_m"])
    else:
        status8, msg8 = "pass", "加工区与办公/宿舍间距满足经验值"
    checks.append(_check(
        8, "加工区与办公/宿舍分离", status8, "经验", msg8,
        {"pairs": too_close, "min_m": p["processing_separation_m"]},
    ))
    return checks

def _checks_living_and_compliance(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    """九牌一图、垃圾池、永临结合与周边（规则 9-12）。"""
    checks: List[Dict[str, Any]] = []
    p = model["rule_params"]
    rows = model["facilities"]
    redline = model["redline"]
    quiet = _by_categories(rows, QUIET_CATEGORIES)
    required_categories = set(REQUIRED_BY_STAGE.get(model["stage"], ()))
    # 9 九牌一图/宣讲台靠近大门
    gate = _by_category(rows, "site_access")
    boards = _by_category(rows, "notice_board") + _by_category(rows, "safety_podium")
    far_boards = []
    for board in boards:
        bc = _centroid(board)
        if not bc or not gate:
            continue
        nearest = min((_dist(bc, _centroid(g)) / 1000.0 for g in gate if _centroid(g)),
                      default=None)
        if nearest is not None and nearest > p["notice_to_gate_m"]:
            far_boards.append({"facility": board["id"], "nearest_gate_m": round(nearest, 1)})
    if not boards:
        status9, msg9 = "manual", "未提供九牌一图/安全宣讲台"
    elif not gate:
        status9, msg9 = "manual", "缺出入口，无法判断九牌一图位置"
    elif far_boards:
        status9, msg9 = "manual", "九牌一图/宣讲台距大门超过 {} m，需复核可见性".format(
            p["notice_to_gate_m"])
    else:
        status9, msg9 = "pass", "九牌一图/宣讲台位于大门 {} m 范围内".format(p["notice_to_gate_m"])
    notice_rows = _by_category(rows, "notice_board")
    layouts = []
    for board in notice_rows:
        attrs = board.get("attrs") if isinstance(board.get("attrs"), dict) else {}
        layouts.append({"id": board["id"], "layout": attrs.get("layout"),
                        "board_count": attrs.get("board_count"),
                        "total_length_m": attrs.get("total_length_m")})
    linear_bad = [item for item in layouts
                  if (item["layout"] is not None and item["layout"] != "linear")
                  or (item["board_count"] is not None and int(item["board_count"]) < 9)]
    if notice_rows and linear_bad:
        status9, msg9 = "manual", "九牌一图未按 9 块直线排布，需确认板数与朝向"
    elif notice_rows and all(item["layout"] == "linear" for item in layouts):
        first = layouts[0]
        msg9 = "九牌一图 {} 块直线排布（{} m），位于大门 {} m 范围内".format(
            first["board_count"] or 9, first["total_length_m"] or "?", p["notice_to_gate_m"])
    checks.append(_check(
        9, "九牌一图/安全宣讲台位置", status9, "经验", msg9,
        {"facilities": [b["id"] for b in boards], "gates": [g["id"] for g in gate],
         "farther": far_boards, "limit_m": p["notice_to_gate_m"], "layouts": layouts},
    ))
    # 10 垃圾池与办公/宿舍距离
    waste = _by_category(rows, "waste_pool")
    near_waste = []
    for w in waste:
        wc = _centroid(w)
        for q in quiet:
            qc = _centroid(q)
            if wc and qc:
                distance = _dist(wc, qc) / 1000.0
                if distance < p["waste_separation_m"]:
                    near_waste.append({"waste": w["id"], "quiet": q["id"],
                                       "distance_m": round(distance, 1)})
    if not waste and "waste_pool" not in required_categories:
        status10, msg10 = "pass", "本阶段未设垃圾池，不适用"
    elif not waste:
        status10, msg10 = "manual", "未提供垃圾池，无法校核卫生间距"
    elif near_waste:
        status10, msg10 = "manual", "垃圾池距办公/宿舍小于 {} m，需复核朝向与封闭措施".format(
            p["waste_separation_m"])
    else:
        status10, msg10 = "pass", "垃圾池与办公/宿舍间距满足经验值"
    checks.append(_check(
        10, "垃圾池卫生间距", status10, "经验", msg10,
        {"pairs": near_waste, "min_m": p["waste_separation_m"]},
    ))
    # 11 永临结合：临时道路沿永久道路比例
    temp = _by_category(rows, "temporary_road")
    perm = _by_category(rows, "permanent_road")
    ratio = None
    if temp and perm:
        samples = []
        for row in temp:
            samples.extend(_sample_polyline(row["geometry"]["points_mm"],
                                            p["road_overlap_sample_m"] * 1000.0))
        perm_lines = [row["geometry"]["points_mm"] for row in perm]
        hit = 0
        for point in samples:
            if any(_point_segment_distance(point, line[i], line[i + 1])
                   <= p["road_overlap_tolerance_m"] * 1000.0
                   for line in perm_lines for i in range(len(line) - 1)):
                hit += 1
        ratio = (hit / len(samples)) if samples else None
    if ratio is None:
        status11, msg11 = "manual", "缺临时道路或永久道路，无法评估永临结合"
    elif ratio < p["road_overlap_min_ratio"]:
        status11, msg11 = "manual", "临时道路沿永久道路比例 {:.0%}，低于 {}%，建议优化永临结合".format(
            ratio, p["road_overlap_min_ratio"])
    else:
        status11, msg11 = "pass", "临时道路沿永久道路比例 {:.0%}".format(ratio)
    checks.append(_check(
        11, "永久道路与临时道路结合", status11, "经验", msg11,
        {"overlap_ratio": None if ratio is None else round(ratio, 3),
         "min_ratio": p["road_overlap_min_ratio"],
         "sample_step_m": p["road_overlap_sample_m"],
         "tolerance_m": p["road_overlap_tolerance_m"]},
    ))
    # 12 相邻地貌证据
    neighbor = _by_category(rows, "site_boundary_neighbor")
    checks.append(_check(
        12, "相邻地貌/周边条件", "pass" if neighbor else "manual", "经验",
        "已提供相邻地貌 {} 项".format(len(neighbor)) if neighbor
        else "未见相邻地貌/周边条件；需现场踏勘补高差、边坡、既有建筑与市政接口",
        {"items": [row["id"] for row in neighbor],
         "required": ["周边道路标高", "相邻建筑/边坡", "市政水电接口", "排水去向"]},
    ))
    return checks

def _checks_completeness(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    """阶段必备、几何冲突与消防净空（规则 13-15）。"""
    checks: List[Dict[str, Any]] = []
    p = model["rule_params"]
    rows = model["facilities"]
    redline = model["redline"]
    # 13 阶段必备设施
    required = REQUIRED_BY_STAGE[model["stage"]]
    present = {row["category"] for row in rows}
    # 加工区拆分为钢筋/木工/砂浆后，任一存在即视为满足 processing_zone 必备项
    processing_present = sorted(present & set(PROCESSING_CATEGORIES))
    if processing_present:
        present.add("processing_zone")
    if model["cranes"]:
        present.add("tower_crane")
    missing = [item for item in required if item not in present]
    checks.append(_check(
        13, "阶段必备设施齐全", "fail" if missing else "pass", "规范",
        "缺：" + "、".join(meta(item)["zh"] for item in missing) if missing
        else "{} 必备设施齐全".format(model["stage_name"]),
        {"required": list(required), "present": sorted(present),
         "processing_present": processing_present,
         "missing": [{"category": item, "name": meta(item)["zh"]} for item in missing]},
    ))
    # 14 阶段间/设施间几何冲突
    conflicts = []
    area_rows = [row for row in rows if row["geometry"]["type"] == "area"]

    def parent_child(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
        attrs_a = a.get("attrs") if isinstance(a.get("attrs"), dict) else {}
        attrs_b = b.get("attrs") if isinstance(b.get("attrs"), dict) else {}
        return (attrs_a.get("parent_id") == b.get("id")
                or attrs_b.get("parent_id") == a.get("id"))

    for i in range(len(area_rows)):
        for j in range(i + 1, len(area_rows)):
            a, b = area_rows[i], area_rows[j]
            # 工人生活区内的食堂/淋浴/晾晒子块天然落在父区域内，不是几何冲突；
            # 父子关系必须由 attrs.parent_id 明确声明，不能靠包含关系猜。
            if parent_child(a, b):
                continue
            if _polylines_intersect(a["geometry"]["points_mm"] + [a["geometry"]["points_mm"][0]],
                                    b["geometry"]["points_mm"] + [b["geometry"]["points_mm"][0]]):
                conflicts.append({"a": a["id"], "b": b["id"],
                                  "a_category": a["category"], "b_category": b["category"]})
    # 道路才按“占地冲突”判；临水临电、消防水管等管线允许埋地穿越区域，
    # 共线消防车道（attrs.shared_with）不重复报，避免一条环道报两次。
    conflict_lines = [row for row in rows if row["geometry"]["type"] == "line"
                      and row["category"] in ("temporary_road", "fire_access", "permanent_road")]
    # 洗车台/地磅按功能必须跨路或压路布置，不按“设施压路”报冲突；
    # 其与道路的贴合关系由规则 22 单独校核。
    road_embedded = {"wheel_wash", "weighbridge"}
    seen_pairs = set()
    for line in conflict_lines:
        attrs = line.get("attrs") if isinstance(line.get("attrs"), dict) else {}
        if attrs.get("shared_with"):
            continue
        points = line["geometry"]["points_mm"]
        for area in area_rows:
            if area["category"] in road_embedded:
                continue
            key = (line["id"], area["id"])
            if key in seen_pairs:
                continue
            poly = area["geometry"]["points_mm"] + [area["geometry"]["points_mm"][0]]
            if _polylines_intersect(points, poly):
                seen_pairs.add(key)
                conflicts.append({"a": line["id"], "b": area["id"],
                                  "a_category": line["category"], "b_category": area["category"]})
    checks.append(_check(
        14, "设施几何冲突", "manual" if conflicts else "pass", "经验",
        "{} 处设施边界相交，需确认是否允许（如道路穿越堆场）".format(len(conflicts))
        if conflicts else "未发现设施边界相交",
        {"conflicts": conflicts[:30], "tested_area": len(area_rows), "tested_line": len(conflict_lines)},
    ))
    # 15 消防车道净空
    fire = _by_category(rows, "fire_access")
    checks.append(_check(
        15, "消防车道净空", "manual" if fire else "manual", "规范",
        "平面图无法判断净高与架体/塔吊回转是否侵占净空，需剖面或现场复核",
        {"fire_lanes": [row["id"] for row in fire], "required_clear_height_m": 4.0},
        "GB 50720：消防车道净高不小于 4 m",
    ))
    return checks


def _checks_new_facilities(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    """0.6.0 新增：加工区三类分项隔离、消防泵房/水池、变压器、排水沟；
    0.6.7 增加出入口洗车/称重组织（规则 16-22）。"""
    checks: List[Dict[str, Any]] = []
    p = model["rule_params"]
    rows = model["facilities"]
    quiet = _by_categories(rows, QUIET_CATEGORIES)

    def separation_pairs(work: Sequence[Dict[str, Any]], others: Sequence[Dict[str, Any]],
                         limit_m: float, left_key: str, right_key: str) -> List[Dict[str, Any]]:
        found = []
        for w in work:
            wc = _centroid(w)
            for o in others:
                oc = _centroid(o)
                if wc and oc:
                    distance = _dist(wc, oc) / 1000.0
                    if distance < limit_m:
                        found.append({left_key: w["id"], right_key: o["id"],
                                      "distance_m": round(distance, 1)})
        return found

    # 16 钢筋加工区与办公/宿舍分离
    steel = _by_category(rows, "steel_processing")
    steel_close = separation_pairs(steel, quiet, p["steel_processing_separation_m"],
                                   "processing", "quiet")
    if not steel:
        status16, msg16 = "pass", "本阶段未设钢筋加工区，不适用"
    elif not quiet:
        status16, msg16 = "manual", "缺办公区/宿舍，无法判断钢筋加工区隔离"
    elif steel_close:
        status16, msg16 = "manual", "钢筋加工区距办公/宿舍小于 {} m，需复核噪声影响".format(
            p["steel_processing_separation_m"])
    else:
        status16, msg16 = "pass", "钢筋加工区与办公/宿舍间距满足经验值"
    checks.append(_check(
        16, "钢筋加工区隔离", status16, "经验", msg16,
        {"pairs": steel_close, "min_m": p["steel_processing_separation_m"],
         "facilities": [row["id"] for row in steel]},
        "经验值；钢筋切断/弯曲噪声与短料飞溅需现场复核",
    ))

    # 17 木工加工区：人员隔离 + 与配电设施/变压器的防火间距
    wood = _by_category(rows, "wood_processing")
    wood_close = separation_pairs(wood, quiet, p["wood_processing_separation_m"],
                                  "processing", "quiet")
    power_rows = (_by_category(rows, "distribution_room")
                  + _by_category(rows, "primary_distribution_box")
                  + _by_category(rows, "transformer"))
    wood_fire = separation_pairs(wood, power_rows, p["wood_to_power_min_m"],
                                 "processing", "power")
    if not wood:
        status17, msg17 = "pass", "本阶段未设木工加工区，不适用"
    elif not quiet:
        status17, msg17 = "manual", "缺办公区/宿舍，无法判断木工加工区隔离"
    elif wood_close or wood_fire:
        status17, msg17 = "manual", "木工加工区距人员区或配电/变压器过近，需复核噪声与防火"
    else:
        status17, msg17 = "pass", "木工加工区人员隔离与防火间距满足经验值"
    checks.append(_check(
        17, "木工加工区隔离与防火", status17, "经验", msg17,
        {"pairs": wood_close, "fire_pairs": wood_fire,
         "min_m": p["wood_processing_separation_m"],
         "power_min_m": p["wood_to_power_min_m"],
         "facilities": [row["id"] for row in wood]},
        "木屑属可燃物；与配电设施、动火点的防火间距须按消防专项方案复核",
    ))

    # 18 砂浆/砌体加工区：人员隔离（扬尘为主）
    mortar = _by_category(rows, "mortar_processing")
    mortar_close = separation_pairs(mortar, quiet, p["mortar_processing_separation_m"],
                                    "processing", "quiet")
    if not mortar:
        status18, msg18 = "pass", "本阶段未设砂浆/砌体加工区，不适用"
    elif not quiet:
        status18, msg18 = "manual", "缺办公区/宿舍，无法判断砂浆加工区隔离"
    elif mortar_close:
        status18, msg18 = "manual", "砂浆/砌体加工区距办公/宿舍小于 {} m，需复核扬尘".format(
            p["mortar_processing_separation_m"])
    else:
        status18, msg18 = "pass", "砂浆/砌体加工区与办公/宿舍间距满足经验值"
    checks.append(_check(
        18, "砂浆/砌体加工区隔离", status18, "经验", msg18,
        {"pairs": mortar_close, "min_m": p["mortar_processing_separation_m"],
         "facilities": [row["id"] for row in mortar],
         "note": "搅拌扬尘受主导风向影响，本规则不含风向判断，需现场确认"},
    ))

    # 19 消防泵房与消防水池：成组、靠近消防车道
    pumps = _by_category(rows, "fire_pump_room")
    tanks = _by_category(rows, "fire_water_tank")
    lanes = _by_category(rows, "fire_access")
    tank_gaps, lane_gaps = [], []
    for pump in pumps:
        pc = _centroid(pump)
        if not pc:
            continue
        for tank in tanks:
            tc = _centroid(tank)
            if tc:
                gap = _dist(pc, tc) / 1000.0
                if gap > p["pump_to_tank_max_m"]:
                    tank_gaps.append({"pump": pump["id"], "tank": tank["id"],
                                      "distance_m": round(gap, 1)})
        for lane in lanes:
            pts = lane["geometry"]["points_mm"]
            nearest = min((_point_segment_distance(pc, pts[i], pts[i + 1])
                           for i in range(len(pts) - 1)), default=None)
            if nearest is not None and nearest / 1000.0 > p["pump_to_fire_lane_max_m"]:
                lane_gaps.append({"pump": pump["id"], "lane": lane["id"],
                                  "distance_m": round(nearest / 1000.0, 1)})
    if not pumps and not tanks:
        status19, msg19 = "manual", "未提供消防泵房与消防水池，无法校核临时消防水源"
    elif not pumps or not tanks:
        status19, msg19 = "manual", "消防泵房/消防水池缺项，临时消防水源不成组"
    elif tank_gaps or lane_gaps:
        status19, msg19 = "manual", "泵房与水池或消防车道距离超经验值，需复核取水与补水"
    else:
        status19, msg19 = "pass", "消防泵房与水池成组，且泵房在消防车道 {} m 内".format(
            p["pump_to_fire_lane_max_m"])
    checks.append(_check(
        19, "消防泵房与消防水池", status19, "经验", msg19,
        {"pumps": [row["id"] for row in pumps], "tanks": [row["id"] for row in tanks],
         "tank_gaps": tank_gaps, "lane_gaps": lane_gaps,
         "limits_m": {"pump_to_tank": p["pump_to_tank_max_m"],
                      "pump_to_fire_lane": p["pump_to_fire_lane_max_m"]},
         "note": "GB 50720 要求临时消防给水系统完整；水量与水压须按在建工程体积专项计算"},
        "GB 50720 施工现场临时消防给水系统；泵房/水池应靠近消防车道便于取水补水",
    ))

    # 20 变压器与人员密集临建、可燃堆场的安全距离
    transformers = _by_category(rows, "transformer")
    living = _by_categories(rows, QUIET_CATEGORIES)
    combustible = _by_category(rows, "wood_processing") + _by_category(rows, "material_yard")
    trans_living = separation_pairs(transformers, living, p["transformer_to_living_min_m"],
                                    "transformer", "living")
    trans_fire = separation_pairs(transformers, combustible,
                                  p["transformer_to_combustible_min_m"],
                                  "transformer", "combustible")
    if not transformers:
        status20, msg20 = "manual", "未提供变压器/箱变，无法校核安全距离"
    elif trans_living or trans_fire:
        status20, msg20 = "manual", ("变压器距人员区（<{} m）或可燃堆场（<{} m）过近，"
                                     "需电气与消防复核").format(
            p["transformer_to_living_min_m"], p["transformer_to_combustible_min_m"])
    else:
        status20, msg20 = "pass", "变压器与人员区、可燃堆场距离满足经验值"
    checks.append(_check(
        20, "变压器安全距离", status20, "经验", msg20,
        {"living_pairs": trans_living, "combustible_pairs": trans_fire,
         "limits_m": {"to_living": p["transformer_to_living_min_m"],
                      "to_combustible": p["transformer_to_combustible_min_m"]},
         "facilities": [row["id"] for row in transformers]},
        "JGJ 46 施工现场临时用电安全技术规范：变压器应设围栏与警示；距离为经验控制值",
    ))

    # 21 排水沟：连续成网并接入沉淀池/洗车池
    ditches = _by_category(rows, "drainage_ditch")
    tol_mm = p["drainage_connect_tolerance_m"] * 1000.0
    wash = _by_category(rows, "wheel_wash")
    components = _components(ditches, tol_mm) if ditches else []
    discharge = []
    for ditch in ditches:
        for pt in ditch["geometry"]["points_mm"]:
            for pit in wash:
                poly = pit["geometry"]["points_mm"]
                if point_in_polygon(pt, poly, tol_mm):
                    discharge.append({"ditch": ditch["id"], "pit": pit["id"]})
                    break
                nearest = min((_point_segment_distance(pt, poly[i], poly[(i + 1) % len(poly)])
                               for i in range(len(poly))), default=None)
                if nearest is not None and nearest <= tol_mm:
                    discharge.append({"ditch": ditch["id"], "pit": pit["id"]})
                    break
    if not ditches:
        status21, msg21 = "manual", "未提供排水沟，无法校核场地排水组织"
    elif len(components) > 1:
        status21, msg21 = "manual", "排水沟分 {} 段未连通，需补全排水路径".format(len(components))
    elif not wash:
        status21, msg21 = "manual", "排水沟连续，但本阶段无洗车池/沉淀池，排放去向需人工确认"
    elif not discharge:
        status21, msg21 = "manual", "排水沟未接入洗车池/沉淀池，需确认排放口"
    else:
        status21, msg21 = "pass", "排水沟连续成网，并接入沉淀池/洗车池"
    checks.append(_check(
        21, "排水沟连续与排放", status21, "经验", msg21,
        {"ditches": [row["id"] for row in ditches], "components": len(components),
         "discharge": discharge[:20], "tolerance_m": p["drainage_connect_tolerance_m"],
         "note": "市政排水接口、坡度与沉淀池容积须按现场竖向与环保要求复核"},
    ))

    # 22 出入口洗车/称重组织：洗车台跨接入道路、地磅贴主路且都在大门服务范围内
    wash_rows = _by_category(rows, "wheel_wash")
    scale_rows = _by_category(rows, "weighbridge")
    gate_rows = _by_category(rows, "site_access")
    road_rows = [row for row in rows if row["category"] in
                 ("temporary_road", "permanent_road", "fire_access")]

    def _distance_to_roads(center: Sequence[float]) -> Optional[float]:
        best: Optional[float] = None
        for road in road_rows:
            pts = road["geometry"]["points_mm"]
            if len(pts) < 2:
                continue
            closed = bool(road["geometry"].get("closed"))
            last = len(pts) if closed else len(pts) - 1
            for index in range(last):
                a, b = pts[index], pts[(index + 1) % len(pts)]
                value = _point_segment_distance(center, a, b)
                if best is None or value < best:
                    best = value
        return best

    def _gate_distance(center: Sequence[float]) -> Optional[float]:
        values = [_dist(center, _centroid(g)) for g in gate_rows if _centroid(g)]
        return min(values) if values else None

    wash_far = []
    wash_layout_bad = []
    for row in wash_rows:
        center = _centroid(row)
        if not center:
            continue
        attrs = row.get("attrs") if isinstance(row.get("attrs"), dict) else {}
        # 有属性时必须有“跨接入道路”的证据；完全无属性的人工设施不冒充已验证。
        if attrs and attrs.get("on_access_road") is not True:
            wash_layout_bad.append({"facility": row["id"], "layout": attrs.get("layout")})
        elif not attrs:
            wash_layout_bad.append({"facility": row["id"], "layout": "unverified"})
        gate_d = _gate_distance(center)
        road_d = _distance_to_roads(center)
        if gate_d is not None and gate_d / 1000.0 > p["wash_to_gate_max_m"]:
            wash_far.append({"facility": row["id"], "to_gate_m": round(gate_d / 1000.0, 1)})
        if road_d is not None and road_d / 1000.0 > p["wash_to_road_max_m"]:
            wash_far.append({"facility": row["id"], "to_road_m": round(road_d / 1000.0, 1)})
    scale_far = []
    scale_layout_bad = []
    for row in scale_rows:
        center = _centroid(row)
        if not center:
            continue
        attrs = row.get("attrs") if isinstance(row.get("attrs"), dict) else {}
        if attrs and attrs.get("layout") != "on_main_road":
            scale_layout_bad.append({"facility": row["id"], "layout": attrs.get("layout")})
        elif not attrs:
            scale_layout_bad.append({"facility": row["id"], "layout": "unverified"})
        gate_d = _gate_distance(center)
        road_d = _distance_to_roads(center)
        if gate_d is not None and gate_d / 1000.0 > p["weighbridge_to_gate_max_m"]:
            scale_far.append({"facility": row["id"], "to_gate_m": round(gate_d / 1000.0, 1)})
        if road_d is not None and road_d / 1000.0 > p["weighbridge_to_road_max_m"]:
            scale_far.append({"facility": row["id"], "to_road_m": round(road_d / 1000.0, 1)})

    wash_required = model["stage"] == "earthwork" or bool(wash_rows)
    if not gate_rows:
        status22, msg22 = "manual", "缺出入口，无法判断洗车台/地磅组织"
    elif wash_required and not wash_rows:
        status22, msg22 = "manual", "土石方阶段未设洗车台，需补出入口冲洗设施"
    elif not scale_rows:
        status22, msg22 = "manual", "未设地磅；如项目需材料称重，应在地磅近大门主路设置"
    elif wash_layout_bad or scale_layout_bad:
        status22, msg22 = "manual", "洗车台/地磅布置属性未证明跨接入道路或位于主路，需人工确认"
    elif wash_far or scale_far:
        status22, msg22 = "manual", "洗车台/地磅偏离大门主路超经验值，需复核行车组织"
    elif not wash_rows:
        status22, msg22 = "pass", "本阶段未涉土石方，地磅位于大门主路服务范围内"
    else:
        status22, msg22 = "pass", "洗车台跨出入口接入道路，地磅位于大门主路服务范围内"
    checks.append(_check(
        22, "出入口洗车/称重组织", status22, "经验", msg22,
        {"wash": [row["id"] for row in wash_rows],
         "weighbridge": [row["id"] for row in scale_rows],
         "wash_far": wash_far, "weighbridge_far": scale_far,
         "wash_layout_bad": wash_layout_bad, "weighbridge_layout_bad": scale_layout_bad,
         "limits_m": {"wash_to_gate": p["wash_to_gate_max_m"],
                      "wash_to_road": p["wash_to_road_max_m"],
                      "weighbridge_to_gate": p["weighbridge_to_gate_max_m"],
                      "weighbridge_to_road": p["weighbridge_to_road_max_m"]},
         "note": "洗车台应跨接入道路，车辆进出必过；地磅应位于重车行驶主线，"
                 "并设超限车绕行、排水与检定条件，具体按项目称重要求确认"},
        "JGJ 59 文明施工与出入口管理经验；地磅按项目材料称重需求设置，不替代计量检定",
    ))
    return checks


def _checks_living_zones(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    """0.7.0 生活区专项（规则 23-26）。

    生活区安全是“位置 + 配套 + 消防疏散”的组合判断。平面几何只能证明
    距离、包含与道路穿越；人数、疏散宽度、风玫瑰和消防专项结论必须人工确认。
    """
    checks: List[Dict[str, Any]] = []
    p = model["rule_params"]
    rows = model["facilities"]
    living = _by_categories(rows, LIVING_ZONE_CATEGORIES)
    processing = _by_categories(rows, PROCESSING_CATEGORIES)
    structure = []
    raw_outline = model.get("structure_outline") or []
    if isinstance(raw_outline, list):
        for item in raw_outline:
            if isinstance(item, dict):
                item = [item.get("x"), item.get("y")]
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                structure.append((float(item[0]), float(item[1])))

    # 23 生活区与作业面分离
    overlaps, short_processing, short_worksite = [], [], []
    for zone in living:
        for work in processing:
            distance = _row_distance_mm(zone, work) / 1000.0
            item = {"living": zone["id"], "processing": work["id"],
                    "distance_m": round(distance, 2)}
            if distance <= 0.001:
                overlaps.append(item)
            elif distance < p["living_to_processing_min_m"]:
                short_processing.append(item)
        if len(structure) >= 3:
            distance = _polygon_distance_mm(_row_polygon(zone), structure) / 1000.0
            item = {"living": zone["id"], "worksite": "structure_outline",
                    "distance_m": round(distance, 2)}
            if distance <= 0.001:
                overlaps.append(item)
            elif distance < p["living_to_worksite_min_m"]:
                short_worksite.append(item)
    wind = _wind_evidence(model)
    wind_verified = bool(wind.get("living_upwind_verified") or wind.get("upwind_verified"))
    wind_direction = (wind.get("prevailing_from") or wind.get("dominant_from")
                      or wind.get("direction_from") or wind.get("from"))
    if not living:
        status23, msg23 = "manual", "未提供员工宿舍区/工人生活区，无法判断与作业面分离"
    elif overlaps:
        status23, msg23 = "fail", "生活区与加工区/主体作业面重叠，人员密集区不能压在作业面上"
    elif short_processing or short_worksite:
        status23, msg23 = "manual", (
            "生活区距加工区小于 {} m 或距主体作业面小于 {} m，需结合噪声、扬尘、"
            "坠物与风向复核").format(p["living_to_processing_min_m"],
                                      p["living_to_worksite_min_m"])
    elif not wind_verified:
        status23, msg23 = "manual", (
            "生活区与作业面的平面距离满足经验值，但未证明生活区位于主导风向上风向；"
            "必须按项目风玫瑰和季节风向复核")
    else:
        status23, msg23 = "pass", "生活区与加工区/主体作业面分离，且已声明上风向复核证据"
    checks.append(_check(
        23, "生活区与作业面分离", status23, "经验", msg23,
        {"overlaps": overlaps[:20], "short_processing": short_processing[:20],
         "short_worksite": short_worksite[:20],
         "limits_m": {"to_processing": p["living_to_processing_min_m"],
                      "to_worksite": p["living_to_worksite_min_m"]},
         "wind": {"direction_from": wind_direction,
                  "living_upwind_verified": wind_verified,
                  "note": "无风玫瑰时不得把西/北侧候选说成已证明上风向"}},
        "JGJ 59：人员密集临建不得设在塔吊回转范围内；生活区与作业面分离及上风向为经验控制，须按项目风玫瑰复核",
    ))

    # 24 生活区道路与消防疏散
    road_rows = [row for row in rows if row["geometry"]["type"] == "line"
                 and row["category"] in ("temporary_road", "fire_access", "permanent_road")]
    crossings = []
    for zone in living:
        poly = _row_polygon(zone)
        for road in road_rows:
            if _line_crosses_polygon(road["geometry"]["points_mm"], poly):
                crossings.append({"living": zone["id"], "road": road["id"],
                                  "road_category": road["category"]})
    fire_lanes = _by_category(rows, "fire_access")
    fire_distances = []
    for zone in living:
        poly = _row_polygon(zone)
        best = None
        for lane in fire_lanes:
            distance = _line_polygon_distance_mm(lane["geometry"]["points_mm"], poly)
            if best is None or distance < best:
                best = distance
        if best is not None:
            fire_distances.append({"living": zone["id"],
                                   "nearest_fire_lane_m": round(best / 1000.0, 2)})
    far_fire = [item for item in fire_distances
                if item["nearest_fire_lane_m"] > p["living_fire_lane_max_m"]]
    evac_missing = []
    for zone in living:
        attrs = zone.get("attrs") if isinstance(zone.get("attrs"), dict) else {}
        exits = attrs.get("evacuation_exits", attrs.get("emergency_exits"))
        try:
            exit_count = int(exits) if exits is not None else 0
        except (TypeError, ValueError):
            exit_count = 0
        if exit_count < 2:
            evac_missing.append(zone["id"])
    if not living:
        status24, msg24 = "pass", "本阶段未设生活区，不适用"
    elif crossings:
        status24, msg24 = "fail", "道路穿越生活区，需改线并重做消防疏散组织"
    elif not fire_lanes:
        status24, msg24 = "manual", "缺消防车道，无法判断生活区消防可达性"
    elif far_fire:
        status24, msg24 = "manual", "生活区距消防车道超过 {} m，需复核取水与救援可达性".format(
            p["living_fire_lane_max_m"])
    elif evac_missing:
        status24, msg24 = "manual", "生活区消防车道可达，但缺少不少于 2 个疏散口的证据"
    else:
        status24, msg24 = "pass", "生活区未被道路穿越，消防车道可达且疏散口有证据"
    checks.append(_check(
        24, "生活区道路与消防疏散", status24, "规范", msg24,
        {"road_crossings": crossings, "fire_distances": fire_distances,
         "far_fire": far_fire, "evacuation_missing": evac_missing,
         "limit_m": p["living_fire_lane_max_m"],
         "note": "疏散口数量/宽度须按人数、层数、总平面出口和消防专项方案复核"},
        "GB 50720 施工现场临时建筑物技术规范：生活区应满足消防车道、疏散和临时消防给水要求",
    ))

    # 25 生活区配套完整性
    staff = _by_category(rows, "staff_dormitory") + _by_category(rows, "temporary_dormitory")
    workers = _by_category(rows, "worker_living_zone")
    canteens = _by_category(rows, "canteen")
    toilets = _by_category(rows, "toilet_shower")
    drying = _by_category(rows, "drying_area")
    missing = []
    if not staff and not workers:
        missing.append("宿舍载体（员工宿舍区/工人生活区）")
    if workers and not canteens:
        missing.append("食堂")
    if workers and not toilets:
        missing.append("卫生间/淋浴")
    issues = []
    if staff and workers:
        for a in staff:
            for b in workers:
                if _polygon_distance_mm(_row_polygon(a), _row_polygon(b)) <= 0.001:
                    issues.append("员工宿舍区与工人生活区重叠，需确认是否混用")
    by_id = {row["id"]: row for row in workers}
    for child in canteens + toilets + drying:
        attrs = child.get("attrs") if isinstance(child.get("attrs"), dict) else {}
        parent_id = attrs.get("parent_id")
        parent = by_id.get(parent_id)
        if parent is None:
            issues.append("{} 未声明有效的 worker_living_zone 父区域".format(child["id"]))
            continue
        if not _polygon_inside(_row_polygon(child), _row_polygon(parent)):
            issues.append("{} 未完全位于父区域 {} 内".format(child["id"], parent_id))
    if missing or issues:
        status25, msg25 = "manual", "生活区配套不完整：" + "；".join(missing + issues)
    elif not workers:
        status25, msg25 = "manual", "仅有员工宿舍载体，未设工人生活区；如项目无工人住宿需书面确认"
    else:
        status25, msg25 = "pass", "员工宿舍、工人生活区及食堂/卫生间配套齐全，子块均位于父区域内"
    checks.append(_check(
        25, "生活区配套完整性", status25, "经验", msg25,
        {"missing": missing, "issues": issues,
         "staff_dormitory": [row["id"] for row in staff],
         "worker_living_zone": [row["id"] for row in workers],
         "canteen": [row["id"] for row in canteens],
         "toilet_shower": [row["id"] for row in toilets],
         "drying_area": [row["id"] for row in drying]},
        "生活区应成组配置宿舍、食堂、卫生间/淋浴和晾晒；人数与面积定额须按项目实际复核",
    ))

    # 26 办公区靠近主出入口
    offices = _by_category(rows, "site_office")
    gates = _by_category(rows, "site_access")
    office_distances = []
    for office in offices:
        poly = _row_polygon(office)
        best = None
        for gate in gates:
            center = _centroid(gate)
            if not center:
                continue
            distance = _point_polygon_distance_mm(center, poly) / 1000.0
            if best is None or distance < best:
                best = distance
        if best is not None:
            office_distances.append({"office": office["id"], "nearest_gate_m": round(best, 2)})
    far_office = [item for item in office_distances
                  if item["nearest_gate_m"] > p["office_to_gate_max_m"]]
    if not offices:
        status26, msg26 = "manual", "未提供办公区，无法判断与主出入口关系"
    elif not gates:
        status26, msg26 = "manual", "缺出入口，无法判断办公区位置"
    elif far_office:
        status26, msg26 = "manual", "办公区距最近出入口超过 {} m，需复核人员进出与应急响应".format(
            p["office_to_gate_max_m"])
    else:
        status26, msg26 = "pass", "办公区位于最近出入口 {} m 范围内".format(
            p["office_to_gate_max_m"])
    checks.append(_check(
        26, "办公区靠近主出入口", status26, "经验", msg26,
        {"office_distances": office_distances, "far_office": far_office,
         "limit_m": p["office_to_gate_max_m"],
         "note": "主出入口应按现场交通组织确认；本规则只比最近大门，不替代门禁与人车分流"},
    ))

    return checks


def run_checks(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    """按规则分组执行；返回顺序固定为 1..26，供出图/自检/审查面板共用。"""
    checks: List[Dict[str, Any]] = []
    checks.extend(_checks_site_and_roads(model))
    checks.extend(_checks_fire_and_crane(model))
    checks.extend(_checks_power_and_processing(model))
    checks.extend(_checks_living_and_compliance(model))
    checks.extend(_checks_completeness(model))
    checks.extend(_checks_new_facilities(model))
    checks.extend(_checks_living_zones(model))
    return checks

def _components(rows: Sequence[Dict[str, Any]], tolerance_mm: float) -> List[List[Dict[str, Any]]]:
    """按端点距离把线状设施串成连通分量（并查集）。"""
    parent = list(range(len(rows)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if _endpoints_close(rows[i], rows[j], tolerance_mm):
                union(i, j)
    groups: Dict[int, List[Dict[str, Any]]] = {}
    for i, row in enumerate(rows):
        groups.setdefault(find(i), []).append(row)
    return list(groups.values())


def _endpoints_close(a: Dict[str, Any], b: Dict[str, Any], tolerance_mm: float) -> bool:
    pa = a["geometry"]["points_mm"]
    pb = b["geometry"]["points_mm"]
    if not pa or not pb:
        return False
    for p in (pa[0], pa[-1]):
        for q in (pb[0], pb[-1]):
            if _dist(p, q) <= tolerance_mm:
                return True
    # 端点落在对方线段上也算连通（T 形接口）；闭合折线要算上首尾闭合段
    def segments(row: Dict[str, Any]):
        pts = row["geometry"]["points_mm"]
        count = len(pts) if row["geometry"].get("closed") and len(pts) > 2 else len(pts) - 1
        for i in range(count):
            yield pts[i], pts[(i + 1) % len(pts)]

    for p in (pa[0], pa[-1]):
        for s0, s1 in segments(b):
            if _point_segment_distance(p, s0, s1) <= tolerance_mm:
                return True
    for q in (pb[0], pb[-1]):
        for s0, s1 in segments(a):
            if _point_segment_distance(q, s0, s1) <= tolerance_mm:
                return True
    return False


def stage_changes(models: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    ordered = [stage for stage in STAGES if stage in models]
    transitions = []
    for i in range(len(ordered) - 1):
        before, after = models[ordered[i]], models[ordered[i + 1]]
        before_ids = {row["id"] for row in before["facilities"]}
        after_ids = {row["id"] for row in after["facilities"]}
        before_cranes = {row["id"] for row in before.get("cranes") or []}
        after_cranes = {row["id"] for row in after.get("cranes") or []}
        transitions.append({
            "from": ordered[i],
            "to": ordered[i + 1],
            "from_name": STAGE_NAMES[ordered[i]],
            "to_name": STAGE_NAMES[ordered[i + 1]],
            "added": sorted(after_ids - before_ids),
            "removed": sorted(before_ids - after_ids),
            "unchanged": len(before_ids & after_ids),
            "cranes_added": sorted(after_cranes - before_cranes),
            "cranes_removed": sorted(before_cranes - after_cranes),
            "cranes_unchanged": sorted(before_cranes & after_cranes),
        })
    return {
        "schema": "site-stage-changes/v1",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "transitions": transitions,
        "note": "阶段变化只反映 active_stages 声明，不代表已审批的施工顺序；拆除/改线日期需项目确认",
    }


def render_markdown(model: Dict[str, Any]) -> str:
    lines = [
        "# {} 施工平面布置校核".format(model["stage_name"]),
        "",
        "- 项目：{}".format(model.get("project") or "—"),
        "- 阶段：`{}`".format(model["stage"]),
        "- 坐标单位：mm；红线面积：{}".format(
            "—" if model.get("redline_area_m2") is None else "{:.1f} m²".format(model["redline_area_m2"])),
        "- 设施：全部 {} 项，本阶段生效 {} 项".format(
            model["counts"]["all"], model["counts"]["active"]),
        "- 校核汇总：pass {} / manual {} / fail {}".format(
            model["summary"]["pass"], model["summary"]["manual"], model["summary"]["fail"]),
        "- 结论性质：布置草案校核，final_check=false，不替代审批",
        "",
        "## 校核明细",
        "",
        "| # | 项目 | 状态 | 依据 | 说明 |",
        "|---:|---|---|---|---|",
    ]
    for check in model["checks"]:
        lines.append("| {} | {} | {} | {} | {} |".format(
            check["id"], check["name"], check["status"], check["basis"],
            check["message"].replace("|", "/")))
    lines += ["", "## 本阶段设施", "", "| id | 分类 | 名称 | 来源 | 置信 | 生效阶段 |",
              "|---|---|---|---|---|---|"]
    for row in model["facilities"]:
        lines.append("| {} | {} | {} | {} | {} | {} |".format(
            row["id"], row["category_name"], row["name"], row["source"],
            row["confidence"], ",".join(row["active_stages"])))
    if model["warnings"]:
        lines += ["", "## 警告", ""] + ["- {}".format(w) for w in model["warnings"]]
    return "\n".join(lines) + "\n"
