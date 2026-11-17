#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""审计梁图层图线是否已被算量实例覆盖，找出图框内未提取的梁候选。"""



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
from collections import defaultdict
from pathlib import Path
from typing import Any


SCHEMA = "cad-beam-coverage-audit/v0.1"

NOTE_MIRROR = "（关于镜像轴对称的真构件，是否已计入须人工判定）"
NOTE_TRANSLATED = "（整视图平移重复绘制，只作证据不计漏量）"

BEAM_LAYERS = ("S-梁-虚线", "S-梁-实线")
COUPLING_LAYERS = ("S-剪力墙-连梁",)



def _orientation(first: tuple, second: tuple) -> str:
    return "H" if abs(first[1] - second[1]) <= abs(first[0] - second[0]) else "V"


def _normalize_entities(raw: list[dict[str, Any]], layers: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in raw:
        layer = _text(row.get("layer"))
        if layer not in layers:
            continue
        points = [
            (_number(point[0]), _number(point[1]))
            for point in (row.get("points") or []) if point and len(point) >= 2
        ]
        for index in range(len(points) - 1):
            start, end = points[index], points[index + 1]
            if math.hypot(end[0] - start[0], end[1] - start[1]) < 1.0:
                continue
            rows.append({
                "handle": _text(row.get("handle")),
                "layer": layer,
                "start": start,
                "end": end,
                "orientation": _orientation(start, end),
                "length_mm": math.hypot(end[0] - start[0], end[1] - start[1]),
            })
    return rows


def _read_entities(dxf_path: Path, layers: set[str]) -> list[dict[str, Any]]:
    from dev_dxf import readfile

    document = readfile(str(dxf_path))
    raw: list[dict[str, Any]] = []
    for entity in document.modelspace():
        if _text(entity.dxf.layer) not in layers:
            continue
        if entity.dxftype() == "LINE":
            points = [
                [float(entity.dxf.start.x), float(entity.dxf.start.y)],
                [float(entity.dxf.end.x), float(entity.dxf.end.y)],
            ]
        elif entity.dxftype() == "LWPOLYLINE":
            points = [[float(x), float(y)] for x, y in entity.get_points("xy")]
        else:
            continue
        raw.append({
            "handle": _text(entity.dxf.handle),
            "layer": _text(entity.dxf.layer),
            "points": points,
        })
    return raw


def _run_faces(model: dict[str, Any]) -> dict[str, list[tuple[str, float, float, float]]]:
    """按方向汇总每条 run 的两条边线：(axis, from, to, width)。"""
    faces: dict[str, list[tuple[str, float, float, float]]] = {"H": [], "V": []}
    registry = model.get("run_registry") or {}
    for run in registry.get("runs") or []:
        orientation = _text(run.get("orientation"))
        if orientation not in faces:
            continue
        half = _number(run.get("paired_width_mm"), 200.0) / 2.0
        axis = _number(run.get("axis_mm"))
        start = _number(run.get("start_mm"))
        end = _number(run.get("end_mm"))
        run_id = _text(run.get("id"))
        for offset in (axis - half, axis + half):
            faces[orientation].append((run_id, offset, min(start, end), max(start, end)))
    return faces


def _line_bounds(row: dict[str, Any]) -> tuple[float, float, float]:
    """返回 (横向坐标, 沿线起点, 沿线终点)。"""
    if row["orientation"] == "H":
        cross = (row["start"][1] + row["end"][1]) / 2.0
        low, high = sorted((row["start"][0], row["end"][0]))
    else:
        cross = (row["start"][0] + row["end"][0]) / 2.0
        low, high = sorted((row["start"][1], row["end"][1]))
    return cross, low, high


def _uncovered_intervals(
        row: dict[str, Any],
        faces: dict[str, list[tuple]],
        tolerance: float,
        ) -> tuple[float, list[tuple[float, float]], list[str]]:
    """按区间求未被实例边线吃到的线段，避免整条线只按端点判覆盖。"""
    cross, low, high = _line_bounds(row)
    spans = []
    run_ids: list[str] = []
    for run_id, offset, face_low, face_high in faces.get(row["orientation"], []):
        if abs(cross - offset) > tolerance:
            continue
        start = max(low, face_low - tolerance)
        end = min(high, face_high + tolerance)
        if end > start:
            spans.append((start, end))
            if run_id not in run_ids:
                run_ids.append(run_id)
    spans.sort()
    merged: list[list[float]] = []
    for start, end in spans:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    covered = sum(end - start for start, end in merged)
    gaps: list[tuple[float, float]] = []
    cursor = low
    for start, end in merged:
        if start > cursor:
            gaps.append((cursor, start))
        cursor = max(cursor, end)
        if cursor >= high:
            break
    if cursor < high:
        gaps.append((cursor, high))
    return covered, [gap for gap in gaps if gap[1] - gap[0] > 1.0], run_ids


def _stub_segment(
        row: dict[str, Any],
        gap: tuple[float, float],
        status: str,
        ) -> dict[str, Any]:
    start, end = gap
    if row["orientation"] == "H":
        first, second = (start, row["start"][1]), (end, row["end"][1])
    else:
        first, second = (row["start"][0], start), (row["end"][0], end)
    stub = dict(row)
    stub["start"] = first
    stub["end"] = second
    stub["length_mm"] = end - start
    stub["status"] = status
    return stub


def _face_spans(
        faces: dict[str, list[tuple]],
        orientation: str,
        cross: float,
        tolerance: float,
        ) -> list[list[float]]:
    """取横向坐标相同（容差内）的全部实例边线区间。"""
    spans = [[low, high] for _, offset, low, high in faces.get(orientation, [])
             if abs(cross - offset) <= tolerance]
    spans.sort()
    return spans


def _covered(spans: list[list[float]], low: float, high: float) -> float:
    if high <= low or not spans:
        return 0.0
    total = 0.0
    for start, end in spans:
        overlap = min(high, end) - max(low, start)
        if overlap > 0:
            total += overlap
    return min(1.0, total / (high - low))


def _translation_offset(
        row: dict[str, Any],
        faces: dict[str, list[tuple]],
        tolerance: float,
        ) -> float | None:
    """整视图平移重复：H 线沿线平移、V 线横向平移，能被已提取边线覆盖。

    候选偏移只取实例边线端点对齐产生的位移，择优顺序为覆盖率最高、位移最小，
    因此重复视图落在最近的一次对齐上，不会挑到跨越半张图的假偏移。
    """
    cross, low, high = _line_bounds(row)
    if row["orientation"] == "H":
        spans = _face_spans(faces, "H", cross, tolerance)
        best: tuple[float, float] | None = None
        for start, end in spans:
            for candidate in (start - low, end - high):
                if abs(candidate) <= 1000.0:
                    continue
                ratio = _covered(spans, low + candidate, high + candidate)
                if ratio < 0.9:
                    continue
                if best is None or (ratio, -abs(candidate)) > best:
                    best = (ratio, candidate)
        return best[1] if best else None
    best = None
    for _, offset, _, _ in faces.get("V", []):
        candidate = offset - cross
        if abs(candidate) <= 1000.0:
            continue
        spans = _face_spans(faces, "V", offset, tolerance)
        ratio = _covered(spans, low, high)
        if ratio < 0.9:
            continue
        if best is None or (ratio, -abs(candidate)) > best:
            best = (ratio, candidate)
    return best[1] if best else None


def _mirrored_pair_offset(
        row: dict[str, Any],
        faces: dict[str, list[tuple]],
        mirror_axes: list[float],
        tolerance: float,
        ) -> float | None:
    """镜像对称构件：关于模型已识别的镜像轴翻折后能被已提取边线覆盖。"""
    cross, low, high = _line_bounds(row)
    for axis in mirror_axes:
        if row["orientation"] == "H":
            spans = _face_spans(faces, "H", cross, tolerance)
            if _covered(spans, 2 * axis - high, 2 * axis - low) >= 0.9:
                return axis
        else:
            mirrored = 2 * axis - cross
            if abs(mirrored - cross) <= tolerance:
                continue
            spans = _face_spans(faces, "V", mirrored, tolerance)
            if _covered(spans, low, high) >= 0.9:
                return axis
    return None


def _mirror_pair_countable(
        mirrored_volume: float,
        residual: float,
        tolerance: float,
        ) -> bool:
    """镜像对称体量只有在与缺口同量级时才可能是漏量，超出即判对称视图副本。"""
    if residual < 0:
        return False
    return mirrored_volume <= residual + max(tolerance, 0.0)


def _model_plan_bbox(model: dict[str, Any]) -> list[float]:
    """板面域并集 + 已提取梁实例范围，作为本层平面轮廓。"""
    xs: list[float] = []
    ys: list[float] = []
    panels = ((model.get("members") or {}).get("slab_panels")) or []
    for panel in panels:
        bbox = panel.get("bbox") or panel.get("bbox_mm")
        if isinstance(bbox, list) and len(bbox) == 4:
            xs += [bbox[0], bbox[2]]
            ys += [bbox[1], bbox[3]]
        for point in panel.get("points") or []:
            if isinstance(point, (list, tuple)) and len(point) >= 2:
                xs.append(_number(point[0]))
                ys.append(_number(point[1]))
    registry = model.get("run_registry") or {}
    for run in registry.get("runs") or []:
        axis = _number(run.get("axis_mm"))
        low = min(_number(run.get("start_mm")), _number(run.get("end_mm")))
        high = max(_number(run.get("start_mm")), _number(run.get("end_mm")))
        if run.get("orientation") == "H":
            xs += [low, high]
            ys += [axis, axis]
        else:
            xs += [axis, axis]
            ys += [low, high]
    if not xs or not ys:
        return []
    return [min(xs), min(ys), max(xs), max(ys)]


def _inside_bbox(bbox: list[float], point: tuple, margin: float) -> bool:
    return (bbox[0] - margin <= point[0] <= bbox[2] + margin
            and bbox[1] - margin <= point[1] <= bbox[3] + margin)


def _pair_candidates(
        segments: list[dict[str, Any]],
        options: dict[str, float],
        heights: dict[str, float],
        ) -> list[dict[str, Any]]:
    used: set[int] = set()
    candidates: list[dict[str, Any]] = []
    for orientation in ("H", "V"):
        rows = [
            (index, row) for index, row in enumerate(segments)
            if row["orientation"] == orientation
        ]
        rows.sort(key=lambda item: -item[1]["length_mm"])
        for position, (index, first) in enumerate(rows):
            if index in used:
                continue
            best: tuple | None = None
            for other_position in range(position + 1, len(rows)):
                other_index, second = rows[other_position]
                if other_index in used:
                    continue
                if orientation == "H":
                    gap = abs(first["start"][1] - second["start"][1])
                    low = max(
                        min(first["start"][0], first["end"][0]),
                        min(second["start"][0], second["end"][0]))
                    high = min(
                        max(first["start"][0], first["end"][0]),
                        max(second["start"][0], second["end"][0]))
                    axis = (first["start"][1] + second["start"][1]) / 2.0
                    extent = [low, axis, high, axis]
                else:
                    gap = abs(first["start"][0] - second["start"][0])
                    low = max(
                        min(first["start"][1], first["end"][1]),
                        min(second["start"][1], second["end"][1]))
                    high = min(
                        max(first["start"][1], first["end"][1]),
                        max(second["start"][1], second["end"][1]))
                    axis = (first["start"][0] + second["start"][0]) / 2.0
                    extent = [axis, low, axis, high]
                if not (options["pair_min_width_mm"] <= gap
                        <= options["pair_max_width_mm"]):
                    continue
                if high - low < options["pair_min_overlap_mm"]:
                    continue
                if best is None or gap < best[0]:
                    best = (gap, other_index, second, low, high, axis, extent)
            if best is None:
                continue
            gap, other_index, second, low, high, axis, extent = best
            length = high - low
            height = heights.get(f"{round(gap)}", options["default_height_mm"])
            volume = gap * height * length / 1_000_000_000.0
            candidates.append({
                "status": "uncovered-beam-candidate",
                "handles": sorted([first["handle"], second["handle"]]),
                "orientation": orientation,
                "axis_mm": _round(axis, 1),
                "start_mm": _round(low, 1),
                "end_mm": _round(high, 1),
                "width_mm": _round(gap, 1),
                "length_mm": _round(length, 1),
                "assumed_height_mm": _round(height, 1),
                "volume_m3": _round(volume),
                "bbox_mm": [_round(extent[0], 1), _round(extent[1], 1),
                            _round(extent[2], 1), _round(extent[3], 1)],
                "evidence": "两条未覆盖平行梁线，间距取最近的梁宽区间配对，轴向重叠",
                "review_required": True,
            })
            used.add(index)
            used.add(other_index)

    for index, row in enumerate(segments):
        if index in used:
            continue
        candidates.append({
            "status": "uncovered-single-line",
            "handles": [row["handle"]],
            "orientation": row["orientation"],
            "axis_mm": _round(
                row["start"][1] if row["orientation"] == "H" else row["start"][0], 1),
            "start_mm": _round(
                min(row["start"][0], row["end"][0])
                if row["orientation"] == "H" else
                min(row["start"][1], row["end"][1]), 1),
            "end_mm": _round(
                max(row["start"][0], row["end"][0])
                if row["orientation"] == "H" else
                max(row["start"][1], row["end"][1]), 1),
            "width_mm": 0.0,
            "length_mm": _round(row["length_mm"], 1),
            "assumed_height_mm": 0.0,
            "volume_m3": 0.0,
            "bbox_mm": [_round(min(row["start"][0], row["end"][0]), 1),
                        _round(min(row["start"][1], row["end"][1]), 1),
                        _round(max(row["start"][0], row["end"][0]), 1),
                        _round(max(row["start"][1], row["end"][1]), 1)],
            "evidence": "只有一条未覆盖梁线，无法确定梁宽，不计体积",
            "review_required": True,
        })
    candidates.sort(key=lambda row: (-_number(row["volume_m3"]),
                                     row["bbox_mm"][0], row["bbox_mm"][1]))
    return candidates


def build_audit(
        raw_entities: list[dict[str, Any]],
        model: dict[str, Any],
        options: dict[str, float] | None = None,
        ) -> dict[str, Any]:
    options = dict(options or {})
    options.setdefault("cover_tolerance_mm", 60.0)
    options.setdefault("pair_min_width_mm", 120.0)
    options.setdefault("pair_max_width_mm", 400.0)
    options.setdefault("pair_min_overlap_mm", 300.0)
    options.setdefault("default_height_mm", 500.0)
    options.setdefault("frame_margin_mm", 0.0)
    options.setdefault("residual_gap_m3", -1.0)
    options.setdefault("duplicate_offset_tolerance_mm", 60.0)
    options.setdefault("plan_margin_mm", 0.0)
    options.setdefault("min_stub_length_mm", 100.0)
    options.setdefault("unexplained_tolerance_m3", 0.05)
    layers = set(BEAM_LAYERS) | set(COUPLING_LAYERS)
    if options.get("beam_layers"):
        layers = set(str(options["beam_layers"]).split(",")) | set(COUPLING_LAYERS)
    segments = _normalize_entities(raw_entities, layers)
    registry = model.get("run_registry") or {}
    faces = _run_faces(model)
    mirror_axes = []
    for entry in registry.get("mirror_axes") or []:
        if isinstance(entry, dict):
            mirror_axes.append(_number(entry.get("axis_mm")))
        else:
            mirror_axes.append(_number(entry))
    frame = [_number(value) for value in (registry.get("bbox") or [])]
    if len(frame) != 4:
        xs = [value for row in segments for value in (row["start"][0], row["end"][0])]
        ys = [value for row in segments for value in (row["start"][1], row["end"][1])]
        frame = [min(xs), min(ys), max(xs), max(ys)] if xs else [0, 0, 0, 0]
    heights: dict[str, float] = {}
    for run in registry.get("runs") or []:
        width = _round(_number(run.get("paired_width_mm"), 200.0), 0)
        height = _number(run.get("section_h_mm"))
        if width and height:
            heights.setdefault(str(int(width)), height)
    for row in segments:
        center = (
            (row["start"][0] + row["end"][0]) / 2.0,
            (row["start"][1] + row["end"][1]) / 2.0,
        )
        row["in_frame"] = _inside_bbox(frame, center, options["frame_margin_mm"])
        row["is_coupling"] = row["layer"] in COUPLING_LAYERS
        covered_len, gaps, run_ids = _uncovered_intervals(
            row, faces, options["cover_tolerance_mm"])
        row["covered_length_mm"] = covered_len
        row["run_ids"] = run_ids
        row["gaps"] = gaps
    plan_bbox = _model_plan_bbox(model)
    # 先按区间取出每条梁线上没被实例边线吃到的线段，再按视图归属分桶。
    uncovered: list[dict[str, Any]] = []
    stubs_in_frame: list[dict[str, Any]] = []
    stubs_outside: list[dict[str, Any]] = []
    coupling_uncovered: list[dict[str, Any]] = []
    coupling_outside: list[dict[str, Any]] = []
    covered_line_count = 0
    partial_covered_count = 0
    for row in segments:
        if not row["gaps"]:
            covered_line_count += 1
            continue
        if row["covered_length_mm"] > 1.0:
            partial_covered_count += 1
        if row["is_coupling"]:
            (coupling_uncovered if row["in_frame"] else coupling_outside).append(row)
            continue
        if row["in_frame"]:
            uncovered.append(row)
        for gap in row["gaps"]:
            if gap[1] - gap[0] < options["min_stub_length_mm"]:
                continue
            stub = _stub_segment(row, gap, "pending")
            (stubs_in_frame if row["in_frame"] else stubs_outside).append(stub)
    # 提取窗口外的线段做平移孪生判定：整视图重复绘制的只能算证据，不算漏量。
    votes: dict[float, int] = defaultdict(int)
    stub_offsets: dict[int, float] = {}
    for index, stub in enumerate(stubs_outside):
        offset = _translation_offset(
            stub, faces, options["cover_tolerance_mm"])
        if offset is None:
            continue
        stub_offsets[index] = offset
        votes[round(offset / 50.0) * 50] += 1
    dominant_offset, dominant_count = (
        max(votes.items(), key=lambda item: (item[1], -abs(item[0])))
        if votes else (None, 0))
    candidates_in_frame = list(stubs_in_frame)
    candidates_window_out: list[dict[str, Any]] = []
    candidates_beyond_plan: list[dict[str, Any]] = []
    twin_stubs: list[dict[str, Any]] = []
    mirrored_stubs: list[dict[str, Any]] = []
    for index, stub in enumerate(stubs_outside):
        offset = stub_offsets.get(index)
        center = ((stub["start"][0] + stub["end"][0]) / 2.0,
                  (stub["start"][1] + stub["end"][1]) / 2.0)
        axis = _mirrored_pair_offset(
            stub, faces, mirror_axes, options["cover_tolerance_mm"])
        if (dominant_offset is not None and offset is not None
                and abs(offset - dominant_offset)
                <= options["duplicate_offset_tolerance_mm"]):
            stub = dict(stub)
            stub["offset_mm"] = _round(offset, 1)
            stub["beyond_plan"] = not _inside_bbox(
                plan_bbox, center, options["plan_margin_mm"])
            twin_stubs.append(stub)
        elif axis is not None:
            stub = dict(stub)
            stub["mirror_axis_mm"] = _round(axis, 1)
            stub["beyond_plan"] = not _inside_bbox(
                plan_bbox, center, options["plan_margin_mm"])
            mirrored_stubs.append(stub)
        elif _inside_bbox(plan_bbox, center, options["plan_margin_mm"]):
            candidates_window_out.append(stub)
        else:
            candidates_beyond_plan.append(stub)
    covered = [row for row in segments if not row["gaps"]]
    outside: list[dict[str, Any]] = []
    mirrored_candidates = _pair_candidates(mirrored_stubs, options, heights)
    for row in mirrored_candidates:
        row["view_zone"] = "mirror-pair-outside-window"
        row["evidence"] += NOTE_MIRROR
    translated_candidates = _pair_candidates(twin_stubs, options, heights)
    for row in translated_candidates:
        row["view_zone"] = "translated-duplicate-view"
        row["evidence"] += NOTE_TRANSLATED
    candidates = _pair_candidates(candidates_in_frame, options, heights)
    for row in candidates:
        row["view_zone"] = "inside-extraction-window"
    window_out_candidates = _pair_candidates(
        candidates_window_out, options, heights)
    for row in window_out_candidates:
        row["view_zone"] = "outside-window-inside-plan-envelope"
        row["evidence"] += "（在本层板面域内、但在梁提取窗口外，属可回图的漏量候选）"
    beyond_candidates = _pair_candidates(
        candidates_beyond_plan, options, heights)
    for row in beyond_candidates:
        row["view_zone"] = "beyond-plan-envelope"
        row["evidence"] += "（落在本层板面域外，判为相邻视图，不得并入本层量）"
    all_candidates = (candidates + window_out_candidates + beyond_candidates
                      + mirrored_candidates + translated_candidates)
    mirrored_volume = sum(_number(row["volume_m3"]) for row in mirrored_candidates)
    translated_volume = sum(_number(row["volume_m3"])
                            for row in translated_candidates)
    candidate_volume = sum(_number(row["volume_m3"]) for row in all_candidates)
    in_frame_volume = sum(_number(row["volume_m3"]) for row in candidates)
    window_out_volume = sum(_number(row["volume_m3"]) for row in window_out_candidates)
    beyond_volume = sum(_number(row["volume_m3"]) for row in beyond_candidates)
    explanatory_volume = in_frame_volume + window_out_volume
    candidate_length = sum(_number(row["length_mm"]) for row in all_candidates
                           if row["status"] == "uncovered-beam-candidate")
    total_length = sum(_number(row["length_mm"]) for row in segments)
    beam_rows = [row for row in segments if not row["is_coupling"]]
    beam_length = sum(_number(row["length_mm"]) for row in beam_rows)
    covered_beam = [row for row in covered if not row["is_coupling"]]
    in_frame_beam = [row for row in beam_rows if row["in_frame"]]

    def _covered(rows):
        return sum(min(_number(row["length_mm"]), _number(row["covered_length_mm"]))
                   for row in rows)

    def _gaps(rows):
        return sum(sum(end - start for start, end in row["gaps"]) for row in rows)

    in_frame_length = sum(_number(row["length_mm"]) for row in in_frame_beam)
    in_frame_covered_length = _covered(in_frame_beam)
    in_frame_gap_length = _gaps(in_frame_beam)
    residual = _number(options.get("residual_gap_m3"), -1.0)
    usable_volume = in_frame_volume
    summary = {
        "segment_count": len(segments),
        "beam_segment_count": len(beam_rows),
        "beam_segment_length_mm": _round(beam_length, 1),
        "segment_length_mm": _round(total_length, 1),
        "covered_segment_count": len([
            row for row in covered_beam if not row["gaps"]]),
        "covered_length_mm": _round(_covered(beam_rows), 1),
        "partial_covered_segment_count": partial_covered_count,
        "coverage_length_ratio": _round(
            _covered(beam_rows) / beam_length, 6) if beam_length else 0.0,
        "in_frame_segment_count": len(in_frame_beam),
        "in_frame_length_mm": _round(in_frame_length, 1),
        "in_frame_covered_length_mm": _round(in_frame_covered_length, 1),
        "in_frame_coverage_ratio": _round(
            in_frame_covered_length / in_frame_length, 6)
        if in_frame_length else 0.0,
        "uncovered_in_frame_line_count": len(uncovered),
        "uncovered_in_frame_count": len(stubs_in_frame),
        "uncovered_in_frame_length_mm": _round(
            sum(_number(row["length_mm"]) for row in stubs_in_frame), 1),
        "in_frame_gap_length_mm": _round(in_frame_gap_length, 1),
        "outside_frame_count": len(candidates_window_out) + len(candidates_beyond_plan),
        "outside_frame_length_mm": _round(sum(
            _number(row["length_mm"])
            for row in candidates_window_out + candidates_beyond_plan), 1),
        "mirrored_line_count": len(mirrored_stubs),
        "mirrored_length_mm": _round(
            sum(_number(row["length_mm"]) for row in mirrored_stubs), 1),
        "mirror_axis_count": len(mirror_axes),
        "mirrored_beyond_plan_count": len(
            [row for row in mirrored_stubs if row.get("beyond_plan")]),
        "duplicate_view_beyond_plan_count": len(
            [row for row in twin_stubs if row.get("beyond_plan")]),
        "duplicate_view_line_count": len(twin_stubs),
        "duplicate_view_length_mm": _round(
            sum(_number(row["length_mm"]) for row in twin_stubs), 1),
        "duplicate_view_offset_mm": _round(dominant_offset, 1)
        if dominant_offset is not None else None,
        "duplicate_view_twin_line_count": dominant_count,
        "candidate_beam_in_frame_count": len([
            row for row in candidates
            if row["status"] == "uncovered-beam-candidate"]),
        "candidate_beam_window_out_count": len([
            row for row in window_out_candidates
            if row["status"] == "uncovered-beam-candidate"]),
        "candidate_beam_beyond_plan_count": len([
            row for row in beyond_candidates
            if row["status"] == "uncovered-beam-candidate"]),
        "candidate_volume_in_frame_m3": _round(in_frame_volume),
        "candidate_volume_window_out_m3": _round(window_out_volume),
        "candidate_volume_beyond_plan_m3": _round(beyond_volume),
        "candidate_volume_explanatory_m3": _round(explanatory_volume),
        "candidate_volume_mirror_pair_m3": _round(mirrored_volume),
        "candidate_volume_translated_view_m3": _round(translated_volume),
        "mirror_pair_candidate_count": len([
            row for row in mirrored_candidates
            if row["status"] == "uncovered-beam-candidate"]),
        "translated_view_candidate_count": len([
            row for row in translated_candidates
            if row["status"] == "uncovered-beam-candidate"]),
        "plan_bbox_mm": [_round(value, 1) for value in plan_bbox],
        "window_out_stub_count": len(candidates_window_out),
        "beyond_plan_stub_count": len(candidates_beyond_plan),
        "coupling_segment_count": len(segments) - len(beam_rows),
        "coupling_uncovered_count": len(coupling_uncovered),
        "coupling_uncovered_length_mm": _round(_gaps(coupling_uncovered), 1),
        "coupling_outside_frame_count": len(coupling_outside),
        "coupling_outside_frame_length_mm": _round(_gaps(coupling_outside), 1),
        "candidate_beam_count": len([
            row for row in all_candidates
            if row["status"] == "uncovered-beam-candidate"]),
        "candidate_single_line_count": len([
            row for row in all_candidates
            if row["status"] == "uncovered-single-line"]),
        "candidate_length_mm": _round(candidate_length, 1),
        "candidate_volume_m3": _round(candidate_volume),
        "review_required_count": len(all_candidates),
        "residual_gap_m3": _round(residual),
        "residual_covered_by_candidates_m3": (
            _round(min(usable_volume, residual)) if residual >= 0 else None),
        "explanatory_candidate_volume_m3": _round(explanatory_volume),
        "residual_still_unexplained_m3": (
            _round(max(0.0, residual - usable_volume)) if residual >= 0 else None),
        "residual_still_unexplained_with_window_out_m3": (
            _round(max(0.0, residual - explanatory_volume))
            if residual >= 0 else None),
        "mirror_pair_overshoot_m3": (
            _round(max(0.0, mirrored_volume - residual))
            if residual >= 0 else None),
        "mirror_pair_countable": _mirror_pair_countable(
            mirrored_volume, residual,
            _number(options.get("unexplained_tolerance_m3", 0.05), 0.05)),
        "residual_if_mirror_pair_added_m3": (
            _round(max(0.0, residual - explanatory_volume - mirrored_volume))
            if residual >= 0 else None),
        "unexplained_tolerance_m3": _round(
            options.get("unexplained_tolerance_m3", 0.05), 4),
        "residual_within_tolerance": bool(
            residual >= 0
            and max(0.0, residual - usable_volume)
            <= _number(options.get("unexplained_tolerance_m3", 0.05), 0.05)),
        "run_count": len(registry.get("runs") or []),
        "frame_bbox_mm": [_round(value, 1) for value in frame],
    }
    # 门槛只看图框内主梁线是否全部被实例吃到；连梁走独立台账，不并入本门槛。
    summary["coverage_closed"] = bool(summary["uncovered_in_frame_count"] == 0)
    return {
        "schema": SCHEMA,
        "floor": _text((model.get("floor") or {}).get("label")),
        "layers": sorted(layers),
        "options": {key: _round(value, 3) for key, value in sorted(options.items())
                    if key != "beam_layers"},
        "summary": summary,
        "candidates": all_candidates,
        "mirrored_lines": [
            {
                "handle": row["handle"],
                "layer": row["layer"],
                "orientation": row["orientation"],
                "length_mm": _round(row["length_mm"], 1),
                "mirror_axis_mm": row.get("mirror_axis_mm"),
                "beyond_plan_bbox": bool(row.get("beyond_plan")),
                "bbox_mm": [_round(min(row["start"][0], row["end"][0]), 1),
                            _round(min(row["start"][1], row["end"][1]), 1),
                            _round(max(row["start"][0], row["end"][0]), 1),
                            _round(max(row["start"][1], row["end"][1]), 1)],
            }
            for row in mirrored_stubs],
        "duplicate_view_lines": [
            {
                "handle": row["handle"],
                "layer": row["layer"],
                "orientation": row["orientation"],
                "length_mm": _round(row["length_mm"], 1),
                "offset_mm": row.get("offset_mm"),
                "beyond_plan_bbox": bool(row.get("beyond_plan")),
                "bbox_mm": [_round(min(row["start"][0], row["end"][0]), 1),
                            _round(min(row["start"][1], row["end"][1]), 1),
                            _round(max(row["start"][0], row["end"][0]), 1),
                            _round(max(row["start"][1], row["end"][1]), 1)],
            }
            for row in twin_stubs],
        "uncovered_segments": [
            {
                "handle": row["handle"],
                "layer": row["layer"],
                "orientation": row["orientation"],
                "length_mm": _round(row["length_mm"], 1),
                "bbox_mm": [_round(min(row["start"][0], row["end"][0]), 1),
                            _round(min(row["start"][1], row["end"][1]), 1),
                            _round(max(row["start"][0], row["end"][0]), 1),
                            _round(max(row["start"][1], row["end"][1]), 1)],
            }
            for row in uncovered],
        "formal_ready": False,
        "applied_to_formal_quantity": False,
    }


def csv_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows = [[
        "类别", "句柄", "状态", "视图归属", "方向", "轴位置mm", "起点mm", "终点mm",
        "梁宽mm", "长mm", "假定高mm", "体积m3", "证据",
    ]]
    for row in result["candidates"]:
        rows.append([
            "候选梁" if row["status"] == "uncovered-beam-candidate" else "单线",
            "+".join(row["handles"]), row["status"],
            row.get("view_zone") or "", row["orientation"],
            row["axis_mm"], row["start_mm"], row["end_mm"],
            row["width_mm"], row["length_mm"], row["assumed_height_mm"],
            row["volume_m3"], row["evidence"],
        ])
    return rows


def _md(value: Any) -> str:
    return "-" if value is None else _text(value)


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# 梁图层覆盖审计",
        "",
        f"- Schema：`{result['schema']}`，来源图框 "
        f"`{summary['frame_bbox_mm']}`，实例 {summary['run_count']} 条。",
        f"- 本图框内梁线 {summary['in_frame_segment_count']} 条"
        f" / {summary['in_frame_length_mm']:.1f} mm，"
        f"被算量实例边线覆盖 {summary['in_frame_covered_length_mm']:.1f} mm，"
        f"**图框内覆盖率 {summary['in_frame_coverage_ratio'] * 100:.2f}%**。",
        f"- 全图口径（含相邻图框）梁线 {summary['beam_segment_count']} 条"
        f" / {summary['beam_segment_length_mm']:.1f} mm，"
        f"覆盖率 {summary['coverage_length_ratio'] * 100:.2f}%。",
        f"- 提取窗口内未被吃到的线段 {summary['uncovered_in_frame_count']} 段、"
        f"{summary['uncovered_in_frame_length_mm']:.1f} mm，来自 "
        f"{summary['uncovered_in_frame_line_count']} 条梁线"
        f"（含 {summary['partial_covered_segment_count']} 条部分覆盖）。",
        ("- 提取窗口外的图线全部有视图归属，不计本层漏量："
         f"{summary['mirrored_line_count']} 条（{summary['mirrored_length_mm']:.1f} mm、"
         f"配对估算 {summary['candidate_volume_mirror_pair_m3']:.4f} m3）关于 "
         f"{summary['mirror_axis_count']} 条镜像轴与已提取实例对称，判为对称视图绘制；"
         f"{summary['duplicate_view_line_count']} 条"
         f"（{summary['duplicate_view_length_mm']:.1f} mm、"
         f"{summary['candidate_volume_translated_view_m3']:.4f} m3）与已提取实例构成统一偏移 "
         f"{_md(summary['duplicate_view_offset_mm'])} mm 的平移孪生，判为整视图重复绘制。"
         f"剩余 {summary['outside_frame_count']} 段无孪生（其中板面域内 "
         f"{summary['window_out_stub_count']} 段、板面域外 "
         f"{summary['beyond_plan_stub_count']} 段）。"),
        (f"- 镜像对称线只能算对称视图证据：其配对体量比本层缺口多 "
         f"{_md(summary['mirror_pair_overshoot_m3'])} m3，计入即超出广联达参考量，"
         f"因此不并入漏量；扩窗重跑源 DWG 已核验新增实体为 0，"
         f"不存在被窗口裁掉的梁线。"),
        (f"- 交叉验证：{summary['mirrored_beyond_plan_count']} 条镜像线、"
         f"{summary['duplicate_view_beyond_plan_count']} 条平移线落在本层板面域 "
         f"{summary['plan_bbox_mm']} 之外，位置证据与对称、平移证据一致。"),
        f"- 未覆盖图线配对出 {summary['candidate_beam_count']} 条候选梁、"
        f"{summary['candidate_length_mm']:.1f} mm，"
        f"按截面估算 {summary['candidate_volume_m3']:.4f} m3；"
        f"另有 {summary['candidate_single_line_count']} 条单线无法定宽。",
        f"- 连梁图层 {summary['coupling_segment_count']} 条：图框内未覆盖 "
        f"{summary['coupling_uncovered_count']} 条、"
        f"{summary['coupling_uncovered_length_mm']:.1f} mm，图框外 "
        f"{summary['coupling_outside_frame_count']} 条、"
        f"{summary['coupling_outside_frame_length_mm']:.1f} mm；"
        "连梁体积走独立台账，不计入本门槛。",
    ]
    if _number(summary.get("residual_gap_m3"), -1.0) >= 0:
        lines.append(
            f"- 与梁净缺口对照：缺口 {summary['residual_gap_m3']:.4f} m3，"
            f"窗口内配对候选最多解释 "
            f"{summary['residual_covered_by_candidates_m3']:.4f} m3，"
            f"仍无法解释 {summary['residual_still_unexplained_m3']:.4f} m3。"
            f"剩余缺口的来源不在图线覆盖，而在截面高度与编号归属，"
            f"须回到梁实例台账逐编号核对，不得用窗口外图线凑量。")
    lines += [
        "- 覆盖判定只说明图线有没有被实例吃到，不证明编号归属正确。",
        "",
        "## 未覆盖候选（按未覆盖线段配对）",
        "",
        "| 状态 | 句柄 | 方向 | 梁宽mm | 长mm | 假定高mm | 体积m3 | 位置 |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]
    for row in result["candidates"]:
        lines.append(
            f"| {row['status']} | {'+'.join(row['handles'])} | "
            f"{row['orientation']} | {row['width_mm']:.0f} | "
            f"{row['length_mm']:.0f} | {row['assumed_height_mm']:.0f} | "
            f"{row['volume_m3']:.4f} | {row['bbox_mm']} |")
    if not result["candidates"]:
        lines.append("| 无 | - | - | 0 | 0 | 0 | 0.0000 | - |")
    lines += [
        "",
        "## 结论",
        "",
        "- 候选梁只作为回图检索目标，未经人工确认编号与截面前不计入任何量。",
        "- 图框外图线属相邻图框，不得并入本层。",
        "- 覆盖审计不改变混凝土候选合计，`formal_ready=false`。",
    ]
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="审计梁图层图线是否已被算量实例覆盖")
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--geometry-dxf", default=None)
    parser.add_argument("--entities-json", default=None)
    parser.add_argument("--beam-layers", default=",".join(BEAM_LAYERS))
    parser.add_argument("--cover-tolerance-mm", type=float, default=60.0)
    parser.add_argument("--pair-min-width-mm", type=float, default=120.0)
    parser.add_argument("--pair-max-width-mm", type=float, default=400.0)
    parser.add_argument("--pair-min-overlap-mm", type=float, default=300.0)
    parser.add_argument("--default-height-mm", type=float, default=500.0)
    parser.add_argument("--frame-margin-mm", type=float, default=0.0)
    parser.add_argument("--residual-gap-m3", type=float, default=None)
    parser.add_argument("--unexplained-tolerance-m3", type=float, default=0.05)
    parser.add_argument("--duplicate-offset-tolerance-mm", type=float, default=60.0)
    parser.add_argument("--plan-margin-mm", type=float, default=0.0)
    parser.add_argument("--min-stub-length-mm", type=float, default=100.0)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    model_path = Path(args.model_json)
    if not model_path.exists():
        parser.error(f"缺少结构模型 JSON：{model_path}")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    layers = set(
        layer.strip() for layer in args.beam_layers.split(",") if layer.strip())
    read_layers = layers | set(COUPLING_LAYERS)
    if args.geometry_dxf:
        dxf_path = Path(args.geometry_dxf)
        if not dxf_path.exists():
            parser.error(f"缺少几何 DXF：{dxf_path}")
        raw = _read_entities(dxf_path, read_layers)
    elif args.entities_json:
        payload = json.loads(
            Path(args.entities_json).read_text(encoding="utf-8"))
        raw = payload.get("entities") if isinstance(payload, dict) else payload
    else:
        parser.error("必须提供 --geometry-dxf 或 --entities-json")
    options = {
        "cover_tolerance_mm": args.cover_tolerance_mm,
        "pair_min_width_mm": args.pair_min_width_mm,
        "pair_max_width_mm": args.pair_max_width_mm,
        "pair_min_overlap_mm": args.pair_min_overlap_mm,
        "default_height_mm": args.default_height_mm,
        "frame_margin_mm": args.frame_margin_mm,
        "residual_gap_m3": (
            args.residual_gap_m3 if args.residual_gap_m3 is not None else -1.0),
        "unexplained_tolerance_m3": args.unexplained_tolerance_m3,
        "duplicate_offset_tolerance_mm": args.duplicate_offset_tolerance_mm,
        "plan_margin_mm": args.plan_margin_mm,
        "min_stub_length_mm": args.min_stub_length_mm,
        "beam_layers": args.beam_layers,
    }
    result = build_audit(list(raw), model, options)
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
        "coverage_length_ratio": summary["coverage_length_ratio"],
        "candidate_volume_mirror_pair_m3": summary["candidate_volume_mirror_pair_m3"],
        "candidate_volume_translated_view_m3":
            summary["candidate_volume_translated_view_m3"],
        "mirror_pair_overshoot_m3": summary["mirror_pair_overshoot_m3"],
        "mirror_pair_countable": summary["mirror_pair_countable"],
        "mirrored_line_count": summary["mirrored_line_count"],
        "in_frame_coverage_ratio": summary["in_frame_coverage_ratio"],
        "in_frame_length_mm": summary["in_frame_length_mm"],
        "uncovered_in_frame_length_mm": summary["uncovered_in_frame_length_mm"],
        "duplicate_view_line_count": summary["duplicate_view_line_count"],
        "duplicate_view_offset_mm": summary["duplicate_view_offset_mm"],
        "candidate_volume_in_frame_m3": summary["candidate_volume_in_frame_m3"],
        "candidate_volume_window_out_m3": summary["candidate_volume_window_out_m3"],
        "candidate_volume_beyond_plan_m3": summary["candidate_volume_beyond_plan_m3"],
        "uncovered_in_frame_count": summary["uncovered_in_frame_count"],
        "outside_frame_count": summary["outside_frame_count"],
        "candidate_beam_count": summary["candidate_beam_count"],
        "candidate_volume_m3": summary["candidate_volume_m3"],
        "residual_still_unexplained_m3": summary["residual_still_unexplained_m3"],
        "outputs": [str(json_path), str(csv_path), str(md_path), str(checksums)],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
