"""道路几何校核：宽度、会车、转弯半径、尽头式回车场。

只做确定性几何计算，不判断"道路走向是否最优"。
阈值来自 rule_params，缺证据给 manual，不补 0。
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

ROAD_CATEGORIES = ("temporary_road", "fire_access", "permanent_road")
SCHEMA = "site-road-check/v1"


def _dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _polyline_length_mm(points: Sequence[Sequence[float]]) -> float:
    return sum(_dist(points[i], points[i + 1]) for i in range(len(points) - 1))


def _angle_deg(a: Sequence[float], b: Sequence[float], c: Sequence[float]) -> float:
    """∠ABC，单位度。"""
    v1 = (a[0] - b[0], a[1] - b[1])
    v2 = (c[0] - b[0], c[1] - b[1])
    n1 = math.hypot(*v1)
    n2 = math.hypot(*v2)
    if n1 <= 1e-9 or n2 <= 1e-9:
        return 180.0
    cos = max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))
    return math.degrees(math.acos(cos))


def _circumradius_mm(a: Sequence[float], b: Sequence[float], c: Sequence[float]) -> Optional[float]:
    """三点外接圆半径；近共线返回 None。"""
    ab = _dist(a, b)
    bc = _dist(b, c)
    ca = _dist(c, a)
    if ab <= 1e-9 or bc <= 1e-9 or ca <= 1e-9:
        return None
    area2 = abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))
    if area2 <= 1e-9:
        return None
    return ab * bc * ca / (2.0 * area2)


def _lanes(row: Dict[str, Any]) -> int:
    attrs = row.get("attrs") if isinstance(row.get("attrs"), dict) else {}
    raw = attrs.get("lanes")
    try:
        lanes = int(raw)
    except (TypeError, ValueError):
        lanes = 0
    if lanes in (1, 2):
        return lanes
    width = row.get("width_mm")
    if width is not None and float(width) >= 6000.0:
        return 2
    return 1


def _bay_stations_m(row: Dict[str, Any]) -> Optional[List[float]]:
    attrs = row.get("attrs") if isinstance(row.get("attrs"), dict) else {}
    bays = attrs.get("passing_bays")
    if bays is None:
        return None
    if not isinstance(bays, list):
        return None
    stations: List[float] = []
    for item in bays:
        value = item.get("station_m") if isinstance(item, dict) else item
        try:
            stations.append(float(value))
        except (TypeError, ValueError):
            continue
    return sorted(stations)


def check_roads(facilities: Sequence[Dict[str, Any]],
                params: Dict[str, float]) -> Dict[str, Any]:
    roads = [row for row in facilities if row.get("category") in ROAD_CATEGORIES]
    checks: List[Dict[str, Any]] = []

    dual_min = float(params.get("road_dual_min_width_m", 6.0))
    single_min = float(params.get("road_min_width_m", 3.5))
    fire_min = float(params.get("fire_lane_min_width_m", 4.0))
    bay_interval = float(params.get("passing_bay_interval_m", 100.0))
    turn_min = float(params.get("turning_radius_min_m", 9.0))
    fire_turn_min = float(params.get("fire_turning_radius_min_m", 12.0))
    turnaround_min = float(params.get("dead_end_turnaround_min_m", 12.0))

    # R1 宽度（按车道数区分单/双车道）
    narrow = []
    tested = 0
    for row in roads:
        width = row.get("width_mm")
        if width is None:
            continue
        tested += 1
        lanes = _lanes(row)
        if row["category"] == "fire_access":
            limit = max(fire_min, single_min)
            limit_name = "消防车道"
        elif lanes == 2:
            limit = dual_min
            limit_name = "双车道"
        else:
            limit = single_min
            limit_name = "单车道"
        if float(width) < limit * 1000.0 - 1e-6:
            narrow.append({"road": row["id"], "category": row["category"],
                           "width_m": round(float(width) / 1000.0, 2),
                           "lanes": lanes, "limit_m": limit, "limit_name": limit_name})
    checks.append({
        "id": "R1", "name": "道路宽度（单/双车道）",
        "status": "fail" if narrow else ("pass" if tested else "manual"),
        "basis": "规范",
        "message": "{} 条道路宽度不足".format(len(narrow)) if narrow else
                   ("{} 条道路宽度满足".format(tested) if tested else "未提供道路宽度"),
        "evidence": {"tested": tested, "narrow": narrow,
                     "single_min_m": single_min, "dual_min_m": dual_min,
                     "fire_min_m": fire_min},
        "action": "按 lane 数加宽或改为双车道；消防车道净宽不得小于 4 m" if narrow else "",
        "source": "GB 50720 消防车道净宽≥4 m；单/双车道取值按施工组织经验，待项目复核",
    })

    # R2 会车点（仅单车道长路）
    passing_fail = []
    passing_manual = []
    passing_tested = 0
    for row in roads:
        if _lanes(row) != 1:
            continue
        points = row["geometry"]["points_mm"]
        length_m = _polyline_length_mm(points) / 1000.0
        if length_m <= bay_interval + 1e-6:
            continue
        passing_tested += 1
        attrs = row.get("attrs") if isinstance(row.get("attrs"), dict) else {}
        interval = float(attrs.get("passing_bay_interval_m") or bay_interval)
        stations = _bay_stations_m(row)
        if stations is None:
            passing_manual.append({"road": row["id"], "length_m": round(length_m, 1),
                                   "interval_m": interval})
            continue
        stops = [0.0] + [s for s in stations if 0.0 <= s <= length_m] + [length_m]
        gaps = [stops[i + 1] - stops[i] for i in range(len(stops) - 1)]
        worst = max(gaps) if gaps else length_m
        if worst > interval + 1e-6:
            passing_fail.append({"road": row["id"], "length_m": round(length_m, 1),
                                 "max_gap_m": round(worst, 1), "interval_m": interval,
                                 "stations_m": [round(s, 1) for s in stations]})
    if passing_fail:
        status2, msg2 = "fail", "{} 条单车道会车点间距超限".format(len(passing_fail))
    elif passing_manual:
        status2, msg2 = "manual", "{} 条单车道未提供会车点位置".format(len(passing_manual))
    else:
        status2, msg2 = "pass", "单车道会车点满足要求（无长单车道或已给会车点）"
    checks.append({
        "id": "R2", "name": "单车道会车点",
        "status": status2, "basis": "经验",
        "message": msg2,
        "evidence": {"tested": passing_tested, "over": passing_fail,
                     "missing": passing_manual, "default_interval_m": bay_interval},
        "action": "按不超过 {} m 间距补会车点，或改为双车道".format(int(bay_interval)) if passing_fail else
                  ("在 attrs.passing_bays 中标注会车点里程" if passing_manual else ""),
        "source": "施工道路会车经验值，待项目按车型与流量复核",
    })

    # R3 转弯半径（折线顶点外接圆）
    turn_bad = []
    turn_tested = 0
    for row in roads:
        points = row["geometry"]["points_mm"]
        if len(points) < 3:
            continue
        limit = fire_turn_min if row["category"] == "fire_access" else turn_min
        for index in range(1, len(points) - 1):
            a, b, c = points[index - 1], points[index], points[index + 1]
            if _angle_deg(a, b, c) >= 170.0:
                continue
            radius = _circumradius_mm(a, b, c)
            if radius is None:
                continue
            turn_tested += 1
            if radius / 1000.0 < limit - 1e-6:
                turn_bad.append({"road": row["id"], "category": row["category"],
                                 "vertex_index": index,
                                 "vertex_mm": [round(b[0], 1), round(b[1], 1)],
                                 "radius_m": round(radius / 1000.0, 2),
                                 "limit_m": limit})
    checks.append({
        "id": "R3", "name": "道路转弯半径",
        "status": "fail" if turn_bad else ("pass" if turn_tested else "manual"),
        "basis": "经验",
        "message": "{} 处转弯半径不足".format(len(turn_bad)) if turn_bad else
                   ("{} 处转弯满足".format(turn_tested) if turn_tested else "道路无转折，未校核转弯半径"),
        "evidence": {"tested": turn_tested, "over": turn_bad,
                     "temporary_min_m": turn_min, "fire_min_m": fire_turn_min},
        "action": "加大转弯半径或改小折角；消防车道按消防车转弯要求复核" if turn_bad else "",
        "source": "施工道路经验值 9 m、消防车道 12 m，待按车型与消防车参数复核",
    })

    # R4 尽头式道路回车场
    # 只对临时道路和消防车道判“尽头”；永久/既有市政道路归市政管理，
    # 但它的端点可作为临时道路的“接顺点”，因此端点集合仍收全部道路。
    dead = []
    tested4 = 0
    endpoints: List[Tuple[str, Tuple[float, float]]] = []
    dead_end_roads = [row for row in roads
                      if row.get("category") in ("temporary_road", "fire_access")]
    for row in roads:
        points = row["geometry"]["points_mm"]
        if len(points) < 2:
            continue
        if row["geometry"].get("closed"):
            continue
        endpoints.append((row["id"], points[0]))
        endpoints.append((row["id"], points[-1]))
    for row in dead_end_roads:
        points = row["geometry"]["points_mm"]
        if len(points) < 2 or row["geometry"].get("closed"):
            continue
        tested4 += 1
        attrs = row.get("attrs") if isinstance(row.get("attrs"), dict) else {}
        turnaround = attrs.get("turnaround")
        area = attrs.get("turnaround_area_m")
        has_turnaround = bool(turnaround) or (area is not None and float(area) >= turnaround_min ** 2)
        for end in (points[0], points[-1]):
            shared = any(other_id != row["id"] and _dist(end, pt) <= 2000.0
                         for other_id, pt in endpoints)
            if shared or has_turnaround:
                continue
            dead.append({"road": row["id"], "category": row["category"],
                         "end_mm": [round(end[0], 1), round(end[1], 1)],
                         "has_turnaround": has_turnaround})
    fire_dead = [d for d in dead if d["category"] == "fire_access"]
    if fire_dead:
        status4, msg4 = "fail", "{} 处尽头式消防车道缺回车场".format(len(fire_dead))
    elif dead:
        status4, msg4 = "manual", "{} 处临时道路尽头未标回车条件".format(len(dead))
    else:
        status4, msg4 = ("pass" if tested4 else "manual"), \
            ("道路无独立尽头或已设回车场" if tested4 else "未提供道路")
    checks.append({
        "id": "R4", "name": "尽头式道路回车场",
        "status": status4, "basis": "规范",
        "message": msg4,
        "evidence": {"tested": tested4, "dead_ends": dead,
                     "min_area_m": turnaround_min ** 2,
                     "min_side_m": turnaround_min},
        "action": "尽头式消防车道补 12m×12m（高层 15m×15m）回车场" if fire_dead else
                  ("临时道路尽头补回车场或在 attrs.turnaround 标注" if dead else ""),
        "source": "GB 50016 尽头式消防车道应设回车道或回车场；面积按项目高层/多层复核",
    })

    summary = {"pass": 0, "fail": 0, "manual": 0}
    for check in checks:
        summary[check["status"]] += 1
    return {
        "schema": SCHEMA,
        "roads": len(roads),
        "checks": checks,
        "summary": summary,
        "final_check": False,
    }


def render_road_markdown(result: Dict[str, Any]) -> str:
    lines = ["# 道路几何校核", "",
             "> 只校核宽度、会车、转弯半径、回车场；不判断道路走向是否最优。", ""]
    for check in result["checks"]:
        lines += ["## {} {}（{}）".format(check["id"], check["name"], check["status"]),
                  "", check["message"], "",
                  "依据：{}".format(check.get("source") or check.get("basis") or ""), ""]
        if check.get("action"):
            lines += ["处理：{}".format(check["action"]), ""]
    lines += ["## 汇总", "",
              "- 通过：{pass}　不通过：{fail}　待人工：{manual}".format(**result["summary"]), ""]
    return "\n".join(lines)
