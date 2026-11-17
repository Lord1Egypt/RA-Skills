#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把算量实例 run 与模型梁 members.beams 判为同一物理梁，防止两套口径重复计量。"""



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
from pathlib import Path
from typing import Any


SCHEMA = "cad-beam-instance-dedup/v0.1"



def _code(value: Any) -> str:
    return _text(value).strip().lower().replace(" ", "")


def _overlap(first: tuple, second: tuple) -> float:
    return max(0.0, min(first[1], second[1]) - max(first[0], second[0]))


def _runs(model: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run in (model.get("run_registry") or {}).get("runs") or []:
        lo, hi = sorted((_number(run.get("start_mm")), _number(run.get("end_mm"))))
        rows.append({
            "id": _text(run.get("id")),
            "orientation": _text(run.get("orientation")),
            "axis_mm": _round(_number(run.get("axis_mm")), 1),
            "lo_mm": _round(lo, 1), "hi_mm": _round(hi, 1),
            "length_mm": _round(hi - lo, 1),
            "section": _text(run.get("section")),
            "volume_m3": _round(run.get("volume_m3")),
            "code": _text(run.get("matched_code")),
            "code_key": _code(run.get("matched_code")),
            "evidence": _text(run.get("code_assignment_status")),
            "confidence": _text(run.get("confidence")),
        })
    return rows


def _beams(model: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for beam in (model.get("members") or {}).get("beams") or []:
        centerline = beam.get("centerline") or {}
        start = centerline.get("start") or [0.0, 0.0]
        end = centerline.get("end") or [0.0, 0.0]
        orientation = _text(centerline.get("orientation")) or (
            "H" if abs(_number(start[1]) - _number(end[1])) <= 1.0 else "V")
        if orientation == "H":
            axis, lo, hi = _number(start[1]), _number(start[0]), _number(end[0])
        else:
            axis, lo, hi = _number(start[0]), _number(start[1]), _number(end[1])
        lo, hi = sorted((lo, hi))
        rows.append({
            "id": _text(beam.get("id")),
            "code": _text(beam.get("code")),
            "code_key": _code(beam.get("code")),
            "section": _text(beam.get("section")),
            "orientation": orientation,
            "axis_mm": _round(axis, 1), "lo_mm": _round(lo, 1),
            "hi_mm": _round(hi, 1),
            "length_mm": _round(hi - lo, 1),
            "volume_m3": _round(beam.get("gross_volume_m3")),
            "quantity_status": _text(beam.get("quantity_status")),
        })
    return rows


def _candidates(beam: dict[str, Any], run: dict[str, Any],
                options: dict[str, Any]) -> tuple[str, float, float] | None:
    """返回（证据级别, 沿轴重叠 mm, 轴距 mm），不成立时返回 None。"""
    if run["orientation"] != beam["orientation"]:
        return None
    offset = abs(_number(run["axis_mm"]) - _number(beam["axis_mm"]))
    shared = _overlap((run["lo_mm"], run["hi_mm"]),
                      (beam["lo_mm"], beam["hi_mm"]))
    shorter = min(_number(run["length_mm"]), _number(beam["length_mm"]))
    if shorter <= 0.0:
        return None
    min_overlap = _number(options.get("min_overlap_ratio"), 0.5)
    if shared < min_overlap * shorter:
        return None
    if beam["code_key"] and run["code_key"] == beam["code_key"]:
        if offset > _number(options.get("code_axis_tolerance_mm"), 5000.0):
            return None
        return "编号+同轴区间", shared, offset
    if not run["code_key"]:
        if offset > _number(options.get("geometry_axis_tolerance_mm"), 400.0):
            return None
        if _text(run["section"]) != _text(beam["section"]):
            return None
        return "无编号纯几何", shared, offset
    return None


def match(runs: list[dict[str, Any]], beams: list[dict[str, Any]],
          options: dict[str, Any]) -> tuple[list[dict[str, Any]],
                                            list[dict[str, Any]]]:
    """先按轴距最近做一对一锁配，再为未覆盖的梁续接同编号 run。"""
    tolerance = _number(options.get("code_axis_tolerance_mm"), 5000.0)
    pairs: list[tuple[float, float, int, int, str]] = []
    for b_index, beam in enumerate(beams):
        for r_index, run in enumerate(runs):
            hit = _candidates(beam, run, options)
            if hit is not None:
                pairs.append((hit[2], -hit[1], b_index, r_index, hit[0]))
    pairs.sort()
    owned: dict[int, list[tuple[float, float, dict[str, Any]]]] = {
        index: [] for index in range(len(beams))}
    used_runs: set[int] = set()
    for offset, neg_shared, b_index, r_index, evidence in pairs:
        if owned[b_index] or r_index in used_runs:
            continue
        owned[b_index].append((offset, _number(runs[r_index]["length_mm"]),
                               runs[r_index]))
        used_runs.add(r_index)
    for b_index, beam in enumerate(beams):
        claimed = owned[b_index]
        covered = sum(item[1] for item in claimed)
        while covered < _number(beam["length_mm"]) - 1.0:
            best: tuple[float, int] | None = None
            for r_index, run in enumerate(runs):
                if r_index in used_runs:
                    continue
                if run["orientation"] != beam["orientation"]:
                    continue
                if run["code_key"] != beam["code_key"] or not beam["code_key"]:
                    continue
                offset = abs(_number(run["axis_mm"]) - _number(beam["axis_mm"]))
                if offset > tolerance:
                    continue
                shared = _overlap((run["lo_mm"], run["hi_mm"]),
                                  (beam["lo_mm"], beam["hi_mm"]))
                if shared < _number(options.get("min_overlap_ratio"), 0.5) * _number(
                        run["length_mm"]):
                    continue
                if best is None or (offset, -shared) < best[:2]:
                    best = (offset, -shared, r_index)  # type: ignore[assignment]
            if best is None:
                break
            run = runs[best[2]]
            used_runs.add(best[2])
            claimed.append((best[0], _number(run["length_mm"]), run))
            covered += _number(run["length_mm"])
    rows: list[dict[str, Any]] = []
    for b_index, beam in enumerate(beams):
        claimed = owned[b_index]
        covered = sum(item[1] for item in claimed)
        run_volume = sum(_number(item[2]["volume_m3"]) for item in claimed)
        length_tol = _number(options.get("length_tolerance_mm"), 200.0)
        if not claimed:
            status = "beam-only"
        elif len(claimed) == 1 and abs(covered - _number(
                beam["length_mm"])) <= length_tol:
            status = "same-instance-1to1"
        elif covered + length_tol < _number(beam["length_mm"]):
            status = "same-instance-partial-cover"
        else:
            status = "same-instance-multi-run"
        rows.append({
            "beam_id": beam["id"], "code": beam["code"],
            "code_key": beam["code_key"],
            "section": beam["section"], "orientation": beam["orientation"],
            "axis_mm": beam["axis_mm"], "lo_mm": beam["lo_mm"],
            "hi_mm": beam["hi_mm"], "beam_length_mm": beam["length_mm"],
            "beam_volume_m3": beam["volume_m3"],
            "evidence": ("无" if not claimed else (
                "编号+同轴区间" if claimed[0][2]["code_key"] == beam["code_key"]
                else "无编号纯几何")),
            "run_ids": [item[2]["id"] for item in claimed],
            "run_codes": sorted({item[2]["code"] or "未归属" for item in claimed}),
            "run_length_mm": _round(covered, 1),
            "run_volume_m3": _round(run_volume),
            "coverage_ratio": _round(
                covered / (abs(_number(beam["length_mm"])) or 1.0), 3),
            "axis_offset_max_mm": _round(max(
                (item[0] for item in claimed), default=0.0), 1),
            "section_conflict": bool(
                claimed and any(_text(item[2]["section"]) != _text(beam["section"])
                                for item in claimed)),
            "status": status,
            "double_count_m3": 0.0 if not claimed else _round(
                min(_number(beam["volume_m3"]), run_volume)),
        })
    leftovers = [run for index, run in enumerate(runs) if index not in used_runs]
    return rows, leftovers


def _self_overlap(runs: list[dict[str, Any]],
                  options: dict[str, Any]) -> dict[str, Any]:
    """run 口径内部重叠扫描：同向、同轴、沿轴区间相交即为潜在重复计量。"""
    tolerance = _number(options.get("self_overlap_axis_tolerance_mm"), 400.0)
    pairs: list[dict[str, Any]] = []
    for i in range(len(runs)):
        for j in range(i + 1, len(runs)):
            first, second = runs[i], runs[j]
            if first["orientation"] != second["orientation"]:
                continue
            offset = abs(_number(first["axis_mm"]) - _number(second["axis_mm"]))
            if offset > tolerance:
                continue
            shared = _overlap((first["lo_mm"], first["hi_mm"]),
                              (second["lo_mm"], second["hi_mm"]))
            if shared <= 1.0:
                continue
            shorter = min(_number(first["length_mm"]), _number(second["length_mm"]))
            smaller = first if _number(first["volume_m3"]) <= _number(
                second["volume_m3"]) else second
            pairs.append({
                "run_ids": [first["id"], second["id"]],
                "orientation": first["orientation"],
                "axis_offset_mm": _round(offset, 1),
                "overlap_mm": _round(shared, 1),
                "codes": sorted({first["code"] or "未归属",
                                 second["code"] or "未归属"}),
                "overlapped_volume_m3": _round(_number(smaller["volume_m3"])
                                               * shared / max(shorter, 1.0)),
            })
    return {"axis_tolerance_mm": _round(tolerance, 1),
            "pair_count": len(pairs),
            "overlap_length_mm": _round(sum(item["overlap_mm"] for item in pairs), 1),
            "overlapped_volume_m3": _round(sum(
                item["overlapped_volume_m3"] for item in pairs)),
            "pairs": pairs}


def _triage(leftovers: list[dict[str, Any]], beams: list[dict[str, Any]],
            options: dict[str, Any]) -> list[dict[str, Any]]:
    """给未配对 run 定责：续接段、归属冲突，还是模型确实缺这根实例。"""
    tolerance = _number(options.get("code_axis_tolerance_mm"), 5000.0)
    gap = _number(options.get("gap_tolerance_mm"), 400.0)
    rows: list[dict[str, Any]] = []
    for run in leftovers:
        continuation: list[dict[str, Any]] = []
        same_code: list[dict[str, Any]] = []
        conflict: list[dict[str, Any]] = []
        for beam in beams:
            if beam["orientation"] != run["orientation"]:
                continue
            offset = abs(_number(run["axis_mm"]) - _number(beam["axis_mm"]))
            if offset > tolerance:
                continue
            shared = _overlap((run["lo_mm"], run["hi_mm"]),
                              (beam["lo_mm"], beam["hi_mm"]))
            shortest = min(_number(run["length_mm"]), _number(beam["length_mm"]))
            if run["code_key"] and beam["code_key"] == run["code_key"]:
                same_code.append(beam)
                near = (run["lo_mm"] >= beam["hi_mm"] - gap
                        and run["lo_mm"] <= beam["hi_mm"] + gap) or (
                    run["hi_mm"] <= beam["lo_mm"] + gap
                    and run["hi_mm"] >= beam["lo_mm"] - gap)
                if near:
                    continuation.append(beam)
            elif shared >= 0.5 * shortest and beam["code_key"] != run["code_key"]:
                conflict.append(beam)
        if continuation:
            verdict = "continuation-candidate"
        elif conflict:
            verdict = "attribution-conflict"
        elif same_code:
            verdict = "same-code-other-location"
        else:
            verdict = "model-missing-instance"
        rows.append({
            "run_id": run["id"], "code": run["code"],
            "orientation": run["orientation"], "axis_mm": run["axis_mm"],
            "lo_mm": run["lo_mm"], "hi_mm": run["hi_mm"],
            "length_mm": run["length_mm"], "volume_m3": run["volume_m3"],
            "evidence": run["evidence"], "confidence": run["confidence"],
            "verdict": verdict,
            "continuation_beam_ids": [b["id"] for b in continuation],
            "conflicting_beam_ids": [b["id"] for b in conflict],
            "conflicting_codes": sorted({b["code"] for b in conflict}),
            "same_code_beam_count": len(same_code),
        })
    rows.sort(key=lambda row: (-_number(row["volume_m3"]), row["run_id"]))
    return rows


def _instance_table(runs: list[dict[str, Any]],
                    links: list[dict[str, Any]],
                    leftovers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in links:
        key = row.get("code_key") or _code(row["code"])
        entry = grouped.setdefault(key, {
            "code": row["code"], "beam_count": 0, "run_count": 0,
            "beam_volume_m3": 0.0, "run_volume_m3": 0.0,
            "extra_run_ids": [], "unresolved_beam_ids": []})
        entry["beam_count"] += 1
        entry["beam_volume_m3"] += _number(row["beam_volume_m3"])
        entry["run_count"] += len(row["run_ids"])
        entry["run_volume_m3"] += _number(row["run_volume_m3"])
        if row["status"] == "beam-only":
            entry["unresolved_beam_ids"].append(row["beam_id"])
    for run in leftovers:
        key = run["code_key"] or "未归属"
        entry = grouped.setdefault(key, {
            "code": run["code"] or "未归属", "beam_count": 0, "run_count": 0,
            "beam_volume_m3": 0.0, "run_volume_m3": 0.0,
            "extra_run_ids": [], "unresolved_beam_ids": []})
        entry["run_count"] += 1
        entry["run_volume_m3"] += _number(run["volume_m3"])
        entry["extra_run_ids"].append(run["id"])
    rows: list[dict[str, Any]] = []
    for entry in grouped.values():
        rows.append({
            "code": entry["code"],
            "beam_count": entry["beam_count"],
            "run_count": entry["run_count"],
            "instance_delta": entry["run_count"] - entry["beam_count"],
            "beam_volume_m3": _round(entry["beam_volume_m3"]),
            "run_volume_m3": _round(entry["run_volume_m3"]),
            "extra_run_ids": entry["extra_run_ids"],
            "unresolved_beam_ids": entry["unresolved_beam_ids"],
        })
    rows.sort(key=lambda row: (-abs(row["instance_delta"]), row["code"]))
    return rows


def build_dedup(model: dict[str, Any],
                options: dict[str, Any]) -> dict[str, Any]:
    runs = _runs(model)
    beams = _beams(model)
    links, leftovers = match(runs, beams, options)
    tol = _number(options.get("conflict_tolerance_m3"), 0.05)
    run_volume = sum(_number(row["volume_m3"]) for row in runs)
    beam_volume = sum(_number(row["volume_m3"]) for row in beams)
    double_count = sum(_number(row["double_count_m3"]) for row in links)
    additions = [row for row in links if row["status"] == "beam-only"]
    addition_volume = sum(_number(row["beam_volume_m3"]) for row in additions)
    leftover_volume = sum(_number(row["volume_m3"]) for row in leftovers)
    matched_beams = [row for row in links if row["status"] != "beam-only"]
    table = _instance_table(runs, links, leftovers)
    unpaired_by_code: dict[str, list[str]] = {}
    for run in leftovers:
        unpaired_by_code.setdefault(run["code_key"], []).append(run["id"])
    claimed_codes = {row["code_key"] for row in links if row["run_ids"]}
    for row in links:
        same_code = unpaired_by_code.get(row["code_key"], [])
        row["unpaired_same_code_run_ids"] = same_code
        if row["status"] != "beam-only":
            row["beam_only_class"] = ""
        elif same_code:
            row["beam_only_class"] = "attribution-conflict"
        elif row["code_key"] in claimed_codes:
            row["beam_only_class"] = "model-extra-instance"
        else:
            row["beam_only_class"] = "code-absent"
    classes = ("attribution-conflict", "model-extra-instance", "code-absent")
    beam_only_class = {
        name: [row for row in links
               if row.get("beam_only_class") == name] for name in classes}
    by_evidence: dict[str, list[float]] = {}
    for run in leftovers:
        entry = by_evidence.setdefault(run["evidence"] or "未记录", [0.0, 0.0])
        entry[0] += 1.0
        entry[1] = _round(entry[1] + _number(run["volume_m3"]))
    by_evidence = {key: [int(value[0]), value[1]]
                   for key, value in sorted(by_evidence.items())}
    real_candidate_volume = sum(_number(row["beam_volume_m3"]) for row
                                in links if row.get("beam_only_class") in (
                                    "model-extra-instance", "code-absent"))
    triage = _triage(leftovers, beams, options)
    self_overlap = _self_overlap(runs, options)
    triage_summary: dict[str, list[float]] = {}
    for row in triage:
        entry = triage_summary.setdefault(row["verdict"], [0.0, 0.0])
        entry[0] += 1.0
        entry[1] = _round(entry[1] + _number(row["volume_m3"]))
    triage_summary = {key: [int(value[0]), value[1]]
                      for key, value in sorted(triage_summary.items())}
    label_backed = [row for row in triage if row["evidence"] in (
        "leader-target", "direct-label", "nearest-label")]
    tolerance = _number(options.get("code_axis_tolerance_mm"), 5000.0)
    return {
        "schema": SCHEMA,
        "rule": ("模型梁轴取网格轴、算量实例 run 轴取边线中轴，两者可差 1.5 m 级，"
                 "因此配对以「同编号 + 同向 + 沿轴重叠达阈值」为主证据，轴距只作约束；"
                 "每根梁只认领覆盖自身长度所需的 run，剩余 run 判为该编号在 CAD 里多出的实例。"
                 "已配对的梁不得再作为新增量并入，只有无 run 可配的梁才是真未提取候选。"),
        "options": {
            "code_axis_tolerance_mm": _round(tolerance, 1),
            "geometry_axis_tolerance_mm": _round(
                options.get("geometry_axis_tolerance_mm", 400.0), 1),
            "min_overlap_ratio": _round(options.get("min_overlap_ratio", 0.5), 2),
            "length_tolerance_mm": _round(
                options.get("length_tolerance_mm", 200.0), 1),
            "self_overlap_axis_tolerance_mm": _round(
                options.get("self_overlap_axis_tolerance_mm", 400.0), 1),
            "gap_tolerance_mm": _round(options.get("gap_tolerance_mm", 400.0), 1),
            "conflict_tolerance_m3": _round(tol),
            "floor_label": _text(options.get("floor_label")),
        },
        "summary": {
            "run_count": len(runs),
            "run_volume_m3": _round(run_volume),
            "beam_count": len(beams),
            "beam_volume_m3": _round(beam_volume),
            "matched_beam_count": len(matched_beams),
            "beam_only_count": len(additions),
            "beam_only_codes": sorted({row["code"] for row in additions}),
            "beam_only_candidate_volume_m3": _round(addition_volume),
            "double_count_volume_m3": _round(double_count),
            "unmatched_run_count": len(leftovers),
            "unmatched_run_volume_m3": _round(leftover_volume),
            "extra_instance_codes": [
                row["code"] for row in table if row["instance_delta"] > 0],
            "beam_only_class_count": {
                name: len(beam_only_class[name]) for name in classes},
            "beam_only_class_volume_m3": {
                name: _round(sum(_number(row["beam_volume_m3"])
                                 for row in beam_only_class[name]))
                for name in classes},
            "model_beam_net_new_volume_m3": _round(real_candidate_volume),
            "run_self_overlap_pair_count": self_overlap["pair_count"],
            "run_self_overlap_volume_m3": self_overlap["overlapped_volume_m3"],
            "unpaired_run_verdict_summary": triage_summary,
            "unpaired_run_volume_by_evidence": by_evidence,
            "unpaired_run_verdict_count": {
                key: int(value[0]) for key, value in triage_summary.items()},
            "unpaired_run_verdict_volume_m3": {
                key: value[1] for key, value in triage_summary.items()},
            "unpaired_run_label_backed_volume_m3": _round(
                sum(_number(row["volume_m3"]) for row in label_backed)),
            "unpaired_run_model_missing": [
                row["run_id"] for row in triage
                if row["verdict"] == "model-missing-instance"],
            "partial_cover_count": sum(
                1 for row in links if row["status"] == "same-instance-partial-cover"),
            "section_conflict_count": sum(
                1 for row in links if row["section_conflict"]),
            "attribution_differs_count": sum(
                1 for row in matched_beams
                if row["code"] and row["run_codes"] and row["code"]
                not in row["run_codes"]),
        },
        "links": [{key: value for key, value in row.items()
                   if key != "code_key"} for row in links],
        "unmatched_runs": [{key: value for key, value in row.items()
                            if key != "code_key"} for row in leftovers],
        "run_self_overlap": self_overlap,
        "instance_table": table,
        "unpaired_run_triage": [{key: value for key, value in row.items()
                                 if key != "code_key"} for row in triage],
        "closure": {"gates": {
            "populations-comparable": bool(runs and beams),
            "all-beams-resolved": bool(links) and len(links) == len(beams),
            "no-silent-double-count": addition_volume <= tol,
            "no-stray-run-instances": leftover_volume <= tol,
            "beam-only-evidence-classified": all(
                row.get("beam_only_class") for row in additions),
            "model-beams-not-additive": real_candidate_volume <= tol,
            "run-population-no-self-overlap": self_overlap["pair_count"] == 0,
        }},
        "formal_ready": False,
        "applied_to_formal_quantity": False,
    }


def csv_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows: list[list[Any]] = [
        ["type", "beam_id", "code", "orientation", "axis_mm", "lo_mm", "hi_mm",
         "beam_len_mm", "beam_vol_m3", "run_ids", "run_codes", "run_len_mm",
         "run_vol_m3", "coverage", "offset_mm", "status", "note"]]
    for row in result["links"]:
        rows.append([
            "link", row["beam_id"], row["code"], row["orientation"],
            row["axis_mm"], row["lo_mm"], row["hi_mm"], row["beam_length_mm"],
            row["beam_volume_m3"], "|".join(row["run_ids"]),
            "|".join(row["run_codes"]), row["run_length_mm"],
            row["run_volume_m3"], row["coverage_ratio"],
            row["axis_offset_max_mm"], row["status"],
            row["evidence"] + ("；" + row.get("beam_only_class", "")
                               if row.get("beam_only_class") else "")
            + ("；同编号未配对 run " + "|".join(
                row.get("unpaired_same_code_run_ids") or [])
               if row.get("unpaired_same_code_run_ids") else "")
            + ("；截面不一致" if row["section_conflict"] else "")
            + (f"；重复计量风险 {row['double_count_m3']:.4f} m3"
               if _number(row["double_count_m3"]) else "")])
    for row in result["unmatched_runs"]:
        rows.append(["run-only", "", row["code"], row["orientation"],
                     row["axis_mm"], row["lo_mm"], row["hi_mm"],
                     row["length_mm"], "", row["id"], row["code"],
                     row["length_mm"], row["volume_m3"], "", "", "run-only",
                     "编号证据 " + (row.get("evidence") or "未记录")
                     + "；CAD 多出实例，模型梁未建，补充前先与梁口径去重"])
    for row in result["unpaired_run_triage"]:
        rows.append(["run-triage", "", row["code"], row["orientation"],
                     row["axis_mm"], row["lo_mm"], row["hi_mm"],
                     row["length_mm"], "", row["run_id"], row["code"],
                     row["length_mm"], row["volume_m3"], "", "",
                     row["verdict"],
                     "相邻模型梁 " + ("|".join(row["continuation_beam_ids"]) or "无")
                     + "；冲突编号 " + ("|".join(row["conflicting_codes"]) or "无")
                     + "；证据 " + (row["evidence"] or "未记录")])
    for row in result["instance_table"]:
        rows.append(["code-delta", "", row["code"], "", "", "", "", "",
                     row["beam_volume_m3"], "|".join(row["extra_run_ids"]), "",
                     "", row["run_volume_m3"], "", "",
                     f"beams={row['beam_count']} runs={row['run_count']}",
                     "实例数差 " + str(row["instance_delta"]) + "；未解释梁 "
                     + ("|".join(row["unresolved_beam_ids"]) or "无")])
    return rows


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    triage_rows = result["unpaired_run_triage"]
    options = result["options"]
    lines = [
        "# 梁实例双口径去重台账",
        "",
        f"- 判定规则：{result['rule']}",
        f"- 参数：编号配对轴距上限 {options['code_axis_tolerance_mm']} mm，"
        f"纯几何配对轴距上限 {options['geometry_axis_tolerance_mm']} mm，"
        f"沿轴重叠下限 {options['min_overlap_ratio']}（按较短者），"
        f"长度容差 {options['length_tolerance_mm']} mm、"
        f"续接端头间隙 {options['gap_tolerance_mm']} mm、"
        f"run 自扫描同轴容差 "
        f"{options['self_overlap_axis_tolerance_mm']} mm。",
        "",
        "| 口径 | 实例数 | 体积m3 |",
        "|---|---:|---:|",
        f"| 算量实例 run_registry | {summary['run_count']} | "
        f"{summary['run_volume_m3']:.4f} |",
        f"| 模型梁 members.beams | {summary['beam_count']} | "
        f"{summary['beam_volume_m3']:.4f} |",
        "",
        f"- 判为同一根物理梁 {summary['matched_beam_count']} 根，"
        f"两套口径相加会重复计量 **{summary['double_count_volume_m3']:.4f} m3**；"
        f"无 run 可配的模型梁 {summary['beam_only_count']} 根/"
        f"{summary['beam_only_candidate_volume_m3']:.4f} m3。",
        f"- CAD 侧多出的 run {summary['unmatched_run_count']} 条/"
        f"{summary['unmatched_run_volume_m3']:.4f} m3；"
        f"部分覆盖 {summary['partial_cover_count']} 根；"
        f"截面不一致 {summary['section_conflict_count']} 处；"
        f"编号归属不一致 {summary['attribution_differs_count']} 处。",
        "",
        "## 模型梁口径净新增",
        "",
        "把无 run 可配的模型梁按证据分三类，只有后两类才是候选新增：",
        "",
        "| 分类 | 根数 | 体积m3 | 含义 |",
        "|---|---:|---:|---|",
    ]
    meaning = {
        "attribution-conflict": "同编号在 CAD 里有未配对 run，只是位置或方向不符，"
                                "属归属冲突，不得当新增量",
        "model-extra-instance": "该编号其余实例已被 run 配对，模型梁多出一根，"
                                "需回原图复核几何",
        "code-absent": "run 口径完全没有该编号，才是真未提取候选",
    }
    for name in ("attribution-conflict", "model-extra-instance", "code-absent"):
        lines.append(
            f"| `{name}` | {summary['beam_only_class_count'][name]} | "
            f"{summary['beam_only_class_volume_m3'][name]:.4f} | {meaning[name]} |")
    lines += [
        "",
        f"因此模型梁口径的净新增候选只有 "
        f"**{summary['model_beam_net_new_volume_m3']:.4f} m3**。统一分账按 run 口径"
        f"计量梁，两套口径不得相加。",
        "",
        "## 未配对 run 的编号证据分层",
        "",
        "| 编号证据 | 条数 | 体积m3 |",
        "|---|---:|---:|",
    ]
    for key, value in summary["unpaired_run_volume_by_evidence"].items():
        lines.append(f"| {key} | {value[0]} | {value[1]:.4f} |")
    lines += [
        "",
        "## 实例数对账（按编号）",
        "",
        "| 编号 | 模型梁数 | run 数 | 实例差 | 梁体积m3 | run 体积m3 | 多出 run |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in result["instance_table"]:
        if not row["instance_delta"] and not row["unresolved_beam_ids"]:
            continue
        lines.append(
            f"| {row['code']} | {row['beam_count']} | {row['run_count']} | "
            f"{row['instance_delta']:+d} | {row['beam_volume_m3']:.4f} | "
            f"{row['run_volume_m3']:.4f} | "
            f"{', '.join(row['extra_run_ids']) or '—'} |")
    lines += [
        "",
        "## run 口径内部重叠扫描",
        "",
        f"- 同轴容差 {result['options']['self_overlap_axis_tolerance_mm']} mm 内，"
        f"重叠 {result['run_self_overlap']['pair_count']} 处/"
        f"{result['run_self_overlap']['overlap_length_mm']:.1f} mm，"
        f"潜在重复计量 "
        f"**{result['run_self_overlap']['overlapped_volume_m3']:.4f} m3**"
        "（0 处即 run 口径内部无重复计量，统一分账的梁量基数可信）。",
        "",
        "## 未配对 run 定责",
        "",
        "| 判定 | 条数 | 体积m3 | 含义 |",
        "|---|---:|---:|---|",
    ]
    verdict_meaning = {
        "continuation-candidate": "端头与同编号模型梁相邻，是该梁的续接段，不是新实例",
        "attribution-conflict": "同一位置模型梁挂的是别的编号，归属冲突需回图定谁对",
        "same-code-other-location": "同编号模型梁在别处，此实例位置模型未建",
        "model-missing-instance": "该位置没有任何模型梁，才是可能缺的实例",
    }
    for key in ("continuation-candidate", "attribution-conflict",
                "same-code-other-location", "model-missing-instance"):
        count = summary["unpaired_run_verdict_count"].get(key, 0)
        volume = summary["unpaired_run_verdict_volume_m3"].get(key, 0.0)
        lines.append(f"| `{key}` | {count} | {volume:.4f} | {verdict_meaning[key]} |")
    lines += [
        "",
        f"其中带引线或标注证据的未配对 run 合计 "
        f"**{summary['unpaired_run_label_backed_volume_m3']:.4f} m3**，"
        f"模型缺实例候选 {len(summary['unpaired_run_model_missing'])} 条"
        f"（{', '.join(summary['unpaired_run_model_missing']) or '无'}）。",
        "",
        "| run | 编号 | 向 | 区间mm | 体积m3 | 证据 | 判定 | 相邻模型梁 | 冲突编号 |",
        "|---|---|---|---|---:|---|---|---|---|",
    ]
    for row in triage_rows:
        lines.append(
            f"| {row['run_id']} | {row['code'] or '未归属'} | {row['orientation']} | "
            f"{row['lo_mm']:.0f}→{row['hi_mm']:.0f} | {row['volume_m3']:.4f} | "
            f"{row['evidence'] or '未记录'} | {row['verdict']} | "
            f"{', '.join(row['continuation_beam_ids']) or '—'} | "
            f"{', '.join(row['conflicting_codes']) or '—'} |")
    lines += [
        "",
        "## 逐根配对结果",
        "",
        "| 模型梁 | 编号 | 向 | 轴mm | 区间mm | 梁体积m3 | 配对 run | run 体积m3 | 覆盖 | 轴偏mm | 状态 | 分类 |",
        "|---|---|---|---:|---|---:|---|---:|---:|---:|---|---|",
    ]
    for row in result["links"]:
        lines.append(
            f"| {row['beam_id']} | {row['code']} | {row['orientation']} | "
            f"{row['axis_mm']:.1f} | {row['lo_mm']:.0f}→{row['hi_mm']:.0f} | "
            f"{row['beam_volume_m3']:.4f} | "
            f"{', '.join(row['run_ids']) or '—'} | "
            f"{row['run_volume_m3']:.4f} | {row['coverage_ratio']:.2f} | "
            f"{row['axis_offset_max_mm']:.1f} | {row['status']} | "
            f"{row.get('beam_only_class') or '—'} |")
    lines += [
        "",
        "## 未配对的 CAD 实例 run",
        "",
        "| run | 编号 | 向 | 轴mm | 区间mm | 长mm | 体积m3 | 编号证据 |",
        "|---|---|---|---:|---|---:|---:|---|",
    ]
    for row in result["unmatched_runs"]:
        lines.append(
            f"| {row['id']} | {row['code'] or '未归属'} | {row['orientation']} | "
            f"{row['axis_mm']:.1f} | {row['lo_mm']:.0f}→{row['hi_mm']:.0f} | "
            f"{row['length_mm']:.0f} | {row['volume_m3']:.4f} | "
            f"{row.get('evidence') or '未记录'} |")
    lines += [
        "",
        "## 门槛",
        "",
        "- `" + json.dumps(result["closure"]["gates"], ensure_ascii=False) + "`",
        "- 本表只判重复计量与实例归属，不改任何构件体积，"
        "`applied_to_formal_quantity=false`、`formal_ready=false`。",
    ]
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="梁实例双口径去重")
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--code-axis-tolerance-mm", type=float, default=5000.0,
                        help="同编号配对允许的模型梁轴与 run 边线中轴最大偏差")
    parser.add_argument("--geometry-axis-tolerance-mm", type=float, default=400.0,
                        help="无编号 run 纯几何配对允许的轴距偏差")
    parser.add_argument("--min-overlap-ratio", type=float, default=0.5,
                        help="沿轴重叠占较短者的最小比例")
    parser.add_argument("--length-tolerance-mm", type=float, default=200.0)
    parser.add_argument("--self-overlap-axis-tolerance-mm", type=float,
                        default=400.0, help="run 口径内部重叠扫描的同轴容差")
    parser.add_argument("--gap-tolerance-mm", type=float, default=400.0,
                        help="判定同编号续接段允许的最大端头间隙")
    parser.add_argument("--conflict-tolerance-m3", type=float, default=0.05)
    parser.add_argument("--floor-label", default=None)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()
    path = Path(args.model_json)
    if not path.exists():
        parser.error(f"缺少输入：{path}")
    result = build_dedup(json.loads(path.read_text(encoding="utf-8")), {
        "code_axis_tolerance_mm": args.code_axis_tolerance_mm,
        "geometry_axis_tolerance_mm": args.geometry_axis_tolerance_mm,
        "min_overlap_ratio": args.min_overlap_ratio,
        "length_tolerance_mm": args.length_tolerance_mm,
        "gap_tolerance_mm": args.gap_tolerance_mm,
        "self_overlap_axis_tolerance_mm": args.self_overlap_axis_tolerance_mm,
        "conflict_tolerance_m3": args.conflict_tolerance_m3,
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
    out.with_name(out.name + ".sha256").write_text("\n".join(
        f"{sha256(path)}  {path.resolve()}"
        for path in (json_path, csv_path, md_path)) + "\n", encoding="utf-8")
    print(json.dumps({"schema": result["schema"], "summary": result["summary"],
                      "gates": result["closure"]["gates"],
                      "formal_ready": result["formal_ready"]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
