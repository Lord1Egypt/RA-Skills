#!/usr/bin/env python3
"""审计 CAD 构件矩形之间的重复计量区域。"""




from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

from cad_common import round_number as _round  # noqa: E402,F401

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


SCHEMA = "cad-member-intersection-audit/v0.3"


def _number(value: Any) -> float:
    return float(value or 0.0)

def _mm2_to_m2(value: float) -> float:
    return value / 1_000_000.0


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rect(
        member_id: str,
        kind: str,
        code: str,
        orientation: str,
        x0: float,
        x1: float,
        y0: float,
        y1: float,
        height_mm: float,
        source: str,
        evidence: str = "direct") -> dict[str, Any]:
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    return {
        "id": member_id,
        "kind": kind,
        "code": code,
        "orientation": orientation,
        "x0_mm": _round(x0, 1),
        "x1_mm": _round(x1, 1),
        "y0_mm": _round(y0, 1),
        "y1_mm": _round(y1, 1),
        "height_mm": _round(height_mm, 1),
        "area_m2": _round(_mm2_to_m2(max(0.0, x1 - x0) * max(0.0, y1 - y0))),
        "volume_m3": _round(
            _mm2_to_m2(max(0.0, x1 - x0) * max(0.0, y1 - y0))
            * height_mm / 1000.0),
        "source": source,
        "evidence": evidence,
    }


def _axis_rect(
        member_id: str,
        kind: str,
        code: str,
        orientation: str,
        axis_mm: float,
        start_mm: float,
        end_mm: float,
        width_mm: float,
        height_mm: float,
        source: str,
        evidence: str = "direct") -> dict[str, Any]:
    half = width_mm / 2.0
    if orientation == "H":
        return _rect(member_id, kind, code, "H",
                     start_mm, end_mm, axis_mm - half, axis_mm + half,
                     height_mm, source, evidence)
    return _rect(member_id, kind, code, "V",
                 axis_mm - half, axis_mm + half, start_mm, end_mm,
                 height_mm, source, evidence)


def _center_rect(
        member_id: str,
        kind: str,
        code: str,
        orientation: str,
        center_mm: list[float],
        length_mm: float,
        width_mm: float,
        height_mm: float,
        source: str,
        evidence: str = "direct") -> dict[str, Any]:
    cx, cy = center_mm
    half_length = length_mm / 2.0
    half_width = width_mm / 2.0
    if orientation == "H":
        return _rect(member_id, kind, code, "H",
                     cx - half_length, cx + half_length,
                     cy - half_width, cy + half_width,
                     height_mm, source, evidence)
    return _rect(member_id, kind, code, "V",
                 cx - half_width, cx + half_width,
                 cy - half_length, cy + half_length,
                 height_mm, source, evidence)


def _build_rectangles(
        model: dict[str, Any],
        phase20: dict[str, Any],
        story_height_mm: float,
        coupling_height_mm: float) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rectangles: list[dict[str, Any]] = []
    skipped: dict[str, int] = defaultdict(int)

    for run in model.get("run_registry", {}).get("runs") or []:
        width = _number(run.get("section_b_mm") or run.get("paired_width_mm"))
        height = _number(run.get("section_h_mm"))
        if width <= 0 or height <= 0:
            skipped["beam_missing_section"] += 1
            continue
        rectangles.append(_axis_rect(
            str(run.get("id") or f"BR{len(rectangles) + 1:04d}"),
            "beam", str(run.get("matched_code") or ""),
            str(run.get("orientation") or ""),
            _number(run.get("axis_mm")), _number(run.get("start_mm")),
            _number(run.get("end_mm")), width, height,
            "model.run_registry",
            str(run.get("section_status") or "")))

    members = model.get("members", {})
    for index, column in enumerate(members.get("columns") or []):
        height = _number(column.get("height_mm")) or story_height_mm
        label = str(column.get("label") or f"COL{index + 1}")
        rectangles.append(_rect(
            f"C{index + 1:04d}", "column", label, "area",
            _number(column.get("x0")), _number(column.get("x1")),
            _number(column.get("y0")), _number(column.get("y1")),
            height, "model.members.columns",
            str(column.get("label_status") or "")))

    for index, edge in enumerate(members.get("edge_members") or []):
        bbox = edge.get("bbox") or []
        if len(bbox) != 4:
            skipped["edge_missing_bbox"] += 1
            continue
        height = _number(edge.get("height_mm")) or story_height_mm
        rectangles.append(_rect(
            f"E{index + 1:04d}", "edge-member", str(edge.get("label") or ""),
            "area", bbox[0], bbox[2], bbox[1], bbox[3],
            height, "model.members.edge_members",
            str(edge.get("label_status") or "")))

    for index, wall in enumerate(members.get("walls") or []):
        orientation = str(wall.get("orientation") or "")
        width = _number(wall.get("width_mm"))
        if orientation not in ("H", "V") or width <= 0:
            skipped["wall_missing_geometry"] += 1
            continue
        rectangles.append(_axis_rect(
            f"W{index + 1:04d}", "wall", "", orientation,
            _number(wall.get("center")), _number(wall.get("start")),
            _number(wall.get("end")), width, story_height_mm,
            "model.members.walls", "strip"))

    for instance in phase20.get("coupling_beam_instances") or []:
        center = instance.get("model_center_mm") or []
        length = _number(instance.get("nominal_length_mm"))
        width = _number(instance.get("thickness_mm"))
        if len(center) != 2 or length <= 0 or width <= 0:
            skipped["coupling_missing_geometry"] += 1
            continue
        rectangles.append(_center_rect(
            str(instance.get("id") or f"CB{len(rectangles) + 1:04d}"),
            "coupling-beam", str(instance.get("code") or ""),
            str(instance.get("orientation") or ""), center,
            length, width, coupling_height_mm,
            "phase20.coupling_beam_instances",
            "reference-height"))

    counts = defaultdict(int)
    for rectangle in rectangles:
        counts[rectangle["kind"]] += 1
    return rectangles, {
        "rectangle_counts": dict(sorted(counts.items())),
        "skipped": dict(sorted(skipped.items())),
    }


def _classify_pair(left: dict[str, Any], right: dict[str, Any]) -> tuple[str, str, str]:
    kinds = {left["kind"], right["kind"]}
    beam_kinds = {"beam", "coupling-beam"}
    vertical_kinds = {"column", "edge-member", "wall"}
    if kinds == {"beam"}:
        return "beam-beam", "larger-section", "potential"
    if kinds == {"beam", "coupling-beam"}:
        return "beam-coupling", "coupling-beam", "reference"
    if "coupling-beam" in kinds and kinds & vertical_kinds:
        return "coupling-vertical", "vertical", "reference"
    if "beam" in kinds and kinds & vertical_kinds:
        return "beam-vertical", "vertical", "potential"
    if kinds <= vertical_kinds:
        return "vertical-vertical", "audit-only", "audit"
    return "other", "audit-only", "audit"


def _overlap(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any] | None:
    width = min(left["x1_mm"], right["x1_mm"]) - max(left["x0_mm"], right["x0_mm"])
    height = min(left["y1_mm"], right["y1_mm"]) - max(left["y0_mm"], right["y0_mm"])
    if width <= 0 or height <= 0:
        return None
    area_m2 = _round(_mm2_to_m2(width * height))
    if area_m2 <= 0:
        return None
    pair_type, owner, confidence = _classify_pair(left, right)
    deduction_height = min(left["height_mm"], right["height_mm"])
    potential = _round(area_m2 * deduction_height / 1000.0)
    return {
        "pair_type": pair_type,
        "member_ids": [left["id"], right["id"]],
        "codes": [left["code"], right["code"]],
        "kinds": [left["kind"], right["kind"]],
        "overlap_bbox_mm": [
            _round(max(left["x0_mm"], right["x0_mm"]), 1),
            _round(max(left["y0_mm"], right["y0_mm"]), 1),
            _round(min(left["x1_mm"], right["x1_mm"]), 1),
            _round(min(left["y1_mm"], right["y1_mm"]), 1),
        ],
        "overlap_area_m2": area_m2,
        "deduction_height_mm": _round(deduction_height, 1),
        "potential_deduction_volume_m3": potential,
        "suggested_owner": owner,
        "confidence": confidence,
        "deduction_basis": (
            "重叠区取最小截面高度；墙柱按通高计量时从梁中扣除"
            if pair_type == "beam-vertical"
            else "相交节点只保留一次最小截面高度体积"
            if pair_type in ("beam-beam", "beam-coupling")
            else "同类竖向构件重叠仅暴露，不自动选择归属"
        ),
    }


def _unique_overlap_metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    """合并同坐标重叠格，避免三构件同点相交时重复累计。"""
    if not rows:
        return {
            "unique_overlap_cell_count": 0.0,
            "unique_overlap_area_m2": 0.0,
            "unique_potential_deduction_volume_m3": 0.0,
        }
    xs = sorted({
        value for row in rows
        for value in (row["overlap_bbox_mm"][0], row["overlap_bbox_mm"][2])
    })
    ys = sorted({
        value for row in rows
        for value in (row["overlap_bbox_mm"][1], row["overlap_bbox_mm"][3])
    })
    unique_area = 0.0
    unique_volume = 0.0
    cell_count = 0
    for x0, x1 in zip(xs, xs[1:]):
        if x1 <= x0:
            continue
        for y0, y1 in zip(ys, ys[1:]):
            if y1 <= y0:
                continue
            covering = [
                row for row in rows
                if (row["overlap_bbox_mm"][0] <= x0
                    and row["overlap_bbox_mm"][2] >= x1
                    and row["overlap_bbox_mm"][1] <= y0
                    and row["overlap_bbox_mm"][3] >= y1)
            ]
            if not covering:
                continue
            height_mm = max(
                _number(row["deduction_height_mm"]) for row in covering)
            area_m2 = _mm2_to_m2((x1 - x0) * (y1 - y0))
            unique_area += area_m2
            unique_volume += area_m2 * height_mm / 1000.0
            cell_count += 1
    return {
        "unique_overlap_cell_count": cell_count,
        "unique_overlap_area_m2": _round(unique_area),
        "unique_potential_deduction_volume_m3": _round(unique_volume),
    }


def _aggregate(overlaps: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in overlaps:
        groups[row["pair_type"]].append(row)
    result: dict[str, Any] = {}
    for pair_type, rows in sorted(groups.items()):
        by_code = defaultdict(float)
        for row in rows:
            for code in row["codes"]:
                if code:
                    by_code[code] += _number(row["potential_deduction_volume_m3"])
        top_codes = sorted(
            ((code, _round(volume)) for code, volume in by_code.items()),
            key=lambda item: (-item[1], item[0]),
        )[:10]
        unique = _unique_overlap_metrics(rows)
        pairwise_volume = sum(
            _number(row["potential_deduction_volume_m3"]) for row in rows)
        result[pair_type] = {
            "overlap_count": len(rows),
            "overlap_area_m2": _round(unique["unique_overlap_area_m2"]),
            "potential_deduction_volume_m3": _round(
                unique["unique_potential_deduction_volume_m3"]),
            "pairwise_potential_deduction_volume_m3": _round(pairwise_volume),
            "unique_overlap_cell_count": int(
                unique["unique_overlap_cell_count"]),
            "deduplication_overcount_m3": _round(
                pairwise_volume - _number(
                    unique["unique_potential_deduction_volume_m3"])),
            "top_codes": [{"code": code, "volume_m3": volume}
                          for code, volume in top_codes],
        }
    return result


def _unique_overlap_cells(
        rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """返回按坐标拆分后的唯一重叠格及其中的成对证据。"""
    if not rows:
        return []
    xs = sorted({
        value for row in rows
        for value in (row["overlap_bbox_mm"][0], row["overlap_bbox_mm"][2])
    })
    ys = sorted({
        value for row in rows
        for value in (row["overlap_bbox_mm"][1], row["overlap_bbox_mm"][3])
    })
    cells: list[dict[str, Any]] = []
    for x0, x1 in zip(xs, xs[1:]):
        if x1 <= x0:
            continue
        for y0, y1 in zip(ys, ys[1:]):
            if y1 <= y0:
                continue
            covering = [
                row for row in rows
                if (row["overlap_bbox_mm"][0] <= x0
                    and row["overlap_bbox_mm"][2] >= x1
                    and row["overlap_bbox_mm"][1] <= y0
                    and row["overlap_bbox_mm"][3] >= y1)
            ]
            if len({
                    member_id for row in covering
                    for member_id in row["member_ids"]}
            ) < 2:
                continue
            cells.append({
                "bbox_mm": [_round(x0, 1), _round(y0, 1),
                            _round(x1, 1), _round(y1, 1)],
                "area_m2": _round(_mm2_to_m2((x1 - x0) * (y1 - y0))),
                "pair_types": sorted({row["pair_type"] for row in covering}),
                "member_ids": sorted({
                    member_id for row in covering
                    for member_id in row["member_ids"]}),
                "codes": sorted({
                    code for row in covering for code in row["codes"] if code}),
            })
    return cells


def _calculate_net_quantities(
        rectangles: list[dict[str, Any]],
        overlaps: list[dict[str, Any]],
        located_total_m3: float) -> dict[str, Any]:
    members = {row["id"]: row for row in rectangles}
    cells = _unique_overlap_cells(overlaps)
    deductions: dict[str, float] = defaultdict(float)
    decisions: list[dict[str, Any]] = []
    unresolved_vertical_area = 0.0
    unresolved_vertical_volume = 0.0
    vertical_kinds = {"column", "edge-member", "wall"}
    beamlike_kinds = {"beam", "coupling-beam"}

    for cell in cells:
        cell_members = [members.get(mid) for mid in cell["member_ids"]]
        cell_members = [row for row in cell_members if row]
        verticals = [row for row in cell_members if row["kind"] in vertical_kinds]
        beamlike = [row for row in cell_members if row["kind"] in beamlike_kinds]
        owner_rule = ""
        deducted_members: list[dict[str, Any]] = []

        if verticals and beamlike:
            owner_rule = "vertical-member-retains-cell"
            deducted_members = beamlike
        elif len(beamlike) > 1:
            owner = max(
                beamlike,
                key=lambda row: (
                    _number(row["height_mm"]),
                    _number(row["volume_m3"]), row["id"]))
            owner_rule = "deepest-beam-retains-cell"
            deducted_members = [row for row in beamlike if row is not owner]
        elif len(verticals) > 1:
            owner_rule = "vertical-ownership-unresolved"
            height_mm = max(_number(row["height_mm"]) for row in verticals)
            unresolved_vertical_area += _number(cell["area_m2"])
            unresolved_vertical_volume += (
                _number(cell["area_m2"]) * height_mm / 1000.0)
        else:
            continue

        for member in deducted_members:
            deduction_m3 = _number(cell["area_m2"]) * _number(
                member["height_mm"]) / 1000.0
            if deduction_m3 <= 0:
                continue
            deductions[member["id"]] += deduction_m3

        decisions.append({
            "bbox_mm": cell["bbox_mm"],
            "area_m2": cell["area_m2"],
            "owner_rule": owner_rule,
            "pair_types": cell["pair_types"],
            "codes": cell["codes"],
            "deducted_member_ids": [
                row["id"] for row in deducted_members
                if _number(cell["area_m2"]) * _number(row["height_mm"]) > 0],
        })

    affected_by_id = defaultdict(list)
    for member_id, deduction in deductions.items():
        member = members[member_id]
        affected_by_id[member["kind"]].append({
            "id": member_id,
            "code": member["code"],
            "gross_volume_m3": _round(member["volume_m3"]),
            "intersection_deduction_m3": _round(deduction),
            "net_volume_m3": _round(
                _number(member["volume_m3"]) - deduction),
        })
    for kind in affected_by_id:
        affected_by_id[kind].sort(key=lambda row: (
            -_number(row["intersection_deduction_m3"]), row["code"]))

    gross_by_kind = defaultdict(float)
    deduction_by_kind = defaultdict(float)
    for member in rectangles:
        gross_by_kind[member["kind"]] += _number(member["volume_m3"])
        deduction_by_kind[member["kind"]] += _number(
            deductions.get(member["id"], 0.0))
    applied_deduction = _number(deduction_by_kind.get("beam"))
    reference_deduction = _number(deduction_by_kind["coupling-beam"])
    return {
        "status": "候选构件净量；仅按相交去重规则试算，未进入正式总量",
        "rule": "竖向构件保留节点格；同层多梁取最大截面高度者为所有者；竖向构件之间归属未定",
        "unique_overlap_cell_count": len(cells),
        "deduction_decision_count": len(decisions),
        "applied_deduction_m3": _round(applied_deduction),
        "reference_only_deduction_m3": _round(reference_deduction),
        "unresolved_vertical_overlap_area_m2": _round(
            unresolved_vertical_area),
        "unresolved_vertical_overlap_volume_m3": _round(
            unresolved_vertical_volume),
        "gross_by_kind": {
            kind: _round(value) for kind, value in sorted(gross_by_kind.items())},
        "deduction_by_kind": {
            kind: _round(value) for kind, value in sorted(deduction_by_kind.items())},
        "net_by_kind": {
            kind: _round(
                _number(gross_by_kind.get(kind)) - _number(
                    deduction_by_kind.get(kind)))
            for kind in sorted(set(gross_by_kind) | set(deduction_by_kind))},
        "top_affected_members": affected_by_id,
        "current_located_total_m3": _round(located_total_m3),
        "candidate_total_after_beam_deduction_m3": _round(
            _number(located_total_m3) - applied_deduction),
        "candidate_total_after_beam_and_coupling_deduction_m3": _round(
            _number(located_total_m3) - applied_deduction - reference_deduction),
        "decisions": sorted(decisions, key=lambda row: (
            -_number(row["area_m2"]), row["owner_rule"]))[:20],
        "applied_to_formal_quantity": False,
    }


def build_audit(
        model: dict[str, Any],
        phase20: dict[str, Any],
        ledger: dict[str, Any],
        story_height_mm: float,
        coupling_height_mm: float,
        area_tolerance_m2: float) -> dict[str, Any]:
    rectangles, diagnostics = _build_rectangles(
        model, phase20, story_height_mm, coupling_height_mm)
    overlaps = []
    for index, left in enumerate(rectangles):
        for right in rectangles[index + 1:]:
            row = _overlap(left, right)
            if row and _number(row["overlap_area_m2"]) > area_tolerance_m2:
                overlaps.append(row)
    overlaps.sort(key=lambda row: (
        -_number(row["potential_deduction_volume_m3"]),
        row["pair_type"],
        row["codes"][0],
        row["codes"][1],
    ))
    groups = _aggregate(overlaps)
    unique = _unique_overlap_metrics(overlaps)
    pairwise_volume = sum(
        _number(row["potential_deduction_volume_m3"]) for row in overlaps)
    beam_side = _number(groups.get("beam-vertical", {}).get(
        "potential_deduction_volume_m3")) + _number(groups.get(
            "beam-beam", {}).get("potential_deduction_volume_m3"))
    located_total = _number(
        (ledger.get("quantities") or {}).get("candidate_total_volume_m3"))
    if not located_total:
        located_total = _number((ledger.get("concrete_ledger") or {}).get(
            "located_total_m3"))
    net_quantity = _calculate_net_quantities(
        rectangles, overlaps, located_total)
    return {
        "schema": SCHEMA,
        "floor": model.get("floor") or {},
        "formal_ready": False,
        "status": (
            "构件矩形重叠审计与候选净量试算；未确认正式归属规则前不修改总量"
        ),
        "parameters": {
            "story_height_mm": story_height_mm,
            "coupling_height_mm": coupling_height_mm,
            "area_tolerance_m2": area_tolerance_m2,
        },
        "diagnostics": {
            **diagnostics,
            "comparison_pairs": len(rectangles) * max(0, len(rectangles) - 1) // 2,
        },
        "summary": {
            "overlap_count": len(overlaps),
            "overlap_area_m2": unique["unique_overlap_area_m2"],
            "potential_deduction_volume_m3": unique[
                "unique_potential_deduction_volume_m3"],
            "unique_overlap_cell_count": int(
                unique["unique_overlap_cell_count"]),
            "pairwise_potential_deduction_volume_m3": _round(pairwise_volume),
            "deduplication_overcount_m3": _round(
                pairwise_volume - _number(
                    unique["unique_potential_deduction_volume_m3"])),
            "beam_side_deduction_candidate_m3": _round(beam_side),
            "current_located_total_m3": _round(located_total),
            "unapplied_after_beam_side_deduction_m3": _round(
                located_total - beam_side),
            "groups": groups,
        },
        "net_quantity": net_quantity,
        "overlaps": overlaps,
        "closure": {
            "applied_to_formal_quantity": False,
            "reason": (
                "墙柱通高与梁端支座的先后关系尚未由设计/计算规则绑定；"
                "当前先作为重复计量证据，不自动改写候选合计"
            ),
            "next_gate": (
                "确定节点混凝土归属、梁与连梁顶底标高和竖向构件扣减边界后，"
                "再由同一扣减引擎生成构件净量"
            ),
        },
    }


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    groups = summary["groups"]
    lines = [
        f"# {result['schema']} 构件相交扣减审计",
        "",
        f"- 状态：{result['status']}",
        f"- 重叠对：`{summary['overlap_count']}`",
        f"- 去重后唯一重叠格：`{summary.get('unique_overlap_cell_count', 0)}`",
        f"- 重叠面积：`{summary['overlap_area_m2']} m2`",
        f"- 潜在重复体积：`{summary['potential_deduction_volume_m3']} m3`",
        f"- 成对原值：`{summary.get('pairwise_potential_deduction_volume_m3', 0)} m3`；"
        f"同点去重：`{summary.get('deduplication_overcount_m3', 0)} m3`",
        f"- 当前已定位候选合计：`{summary['current_located_total_m3']} m3`",
        "",
        "## 分组",
        "",
        "| 类型 | 重叠对 | 重叠面积 m2 | 潜在体积 m3 | 处理 |",
        "|---|---:|---:|---:|---|",
    ]
    labels = {
        "beam-vertical": "梁与墙柱",
        "beam-beam": "梁与梁",
        "beam-coupling": "梁与连梁",
        "coupling-vertical": "连梁与竖向构件",
        "vertical-vertical": "竖向构件之间",
        "other": "其他",
    }
    for key in ("beam-vertical", "beam-beam", "beam-coupling", "coupling-vertical", "vertical-vertical"):
        row = groups.get(key)
        if not row:
            continue
        handling = (
            "候选扣减，不自动改总量"
            if key in ("beam-vertical", "beam-beam")
            else "参考复核，不自动改总量"
        )
        lines.append(
            f"| {labels[key]} | {row['overlap_count']} | "
            f"{row['overlap_area_m2']} | "
            f"{row['potential_deduction_volume_m3']} | {handling} |"
        )
    lines.extend(["", "## 重点重叠", "",
                  "| 类型 | 构件 | 面积 m2 | 高度 mm | 潜在体积 m3 |",
                  "|---|---|---:|---:|---:|"])
    for row in result["overlaps"][:30]:
        lines.append(
            f"| {labels.get(row['pair_type'], row['pair_type'])} | "
            f"{row['codes'][0] or row['member_ids'][0]} / "
            f"{row['codes'][1] or row['member_ids'][1]} | "
            f"{row['overlap_area_m2']} | {row['deduction_height_mm']} | "
            f"{row['potential_deduction_volume_m3']} |"
        )
    lines.extend([
        "",
        "## 门槛",
        "",
        f"- 未应用：`{result['closure']['applied_to_formal_quantity']}`。",
        f"- 原因：{result['closure']['reason']}。",
        f"- 下一步：{result['closure']['next_gate']}。",
    ])
    net = result.get("net_quantity") or {}
    if net:
        lines += [
            "",
            "## 候选构件净量",
            "",
            f"- 规则：{net['rule']}。",
            f"- 梁净扣候选：`{net.get('applied_deduction_m3', 0)} m3`；"
            f"连梁参考净扣：`{net.get('reference_only_deduction_m3', 0)} m3`。",
            f"- 规则试算总量：`{net.get('candidate_total_after_beam_deduction_m3', 0)} m3`；"
            f"当前候选合计仍为 `{net.get('current_located_total_m3', 0)} m3`。",
            f"- 竖向构件未决面积：`{net.get('unresolved_vertical_overlap_area_m2', 0)} m2`。",
            "",
            "| 构件类型 | 毛量m3 | 相交扣减m3 | 净量m3 |",
            "|---|---:|---:|---:|",
        ]
        labels = {
            "beam": "梁",
            "column": "柱",
            "coupling-beam": "连梁",
            "edge-member": "边缘构件",
            "wall": "墙",
        }
        for kind in ("beam", "coupling-beam", "column", "edge-member", "wall"):
            lines.append(
                f"| {labels.get(kind, kind)} | "
                f"{net.get('gross_by_kind', {}).get(kind, 0)} | "
                f"{net.get('deduction_by_kind', {}).get(kind, 0)} | "
                f"{net.get('net_by_kind', {}).get(kind, 0)} |"
            )
    return "\n".join(lines) + "\n"


def csv_rows(result: dict[str, Any]) -> list[list[str]]:
    rows = [[
        "记录类型", "类型", "构件1", "构件2", "面积m2", "高度mm",
        "潜在体积m3", "建议归属", "置信度", "坐标范围",
    ]]
    for pair_type, group in sorted(result["summary"]["groups"].items()):
        rows.append([
            "汇总", pair_type, "", "", str(group["overlap_area_m2"]), "",
            str(group["potential_deduction_volume_m3"]), "", "",
            f"重叠{group['overlap_count']}对",
        ])
    for row in result["overlaps"]:
        rows.append([
            "明细", row["pair_type"],
            row["codes"][0] or row["member_ids"][0],
            row["codes"][1] or row["member_ids"][1],
            str(row["overlap_area_m2"]), str(row["deduction_height_mm"]),
            str(row["potential_deduction_volume_m3"]), row["suggested_owner"],
            row["confidence"],
            ";".join(str(value) for value in row["overlap_bbox_mm"]),
        ])
    return rows


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="审计 CAD 梁、墙、柱、边缘构件和连梁的矩形重复计量")
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--phase20-json", default=None)
    parser.add_argument("--ledger-json", required=True)
    parser.add_argument("--story-height-mm", type=float, default=3870.0)
    parser.add_argument("--coupling-height-mm", type=float, default=500.0)
    parser.add_argument("--area-tolerance-m2", type=float, default=0.0001)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    paths = {
        "model": Path(args.model_json),
        "ledger": Path(args.ledger_json),
    }
    if args.phase20_json:
        paths["phase20"] = Path(args.phase20_json)
    missing = [name for name, path in paths.items() if not path.exists()]
    if missing:
        parser.error("缺少输入：" + "、".join(missing))
    result = build_audit(
        _load(paths["model"]),
        _load(paths["phase20"]) if "phase20" in paths else {},
        _load(paths["ledger"]),
        args.story_height_mm,
        args.coupling_height_mm,
        args.area_tolerance_m2,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    json_path = out.with_suffix(".json")
    csv_path = out.with_suffix(".csv")
    md_path = out.with_suffix(".md")
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle).writerows(csv_rows(result))
    md_path.write_text(render_markdown(result), encoding="utf-8")
    checksums = out.with_name(out.name + ".sha256")
    checksums.write_text("\n".join(
        f"{sha256(path)}  {path.resolve()}"
        for path in (json_path, csv_path, md_path)) + "\n", encoding="utf-8")
    summary = result["summary"]
    print(json.dumps({
        "overlap_count": summary["overlap_count"],
        "overlap_area_m2": summary["overlap_area_m2"],
        "potential_deduction_volume_m3": summary["potential_deduction_volume_m3"],
        "groups": {k: v["potential_deduction_volume_m3"]
                   for k, v in summary["groups"].items()},
        "outputs": [str(json_path), str(csv_path), str(md_path), str(checksums)],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
