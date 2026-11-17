#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""审计板图层洞口证据，逐条分类并核对历史洞口候选。"""



from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

from cad_common import to_number as _number, round_number as _round, to_text as _text  # noqa: E402,F401

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any


SCHEMA = "cad-slab-opening-audit/v0.1"
OPENING_LAYER = "S-板-开洞"
CONFIRMED_STATUSES = {"rectangle-x", "closed-polyline", "closed-line-ring"}
NON_OPENING_STATUSES = {
    "annotation-leader", "adjacent-to-confirmed-opening", "out-of-frame",
}
EXPLAINED_STATUSES = CONFIRMED_STATUSES | NON_OPENING_STATUSES
DEFAULT_CLOSURE_LAYERS = (
    "S-板-板边线", "S-板-降板边线", "S-剪力墙", "A-WALL",
    "S-柱", "A-COLUMN", "S-剪力墙-连梁",
)



def _mm2_to_m2(value: float) -> float:
    return value / 1_000_000.0


def _bbox(points: list[tuple[float, float]]) -> list[float]:
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return [min(xs), min(ys), max(xs), max(ys)]


def _polygon_area_m2(points: list[tuple[float, float]]) -> float:
    if len(points) < 3:
        return 0.0
    total = 0.0
    for index in range(len(points)):
        x0, y0 = points[index]
        x1, y1 = points[(index + 1) % len(points)]
        total += x0 * y1 - x1 * y0
    return abs(total) / 2_000_000.0


def _distance(first: tuple[float, float], second: tuple[float, float]) -> float:
    return math.hypot(first[0] - second[0], first[1] - second[1])


def _corner_set(bbox: list[float]) -> list[tuple[float, float]]:
    return [
        (bbox[0], bbox[1]),
        (bbox[0], bbox[3]),
        (bbox[2], bbox[1]),
        (bbox[2], bbox[3]),
    ]


def _same_point_set(
        points: list[tuple[float, float]],
        expected: list[tuple[float, float]],
        tolerance: float) -> bool:
    if len(points) != len(expected):
        return False
    remaining = list(expected)
    for point in points:
        for index, candidate in enumerate(remaining):
            if _distance(point, candidate) <= tolerance:
                remaining.pop(index)
                break
        else:
            return False
    return True


def _same_bbox(
        first: list[float], second: list[float], tolerance: float) -> bool:
    return all(
        abs(_number(first[index]) - _number(second[index])) <= tolerance
        for index in range(4))


def _snap(point: tuple[float, float], tolerance: float) -> tuple[float, float]:
    if tolerance <= 0:
        return (point[0], point[1])
    return (round(point[0] / tolerance) * tolerance,
            round(point[1] / tolerance) * tolerance)


def _node_key(point: tuple[float, float]) -> tuple[float, float]:
    return (round(point[0] / 2.0) * 2.0, round(point[1] / 2.0) * 2.0)


def _entity_segments(points: list[tuple[float, float]], closed: bool
                     ) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    pairs = [
        (points[index], points[index + 1]) for index in range(len(points) - 1)
    ]
    if closed and len(points) > 2 and _distance(points[0], points[-1]) > 1.0:
        pairs.append((points[-1], points[0]))
    return pairs


def _normalize_entities(
        raw: list[dict[str, Any]],
        transform: tuple[float, float],
        layers: set[str],
        ) -> list[dict[str, Any]]:
    tx, ty = transform
    entities: list[dict[str, Any]] = []
    for row in raw:
        layer = _text(row.get("layer"))
        if layer not in layers:
            continue
        points = [
            (_number(point[0]) + tx, _number(point[1]) + ty)
            for point in (row.get("points") or [])
            if point and len(point) >= 2
        ]
        if len(points) < 2:
            continue
        entities.append({
            "handle": _text(row.get("handle")),
            "layer": layer,
            "kind": _text(row.get("kind")) or "LINE",
            "closed": bool(row.get("closed")),
            "points": points,
            "bbox": _bbox(points),
        })
    entities.sort(
        key=lambda row: (row["bbox"][0], row["bbox"][1], row["handle"]))
    return entities


def _read_entities(dxf_path: Path, layers: set[str]) -> list[dict[str, Any]]:
    from dev_dxf import readfile

    document = readfile(str(dxf_path))
    raw: list[dict[str, Any]] = []
    for entity in document.modelspace():
        layer = _text(entity.dxf.layer)
        if layer not in layers:
            continue
        entity_type = entity.dxftype()
        closed = False
        if entity_type == "LINE":
            points = [
                [float(entity.dxf.start.x), float(entity.dxf.start.y)],
                [float(entity.dxf.end.x), float(entity.dxf.end.y)],
            ]
        elif entity_type == "LWPOLYLINE":
            points = [[float(x), float(y)] for x, y in entity.get_points("xy")]
            closed = bool(entity.closed)
        else:
            continue
        raw.append({
            "handle": _text(entity.dxf.handle),
            "layer": layer,
            "kind": entity_type,
            "closed": closed,
            "points": points,
        })
    return raw


def _adjacent_to_opening(
        bbox: list[float],
        openings: list[dict[str, Any]],
        tolerance: float) -> dict[str, Any] | None:
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    for opening in openings:
        target = [_number(value) for value in opening["bbox"]]
        span_x = (
            abs(bbox[0] - target[0]) <= tolerance
            and abs(bbox[2] - target[2]) <= tolerance)
        span_y = (
            abs(bbox[1] - target[1]) <= tolerance
            and abs(bbox[3] - target[3]) <= tolerance)
        gap_y = min(
            abs(bbox[1] - target[3]), abs(bbox[3] - target[1]),
            abs(bbox[1] - target[1]), abs(bbox[3] - target[3]))
        gap_x = min(
            abs(bbox[0] - target[2]), abs(bbox[2] - target[0]),
            abs(bbox[0] - target[0]), abs(bbox[2] - target[2]))
        near_y = gap_y <= max(width, 1.0) + tolerance
        near_x = gap_x <= max(height, 1.0) + tolerance
        if (span_x and near_y) or (span_y and near_x):
            return opening
    return None


def _match_panel(
        bbox: list[float],
        panels: list[dict[str, Any]],
        ) -> dict[str, Any] | None:
    best: dict[str, Any] | None = None
    best_score = 0.0
    for panel in panels:
        target = panel["bbox"]
        overlap_x = min(bbox[2], target[2]) - max(bbox[0], target[0])
        overlap_y = min(bbox[3], target[3]) - max(bbox[1], target[1])
        if overlap_x <= 0.0 or overlap_y <= 0.0:
            continue
        same_envelope = _same_bbox(bbox, target, 2.0)
        score = overlap_x * overlap_y * (100.0 if same_envelope else 1.0)
        if score > best_score:
            best_score = score
            best = dict(panel)
            best["same_envelope"] = same_envelope
    return best


def _classify_crossings(
        entities: list[dict[str, Any]],
        tolerance: float,
        min_area_m2: float,
        ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """用包围盒网格索引找对角线成对洞口，避免全图两两比较。"""
    lines = [row for row in entities if row["kind"] == "LINE"]
    cell = max(tolerance * 2.0, 1.0)

    def cell_key(bbox: list[float]) -> tuple[int, int]:
        return (int(math.floor(bbox[0] / cell)), int(math.floor(bbox[1] / cell)))

    buckets: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in lines:
        buckets[cell_key(row["bbox"])].append(row)
    used: set[str] = set()
    openings: list[dict[str, Any]] = []
    for row in lines:
        if row["handle"] in used:
            continue
        gx, gy = cell_key(row["bbox"])
        candidates: list[dict[str, Any]] = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                candidates.extend(buckets.get((gx + dx, gy + dy), []))
        best: dict[str, Any] | None = None
        for other in candidates:
            if other["handle"] == row["handle"] or other["handle"] in used:
                continue
            if not _same_bbox(row["bbox"], other["bbox"], tolerance):
                continue
            if not _same_point_set(
                    row["points"] + other["points"],
                    _corner_set(row["bbox"]), tolerance):
                continue
            best = other
            break
        if best is None:
            continue
        area = _mm2_to_m2(
            (row["bbox"][2] - row["bbox"][0])
            * (row["bbox"][3] - row["bbox"][1]))
        if area < min_area_m2:
            continue
        openings.append({
            "status": "rectangle-x",
            "handles": sorted([row["handle"], best["handle"]]),
            "segment_count": 2,
            "bbox": [_round(value, 1) for value in row["bbox"]],
            "envelope_area_m2": _round(area),
            "enclosed_area_m2": _round(area),
            "area_m2": _round(area),
            "deduct_area_m2": _round(area),
            "free_end_count": 0,
            "evidence": "两条对角线四个端点命中同一矩形四角",
            "review_required": False,
        })
        used.add(row["handle"])
        used.add(best["handle"])
    residual = [row for row in entities if row["handle"] not in used]
    return openings, residual


def _classify_closed_polylines(
        entities: list[dict[str, Any]],
        min_area_m2: float,
        ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    openings: list[dict[str, Any]] = []
    residual: list[dict[str, Any]] = []
    for row in entities:
        area = _polygon_area_m2(row["points"]) if row["closed"] else 0.0
        if row["kind"] != "LINE" and row["closed"] and area >= min_area_m2:
            openings.append({
                "status": "closed-polyline",
                "handles": [row["handle"]],
                "segment_count": max(1, len(row["points"]) - 1),
                "bbox": [_round(value, 1) for value in row["bbox"]],
                "envelope_area_m2": _round(area),
                "enclosed_area_m2": _round(area),
                "area_m2": _round(area),
                "deduct_area_m2": _round(area),
                "free_end_count": 0,
                "evidence": "闭合多段线自身围合成环",
                "review_required": False,
            })
        else:
            residual.append(row)
    return openings, residual


def _components(
        entities: list[dict[str, Any]],
        ) -> list[list[dict[str, Any]]]:
    indexed: list[dict[str, Any]] = []
    for entity in entities:
        for segment in _entity_segments(entity["points"], entity["closed"]):
            indexed.append({"handle": entity["handle"], "segment": segment})
    adjacency: dict[tuple[float, float], list[int]] = defaultdict(list)
    for index, row in enumerate(indexed):
        for point in row["segment"]:
            adjacency[_node_key(point)].append(index)
    seen: set[int] = set()
    groups: list[list[dict[str, Any]]] = []
    for index in range(len(indexed)):
        if index in seen:
            continue
        stack = [index]
        members: set[int] = set()
        while stack:
            current = stack.pop()
            if current in members:
                continue
            members.add(current)
            seen.add(current)
            for point in indexed[current]["segment"]:
                for peer in adjacency[_node_key(point)]:
                    if peer not in members:
                        stack.append(peer)
        groups.append([indexed[current] for current in sorted(members)])
    return groups


def _order_ring(members: list[dict[str, Any]]) -> list[tuple[float, float]]:
    adjacency: dict[tuple[float, float], list[tuple[float, float]]] = \
        defaultdict(list)
    for row in members:
        start, end = row["segment"]
        adjacency[_node_key(start)].append(_node_key(end))
        adjacency[_node_key(end)].append(_node_key(start))
    if not adjacency:
        return []
    if any(len(nodes) != 2 for nodes in adjacency.values()):
        return []
    start = next(iter(adjacency))
    ring = [start]
    previous: tuple[float, float] | None = None
    current = start
    while True:
        options = [node for node in adjacency[current] if node != previous]
        if not options:
            return []
        nxt = options[0]
        if nxt == start:
            break
        ring.append(nxt)
        previous, current = current, nxt
        if len(ring) > len(members) + 2:
            return []
    return ring if len(ring) >= 3 else []


def _classify_residual(
        entities: list[dict[str, Any]],
        openings: list[dict[str, Any]],
        panels: list[dict[str, Any]],
        options: dict[str, float],
        ) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    tolerance = options["junction_tolerance_mm"]
    for members in _components(entities):
        handles = sorted({row["handle"] for row in members})
        points = [point for row in members for point in row["segment"]]
        bbox = _bbox(points)
        degree = Counter(
            _node_key(point) for row in members for point in row["segment"])
        free_ends = sorted(
            node for node, count in degree.items() if count == 1)
        lengths = sorted(
            _distance(row["segment"][0], row["segment"][1]) for row in members)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        envelope = _mm2_to_m2(width * height)
        ring = _order_ring(members) if not free_ends else []
        ring_area = _polygon_area_m2(ring) if ring else 0.0
        adjacent = _adjacent_to_opening(bbox, openings, tolerance + 1.0)
        if ring_area >= options["min_opening_area_m2"]:
            status = "closed-line-ring"
            deduct = ring_area
            evidence = "同图层多条线段首尾相连围合成环"
        elif adjacent:
            status = "adjacent-to-confirmed-opening"
            deduct = 0.0
            evidence = (
                f"包络与已确认洞口 {_text(adjacent.get('panel_id')) or '+'.join(adjacent['handles'])} "
                "同跨并紧贴洞口边，判为标注引出线")
        elif min(width, height) <= options["leader_strip_max_mm"]:
            status = "annotation-leader"
            deduct = 0.0
            evidence = (
                f"包络短边 {min(width, height):.1f} mm 在引线阈值内，"
                "两端开放不成环")
        elif len(members) == 1 and len(handles) == 1:
            status = "standalone-line"
            deduct = 0.0
            evidence = "单条独立线段，无第二条线与之成 X，也无闭合边界"
        else:
            status = "open-chain"
            deduct = 0.0
            evidence = f"{len(members)} 段开放折线，两端自由端未闭合"
        panel = _match_panel(bbox, panels)
        envelope_volume = 0.0
        touched_panels: list[str] = []
        for candidate in panels:
            target = candidate["bbox"]
            overlap_x = min(bbox[2], target[2]) - max(bbox[0], target[0])
            overlap_y = min(bbox[3], target[3]) - max(bbox[1], target[1])
            if overlap_x <= 0.0 or overlap_y <= 0.0:
                continue
            overlap_area = min(_mm2_to_m2(overlap_x * overlap_y),
                               _number(candidate["area_m2"]))
            if overlap_area <= 0.0:
                continue
            envelope_volume += overlap_area * (
                _number(candidate["thickness_mm"]) / 1000.0)
            touched_panels.append(_text(candidate["id"]))
        # 逐块累加会把同一包络压到的每块板都算一遍，只能当保守上限；
        # 归属口径只认匹配到的那块板，取包络与板面较小面积乘该板厚度。
        attributed_volume = 0.0
        if panel:
            attributed_volume = min(
                envelope, _number(panel["area_m2"])) * (
                _number(panel["thickness_mm"]) / 1000.0)
        if status == "open-chain" and panel and panel["same_envelope"]:
            status = "panel-diagonal-chain"
            evidence = (
                f"{len(members)} 段开放折线，两个自由端未闭合；"
                f"包络与板面 {_text(panel['id'])} 完全重合，"
                "需人工确认该板面是否就是洞口")
        record = {
            "status": status,
            "handles": handles,
            "segment_count": len(members),
            "bbox": [_round(value, 1) for value in bbox],
            "envelope_area_m2": _round(envelope),
            "enclosed_area_m2": _round(ring_area),
            "deduct_area_m2": _round(deduct),
            "free_end_count": len(free_ends),
            "free_ends": [[_round(node[0], 1), _round(node[1], 1)]
                          for node in free_ends],
            "min_segment_length_mm": _round(lengths[0], 1),
            "max_segment_length_mm": _round(lengths[-1], 1),
            "evidence": evidence,
            "panel_id": _text(panel.get("id")) if panel else "",
            "panel_area_m2": _round(panel["area_m2"]) if panel else None,
            "panel_thickness_mm": _round(
                panel["thickness_mm"], 1) if panel else None,
            "panel_same_envelope": bool(panel["same_envelope"]) if panel else False,
            "review_required": status not in EXPLAINED_STATUSES,
        }
        if status in CONFIRMED_STATUSES:
            record["area_m2"] = _round(deduct)
        else:
            record["touched_panel_ids"] = touched_panels
            record["potential_volume_upper_bound_m3"] = _round(envelope_volume)
            record["potential_volume_attributed_m3"] = _round(attributed_volume)
        records.append(record)
    records.sort(key=lambda row: (row["bbox"][0], row["bbox"][1]))
    return records


def _probe_closure(
        records: list[dict[str, Any]],
        entities: list[dict[str, Any]],
        closure_layers: set[str],
        options: dict[str, float],
        ) -> None:
    tolerance = max(options["closure_tolerance_mm"], 1.0)
    margin = options["closure_search_margin_mm"]
    segments: list[tuple[tuple[float, float], tuple[float, float], str]] = []
    for row in entities:
        layer = _text(row.get("layer"))
        if layer not in closure_layers:
            continue
        for start, end in _entity_segments(row["points"], row["closed"]):
            segments.append((
                _snap(start, tolerance), _snap(end, tolerance), layer))
    if not segments:
        return
    for record in records:
        if not record.get("review_required"):
            continue
        ends = [tuple(node) for node in record.get("free_ends") or []]
        if len(ends) != 2:
            continue
        bbox = record["bbox"]
        low_x, low_y = bbox[0] - margin, bbox[1] - margin
        high_x, high_y = bbox[2] + margin, bbox[3] + margin
        adjacency: dict[tuple[float, float], list[tuple[float, float]]] = \
            defaultdict(list)
        hit_layers: set[str] = set()
        for start, end, layer in segments:
            if max(start[0], end[0]) < low_x or min(start[0], end[0]) > high_x:
                continue
            if max(start[1], end[1]) < low_y or min(start[1], end[1]) > high_y:
                continue
            if start == end:
                continue
            hit_layers.add(layer)
            adjacency[start].append(end)
            adjacency[end].append(start)
        source = _snap(ends[0], tolerance)
        target = _snap(ends[1], tolerance)
        result = {
            "closed": False,
            "node_count": 0,
            "ring_area_m2": 0.0,
            "rectangular_likeness": 0.0,
            "confidence": "none",
            "treat_as_opening_candidate": False,
            "deduction_applied": False,
            "searched_node_count": len(adjacency),
            "reached_layers": sorted(hit_layers),
        }
        previous: dict[tuple[float, float], Any] = {source: None}
        queue = deque([source])
        found = source == target
        while queue and not found:
            node = queue.popleft()
            for peer in adjacency.get(node, []):
                if peer in previous:
                    continue
                previous[peer] = node
                if peer == target:
                    found = True
                    break
                queue.append(peer)
        if found:
            path: list[tuple[float, float]] = []
            node = target
            while node is not None:
                path.append(node)
                node = previous[node]
            path.reverse()
            ring_area = _polygon_area_m2(path)
            ring_bbox = _bbox(path)
            ring_envelope = _mm2_to_m2(
                (ring_bbox[2] - ring_bbox[0]) * (ring_bbox[3] - ring_bbox[1]))
            likeness = ring_area / ring_envelope if ring_envelope else 0.0
            high = bool(
                likeness >= 0.95 and len(path) <= 6
                and ring_area >= _number(options.get("min_opening_area_m2")))
            result.update({
                "closed": len(path) > 2,
                "node_count": len(path),
                "ring_area_m2": _round(ring_area),
                "rectangular_likeness": _round(likeness),
                "confidence": "high" if high else "low",
                "treat_as_opening_candidate": high,
            })
        record["cross_layer_closure"] = result


def _gap_consistency(
        options: dict[str, float],
        review_rows: list[dict[str, Any]],
        ) -> dict[str, Any]:
    gap = _number(options.get("reference_gap_m3"), -1.0)
    upper = sum(
        _number(row.get("potential_volume_upper_bound_m3"))
        for row in review_rows)
    attributed = sum(
        _number(row.get("potential_volume_attributed_m3"))
        for row in review_rows)
    if gap < 0.0:
        return {
            "provided": False,
            "note": "未提供 CAD 与参考混凝土差额，不做一致性判定",
        }
    return {
        "provided": True,
        "reference_gap_m3": _round(gap),
        "review_volume_upper_bound_m3": _round(upper),
        "review_volume_attributed_m3": _round(attributed),
        "all_residual_are_openings": bool(upper <= gap),
        "note": (
            "待复核图线全部按洞口扣除"
            + ("仍在量差范围内，需要逐条人工确认。"
               if upper <= gap else
               f"会超出当前量差 {upper - gap:.4f} m3，"
               "因此至少部分图线不是洞口。")
        ),
    }


def _load_panels(model: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    panels = (model.get("members") or {}).get("slab_panels") or []
    for panel in panels:
        bbox = panel.get("bbox") or []
        if len(bbox) != 4:
            continue
        result.append({
            "id": _text(panel.get("id")),
            "bbox": [_number(value) for value in bbox],
            "area_m2": _number(panel.get("area_m2")),
            "thickness_mm": _number(panel.get("thickness_mm")),
            "opening_status": _text(panel.get("opening_status")),
            "opening_area_m2": _number(panel.get("opening_area_m2")),
            "opening_evidence": panel.get("opening_evidence") or [],
        })
    return result


def _reconcile_prior(
        prior: dict[str, Any],
        records: list[dict[str, Any]],
        panels: list[dict[str, Any]],
        ) -> list[dict[str, Any]]:
    by_handle: dict[str, dict[str, Any]] = {}
    for record in records:
        for handle in record["handles"]:
            by_handle[handle] = record
    candidates: dict[str, dict[str, Any]] = {}
    sources: list[dict[str, Any]] = []
    sources.extend(panels)
    sources.extend((prior.get("members") or {}).get("slab_panels") or [])
    for panel in sources:
        if _text(panel.get("opening_status")) != "opening-candidate":
            continue
        panel_id = _text(panel.get("id"))
        if not panel_id or panel_id in candidates:
            continue
        candidates[panel_id] = panel
    rows: list[dict[str, Any]] = []
    for panel_id, panel in candidates.items():
        evidence = sorted({
            _text(item.get("handle"))
            for item in panel.get("opening_evidence") or []
            if _text(item.get("handle"))
        })
        matched = [by_handle[handle] for handle in evidence if handle in by_handle]
        review = any(row.get("review_required") for row in matched)
        rows.append({
            "panel_id": panel_id,
            "panel_area_m2": _round(panel.get("area_m2")),
            "panel_thickness_mm": _round(panel.get("thickness_mm"), 1),
            "prior_handles": evidence,
            "matched_handles": sorted({
                handle for row in matched for handle in row["handles"]}),
            "current_statuses": sorted({row["status"] for row in matched}),
            "review_required": review,
            "deduct_area_m2": _round(sum(
                _number(row.get("deduct_area_m2")) for row in matched
                if row["status"] in CONFIRMED_STATUSES)),
        })
    rows.sort(key=lambda row: row["panel_id"])
    return rows


def build_audit(
        raw_entities: list[dict[str, Any]],
        model: dict[str, Any],
        prior: dict[str, Any] | None = None,
        transform: tuple[float, float] = (0.0, 0.0),
        options: dict[str, float] | None = None,
        closure_layers: tuple[str, ...] = DEFAULT_CLOSURE_LAYERS,
        probe_closure: bool = True,
        ) -> dict[str, Any]:
    options = dict(options or {})
    options.setdefault("junction_tolerance_mm", 2.0)
    options.setdefault("min_opening_area_m2", 0.01)
    options.setdefault("leader_strip_max_mm", 600.0)
    options.setdefault("frame_margin_mm", 1000.0)
    options.setdefault("closure_tolerance_mm", 50.0)
    options.setdefault("closure_search_margin_mm", 12000.0)
    options.setdefault("reference_gap_m3", -1.0)
    opening_layer = OPENING_LAYER
    panels = _load_panels(model)
    entities = _normalize_entities(
        raw_entities, transform, {opening_layer} | set(closure_layers))
    opening_entities = [
        row for row in entities if row["layer"] == opening_layer]
    frame: list[float] | None = None
    if panels:
        xs = [value for panel in panels for value in (panel["bbox"][0], panel["bbox"][2])]
        ys = [value for panel in panels for value in (panel["bbox"][1], panel["bbox"][3])]
        frame = [min(xs), min(ys), max(xs), max(ys)]
    in_frame: list[dict[str, Any]] = []
    outside: list[dict[str, Any]] = []
    for entity in opening_entities:
        bbox = entity["bbox"]
        if frame and (
                bbox[2] < frame[0] - options["frame_margin_mm"]
                or bbox[0] > frame[2] + options["frame_margin_mm"]
                or bbox[3] < frame[1] - options["frame_margin_mm"]
                or bbox[1] > frame[3] + options["frame_margin_mm"]):
            outside.append(entity)
        else:
            in_frame.append(entity)
    poly_openings, residual = _classify_closed_polylines(
        in_frame, options["min_opening_area_m2"])
    cross_openings, residual = _classify_crossings(
        residual, options["junction_tolerance_mm"],
        options["min_opening_area_m2"])
    openings = sorted(
        poly_openings + cross_openings, key=lambda row: row["bbox"][:2])
    for opening in openings:
        panel = _match_panel(
            [_number(value) for value in opening["bbox"]], panels)
        opening["panel_id"] = _text(panel.get("id")) if panel else ""
        opening["panel_area_m2"] = _round(panel["area_m2"]) if panel else None
        opening["panel_thickness_mm"] = (
            _round(panel["thickness_mm"], 1) if panel else None)
        opening["panel_same_envelope"] = (
            bool(panel["same_envelope"]) if panel else False)
    records = list(openings)
    records.extend(_classify_residual(residual, openings, panels, options))
    if probe_closure:
        _probe_closure(records, entities, set(closure_layers), options)
    for members in _components(outside):
        group_points = [point for row in members for point in row["segment"]]
        group_bbox = _bbox(group_points)
        degree = Counter(
            _node_key(point) for row in members for point in row["segment"])
        records.append({
            "status": "out-of-frame",
            "handles": sorted({row["handle"] for row in members}),
            "segment_count": len(members),
            "bbox": [_round(value, 1) for value in group_bbox],
            "envelope_area_m2": _round(_mm2_to_m2(
                (group_bbox[2] - group_bbox[0])
                * (group_bbox[3] - group_bbox[1]))),
            "enclosed_area_m2": 0.0,
            "deduct_area_m2": 0.0,
            "free_end_count": len([
                node for node, count in degree.items() if count == 1]),
            "free_ends": [],
            "evidence": "落在本层板面范围外，属于相邻图框的重复图形",
            "review_required": False,
        })
    records.sort(key=lambda row: (row["bbox"][0], row["bbox"][1]))
    prior_rows = _reconcile_prior(prior or {}, records, panels)
    confirmed = [row for row in records if row["status"] in CONFIRMED_STATUSES]
    review_rows = [row for row in records if row.get("review_required")]
    opening_area = sum(_number(row["deduct_area_m2"]) for row in confirmed)
    gross = sum(_number(panel["area_m2"]) for panel in panels)
    accounted = {
        handle for row in records for handle in row["handles"]}
    unaccounted = [
        row["handle"] for row in opening_entities if row["handle"] not in accounted]
    summary = {
        "source_entity_count": len(opening_entities),
        "accounted_entity_count": len([
            row for row in opening_entities if row["handle"] in accounted]),
        "unaccounted_entity_count": len(unaccounted),
        "confirmed_opening_count": len(confirmed),
        "confirmed_opening_area_m2": _round(opening_area),
        "annotation_record_count": len([
            row for row in records if row["status"] in NON_OPENING_STATUSES
            and row["status"] != "out-of-frame"]),
        "out_of_frame_count": len([
            row for row in records if row["status"] == "out-of-frame"]),
        "review_required_count": len(review_rows),
        "review_handles": sorted({
            handle for row in review_rows for handle in row["handles"]}),
        "review_envelope_area_upper_bound_m2": _round(sum(
            _number(row.get("envelope_area_m2")) for row in review_rows)),
        "review_volume_upper_bound_m3": _round(sum(
            _number(row.get("potential_volume_upper_bound_m3"))
            for row in review_rows)),
        "review_volume_attributed_m3": _round(sum(
            _number(row.get("potential_volume_attributed_m3"))
            for row in review_rows)),
        "review_handles_status": {
            "+".join(row["handles"]): row["status"] for row in review_rows},
        "review_boundary_closure_found": any(
            (row.get("cross_layer_closure") or {}).get(
                "treat_as_opening_candidate") for row in review_rows),
        "gap_consistency": _gap_consistency(options, review_rows),
        "panel_count": len(panels),
        "gross_panel_area_m2": _round(gross),
        "net_panel_area_m2": _round(gross - opening_area),
        "prior_candidate_panel_count": len(prior_rows),
        "prior_candidate_explained_panel_count": len([
            row for row in prior_rows if not row["review_required"]]),
        "prior_candidate_review_panel_count": len([
            row for row in prior_rows if row["review_required"]]),
        "entity_ledger_closed": bool(opening_entities and not unaccounted),
        "openings_closed": bool(
            opening_entities and not unaccounted and not review_rows),
        "status_counts": dict(sorted(Counter(
            _text(row["status"]) for row in records).items())),
    }
    return {
        "schema": SCHEMA,
        "opening_layer": opening_layer,
        "closure_layers": sorted(closure_layers),
        "floor": _text(model.get("floor")),
        "slab_transform": [_round(transform[0], 3), _round(transform[1], 3)],
        "frame_bbox_mm": [_round(value, 1) for value in frame] if frame else [],
        "options": {key: _round(value, 3) for key, value in sorted(options.items())},
        "records": records,
        "confirmed_openings": [
            {key: row.get(key) for key in (
                "handles", "status", "bbox", "area_m2", "deduct_area_m2",
                "panel_id", "panel_area_m2", "panel_thickness_mm",
                "panel_same_envelope", "evidence")}
            for row in confirmed],
        "prior_candidate_reconciliation": prior_rows,
        "panel_envelope_conflicts": [
            {
                "panel_id": row["panel_id"],
                "handles": row["handles"],
                "status": row["status"],
                "note": "候选洞口包络与板面范围完全重合，需要人工确认该板面是否就是洞口",
            }
            for row in records
            if row.get("panel_same_envelope")
            and row["status"] not in CONFIRMED_STATUSES],
        "summary": summary,
        "applied_to_formal_quantity": False,
        "formal_ready": False,
    }


def csv_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows = [[
        "类别", "句柄", "状态", "范围mm", "包络面积m2", "围合面积m2", "扣减面积m2",
        "线段数", "自由端数", "匹配板面", "板面面积m2", "复核上限m3",
        "跨层闭合", "复核需要", "证据",
    ]]
    for row in result["records"]:
        closure = row.get("cross_layer_closure") or {}
        rows.append([
            "洞口" if row["status"] in CONFIRMED_STATUSES else "非洞口",
            "+".join(_text(handle) for handle in row.get("handles") or []),
            _text(row.get("status")),
            ",".join(f"{_number(value):.1f}" for value in row.get("bbox") or []),
            _round(row.get("envelope_area_m2")),
            _round(row.get("enclosed_area_m2")),
            _round(row.get("deduct_area_m2")),
            int(_number(row.get("segment_count"))),
            int(_number(row.get("free_end_count"))),
            _text(row.get("panel_id")),
            _round(row.get("panel_area_m2")),
            _round(row.get("potential_volume_upper_bound_m3")),
            ("环面积%.3fm2/%s/方整度%.2f" % (
                _number(closure.get("ring_area_m2")),
                _text(closure.get("confidence")),
                _number(closure.get("rectangular_likeness")))) if closure
            else "",
            "是" if row.get("review_required") else "否",
            _text(row.get("evidence")),
        ])
    rows.append([])
    rows.append(["历史候选对账", "板编号", "板面积m2", "原句柄", "命中句柄",
                 "当前状态", "扣减m2", "待复核"])
    for row in result["prior_candidate_reconciliation"]:
        rows.append([
            "", row["panel_id"], row["panel_area_m2"],
            "+".join(row["prior_handles"]), "+".join(row["matched_handles"]),
            ",".join(row["current_statuses"]) or "未命中",
            row["deduct_area_m2"], "是" if row["review_required"] else "否",
        ])
    return rows


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# 板图层洞口证据审计",
        "",
        f"- Schema：`{result['schema']}`，图层 `{result['opening_layer']}`。",
        f"- 图层实体 {summary['source_entity_count']} 条，"
        f"完成分类 {summary['accounted_entity_count']} 条，"
        f"未分类 {summary['unaccounted_entity_count']} 条。",
        f"- 确认洞口 {summary['confirmed_opening_count']} 个、"
        f"{summary['confirmed_opening_area_m2']:.4f} m2；"
        f"板面毛 {summary['gross_panel_area_m2']:.4f} m2，"
        f"扣洞净 {summary['net_panel_area_m2']:.4f} m2。",
        f"- 判为引出线/标注 {summary['annotation_record_count']} 组，"
        f"图框外重复 {summary['out_of_frame_count']} 组。",
        f"- 仍需人工复核 {summary['review_required_count']} 组"
        f"（句柄 {'、'.join(summary['review_handles']) or '无'}），"
        f"包络上限 {summary['review_envelope_area_upper_bound_m2']:.4f} m2、"
        f"体积上限 {summary['review_volume_upper_bound_m3']:.4f} m3，"
        "均未计入扣减。",
        f"- 历史候选板 {summary['prior_candidate_panel_count']} 个："
        f"已解释 {summary['prior_candidate_explained_panel_count']} 个、"
        f"待复核 {summary['prior_candidate_review_panel_count']} 个。",
        f"- 实体台账闭合 `{'是' if summary['entity_ledger_closed'] else '否'}`、"
        f"洞口全部闭合 `{'是' if summary['openings_closed'] else '否'}`、"
        "`formal_ready=false`。",
        "",
        "## 逐条证据",
        "",
        "| 句柄 | 状态 | 包络m2 | 扣减m2 | 板面 | 自由端 | 证据 |",
        "|---|---|---:|---:|---|---:|---|",
    ]
    for row in result["records"]:
        lines.append(
            f"| {'+'.join(row.get('handles') or [])} | {row['status']} | "
            f"{_number(row.get('envelope_area_m2')):.4f} | "
            f"{_number(row.get('deduct_area_m2')):.4f} | "
            f"{_text(row.get('panel_id')) or '-'} | "
            f"{int(_number(row.get('free_end_count')))} | "
            f"{_text(row.get('evidence'))} |")
    lines += [
        "",
        "## 历史候选对账",
        "",
        "| 板编号 | 板面积m2 | 原句柄 | 当前状态 | 待复核 |",
        "|---|---:|---|---|---|",
    ]
    for row in result["prior_candidate_reconciliation"]:
        lines.append(
            f"| {row['panel_id']} | {_number(row['panel_area_m2']):.4f} | "
            f"{'+'.join(row['prior_handles'])} | "
            f"{','.join(row['current_statuses']) or '未命中'} | "
            f"{'是' if row['review_required'] else '否'} |")
    conflicts = result["panel_envelope_conflicts"]
    if conflicts:
        lines += ["", "## 板面与洞口包络重合", ""]
        for row in conflicts:
            lines.append(
                f"- {row['panel_id']} ↔ {'+'.join(row['handles'])}"
                f"（{row['status']}）：{row['note']}")
    lines += [
        "",
        "## 结论",
        "",
        "- 只有围合成环的图形参与扣减；开放折线和单线段不扣板面积。",
        "- "
        + _text((summary.get("gap_consistency") or {}).get("note")),
        ("- 待复核折线可在板边线、降板边线、墙、柱和连梁图层上找到方形闭合环，"
         "需要人工确认是否升级为洞口。"
         if summary.get("review_boundary_closure_found")
         else "- 待复核折线在板边线、降板边线、墙、柱和连梁图层上均未找到闭合环，"
              "几何上不具备洞口边界证据。"),
        "- 待复核项只给上限，不改写统一候选总量。",
        "- 板洞口升级为正式量前，需要人工在图上确认待复核折线的真实含义。",
    ]
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="审计板图层洞口证据并核对历史洞口候选")
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--geometry-dxf", default=None)
    parser.add_argument("--entities-json", default=None,
                        help="已抽取的板图层实体 JSON，用于复算或测试")
    parser.add_argument("--prior-json", default=None)
    parser.add_argument("--slab-transform", default=None,
                        help="形如 -117804.129,2540.754；缺省读模型 slab_transform")
    parser.add_argument("--closure-layers",
                        default=",".join(DEFAULT_CLOSURE_LAYERS))
    parser.add_argument("--junction-tolerance-mm", type=float, default=2.0)
    parser.add_argument("--min-opening-area-m2", type=float, default=0.01)
    parser.add_argument("--leader-strip-max-mm", type=float, default=600.0)
    parser.add_argument("--frame-margin-mm", type=float, default=1000.0)
    parser.add_argument("--closure-tolerance-mm", type=float, default=50.0)
    parser.add_argument("--closure-search-margin-mm", type=float, default=12000.0)
    parser.add_argument("--reference-gap-m3", type=float, default=None,
                        help="CAD 候选合计与参考量的差额，用于待复核洞口一致性判定")
    parser.add_argument("--no-closure-probe", action="store_true")
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    model_path = Path(args.model_json)
    if not model_path.exists():
        parser.error(f"缺少模型 JSON：{model_path}")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    closure_layers = tuple(
        layer.strip() for layer in _text(args.closure_layers).split(",")
        if layer.strip())
    if args.geometry_dxf:
        dxf_path = Path(args.geometry_dxf)
        if not dxf_path.exists():
            parser.error(f"缺少几何 DXF：{dxf_path}")
        raw = _read_entities(dxf_path, {OPENING_LAYER} | set(closure_layers))
    elif args.entities_json:
        raw = json.loads(
            Path(args.entities_json).read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            raw = raw.get("entities") or raw.get("opening_entities") or []
    else:
        parser.error("必须提供 --geometry-dxf 或 --entities-json")
    prior = {}
    if args.prior_json:
        prior_path = Path(args.prior_json)
        if prior_path.exists():
            prior = json.loads(prior_path.read_text(encoding="utf-8"))
    if args.slab_transform:
        transform = tuple(
            float(value) for value in args.slab_transform.split(",", 1))
    else:
        value = model.get("slab_transform") or [0.0, 0.0]
        transform = (_number(value[0]), _number(value[1]))
    result = build_audit(
        list(raw),
        model,
        prior,
        transform,
        {
            "junction_tolerance_mm": args.junction_tolerance_mm,
            "min_opening_area_m2": args.min_opening_area_m2,
            "leader_strip_max_mm": args.leader_strip_max_mm,
            "frame_margin_mm": args.frame_margin_mm,
            "closure_tolerance_mm": args.closure_tolerance_mm,
            "closure_search_margin_mm": args.closure_search_margin_mm,
            "reference_gap_m3": (
                args.reference_gap_m3
                if args.reference_gap_m3 is not None else -1.0),
        },
        closure_layers,
        not args.no_closure_probe,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    json_path = out.with_suffix(".json")
    csv_path = out.with_suffix(".csv")
    md_path = out.with_suffix(".md")
    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle).writerows(csv_rows(result))
    md_path.write_text(render_markdown(result), encoding="utf-8")
    checksums = out.with_name(out.name + ".sha256")
    checksums.write_text("\n".join(
        f"{sha256(path)}  {path.resolve()}"
        for path in (json_path, csv_path, md_path)) + "\n", encoding="utf-8")
    summary = result["summary"]
    print(json.dumps({
        "source_entity_count": summary["source_entity_count"],
        "confirmed_opening_count": summary["confirmed_opening_count"],
        "confirmed_opening_area_m2": summary["confirmed_opening_area_m2"],
        "net_panel_area_m2": summary["net_panel_area_m2"],
        "review_required_count": summary["review_required_count"],
        "entity_ledger_closed": summary["entity_ledger_closed"],
        "openings_closed": summary["openings_closed"],
        "outputs": [str(json_path), str(csv_path), str(md_path), str(checksums)],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
