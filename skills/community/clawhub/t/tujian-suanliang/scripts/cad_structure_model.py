#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cad_structure_model.py - 把展开后的梁、墙柱和板几何组装成可复核结构模型。

第一阶段目标不是直接替代广联达，而是建立稳定的数据链：
  梁中心线对象 + 墙柱/板展开 DXF -> 构件对象 -> 净跨/闭合状态 -> 混凝土台账

当前可信度分级：
  * 梁：保留中心线粗方量，并尝试用墙柱支座区间计算逐跨净长。
  * 柱：只接收平面图中可闭合的矩形候选。
  * 墙：接收平行边界配成的中心线候选，暂不处理门窗洞口。
  * 板：接收闭合边界环路；开放链只输出缺口，不计算方量。

所有推测和缺口都写入输出，不把不完整模型包装成结算量。
"""



from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import argparse
import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Optional

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
VENDOR_DIR = SKILL_DIR / "vendor"
if VENDOR_DIR.exists():
    sys.path.insert(0, str(VENDOR_DIR))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import cad_beam_objects  # noqa: E402


DEFAULT_SUPPORT_LAYERS = (
    r"S-剪力墙$|S-剪力墙-边缘构件$|S-柱$|砼墙|A-WALL$|"
    r"A-COLUMN$|COLU_LC$"
)
DEFAULT_WALL_LAYERS = (
    r"S-剪力墙$|砼墙|A-WALL$"
)
DEFAULT_EDGE_MEMBER_LAYERS = r"S-剪力墙-边缘构件$"
DEFAULT_COLUMN_LAYERS = r"S-柱$|A-COLUMN$|COLU_LC$"
DEFAULT_SLAB_LAYERS = (
    r"S-板-板边线|S-板-降板填充|82-板-降板边线|"
    r"S-板-轮廓线|S-SLAB"
)
DEFAULT_SLAB_BOUNDARY_LAYERS = (
    r"S-板-板边线|S-板-降板填充|82-板-降板边线|"
    r"S-梁-虚线|S-梁-实线|砼墙|S-剪力墙$|S-柱$|A-COLUMN$"
)
DEFAULT_OPENING_LAYERS = r"S-板-开洞|OPENING|HOLE"
DEFAULT_COMPONENT_TEXT_LAYER = r"S-剪力墙-构件文字"
DEFAULT_EDGE_MEMBER_LABEL_PATTERN = r"^(?:YBZ|GBZ|QZ)\d+[A-Za-z]?$"
DEFAULT_COLUMN_LABEL_PATTERN = r"^KZ\d+[A-Za-z]?$"
DEFAULT_SLAB_THICKNESS_TEXT_LAYER = r"S-板-板厚"
DEFAULT_SLAB_HATCH_LAYERS = r"S-板-降板填充"
DEFAULT_SLAB_NOTE_LAYER = r"S-文字说明"
DEFAULT_AUTO_ALIGN_LAYERS = (
    r"S-梁-虚线|S-梁-实线|BEAM|砼墙|S-剪力墙$|"
    r"S-剪力墙-边缘构件$|S-柱$|S-板-板边线|降板边线"
)


def _parse_transform(value: Optional[str]) -> tuple[float, float] | str:
    if not value:
        return (0.0, 0.0)
    if str(value).strip().lower() == "auto":
        return "auto"
    try:
        parts = [float(v.strip()) for v in str(value).split(",")]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("变换必须是 dx,dy") from exc
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("变换必须是 dx,dy")
    return (parts[0], parts[1])


def _round(value: Any, digits: int = 3) -> float:
    try:
        return round(float(value), digits)
    except (TypeError, ValueError):
        return 0.0


def _merge_intervals(items: list[tuple[float, float]],
                     gap: float = 10.0) -> list[tuple[float, float]]:
    out: list[list[float]] = []
    for lo, hi in sorted((float(a), float(b)) for a, b in items if b > a):
        if not out or lo - out[-1][1] > gap:
            out.append([lo, hi])
        else:
            out[-1][1] = max(out[-1][1], hi)
    return [(a, b) for a, b in out]


def _segment_length(seg: dict[str, Any]) -> float:
    return max(0.0, float(seg["hi"]) - float(seg["lo"]))


def _shift_segment(seg: dict[str, Any],
                   dx: float,
                   dy: float) -> dict[str, Any]:
    shifted = dict(seg)
    shifted["a"] = (float(seg["a"][0]) + dx, float(seg["a"][1]) + dy)
    shifted["b"] = (float(seg["b"][0]) + dx, float(seg["b"][1]) + dy)
    if str(seg["orientation"]) == "H":
        shifted["const"] = float(seg["const"]) + dy
        shifted["lo"] = float(seg["lo"]) + dx
        shifted["hi"] = float(seg["hi"]) + dx
    else:
        shifted["const"] = float(seg["const"]) + dx
        shifted["lo"] = float(seg["lo"]) + dy
        shifted["hi"] = float(seg["hi"]) + dy
    return shifted


def _filter_segments_to_bbox(
        segments: list[dict[str, Any]],
        bbox: Optional[list[float]],
        margin_mm: float = 5000.0) -> list[dict[str, Any]]:
    if not bbox or len(bbox) != 4:
        return segments
    x0, y0, x1, y1 = [float(value) for value in bbox]
    return [
        segment for segment in segments
        if (x0 - margin_mm <= min(float(segment["a"][0]), float(segment["b"][0]))
            and max(float(segment["a"][0]), float(segment["b"][0])) <= x1 + margin_mm
            and y0 - margin_mm <= min(float(segment["a"][1]), float(segment["b"][1]))
            and max(float(segment["a"][1]), float(segment["b"][1])) <= y1 + margin_mm)
    ]


def _same_layer_translation(
        anchors: list[dict[str, Any]],
        sources: list[dict[str, Any]],
        length_tol: float = 5.0,
        quantize_mm: float = 5.0) -> Optional[dict[str, Any]]:
    """用同名图层的等长线段配对，优先恢复真正共享的结构几何。"""
    source_layers = {str(row.get("layer") or "") for row in sources}
    votes: dict[tuple[float, float], list[tuple[int, int]]] = defaultdict(list)

    def pair_shift(anchor: dict[str, Any],
                   source: dict[str, Any]) -> tuple[float, float]:
        if str(anchor["orientation"]) == "H":
            return (
                (float(anchor["lo"]) + float(anchor["hi"])) / 2.0
                - (float(source["lo"]) + float(source["hi"])) / 2.0,
                float(anchor["const"]) - float(source["const"]),
            )
        return (
            float(anchor["const"]) - float(source["const"]),
            (float(anchor["lo"]) + float(anchor["hi"])) / 2.0
            - (float(source["lo"]) + float(source["hi"])) / 2.0,
        )

    for anchor_idx, anchor in enumerate(anchors):
        layer = str(anchor.get("layer") or "")
        if not layer or layer not in source_layers:
            continue
        anchor_len = _segment_length(anchor)
        for source_idx, source in enumerate(sources):
            if str(source.get("layer") or "") != layer:
                continue
            if str(source["orientation"]) != str(anchor["orientation"]):
                continue
            if abs(_segment_length(source) - anchor_len) > length_tol:
                continue
            dx, dy = pair_shift(anchor, source)
            key = (
                round(dx / quantize_mm) * quantize_mm,
                round(dy / quantize_mm) * quantize_mm,
            )
            votes[key].append((anchor_idx, source_idx))

    if not votes:
        return None

    ranked: list[dict[str, Any]] = []
    for (dx, dy), pair_votes in votes.items():
        if len(pair_votes) < 2:
            continue
        matched_anchors: dict[int, int] = {}
        matched_sources: dict[int, int] = {}
        layer_anchor_totals: Counter[str] = Counter()
        layer_source_totals: Counter[str] = Counter()
        for anchor_idx, source_idx in pair_votes:
            matched_anchors.setdefault(anchor_idx, source_idx)
            matched_sources.setdefault(source_idx, anchor_idx)
        for anchor_idx in matched_anchors:
            layer_anchor_totals[str(anchors[anchor_idx].get("layer") or "")] += 1
        for source_idx in matched_sources:
            layer_source_totals[str(sources[source_idx].get("layer") or "")] += 1

        matched_anchor_length = sum(
            _segment_length(anchors[idx]) for idx in matched_anchors)
        matched_source_length = sum(
            _segment_length(sources[idx]) for idx in matched_sources)
        ratios = []
        for layer, count in layer_anchor_totals.items():
            layer_anchor_total = sum(
                1 for row in anchors if str(row.get("layer") or "") == layer)
            layer_source_total = sum(
                1 for row in sources if str(row.get("layer") or "") == layer)
            if layer_anchor_total and layer_source_total:
                ratios.append(min(
                    count / layer_anchor_total,
                    layer_source_totals[layer] / layer_source_total,
                ))
        quality = (min(ratios) if ratios else 0.0) * (
            matched_anchor_length + matched_source_length)
        ranked.append({
            "dx": float(dx),
            "dy": float(dy),
            "matched_anchor_count": len(matched_anchors),
            "matched_source_count": len(matched_sources),
            "matched_anchor_length_mm": _round(matched_anchor_length, 1),
            "matched_source_length_mm": _round(matched_source_length, 1),
            "match_quality": _round(quality, 3),
            "layers": [
                layer for layer, _ in layer_anchor_totals.most_common()
            ],
            "quantized_transform": [float(dx), float(dy)],
        })
    if not ranked:
        return None
    ranked.sort(
        key=lambda row: (
            row["match_quality"],
            row["matched_anchor_count"],
            min(row["matched_anchor_length_mm"], row["matched_source_length_mm"]),
        ),
        reverse=True,
    )
    best = ranked[0]
    if best["matched_anchor_count"] < 2:
        return None
    quantized_key = (
        float(best["quantized_transform"][0]),
        float(best["quantized_transform"][1]),
    )
    exact_pairs = votes.get(quantized_key) or []
    if exact_pairs:
        exact_shifts = [
            pair_shift(anchors[anchor_idx], sources[source_idx])
            for anchor_idx, source_idx in exact_pairs
        ]
        best["dx"] = _median([row[0] for row in exact_shifts])
        best["dy"] = _median([row[1] for row in exact_shifts])
        best["transform"] = [best["dx"], best["dy"]]
    return {
        "mode": "same-layer-shape",
        "transform": [best["dx"], best["dy"]],
        "selected": best,
        "candidates": ranked[:5],
        "anchor_line_count": len(anchors),
        "source_line_count": len(sources),
    }


def estimate_translation(anchor_dxf: Path,
                         source_dxf: Path,
                         layer_pattern: str,
                         target_bbox: list[float],
                         beam_rows: Optional[list[dict[str, Any]]] = None,
                         support_max_width_mm: float = 1200.0,
                         length_tol: float = 5.0,
                         quantize_mm: float = 100.0,
                         candidate_limit: int = 32) -> dict[str, Any]:
    """按同方向、近等长线段投票估计 dx/dy，再用目标图框内覆盖长度复核。"""
    anchors = _read_line_segments(anchor_dxf, layer_pattern, (0.0, 0.0))
    sources = _read_line_segments(source_dxf, layer_pattern, (0.0, 0.0))
    if not anchors or not sources:
        raise ValueError("自动配准失败：锚点图或来源图没有匹配图层线段")

    same_layer = _same_layer_translation(
        anchors, sources, length_tol=length_tol, quantize_mm=quantize_mm)
    if same_layer:
        best = same_layer["selected"]
        shifted = [_shift_segment(row, best["dx"], best["dy"]) for row in sources]
        inside_length = 0.0
        inside_count = 0
        x0, y0, x1, y1 = [float(v) for v in target_bbox]
        margin = max(10000.0, max(x1 - x0, y1 - y0) * 0.08)
        for row in shifted:
            ax, ay = row["a"]
            bx, by = row["b"]
            if (x0 - margin <= ax <= x1 + margin
                    and y0 - margin <= ay <= y1 + margin
                    and x0 - margin <= bx <= x1 + margin
                    and y0 - margin <= by <= y1 + margin):
                inside_length += _segment_length(row)
                inside_count += 1
        best["inside_length_mm"] = _round(inside_length, 1)
        best["inside_line_count"] = inside_count
        return same_layer

    source_index: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for seg in sources:
        source_index[(str(seg["orientation"]),
                      int(round(_segment_length(seg) / length_tol)))].append(seg)

    votes: Counter[tuple[float, float]] = Counter()
    for anchor in anchors:
        key = (str(anchor["orientation"]),
               int(round(_segment_length(anchor) / length_tol)))
        a_len = _segment_length(anchor)
        weight = math.sqrt(max(1.0, a_len))
        for source in source_index.get(key, []):
            if abs(a_len - _segment_length(source)) > length_tol:
                continue
            for (source_at, anchor_at) in (
                    (source["lo"], anchor["lo"]),
                    (source["hi"], anchor["hi"])):
                dx = round((float(anchor_at) - float(source_at)) / quantize_mm) * quantize_mm
                dy = round((float(anchor["const"]) - float(source["const"]))
                           / quantize_mm) * quantize_mm
                votes[(dx, dy)] += weight

    if not votes:
        raise ValueError("自动配准失败：没有找到近等长构件线")

    x0, y0, x1, y1 = [float(v) for v in target_bbox]
    margin = max(10000.0, max(x1 - x0, y1 - y0) * 0.08)
    ranked: list[dict[str, Any]] = []
    for (dx, dy), vote in votes.most_common(candidate_limit):
        inside_length = 0.0
        inside_count = 0
        transformed: list[dict[str, Any]] = []
        for seg in sources:
            ax = float(seg["a"][0]) + dx
            ay = float(seg["a"][1]) + dy
            bx = float(seg["b"][0]) + dx
            by = float(seg["b"][1]) + dy
            shifted = dict(seg)
            shifted["a"] = (ax, ay)
            shifted["b"] = (bx, by)
            if str(seg["orientation"]) == "H":
                shifted["const"] = float(seg["const"]) + dy
                shifted["lo"] = float(seg["lo"]) + dx
                shifted["hi"] = float(seg["hi"]) + dx
            else:
                shifted["const"] = float(seg["const"]) + dx
                shifted["lo"] = float(seg["lo"]) + dy
                shifted["hi"] = float(seg["hi"]) + dy
            transformed.append(shifted)
            if (x0 - margin <= ax <= x1 + margin
                    and y0 - margin <= ay <= y1 + margin
                    and x0 - margin <= bx <= x1 + margin
                    and y0 - margin <= by <= y1 + margin):
                inside_length += _segment_length(seg)
                inside_count += 1
        clear_span_count = 0
        support_count = 0
        if beam_rows:
            support_runs = _pair_parallel_runs(
                transformed, 50.0, support_max_width_mm, overlap_min=50.0)
            for beam_row in beam_rows:
                quantity = _clear_span_quantity(
                    beam_row, support_runs, support_max_width_mm, 300.0, 300.0)
                support_count += int(quantity.get("support_count") or 0)
                if quantity.get("status") == "clear-span":
                    clear_span_count += 1
        ranked.append({
            "dx": float(dx),
            "dy": float(dy),
            "vote": _round(vote, 3),
            "inside_length_mm": _round(inside_length, 1),
            "inside_line_count": inside_count,
            "clear_span_count": clear_span_count,
            "support_count": support_count,
            "score": _round(
                clear_span_count * 1e12
                + support_count * 1e8
                + inside_length
                + vote * 0.5,
                3,
            ),
        })
    ranked.sort(key=lambda row: (
        row["clear_span_count"], row["support_count"],
        row["inside_length_mm"], row["vote"]), reverse=True)
    best = ranked[0]
    return {
        "mode": "auto",
        "transform": [best["dx"], best["dy"]],
        "selected": best,
        "candidates": ranked[:5],
        "anchor_line_count": len(anchors),
        "source_line_count": len(sources),
    }


def _read_line_segments(path: Path, layer_pattern: str,
                        transform: tuple[float, float]) -> list[dict[str, Any]]:
    from dev_dxf import readfile

    doc = readfile(str(path))
    pat = re.compile(layer_pattern, re.I)
    out: list[dict[str, Any]] = []
    tx, ty = transform
    for entity in doc.modelspace():
        if entity.dxftype() != "LINE":
            continue
        layer = str(entity.dxf.layer or "")
        if layer == "__SHEET_BBOX" or not pat.search(layer):
            continue
        a = entity.dxf.start
        b = entity.dxf.end
        ax, ay = float(a.x) + tx, float(a.y) + ty
        bx, by = float(b.x) + tx, float(b.y) + ty
        if abs(bx - ax) + abs(by - ay) < 1e-4:
            continue
        if abs(by - ay) <= abs(bx - ax) * 0.02:
            orientation = "H"
            const = (ay + by) / 2.0
            lo, hi = sorted((ax, bx))
        elif abs(bx - ax) <= abs(by - ay) * 0.02:
            orientation = "V"
            const = (ax + bx) / 2.0
            lo, hi = sorted((ay, by))
        else:
            continue
        out.append({
            "orientation": orientation,
            "const": const,
            "lo": lo,
            "hi": hi,
            "layer": layer,
            "a": (ax, ay),
            "b": (bx, by),
        })
    return out


def _group_segments(segments: list[dict[str, Any]],
                    lateral_tol: float = 12.5) -> dict[tuple[str, int], list[dict[str, Any]]]:
    groups: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for seg in segments:
        key = (str(seg["orientation"]), int(round(float(seg["const"]) / lateral_tol)))
        groups[key].append(seg)
    return groups


def _median(values: list[float]) -> float:
    values = sorted(float(v) for v in values)
    if not values:
        return 0.0
    mid = len(values) // 2
    if len(values) % 2:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2.0


def _pair_parallel_runs(
        segments: list[dict[str, Any]],
        min_width: float,
        max_width: float,
        lateral_tol: float = 12.5,
        overlap_min: float = 100.0) -> list[dict[str, Any]]:
    """把平行双线配成中心线构件候选，返回墙/梁等线性对象。"""
    groups = _group_segments(segments, lateral_tol)
    keys = sorted(groups)
    out: list[dict[str, Any]] = []
    seen: set[tuple] = set()
    for idx, key1 in enumerate(keys):
        for key2 in keys[idx + 1:]:
            if key1[0] != key2[0]:
                continue
            rows1, rows2 = groups[key1], groups[key2]
            c1 = _median([float(r["const"]) for r in rows1])
            c2 = _median([float(r["const"]) for r in rows2])
            width = abs(c2 - c1)
            if width < min_width or width > max_width:
                continue
            for a in rows1:
                for b in rows2:
                    lo = max(float(a["lo"]), float(b["lo"]))
                    hi = min(float(a["hi"]), float(b["hi"]))
                    if hi - lo < overlap_min:
                        continue
                    center = (float(a["const"]) + float(b["const"])) / 2.0
                    rw = abs(float(a["const"]) - float(b["const"]))
                    dedupe = (
                        key1[0], round(center / 25.0), round(lo / 100.0),
                        round(hi / 100.0), round(rw / 10.0),
                    )
                    if dedupe in seen:
                        continue
                    seen.add(dedupe)
                    out.append({
                        "orientation": key1[0],
                        "center": center,
                        "start": lo,
                        "end": hi,
                        "width_mm": rw,
                        "layers": sorted({str(a["layer"]), str(b["layer"])}),
                    })
    return out


def _merge_collinear_runs(runs: list[dict[str, Any]],
                          center_tol: float = 25.0,
                          gap: float = 25.0) -> list[dict[str, Any]]:
    groups: dict[tuple[str, int, int], list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        key = (
            str(run["orientation"]),
            int(round(float(run["center"]) / center_tol)),
            int(round(float(run["width_mm"]) / 25.0)),
        )
        groups[key].append(run)
    out: list[dict[str, Any]] = []
    for key, rows in groups.items():
        merged = _merge_intervals(
            [(float(r["start"]), float(r["end"])) for r in rows], gap=gap)
        for lo, hi in merged:
            out.append({
                "orientation": key[0],
                "center": _median([float(r["center"]) for r in rows]),
                "start": lo,
                "end": hi,
                "width_mm": _median([float(r["width_mm"]) for r in rows]),
                "layers": sorted({layer for r in rows for layer in r.get("layers", [])}),
            })
    return sorted(out, key=lambda r: (
        str(r["orientation"]), float(r["center"]), float(r["start"])))


def _open_chain_polygons(
        segments: list[dict[str, Any]],
        snap_mm: float = 10.0,
        min_area_m2: float = 0.01,
        max_area_m2: float = 2.0,
        max_gap_mm: float = 1200.0) -> list[dict[str, Any]]:
    """把只剩缺口的简单链闭合为边缘构件/柱截面，并保留闭合依据。"""
    nodes: dict[tuple[int, int], tuple[float, float]] = {}
    edges: list[tuple[tuple[int, int], tuple[int, int]]] = []
    adjacency: dict[tuple[int, int], list[int]] = defaultdict(list)

    def node(point: tuple[float, float]) -> tuple[int, int]:
        key = (
            int(round(float(point[0]) / snap_mm)),
            int(round(float(point[1]) / snap_mm)),
        )
        nodes.setdefault(key, (float(point[0]), float(point[1])))
        return key

    for segment in segments:
        a = node((float(segment["a"][0]), float(segment["a"][1])))
        b = node((float(segment["b"][0]), float(segment["b"][1])))
        if a == b:
            continue
        edge_index = len(edges)
        edges.append((a, b))
        adjacency[a].append(edge_index)
        adjacency[b].append(edge_index)

    polygons: list[dict[str, Any]] = []
    for loop in _component_cycles(
            [(nodes[a], nodes[b]) for a, b in edges], snap_mm):
        if loop.get("status") != "closed":
            continue
        area_m2 = float(loop.get("area_m2") or 0.0)
        if not min_area_m2 <= area_m2 <= max_area_m2:
            continue
        points = [
            (float(x), float(y))
            for x, y in (loop.get("points") or [])
        ]
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        polygons.append({
            "area_m2": _round(area_m2, 6),
            "gap_mm": 0.0,
            "edge_count": int(loop.get("edge_count") or 0),
            "points": loop.get("points") or [],
            "bbox": [
                _round(min(xs), 1), _round(min(ys), 1),
                _round(max(xs), 1), _round(max(ys), 1),
            ],
        })

    unused = set(range(len(edges)))
    while unused:
        start_edge = min(unused)
        stack = [start_edge]
        component_edges: set[int] = set()
        while stack:
            edge_index = stack.pop()
            if edge_index in component_edges:
                continue
            component_edges.add(edge_index)
            unused.discard(edge_index)
            for endpoint in edges[edge_index]:
                stack.extend(adjacency[endpoint])

        component_nodes = {
            endpoint for edge_index in component_edges
            for endpoint in edges[edge_index]
        }
        endpoints = sorted(
            endpoint for endpoint in component_nodes
            if len(adjacency[endpoint]) == 1)
        degrees_ok = all(
            len(adjacency[node]) == 2 for node in component_nodes
            if node not in endpoints)
        if len(endpoints) != 2 or not degrees_ok:
            continue

        current = endpoints[0]
        previous_edge = -1
        node_order = [current]
        used_edges: set[int] = set()
        while current != endpoints[1]:
            candidates = [
                edge_index for edge_index in adjacency[current]
                if edge_index != previous_edge and edge_index not in used_edges
            ]
            if not candidates:
                break
            edge_index = candidates[0]
            used_edges.add(edge_index)
            a, b = edges[edge_index]
            current = b if a == current else a
            previous_edge = edge_index
            node_order.append(current)
        if current != endpoints[1] or len(used_edges) != len(component_edges):
            continue

        points = [nodes[node] for node in node_order]
        first, last = points[0], points[-1]
        gap = math.dist(first, last)
        if gap > max_gap_mm:
            continue
        if abs(first[0] - last[0]) > snap_mm and abs(first[1] - last[1]) > snap_mm:
            continue
        area_m2 = _polygon_area(points) / 1e6
        if not min_area_m2 <= area_m2 <= max_area_m2:
            continue
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        polygons.append({
            "area_m2": _round(area_m2, 6),
            "gap_mm": _round(gap, 1),
            "edge_count": len(component_edges),
            "points": [[_round(x, 1), _round(y, 1)] for x, y in points],
            "bbox": [
                _round(min(xs), 1), _round(min(ys), 1),
                _round(max(xs), 1), _round(max(ys), 1),
            ],
        })
    return polygons


def _line_polygon_intervals(
        run: dict[str, Any],
        polygons: list[dict[str, Any]]) -> list[tuple[float, float]]:
    """返回中心线落在多边形内部的区间。"""
    start, end, center = (
        float(run["start"]), float(run["end"]), float(run["center"]))
    if end <= start:
        return []
    orientation = str(run["orientation"])
    cuts = {start, end}
    for polygon in polygons:
        points = [
            (float(x), float(y))
            for x, y in (polygon.get("points") or [])
        ]
        if orientation == "H":
            cuts.update(x for x, _ in points)
        else:
            cuts.update(y for _, y in points)
    ordered = sorted(cut for cut in cuts if start <= cut <= end)
    inside: list[tuple[float, float]] = []
    for left, right in zip(ordered, ordered[1:]):
        if right - left <= 1e-6:
            continue
        midpoint = (left + right) / 2.0
        point = (
            (midpoint, center)
            if orientation == "H" else (center, midpoint)
        )
        if any(_point_in_polygon(
                point,
                [(float(x), float(y))
                 for x, y in (polygon.get("points") or [])])
               for polygon in polygons):
            inside.append((left, right))
    return _merge_intervals(inside, gap=1.0)


def _subtract_intervals(
        start: float,
        end: float,
        intervals: list[tuple[float, float]]) -> list[tuple[float, float]]:
    output: list[tuple[float, float]] = []
    cursor = float(start)
    for left, right in _merge_intervals(intervals, gap=1.0):
        left = max(float(start), float(left))
        right = min(float(end), float(right))
        if right <= cursor:
            continue
        if left > cursor:
            output.append((cursor, left))
        cursor = max(cursor, right)
    if cursor < float(end):
        output.append((cursor, float(end)))
    return [(left, right) for left, right in output if right - left > 1e-6]


def _wall_width_mm(value: float,
                   candidates: tuple[float, ...] = (200.0, 250.0),
                   tolerance: float = 60.0) -> Optional[float]:
    closest = min(candidates, key=lambda candidate: abs(candidate - value))
    if abs(closest - value) <= tolerance:
        return float(closest)
    return None


def _clip_wall_runs(
        runs: list[dict[str, Any]],
        polygons: list[dict[str, Any]],
        min_length_mm: float) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for run in runs:
        inside = _line_polygon_intervals(run, polygons)
        for start, end in _subtract_intervals(
                float(run["start"]), float(run["end"]), inside):
            if end - start < min_length_mm:
                continue
            row = dict(run)
            row["start"] = start
            row["end"] = end
            row["clipped_length_mm"] = _round(
                float(run["end"]) - float(run["start"]) - (end - start), 1)
            output.append(row)
    return _merge_collinear_runs(output)


def _dedupe_overlapping_runs(
        runs: list[dict[str, Any]],
        center_tolerance_mm: float = 75.0,
        overlap_ratio: float = 0.8) -> list[dict[str, Any]]:
    kept: list[dict[str, Any]] = []
    for row in sorted(
            runs,
            key=lambda item: (
                float(item["end"]) - float(item["start"]),
                -float(item["width_mm"]),
            ),
            reverse=True,
    ):
        duplicate = False
        for existing in kept:
            if str(row["orientation"]) != str(existing["orientation"]):
                continue
            if abs(float(row["center"]) - float(existing["center"])) > center_tolerance_mm:
                continue
            overlap = max(
                0.0,
                min(float(row["end"]), float(existing["end"]))
                - max(float(row["start"]), float(existing["start"])),
            )
            shortest = min(
                float(row["end"]) - float(row["start"]),
                float(existing["end"]) - float(existing["start"]),
            )
            if shortest > 0 and overlap / shortest >= overlap_ratio:
                duplicate = True
                break
        if not duplicate:
            kept.append(row)
    return sorted(kept, key=lambda item: (
        str(item["orientation"]), float(item["center"]), float(item["start"])))


def _split_axis_segments(
        segments: list[dict[str, Any]]) -> tuple[
            dict[tuple[int, int], tuple[float, float]],
            list[tuple[tuple[int, int], tuple[int, int]]]]:
    """切分轴线交点并去重，为板面环路提供平面线框。"""
    x_values = sorted({
        float(point)
        for segment in segments
        for point in (
            float(segment["a"][0]), float(segment["b"][0]))
    })
    y_values = sorted({
        float(point)
        for segment in segments
        for point in (
            float(segment["a"][1]), float(segment["b"][1]))
    })

    def merge_axis(values: list[float], tolerance: float = 5.0) -> list[float]:
        merged: list[float] = []
        for value in values:
            if not merged or value - merged[-1] > tolerance:
                merged.append(value)
            else:
                merged[-1] = (merged[-1] + value) / 2.0
        return merged

    xs = merge_axis(x_values)
    ys = merge_axis(y_values)
    nodes: dict[tuple[int, int], tuple[float, float]] = {}
    edge_keys: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    edges: list[tuple[tuple[int, int], tuple[int, int]]] = []

    def nearest(value: float, values: list[float]) -> float:
        if not values:
            return value
        index = min(
            range(len(values)),
            key=lambda idx: abs(values[idx] - value),
        )
        return values[index]

    def node(point: tuple[float, float]) -> tuple[int, int]:
        key = (int(round(point[0] / 5.0)), int(round(point[1] / 5.0)))
        nodes.setdefault(key, point)
        return key

    for segment in segments:
        if str(segment["orientation"]) == "H":
            axis = nearest(
                (float(segment["a"][1]) + float(segment["b"][1])) / 2.0, ys)
            start, end = sorted((
                float(segment["a"][0]), float(segment["b"][0])))
            cuts = [start, end]
            cuts.extend(
                value for value in xs
                if start - 5.0 <= value <= end + 5.0)
            points = [(value, axis) for value in sorted(set(cuts))]
        else:
            axis = nearest(
                (float(segment["a"][0]) + float(segment["b"][0])) / 2.0, xs)
            start, end = sorted((
                float(segment["a"][1]), float(segment["b"][1])))
            cuts = [start, end]
            cuts.extend(
                value for value in ys
                if start - 5.0 <= value <= end + 5.0)
            points = [(axis, value) for value in sorted(set(cuts))]
        for first, second in zip(points, points[1:]):
            if math.dist(first, second) <= 1.0:
                continue
            edge = tuple(sorted((node(first), node(second))))
            if edge in edge_keys:
                continue
            edge_keys.add(edge)
            edges.append(edge)
    return nodes, edges


def _planar_face_polygons(
        segments: list[dict[str, Any]],
        min_area_m2: float = 1.0) -> list[dict[str, Any]]:
    nodes, edges = _split_axis_segments(segments)
    if not edges:
        return []
    adjacency: dict[tuple[int, int], list[int]] = defaultdict(list)
    directed: list[tuple[tuple[int, int], tuple[int, int]]] = []
    directed_index: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
    for edge_index, (a, b) in enumerate(edges):
        adjacency[a].append(edge_index)
        adjacency[b].append(edge_index)
        directed_index[(a, b)] = len(directed)
        directed.append((a, b))
        directed_index[(b, a)] = len(directed)
        directed.append((b, a))

    def angle(a: tuple[int, int], b: tuple[int, int]) -> float:
        ax, ay = nodes[a]
        bx, by = nodes[b]
        return math.atan2(by - ay, bx - ax)

    used: set[int] = set()
    faces: list[dict[str, Any]] = []
    for start in range(len(directed)):
        if start in used:
            continue
        face: list[int] = []
        current = start
        for _ in range(len(directed) + 1):
            if current in used:
                break
            used.add(current)
            face.append(current)
            a, b = directed[current]
            reverse_angle = angle(b, a)
            candidates: list[tuple[float, tuple[int, int]]] = []
            for edge_index in adjacency[b]:
                x, y = edges[edge_index]
                other = y if x == b else x
                delta = (reverse_angle - angle(b, other)) % (2.0 * math.pi)
                if delta < 1e-9:
                    delta = 2.0 * math.pi
                candidates.append((delta, other))
            if not candidates:
                break
            _, other = min(candidates)
            current = directed_index[(b, other)]
            if current == start:
                break
        if current != start or len(face) < 3:
            continue
        points = [nodes[directed[index][0]] for index in face]
        signed_area_m2 = 0.0
        for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
            signed_area_m2 += x1 * y2 - x2 * y1
        signed_area_m2 /= 2e6
        if signed_area_m2 <= 0:
            continue
        area_m2 = abs(signed_area_m2)
        if area_m2 < min_area_m2:
            continue
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        faces.append({
            "area_m2": _round(area_m2, 4),
            "signed_area_m2": _round(signed_area_m2, 4),
            "points": [[_round(x, 1), _round(y, 1)] for x, y in points],
            "bbox": [
                _round(min(xs), 1), _round(min(ys), 1),
                _round(max(xs), 1), _round(max(ys), 1),
            ],
        })
    return sorted(faces, key=lambda row: row["area_m2"], reverse=True)


def _interval_on_axis(run: dict[str, Any], orientation: str,
                      axis: float, max_width: float,
                      crossing_tolerance_mm: float = 0.0
                      ) -> Optional[tuple[float, float]]:
    """返回墙柱沿目标梁轴方向的占用区间。"""
    center = float(run["center"])
    width = float(run["width_mm"])
    lo, hi = float(run["start"]), float(run["end"])
    if str(run["orientation"]) != orientation:
        tolerance = max(0.0, float(crossing_tolerance_mm))
        if lo - tolerance - 1e-6 <= axis <= hi + tolerance + 1e-6:
            return (center - width / 2.0, center + width / 2.0)
        return None
    if abs(center - axis) <= max_width / 2.0:
        return (lo, hi)
    return None


def _beam_intersection_support_runs(
        runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """把全图梁拓扑段转换成另一方向梁的交叉支座候选。"""
    support_runs: list[dict[str, Any]] = []
    for run in runs:
        orientation = str(run.get("orientation") or "")
        if orientation not in ("H", "V"):
            continue
        width = run.get("section_b_mm") or run.get("paired_width_mm")
        try:
            width = float(width)
            center = float(run["axis_mm"])
            start = float(run["start_mm"])
            end = float(run["end_mm"])
        except (KeyError, TypeError, ValueError):
            continue
        if width <= 0 or end <= start:
            continue
        support_runs.append({
            "id": run.get("id"),
            "code": run.get("matched_code") or "",
            "orientation": orientation,
            "center": center,
            "start": start,
            "end": end,
            "width_mm": width,
            "section_h_mm": run.get("section_h_mm"),
            "source": "beam-intersection",
        })
    return support_runs


def _cluster_support_candidates(
        candidates: list[dict[str, Any]],
        tolerance_mm: float = 400.0) -> list[dict[str, Any]]:
    """把同一支座节点附近的墙段/梁段证据合并为一个候选。"""
    clusters: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda row: float(row["center_mm"])):
        center = float(candidate["center_mm"])
        if clusters:
            current = clusters[-1]
            if abs(center - float(current["center_mm"])) <= tolerance_mm:
                current["members"].append(candidate)
                current["start_mm"] = min(
                    float(current["start_mm"]), float(candidate["start_mm"]))
                current["end_mm"] = max(
                    float(current["end_mm"]), float(candidate["end_mm"]))
                current["center_mm"] = (
                    float(current["start_mm"]) + float(current["end_mm"])
                ) / 2.0
                current["score"] = max(
                    float(current["score"]), float(candidate["score"]))
                current["requires_review"] = bool(
                    current["requires_review"]
                    or candidate.get("requires_review"))
                continue
        clusters.append({
            "start_mm": float(candidate["start_mm"]),
            "end_mm": float(candidate["end_mm"]),
            "center_mm": center,
            "score": float(candidate["score"]),
            "requires_review": bool(candidate.get("requires_review")),
            "members": [candidate],
        })
    return clusters


def _select_support_clusters(
        clusters: list[dict[str, Any]],
        start_mm: float,
        end_mm: float,
        end_tolerance_mm: float,
        expected_count: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """按端点优先、证据分优先，选出与编号跨数一致的候选支座。"""
    if expected_count < 0 or len(clusters) <= expected_count:
        return clusters, []
    selected: set[int] = set()
    endpoint_candidates: list[tuple[float, float, int]] = []
    for index, cluster in enumerate(clusters):
        lo = float(cluster["start_mm"])
        hi = float(cluster["end_mm"])
        if lo <= start_mm + end_tolerance_mm and hi >= start_mm - end_tolerance_mm:
            endpoint_candidates.append(
                (0.0, -float(cluster["score"]), index))
        if lo <= end_mm + end_tolerance_mm and hi >= end_mm - end_tolerance_mm:
            endpoint_candidates.append(
                (1.0, -float(cluster["score"]), index))
    for _, _, index in sorted(endpoint_candidates):
        if len(selected) >= expected_count:
            break
        selected.add(index)
    remaining = [
        index for index in range(len(clusters)) if index not in selected
    ]
    remaining.sort(key=lambda index: (
        -float(clusters[index]["score"]),
        float(clusters[index]["center_mm"]),
    ))
    for index in remaining:
        if len(selected) >= expected_count:
            break
        selected.add(index)
    accepted = [cluster for index, cluster in enumerate(clusters)
                if index in selected]
    rejected = [cluster for index, cluster in enumerate(clusters)
                if index not in selected]
    return accepted, rejected


def _rectangles_from_runs(horizontal: list[dict[str, Any]],
                          vertical: list[dict[str, Any]],
                          max_size: float = 2000.0,
                          tol: float = 40.0) -> list[dict[str, Any]]:
    """由两组正交中心线候选交叉生成平面矩形柱候选。"""
    out: list[dict[str, Any]] = []
    for h in horizontal:
        h_lo, h_hi = float(h["start"]), float(h["end"])
        h_center = float(h["center"])
        h_width = float(h["width_mm"])
        if h_hi - h_lo > max_size * 1.4 or h_width > max_size:
            continue
        for v in vertical:
            v_lo, v_hi = float(v["start"]), float(v["end"])
            v_center = float(v["center"])
            v_width = float(v["width_mm"])
            if v_hi - v_lo > max_size * 1.4 or v_width > max_size:
                continue
            x0, x1 = v_center - v_width / 2.0, v_center + v_width / 2.0
            y0, y1 = h_center - h_width / 2.0, h_center + h_width / 2.0
            if not (x0 - tol <= v_center <= x1 + tol
                    and h_lo - tol <= v_center <= h_hi + tol):
                continue
            if not (y0 - tol <= h_center <= y1 + tol
                    and v_lo - tol <= h_center <= v_hi + tol):
                continue
            width, height = x1 - x0, y1 - y0
            if width < 100.0 or height < 100.0:
                continue
            geometry_tol = max(tol, min(width, height) * 0.5)
            if not (h_lo <= x0 + geometry_tol
                    and h_hi >= x1 - geometry_tol
                    and v_lo <= y0 + geometry_tol
                    and v_hi >= y1 - geometry_tol):
                continue
            out.append({
                "x0": x0, "x1": x1, "y0": y0, "y1": y1,
                "b_mm": width, "h_mm": height,
                "layers": sorted(set(h.get("layers", [])) | set(v.get("layers", []))),
            })

    deduped: list[dict[str, Any]] = []
    for rect in sorted(out, key=lambda r: (r["x0"], r["y0"], r["x1"], r["y1"])):
        duplicate = False
        for kept in deduped:
            ix = max(0.0, min(rect["x1"], kept["x1"]) - max(rect["x0"], kept["x0"]))
            iy = max(0.0, min(rect["y1"], kept["y1"]) - max(rect["y0"], kept["y0"]))
            inter = ix * iy
            area1 = (rect["x1"] - rect["x0"]) * (rect["y1"] - rect["y0"])
            area2 = (kept["x1"] - kept["x0"]) * (kept["y1"] - kept["y0"])
            if inter / max(1.0, min(area1, area2)) > 0.85:
                duplicate = True
                break
        if not duplicate:
            deduped.append(rect)
    return deduped


def build_support_model(
        support_dxf: Optional[Path],
        support_layers: str,
        wall_layers: str,
        edge_member_layers: str,
        column_layers: str,
        support_transform: tuple[float, float],
        max_support_width: float,
        min_candidate_length: float,
        model_bbox: Optional[list[float]] = None,
        wall_width_tolerance_mm: float = 60.0) -> dict[str, Any]:
    if support_dxf is None:
        return {
            "path": None,
            "support_runs": [],
            "walls": [],
            "edge_members": [],
            "columns": [],
            "line_count": 0,
        }

    all_lines = _filter_segments_to_bbox(
        _read_line_segments(support_dxf, support_layers, support_transform),
        model_bbox,
        margin_mm=20000.0,
    )
    support_runs = _pair_parallel_runs(
        all_lines, 50.0, max_support_width, overlap_min=50.0)

    wall_lines = _filter_segments_to_bbox(
        _read_line_segments(support_dxf, wall_layers, support_transform),
        model_bbox,
        margin_mm=20000.0,
    )
    wall_runs = _pair_parallel_runs(
        wall_lines, 70.0, 700.0, overlap_min=min_candidate_length)
    wall_source_runs = [
        run for run in _merge_collinear_runs(wall_runs)
        if float(run["end"]) - float(run["start"]) >= min_candidate_length
    ]

    edge_lines = _filter_segments_to_bbox(
        _read_line_segments(support_dxf, edge_member_layers, support_transform),
        model_bbox,
        margin_mm=20000.0,
    )
    edge_members = _open_chain_polygons(
        edge_lines,
        min_area_m2=0.02,
        max_area_m2=2.0,
        max_gap_mm=1200.0,
    )

    column_lines = _filter_segments_to_bbox(
        _read_line_segments(support_dxf, column_layers, support_transform),
        model_bbox,
        margin_mm=20000.0,
    )
    column_runs = _pair_parallel_runs(
        column_lines, 50.0, 2000.0, overlap_min=50.0)
    columns = _rectangles_from_runs(
        [r for r in column_runs if r["orientation"] == "H"],
        [r for r in column_runs if r["orientation"] == "V"],
    )
    column_contours = _open_chain_polygons(
        column_lines,
        min_area_m2=0.04,
        max_area_m2=2.0,
        max_gap_mm=1200.0,
    )
    for contour in column_contours:
        x0, y0, x1, y1 = [float(value) for value in contour["bbox"]]
        columns.append({
            "x0": x0,
            "x1": x1,
            "y0": y0,
            "y1": y1,
            "b_mm": x1 - x0,
            "h_mm": y1 - y0,
            "layers": [column_layers],
            "source": "open-contour",
        })
    deduped_columns: list[dict[str, Any]] = []
    for column in sorted(
            columns,
            key=lambda row: (row["x0"], row["y0"], row["x1"], row["y1"])):
        duplicate = False
        for existing in deduped_columns:
            interval_x = max(
                0.0,
                min(float(column["x1"]), float(existing["x1"]))
                - max(float(column["x0"]), float(existing["x0"])),
            )
            interval_y = max(
                0.0,
                min(float(column["y1"]), float(existing["y1"]))
                - max(float(column["y0"]), float(existing["y0"])),
            )
            area = (
                (float(column["x1"]) - float(column["x0"]))
                * (float(column["y1"]) - float(column["y0"]))
            )
            existing_area = (
                (float(existing["x1"]) - float(existing["x0"]))
                * (float(existing["y1"]) - float(existing["y0"]))
            )
            if interval_x * interval_y / max(
                    1.0, min(area, existing_area)) > 0.85:
                duplicate = True
                break
        if not duplicate:
            deduped_columns.append(column)
    columns = deduped_columns

    clipped_walls: list[dict[str, Any]] = []
    for run in wall_source_runs:
        width = _wall_width_mm(
            float(run["width_mm"]), tolerance=wall_width_tolerance_mm)
        if width is None:
            continue
        row = dict(run)
        row["width_mm"] = width
        row["source_width_mm"] = _round(run["width_mm"], 1)
        clipped_walls.append(row)
    clipped_walls = _clip_wall_runs(
        clipped_walls, edge_members + column_contours, min_candidate_length)
    walls = _dedupe_overlapping_runs(clipped_walls)

    return {
        "path": str(support_dxf),
        "support_runs": support_runs,
        "walls": walls,
        "wall_source_runs": wall_source_runs,
        "edge_members": edge_members,
        "columns": columns,
        "line_count": len(all_lines),
        "wall_line_count": len(wall_lines),
        "edge_member_line_count": len(edge_lines),
        "column_line_count": len(column_lines),
        "edge_member_polygon_count": len(edge_members),
        "column_contour_count": len(column_contours),
    }


def annotate_support_components(
        support: dict[str, Any],
        text_records: list[dict[str, Any]],
        transform: tuple[float, float],
        component_text_layer: str,
        edge_label_pattern: str,
        column_label_pattern: str,
        sheet: Optional[int] = None,
        max_distance_mm: float = 1200.0,
        edge_mirror_match_tolerance_mm: float = 25.0,
        edge_mirror_review_tolerance_mm: Optional[float] = 800.0,
        edge_mirror_review_shape_tolerance_mm: float = 600.0
        ) -> dict[str, Any]:
    edge = assign_object_labels(
        support.get("edge_members") or [],
        text_records,
        transform,
        component_text_layer,
        edge_label_pattern,
        max_distance_mm=max_distance_mm,
        sheet=sheet,
        require_mirror_shape=True,
        mirror_match_tolerance_mm=edge_mirror_match_tolerance_mm,
        mirror_review_tolerance_mm=edge_mirror_review_tolerance_mm,
        mirror_review_shape_tolerance_mm=(
            edge_mirror_review_shape_tolerance_mm),
    )
    column = assign_object_labels(
        support.get("columns") or [],
        text_records,
        transform,
        component_text_layer,
        column_label_pattern,
        max_distance_mm=max_distance_mm,
        sheet=sheet,
        require_mirror_shape=False,
        mirror_match_tolerance_mm=300.0,
    )
    return {
        "edge_member": edge,
        "column": column,
    }


def _beam_axis(row: dict[str, Any]) -> Optional[dict[str, Any]]:
    detail = row.get("detail") or {}
    orientation = str(detail.get("orientation") or "")
    start, end = detail.get("start"), detail.get("end")
    if orientation not in ("H", "V") or not start or not end:
        return None
    if orientation == "H":
        s0, s1 = sorted((float(start[0]), float(end[0])))
        axis = (float(start[1]) + float(end[1])) / 2.0
    else:
        s0, s1 = sorted((float(start[1]), float(end[1])))
        axis = (float(start[0]) + float(end[0])) / 2.0
    return {
        "orientation": orientation,
        "start": s0,
        "end": s1,
        "axis": axis,
        "centerline_length_mm": s1 - s0,
    }


def _beam_span_count(code: str) -> Optional[int]:
    match = re.search(r"\(\s*(\d+)\s*[AB]?\s*\)", str(code or ""), re.I)
    return int(match.group(1)) if match else None


def _clear_span_quantity(
        row: dict[str, Any],
        support_runs: list[dict[str, Any]],
        max_support_width: float,
        end_tolerance: float,
        min_span: float,
        assumed_end_support_width: float = 0.0,
        beam_support_runs: Optional[list[dict[str, Any]]] = None,
        beam_intersection_end_tolerance_mm: float = 0.0,
        arbitrate_support_count: bool = False,
        support_cluster_tolerance_mm: float = 400.0,
        endpoint_support_polygons: Optional[list[dict[str, Any]]] = None,
        endpoint_polygon_search_mm: float = 0.0,
        endpoint_polygon_width_mm: float = 500.0
        ) -> dict[str, Any]:
    axis_info = _beam_axis(row)
    if not axis_info:
        return {
            "status": "no-centerline",
            "spans": [],
            "support_count": 0,
            "clear_length_mm": None,
            "issue": "没有可用的梁中心线",
        }

    orientation = axis_info["orientation"]
    axis = axis_info["axis"]
    s0, s1 = axis_info["start"], axis_info["end"]
    target_height = float(row.get("section_h_mm") or 0.0)
    support_candidates: list[dict[str, Any]] = []
    for run in support_runs:
        interval = _interval_on_axis(run, orientation, axis, max_support_width)
        if interval is None:
            continue
        lo, hi = interval
        if min(hi, s1) - max(lo, s0) > 0:
            start = max(lo, s0)
            end = min(hi, s1)
            evidence = {
                "type": run.get("source") or "wall-column",
                "id": run.get("id"),
                "code": run.get("code"),
                "orientation": run.get("orientation"),
                "center_mm": _round(float(run["center"]), 1),
                "width_mm": _round(float(run["width_mm"]), 1),
                "start_mm": _round(start, 1),
                "end_mm": _round(end, 1),
            }
            support_candidates.append({
                "start_mm": start,
                "end_mm": end,
                "center_mm": (start + end) / 2.0,
                "score": 100.0,
                "requires_review": False,
                "evidence": evidence,
            })
    for run in beam_support_runs or []:
        if str(run.get("orientation") or "") == orientation:
            continue
        interval = _interval_on_axis(
            run,
            orientation,
            axis,
            max_support_width,
            crossing_tolerance_mm=beam_intersection_end_tolerance_mm,
        )
        if interval is None:
            continue
        lo, hi = interval
        if min(hi, s1) - max(lo, s0) > 0:
            run_start = float(run["start"])
            run_end = float(run["end"])
            crossing_status = (
                "inside"
                if run_start - 1e-6 <= axis <= run_end + 1e-6
                else "endpoint-tolerance"
            )
            start = max(lo, s0)
            end = min(hi, s1)
            crossing_height = float(run.get("section_h_mm") or 0.0)
            if crossing_status == "endpoint-tolerance":
                score = 80.0
            elif target_height and crossing_height > target_height:
                score = 70.0 + min(crossing_height - target_height, 200.0) / 100.0
            elif target_height and crossing_height == target_height:
                score = 50.0
            else:
                score = 30.0
            if (
                    run.get("code")
                    and run.get("code") == row.get("code")):
                score -= 20.0
            evidence = {
                "type": "beam-intersection",
                "id": run.get("id"),
                "code": run.get("code"),
                "orientation": run.get("orientation"),
                "center_mm": _round(float(run["center"]), 1),
                "width_mm": _round(float(run["width_mm"]), 1),
                "start_mm": _round(max(lo, s0), 1),
                "end_mm": _round(min(hi, s1), 1),
                "crossing_status": crossing_status,
                "requires_review": crossing_status == "endpoint-tolerance",
            }
            support_candidates.append({
                "start_mm": start,
                "end_mm": end,
                "center_mm": (start + end) / 2.0,
                "score": score,
                "requires_review": crossing_status == "endpoint-tolerance",
                "evidence": evidence,
            })

    endpoint_polygon_support_count = 0
    if endpoint_polygon_search_mm > 0:
        existing_intervals = [
            (float(candidate["start_mm"]), float(candidate["end_mm"]))
            for candidate in support_candidates
        ]
        for side, endpoint in (("start", s0), ("end", s1)):
            if any(
                    lo <= endpoint + end_tolerance
                    and hi >= endpoint - end_tolerance
                    for lo, hi in existing_intervals):
                continue
            point = (
                (axis, endpoint)
                if orientation == "V" else (endpoint, axis)
            )
            best: Optional[tuple[float, dict[str, Any], list[float]]] = None
            for polygon in endpoint_support_polygons or []:
                points = [
                    (float(p[0]), float(p[1]))
                    for p in polygon.get("points") or []
                ]
                if len(points) < 3:
                    continue
                distance = _point_polygon_distance(point, points)
                if distance > endpoint_polygon_search_mm:
                    continue
                projection = [
                    p[1] if orientation == "V" else p[0] for p in points
                ]
                if best is None or distance < best[0]:
                    best = (distance, polygon, projection)
            if best is None:
                continue
            distance, polygon, projection = best
            projected_start = min(projection)
            projected_end = max(projection)
            overlap = max(
                0.0,
                min(projected_end, s1) - max(projected_start, s0),
            )
            if overlap > 0:
                start = max(s0, projected_start)
                end = min(s1, projected_end)
                width = end - start
                position_status = "projected-overlap"
            else:
                width = min(
                    max(float(endpoint_polygon_width_mm), 200.0),
                    max_support_width,
                )
                if side == "start":
                    start, end = s0, min(s1, s0 + width)
                else:
                    start, end = max(s0, s1 - width), s1
                position_status = "nearest-outside-endpoint"
            evidence = {
                "type": "endpoint-polygon",
                "id": polygon.get("id"),
                "code": polygon.get("label") or "",
                "orientation": orientation,
                "center_mm": _round((start + end) / 2.0, 1),
                "width_mm": _round(width, 1),
                "start_mm": _round(start, 1),
                "end_mm": _round(end, 1),
                "side": side,
                "distance_mm": _round(distance, 1),
                "source": polygon.get("source") or "support-polygon",
                "support_position_status": position_status,
                "requires_review": True,
            }
            support_candidates.append({
                "start_mm": start,
                "end_mm": end,
                "center_mm": (start + end) / 2.0,
                "score": 90.0,
                "requires_review": True,
                "evidence": evidence,
            })
            existing_intervals.append((start, end))
            endpoint_polygon_support_count += 1

    expected_support_count = _beam_span_count(str(row.get("code") or ""))
    expected_total_support_count = (
        expected_support_count + 1
        if expected_support_count is not None else None
    )
    clusters = _cluster_support_candidates(
        support_candidates, tolerance_mm=support_cluster_tolerance_mm)
    rejected_clusters: list[dict[str, Any]] = []
    support_selection_status = "not-arbitrated"
    covered_start = any(
        float(cluster["start_mm"]) <= s0 + end_tolerance
        and float(cluster["end_mm"]) >= s0 - end_tolerance
        for cluster in clusters)
    covered_end = any(
        float(cluster["start_mm"]) <= s1 + end_tolerance
        and float(cluster["end_mm"]) >= s1 - end_tolerance
        for cluster in clusters)
    missing_endpoint_count = int(not covered_start) + int(not covered_end)
    maximum_selected_clusters = (
        max(0, expected_total_support_count - missing_endpoint_count)
        if expected_total_support_count is not None else None
    )
    if (
            arbitrate_support_count
            and expected_total_support_count is not None
            and len(clusters) > maximum_selected_clusters):
        selected_clusters, rejected_clusters = _select_support_clusters(
            clusters,
            s0,
            s1,
            end_tolerance,
            maximum_selected_clusters,
        )
        clusters = selected_clusters
        support_selection_status = "expected-count-arbitrated"
    elif arbitrate_support_count:
        support_selection_status = "candidate-count-not-more-than-required"

    selected_members = {
        id(member)
        for cluster in clusters
        for member in cluster.get("members") or []
    }
    rejected_members = {
        id(member)
        for cluster in rejected_clusters
        for member in cluster.get("members") or []
    }
    support_evidence: list[dict[str, Any]] = []
    for candidate in support_candidates:
        evidence = dict(candidate["evidence"])
        evidence["selection_score"] = _round(float(candidate["score"]), 1)
        if id(candidate) in rejected_members:
            evidence["selection_status"] = "rejected-by-expected-support-count"
        elif id(candidate) in selected_members:
            evidence["selection_status"] = "selected"
        else:
            evidence["selection_status"] = "kept"
        support_evidence.append(evidence)
    raw_intervals = [
        (float(cluster["start_mm"]), float(cluster["end_mm"]))
        for cluster in clusters
    ]
    intervals = _merge_intervals(raw_intervals, gap=15.0)
    inferred_end_supports: list[dict[str, Any]] = []
    if assumed_end_support_width > 0 and s1 - s0 > assumed_end_support_width:
        covered_start = any(
            lo <= s0 + end_tolerance and hi >= s0 - end_tolerance
            for lo, hi in intervals)
        covered_end = any(
            lo <= s1 + end_tolerance and hi >= s1 - end_tolerance
            for lo, hi in intervals)
        if not covered_start:
            intervals.append((s0, min(s1, s0 + assumed_end_support_width)))
            inferred_end_supports.append({
                "side": "start",
                "start_mm": _round(s0, 1),
                "end_mm": _round(min(s1, s0 + assumed_end_support_width), 1),
                "assumed_width_mm": assumed_end_support_width,
            })
        if not covered_end:
            intervals.append((max(s0, s1 - assumed_end_support_width), s1))
            inferred_end_supports.append({
                "side": "end",
                "start_mm": _round(max(s0, s1 - assumed_end_support_width), 1),
                "end_mm": _round(s1, 1),
                "assumed_width_mm": assumed_end_support_width,
            })
        intervals = _merge_intervals(intervals, gap=15.0)

    spans: list[dict[str, Any]] = []
    for left, right in zip(intervals, intervals[1:]):
        length = float(right[0]) - float(left[1])
        if length >= min_span:
            spans.append({
                "start_mm": _round(left[1], 1),
                "end_mm": _round(right[0], 1),
                "length_mm": _round(length, 1),
            })

    if expected_total_support_count is None:
        support_count_status = "unknown"
    elif len(intervals) < expected_total_support_count:
        support_count_status = "under"
    elif len(intervals) > expected_total_support_count:
        support_count_status = "over"
    else:
        support_count_status = "exact"
    count_complete = bool(
        expected_total_support_count is None
        or len(intervals) >= expected_total_support_count
    )
    complete = bool(
        len(intervals) >= 2
        and intervals[0][0] <= s0 + end_tolerance
        and intervals[-1][1] >= s1 - end_tolerance
        and spans
        and count_complete
    )
    selection_review_required = bool(rejected_clusters)
    selection_summary = {
        "status": support_selection_status,
        "candidate_cluster_count": len(
            clusters) + len(rejected_clusters),
        "selected_cluster_count": len(clusters),
        "rejected_cluster_count": len(rejected_clusters),
        "endpoint_polygon_support_count": endpoint_polygon_support_count,
        "rejected_candidates": [
            {
                "start_mm": _round(float(cluster["start_mm"]), 1),
                "end_mm": _round(float(cluster["end_mm"]), 1),
                "center_mm": _round(float(cluster["center_mm"]), 1),
                "score": _round(float(cluster["score"]), 1),
                "evidence": [
                    member["evidence"] for member in cluster["members"]
                ],
            }
            for cluster in rejected_clusters
        ],
    }
    selection_issue = (
        f"支座候选{len(clusters) + len(rejected_clusters)}个，按编号跨数保留"
        f"{len(clusters)}个，剔除{len(rejected_clusters)}个候选，需复核"
        if selection_review_required else ""
    )
    if complete:
        clear_length = sum(float(span["length_mm"]) for span in spans)
        gross_length = row.get("length_mm")
        if gross_length and clear_length > float(gross_length) * 1.05 + 1.0:
            return {
                "status": "centerline-mismatch",
                "spans": spans,
                "support_count": len(intervals),
                "clear_length_mm": None,
                "issue": "；".join(filter(None, [
                    "支座净跨大于中心线粗长，中心线端点不可信",
                    selection_issue,
                ])),
                "support_selection": selection_summary,
                "support_evidence": support_evidence,
            }
        reviewed_support = any(
            support.get("requires_review")
            and support.get("selection_status") != (
                "rejected-by-expected-support-count")
            for support in support_evidence
        )
        quantity_status = (
            "clear-span-inferred"
            if inferred_end_supports else
            "clear-span-review"
            if reviewed_support else
            "clear-span"
        )
        return {
            "status": quantity_status,
            "spans": spans,
            "support_count": len(intervals),
            "expected_support_count": expected_total_support_count,
            "support_count_status": support_count_status,
            "clear_length_mm": _round(clear_length, 1),
            "inferred_end_supports": inferred_end_supports,
            "issue": "；".join(filter(None, [
                (
                    f"支座数{len(intervals)}超过编号跨数需要"
                    f"{expected_total_support_count}个，需复核"
                    if support_count_status == "over" else ""
                ),
                selection_issue,
            ])),
            "support_selection": selection_summary,
            "support_evidence": support_evidence,
        }

    issues = []
    if len(intervals) < 2:
        issues.append("有效支座少于2个")
    if intervals and intervals[0][0] > s0 + end_tolerance:
        issues.append("起点端支座未闭合")
    if intervals and intervals[-1][1] < s1 - end_tolerance:
        issues.append("终点端支座未闭合")
    if len(intervals) >= 2 and not spans:
        issues.append("相邻支座没有形成有效净跨")
    if not count_complete and expected_support_count is not None:
        issues.append(
            f"编号标注{expected_support_count}跨，需要{expected_support_count + 1}个支座，"
            f"当前仅{len(intervals)}个"
        )
    if selection_issue:
        issues.append(selection_issue)
    return {
        "status": "support-gap",
        "spans": spans,
        "support_count": len(intervals),
        "expected_support_count": expected_total_support_count,
        "support_count_status": support_count_status,
        "clear_length_mm": None,
        "issue": "；".join(issues) or "支座拓扑不完整",
        "support_intervals": [[_round(a, 1), _round(b, 1)] for a, b in intervals],
        "inferred_end_supports": inferred_end_supports,
        "support_selection": selection_summary,
        "support_evidence": support_evidence,
    }


def build_beams(beam_json: Path,
                support_runs: list[dict[str, Any]],
                max_support_width: float,
                end_tolerance: float,
                min_span: float,
                assumed_end_support_width: float = 0.0,
                beam_support_runs: Optional[list[dict[str, Any]]] = None,
                beam_intersection_end_tolerance_mm: float = 0.0,
                arbitrate_support_count: bool = False,
                support_cluster_tolerance_mm: float = 400.0,
                endpoint_support_polygons: Optional[list[dict[str, Any]]] = None,
                endpoint_polygon_search_mm: float = 0.0,
                endpoint_polygon_width_mm: float = 500.0
                ) -> list[dict[str, Any]]:
    data = json.loads(beam_json.read_text(encoding="utf-8"))
    rows = data.get("rows") or []
    out: list[dict[str, Any]] = []
    for idx, row in enumerate(rows, 1):
        b = row.get("section_b_mm")
        h = row.get("section_h_mm")
        gross_length = row.get("length_mm")
        gross_volume = row.get("volume_m3")
        clear = _clear_span_quantity(
            row,
            support_runs,
            max_support_width,
            end_tolerance,
            min_span,
            assumed_end_support_width,
            beam_support_runs,
            beam_intersection_end_tolerance_mm,
            arbitrate_support_count,
            support_cluster_tolerance_mm,
            endpoint_support_polygons,
            endpoint_polygon_search_mm,
            endpoint_polygon_width_mm,
        )
        clear_volume = None
        if (clear["status"] in (
                "clear-span", "clear-span-inferred", "clear-span-review")
                and b and h and clear["clear_length_mm"]):
            clear_volume = float(b) * float(h) * float(clear["clear_length_mm"]) / 1e9
        out.append({
            "id": f"B{idx:04d}",
            "type": "beam",
            "code": row.get("code") or "",
            "base_code": row.get("base_code") or "",
            "section": row.get("section") or "",
            "section_b_mm": b,
            "section_h_mm": h,
            "centerline": row.get("detail") or {},
            "centerline_length_mm": gross_length,
            "gross_volume_m3": _round(gross_volume, 4) if gross_volume is not None else None,
            "clear_spans": clear.get("spans") or [],
            "clear_length_mm": clear.get("clear_length_mm"),
            "clear_volume_m3": _round(clear_volume, 4) if clear_volume is not None else None,
            "support_count": clear.get("support_count") or 0,
            "expected_support_count": clear.get("expected_support_count"),
            "support_count_status": clear.get("support_count_status") or "unknown",
            "support_intervals": clear.get("support_intervals") or [],
            "support_selection": clear.get("support_selection") or {},
            "endpoint_polygon_support_count": int(
                (clear.get("support_selection") or {}).get(
                    "endpoint_polygon_support_count") or 0),
            "support_evidence": clear.get("support_evidence") or [],
            "beam_intersection_support_count": sum(
                1 for support in clear.get("support_evidence") or []
                if support.get("type") == "beam-intersection"),
            "beam_intersection_review_support_count": sum(
                1 for support in clear.get("support_evidence") or []
                if support.get("requires_review")),
            "inferred_end_supports": clear.get("inferred_end_supports") or [],
            "quantity_status": clear["status"],
            "issue": clear.get("issue") or "",
            "source": row.get("source"),
            "position": {
                "x": row.get("x"),
                "y": row.get("y"),
            },
        })
    return out


def _snap_node(point: tuple[float, float],
               snap_mm: float) -> tuple[int, int]:
    return (
        int(round(point[0] / snap_mm)),
        int(round(point[1] / snap_mm)),
    )


def _polygon_area(points: list[tuple[float, float]]) -> float:
    if len(points) < 3:
        return 0.0
    total = 0.0
    for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
        total += x1 * y2 - x2 * y1
    return abs(total) / 2.0


def _point_in_polygon(point: tuple[float, float],
                      polygon: list[tuple[float, float]]) -> bool:
    x, y = point
    inside = False
    if len(polygon) < 3:
        return False
    for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]):
        if (y1 > y) != (y2 > y):
            cross = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if cross > x:
                inside = not inside
    return inside


def _point_segment_distance(point: tuple[float, float],
                            a: tuple[float, float],
                            b: tuple[float, float]) -> float:
    x, y = point
    ax, ay = a
    bx, by = b
    vx, vy = bx - ax, by - ay
    denominator = vx * vx + vy * vy
    if denominator <= 1e-12:
        return math.dist(point, a)
    t = max(0.0, min(1.0, ((x - ax) * vx + (y - ay) * vy) / denominator))
    return math.hypot(x - (ax + t * vx), y - (ay + t * vy))


def _point_polygon_distance(point: tuple[float, float],
                            polygon: list[tuple[float, float]]) -> float:
    if len(polygon) < 2:
        return float("inf")
    if _point_in_polygon(point, polygon):
        return 0.0
    return min(
        _point_segment_distance(point, a, b)
        for a, b in zip(polygon, polygon[1:] + polygon[:1])
    )


def _polygon_bbox(points: list[tuple[float, float]]) -> list[float]:
    if not points:
        return []
    return [
        min(point[0] for point in points),
        min(point[1] for point in points),
        max(point[0] for point in points),
        max(point[1] for point in points),
    ]


def _polygon_center(points: list[tuple[float, float]]) -> tuple[float, float]:
    if not points:
        return 0.0, 0.0
    return (
        sum(point[0] for point in points) / len(points),
        sum(point[1] for point in points) / len(points),
    )


def _object_points(row: dict[str, Any]) -> list[tuple[float, float]]:
    if row.get("points"):
        return [(float(point[0]), float(point[1]))
                for point in row["points"]]
    if all(key in row for key in ("x0", "y0", "x1", "y1")):
        return [
            (float(row["x0"]), float(row["y0"])),
            (float(row["x1"]), float(row["y0"])),
            (float(row["x1"]), float(row["y1"])),
            (float(row["x0"]), float(row["y1"])),
        ]
    return []


def _object_shape_key(row: dict[str, Any]) -> tuple[Any, ...]:
    points = _object_points(row)
    bbox = _polygon_bbox(points)
    area = float(row.get("area_m2") or _polygon_area(points) / 1e6)
    width = bbox[2] - bbox[0] if len(bbox) == 4 else 0.0
    height = bbox[3] - bbox[1] if len(bbox) == 4 else 0.0
    return (
        round(area, 4),
        round(width, 1),
        round(height, 1),
        len(points),
    )


def _objects_shape_review_compatible(
        first: dict[str, Any],
        second: dict[str, Any],
        tolerance_mm: float) -> bool:
    """判断截断轮廓是否可在待复核镜像匹配中视为同类截面。"""
    first_key = _object_shape_key(first)
    second_key = _object_shape_key(second)
    if first_key == second_key:
        return True
    first_area, first_width, first_height, first_points = first_key
    second_area, second_width, second_height, second_points = second_key
    max_area = max(float(first_area), float(second_area), 0.01)
    return (
        abs(float(first_width) - float(second_width)) <= tolerance_mm
        and abs(float(first_height) - float(second_height)) <= tolerance_mm
        and abs(int(first_points) - int(second_points)) <= 2
        and abs(float(first_area) - float(second_area)) <= max_area * 0.35
    )


def _load_text_records(source: Optional[Path]) -> list[dict[str, Any]]:
    if source is None:
        return []
    data = json.loads(source.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    records = data.get("text_records")
    return records if isinstance(records, list) else []


def _extract_component_labels(
        records: list[dict[str, Any]],
        layer_pattern: str,
        label_pattern: str,
        transform: tuple[float, float],
        sheet: Optional[int] = None) -> list[dict[str, Any]]:
    layer_re = re.compile(layer_pattern, re.I)
    label_re = re.compile(label_pattern, re.I)
    tx, ty = transform
    labels: list[dict[str, Any]] = []
    for record in records:
        if sheet is not None and record.get("sheet") != sheet:
            continue
        layer = str(record.get("layer") or "")
        if not layer_re.search(layer):
            continue
        label = re.sub(r"\s+", "", str(record.get("text") or ""))
        if not label_re.fullmatch(label):
            continue
        try:
            x = float(record["x"]) + tx
            y = float(record["y"]) + ty
        except (KeyError, TypeError, ValueError):
            continue
        labels.append({
            "label": label,
            "x": x,
            "y": y,
            "layer": layer,
            "sheet": record.get("sheet"),
        })
    return labels


def _estimate_mirror_axis_x(
        objects: list[dict[str, Any]],
        quantize_mm: float = 5.0,
        y_tolerance_mm: float = 5.0,
        min_votes: int = 2) -> Optional[float]:
    rows: list[tuple[tuple[Any, ...], float, float]] = []
    for row in objects:
        center = _polygon_center(_object_points(row))
        rows.append((_object_shape_key(row), center[0], center[1]))

    votes: dict[float, list[float]] = defaultdict(list)
    for index, (shape, x, y) in enumerate(rows):
        for other_shape, other_x, other_y in rows[index + 1:]:
            if shape != other_shape or abs(y - other_y) > y_tolerance_mm:
                continue
            axis = (x + other_x) / 2.0
            key = round(axis / quantize_mm) * quantize_mm
            votes[key].append(axis)
    if not votes:
        return None
    key, values = max(votes.items(), key=lambda item: len(item[1]))
    if len(values) < min_votes:
        return None
    return _median(values)


def assign_object_labels(
        objects: list[dict[str, Any]],
        records: list[dict[str, Any]],
        transform: tuple[float, float],
        layer_pattern: str,
        label_pattern: str,
        max_distance_mm: float = 1200.0,
        sheet: Optional[int] = None,
        require_mirror_shape: bool = True,
        mirror_min_votes: int = 2,
        mirror_match_tolerance_mm: float = 25.0,
        mirror_review_tolerance_mm: Optional[float] = None,
        mirror_review_shape_tolerance_mm: float = 600.0,
        mirror_axis_x_mm: Optional[float] = None) -> dict[str, Any]:
    """把构件文字直接关联到最近轮廓，并沿图面镜像轴补齐未重复标注的实例。"""
    labels = _extract_component_labels(
        records, layer_pattern, label_pattern, transform, sheet=sheet)
    points = [_object_points(row) for row in objects]
    if not labels or not points:
        for row in objects:
            row["label_status"] = "unlabeled"
        return {
            "label_count": len(labels),
            "direct_count": 0,
            "mirror_count": 0,
            "unlabeled_count": len(objects),
            "mirror_axis_x_mm": None,
            "labels": labels,
        }

    candidates: list[tuple[float, int, int]] = []
    for label_index, label in enumerate(labels):
        point = (float(label["x"]), float(label["y"]))
        for object_index, polygon in enumerate(points):
            if len(polygon) < 3:
                continue
            distance = _point_polygon_distance(point, polygon)
            if distance <= max_distance_mm:
                candidates.append((distance, object_index, label_index))
    candidates.sort()

    assignments: dict[int, dict[str, Any]] = {}
    used_labels: set[int] = set()
    for distance, object_index, label_index in candidates:
        if object_index in assignments or label_index in used_labels:
            continue
        label = labels[label_index]
        assignments[object_index] = {
            "label": label["label"],
            "label_layer": label["layer"],
            "label_x": _round(label["x"], 1),
            "label_y": _round(label["y"], 1),
            "label_distance_mm": _round(distance, 1),
            "label_status": "direct",
            "label_basis": "text-nearest-polygon",
            "mirror_partner_index": None,
        }
        used_labels.add(label_index)

    mirror_axis = (
        float(mirror_axis_x_mm) if mirror_axis_x_mm is not None
        else _estimate_mirror_axis_x(objects, min_votes=mirror_min_votes)
    )
    mirror_count = 0
    mirror_review_count = 0
    if mirror_axis is not None:
        for object_index, row in enumerate(objects):
            if object_index in assignments:
                continue
            center = _polygon_center(points[object_index])
            shape = _object_shape_key(row)
            mirrored_x = 2.0 * mirror_axis - center[0]
            best: Optional[tuple[int, float, int, str]] = None
            for partner_index, assignment in assignments.items():
                partner_center = _polygon_center(points[partner_index])
                partner_shape = _object_shape_key(objects[partner_index])
                exact_shape = partner_shape == shape
                distance = math.hypot(
                    partner_center[0] - mirrored_x,
                    partner_center[1] - center[1],
                )
                if (
                        distance <= mirror_match_tolerance_mm
                        and (exact_shape or not require_mirror_shape)):
                    candidate = (
                        0, distance, partner_index, "strict-mirror")
                elif (
                        mirror_review_tolerance_mm is not None
                        and distance <= mirror_review_tolerance_mm
                        and _objects_shape_review_compatible(
                            row,
                            objects[partner_index],
                            mirror_review_shape_tolerance_mm)):
                    reason = (
                        "review-distance-beyond-strict-tolerance"
                        if exact_shape else
                        "review-truncated-or-resized-shape"
                    )
                    candidate = (1, distance, partner_index, reason)
                else:
                    continue
                if best is None or candidate[:2] < best[:2]:
                    best = candidate
            if best is None:
                continue
            _, distance, partner_index, review_reason = best
            assignment = dict(assignments[partner_index])
            requires_review = review_reason != "strict-mirror"
            assignment.update({
                "label_status": (
                    "mirror-propagated-review"
                    if requires_review else "mirror-propagated"
                ),
                "label_basis": (
                    "shape-and-y-mirror-review"
                    if requires_review else "shape-and-y-mirror"
                ),
                "mirror_partner_index": partner_index + 1,
                "mirror_axis_x_mm": _round(mirror_axis, 1),
                "mirror_match_distance_mm": _round(distance, 1),
                "mirror_review_reason": (
                    review_reason if requires_review else ""),
                "mirror_requires_review": requires_review,
            })
            assignments[object_index] = assignment
            mirror_count += 1
            if requires_review:
                mirror_review_count += 1

    for object_index, row in enumerate(objects):
        row.update(assignments.get(object_index, {
            "label": "",
            "label_status": "unlabeled",
            "label_basis": "",
        }))
        if mirror_axis is not None:
            row.setdefault("mirror_axis_x_mm", _round(mirror_axis, 1))

    label_counts = Counter(
        str(row.get("label") or "") for row in objects if row.get("label"))
    return {
        "label_count": len(labels),
        "direct_count": len([row for row in objects
                             if row.get("label_status") == "direct"]),
        "mirror_count": mirror_count,
        "mirror_strict_count": mirror_count - mirror_review_count,
        "mirror_review_count": mirror_review_count,
        "unlabeled_count": len([row for row in objects
                                if row.get("label_status") == "unlabeled"]),
        "mirror_axis_x_mm": (
            _round(mirror_axis, 1) if mirror_axis is not None else None),
        "label_counts": dict(sorted(label_counts.items())),
        "labels": labels,
    }


def _read_geometry_lines(path: Optional[Path],
                         layer_pattern: str,
                         transform: tuple[float, float]) -> list[dict[str, Any]]:
    if path is None:
        return []
    from dev_dxf import readfile

    doc = readfile(str(path))
    layer_re = re.compile(layer_pattern, re.I)
    tx, ty = transform
    rows: list[dict[str, Any]] = []
    for entity in doc.modelspace():
        if entity.dxftype() != "LINE":
            continue
        layer = str(entity.dxf.layer or "")
        if layer == "__SHEET_BBOX" or not layer_re.search(layer):
            continue
        start, end = entity.dxf.start, entity.dxf.end
        a = (float(start.x) + tx, float(start.y) + ty)
        b = (float(end.x) + tx, float(end.y) + ty)
        if math.dist(a, b) > 1e-4:
            rows.append({
                "handle": str(entity.dxf.handle or ""),
                "layer": layer,
                "a": a,
                "b": b,
            })
    return rows


def load_hatch_regions(
        source: Optional[Path],
        layer_pattern: str,
        transform: tuple[float, float],
        model_bbox: Optional[list[float]] = None,
        margin_mm: float = 5000.0,
        rule_map: Optional[dict[str, str]] = None) -> list[dict[str, Any]]:
    if source is None:
        return []
    layer_re = re.compile(layer_pattern, re.I)
    tx, ty = transform
    regions: list[dict[str, Any]] = []

    if source.suffix.lower() == ".dxf":
        from dev_dxf import readfile

        doc = readfile(str(source))
        for entity in doc.modelspace().query("HATCH"):
            layer = str(entity.dxf.layer or "")
            if not layer_re.search(layer):
                continue
            pattern_name = str(entity.dxf.get("pattern_name") or "")
            solid_fill = bool(entity.dxf.get("solid_fill"))
            for path_index, path in enumerate(entity.paths, 1):
                points: list[tuple[float, float]] = []
                try:
                    vertices = list(path.vertices)
                except AttributeError:
                    vertices = []
                for vertex in vertices:
                    points.append((
                        float(vertex[0]) + tx,
                        float(vertex[1]) + ty,
                    ))
                if len(points) < 3:
                    continue
                if points[0] == points[-1]:
                    points = points[:-1]
                regions.append({
                    "handle": str(entity.dxf.handle or ""),
                    "path_index": path_index,
                    "layer": layer,
                    "pattern_name": pattern_name,
                    "solid_fill": solid_fill,
                    "points": [[_round(x, 1), _round(y, 1)]
                               for x, y in points],
                    "area_m2": _round(_polygon_area(points) / 1e6, 4),
                    "bbox": [_round(value, 1)
                             for value in _polygon_bbox(points)],
                })
    elif source.suffix.lower() == ".dwg":
        from dev_dxf import raw

        rows = list(raw.decode_hatch_entities(str(source)) or [])
        layer_names = dict(raw.decode_layer_names(str(source)) or [])
        handles = [int(row[0]) for row in rows]
        layer_map: dict[int, str] = {}
        for index in range(0, len(handles), 1000):
            for handle, layer_handle in raw.decode_object_entity_layer_handles(
                    str(source), handles[index:index + 1000]) or []:
                layer_map[int(handle)] = layer_names.get(int(layer_handle), "")
        for row in rows:
            handle, pattern_name, solid_fill, _, _, _, paths = row
            layer = layer_map.get(int(handle), "")
            if not layer_re.search(layer):
                continue
            for path_index, (closed, raw_points) in enumerate(paths, 1):
                points = [(float(x) + tx, float(y) + ty)
                          for x, y in raw_points]
                if len(points) >= 2 and points[0] == points[-1]:
                    points = points[:-1]
                if len(points) < 3 or not closed:
                    continue
                regions.append({
                    "handle": str(handle),
                    "path_index": path_index,
                    "layer": layer,
                    "pattern_name": str(pattern_name or ""),
                    "solid_fill": bool(solid_fill),
                    "points": [[_round(x, 1), _round(y, 1)]
                               for x, y in points],
                    "area_m2": _round(_polygon_area(points) / 1e6, 4),
                    "bbox": [_round(value, 1)
                             for value in _polygon_bbox(points)],
                })
    else:
        raise ValueError("板填充来源仅支持 DXF 或 DWG")

    rules = rule_map or {}
    filtered: list[dict[str, Any]] = []
    for region in regions:
        bbox = region["bbox"]
        if model_bbox and len(model_bbox) == 4:
            x0, y0, x1, y1 = [float(value) for value in model_bbox]
            if (bbox[2] < x0 - margin_mm or bbox[0] > x1 + margin_mm
                    or bbox[3] < y0 - margin_mm or bbox[1] > y1 + margin_mm):
                continue
        rule = rules.get(str(region["handle"]), "")
        region["fill_rule"] = rule
        region["fill_code"] = rule or region.get("pattern_name") or "filled"
        filtered.append(region)
    filtered.sort(key=lambda row: (
        str(row.get("handle") or ""), int(row.get("path_index") or 1)))
    for index, region in enumerate(filtered, 1):
        region["id"] = f"H{index:04d}"
    return filtered


def _parse_hatch_rule_map(value: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for group in str(value or "").split(";"):
        group = group.strip()
        if not group:
            continue
        if "=" not in group:
            raise argparse.ArgumentTypeError(
                "板填充规则必须是 句柄1,句柄2=规则 格式")
        handles, rule = group.split("=", 1)
        rule = rule.strip()
        if not rule:
            raise argparse.ArgumentTypeError("板填充规则不能为空")
        for handle in handles.split(","):
            handle = handle.strip()
            if handle:
                result[handle] = rule
    return result


def _segments_intersect(
        a: tuple[float, float],
        b: tuple[float, float],
        c: tuple[float, float],
        d: tuple[float, float]) -> bool:
    def cross(p: tuple[float, float],
              q: tuple[float, float],
              r: tuple[float, float]) -> float:
        return ((q[0] - p[0]) * (r[1] - p[1])
                - (q[1] - p[1]) * (r[0] - p[0]))

    def on_segment(p: tuple[float, float],
                   q: tuple[float, float],
                   r: tuple[float, float]) -> bool:
        return (
            min(p[0], r[0]) - 1e-6 <= q[0] <= max(p[0], r[0]) + 1e-6
            and min(p[1], r[1]) - 1e-6 <= q[1] <= max(p[1], r[1]) + 1e-6
        )

    c1 = cross(a, b, c)
    c2 = cross(a, b, d)
    c3 = cross(c, d, a)
    c4 = cross(c, d, b)
    if ((c1 > 0 and c2 < 0) or (c1 < 0 and c2 > 0)) and (
            (c3 > 0 and c4 < 0) or (c3 < 0 and c4 > 0)):
        return True
    if abs(c1) <= 1e-6 and on_segment(a, c, b):
        return True
    if abs(c2) <= 1e-6 and on_segment(a, d, b):
        return True
    if abs(c3) <= 1e-6 and on_segment(c, a, d):
        return True
    if abs(c4) <= 1e-6 and on_segment(c, b, d):
        return True
    return False


def _line_intersects_polygon(line: dict[str, Any],
                             polygon: list[tuple[float, float]]) -> bool:
    if len(polygon) < 3:
        return False
    a = (float(line["a"][0]), float(line["a"][1]))
    b = (float(line["b"][0]), float(line["b"][1]))
    if _point_in_polygon(a, polygon) or _point_in_polygon(b, polygon):
        return True
    return any(
        _segments_intersect(a, b, edge_a, edge_b)
        for edge_a, edge_b in zip(polygon, polygon[1:] + polygon[:1])
    )


def _hatch_thickness_rule(rule: str) -> dict[str, Any]:
    text = str(rule or "").strip().lower()
    if not text:
        return {}
    if "drop" in text or "标高" in text:
        match = re.search(r"-?\d+(?:\.\d+)?", text)
        drop = float(match.group(0)) if match else -30.0
        return {
            "thickness_mm": None,
            "elevation_drop_mm": drop,
            "attribute_source": "hatch-elevation-rule",
        }
    match = re.search(r"\d+(?:\.\d+)?", text)
    if match:
        return {
            "thickness_mm": float(match.group(0)),
            "elevation_drop_mm": None,
            "attribute_source": "hatch-thickness-rule",
        }
    return {}


def assign_slab_attributes(
        panels: list[dict[str, Any]],
        hatch_regions: list[dict[str, Any]],
        thickness_records: list[dict[str, Any]],
        opening_lines: list[dict[str, Any]],
        opening_notes: list[dict[str, Any]],
        transform: tuple[float, float],
        default_thickness_mm: Optional[float] = None,
        thickness_label_max_distance_mm: float = 1500.0) -> dict[str, Any]:
    """关联板厚、材料状态和洞口证据；未闭合洞口不做面积扣减。"""
    material_area: Counter[str] = Counter()
    thickness_area: Counter[str] = Counter()
    direct_thickness_count = 0
    hatch_thickness_count = 0
    opening_candidate_count = 0

    direct_labels: list[dict[str, Any]] = []
    tx, ty = transform
    for record in thickness_records:
        text = str(record.get("text") or "")
        match = re.search(r"h\s*=\s*(\d+(?:\.\d+)?)", text, re.I)
        if not match:
            continue
        try:
            direct_labels.append({
                "thickness_mm": float(match.group(1)),
                "x": float(record["x"]) + tx,
                "y": float(record["y"]) + ty,
                "text": text,
                "layer": str(record.get("layer") or ""),
            })
        except (KeyError, TypeError, ValueError):
            continue

    transformed_notes: list[dict[str, Any]] = []
    for record in opening_notes:
        try:
            transformed_notes.append({
                "text": str(record.get("text") or ""),
                "x": float(record["x"]) + tx,
                "y": float(record["y"]) + ty,
                "layer": str(record.get("layer") or ""),
            })
        except (KeyError, TypeError, ValueError):
            continue

    for panel in panels:
        polygon = [(float(point[0]), float(point[1]))
                   for point in panel.get("points") or []]
        if len(polygon) < 3:
            continue
        area = float(panel.get("area_m2") or 0.0)
        matches = []
        for region in hatch_regions:
            region_polygon = [
                (float(point[0]), float(point[1]))
                for point in region.get("points") or []
            ]
            if len(region_polygon) < 3:
                continue
            center = _polygon_center(polygon)
            if (_point_in_polygon(center, region_polygon)
                    or any(_point_in_polygon(point, region_polygon)
                           for point in polygon)):
                matches.append(region)

        thickness: Optional[float] = default_thickness_mm
        thickness_source = "note-default" if default_thickness_mm else ""
        elevation_drop: Optional[float] = None
        rules: list[dict[str, Any]] = []
        for region in matches:
            rule = _hatch_thickness_rule(str(region.get("fill_rule") or ""))
            if rule:
                rules.append(rule)
            if rule.get("thickness_mm") is not None:
                thickness = float(rule["thickness_mm"])
                thickness_source = "hatch-rule"
            if rule.get("elevation_drop_mm") is not None:
                elevation_drop = float(rule["elevation_drop_mm"])

        # key= 必须显式给：距离相等时 sorted 会退化成比较 label 字典本身
        direct_candidates = sorted(
            ((_point_polygon_distance((label["x"], label["y"]), polygon), label)
             for label in direct_labels),
            key=lambda item: item[0],
        )
        if (direct_candidates
                and direct_candidates[0][0] <= thickness_label_max_distance_mm):
            label = direct_candidates[0][1]
            thickness = float(label["thickness_mm"])
            thickness_source = "dimension-label"
            direct_thickness_count += 1

        opening_evidence: list[dict[str, Any]] = []
        for line in opening_lines:
            if _line_intersects_polygon(line, polygon):
                opening_evidence.append({
                    "kind": "line",
                    "handle": line.get("handle"),
                    "layer": line.get("layer"),
                })
        for note in transformed_notes:
            point = (float(note["x"]), float(note["y"]))
            if _point_in_polygon(point, polygon):
                opening_evidence.append({
                    "kind": "text",
                    "text": note.get("text"),
                    "layer": note.get("layer"),
                })
        opening_status = (
            "opening-candidate" if opening_evidence else "none-known")
        if opening_evidence:
            opening_candidate_count += 1

        if thickness_source == "hatch-rule":
            hatch_thickness_count += 1
        if thickness is not None:
            thickness_area[str(int(thickness))
                           if float(thickness).is_integer()
                           else str(thickness)] += area
        material_status = (
            "cast-candidate"
            if (matches or thickness_source == "dimension-label")
            else "undetermined"
        )
        material_area[material_status] += area
        thickness_verification = {
            "dimension-label": "drawing-label",
            "hatch-rule": "legend-review-required",
            "note-default": "default-assumption",
            "": "unresolved",
        }.get(thickness_source, "unresolved")
        attribute_issue = ""
        if thickness_source == "hatch-rule":
            attribute_issue = (
                "板填充规则由几何位置和邻近说明推定，需按图纸图例复核")
        elif matches and not rules:
            attribute_issue = "填充图案规则未提供；板厚仅按默认值处理"
        elif material_status == "undetermined":
            attribute_issue = "材料体系需预制板拆分图复核"
        panel.update({
            "thickness_mm": (
                int(thickness) if thickness is not None
                and float(thickness).is_integer()
                else thickness
            ),
            "thickness_source": thickness_source or "unknown",
            "thickness_verification": thickness_verification,
            "thickness_status": (
                "resolved"
                if thickness is not None else "unresolved"
            ),
            "material_system": material_status,
            "elevation_drop_mm": elevation_drop,
            "hatch_region_ids": [region["id"] for region in matches],
            "hatch_area_m2": _round(sum(
                float(region.get("area_m2") or 0.0)
                for region in matches), 4),
            "opening_status": opening_status,
            "opening_evidence": opening_evidence,
            "attribute_issue": attribute_issue,
        })

    return {
        "panel_count": len(panels),
        "thickness_area_m2": dict(sorted(thickness_area.items())),
        "material_area_m2": dict(sorted(material_area.items())),
        "direct_thickness_count": direct_thickness_count,
        "hatch_thickness_count": hatch_thickness_count,
        "thickness_review_required_count": sum(
            1 for panel in panels
            if panel.get("thickness_verification")
            == "legend-review-required"),
        "thickness_default_count": sum(
            1 for panel in panels
            if panel.get("thickness_verification") == "default-assumption"),
        "opening_candidate_count": opening_candidate_count,
        "default_thickness_mm": default_thickness_mm,
        "issue": (
            "现浇/叠合材料体系需叠合板拆分图；开洞线未闭合成可靠扣减环"
        ),
    }


def _component_cycles(
        edges: list[tuple[int, int]],
        snap_mm: float) -> list[dict[str, Any]]:
    """在仅含LINE的平面图中提取闭合环和开放链。"""
    edge_nodes: list[tuple[tuple[int, int], tuple[int, int]]] = []
    adjacency: dict[tuple[int, int], list[int]] = defaultdict(list)
    for a, b in edges:
        na, nb = _snap_node(a, snap_mm), _snap_node(b, snap_mm)
        if na == nb:
            continue
        idx = len(edge_nodes)
        edge_nodes.append((na, nb))
        adjacency[na].append(idx)
        adjacency[nb].append(idx)

    unused = set(range(len(edge_nodes)))
    output: list[dict[str, Any]] = []
    while unused:
        start_edge = min(unused)
        na, nb = edge_nodes[start_edge]
        component_edges: set[int] = {start_edge}
        component_nodes: set[tuple[int, int]] = {na, nb}
        stack = [na, nb]
        while stack:
            node = stack.pop()
            for edge in adjacency.get(node, []):
                component_edges.add(edge)
                ea, eb = edge_nodes[edge]
                other = eb if ea == node else ea
                if other not in component_nodes:
                    component_nodes.add(other)
                    stack.append(other)
        unused -= component_edges
        degrees = {node: sum(1 for edge in adjacency[node]
                             if edge in component_edges)
                   for node in component_nodes}
        closed = bool(component_edges and all(degree == 2 for degree in degrees.values()))
        if closed:
            current = min(component_nodes)
            start = current
            previous_edge = -1
            node_order = [current]
            used_order: set[int] = set()
            for _ in range(len(component_edges) + 1):
                candidates = [
                    edge for edge in adjacency[current]
                    if edge in component_edges and edge != previous_edge
                    and edge not in used_order
                ]
                if not candidates:
                    break
                edge = candidates[0]
                used_order.add(edge)
                ea, eb = edge_nodes[edge]
                current = eb if ea == current else ea
                node_order.append(current)
                previous_edge = edge
                if current == start and len(used_order) == len(component_edges):
                    break
            if (current == start and len(used_order) == len(component_edges)
                    and len(node_order) >= 4):
                points = [(x * snap_mm, y * snap_mm) for x, y in node_order]
                output.append({
                    "status": "closed",
                    "edge_count": len(component_edges),
                    "points": [[_round(x, 1), _round(y, 1)] for x, y in points[:-1]],
                    "area_m2": _round(_polygon_area(points) / 1e6, 4),
                    "length_mm": _round(sum(
                        math.dist(edge_nodes[edge][0], edge_nodes[edge][1])
                        for edge in component_edges) * snap_mm, 1),
                })
                continue
        endpoints = [
            (x * snap_mm, y * snap_mm)
            for node, degree in degrees.items() if degree == 1 for x, y in [node]
        ]
        xs = [node[0] * snap_mm for node in component_nodes]
        ys = [node[1] * snap_mm for node in component_nodes]
        length = 0.0
        for edge in component_edges:
            a, b = edge_nodes[edge]
            length += math.dist(a, b) * snap_mm
        output.append({
            "status": "open",
            "edge_count": len(component_edges),
            "endpoints": [[_round(x, 1), _round(y, 1)] for x, y in endpoints[:8]],
            "bbox": [_round(min(xs), 1), _round(min(ys), 1),
                     _round(max(xs), 1), _round(max(ys), 1)],
            "length_mm": _round(length, 1),
            "issue": "边界未闭合，不计算板方量",
        })
    return output


def build_slabs(slab_dxf: Optional[Path],
                opening_dxf: Optional[Path],
                slab_layers: str,
                opening_layers: str,
                transform: tuple[float, float],
                snap_mm: float,
                thickness_mm: Optional[float],
                boundary_layers: str = DEFAULT_SLAB_BOUNDARY_LAYERS,
                model_bbox: Optional[list[float]] = None,
                panel_min_area_m2: float = 1.0,
                hatch_regions: Optional[list[dict[str, Any]]] = None,
                thickness_text_records: Optional[list[dict[str, Any]]] = None,
                opening_geometry_lines: Optional[list[dict[str, Any]]] = None,
                opening_note_records: Optional[list[dict[str, Any]]] = None,
                default_thickness_mm: Optional[float] = None,
                thickness_label_max_distance_mm: float = 1500.0,
                ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if slab_dxf is None:
        return [], {
            "status": "not-provided",
            "closed_count": 0,
            "open_count": 0,
            "closed_area_m2": 0.0,
            "net_volume_m3": None,
        }

    slab_lines = _filter_segments_to_bbox(
        _read_line_segments(slab_dxf, slab_layers, transform),
        model_bbox,
    )
    slab_loops = _component_cycles(
        [((float(s["a"][0]), float(s["a"][1])),
          (float(s["b"][0]), float(s["b"][1]))) for s in slab_lines],
        snap_mm,
    )
    openings: list[dict[str, Any]] = []
    if opening_dxf:
        opening_lines = _filter_segments_to_bbox(
            _read_line_segments(opening_dxf, opening_layers, transform),
            model_bbox,
        )
        openings = [
            loop for loop in _component_cycles(
                [((float(s["a"][0]), float(s["a"][1])),
                  (float(s["b"][0]), float(s["b"][1]))) for s in opening_lines],
                snap_mm,
            )
            if loop.get("status") == "closed"
        ]

    slab_rows: list[dict[str, Any]] = []
    closed_area = 0.0
    net_volume = 0.0 if thickness_mm else None
    closed_count = 0
    next_id = 1
    for loop in slab_loops:
        if loop.get("status") != "closed":
            continue
        points = [(float(x), float(y)) for x, y in loop.get("points") or []]
        deductions = []
        deduction_area = 0.0
        for opening in openings:
            op_points = [(float(x), float(y))
                         for x, y in opening.get("points") or []]
            if op_points and _point_in_polygon(op_points[0], points):
                deduction_area += float(opening.get("area_m2") or 0.0)
                deductions.append(opening)
        net_area = max(0.0, float(loop["area_m2"]) - deduction_area)
        volume = net_area * thickness_mm / 1000.0 if thickness_mm else None
        closed_area += net_area
        if volume is not None:
            net_volume += volume
        slab_rows.append({
            "id": f"S{next_id:04d}",
            "type": "slab",
            "area_m2": _round(net_area, 4),
            "gross_area_m2": _round(loop["area_m2"], 4),
            "opening_count": len(deductions),
            "opening_area_m2": _round(deduction_area, 4),
            "thickness_mm": thickness_mm,
            "volume_m3": _round(volume, 4) if volume is not None else None,
            "status": "closed",
            "points": loop.get("points") or [],
        })
        next_id += 1
        closed_count += 1

    open_loops = [loop for loop in slab_loops if loop.get("status") == "open"]
    boundary_lines = _filter_segments_to_bbox(
        _read_line_segments(slab_dxf, boundary_layers, transform),
        model_bbox,
    )
    planar_panels = _planar_face_polygons(
        boundary_lines, min_area_m2=panel_min_area_m2)
    for index, panel in enumerate(planar_panels, 1):
        panel["id"] = f"P{index:04d}"
        panel["type"] = "slab-panel"
        panel["status"] = "topology-candidate"
        panel["issue"] = "板面由梁墙边界平面切分，材料类别和板厚待分账"
    attribute_summary = assign_slab_attributes(
        planar_panels,
        hatch_regions or [],
        thickness_text_records or [],
        opening_geometry_lines or [],
        opening_note_records or [],
        transform,
        default_thickness_mm=default_thickness_mm,
        thickness_label_max_distance_mm=thickness_label_max_distance_mm,
    )
    return slab_rows, {
        "status": "partial" if open_loops else "complete-closed-loops",
        "closed_count": closed_count,
        "open_count": len(open_loops),
        "closed_area_m2": _round(closed_area, 4),
        "net_volume_m3": _round(net_volume, 4) if net_volume is not None else None,
        "opening_count": len(openings),
        "open_loops": open_loops,
        "boundary_line_count": len(boundary_lines),
        "planar_panel_count": len(planar_panels),
        "planar_panel_area_m2": _round(
            sum(float(row["area_m2"]) for row in planar_panels), 4),
        "planar_panel_candidates": planar_panels,
        "attribute_summary": attribute_summary,
        "issue": (
            f"{len(open_loops)} 条板边界链未闭合，未计入板方量"
            if open_loops else ""
        ),
    }


def _quantity_summary(beams: list[dict[str, Any]],
                      slabs: list[dict[str, Any]],
                      support: dict[str, Any],
                      story_height_mm: Optional[float],
                      run_registry: Optional[dict[str, Any]] = None,
                      slab_diagnostics: Optional[dict[str, Any]] = None,
                      component_labels: Optional[dict[str, Any]] = None
                      ) -> dict[str, Any]:
    beam_gross = sum(float(row.get("gross_volume_m3") or 0.0) for row in beams)
    beam_clear_rows = [
        row for row in beams if row.get("quantity_status") == "clear-span"]
    beam_clear = sum(float(row.get("clear_volume_m3") or 0.0)
                     for row in beam_clear_rows)
    beam_inferred_rows = [
        row for row in beams
        if row.get("quantity_status") == "clear-span-inferred"
    ]
    beam_inferred = sum(float(row.get("clear_volume_m3") or 0.0)
                        for row in beam_inferred_rows)
    beam_review_rows = [
        row for row in beams if row.get("quantity_status") == "clear-span-review"
    ]
    beam_review = sum(float(row.get("clear_volume_m3") or 0.0)
                      for row in beam_review_rows)
    beam_intersection_support_count = sum(
        int(row.get("beam_intersection_support_count") or 0)
        for row in beams)
    beam_intersection_review_support_count = sum(
        int(row.get("beam_intersection_review_support_count") or 0)
        for row in beams)
    beam_support_count_status_counts = Counter(
        str(row.get("support_count_status") or "unknown")
        for row in beams)
    beam_arbitrated_count = sum(
        1 for row in beams
        if (row.get("support_selection") or {}).get("status")
        == "expected-count-arbitrated")
    beam_rejected_support_candidate_count = sum(
        int((row.get("support_selection") or {}).get(
            "rejected_cluster_count") or 0)
        for row in beams)
    endpoint_polygon_support_count = sum(
        int(row.get("endpoint_polygon_support_count") or 0)
        for row in beams)

    wall_rows: list[dict[str, Any]] = []
    if story_height_mm:
        for idx, wall in enumerate(support.get("walls") or [], 1):
            length = float(wall["end"]) - float(wall["start"])
            volume = length * float(wall["width_mm"]) * story_height_mm / 1e9
            wall_rows.append({
                "id": f"W{idx:04d}",
                "type": "wall",
                "length_mm": _round(length, 1),
                "thickness_mm": _round(wall["width_mm"], 1),
                "source_thickness_mm": wall.get("source_width_mm"),
                "height_mm": story_height_mm,
                "volume_m3": _round(volume, 4),
                "status": "candidate",
                "issue": "墙中心线来自平行边界；已扣除边缘构件/柱轮廓重叠，未扣门窗",
                "orientation": wall["orientation"],
                "center": _round(wall["center"], 1),
            })
    edge_rows: list[dict[str, Any]] = []
    if story_height_mm:
        for idx, member in enumerate(support.get("edge_members") or [], 1):
            area_m2 = float(member["area_m2"])
            edge_rows.append({
                "id": f"E{idx:04d}",
                "type": "edge_member",
                "label": member.get("label") or "",
                "label_status": member.get("label_status") or "unlabeled",
                "label_distance_mm": member.get("label_distance_mm"),
                "label_basis": member.get("label_basis") or "",
                "label_x": member.get("label_x"),
                "label_y": member.get("label_y"),
                "mirror_partner_index": member.get("mirror_partner_index"),
                "mirror_axis_x_mm": member.get("mirror_axis_x_mm"),
                "mirror_match_distance_mm": (
                    member.get("mirror_match_distance_mm")),
                "mirror_review_reason": (
                    member.get("mirror_review_reason") or ""),
                "mirror_requires_review": bool(
                    member.get("mirror_requires_review")),
                "area_m2": _round(area_m2, 4),
                "height_mm": story_height_mm,
                "volume_m3": _round(area_m2 * story_height_mm / 1000.0, 4),
                "status": "candidate",
                "issue": "边缘构件由开口轮廓补缺口闭合，需与大样复核",
                "gap_mm": member.get("gap_mm"),
                "points": member.get("points") or [],
                "bbox": member.get("bbox") or [],
            })
    column_rows: list[dict[str, Any]] = []
    if story_height_mm:
        for idx, column in enumerate(support.get("columns") or [], 1):
            area = float(column["b_mm"]) * float(column["h_mm"])
            volume = area * story_height_mm / 1e9
            column_rows.append({
                "id": f"C{idx:04d}",
                "type": "column",
                "label": column.get("label") or "",
                "label_status": column.get("label_status") or "unlabeled",
                "label_distance_mm": column.get("label_distance_mm"),
                "label_basis": column.get("label_basis") or "",
                "label_x": column.get("label_x"),
                "label_y": column.get("label_y"),
                "mirror_partner_index": column.get("mirror_partner_index"),
                "mirror_axis_x_mm": column.get("mirror_axis_x_mm"),
                "mirror_match_distance_mm": (
                    column.get("mirror_match_distance_mm")),
                "mirror_review_reason": (
                    column.get("mirror_review_reason") or ""),
                "mirror_requires_review": bool(
                    column.get("mirror_requires_review")),
                "b_mm": _round(column["b_mm"], 1),
                "h_mm": _round(column["h_mm"], 1),
                "height_mm": story_height_mm,
                "volume_m3": _round(volume, 4),
                "status": "candidate",
                "issue": "柱来自正交边界矩形或闭合轮廓候选，需与轴网和大样复核",
                "x": _round((column["x0"] + column["x1"]) / 2.0, 1),
                "y": _round((column["y0"] + column["y1"]) / 2.0, 1),
            })

    slab_closed = sum(float(row.get("volume_m3") or 0.0) for row in slabs)
    registry_quantities = (run_registry or {}).get("quantities") or {}
    topology_runs = (run_registry or {}).get("runs") or []
    topology_assigned = sum(
        1 for run in topology_runs if run.get("matched_code"))
    topology_ambiguous = sum(
        1 for run in topology_runs if run.get("competing_codes"))
    slab_panel_area = float(
        (slab_diagnostics or {}).get("planar_panel_area_m2") or 0.0)
    slab_panel_count = int(
        (slab_diagnostics or {}).get("planar_panel_count") or 0)
    panel_attributes = (
        (slab_diagnostics or {}).get("attribute_summary") or {})
    return {
        "beam": {
            "count": len(beams),
            "gross_volume_m3": _round(beam_gross, 4),
            "clear_span_count": len(beam_clear_rows),
            "clear_span_volume_m3": _round(beam_clear, 4),
            "inferred_clear_span_count": len(beam_inferred_rows),
            "inferred_clear_span_volume_m3": _round(beam_inferred, 4),
            "review_clear_span_count": len(beam_review_rows),
            "review_clear_span_volume_m3": _round(beam_review, 4),
            "beam_intersection_support_count": beam_intersection_support_count,
            "beam_intersection_review_support_count": (
                beam_intersection_review_support_count),
            "support_count_status_counts": dict(sorted(
                beam_support_count_status_counts.items())),
            "support_arbitrated_count": beam_arbitrated_count,
            "rejected_support_candidate_count": (
                beam_rejected_support_candidate_count),
            "endpoint_polygon_support_count": (
                endpoint_polygon_support_count),
            "unresolved_count": (
                len(beams)
                - len(beam_clear_rows)
                - len(beam_inferred_rows)
                - len(beam_review_rows)
            ),
            "topology_run_count": int(
                registry_quantities.get("run_count") or 0),
            "topology_length_mm": _round(
                registry_quantities.get("centerline_length_mm"), 1),
            "topology_volume_m3": _round(
                registry_quantities.get("estimated_volume_m3"), 4),
            "topology_status_counts": (
                registry_quantities.get("status_counts") or {}),
            "topology_assigned_run_count": topology_assigned,
            "topology_ambiguous_run_count": topology_ambiguous,
            "topology_unassigned_run_count": (
                len(topology_runs) - topology_assigned),
            "topology_status": (
                (run_registry or {}).get("status")
                or "not-provided"
            ),
        },
        "wall": {
            "count": len(wall_rows),
            "candidate_volume_m3": _round(sum(
                float(row["volume_m3"]) for row in wall_rows), 4),
            "status": "candidate" if wall_rows else "not-modeled",
        },
        "edge_member": {
            "count": len(edge_rows),
            "candidate_volume_m3": _round(sum(
                float(row["volume_m3"]) for row in edge_rows), 4),
            "status": "candidate" if edge_rows else "not-modeled",
            "label_summary": (
                (component_labels or {}).get("edge_member") or {}),
        },
        "column": {
            "count": len(column_rows),
            "candidate_volume_m3": _round(sum(
                float(row["volume_m3"]) for row in column_rows), 4),
            "status": "candidate" if column_rows else "not-modeled",
            "label_summary": (
                (component_labels or {}).get("column") or {}),
        },
        "slab": {
            "closed_count": len(slabs),
            "closed_volume_m3": _round(slab_closed, 4),
            "status": "closed-loops-only" if slabs else "not-modeled",
            "topology_panel_count": slab_panel_count,
            "topology_panel_area_m2": _round(slab_panel_area, 4),
            "attribute_summary": panel_attributes,
        },
        "members": wall_rows + edge_rows + column_rows,
    }


def write_dxf_overlay(out_path: Path,
                      beams: list[dict[str, Any]],
                      slabs: list[dict[str, Any]],
                      support: dict[str, Any],
                      slab_diagnostics: Optional[dict[str, Any]] = None) -> None:
    from dev_dxf import new as new_dxf

    doc = new_dxf("R2010")
    msp = doc.modelspace()
    layers = {
        "AUTO_MODEL_BEAM": 1,
        "AUTO_MODEL_BEAM_NET": 3,
        "AUTO_MODEL_BEAM_REVIEW": 6,
        "AUTO_MODEL_WALL": 6,
        "AUTO_MODEL_EDGE_MEMBER": 4,
        "AUTO_MODEL_EDGE_MEMBER_REVIEW": 30,
        "AUTO_MODEL_COLUMN": 2,
        "AUTO_MODEL_SLAB": 5,
        "AUTO_MODEL_SLAB_PANEL": 8,
        "AUTO_MODEL_SLAB_120": 4,
        "AUTO_MODEL_SLAB_130": 5,
        "AUTO_MODEL_SLAB_140": 3,
        "AUTO_MODEL_SLAB_UNKNOWN": 30,
        "AUTO_MODEL_SUPPORT_SELECTED": 3,
        "AUTO_MODEL_SUPPORT_REJECTED": 1,
        "AUTO_MODEL_ISSUE": 30,
        "AUTO_MODEL_TEXT": 7,
    }
    for name, color in layers.items():
        if name not in doc.layers:
            doc.layers.add(name, color=color)

    for beam in beams:
        center = beam.get("centerline") or {}
        start, end = center.get("start"), center.get("end")
        if not start or not end:
            continue
        layer = (
            "AUTO_MODEL_BEAM_NET"
            if beam.get("quantity_status") in (
                "clear-span", "clear-span-inferred")
            else "AUTO_MODEL_BEAM_REVIEW"
            if beam.get("quantity_status") == "clear-span-review"
            else "AUTO_MODEL_ISSUE"
        )
        msp.add_line(start, end, dxfattribs={"layer": layer})
        midpoint = ((float(start[0]) + float(end[0])) / 2.0,
                    (float(start[1]) + float(end[1])) / 2.0)
        msp.add_text(
            f"{beam.get('code')} {beam.get('quantity_status')}",
            height=150,
            dxfattribs={"layer": "AUTO_MODEL_TEXT"},
        ).set_placement(midpoint)
        orientation = str(center.get("orientation") or "")
        try:
            if orientation == "H":
                axis = (float(start[1]) + float(end[1])) / 2.0
            else:
                axis = (float(start[0]) + float(end[0])) / 2.0
        except (TypeError, ValueError):
            axis = None
        if axis is not None:
            for support_evidence in beam.get("support_evidence") or []:
                selection_status = str(
                    support_evidence.get("selection_status") or "")
                if selection_status not in (
                        "selected", "rejected-by-expected-support-count"):
                    continue
                try:
                    position = (
                        float(support_evidence["start_mm"])
                        + float(support_evidence["end_mm"])
                    ) / 2.0
                    tick = max(
                        float(support_evidence.get("width_mm") or 200.0),
                        200.0,
                    )
                except (KeyError, TypeError, ValueError):
                    continue
                if orientation == "H":
                    tick_start = (position, axis - tick / 2.0)
                    tick_end = (position, axis + tick / 2.0)
                else:
                    tick_start = (axis - tick / 2.0, position)
                    tick_end = (axis + tick / 2.0, position)
                layer = (
                    "AUTO_MODEL_SUPPORT_REJECTED"
                    if selection_status.startswith("rejected")
                    else "AUTO_MODEL_SUPPORT_SELECTED"
                )
                msp.add_line(
                    tick_start,
                    tick_end,
                    dxfattribs={"layer": layer},
                )

    for wall in support.get("walls") or []:
        lo, hi = float(wall["start"]), float(wall["end"])
        center = float(wall["center"])
        if wall["orientation"] == "H":
            start, end = (lo, center), (hi, center)
        else:
            start, end = (center, lo), (center, hi)
        msp.add_line(start, end, dxfattribs={"layer": "AUTO_MODEL_WALL"})

    for member in support.get("edge_members") or []:
        points = member.get("points") or []
        if len(points) >= 3:
            layer = (
                "AUTO_MODEL_EDGE_MEMBER_REVIEW"
                if member.get("mirror_requires_review")
                else "AUTO_MODEL_EDGE_MEMBER"
            )
            msp.add_lwpolyline(
                points,
                close=True,
                dxfattribs={"layer": layer},
            )
            label = member.get("label") or "UNLABELED"
            status = member.get("label_status") or "unlabeled"
            msp.add_text(
                f"{label} {status}",
                height=100,
                dxfattribs={"layer": "AUTO_MODEL_TEXT"},
            ).set_placement(_polygon_center(points))

    for column in support.get("columns") or []:
        points = [
            (column["x0"], column["y0"]),
            (column["x1"], column["y0"]),
            (column["x1"], column["y1"]),
            (column["x0"], column["y1"]),
        ]
        msp.add_lwpolyline(
            points, close=True, dxfattribs={"layer": "AUTO_MODEL_COLUMN"})
        label = column.get("label") or "UNLABELED"
        status = column.get("label_status") or "unlabeled"
        msp.add_text(
            f"{label} {status}",
            height=100,
            dxfattribs={"layer": "AUTO_MODEL_TEXT"},
        ).set_placement(_polygon_center(points))

    for slab in slabs:
        points = slab.get("points") or []
        if len(points) >= 3:
            msp.add_lwpolyline(
                points, close=True, dxfattribs={"layer": "AUTO_MODEL_SLAB"})

    for panel in (slab_diagnostics or {}).get("planar_panel_candidates") or []:
        points = panel.get("points") or []
        if len(points) >= 3:
            thickness = panel.get("thickness_mm")
            layer = {
                120: "AUTO_MODEL_SLAB_120",
                130: "AUTO_MODEL_SLAB_130",
                140: "AUTO_MODEL_SLAB_140",
            }.get(thickness, "AUTO_MODEL_SLAB_UNKNOWN")
            msp.add_lwpolyline(
                points,
                close=True,
                dxfattribs={"layer": layer},
            )

    doc.saveas(str(out_path))


def render_md(result: dict[str, Any]) -> str:
    summary = result["quantities"]
    beam = summary["beam"]
    slab = summary["slab"]
    wall = summary["wall"]
    edge_member = summary["edge_member"]
    column = summary["column"]
    edge_labels = edge_member.get("label_summary") or {}
    column_labels = column.get("label_summary") or {}
    slab_attributes = slab.get("attribute_summary") or {}
    lines = [
        "# CAD 结构模型与混凝土台账",
        "",
        f"- 楼层：{result['floor'].get('label') or '-'}",
        f"- 模型状态：{result['status']}",
        f"- 梁对象：{beam['count']}，净跨已闭合 {beam['clear_span_count']}",
        f"- 墙条带候选：{wall['count']}，边缘构件：{edge_member['count']}，"
        f"柱候选：{column['count']}，闭合板环：{slab['closed_count']}",
        "",
        "## 混凝土台账",
        "",
        "| 构件 | 口径 | 方量m3 | 状态 |",
        "|---|---|---:|---|",
        f"| 梁 | 中心线粗算 | {beam['gross_volume_m3']:.4f} | 全部梁对象 |",
        f"| 梁 | 全图拓扑中心线粗算 | {beam['topology_volume_m3']:.4f} | "
        f"{beam['topology_run_count']} 段，含截面传播，不扣支座 |",
        f"| 梁 | 拓扑编号归属 | - | "
        f"{beam['topology_assigned_run_count']}/"
        f"{beam['topology_run_count']} 已归属，"
        f"{beam['topology_ambiguous_run_count']} 段有竞争编号 |",
        f"| 梁 | 支座净跨 | {beam['clear_span_volume_m3']:.4f} | "
        f"{beam['clear_span_count']} 根确认，"
        f"{beam.get('review_clear_span_count', 0)} 根复核，"
        f"{beam['inferred_clear_span_count']} 根推定，"
        f"{beam['unresolved_count']} 根未闭合；"
        f"交叉支座证据 {beam.get('beam_intersection_support_count', 0)} 个，"
        f"其中端部待复核 "
        f"{beam.get('beam_intersection_review_support_count', 0)} 个；"
        f"支座数超编号 "
        f"{(beam.get('support_count_status_counts') or {}).get('over', 0)} 根；"
        f"按跨数仲裁 {beam.get('support_arbitrated_count', 0)} 根；"
        f"端部构件补支座 "
        f"{beam.get('endpoint_polygon_support_count', 0)} 个 |",
        f"| 梁 | 推定端支座净跨 | {beam['inferred_clear_span_volume_m3']:.4f} | "
        f"{beam['inferred_clear_span_count']} 根，仅为待核对估算 |",
        f"| 梁 | 待复核支座净跨 | {beam.get('review_clear_span_volume_m3', 0):.4f} | "
        f"{beam.get('review_clear_span_count', 0)} 根，含端部构件/T形复核支座 |",
        f"| 板 | 净闭合区域 | {slab['closed_volume_m3']:.4f} | "
        f"{slab['status']} |",
        f"| 板 | 平面拓扑面候选 | - | "
        f"{slab['topology_panel_count']} 个，"
        f"{slab['topology_panel_area_m2']:.4f} m2，待材料分账 |",
        f"| 墙 | 扣除边缘/柱后的条带候选 | {wall['candidate_volume_m3']:.4f} | "
        f"{wall['status']} |",
        f"| 边缘构件 | 开口轮廓补缺闭合 | "
        f"{edge_member['candidate_volume_m3']:.4f} | "
        f"{edge_member['status']} |",
        f"| 柱 | 矩形候选 | {column['candidate_volume_m3']:.4f} | "
        f"{column['status']} |",
        "",
        "## 构件编号与板属性",
        "",
        f"- 边缘构件编号：{edge_labels.get('direct_count', 0)} 个直接标注，"
        f"{edge_labels.get('mirror_strict_count', 0)} 个严格镜像补齐，"
        f"{edge_labels.get('mirror_review_count', 0)} 个跨截断容差、待复核，"
        f"{edge_labels.get('unlabeled_count', 0)} 个未标注；"
        f"镜像轴 x={edge_labels.get('mirror_axis_x_mm') or '-'} mm。",
        f"- 柱编号：{column_labels.get('direct_count', 0)} 个直接标注，"
        f"{column_labels.get('mirror_count', 0)} 个镜像补齐，"
        f"{column_labels.get('unlabeled_count', 0)} 个未标注。",
        "- 板厚分账面积："
        + (
            "，".join(
                f"{key}mm={value:.4f} m2"
                for key, value in (
                    slab_attributes.get("thickness_area_m2") or {}).items())
            or "-"
        )
        + "；材料状态："
        + (
            "，".join(
                f"{key}={value:.4f} m2"
                for key, value in (
                    slab_attributes.get("material_area_m2") or {}).items())
            or "-"
        )
        + f"；板厚依据：图纸直接标注 {slab_attributes.get('direct_thickness_count', 0)} 个，"
        + f"图例规则待复核 {slab_attributes.get('thickness_review_required_count', 0)} 个，"
        + f"默认值 {slab_attributes.get('thickness_default_count', 0)} 个。",
        f"- 洞口候选板面："
        f"{slab_attributes.get('opening_candidate_count', 0)} 个；"
        "未形成可靠闭合扣减环前不扣板方量。",
        "",
        "## 梁净跨缺口",
        "",
        "| 编号 | 截面 | 粗长mm | 净长mm | 支座数 | 状态 | 缺口 |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for row in result["members"]["beams"]:
        lines.append(
            f"| {row.get('code') or '-'} | {row.get('section') or '-'} | "
            f"{row.get('centerline_length_mm') or '-'} | "
            f"{row.get('clear_length_mm') or '-'} | {row.get('support_count') or 0} | "
            f"{row.get('quantity_status')} | {row.get('issue') or '-'} |")
    lines += [
        "",
        "## 口径与边界",
        "",
        "- 梁中心线来自已展开梁边界双线；墙柱支座来自指定 DXF 的平行边界配对。",
        "- 全图拓扑中心线粗算补出未重复标注的梁段，截面按标注、近邻、镜像和默认值分级；仍不扣支座。",
        "- 只有首尾均有支座、相邻支座之间形成净跨的梁才计入“支座净跨”方量。",
        "- 交叉梁支座证据仅在显式启用 `--include-beam-intersections` 时加入，"
        "并保留墙柱支座和交叉梁支座的来源；当前仍不得当作正式净跨。",
        "- 板只计算闭合环，开洞按闭合环包含关系扣减；开放边界链全部列为缺口。",
        "- 墙条带、边缘构件和柱分栏保留；当前已经扣除轮廓重叠，"
        "材料归属尚未闭合前不得直接相加为剪力墙净量。",
        "- 边缘构件编号优先取实际 TEXT 插入点；严格镜像只在同形状、同 y 和"
        "镜像轴均匹配时补齐，截断轮廓的宽窗匹配全部标为待复核，不得直接视为确认。",
        "- 板厚文字优先于板填充规则，板填充规则优先于“未标注 130”说明；"
        "HATCH 与图例的关联规则仍需视觉复核，叠合板和现浇板拆分仍以预制板拆分图为准。",
        "- 当前结果用于结构模型建设和逐项对账，不能替代广联达模型、翻样或结算。",
        "",
    ]
    return "\n".join(lines)


def csv_rows(result: dict[str, Any]) -> list[list[str]]:
    headers = [
        "构件类型", "编号", "构件代号", "截面", "长度mm", "面积m2",
        "粗方量m3", "净方量m3", "状态", "缺口",
        "板厚mm", "材料状态", "开洞状态",
        "编号状态", "编号/属性依据", "镜像伙伴", "镜像匹配距离mm", "复核提示",
    ]
    rows = [headers]
    for beam in result["members"]["beams"]:
        rows.append([
            "梁", beam.get("id") or "", beam.get("code") or "",
            beam.get("section") or "", str(beam.get("centerline_length_mm") or ""),
            "", str(beam.get("gross_volume_m3") or ""),
            str(beam.get("clear_volume_m3") or ""),
            beam.get("quantity_status") or "", beam.get("issue") or "",
            "", "", "", "", "", "", "", "",
        ])
    for slab in result["members"]["slabs"]:
        rows.append([
            "板", slab.get("id") or "", "", "",
            "", str(slab.get("area_m2") or ""), "",
            str(slab.get("volume_m3") or ""), slab.get("status") or "",
            "", "", "", "", "", "", "", "", "",
        ])
    for panel in result["members"].get("slab_panels") or []:
        rows.append([
            "板", panel.get("id") or "", "", "",
            "", str(panel.get("area_m2") or ""), "",
            "", panel.get("status") or "",
            panel.get("issue") or "",
            str(panel.get("thickness_mm") or ""),
            panel.get("material_system") or "",
            panel.get("opening_status") or "",
            "", panel.get("thickness_verification") or "",
            "", "", panel.get("attribute_issue") or "",
        ])
    for member in result["quantities"]["members"]:
        if member.get("type") == "edge_member":
            member_type = "边缘构件"
        elif member.get("type") == "wall":
            member_type = "墙"
        else:
            member_type = "柱"
        rows.append([
            member_type,
            member.get("id") or "", "",
            (f"{member.get('b_mm')}x{member.get('h_mm')}"
             if member.get("type") == "column" else ""),
            str(member.get("length_mm") or ""),
            str(member.get("area_m2") or ""),
            str(member.get("volume_m3") or ""), "",
            member.get("status") or "", member.get("issue") or "",
            "", "", "",
            member.get("label_status") or "",
            member.get("label_basis") or "",
            str(member.get("mirror_partner_index") or ""),
            str(member.get("mirror_match_distance_mm") or ""),
            (
                "镜像待复核；" if member.get("mirror_requires_review")
                else ""
            ) + (member.get("issue") or ""),
        ])
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(
        description="从梁中心线、墙柱和平板几何组装结构模型与混凝土台账")
    ap.add_argument("--beam-json", required=True,
                    help="cad_beam_objects 输出的梁中心线 JSON")
    ap.add_argument("--beam-dxf", default=None,
                    help="梁展开几何 DXF；--*-transform auto 时用于自动配准")
    ap.add_argument("--support-dxf", default=None,
                    help="墙柱平法展开 DXF；未传时不计算梁净跨")
    ap.add_argument("--slab-dxf", default=None,
                    help="板结构展开 DXF")
    ap.add_argument("--opening-dxf", default=None,
                    help="板开洞展开 DXF；默认与 --slab-dxf 相同")
    ap.add_argument("--text-json", default=None,
                    help="含 text_records 的 CAD 文本明细 JSON")
    ap.add_argument("--component-sheet", type=int, default=None,
                    help="墙柱构件文字所在 sheet；不传时跨 sheet 匹配")
    ap.add_argument("--component-text-layer", default=DEFAULT_COMPONENT_TEXT_LAYER,
                    help="墙柱构件文字图层正则")
    ap.add_argument("--edge-member-label-pattern",
                    default=DEFAULT_EDGE_MEMBER_LABEL_PATTERN,
                    help="边缘构件编号正则")
    ap.add_argument("--column-label-pattern", default=DEFAULT_COLUMN_LABEL_PATTERN,
                    help="柱编号正则")
    ap.add_argument("--component-label-max-distance-mm", type=float,
                    default=1200.0,
                    help="构件文字到轮廓的最大关联距离")
    ap.add_argument("--edge-mirror-match-tolerance-mm", type=float,
                    default=25.0,
                    help="边缘构件严格镜像匹配容差")
    ap.add_argument("--edge-mirror-review-tolerance-mm", type=float,
                    default=800.0,
                    help="边缘构件截断轮廓的待复核镜像匹配容差；0=关闭")
    ap.add_argument("--edge-mirror-review-shape-tolerance-mm", type=float,
                    default=600.0,
                    help="待复核镜像匹配允许的边长差")
    ap.add_argument("--slab-sheet", type=int, default=None,
                    help="板文字所在 sheet；不传时跨 sheet 匹配")
    ap.add_argument("--slab-hatch-source", default=None,
                    help="保留 HATCH 的板图 DWG/DXF；用于板填充分区")
    ap.add_argument("--slab-hatch-layers", default=DEFAULT_SLAB_HATCH_LAYERS,
                    help="板填充 HATCH 图层正则")
    ap.add_argument("--slab-hatch-rule", type=_parse_hatch_rule_map, default={},
                    help="填充规则，如 407573,407575=drop-30;407569=140;9520=120")
    ap.add_argument("--slab-default-thickness-mm", type=float, default=None,
                    help="未标注板厚；二层本图可为 130")
    ap.add_argument("--slab-thickness-text-layer",
                    default=DEFAULT_SLAB_THICKNESS_TEXT_LAYER,
                    help="板厚文字图层正则")
    ap.add_argument("--slab-note-layer", default=DEFAULT_SLAB_NOTE_LAYER,
                    help="板洞口/说明文字图层正则")
    ap.add_argument("--floor-label", default="",
                    help="楼层/图纸名称")
    ap.add_argument("--elevation-mm", type=float, default=None,
                    help="结构标高，单位 mm")
    ap.add_argument("--story-height-mm", type=float, default=None,
                    help="层高，单位 mm；仅用于墙柱候选方量")
    ap.add_argument("--slab-thickness-mm", type=float, default=None,
                    help="板厚，单位 mm")
    ap.add_argument("--concrete-grade", default="",
                    help="本层梁板混凝土等级，如 C30")
    ap.add_argument("--support-transform", type=_parse_transform, default=(0.0, 0.0),
                    help="墙柱 DXF 到梁 DXF 的平移 dx,dy；可传 auto")
    ap.add_argument("--slab-transform", type=_parse_transform, default=(0.0, 0.0),
                    help="板 DXF 到梁 DXF 的平移 dx,dy；可传 auto")
    ap.add_argument("--auto-align-layers", default=DEFAULT_AUTO_ALIGN_LAYERS,
                    help="自动配准使用的共同结构图层正则")
    ap.add_argument("--support-layers", default=DEFAULT_SUPPORT_LAYERS)
    ap.add_argument("--wall-layers", default=DEFAULT_WALL_LAYERS)
    ap.add_argument("--edge-member-layers", default=DEFAULT_EDGE_MEMBER_LAYERS)
    ap.add_argument("--column-layers", default=DEFAULT_COLUMN_LAYERS)
    ap.add_argument("--slab-layers", default=DEFAULT_SLAB_LAYERS)
    ap.add_argument("--slab-boundary-layers", default=DEFAULT_SLAB_BOUNDARY_LAYERS)
    ap.add_argument("--opening-layers", default=DEFAULT_OPENING_LAYERS)
    ap.add_argument("--max-support-width-mm", type=float, default=1200.0)
    ap.add_argument("--beam-end-tolerance-mm", type=float, default=300.0)
    ap.add_argument("--min-span-mm", type=float, default=300.0)
    ap.add_argument("--assumed-end-support-width-mm", type=float, default=0.0,
                    help="端部缺支座时按该宽度做待核对净跨估算；0=关闭")
    ap.add_argument("--include-beam-intersections", action="store_true",
                    help="把全图拓扑中的正交梁段作为交叉支座候选；结果单列来源")
    ap.add_argument("--beam-intersection-end-tolerance-mm", type=float,
                    default=0.0,
                    help="梁段端部距目标轴在此范围内时作为T形交叉待复核支座")
    ap.add_argument("--arbitrate-support-count", action="store_true",
                    help="候选支座超过编号跨数要求时，按端点和证据分保留指定数量")
    ap.add_argument("--support-cluster-tolerance-mm", type=float,
                    default=400.0,
                    help="归并同一支座节点的最大中心距")
    ap.add_argument("--endpoint-polygon-support-search-mm", type=float,
                    default=0.0,
                    help="梁端附近该距离内存在边缘构件/柱时补端部支座；0=关闭")
    ap.add_argument("--endpoint-polygon-width-mm", type=float,
                    default=500.0,
                    help="端部构件与梁投影不重叠时使用的复核支座宽度")
    ap.add_argument("--min-wall-candidate-mm", type=float, default=500.0)
    ap.add_argument("--wall-width-tolerance-mm", type=float, default=60.0)
    ap.add_argument("--slab-snap-mm", type=float, default=10.0)
    ap.add_argument("--slab-panel-min-area-m2", type=float, default=1.0)
    ap.add_argument("--format", default="all",
                    choices=["all", "json", "csv", "md", "dxf"])
    ap.add_argument("-o", "--out", default="cad_structure_model")
    args = ap.parse_args()

    beam_json = Path(args.beam_json)
    if not beam_json.exists():
        print(f"梁对象 JSON 不存在：{beam_json}", file=sys.stderr)
        return 2
    beam_data = json.loads(beam_json.read_text(encoding="utf-8"))
    beam_bbox = [float(v) for v in beam_data.get("bbox") or []]
    if len(beam_bbox) != 4:
        print("梁对象 JSON 缺少有效 bbox，无法自动配准", file=sys.stderr)
        return 2
    beam_dxf = Path(args.beam_dxf) if args.beam_dxf else None
    support_dxf = Path(args.support_dxf) if args.support_dxf else None
    slab_dxf = Path(args.slab_dxf) if args.slab_dxf else None
    opening_dxf = Path(args.opening_dxf) if args.opening_dxf else slab_dxf
    alignment: dict[str, Any] = {"support": None, "slab": None}

    support_transform = args.support_transform
    if support_transform == "auto":
        if not beam_dxf or not support_dxf:
            print("--support-transform auto 需要同时提供 --beam-dxf 和 --support-dxf",
                  file=sys.stderr)
            return 2
        try:
            alignment["support"] = estimate_translation(
                beam_dxf,
                support_dxf,
                args.auto_align_layers,
                beam_bbox,
                beam_rows=beam_data.get("rows") or [],
                support_max_width_mm=args.max_support_width_mm,
            )
            support_transform = tuple(alignment["support"]["transform"])
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2

    slab_transform = args.slab_transform
    if slab_transform == "auto":
        if not beam_dxf or not slab_dxf:
            print("--slab-transform auto 需要同时提供 --beam-dxf 和 --slab-dxf",
                  file=sys.stderr)
            return 2
        try:
            alignment["slab"] = estimate_translation(
                beam_dxf, slab_dxf, args.auto_align_layers, beam_bbox)
            slab_transform = tuple(alignment["slab"]["transform"])
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2

    support = build_support_model(
        support_dxf,
        args.support_layers,
        args.wall_layers,
        args.edge_member_layers,
        args.column_layers,
        support_transform,
        args.max_support_width_mm,
        args.min_wall_candidate_mm,
        beam_bbox,
        args.wall_width_tolerance_mm,
    )
    text_records = _load_text_records(
        Path(args.text_json) if args.text_json else None)
    component_labels: dict[str, Any] = {}
    if text_records:
        component_labels = annotate_support_components(
            support,
            text_records,
            tuple(support_transform),
            args.component_text_layer,
            args.edge_member_label_pattern,
            args.column_label_pattern,
            sheet=args.component_sheet,
            max_distance_mm=args.component_label_max_distance_mm,
            edge_mirror_match_tolerance_mm=(
                args.edge_mirror_match_tolerance_mm),
            edge_mirror_review_tolerance_mm=(
                args.edge_mirror_review_tolerance_mm or None),
            edge_mirror_review_shape_tolerance_mm=(
                args.edge_mirror_review_shape_tolerance_mm),
        )
    beam_support_runs = (
        _beam_intersection_support_runs(
            (beam_data.get("run_registry") or {}).get("runs") or [])
        if args.include_beam_intersections else []
    )
    endpoint_support_polygons: list[dict[str, Any]] = []
    for index, member in enumerate(
            support.get("edge_members") or [], 1):
        endpoint_support_polygons.append({
            "id": f"E{index:04d}",
            "label": member.get("label") or "",
            "source": "edge-member",
            "points": member.get("points") or [],
        })
    for index, column in enumerate(support.get("columns") or [], 1):
        endpoint_support_polygons.append({
            "id": f"C{index:04d}",
            "label": column.get("label") or "",
            "source": "column",
            "points": [
                [column["x0"], column["y0"]],
                [column["x1"], column["y0"]],
                [column["x1"], column["y1"]],
                [column["x0"], column["y1"]],
            ],
        })
    beams = build_beams(
        beam_json,
        support.get("support_runs") or [],
        args.max_support_width_mm,
        args.beam_end_tolerance_mm,
        args.min_span_mm,
        args.assumed_end_support_width_mm,
        beam_support_runs,
        args.beam_intersection_end_tolerance_mm,
        args.arbitrate_support_count,
        args.support_cluster_tolerance_mm,
        endpoint_support_polygons,
        args.endpoint_polygon_support_search_mm,
        args.endpoint_polygon_width_mm,
    )
    hatch_source = (
        Path(args.slab_hatch_source) if args.slab_hatch_source else slab_dxf)
    hatch_regions = load_hatch_regions(
        hatch_source,
        args.slab_hatch_layers,
        tuple(slab_transform),
        beam_bbox,
        rule_map=args.slab_hatch_rule,
    )
    thickness_text_records = [
        row for row in text_records
        if (args.slab_sheet is None or row.get("sheet") == args.slab_sheet)
        and re.search(
            args.slab_thickness_text_layer,
            str(row.get("layer") or ""),
            re.I,
        )
    ]
    opening_note_records = [
        row for row in text_records
        if (args.slab_sheet is None or row.get("sheet") == args.slab_sheet)
        and re.search(
            args.slab_note_layer,
            str(row.get("layer") or ""),
            re.I,
        )
    ]
    opening_geometry_lines = _read_geometry_lines(
        opening_dxf,
        args.opening_layers,
        tuple(slab_transform),
    )
    slabs, slab_diagnostics = build_slabs(
        slab_dxf,
        opening_dxf,
        args.slab_layers,
        args.opening_layers,
        slab_transform,
        args.slab_snap_mm,
        args.slab_thickness_mm,
        args.slab_boundary_layers,
        beam_bbox,
        args.slab_panel_min_area_m2,
        hatch_regions=hatch_regions,
        thickness_text_records=thickness_text_records,
        opening_geometry_lines=opening_geometry_lines,
        opening_note_records=opening_note_records,
        default_thickness_mm=args.slab_default_thickness_mm,
    )
    quantities = _quantity_summary(
        beams,
        slabs,
        support,
        args.story_height_mm,
        beam_data.get("run_registry"),
        slab_diagnostics,
        component_labels,
    )
    issues = [
        {
            "member_type": "beam",
            "member_id": row["id"],
            "code": row.get("code"),
            "issue": row.get("issue"),
        }
        for row in beams if row.get("issue")
    ]
    endpoint_polygon_supports_enabled = bool(
        args.endpoint_polygon_support_search_mm > 0
        and endpoint_support_polygons
    )
    result = {
        "schema": "cad-structure-model/v0.5",
        "floor": {
            "label": args.floor_label,
            "elevation_mm": args.elevation_mm,
            "story_height_mm": args.story_height_mm,
            "concrete_grade": args.concrete_grade,
        },
        "units": {"length": "mm", "area": "m2", "volume": "m3"},
        "support_transform": list(support_transform),
        "slab_transform": list(slab_transform),
        "beam_intersection_supports_enabled": bool(beam_support_runs),
        "endpoint_polygon_supports_enabled": endpoint_polygon_supports_enabled,
        "support_policy": {
            "assumed_end_support_width_mm": args.assumed_end_support_width_mm,
            "beam_intersection_end_tolerance_mm": (
                args.beam_intersection_end_tolerance_mm),
            "support_cluster_tolerance_mm": (
                args.support_cluster_tolerance_mm),
            "endpoint_polygon_support_search_mm": (
                args.endpoint_polygon_support_search_mm),
            "endpoint_polygon_width_mm": args.endpoint_polygon_width_mm,
        },
        "alignment": alignment,
        "topology": {
            "support": support,
            "slab": slab_diagnostics,
            "hatch_regions": hatch_regions,
        },
        "members": {
            "beams": beams,
            "slabs": slabs,
            "slab_panels": slab_diagnostics.get("planar_panel_candidates") or [],
            "walls": support.get("walls") or [],
            "edge_members": support.get("edge_members") or [],
            "columns": support.get("columns") or [],
        },
        "run_registry": beam_data.get("run_registry"),
        "component_labels": component_labels,
        "quantities": quantities,
        "issues": issues,
        "status": (
            "结构模型第六阶段：已补梁端附近边缘构件/柱复核支座，并保留推定端和"
            "按跨数淘汰证据；端部构件与T形支座仍待原图确认，板材料体系和洞口"
            "扣减仍待复核"
            if endpoint_polygon_supports_enabled and args.arbitrate_support_count
            else
            "结构模型第六阶段：已补梁端附近边缘构件/柱复核支座并保留推定端；"
            "端部构件与T形支座仍待原图确认，板材料体系和洞口扣减仍待复核"
            if endpoint_polygon_supports_enabled else
            "结构模型第五阶段：已按编号跨数仲裁支座候选，并保留当选/淘汰证据；"
            "支座位置、板材料体系和洞口扣减仍待复核"
            if args.arbitrate_support_count else
            "结构模型第四阶段：已加入正交梁交叉支座候选，并保留墙柱支座来源；"
            "板材料体系、洞口扣减及净跨最终复核尚未完成"
            if beam_support_runs else
            "结构模型第三阶段：已关联墙柱文字编号、板填充规则、板厚和洞口候选；"
            "叠合板拆分及全构件布尔扣减尚未完成"
        ),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.format in ("md", "all"):
        out.with_suffix(".md").write_text(render_md(result), encoding="utf-8")
        print(f"已写出 {out.with_suffix('.md')}", file=sys.stderr)
    if args.format in ("json", "all"):
        out.with_suffix(".json").write_text(
            json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"已写出 {out.with_suffix('.json')}", file=sys.stderr)
    if args.format in ("csv", "all"):
        with out.with_suffix(".csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(csv_rows(result))
        print(f"已写出 {out.with_suffix('.csv')}", file=sys.stderr)
    if args.format in ("dxf", "all"):
        dxf_path = out.with_suffix(".model.dxf")
        write_dxf_overlay(dxf_path, beams, slabs, support, slab_diagnostics)
        print(f"已写出 {dxf_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
