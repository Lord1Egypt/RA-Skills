#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按体积口径归因梁编号量差，区分真实缺量与实例计数口径差。"""



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


SCHEMA = "cad-beam-gap-attribution/v0.1"
SECTION_RE = re.compile(r"(\d+(?:\.\d+)*)\s*[xX*]\s*(\d+(?:\.\d+)*)")



def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _section_area_m2(section: Any) -> float | None:
    match = SECTION_RE.search(_text(section))
    if not match:
        return None
    width = _number(match.group(1))
    height = _number(match.group(2))
    if width <= 0.0 or height <= 0.0:
        return None
    return width * height / 1_000_000.0


def _assigned_runs(reconciliation: dict[str, Any]) -> set[str]:
    assigned: set[str] = set()
    for code_row in reconciliation.get("beam_code_reconciliation") or []:
        for key in ("selected_chains", "rejected_chains"):
            for chain in code_row.get(key) or []:
                assigned.update(
                    _text(run_id) for run_id in chain.get("run_ids") or [])
    return assigned


def _unassigned_runs(
        model: dict[str, Any], assigned: set[str]) -> list[dict[str, Any]]:
    registry = model.get("run_registry") or {}
    rows: list[dict[str, Any]] = []
    for run in registry.get("runs") or []:
        run_id = _text(run.get("id"))
        if not run_id or run_id in assigned:
            continue
        rows.append({
            "id": run_id,
            "section": _text(run.get("section")),
            "section_area_m2": _section_area_m2(run.get("section")),
            "length_mm": _round(run.get("length_mm"), 1),
            "volume_m3": _round(run.get("volume_m3")),
            "orientation": _text(run.get("orientation")),
            "axis_mm": _round(run.get("axis_mm"), 1),
            "matched_code": _text(run.get("matched_code")),
        })
    return rows


def _action(row: dict[str, Any], prior_status: str) -> str:
    classification = row["classification"]
    if classification == "volume-matched":
        if row["missing_instance_count"]:
            return (
                f"体积已对齐，剩余 {row['missing_instance_count']} 个实例是计数口径差，"
                "只影响钢筋支数，不再算混凝土缺口")
        return "体积与实例数均已对齐"
    if classification == "volume-over":
        return (
            f"多计 {row['difference_m3']:.4f} m3，属编号归属偏置；"
            "复核引线目标与镜像副本，不改几何")
    if prior_status == "missing-cad-geometry":
        return (
            f"缺量 {abs(row['difference_m3']):.4f} m3；本层图框内无该编号任何几何证据，"
            "需确认是否画在其他图框")
    if row["unassigned_candidate_count"]:
        return (
            f"缺量 {abs(row['difference_m3']):.4f} m3，按截面需补 "
            f"{row['needed_length_mm']:.0f} mm 梁线；已展开图中还有同截面未归属图线，"
            "优先回图认领")
    return (
        f"缺量 {abs(row['difference_m3']):.4f} m3，按截面需补 "
        f"{row['needed_length_mm']:.0f} mm 梁线；已展开图线中无对应未归属图线，"
        "需到其他图框或大样检索")


def _build_row(
        code_row: dict[str, Any],
        tolerance: float,
        unassigned: list[dict[str, Any]],
        ) -> dict[str, Any]:
    reference_volume = _number(code_row.get("reference_volume_m3"))
    cad_volume = _number(code_row.get("current_code_volume_m3"))
    difference = cad_volume - reference_volume
    area = _section_area_m2(code_row.get("reference_single_section"))
    single_length = _number(
        code_row.get("reference_single_net_length_mm")) or _number(
        code_row.get("reference_single_axis_length_mm"))
    per_instance_volume = (area or 0.0) * single_length / 1000.0
    missing = int(_number(code_row.get("missing_equivalent_instance_count")) or 0)
    if abs(difference) <= tolerance:
        classification = "volume-matched"
    elif difference < 0.0:
        classification = "volume-under"
    else:
        classification = "volume-over"
    explained = 0
    if difference < -tolerance and per_instance_volume > 0.0:
        explained = min(missing, int(abs(difference) / per_instance_volume))
    needed_length = (
        abs(difference) / area * 1000.0
        if (area and difference < -tolerance) else 0.0)
    candidates = [
        run for run in unassigned
        if run["section_area_m2"] and area
        and abs(run["section_area_m2"] - area) / area <= 0.35
        and _number(run["length_mm"]) >= max(500.0, needed_length * 0.2)
    ] if needed_length > 0.0 else []
    row = {
        "code": _text(code_row.get("code")),
        "base_code": _text(code_row.get("base_code")),
        "reference_section": _text(code_row.get("reference_single_section")),
        "reference_instance_count": int(
            _number(code_row.get("reference_instance_count")) or 0),
        "selected_equivalent_instance_count": int(
            _number(code_row.get("selected_equivalent_instance_count")) or 0),
        "missing_instance_count": missing,
        "reference_volume_m3": _round(reference_volume),
        "cad_volume_m3": _round(cad_volume),
        "difference_m3": _round(difference),
        "difference_pct": _round(
            difference / reference_volume * 100.0, 2) if reference_volume else 0.0,
        "single_instance_volume_m3": _round(per_instance_volume),
        "volume_explained_missing_instance_count": explained,
        "count_only_missing_instance_count": missing - explained,
        "classification": classification,
        "needed_length_mm": _round(needed_length, 1),
        "unassigned_candidate_count": len(candidates),
        "unassigned_candidate_length_mm": _round(
            sum(_number(run["length_mm"]) for run in candidates), 1),
        "cad_run_count": int(_number(code_row.get("cad_run_count")) or 0),
        "cad_chain_count": int(_number(code_row.get("cad_chain_count")) or 0),
        "prior_status": _text(code_row.get("status")),
    }
    row["action"] = _action(row, _text(code_row.get("status")))
    return row


def build_attribution(
        reconciliation: dict[str, Any],
        model: dict[str, Any],
        endpoint: dict[str, Any] | None = None,
        options: dict[str, float] | None = None,
        ) -> dict[str, Any]:
    options = dict(options or {})
    tolerance = _number(options.get("volume_tolerance_m3"), 0.05) or 0.05
    code_rows = list(reconciliation.get("beam_code_reconciliation") or [])
    unassigned = _unassigned_runs(model, _assigned_runs(reconciliation))
    rows = [_build_row(row, tolerance, unassigned) for row in code_rows]
    ledger = (reconciliation.get("concrete_ledger")
              or model.get("concrete_ledger") or {})
    under = [row for row in rows if row["classification"] == "volume-under"]
    over = [row for row in rows if row["classification"] == "volume-over"]
    matched = [row for row in rows if row["classification"] == "volume-matched"]
    under_total = sum(-row["difference_m3"] for row in under)
    over_total = sum(row["difference_m3"] for row in over)
    missing_total = sum(row["missing_instance_count"] for row in rows)
    explained_total = sum(
        row["volume_explained_missing_instance_count"] for row in rows)
    unassigned_volume = sum(_number(run["volume_m3"]) for run in unassigned)
    attributed_total = sum(row["cad_volume_m3"] for row in rows)
    main_reference = sum(row["reference_volume_m3"] for row in rows)
    net_code_difference = sum(row["difference_m3"] for row in rows)
    reattribution_capacity = min(under_total, over_total)
    net_unlocated = abs(net_code_difference)
    residual_new_geometry = max(0.0, net_unlocated - unassigned_volume)
    stair_reference = _number(ledger.get("stair_beam_reference_m3"))
    stair_located = _number(ledger.get("stair_beam_cad_m3"))
    special_located = (
        _number(ledger.get("lb_reference_m3"))
        + _number(ledger.get("tl2_reference_m3")))
    beam_reference_total = _number(ledger.get("beam_reference_m3"))
    coupling_reference = (
        beam_reference_total - main_reference - stair_reference - special_located)
    coupling_located = _number(ledger.get("coupling_beam_m3"))
    main_located = _number(ledger.get("main_beam_cad_m3"))
    components = [
        {"component": "主梁", "reference_m3": _round(main_reference),
         "located_m3": _round(main_located),
         "difference_m3": _round(main_located - main_reference),
         "note": "含未归属图线池"},
        {"component": "连梁", "reference_m3": _round(coupling_reference),
         "located_m3": _round(coupling_located),
         "difference_m3": _round(coupling_located - coupling_reference),
         "note": "参考值由梁总量减主梁、楼梯梁和特殊梁反推"},
        {"component": "楼梯梁", "reference_m3": _round(stair_reference),
         "located_m3": _round(stair_located),
         "difference_m3": _round(stair_located - stair_reference),
         "note": "阶段二十独立台账"},
        {"component": "特殊梁", "reference_m3": _round(special_located),
         "located_m3": _round(special_located),
         "difference_m3": 0.0,
         "note": "TL2 与 Lb-1 只按参考兼容量入账，不是独立 CAD 量"},
    ]
    decomposition = {
        "beam_reference_m3": _round(beam_reference_total),
        "beam_located_m3": _round(_number(ledger.get("located_beam_total_m3"))),
        "beam_remaining_m3": _round(_number(ledger.get("beam_remaining_m3"))),
        "components": components,
        "sum_difference_m3": _round(sum(
            _number(row["difference_m3"]) for row in components)),
    }
    decomposition["matches_ledger"] = bool(
        abs(abs(decomposition["sum_difference_m3"])
            - abs(_number(ledger.get("beam_remaining_m3")))) <= tolerance)
    endpoint_summary = {}
    if endpoint:
        classification = endpoint.get("endpoint_classification") or {}
        endpoint_summary = {
            "total": int(_number(classification.get("total")) or 0),
            "counts": dict(classification.get("counts") or {}),
            "gates": dict(endpoint.get("gates") or {}),
        }
    main_reference = sum(row["reference_volume_m3"] for row in rows)
    summary = {
        "code_count": len(rows),
        "volume_matched_code_count": len(matched),
        "volume_under_code_count": len(under),
        "volume_over_code_count": len(over),
        "under_total_m3": _round(under_total),
        "over_total_m3": _round(over_total),
        "net_code_difference_m3": _round(
            sum(row["difference_m3"] for row in rows)),
        "main_beam_reference_m3": _round(main_reference),
        "main_beam_cad_m3": _round(main_located),
        "beam_reference_m3": _round(ledger.get("beam_reference_m3")),
        "beam_located_m3": _round(ledger.get("located_beam_total_m3")),
        "beam_remaining_m3": _round(ledger.get("beam_remaining_m3")),
        "missing_instance_count": missing_total,
        "volume_explained_missing_instance_count": explained_total,
        "count_only_missing_instance_count": missing_total - explained_total,
        "unassigned_run_count": len(unassigned),
        "unassigned_run_max_length_mm": _round(
            max((_number(run["length_mm"]) for run in unassigned),
                default=0.0), 1),
        "unassigned_run_volume_m3": _round(unassigned_volume),
        "reattribution_capacity_m3": _round(reattribution_capacity),
        "main_beam_net_unlocated_m3": _round(net_unlocated),
        "residual_needing_new_geometry_m3": _round(residual_new_geometry),
        "attributed_code_cad_m3": _round(attributed_total),
        "ledger_main_beam_cad_m3": _round(main_located),
        "run_coverage_gap_m3": _round(main_located - attributed_total),
        "unassigned_run_volume_available_m3": _round(unassigned_volume),
        "gap_decomposition": decomposition,
        "search_target_count": len(under),
    }
    return {
        "schema": SCHEMA,
        "floor": (reconciliation.get("floor_mapping") or {}).get(
            "reference_floor") or _text((model.get("floor") or {}).get("label")),
        "rule": {
            "volume_is_authoritative": True,
            "volume_tolerance_m3": _round(tolerance),
            "instance_count_formula": (
                reconciliation.get("reference_decomposition_rule") or {}
            ).get("instance_count_formula", ""),
            "note": (
                "混凝土量只看体积对账；实例数由累计宽乘累计高除以截面面积推出，"
                "体积不足时该计数不能全部落成几何"),
        },
        "code_attribution": sorted(
            rows, key=lambda row: (row["difference_m3"], row["code"])),
        "search_targets": [
            {
                "code": row["code"],
                "section": row["reference_section"],
                "missing_volume_m3": _round(-row["difference_m3"]),
                "needed_length_mm": row["needed_length_mm"],
                "unassigned_candidate_count": row["unassigned_candidate_count"],
                "unassigned_candidate_length_mm":
                    row["unassigned_candidate_length_mm"],
                "prior_status": row["prior_status"],
            }
            for row in under],
        "unassigned_runs": unassigned,
        "support_and_span": endpoint_summary,
        "summary": summary,
        "closure": {
            "reconciled": bool(decomposition["matches_ledger"]),
            "residual_unexplained_m3": _round(
                abs(_number(ledger.get("beam_remaining_m3")))
                - abs(decomposition["sum_difference_m3"])),
            "net_unlocated_m3": _round(net_unlocated),
            "unassigned_pool_m3": _round(unassigned_volume),
            "applied_to_formal_quantity": False,
            "formal_ready": False,
        },
        "formal_ready": False,
        "applied_to_formal_quantity": False,
    }


def csv_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows = [[
        "编号", "截面", "体积状态", "参考体积m3", "CAD体积m3", "体积差m3",
        "差百分比", "缺失实例", "体积可解释实例", "仅计数口径实例",
        "需补梁线mm", "未归属同截面图线数", "未归属同截面长度mm", "处理动作",
    ]]
    for row in result["code_attribution"]:
        rows.append([
            row["code"], row["reference_section"], row["classification"],
            row["reference_volume_m3"], row["cad_volume_m3"],
            row["difference_m3"], row["difference_pct"],
            row["missing_instance_count"],
            row["volume_explained_missing_instance_count"],
            row["count_only_missing_instance_count"],
            row["needed_length_mm"], row["unassigned_candidate_count"],
            row["unassigned_candidate_length_mm"], row["action"],
        ])
    rows.append([])
    rows.append(["未归属图线", "句柄", "截面", "长度mm", "体积m3", "方向",
                 "轴位置mm", "曾匹配编号"])
    for row in result["unassigned_runs"]:
        rows.append([
            "", row["id"], row["section"], row["length_mm"], row["volume_m3"],
            row["orientation"], row["axis_mm"], row["matched_code"],
        ])
    return rows


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    decomposition = summary["gap_decomposition"]
    lines = [
        "# 梁编号体积缺口归因",
        "",
        f"- Schema：`{result['schema']}`，楼层：{result['floor'] or '未标注'}。",
        f"- {summary['code_count']} 个编号按体积对账：体积一致 "
        f"{summary['volume_matched_code_count']} 个、缺量 "
        f"{summary['volume_under_code_count']} 个（{summary['under_total_m3']:.4f} m3）、"
        f"多计 {summary['volume_over_code_count']} 个（{summary['over_total_m3']:.4f} m3），"
        f"净差 {summary['net_code_difference_m3']:.4f} m3。",
        f"- 缺量拆分：偏多侧最多可转移解释 "
        f"{summary['reattribution_capacity_m3']:.4f} m3（只改归属、不改总量），"
        f"净未定位 {summary['main_beam_net_unlocated_m3']:.4f} m3。",
        f"- 实例口径拆分：原报缺失 {summary['missing_instance_count']} 个实例，"
        f"体积可支撑 {summary['volume_explained_missing_instance_count']} 个，"
        f"其余 {summary['count_only_missing_instance_count']} 个为计数口径差，"
        "只影响钢筋支数，不再算混凝土缺口。",
        f"- 已展开图中未归属图线 {summary['unassigned_run_count']} 条、"
        f"{summary['unassigned_run_volume_m3']:.4f} m3，"
        f"最长仅 {summary['unassigned_run_max_length_mm']:.0f} mm，"
        "不足以按编号认领；扣除后仍需检索新几何 "
        f"{summary['residual_needing_new_geometry_m3']:.4f} m3。",
        f"- 梁缺口分解：",
        "",
        "| 分项 | 参考m3 | 已定位m3 | 差m3 | 说明 |",
        "|---|---:|---:|---:|---|",
    ]
    for row in decomposition["components"]:
        lines.append(
            f"| {row['component']} | {row['reference_m3']:.4f} | "
            f"{row['located_m3']:.4f} | {row['difference_m3']:+.4f} | "
            f"{row['note']} |")
    lines.append(
        f"| 合计 | {decomposition['beam_reference_m3']:.4f} | "
        f"{decomposition['beam_located_m3']:.4f} | "
        f"{decomposition['sum_difference_m3']:+.4f} | 台账缺口 "
        f"{decomposition['beam_remaining_m3']:.4f} m3，"
        + ("完全对上" if decomposition["matches_ledger"] else "未对上") + " |")
    lines += [
        "",
        "## 编号级归因",
        "",
        "| 编号 | 截面 | 体积状态 | 参考m3 | CADm3 | 差m3 | 缺实例 | 体积可解释 | 仅计数 | 需补梁线mm |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in result["code_attribution"]:
        lines.append(
            f"| {row['code']} | {row['reference_section']} | "
            f"{row['classification']} | {row['reference_volume_m3']:.4f} | "
            f"{row['cad_volume_m3']:.4f} | {row['difference_m3']:+.4f} | "
            f"{row['missing_instance_count']} | "
            f"{row['volume_explained_missing_instance_count']} | "
            f"{row['count_only_missing_instance_count']} | "
            f"{row['needed_length_mm']:.0f} |")
    lines += [
        "",
        "## 检索目标",
        "",
        "| 编号 | 截面 | 缺量m3 | 需补梁线mm | 未归属同截面图线 | 原状态 |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in result["search_targets"]:
        lines.append(
            f"| {row['code']} | {row['section']} | "
            f"{row['missing_volume_m3']:.4f} | {row['needed_length_mm']:.0f} | "
            f"{row['unassigned_candidate_count']} | {row['prior_status']} |")
    support = result.get("support_and_span") or {}
    if support:
        lines += [
            "",
            "## 支座与净跨现状",
            "",
            f"- 待分级梁端 {support.get('total', 0)} 个："
            + "、".join(
                f"{key} {value}"
                for key, value in sorted((support.get("counts") or {}).items()))
            + "。",
            f"- 门槛：`"
            + json.dumps(support.get("gates") or {}, ensure_ascii=False) + "`。",
        ]
    lines += [
        "",
        "## 结论",
        "",
        "- 混凝土量以体积对账为准；计数口径差不得当成缺量补造几何。",
        "- 多计编号是归属偏置，复核引线目标即可，不新增也不改写几何。",
        "- 未归属图线不足的部分只能靠其他图框或大样补齐，"
        "正式量保持 `formal_ready=false`。",
    ]
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="按体积口径归因梁编号量差并给出检索目标")
    parser.add_argument("--reconciliation-json", required=True,
                        help="cad-beam-reference-reconciliation JSON")
    parser.add_argument("--model-json", required=True,
                        help="结构模型 JSON，用于取未归属 run")
    parser.add_argument("--endpoint-json", default=None,
                        help="梁端几何分级 JSON")
    parser.add_argument("--volume-tolerance-m3", type=float, default=0.05)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    paths = {"reconciliation": Path(args.reconciliation_json),
             "model": Path(args.model_json)}
    if args.endpoint_json:
        paths["endpoint"] = Path(args.endpoint_json)
    missing = [str(path) for name, path in paths.items() if not path.exists()]
    if missing:
        parser.error("缺少输入：" + "、".join(missing))
    result = build_attribution(
        _load(paths["reconciliation"]),
        _load(paths["model"]),
        _load(paths["endpoint"]) if "endpoint" in paths else None,
        {"volume_tolerance_m3": args.volume_tolerance_m3},
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
        "code_count": summary["code_count"],
        "under_total_m3": summary["under_total_m3"],
        "over_total_m3": summary["over_total_m3"],
        "net_code_difference_m3": summary["net_code_difference_m3"],
        "volume_explained_missing_instance_count":
            summary["volume_explained_missing_instance_count"],
        "count_only_missing_instance_count":
            summary["count_only_missing_instance_count"],
        "unassigned_run_volume_m3": summary["unassigned_run_volume_m3"],
        "residual_needing_new_geometry_m3":
            summary["residual_needing_new_geometry_m3"],
        "gap_decomposition_matches_ledger":
            summary["gap_decomposition"]["matches_ledger"],
        "reconciled": result["closure"]["reconciled"],
        "residual_unexplained_m3": result["closure"]["residual_unexplained_m3"],
        "formal_ready": result["formal_ready"],
        "outputs": [str(json_path), str(csv_path), str(md_path), str(checksums)],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
