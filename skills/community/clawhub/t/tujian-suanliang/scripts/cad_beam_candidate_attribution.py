#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复核梁截面口径，并把图框内未覆盖候选段归属到已有编号或登记为无归属。"""



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
import re
from pathlib import Path
from typing import Any


SCHEMA = "cad-beam-candidate-attribution/v0.1"
SECTION_RE = re.compile(r"(\d+(?:\.\d+)*)\s*[xX*\u00d7]\s*(\d+(?:\.\d+)*)")



def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _code_key(value: Any) -> str:
    return re.sub(r"\s+", "", _text(value)).upper()


def _section(value: Any) -> tuple[float, float] | None:
    match = SECTION_RE.search(_text(value))
    if not match:
        return None
    width = _number(match.group(1))
    height = _number(match.group(2))
    if width <= 0.0 or height <= 0.0:
        return None
    return width, height


def _area(section: tuple[float, float] | None) -> float:
    return 0.0 if section is None else section[0] * section[1] / 1_000_000.0


def _runs(model: dict[str, Any]) -> list[dict[str, Any]]:
    registry = model.get("run_registry") or {}
    return [run for run in registry.get("runs") or [] if _text(run.get("id"))]


def _recon_rows(reconciliation: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in reconciliation.get("beam_code_reconciliation") or []:
        key = _code_key(row.get("code"))
        if key:
            rows[key] = row
    return rows


def recheck_section_caliber(
        model: dict[str, Any], reconciliation: dict[str, Any],
        options: dict[str, Any]) -> dict[str, Any]:
    """把每条实例截面换成编号参考截面，量化"截面口径"本身贡献了多少体积。"""
    recon = _recon_rows(reconciliation)
    run_index = {_text(run.get("id")): run for run in _runs(model)}
    run_rows: list[dict[str, Any]] = []
    code_rows: list[dict[str, Any]] = []
    for key, row in sorted(recon.items()):
        reference = _section(row.get("reference_single_section"))
        area = _area(reference)
        run_ids: list[str] = []
        span = 0.0
        for chain in row.get("selected_chains") or []:
            span += _number(chain.get("span_mm"))
            run_ids.extend(_text(run_id) for run_id in chain.get("run_ids") or [])
        cad_volume = 0.0
        caliber_volume = 0.0
        run_length = 0.0
        for run_id in run_ids:
            run = run_index.get(run_id)
            if not run:
                continue
            length = _number(run.get("length_mm"))
            run_volume = _number(run.get("volume_m3"))
            cad_volume += run_volume
            caliber_volume += area * length / 1000.0
            run_length += length
            run_section = _section(run.get("section"))
            if area <= 0.0 or run_section is None:
                status = "skipped-no-reference-section"
                delta = 0.0
            elif reference and (abs(run_section[0] - reference[0]) > 1.0
                                or abs(run_section[1] - reference[1]) > 1.0):
                status = "rechecked-mismatch"
                delta = area * length / 1000.0 - run_volume
            else:
                status = "rechecked-match"
                delta = 0.0
            run_rows.append({
                "run_id": run_id,
                "matched_code": _text(run.get("matched_code")),
                "cad_section": _text(run.get("section")),
                "reference_section": _text(row.get("reference_single_section")),
                "length_mm": _round(length, 1),
                "cad_volume_m3": _round(run_volume),
                "reference_section_volume_m3": _round(area * length / 1000.0),
                "delta_m3": _round(delta),
                "status": status,
            })
        code_rows.append({
            "code": _text(row.get("code")),
            "reference_section": _text(row.get("reference_single_section")),
            "selected_run_count": len(run_ids),
            "run_length_mm": _round(run_length, 1),
            "chain_span_mm": _round(span, 1),
            "chain_span_minus_run_length_mm": _round(span - run_length, 1),
            "cad_run_volume_m3": _round(cad_volume),
            "reference_section_run_volume_m3": _round(caliber_volume),
            "section_caliber_delta_m3": _round(caliber_volume - cad_volume),
            "current_code_volume_m3": _round(row.get("current_code_volume_m3")),
            "current_code_difference_m3": _round(
                row.get("current_code_difference_m3")),
        })
    rechecked = [row for row in run_rows
                 if row["status"] != "skipped-no-reference-section"]
    mismatch = [row for row in rechecked if row["status"] == "rechecked-mismatch"]
    total_delta = sum(_number(row["delta_m3"]) for row in run_rows)
    under_total = sum(abs(_number(row["current_code_difference_m3"]))
                      for row in code_rows
                      if _number(row["current_code_difference_m3"]) < 0.0)
    worst = max(code_rows,
                key=lambda row: abs(_number(row["section_caliber_delta_m3"])),
                default=None)
    return {
        "run_total": len(run_rows),
        "run_rechecked_count": len(rechecked),
        "run_mismatch_count": len(mismatch),
        "run_recheck_delta_m3": _round(total_delta),
        "code_rechecked_count": len(code_rows),
        "code_section_caliber_delta_m3": _round(
            sum(_number(row["section_caliber_delta_m3"]) for row in code_rows)),
        "max_code_caliber_delta_m3": _round(
            worst["section_caliber_delta_m3"]) if worst else 0.0,
        "max_code_caliber_code": _text(worst["code"]) if worst else "",
        "code_under_total_m3": _round(under_total),
        "caliber_share_of_under_total_pct": _round(
            0.0 if under_total <= 0.0
            else abs(total_delta) / under_total * 100.0, 2),
        "section_caliber_explains_gap": bool(
            abs(_number(total_delta))
            > _number(options.get("residual_tolerance_m3"), 0.05)),
        "mismatch_runs": mismatch,
        "runs": run_rows,
        "codes": code_rows,
    }


def attribute_candidates(
        model: dict[str, Any], coverage: dict[str, Any],
        options: dict[str, Any]) -> list[dict[str, Any]]:
    """把图框内未覆盖候选段按同轴续接规则挂到已有编号实例上。"""
    axis_tolerance = _number(options.get("axis_tolerance_mm"), 60.0)
    joint_max = _number(options.get("joint_max_mm"), 400.0)
    width_tolerance = _number(options.get("width_tolerance_mm"), 50.0)
    runs = _runs(model)
    rows: list[dict[str, Any]] = []
    for candidate in coverage.get("candidates") or []:
        if _text(candidate.get("view_zone")) != "inside-extraction-window":
            continue
        low, high = sorted((_number(candidate.get("start_mm")),
                            _number(candidate.get("end_mm"))))
        best: tuple[float, float, dict[str, Any]] | None = None
        for run in runs:
            if _text(run.get("orientation")) != _text(candidate.get("orientation")):
                continue
            axis_offset = abs(_number(run.get("axis_mm"))
                              - _number(candidate.get("axis_mm")))
            if axis_offset > axis_tolerance:
                continue
            run_low, run_high = sorted(
                (_number(run.get("start_mm")), _number(run.get("end_mm"))))
            joint = max(run_low - high, low - run_high)
            if joint > joint_max:
                continue
            if best is None or (joint, axis_offset) < (best[0], best[1]):
                best = (joint, axis_offset, run)
        width = _number(candidate.get("width_mm"))
        length = _number(candidate.get("length_mm"))
        row: dict[str, Any] = {
            "handles": "+".join(_text(item)
                                for item in candidate.get("handles") or []),
            "orientation": _text(candidate.get("orientation")),
            "axis_mm": _round(candidate.get("axis_mm"), 1),
            "start_mm": _round(low, 1),
            "end_mm": _round(high, 1),
            "length_mm": _round(length, 1),
            "width_mm": _round(width, 1),
            "assumed_height_mm": _round(candidate.get("assumed_height_mm"), 1),
            "candidate_volume_m3": _round(candidate.get("volume_m3")),
            "evidence": _text(candidate.get("evidence")),
        }
        if not best:
            row.update({
                "matched_run_id": "",
                "matched_code": "",
                "matched_section": "",
                "axis_offset_mm": None,
                "joint_gap_mm": None,
                "width_difference_mm": None,
                "attributed_volume_m3": 0.0,
                "status": "no-coaxial-run",
                "action": "同轴无续接实例，不能凭位置补编号，回图核对",
            })
        else:
            joint, axis_offset, run = best
            run_width = _number(run.get("section_b_mm")) or _number(
                run.get("paired_width_mm"))
            height = _number(run.get("section_h_mm"))
            width_difference = (abs(run_width - width)
                                if run_width > 0.0 else None)
            attributed = width * height * length / 1_000_000_000.0
            conflict = bool(width_difference is not None
                            and width_difference > width_tolerance)
            row.update({
                "matched_run_id": _text(run.get("id")),
                "matched_code": _text(run.get("matched_code")),
                "matched_section": _text(run.get("section")),
                "axis_offset_mm": _round(axis_offset, 1),
                "joint_gap_mm": _round(joint, 1),
                "width_difference_mm": (_round(width_difference, 1)
                                        if width_difference is not None else None),
                "attributed_volume_m3": 0.0 if conflict else _round(attributed),
                "status": "section-conflict" if conflict else "attributed",
                "assignment_evidence": _text(run.get("code_assignment_status")),
                "confidence": _text(run.get("confidence")),
                "mirror_axis_mm": _round(run.get("mirror_axis_mm"), 1),
                "action": ("梁宽与实例截面不一致，只登记冲突不回写体积" if conflict
                           else "作为该编号实例的续接段计入已定位梁量"),
            })
        rows.append(row)
    return rows


def decompose_residual(
        coverage: dict[str, Any], attributions: list[dict[str, Any]],
        section_recheck: dict[str, Any],
        options: dict[str, Any]) -> dict[str, Any]:
    """把梁缺口拆成"可归属""有几何无编号""本图框无法解释"三段。"""
    summary = coverage.get("summary") or {}
    residual = _number(summary.get("residual_gap_m3"))
    tolerance = _number(options.get("unexplained_tolerance_m3"),
                        _number(summary.get("unexplained_tolerance_m3"), 0.05))
    attached = sum(_number(row.get("attributed_volume_m3"))
                   for row in attributions
                   if _text(row.get("status")) == "attributed")
    conflict = sum(_number(row.get("candidate_volume_m3"))
                   for row in attributions
                   if _text(row.get("status")) == "section-conflict")
    unattached = sum(_number(row.get("candidate_volume_m3"))
                     for row in attributions
                     if _text(row.get("status")) != "attributed")
    caliber_adjust = sum(
        _number(row.get("candidate_volume_m3")) - _number(row.get("attributed_volume_m3"))
        for row in attributions if _text(row.get("status")) == "attributed")
    unexplained = residual - attached - unattached
    reported = _number(summary.get("residual_still_unexplained_m3"))
    length_unattached = sum(
        _number(row.get("length_mm")) for row in attributions
        if _text(row.get("status")) != "attributed")
    rows = [
        {"item": "需新几何的梁缺口", "key": "residual_needing_new_geometry_m3",
         "value_m3": _round(residual), "counted_in_quantity": "否",
         "note": "取自梁图层覆盖审计"},
        {"item": "可归属到已有编号的续接段",
         "key": "attached_to_existing_code_m3", "value_m3": _round(attached),
         "counted_in_quantity": "是",
         "note": "同轴续接，端头间隙在容差内，按实例截面计量"},
        {"item": "有几何但无同轴编号的候选段",
         "key": "unattached_candidate_m3", "value_m3": _round(unattached),
         "counted_in_quantity": "否",
         "note": "含截面冲突段，必须回图定编号后才能计量"},
        {"item": "其中截面冲突段", "key": "section_conflict_m3",
         "value_m3": _round(conflict), "counted_in_quantity": "否",
         "note": "梁宽与实例截面不一致"},
        {"item": "归属段截面口径调整", "key": "caliber_adjustment_m3",
         "value_m3": _round(caliber_adjust), "counted_in_quantity": "否",
         "note": "候选假定高换成实例截面高产生的量差，不计入构件体积"},
        {"item": "本图框无法解释", "key": "unexplained_by_this_frame_m3",
         "value_m3": _round(unexplained), "counted_in_quantity": "否",
         "note": "图框内已无未覆盖梁线可分配"},
        {"item": "覆盖审计口径的未解释量",
         "key": "coverage_reported_unexplained_m3", "value_m3": _round(reported),
         "counted_in_quantity": "否", "note": "交叉核对项，不参与相加"},
        {"item": "镜像对称视图候选", "key": "mirror_pair_excluded_m3",
         "value_m3": _round(summary.get("candidate_volume_mirror_pair_m3")),
         "counted_in_quantity": "否", "note": "量级校验不通过，判为重复视图证据"},
        {"item": "整视图平移孪生候选", "key": "translated_view_excluded_m3",
         "value_m3": _round(summary.get("candidate_volume_translated_view_m3")),
         "counted_in_quantity": "否", "note": "平移重复绘制，不计漏量"},
        {"item": "截面口径改动的体积",
         "key": "section_caliber_delta_m3",
         "value_m3": _round(section_recheck.get("run_recheck_delta_m3")),
         "counted_in_quantity": "否",
         "note": "全为 0 说明缺口不是截面高取值造成"},
    ]
    identity_delta = residual - (attached + unattached + unexplained)
    return {
        "residual_gap_m3": _round(residual),
        "attached_to_existing_code_m3": _round(attached),
        "unattached_candidate_m3": _round(unattached),
        "section_conflict_m3": _round(conflict),
        "unexplained_by_this_frame_m3": _round(unexplained),
        "coverage_reported_unexplained_m3": _round(reported),
        "caliber_adjustment_m3": _round(caliber_adjust),
        "cross_check_delta_m3": _round(
            abs(unexplained - (reported + caliber_adjust))),
        "unattached_length_mm": _round(length_unattached, 1),
        "unexplained_tolerance_m3": _round(tolerance),
        "unexplained_within_tolerance": bool(abs(unexplained) <= tolerance),
        "decomposition": rows,
        "matches_identity": bool(abs(identity_delta) <= 0.0005),
    }


def build_code_targets(
        gap: dict[str, Any] | None, attributions: list[dict[str, Any]],
        decomposition: dict[str, Any]) -> dict[str, Any]:
    """对偏少编号逐个核对"本图框剩余未归属图线"够不够补齐。"""
    pool = [dict(row) for row in attributions
            if _text(row.get("status")) != "attributed"]
    claimed: set[str] = set()
    pending = sorted(
        (row for row in (gap or {}).get("code_attribution") or []
         if _number(row.get("difference_m3")) < 0.0),
        key=lambda row: _number(row.get("difference_m3")))
    rows: list[dict[str, Any]] = []
    for row in pending:
        section = _section(row.get("reference_section"))
        width = section[0] if section else 0.0
        needed = _number(row.get("needed_length_mm"))
        count_only = needed <= 1.0
        candidate: dict[str, Any] | None = None
        for item in sorted(
                (entry for entry in pool
                 if _text(entry.get("handles")) not in claimed
                 and width > 0.0
                 and abs(_number(entry.get("width_mm")) - width) <= 50.0
                 and _number(entry.get("length_mm")) + 1.0 >= needed),
                key=lambda entry: _number(entry.get("length_mm"))):
            candidate = item
            break
        if candidate is not None:
            claimed.add(_text(candidate.get("handles")))
        compatible = [
            _text(entry.get("handles")) for entry in pool
            if width > 0.0 and abs(_number(entry.get("width_mm")) - width) <= 50.0]
        rows.append({
            "code": _text(row.get("code")),
            "reference_section": _text(row.get("reference_section")),
            "difference_m3": _round(row.get("difference_m3")),
            "needed_length_mm": _round(needed, 1),
            "missing_instance_count": int(_number(
                row.get("missing_instance_count"))),
            "prior_unassigned_candidate_count": int(_number(
                row.get("unassigned_candidate_count"))),
            "in_frame_compatible_count": len(compatible),
            "claim_candidate_handles": _text(
                candidate.get("handles")) if candidate else "",
            "claim_candidate_length_mm": _round(
                candidate.get("length_mm"), 1) if candidate else 0.0,
            "classification": ("count-only-caliber" if count_only else
                               "claimed-in-frame" if candidate else
                               "needs-cross-frame-search"),
            "action": (
                "量差在计数口径内，不需要新几何，只需回图核对实例数"
                if count_only else
                "本图框有一条同宽未归属梁线长度可容纳该缺量，"
                "属长度相容假设，须回图确认编号后才可计量"
                if candidate else
                "本图框无同宽且足够长的未覆盖梁线，须跨图框或大样检索"),
        })
    cross = [row for row in rows
             if _text(row.get("classification")) == "needs-cross-frame-search"]
    count_only = [row for row in rows
                  if _text(row.get("classification")) == "count-only-caliber"]
    return {
        "under_code_count": len(rows),
        "under_total_m3": _round(sum(abs(_number(row["difference_m3"]))
                                     for row in rows)),
        "total_needed_length_mm": _round(
            sum(_number(row["needed_length_mm"]) for row in rows), 1),
        "in_frame_unattached_count": len(pool),
        "in_frame_unattached_length_mm": _round(
            decomposition.get("unattached_length_mm"), 1),
        "in_frame_unattached_volume_m3": _round(
            decomposition["unattached_candidate_m3"]),
        "claimed_candidate_handles": sorted(claimed),
        "unclaimed_candidate_handles": [
            _text(entry.get("handles")) for entry in pool
            if _text(entry.get("handles")) not in claimed],
        "cross_frame_code_count": len(cross),
        "cross_frame_needed_length_mm": _round(
            sum(_number(row["needed_length_mm"]) for row in cross), 1),
        "cross_frame_missing_volume_m3": _round(
            sum(abs(_number(row["difference_m3"])) for row in cross)),
        "count_only_code_count": len(count_only),
        "net_residual_reference_m3": _round(
            decomposition.get("residual_gap_m3")),
        "gross_under_warning": (
            "毛差含偏多编号反向抵消，净需新几何量看 "
            "net_residual_reference_m3，两个口径不得混用"),
        "frame_can_close_all": bool(
            rows and not cross and len(claimed) >= len(pool)),
        "codes": rows,
    }


def build_attribution(
        model: dict[str, Any], coverage: dict[str, Any],
        reconciliation: dict[str, Any], gap: dict[str, Any] | None,
        options: dict[str, Any]) -> dict[str, Any]:
    floor = _text(options.get("floor_label")) or _text(coverage.get("floor"))
    section_recheck = recheck_section_caliber(model, reconciliation, options)
    attributions = attribute_candidates(model, coverage, options)
    decomposition = decompose_residual(coverage, attributions, section_recheck,
                                       options)
    targets = build_code_targets(gap, attributions, decomposition)
    residual = decomposition["unexplained_by_this_frame_m3"]
    unattributed = sum(1 for row in attributions
                       if _text(row.get("status")) != "attributed")
    gates = {
        "section-caliber-cleared": bool(
            section_recheck["run_mismatch_count"] == 0),
        "attribution-decomposition-closed": bool(decomposition["matches_identity"]),
        "all-in-frame-candidates-attributed": bool(
            attributions and unattributed == 0),
        "residual-within-tolerance": bool(
            decomposition["unexplained_within_tolerance"]),
    }
    return {
        "schema": SCHEMA,
        "floor": floor,
        "rule": ("候选段只有同轴（默认 60mm）且端头间隙不超过容差（默认 400mm）"
                 "才归属到已有编号实例；无同轴实例的候选段一律留作回图证据，"
                 "不得凭位置补编号或补体积。"),
        "options": {
            "axis_tolerance_mm": _round(options.get("axis_tolerance_mm", 60.0), 1),
            "joint_max_mm": _round(options.get("joint_max_mm", 400.0), 1),
            "width_tolerance_mm": _round(options.get("width_tolerance_mm", 50.0), 1),
            "section_delta_tolerance_m3": _round(
                options.get("section_delta_tolerance_m3", 0.0005), 6),
            "unexplained_tolerance_m3": _round(
                options.get("unexplained_tolerance_m3", 0.05)),
            "floor_label": floor,
        },
        "summary": {
            "coverage_schema": _text(coverage.get("schema")),
            "run_count": len(_runs(model)),
            "reconciliation_code_count": len(
                reconciliation.get("beam_code_reconciliation") or []),
            "in_frame_candidate_count": len(attributions),
            "attributed_count": sum(
                1 for row in attributions if row["status"] == "attributed"),
            "no_coaxial_run_count": sum(
                1 for row in attributions if row["status"] == "no-coaxial-run"),
            "section_conflict_count": sum(
                1 for row in attributions if row["status"] == "section-conflict"),
            "run_rechecked_count": section_recheck["run_rechecked_count"],
            "run_section_mismatch_count": section_recheck["run_mismatch_count"],
            "section_caliber_delta_m3": section_recheck["run_recheck_delta_m3"],
            "section_caliber_explains_gap":
                section_recheck["section_caliber_explains_gap"],
            "residual_gap_m3": decomposition["residual_gap_m3"],
            "attached_to_existing_code_m3":
                decomposition["attached_to_existing_code_m3"],
            "unattached_candidate_m3": decomposition["unattached_candidate_m3"],
            "unexplained_by_this_frame_m3": residual,
            "unattached_length_mm": decomposition["unattached_length_mm"],
            "under_code_count": targets["under_code_count"],
            "under_total_m3": targets["under_total_m3"],
            "total_needed_length_mm": targets["total_needed_length_mm"],
            "cross_frame_code_count": targets["cross_frame_code_count"],
            "cross_frame_needed_length_mm":
                targets["cross_frame_needed_length_mm"],
            "frame_can_close_all": targets["frame_can_close_all"],
            "caliber_adjustment_m3": decomposition["caliber_adjustment_m3"],
            "unattributed_candidate_count": sum(
                1 for row in attributions
                if _text(row.get("status")) != "attributed"),
            "unexplained_tolerance_m3": decomposition["unexplained_tolerance_m3"],
        },
        "section_recheck": section_recheck,
        "candidate_attribution": attributions,
        "residual_decomposition": decomposition,
        "under_code_targets": targets,
        "closure": {
            "gates": gates,
            "fail_count": sum(1 for value in gates.values() if not value),
            "residual_unexplained_m3": residual,
        },
        "formal_ready": False,
        "applied_to_formal_quantity": False,
    }


def csv_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows: list[list[Any]] = [
        ["section", "group", "key", "code", "orientation", "handles",
         "length_mm", "volume_m3", "value_m3", "counted", "status", "note"]]
    for row in result["section_recheck"]["runs"]:
        rows.append(["section", "run-recheck", row["run_id"], row["matched_code"],
                     "", "", row["length_mm"], row["cad_volume_m3"],
                     row["delta_m3"], "", row["status"],
                     f"CAD {row['cad_section']} / 参考 {row['reference_section']}"])
    for row in result["section_recheck"]["codes"]:
        rows.append(["section", "code-recheck", row["code"], row["code"], "", "",
                     row["run_length_mm"], row["cad_run_volume_m3"],
                     row["section_caliber_delta_m3"], "", "rechecked",
                     f"参考截面 {row['reference_section']}；"
                     f"链长减实例长 {row['chain_span_minus_run_length_mm']}mm"])
    for row in result["candidate_attribution"]:
        rows.append(["attribution", "candidate", row["matched_code"] or "-", "",
                     row["orientation"], row["handles"], row["length_mm"],
                     row["candidate_volume_m3"], row["attributed_volume_m3"],
                     "是" if row["status"] == "attributed" else "否",
                     row["status"],
                     f"实例 {row['matched_run_id'] or '无'}；"
                     f"轴偏 {row['axis_offset_mm']}mm；"
                     f"端头间隙 {row['joint_gap_mm']}mm；{row['action']}"])
    for row in result["residual_decomposition"]["decomposition"]:
        rows.append(["decomposition", "residual", row["key"], "", "", "", "", "",
                     row["value_m3"], row["counted_in_quantity"], "", row["note"]])
    for row in result["under_code_targets"]["codes"]:
        rows.append(["target", "under-code", row["code"], row["code"], "", "",
                     row["needed_length_mm"], row["difference_m3"],
                     row["claim_candidate_length_mm"],
                     "否", "search-target", row["action"]])
    return rows


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    decomposition = result["residual_decomposition"]
    targets = result["under_code_targets"]
    lines = [
        "# 梁候选段归属与截面口径复核",
        "",
        f"- 判定规则：{result['rule']}",
        f"- 容差：轴偏 {result['options']['axis_tolerance_mm']} mm，"
        f"端头间隙 {result['options']['joint_max_mm']} mm，"
        f"未解释量 {result['options']['unexplained_tolerance_m3']} m3。",
        "",
        "## 截面口径复核",
        "",
        f"- 可比对实例 {summary['run_rechecked_count']} 条，"
        f"截面不一致 {summary['run_section_mismatch_count']} 条，"
        f"换成参考截面后体积差 `{summary['section_caliber_delta_m3']:.4f}` m3。",
        f"- 结论：截面口径{'是' if summary['section_caliber_explains_gap'] else '不是'}"
        "偏少编号缺量的来源，缺口只能按长度或实例数处理。",
        "",
        "| 编号 | 参考截面 | 实例长mm | CAD体积 | 截面口径差 | 编号量差 |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in result["section_recheck"]["codes"][:12]:
        lines.append(
            f"| {row['code']} | {row['reference_section']} | "
            f"{row['run_length_mm']:.0f} | {row['cad_run_volume_m3']:.4f} | "
            f"{row['section_caliber_delta_m3']:.4f} | "
            f"{row['current_code_difference_m3']:+.4f} |")
    lines += [
        "",
        "## 图框内未覆盖候选段归属",
        "",
        "| 句柄 | 方向 | 轴mm | 长mm | 候选量m3 | 归属编号 | 归属量m3 | 状态 |",
        "|---|---|---:|---:|---:|---|---:|---|",
    ]
    for row in result["candidate_attribution"]:
        lines.append(
            f"| {row['handles']} | {row['orientation']} | {row['axis_mm']:.1f} | "
            f"{row['length_mm']:.0f} | {row['candidate_volume_m3']:.4f} | "
            f"{row['matched_code'] or '—'} | {row['attributed_volume_m3']:.4f} | "
            f"{row['status']} |")
    lines += [
        "",
        "## 缺口分解",
        "",
        "| 项目 | 体积m3 | 计入量 | 说明 |",
        "|---|---:|---|---|",
    ]
    for row in decomposition["decomposition"]:
        lines.append(f"| {row['item']} | {row['value_m3']:.4f} | "
                     f"{row['counted_in_quantity']} | {row['note']} |")
    lines += [
        "",
        f"- 恒等式校验：{'通过' if decomposition['matches_identity'] else '不通过'}；"
        f"与覆盖审计未解释量差 `{decomposition['cross_check_delta_m3']:.4f}` m3。",
        "",
        "## 偏少编号回图目标",
        "",
        f"- 偏少编号 {targets['under_code_count']} 个（毛差口径 "
        f"`{targets['under_total_m3']:.4f}` m3，共需 "
        f"`{targets['total_needed_length_mm']:.0f}` mm 梁线），其中 "
        f"{targets['count_only_code_count']} 个属计数口径、"
        f"{targets['cross_frame_code_count']} 个本图框无线可补，"
        f"需跨图框检索 `{targets['cross_frame_needed_length_mm']:.0f}` mm / "
        f"`{targets['cross_frame_missing_volume_m3']:.4f}` m3。",
        f"- 本图框未归属梁线 "
        f"`{decomposition['unattached_length_mm']:.0f}` mm / "
        f"`{decomposition['unattached_candidate_m3']:.4f}` m3，"
        f"被认领 {len(targets['claimed_candidate_handles'])} 条，"
        f"剩余 {len(targets['unclaimed_candidate_handles'])} 条无人可配。",
        "",
        "| 编号 | 参考截面 | 量差m3 | 需补mm | 认领候选 | 候选长mm | 判定 |",
        "|---|---|---:|---:|---|---:|---|",
    ]
    for row in targets["codes"]:
        lines.append(
            f"| {row['code']} | {row['reference_section']} | "
            f"{row['difference_m3']:.4f} | {row['needed_length_mm']:.0f} | "
            f"{row['claim_candidate_handles'] or '—'} | "
            f"{row['claim_candidate_length_mm']:.0f} | "
            f"{row['classification']} |")
    lines += [
        "",
        "## 结论",
        "",
        f"- 图框内候选段可正式归属 `{summary['attached_to_existing_code_m3']:.4f}` m3，"
        f"其余 `{summary['unattached_candidate_m3']:.4f}` m3 无同轴编号，只登记不回写。",
        f"- 扣除可归属段后仍有 `{summary['unexplained_by_this_frame_m3']:.4f}` m3 "
        "无法用本图框图线解释，必须跨图框或大样检索。",
        "- 认领只缩短回图目标清单：候选段本身已在「有几何无编号」一栏，"
        "不重复计入梁量；`claimed-in-frame` 仅是长度相容假设，须回图确认编号。",
        f"- 毛差 `{targets['under_total_m3']:.4f}` m3 与净缺口 "
        f"`{decomposition['residual_gap_m3']:.4f}` m3 是两个口径，"
        "偏多编号反向抵消后才是需要补的几何量。",
        "- 本节只澄清证据归属，不改变构件体积，`formal_ready` 仍为 `false`。",
    ]
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="复核梁截面口径并归属图框内未覆盖候选段")
    parser.add_argument("--model-json", required=True, help="结构模型 JSON")
    parser.add_argument("--coverage-json", required=True,
                        help="cad-beam-coverage-audit JSON")
    parser.add_argument("--reconciliation-json", required=True,
                        help="cad-beam-reference-reconciliation JSON")
    parser.add_argument("--gap-json", default=None,
                        help="cad-beam-gap-attribution JSON，用于偏少编号目标")
    parser.add_argument("--axis-tolerance-mm", type=float, default=60.0)
    parser.add_argument("--joint-max-mm", type=float, default=400.0)
    parser.add_argument("--width-tolerance-mm", type=float, default=50.0)
    parser.add_argument("--section-delta-tolerance-m3", type=float, default=0.0005)
    parser.add_argument("--unexplained-tolerance-m3", type=float, default=0.05)
    parser.add_argument("--floor-label", default=None,
                        help="楼层口径名，缺省沿用覆盖审计里的图名")
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    paths = {"model": Path(args.model_json),
             "coverage": Path(args.coverage_json),
             "reconciliation": Path(args.reconciliation_json)}
    if args.gap_json:
        paths["gap"] = Path(args.gap_json)
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        parser.error("缺少输入：" + "、".join(missing))
    coverage = _load(paths["coverage"])
    if _text(coverage.get("schema")) != SCHEMA.replace(
            "candidate-attribution", "coverage-audit"):
        print(f"警告：coverage 输入 schema 为 {_text(coverage.get('schema'))}")
    result = build_attribution(
        _load(paths["model"]), coverage, _load(paths["reconciliation"]),
        _load(paths["gap"]) if "gap" in paths else None,
        {"axis_tolerance_mm": args.axis_tolerance_mm,
         "joint_max_mm": args.joint_max_mm,
         "width_tolerance_mm": args.width_tolerance_mm,
         "section_delta_tolerance_m3": args.section_delta_tolerance_m3,
         "unexplained_tolerance_m3": args.unexplained_tolerance_m3,
         "floor_label": args.floor_label})
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    json_path = out.with_suffix(".json")
    csv_path = out.with_suffix(".csv")
    md_path = out.with_suffix(".md")
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=1),
                         encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle).writerows(csv_rows(result))
    md_path.write_text(render_markdown(result), encoding="utf-8")
    checksums = out.with_name(out.name + ".sha256")
    checksums.write_text("\n".join(
        f"{sha256(path)}  {path.resolve()}"
        for path in (json_path, csv_path, md_path)) + "\n", encoding="utf-8")
    summary = result["summary"]
    print(json.dumps({
        "schema": result["schema"],
        "floor": summary["floor"] if "floor" in summary else result["floor"],
        "run_section_mismatch_count": summary["run_section_mismatch_count"],
        "section_caliber_delta_m3": summary["section_caliber_delta_m3"],
        "attributed_count": summary["attributed_count"],
        "no_coaxial_run_count": summary["no_coaxial_run_count"],
        "attached_to_existing_code_m3": summary["attached_to_existing_code_m3"],
        "unattached_candidate_m3": summary["unattached_candidate_m3"],
        "unexplained_by_this_frame_m3": summary["unexplained_by_this_frame_m3"],
        "frame_can_close_all": summary["frame_can_close_all"],
        "gates": result["closure"]["gates"],
        "formal_ready": result["formal_ready"],
        "outputs": [str(json_path), str(csv_path), str(md_path), str(checksums)],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
