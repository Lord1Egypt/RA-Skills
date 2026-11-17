#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对账梁净跨口径与支座扣减，判定偏少编号的长度差是支座推定还是真缺几何。"""



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
from collections import defaultdict
from pathlib import Path
from typing import Any


SCHEMA = "cad-beam-span-closure/v0.1"



def _code_key(value: Any) -> str:
    return _text(value).replace(" ", "").upper()


def _beams_by_code(model: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for beam in (model.get("members") or {}).get("beams") or []:
        code = _text(beam.get("code"))
        if code:
            grouped[_code_key(code)].append(beam)
    return grouped


def _end_evidence(beam: dict[str, Any]) -> dict[str, Any]:
    """汇总一根梁两端的支座证据类型与推定宽度。"""
    kinds: list[str] = []
    inferred_width = 0.0
    inferred_sides: list[str] = []
    for item in beam.get("support_evidence") or []:
        if not isinstance(item, dict):
            continue
        kind = _text(item.get("type")) or "unknown"
        side = _text(item.get("side"))
        kinds.append(f"{kind}:{side}" if side else kind)
    for item in beam.get("inferred_end_supports") or []:
        if not isinstance(item, dict):
            continue
        inferred_width += _number(item.get("assumed_width_mm"))
        inferred_sides.append(_text(item.get("side")) or "?")
    selection = beam.get("support_selection") or {}
    return {
        "evidence_kinds": sorted(set(kinds)),
        "inferred_end_count": len(inferred_sides),
        "inferred_side": ",".join(inferred_sides),
        "inferred_width_mm": _round(inferred_width, 1),
        "selection_status": _text(selection.get("status")),
        "rejected_cluster_count": int(_number(
            selection.get("rejected_cluster_count"))),
        "endpoint_polygon_support_count": int(_number(
            beam.get("endpoint_polygon_support_count"))),
        "beam_intersection_support_count": int(_number(
            beam.get("beam_intersection_support_count"))),
    }


def _beam_rows(grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for beams in grouped.values():
        for beam in beams:
            centerline = beam.get("centerline") or {}
            evidence = _end_evidence(beam)
            center = _number(beam.get("centerline_length_mm"))
            clear = _number(beam.get("clear_length_mm"))
            rows.append({
                "id": _text(beam.get("id")),
                "code": _text(beam.get("code")),
                "section": _text(beam.get("section")),
                "section_b_mm": _number(beam.get("section_b_mm"), 1),
                "section_h_mm": _number(beam.get("section_h_mm"), 1),
                "centerline_length_mm": _round(center, 1),
                "clear_length_mm": _round(clear, 1),
                "support_deduction_mm": _round(center - clear, 1),
                "gross_volume_m3": _round(beam.get("gross_volume_m3")),
                "clear_volume_m3": _round(beam.get("clear_volume_m3")),
                "quantity_status": _text(beam.get("quantity_status")),
                "support_count": int(_number(beam.get("support_count"))),
                "expected_support_count": int(_number(
                    beam.get("expected_support_count"))),
                "start_xy": [
                    _round((centerline.get("start") or [0, 0])[0], 1),
                    _round((centerline.get("start") or [0, 0])[1], 1)],
                "end_xy": [
                    _round((centerline.get("end") or [0, 0])[0], 1),
                    _round((centerline.get("end") or [0, 0])[1], 1)],
                "length_basis": _text(centerline.get("length_basis")),
                **evidence,
            })
    return rows


def build_closure(model: dict[str, Any], reconciliation: dict[str, Any],
                  frame_index: dict[str, Any],
                  intersection: dict[str, Any] | None,
                  options: dict[str, Any]) -> dict[str, Any]:
    """逐编号比较参考单实例轴长、CAD 链长与模型中心线/净长。"""
    tolerance = _number(options.get("deficit_tolerance_mm"), 100.0)
    grouped = _beams_by_code(model)
    beam_rows = _beam_rows(grouped)
    beam_summary: dict[str, dict[str, Any]] = {}
    for row in beam_rows:
        key = _code_key(row["code"])
        current = beam_summary.setdefault(key, {
            "beam_count": 0, "centerline_length_mm": 0.0,
            "clear_length_mm": 0.0, "gross_volume_m3": 0.0,
            "clear_volume_m3": 0.0, "inferred_end_count": 0,
            "inferred_width_mm": 0.0, "statuses": set(), "evidence": set(),
        })
        current["beam_count"] += 1
        current["centerline_length_mm"] += _number(row["centerline_length_mm"])
        current["clear_length_mm"] += _number(row["clear_length_mm"])
        current["gross_volume_m3"] += _number(row["gross_volume_m3"])
        current["clear_volume_m3"] += _number(row["clear_volume_m3"])
        current["inferred_end_count"] += int(row["inferred_end_count"])
        current["inferred_width_mm"] += _number(row["inferred_width_mm"])
        current["statuses"].add(_text(row["quantity_status"]))
        current["evidence"].update(row["evidence_kinds"])
    classes = {_code_key(row.get("code")): _text(row.get("classification"))
               for row in frame_index.get("code_index") or []}
    rows: list[dict[str, Any]] = []
    for code_row in reconciliation.get("beam_code_reconciliation") or []:
        key = _code_key(code_row.get("code"))
        classification = classes.get(key)
        if not classification or classification == "volume-matched-or-over":
            continue
        single = _number(code_row.get("reference_single_axis_length_mm"))
        selected = int(_number(
            code_row.get("selected_equivalent_instance_count")))
        cad_span = _number(code_row.get("cad_selected_span_mm"))
        per_instance = cad_span / selected if selected else 0.0
        deficit = _round(single - per_instance, 1)
        summary = beam_summary.get(key) or {}
        inferred_width = _number(summary.get("inferred_width_mm"))
        model_count = int(_number(summary.get("beam_count")))
        deduction_total = (_number(summary.get("centerline_length_mm"))
                           - _number(summary.get("clear_length_mm")))
        per_instance_inferred = (inferred_width / model_count
                                 if model_count else 0.0)
        per_instance_deduction = (deduction_total / model_count
                                  if model_count else 0.0)
        if selected == 0 and _number(summary.get("beam_count")) > 0:
            verdict = "chain-lost-in-reconciliation"
            action = ("模型里已有该编号梁实例，但编号链未选中，"
                      "属对账归属丢失，先修链再谈缺量")
        elif selected > 0 and model_count > 0 and selected != model_count:
            verdict = "instance-count-caliber-unstable"
            action = (f"编号链选中 {selected} 条与模型实例 {model_count} 根不一致，"
                      "每实例长度不可比，先统一实例口径再判长度")
        elif deficit <= 0.0:
            verdict = "no-length-deficit"
            action = "单实例长度不小于参考值，量差属实例数或计数口径"
        elif model_count > 0 and deficit <= per_instance_deduction + tolerance:
            verdict = "deficit-within-support-deduction"
            action = (f"长度差 {deficit:.0f} mm 不超过该梁中心线减净长的支座扣减 "
                      f"{per_instance_deduction:.0f} mm，属轴线长与净长口径差："
                      "这段空间已被柱/墙占住，计入即与竖向构件重复计量")
        elif deficit <= per_instance_inferred + tolerance:
            verdict = "deficit-within-support-inference"
            action = (f"长度差 {deficit:.0f} mm 不超过该梁推定端宽度合计 "
                      f"{per_instance_inferred:.0f} mm，属支座推定，"
                      "须回图确认支座后才可改净跨计量")
        else:
            verdict = "deficit-exceeds-support-inference"
            action = ("长度差大于推定端宽度合计，需核对同跨内是否还有未提取的"
                      "梁段，或参考单实例轴长口径本身偏大")
        rows.append({
            "code": _text(code_row.get("code")),
            "frame_classification": classification,
            "reference_instance_count": int(_number(
                code_row.get("reference_instance_count"))),
            "selected_equivalent_instance_count": selected,
            "reference_single_axis_length_mm": _round(single, 1),
            "cad_selected_span_mm": _round(cad_span, 1),
            "cad_span_per_selected_instance_mm": _round(per_instance, 1),
            "single_instance_deficit_mm": deficit,
            "model_beam_count": model_count,
            "model_centerline_mm": _round(
                _number(summary.get("centerline_length_mm")), 1),
            "model_clear_mm": _round(_number(summary.get("clear_length_mm")), 1),
            "model_support_deduction_mm": _round(
                _number(summary.get("centerline_length_mm"))
                - _number(summary.get("clear_length_mm")), 1),
            "model_support_deduction_per_instance_mm": _round(
                per_instance_deduction, 1),
            "inferred_end_width_per_instance_mm": _round(per_instance_inferred, 1),
            "support_evidence_kinds": sorted(summary.get("evidence") or []),
            "quantity_statuses": sorted(summary.get("statuses") or []),
            "current_code_difference_m3": _round(
                code_row.get("current_code_difference_m3")),
            "verdict": verdict,
            "action": action,
        })
    centerline_total = sum(_number(row["centerline_length_mm"])
                           for row in beam_rows)
    clear_total = sum(_number(row["clear_length_mm"]) for row in beam_rows)
    gross_total = sum(_number(row["gross_volume_m3"]) for row in beam_rows)
    clear_volume_total = sum(_number(row["clear_volume_m3"]) for row in beam_rows)
    deduction_volume = gross_total - clear_volume_total
    intersection_summary = (intersection or {}).get("summary") or {}
    beam_side_deduction = _number(
        intersection_summary.get("beam_side_deduction_candidate_m3"))
    verdict_counts: dict[str, int] = defaultdict(int)
    verdict_volume: dict[str, float] = defaultdict(float)
    for row in rows:
        verdict_counts[row["verdict"]] += 1
        verdict_volume[row["verdict"]] += abs(_number(
            row["current_code_difference_m3"]))
    inferred_only = sum(
        _number(row["inferred_width_mm"]) for row in beam_rows)
    return {
        "schema": SCHEMA,
        "floor": _text(reconciliation.get("floor")) or _text(
            model.get("floor") if isinstance(model.get("floor"), str) else ""),
        "rule": ("偏少编号的长度差先与同根梁的支座推定宽度比较："
                 "不超过推定端宽度合计的判为支座推定问题，不得当成缺几何；"
                 "模型已有实例但编号链未选中的判为对账归属丢失。"),
        "options": {"deficit_tolerance_mm": _round(tolerance, 1),
                    "floor_label": _text(options.get("floor_label"))},
        "summary": {
            "beam_instance_count": len(beam_rows),
            "centerline_length_mm": _round(centerline_total, 1),
            "clear_length_mm": _round(clear_total, 1),
            "support_deduction_length_mm": _round(
                centerline_total - clear_total, 1),
            "gross_volume_m3": _round(gross_total),
            "clear_volume_m3": _round(clear_volume_total),
            "span_caliber_difference_m3": _round(deduction_volume),
            "support_deduction_caliber_volume_m3": _round(
                verdict_volume.get("deficit-within-support-deduction")),
            "needs_new_geometry_volume_m3": _round(
                verdict_volume.get("deficit-exceeds-support-inference")),
            "chain_lost_volume_m3": _round(
                verdict_volume.get("chain-lost-in-reconciliation")),
            "inferred_end_support_width_mm": _round(inferred_only, 1),
            "intersection_beam_side_deduction_m3": _round(beam_side_deduction),
            "span_caliber_vs_intersection_conflict_m3": _round(
                deduction_volume - beam_side_deduction),
            "reviewed_code_count": len(rows),
            "verdict_total_m3": _round(sum(verdict_volume.values())),
            "caliber_only_volume_m3": _round(
                _number(verdict_volume.get("deficit-within-support-deduction"))
                + _number(verdict_volume.get("no-length-deficit"))
                + _number(verdict_volume.get("instance-count-caliber-unstable"))),
            "verdict_counts": dict(verdict_counts),
            "verdict_volume_m3": {
                key: _round(value) for key, value in verdict_volume.items()},
            "inferred_status_beam_count": sum(
                1 for row in beam_rows
                if row["quantity_status"] == "clear-span-inferred"),
            "review_status_beam_count": sum(
                1 for row in beam_rows
                if row["quantity_status"] == "clear-span-review"),
        },
        "code_closure": rows,
        "beams": beam_rows,
        "closure": {
            "gates": {
                "span-caliber-conflict-quantified": bool(
                    intersection is not None
                    and abs(deduction_volume - beam_side_deduction)
                    <= _number(options.get("conflict_tolerance_m3"), 0.05)),
                "beam-support-confirmation-closed": bool(
                    inferred_only == 0.0),
                "recon-chain-covers-modeled-beams": bool(
                    "chain-lost-in-reconciliation" not in verdict_counts),
                "all-deficits-classified": bool(
                    rows and "deficit-exceeds-support-inference"
                    not in verdict_counts),
                "verdict-covers-reviewed-codes": bool(
                    rows and abs(sum(verdict_volume.values())
                                 - sum(abs(_number(row["current_code_"
                                                     "difference_m3"]))
                                       for row in rows)) <= 0.0005),
                "span-caliber-volume-flagged": bool(
                    abs(_number(deduction_volume)
                        - _number(beam_side_deduction)) > 0.05
                    if intersection is not None else False),
            },
        },
        "formal_ready": False,
        "applied_to_formal_quantity": False,
    }


def csv_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows: list[list[Any]] = [
        ["section", "code", "frame_classification", "verdict", "ref_single_mm",
         "cad_span_mm", "cad_per_instance_mm", "deficit_mm",
         "inferred_end_mm", "model_centerline_mm", "model_clear_mm",
         "deduction_per_instance_mm", "difference_m3", "evidence", "note"]]
    for row in result["code_closure"]:
        rows.append([
            "code-closure", row["code"], row["frame_classification"],
            row["verdict"], row["reference_single_axis_length_mm"],
            row["cad_selected_span_mm"],
            row["cad_span_per_selected_instance_mm"],
            row["single_instance_deficit_mm"],
            row["inferred_end_width_per_instance_mm"],
            row["model_centerline_mm"], row["model_clear_mm"],
            row["model_support_deduction_per_instance_mm"],
            row["current_code_difference_m3"],
            "|".join(row["support_evidence_kinds"]), row["action"]])
    for row in result["beams"]:
        rows.append([
            "beam", row["code"], row["quantity_status"], row["id"], "", "", "",
            row["support_deduction_mm"], row["inferred_width_mm"],
            row["centerline_length_mm"], row["clear_length_mm"],
            row["gross_volume_m3"], "|".join(row["evidence_kinds"]),
            f"起点 {row['start_xy']} 终点 {row['end_xy']}；"
            f"推定端 {row['inferred_side'] or '无'}；"
            f"支座 {row['support_count']}/{row['expected_support_count']}"])
    return rows


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# 梁净跨口径与支座扣减对账",
        "",
        f"- 判定规则：{result['rule']}",
        f"- 梁实例 {summary['beam_instance_count']} 根："
        f"中心线合计 `{summary['centerline_length_mm']:.0f}` mm、"
        f"净长合计 `{summary['clear_length_mm']:.0f}` mm、"
        f"支座扣减 `{summary['support_deduction_length_mm']:.0f}` mm。",
        f"- 体积口径：中心线 `{summary['gross_volume_m3']:.4f}` m3、"
        f"净跨 `{summary['clear_volume_m3']:.4f}` m3、"
        f"口径差 `{summary['span_caliber_difference_m3']:.4f}` m3；"
        f"构件相交审计的梁侧可扣只有 "
        f"`{summary['intersection_beam_side_deduction_m3']:.4f}` m3，"
        f"两者相差 `{summary['span_caliber_vs_intersection_conflict_m3']:.4f}` m3。",
        f"- 长度差里可由支座扣减解释 "
        f"`{summary['support_deduction_caliber_volume_m3']:.4f}` m3（轴线长与净长口径差，"
        "计入即与柱墙重复），仍需新几何 "
        f"`{summary['needs_new_geometry_volume_m3']:.4f}` m3，"
        f"编号链丢失 `{summary['chain_lost_volume_m3']:.4f}` m3。",
        f"- 定责合计覆盖全部偏少编号毛差 "
        f"`{summary['verdict_total_m3']:.4f}` m3，其中纯口径问题 "
        f"`{summary['caliber_only_volume_m3']:.4f}` m3，"
        "真正需要补几何的只有需要核对长度与修链的两类。",
        f"- 净长证据质量：推定端 "
        f"`{summary['inferred_end_support_width_mm']:.0f}` mm、"
        f"`clear-span-inferred` {summary['inferred_status_beam_count']} 根、"
        f"`clear-span-review` {summary['review_status_beam_count']} 根。",
        "",
        "## 偏少编号长度定责",
        "",
        "| 编号 | 图框判定 | 参考单实例mm | CAD链长mm | 每选中实例mm | 长度差mm | 支座扣减mm | 推定端mm | 结论 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in result["code_closure"]:
        lines.append(
            f"| {row['code']} | {row['frame_classification']} | "
            f"{row['reference_single_axis_length_mm']:.0f} | "
            f"{row['cad_selected_span_mm']:.0f} | "
            f"{row['cad_span_per_selected_instance_mm']:.0f} | "
            f"{row['single_instance_deficit_mm']:.0f} | "
            f"{row['model_support_deduction_per_instance_mm']:.0f} | "
            f"{row['inferred_end_width_per_instance_mm']:.0f} | "
            f"{row['verdict']} |")
    lines += [
        "",
        "## 结论分布",
        "",
        "| 结论 | 编号数 | 量差m3 |",
        "|---|---:|---:|",
    ]
    for key, count in sorted(summary["verdict_counts"].items(),
                             key=lambda item: -item[1]):
        lines.append(f"| {key} | {count} | "
                     f"{summary['verdict_volume_m3'].get(key, 0):.4f} |")
    lines += [
        "",
        "## 门槛",
        "",
        "- `" + json.dumps(result["closure"]["gates"], ensure_ascii=False) + "`",
        "",
        "## 逐根梁证据",
        "",
        "| 实例 | 编号 | 截面 | 中心线mm | 净长mm | 扣减mm | 推定端 | 证据 | 坐标 |",
        "|---|---|---|---:|---:|---:|---|---|---|",
    ]
    for row in result["beams"][:20]:
        lines.append(
            f"| {row['id']} | {row['code']} | {row['section']} | "
            f"{row['centerline_length_mm']:.0f} | {row['clear_length_mm']:.0f} | "
            f"{row['support_deduction_mm']:.0f} | "
            f"{row['inferred_side'] or '—'} | "
            f"{'|'.join(row['evidence_kinds']) or '—'} | "
            f"`{row['start_xy']}→{row['end_xy']}` |")
    lines += [
        "",
        f"- 只有 {len(result['beams'])} 根梁的全部证据，MD 展示前 20 根，"
        "完整清单见同名 CSV。",
        "- 净跨口径在支座确认前不得替换中心线口径，本节不改任何构件体积，"
        "`formal_ready` 仍为 `false`。",
    ]
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="梁净跨口径与支座扣减对账，偏少编号长度定责")
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--reconciliation-json", required=True)
    parser.add_argument("--frame-index-json", required=True,
                        help="cad-beam-frame-label-index JSON")
    parser.add_argument("--intersection-json", default=None,
                        help="构件相交扣减试算 JSON，用于口径冲突量化")
    parser.add_argument("--deficit-tolerance-mm", type=float, default=100.0)
    parser.add_argument("--conflict-tolerance-m3", type=float, default=0.05)
    parser.add_argument("--floor-label", default=None)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()
    paths = {"model": Path(args.model_json),
             "reconciliation": Path(args.reconciliation_json),
             "frame_index": Path(args.frame_index_json)}
    if args.intersection_json:
        paths["intersection"] = Path(args.intersection_json)
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        parser.error("缺少输入：" + "、".join(missing))
    result = build_closure(
        json.loads(paths["model"].read_text(encoding="utf-8")),
        json.loads(paths["reconciliation"].read_text(encoding="utf-8")),
        json.loads(paths["frame_index"].read_text(encoding="utf-8")),
        json.loads(paths["intersection"].read_text(encoding="utf-8"))
        if "intersection" in paths else None,
        {"deficit_tolerance_mm": args.deficit_tolerance_mm,
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
    checksums = out.with_name(out.name + ".sha256")
    checksums.write_text("\n".join(
        f"{sha256(path)}  {path.resolve()}"
        for path in (json_path, csv_path, md_path)) + "\n", encoding="utf-8")
    print(json.dumps({
        "schema": result["schema"],
        "summary": result["summary"],
        "gates": result["closure"]["gates"],
        "formal_ready": result["formal_ready"],
        "outputs": [str(json_path), str(csv_path), str(md_path), str(checksums)],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
