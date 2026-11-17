#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""同轴同截面但编号不同的梁段与模型梁逐对定责，用图面引线标注判谁对。"""



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


SCHEMA = "cad-beam-attribution-conflict/v0.1"
CODE_SUFFIX = re.compile(r"[\(\uff08][0-9]+[\)\uff09]$")



def _base(value: Any) -> str:
    """KL13A(1) 与 WKL4 都归一到不带跨数的底编号。"""
    text = CODE_SUFFIX.sub("", _text(value).strip().upper().replace(" ", ""))
    return text


def _overlap(first: tuple, second: tuple) -> float:
    return max(0.0, min(first[1], second[1]) - max(first[0], second[0]))


def _leaders(model: dict[str, Any]) -> list[dict[str, Any]]:
    registry = model.get("run_registry") or {}
    codes = registry.get("leader_codes") or {}
    rows: list[dict[str, Any]] = []
    for leader_id, target in (registry.get("leader_targets") or {}).items():
        raw = [CODE_SUFFIX.sub("", _text(code).upper())
               for code in (codes.get(leader_id) or [])]
        rows.append({
            "id": _text(leader_id),
            "codes": sorted({code for code in raw if code}),
            "orientation": _text(target.get("orientation")),
            "axis_mm": _round(_number(target.get("axis_mm")), 1),
            "x_mm": _round(_number(target.get("x")), 1),
            "y_mm": _round(_number(target.get("y")), 1),
            "target_lo_mm": _round(min(_number(target.get("start_mm")),
                                       _number(target.get("end_mm"))), 1),
            "target_hi_mm": _round(max(_number(target.get("start_mm")),
                                       _number(target.get("end_mm"))), 1),
        })
    return rows


def _segments(model: dict[str, Any]) -> tuple[list[dict[str, Any]],
                                              list[dict[str, Any]]]:
    runs: list[dict[str, Any]] = []
    for run in (model.get("run_registry") or {}).get("runs") or []:
        lo, hi = sorted((_number(run.get("start_mm")), _number(run.get("end_mm"))))
        runs.append({
            "id": _text(run.get("id")), "code": _text(run.get("matched_code")),
            "base": _base(run.get("matched_code")),
            "orientation": _text(run.get("orientation")),
            "axis_mm": _round(_number(run.get("axis_mm")), 1),
            "lo_mm": _round(lo, 1), "hi_mm": _round(hi, 1),
            "length_mm": _round(hi - lo, 1), "section": _text(run.get("section")),
            "volume_m3": _round(run.get("volume_m3")),
            "leader_id": _text(run.get("matched_leader_id")),
            "evidence": _text(run.get("code_assignment_status")),
        })
    beams: list[dict[str, Any]] = []
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
        beams.append({
            "id": _text(beam.get("id")), "code": _text(beam.get("code")),
            "base": _base(beam.get("base_code") or beam.get("code")),
            "orientation": orientation, "axis_mm": _round(axis, 1),
            "lo_mm": _round(lo, 1), "hi_mm": _round(hi, 1),
            "length_mm": _round(hi - lo, 1), "section": _text(beam.get("section")),
            "volume_m3": _round(beam.get("gross_volume_m3")),
            "quantity_status": _text(beam.get("quantity_status")),
            "axis_offset_mm": _round(centerline.get("axis_offset_mm"), 1),
        })
    return runs, beams


def _labels_on(axis_mm: float, lo_mm: float, hi_mm: float, orientation: str,
               leaders: list[dict[str, Any]],
               tolerance: float) -> list[dict[str, Any]]:
    """落在给定线段范围内的引线标注，并按轴距最近判置信度。"""
    hits: list[dict[str, Any]] = []
    for leader in leaders:
        if leader["orientation"] != orientation:
            continue
        offset = abs(leader["axis_mm"] - axis_mm)
        if offset > tolerance:
            continue
        point = leader["y_mm"] if orientation == "V" else leader["x_mm"]
        if lo_mm - 1.0 <= point <= hi_mm + 1.0:
            entry = dict(leader)
            entry["axis_offset_mm"] = _round(offset, 1)
            hits.append(entry)
    return hits


def _attested(code: str, hits: list[dict[str, Any]],
              leader_id: str) -> tuple[bool, float, dict[str, Any] | None]:
    """该底编号是否有引线落在这段线上，返回（是否成立，最近轴距 mm，引线）。"""
    best: dict[str, Any] | None = None
    for leader in hits:
        if code not in leader["codes"] and leader["id"] != leader_id:
            continue
        if best is None or _number(leader["axis_offset_mm"]) < _number(
                best["axis_offset_mm"]):
            best = leader
    if best is None:
        return False, -1.0, None
    return True, _number(best["axis_offset_mm"]), best


def _apply_ownership(conflicts: list[dict[str, Any]]) -> None:
    """逐对定主：引线目标落在这条绘制线上的那侧成立，只搬编号归属不搬几何。

    判不了的老实留 open，给坐标与区间，不改总量。
    """
    for row in conflicts:
        risk = _number(row["double_count_risk_m3"])
        verdict = row["verdict"]
        if verdict == "parallel-distinct-lines":
            owner = {"kind": "both", "code": "", "rule": "distinct-drawn-lines",
                     "status": "resolved-separate-lines", "transfer_m3": 0.0,
                     "residual_risk_m3": 0.0}
        elif verdict == "run-label-holds":
            owner = {"kind": "run", "code": row["run_code"],
                     "rule": "leader-target-on-this-line",
                     "status": "owner-decided", "transfer_m3": risk,
                     "residual_risk_m3": 0.0}
        elif verdict == "beam-label-holds":
            owner = {"kind": "beam", "code": row["beam_code"],
                     "rule": "beam-label-attests-this-segment",
                     "status": "owner-decided", "transfer_m3": risk,
                     "residual_risk_m3": 0.0}
        elif verdict == "same-line-different-spans":
            owner = {"kind": "split", "code": "",
                     "rule": "labels-cover-different-spans",
                     "status": "review-open", "transfer_m3": 0.0,
                     "residual_risk_m3": risk,
                     "open_interval_mm": list(row["span_split_interval_mm"])}
        elif verdict == "dual-label-same-line":
            owner = {"kind": "unknown", "code": "",
                     "rule": "two-leaders-both-target-this-line",
                     "status": "review-open", "transfer_m3": 0.0,
                     "residual_risk_m3": risk}
        else:
            owner = {"kind": "unknown", "code": "", "rule": "no-label-evidence",
                     "status": "review-open", "transfer_m3": 0.0,
                     "residual_risk_m3": risk}
        row["ownership"] = owner
        if owner["kind"] == "run":
            row["loser_code"] = row["beam_code"]
        elif owner["kind"] == "beam":
            row["loser_code"] = row["run_code"]
        else:
            row["loser_code"] = ""


def adjudicate(model: dict[str, Any],
               options: dict[str, Any]) -> dict[str, Any]:
    runs, beams = _segments(model)
    leaders = _leaders(model)
    tolerance = _number(options.get("conflict_axis_tolerance_mm"), 2500.0)
    min_overlap = _number(options.get("min_overlap_ratio"), 0.5)
    conflicts: list[dict[str, Any]] = []
    for run in runs:
        for beam in beams:
            if run["orientation"] != beam["orientation"]:
                continue
            if not run["base"] or not beam["base"] or run["base"] == beam["base"]:
                continue
            offset = abs(run["axis_mm"] - beam["axis_mm"])
            if offset > tolerance:
                continue
            shortest = min(run["length_mm"], beam["length_mm"])
            shared = _overlap((run["lo_mm"], run["hi_mm"]),
                              (beam["lo_mm"], beam["hi_mm"]))
            if shortest <= 0.0 or shared < min_overlap * shortest:
                continue
            require_section = bool(options.get("require_same_section", True))
            if require_section and run["section"] != beam["section"]:
                continue
            # 引线按两条几何的并集范围取证，再用两侧引线的 target 轴判是否同一条线
            ov_lo, ov_hi = max(run["lo_mm"], beam["lo_mm"]), min(
                run["hi_mm"], beam["hi_mm"])
            un_lo, un_hi = min(run["lo_mm"], beam["lo_mm"]), max(
                run["hi_mm"], beam["hi_mm"])
            run_labels = _labels_on(run["axis_mm"], un_lo, un_hi,
                                    run["orientation"], leaders, tolerance)
            beam_labels = _labels_on(beam["axis_mm"], un_lo, un_hi,
                                     beam["orientation"], leaders, tolerance)
            label_ids = sorted({leader["id"] for leader in
                                (run_labels + beam_labels)})
            label_codes = sorted({code for leader in (run_labels + beam_labels)
                                  for code in leader["codes"]})
            run_holds, run_label_offset, run_leader = _attested(
                run["base"], run_labels, run["leader_id"])
            beam_holds, beam_label_offset, beam_leader = _attested(
                beam["base"], beam_labels, "")
            label_offsets = [value for value in (run_label_offset,
                                                 beam_label_offset)
                             if value >= 0.0]
            if run_leader is not None and beam_leader is not None:
                pair_axis_gap = abs(_number(run_leader["axis_mm"]) - _number(
                    beam_leader["axis_mm"]))
                same_line = pair_axis_gap <= _number(
                    options.get("same_line_label_axis_tolerance_mm"), 200.0)
            else:
                pair_axis_gap = offset
                same_line = offset <= _number(
                    options.get("same_line_max_axis_offset_mm"), 1200.0)
            split_interval: list[float] = []
            if same_line and run_leader is not None and beam_leader is not None:
                lower, upper = sorted((run_leader, beam_leader),
                                       key=lambda item: _number(item["target_lo_mm"]))
                gap_mm = _number(upper["target_lo_mm"]) - _number(
                    lower["target_hi_mm"])
                if gap_mm >= _number(options.get("span_split_min_gap_mm"), 200.0):
                    split_interval = [_number(lower["target_hi_mm"]),
                                      _number(upper["target_lo_mm"])]
            confidence = "near" if (
                not label_offsets or max(label_offsets) > _number(
                    options.get("strong_label_axis_tolerance_mm"), 1000.0)
                ) else "strong"
            if not same_line:
                verdict = "parallel-distinct-lines"
            elif split_interval:
                verdict = "same-line-different-spans"
            elif run_holds and beam_holds:
                verdict = "dual-label-same-line"
            elif run_holds:
                verdict = "run-label-holds"
            elif beam_holds:
                verdict = "beam-label-holds"
            else:
                verdict = "no-label-evidence"
            overlap_ratio = _round(shared / (abs(shortest) or 1.0), 3)
            conflicts.append({
                "run_id": run["id"], "run_code": run["code"],
                "run_leader_id": run["leader_id"],
                "run_evidence": run["evidence"],
                "run_section": run["section"],
                "run_axis_mm": run["axis_mm"],
                "run_interval_mm": [run["lo_mm"], run["hi_mm"]],
                "run_volume_m3": run["volume_m3"],
                "beam_id": beam["id"], "beam_code": beam["code"],
                "beam_section": beam["section"],
                "beam_axis_mm": beam["axis_mm"],
                "beam_interval_mm": [beam["lo_mm"], beam["hi_mm"]],
                "beam_volume_m3": beam["volume_m3"],
                "beam_quantity_status": beam["quantity_status"],
                "orientation": run["orientation"],
                "axis_offset_mm": _round(offset, 1),
                "overlap_mm": _round(shared, 1),
                "overlap_ratio": overlap_ratio,
                "same_axis": offset <= 1.0,
                "label_leader_ids": label_ids,
                "label_codes": label_codes,
                "label_axis_offset_mm": _round(
                    max(label_offsets) if label_offsets else 0.0, 1),
                "confidence": confidence,
                "review_xy": [run["axis_mm"] if run["orientation"] == "V" else
                              _round((run["lo_mm"] + run["hi_mm"]) / 2.0, 1),
                              run["lo_mm"] if run["orientation"] == "V" else
                              run["axis_mm"]],
                "verdict": verdict,
                "same_line": bool(same_line),
                "label_pair_axis_gap_mm": _round(pair_axis_gap, 1),
                "span_split_interval_mm": [_round(value, 1)
                                           for value in split_interval],
                "double_count_risk_m3": 0.0 if not same_line else _round(
                    min(run["volume_m3"], beam["volume_m3"])
                    * min(overlap_ratio, 1.0)),
            })
    conflicts.sort(key=lambda row: (-_number(row["double_count_risk_m3"]),
                                    row["run_id"], row["beam_id"]))
    _apply_ownership(conflicts)
    verdicts: dict[str, list[float]] = {}
    confidence_counts: dict[str, int] = {}
    for row in conflicts:
        confidence_counts[row["confidence"]] = confidence_counts.get(
            row["confidence"], 0) + 1
        entry = verdicts.setdefault(row["verdict"], [0.0, 0.0, 0.0])
        entry[0] += 1.0
        entry[1] = _round(entry[1] + _number(row["double_count_risk_m3"]))
        entry[2] = _round(entry[2] + _number(row["run_volume_m3"]))
    verdict_summary = {
        key: {"pair_count": int(value[0]), "double_count_risk_m3": value[1],
              "run_volume_m3": value[2]}
        for key, value in sorted(verdicts.items())}
    total_risk = _round(sum(_number(row["double_count_risk_m3"])
                            for row in conflicts))
    ownership_counts: dict[str, int] = {}
    shift: dict[str, float] = {}
    transfer_total = 0.0
    transfer_in = 0.0
    transfer_out = 0.0
    closed_risk = 0.0
    open_risk = 0.0
    for row in conflicts:
        owner = dict(row.get("ownership") or {})
        status = _text(owner.get("status"))
        ownership_counts[status] = ownership_counts.get(status, 0) + 1
        moved = _number(owner.get("transfer_m3"))
        transfer_total += moved
        if status == "owner-decided":
            closed_risk += moved
            winner = _text(owner.get("code"))
            loser = _text(row.get("loser_code"))
            shift[winner] = shift.get(winner, 0.0) + moved
            shift[loser] = shift.get(loser, 0.0) - moved
            transfer_in += moved
            transfer_out += moved
        else:
            open_risk += _number(row["double_count_risk_m3"])
    ownership_closed = ownership_counts.get("review-open", 0) == 0
    balance_residual = sum(shift.values())
    return {
        "schema": SCHEMA,
        "rule": ("先用几何找候选对（同向、同截面、轴距不超过容差、沿轴重叠达阈值且底编号不同），"
                 "再用两侧引线的 target 轴判是否同一条绘制线：轴差不超过容差才算同轴冲突，"
                 "否则判 parallel-distinct-lines（平行邻线，不计重复计量风险）。"
                 "同轴冲突里两侧引线目标区间首尾分开判 same-line-different-spans"
                 "（成链未在支座断开）；区间仍重叠则两侧都有标注判 dual-label-same-line、"
                 "单侧有标注该侧成立、都无标注判 no-label-evidence。"),
        "options": {
            "conflict_axis_tolerance_mm": _round(tolerance, 1),
            "min_overlap_ratio": _round(min_overlap, 2),
            "same_line_label_axis_tolerance_mm": _round(
                options.get("same_line_label_axis_tolerance_mm", 200.0), 1),
            "same_line_max_axis_offset_mm": _round(
                options.get("same_line_max_axis_offset_mm", 1200.0), 1),
            "span_split_min_gap_mm": _round(
                options.get("span_split_min_gap_mm", 200.0), 1),
            "require_same_section": bool(options.get("require_same_section", True)),
            "strong_label_axis_tolerance_mm": _round(
                options.get("strong_label_axis_tolerance_mm", 1000.0), 1),
            "floor_label": _text(options.get("floor_label")),
        },
        "summary": {
            "run_count": len(runs), "beam_count": len(beams),
            "leader_count": len(leaders),
            "conflict_pair_count": len(conflicts),
            "conflict_run_count": len({row["run_id"] for row in conflicts}),
            "conflict_beam_count": len({row["beam_id"] for row in conflicts}),
            "same_axis_pair_count": sum(1 for row in conflicts if row["same_axis"]),
            "same_line_pair_count": sum(1 for row in conflicts if row["same_line"]),
            "parallel_pair_count": sum(1 for row in conflicts
                                       if not row["same_line"]),
            "double_count_risk_m3": total_risk,
            "label_confidence_counts": confidence_counts,
            "conflict_run_volume_m3": _round(sum(
                _number(row["run_volume_m3"]) for row in conflicts)),
            "conflict_beam_volume_m3": _round(sum(
                _number(row["beam_volume_m3"]) for row in conflicts)),
            "verdicts": verdict_summary,
            "ownership_status_counts": ownership_counts,
            "ownership_decided_pair_count": ownership_counts.get(
                "owner-decided", 0),
            "ownership_open_pair_count": ownership_counts.get("review-open", 0),
            "attribution_transfer_m3": _round(transfer_total),
            "attribution_balance_residual_m3": _round(
                sum(shift.values()) + transfer_out - transfer_in, 6),
            "code_attribution_shift": [
                {"code": code, "shift_m3": _round(value)}
                for code, value in sorted(shift.items(),
                                          key=lambda item: (-abs(item[1]), item[0]))],
            "closed_double_count_risk_m3": _round(closed_risk),
            "residual_double_count_risk_m3": _round(open_risk),
        },
        "conflicts": conflicts,
        "closure": {"gates": {
            "conflicts-and-labels-present": bool(conflicts) and bool(leaders),
            "no-unadjudicated-dual-label": int(
                (verdict_summary.get("dual-label-same-line")
                 or {}).get("pair_count") or 0) == 0,
            "all-conflicts-classified": all(
                row["verdict"] for row in conflicts),
            "applied-to-formal-quantity": False,
            "conflict-ownership-transfer-balanced": abs(balance_residual) <= 1e-6,
            "conflict-ownership-closed": ownership_closed,
        }},
        "formal_ready": False,
        "applied_to_formal_quantity": False,
    }


def csv_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows: list[list[Any]] = [
        ["type", "run", "run编号", "run证据", "模型梁", "梁编号", "向",
         "轴偏mm", "重叠mm", "重叠比", "run体积m3", "梁体积m3",
         "重复计量风险m3", "线上标注", "判定", "回图坐标",
         "归属主", "编号转移m3", "归属后剩余风险m3", "归属依据"]]
    for row in result["conflicts"]:
        rows.append([
            "conflict", row["run_id"], row["run_code"], row["run_evidence"],
            row["beam_id"], row["beam_code"], row["orientation"],
            row["axis_offset_mm"], row["overlap_mm"], row["overlap_ratio"],
            row["run_volume_m3"], row["beam_volume_m3"],
            row["double_count_risk_m3"], "|".join(row["label_leader_ids"]),
            row["verdict"], f'{row["review_xy"][0]:.1f},{row["review_xy"][1]:.1f}',
            _text((row.get("ownership") or {}).get("code")) or _text(
                (row.get("ownership") or {}).get("status")),
            (row.get("ownership") or {}).get("transfer_m3"),
            (row.get("ownership") or {}).get("residual_risk_m3"),
            _text((row.get("ownership") or {}).get("rule"))])
    for key, value in result["summary"]["verdicts"].items():
        rows.append(["verdict", "", key, "", "", "", "", "", "", "",
                     value["run_volume_m3"], "", value["double_count_risk_m3"],
                     "", f'{value["pair_count"]} 对', ""])
    summ = result["summary"]
    rows += [["", "", ""],
             ["ownership", "", "已定主对数", "", "", "", "", "", "", "", "", "",
              summ["attribution_transfer_m3"], "",
              f'{summ["ownership_decided_pair_count"]} 对', "", "", "",
              summ["closed_double_count_risk_m3"], ""],
             ["ownership", "", "仍需复核对数", "", "", "", "", "", "", "", "", "",
              0.0, "", f'{summ["ownership_open_pair_count"]} 对', "", "", "",
              summ["residual_double_count_risk_m3"], ""],
             ["ownership", "", "转移对平残差", "", "", "", "", "", "", "", "", "",
              summ["attribution_balance_residual_m3"], "", "应为 0", ""]]
    for row in summ["code_attribution_shift"]:
        rows.append(["code-shift", "", row["code"], "", "", "", "", "", "", "", "",
                     "", row["shift_m3"], "", "只改编号归属", ""])
    return rows


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# 梁编号归属冲突定责台账",
        "",
        f"- 判定规则：{result['rule']}",
        f"- 参数：冲突轴距上限 {result['options']['conflict_axis_tolerance_mm']} mm，"
        f"沿轴重叠下限 {result['options']['min_overlap_ratio']}（按较短者），"
        f"{'要求同截面' if result['options']['require_same_section'] else '不要求同截面'}，"
        f"高置信引线轴距 ≤{result['options']['strong_label_axis_tolerance_mm']} mm；"
        f"图面引线标注 {summary['leader_count']} 条。",
        "",
        f"- {summary['run_count']} 条算量实例与 {summary['beam_count']} 根模型梁里，"
        f"编号冲突 {summary['conflict_pair_count']} 对，涉及 run "
        f"{summary['conflict_run_count']} 条、模型梁 "
        f"{summary['conflict_beam_count']} 根；同轴完全重合 "
        f"{summary['same_axis_pair_count']} 对；"
        f"若两侧都计入分账的重复计量风险 **{summary['double_count_risk_m3']:.4f} m3**。",
        "",
        f"- 引线证据置信度：{json.dumps(summary['label_confidence_counts'], ensure_ascii=False)}。",
        "",
        "| 判定 | 对数 | run 体积m3 | 重复计量风险m3 |",
        "|---|---:|---:|---:|",
    ]
    meaning = {
        "parallel-distinct-lines": "两侧引线各自指向自己的轴，是平行邻线不是同轴冲突，不计风险",
        "same-line-different-spans": "同一条绘制线上首尾相接的两构件，算量实例成链未在支座断开",
        "dual-label-same-line": "两侧编号都有引线指向同一条线，图纸同轴两构件，必须人工定跨",
        "run-label-holds": "只有 run 的编号被标注指向该线，模型梁编号错挂",
        "beam-label-holds": "只有模型梁的编号被标注指向该线，run 编号错挂",
        "no-label-evidence": "两侧编号都无标注落在该线上，属推定冲突",
    }
    for key, value in summary["verdicts"].items():
        lines.append(f"| `{key}` | {value['pair_count']} | "
                     f"{value['run_volume_m3']:.4f} | "
                     f"{value['double_count_risk_m3']:.4f} |")
    lines += [
        "",
        "含义（判定）：",
        "",
    ]
    for key, value in summary["verdicts"].items():
        lines.append(f"- `{key}`：{meaning.get(key, '未登记')}")
    lines += [
        "",
        "## 归属判定（只搬编号归属，不搬几何）",
        "",
        f"- 已定主 {summary['ownership_decided_pair_count']} 对、"
        f"仍需复核 {summary['ownership_open_pair_count']} 对；"
        f"归属后风险由 {summary['double_count_risk_m3']:.4f} m3 收到 "
        f"**{summary['residual_double_count_risk_m3']:.4f} m3**"
        f"（已定主部分 {summary['closed_double_count_risk_m3']:.4f} m3 只改编号归属）。",
        f"- 编号转移合计 {summary['attribution_transfer_m3']:.4f} m3，"
        f"移进与移出对平残差 `{summary['attribution_balance_residual_m3']}`"
        f"（必须为 0，非 0 说明归属层动了总量）。",
        "",
        "| 编号 | 归属净增减 m3 | 说明 |",
        "|---|---:|---|",
    ]
    for row in summary["code_attribution_shift"]:
        lines.append(f"| {row['code']} | {row['shift_m3']:+.4f} | "
                     f"{'标注指向该编号，接收重叠段' if row['shift_m3'] > 0 else '错挂方，让出重叠段'} |")
    lines += [
        "",
        "## 逐对清单",
        "",
        "| run | run编号 | 证据 | 模型梁 | 梁编号 | 向 | 轴偏mm | 重叠mm | 线上标注 | 判定 | 风险m3 | 归属主 | 剩余风险m3 | 回图坐标 |",
        "|---|---|---|---|---|---|---:|---:|---|---|---:|---|---:|---|",
    ]
    for row in result["conflicts"]:
        lines.append(
            f"| {row['run_id']} | {row['run_code']} | {row['run_evidence']} | "
            f"{row['beam_id']} | {row['beam_code']} | {row['orientation']} | "
            f"{row['axis_offset_mm']:.1f} | {row['overlap_mm']:.0f} | "
            f"{', '.join(row['label_leader_ids']) or '无'} | {row['verdict']} | "
            f"{row['double_count_risk_m3']:.4f} | "
            f"{_text((row.get('ownership') or {}).get('code')) or _text((row.get('ownership') or {}).get('status'))} | "
            f"{_number((row.get('ownership') or {}).get('residual_risk_m3')):.4f} | "
            f"{row['review_xy'][0]:.1f}, {row['review_xy'][1]:.1f} |")
    lines += [
        "",
        "## 门槛",
        "",
        "- `" + json.dumps(result["closure"]["gates"], ensure_ascii=False) + "`",
        "- 本表只定编号归属，不改任何构件体积，"
        "`applied_to_formal_quantity=false`、`formal_ready=false`。",
    ]
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="梁编号归属冲突定责")
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--conflict-axis-tolerance-mm", type=float, default=2500.0)
    parser.add_argument("--min-overlap-ratio", type=float, default=0.5)
    parser.add_argument("--same-line-label-axis-tolerance-mm", type=float,
                        default=200.0,
                        help="两侧引线的 target 轴差在此内才算同一条绘制线")
    parser.add_argument("--same-line-max-axis-offset-mm", type=float,
                        default=1200.0,
                        help="缺引线证据时允许的最大几何轴距")
    parser.add_argument("--span-split-min-gap-mm", type=float, default=200.0,
                        help="两侧引线目标区间之间的最小间隙，判同线异跨")
    parser.add_argument("--strong-label-axis-tolerance-mm", type=float,
                        default=1000.0,
                        help="判高置信标注证据允许的引线轴距")
    parser.add_argument("--any-section", action="store_true",
                        help="不要求同截面，扩大冲突检出范围")
    parser.add_argument("--floor-label", default=None)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()
    path = Path(args.model_json)
    if not path.exists():
        parser.error(f"缺少输入：{path}")
    result = adjudicate(json.loads(path.read_text(encoding="utf-8")), {
        "conflict_axis_tolerance_mm": args.conflict_axis_tolerance_mm,
        "min_overlap_ratio": args.min_overlap_ratio,
        "same_line_label_axis_tolerance_mm": args.same_line_label_axis_tolerance_mm,
        "same_line_max_axis_offset_mm": args.same_line_max_axis_offset_mm,
        "span_split_min_gap_mm": args.span_split_min_gap_mm,
        "require_same_section": not args.any_section,
        "strong_label_axis_tolerance_mm": args.strong_label_axis_tolerance_mm,
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
    print(json.dumps({"schema": result["schema"],
                      "summary": result["summary"],
                      "gates": result["closure"]["gates"],
                      "formal_ready": result["formal_ready"]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
