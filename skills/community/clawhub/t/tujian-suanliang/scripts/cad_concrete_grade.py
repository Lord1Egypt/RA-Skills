#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""混凝土分标号台账内核：把构件量按强度等级分账，并强制恒等式与来源等级。

输入两套 JSON：
  --rules-json  等级规则行（按项目人工核对后给出，含来源类型与置信）
  来源类型除图面各级外，另有 user-rule：经使用者确认的施工做法（如节点区梁端 500 mm
  按柱等级浇筑），按可采信处理，不当作图面直接计量证据。
  --ledger-report-json 统一混凝土分账报告（用于校核合计，可选）
输出 JSON/CSV/Markdown，含 by_grade、未定量和闭合门槛。
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
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_ROWS = "cad-concrete-grade-rules/v0.1"
SCHEMA_OUT = "cad-concrete-grade-ledger/v0.1"
SOURCE_RANK = {
    "member-label": 0,
    "drawing-table": 1,
    "design-booklet-table": 2,
    "drawing-note": 3,
    "user-rule": 3,
    "inferred": 4,
    "manual": 5,
    "unknown": 6,
}
ADDABLE = {"cast-in-place", "composite-whole", "seam", "beam", "coupling-beam",
           "stair-beam", "vertical", "column", "wall", "slab-cast", "other"}
SUBLAYER = {"prefab-sublayer", "excluded-sublayer"}


def _num(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_dict(value) -> dict:
    """rule_notes 允许 list[str] 或 dict：清单式写法常见，不得因此崩台账。"""
    if isinstance(value, dict):
        return value
    if isinstance(value, (list, tuple)):
        return {f"note{i + 1}": str(item) for i, item in enumerate(value)}
    return {}


def load(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    source = Path(path)
    if not source.exists():
        return {}
    return json.loads(source.read_text())


def report_candidate_total(report: dict[str, Any]) -> float | None:
    """从统一混凝土分账报告里取分账基准，省掉人工抄数。"""
    containers = [report, report.get("concrete_ledger") or {},
                  report.get("quantities") or {}]
    for box in containers:
        if not isinstance(box, dict):
            continue
        for key in ("concrete_candidate_total_m3", "candidate_total_volume_m3",
                    "candidate_total_m3"):
            value = box.get(key)
            if isinstance(value, (int, float)) and value > 0:
                return float(value)
    return None


def material_split_totals(split: dict[str, Any]) -> dict[str, float]:
    """从口径分解结果里取"预制子层体积 / 现浇口径板体系合计"，缺项返回空。"""
    summary = dict(split.get("summary") or {})
    out: dict[str, float] = {}
    for key in ("prefab_sublayer_m3", "slab_cast_in_place_caliber_A_m3",
                "slab_caliber_A_total_m3"):
        value = _num(summary.get(key), -1.0)
        if value >= 0:
            out[key] = round(value, 4)
    return out


def build_ledger(rules: dict[str, Any], report: dict[str, Any],
                 expected_total: float | None,
                 baseline_source: str = "self",
                 material_split: dict[str, Any] | None = None) -> dict[str, Any]:
    rows_in = [row for row in (rules.get("rows") or []) if isinstance(row, dict)]
    rows = []
    split_totals = material_split_totals(material_split or {})
    prefab_sublayer_m3 = split_totals.get("prefab_sublayer_m3", 0.0)
    composite_rows: list[dict[str, Any]] = []
    by_grade: dict[str, float] = {}
    grade_sources: dict[str, set] = {}
    unconfirmed = 0.0
    review = 0.0
    excluded = 0.0
    sublayer_share_excluded = 0.0
    counted = 0.0
    joint_zone = 0.0
    for row in rows_in:
        volume = _num(row.get("volume_m3"))
        treatment = str(row.get("treatment") or "count")
        grade = str(row.get("grade") or "").strip().upper() or "未定"
        source_type = str(row.get("source_type") or "unknown")
        rank = SOURCE_RANK.get(source_type, 6)
        entry = {
            "component": str(row.get("component") or ""),
            "member_group": str(row.get("member_group") or ""),
            "volume_m3": round(volume, 4),
            "grade": grade,
            "source_type": source_type,
            "source_ref": str(row.get("source_ref") or ""),
            "treatment": treatment,
            "evidence_rank": rank,
            "needs_review": bool(row.get("needs_review")) or rank >= SOURCE_RANK["inferred"],
        }
        rows.append(entry)
        if treatment in SUBLAYER or treatment == "exclude":
            excluded += volume
            continue
        # 现浇口径：叠合板整厚含预制底板子层，报现浇量只能取补浇部分，
        # 预制部分退回装配式采购台账；整厚原值留在行里作审计。
        counted_volume = volume
        if prefab_sublayer_m3 > 0 and row.get("member_group") == "composite-whole":
            share = min(prefab_sublayer_m3, volume)
            entry["prefab_sublayer_volume_m3"] = round(share, 4)
            entry["cast_in_place_volume_m3"] = round(volume - share, 4)
            composite_rows.append(entry)
            counted_volume = round(volume - share, 4)
            sublayer_share_excluded += share
        counted += counted_volume
        if str(row.get("treatment") or "").startswith("joint-zone"):
            joint_zone += counted_volume
        if entry["needs_review"]:
            review += counted_volume
        by_grade[grade] = round(by_grade.get(grade, 0.0) + counted_volume, 4)
        grade_sources.setdefault(grade, set()).add(source_type)
        if grade == "未定" or rank >= SOURCE_RANK["inferred"]:
            unconfirmed += counted_volume
    total = round(counted, 4)
    residual = round(total - round(sum(by_grade.values()), 4), 6)
    base = total
    if expected_total is not None and expected_total > 0:
        base = round(float(expected_total), 4)
        if prefab_sublayer_m3 > 0:
            # 分账基准含整厚，报现浇量必须同步减掉预制子层
            base = round(base - prefab_sublayer_m3, 4)
            baseline_source = baseline_source + "-minus-prefab-sublayer"
    identity = round(total - base, 4)
    weak = sorted({
        row["grade"] for row in rows
        if row["treatment"] not in SUBLAYER and row["treatment"] != "exclude"
        and SOURCE_RANK.get(row["source_type"], 6) >= SOURCE_RANK["inferred"]
    })
    whole_thickness_m3 = round(sum(
        _num(row.get("volume_m3")) for row in rows
        if row.get("member_group") == "composite-whole"), 4)
    cast_layer_m3 = round(sum(
        _num(row.get("cast_in_place_volume_m3")) for row in composite_rows), 4)
    split_prefab_m3 = round(sum(
        _num(row.get("prefab_sublayer_volume_m3")) for row in composite_rows), 4)
    slab_cast_rows = round(sum(
        _num(row.get("cast_in_place_volume_m3")) if row.get("member_group") == "composite-whole"
        else _num(row.get("volume_m3"))
        for row in rows if row.get("member_group") in
        ("slab-cast", "seam", "composite-whole")), 4)
    caliber_target = split_totals.get("slab_cast_in_place_caliber_A_m3")
    split_residual = round(whole_thickness_m3 - (cast_layer_m3 + split_prefab_m3), 6)
    caliber_residual = (round(slab_cast_rows - caliber_target, 6)
                        if caliber_target is not None else None)
    if prefab_sublayer_m3 <= 0 or not composite_rows:
        dedup_gate = "fail"
        dedup_evidence = ("未给出现浇/预制材料分账输入，分标号台账仍按整厚全额计入，"
                          "会把预制底板体积重复计入现浇混凝土量")
        dedup_action = "接 --material-split-json（口径分解结果），把整厚拆成补浇层与预制子层。"
    elif abs(split_residual) > 0.001 or (caliber_residual is not None
                                         and abs(caliber_residual) > 0.001):
        dedup_gate = "fail"
        dedup_evidence = ("整厚 %s m3 vs 补浇 %s + 预制 %s（残差 %s）；"
                          "现浇板+板缝+补浇层 %s m3 对现浇口径 %s（残差 %s）" % (
                              whole_thickness_m3, cast_layer_m3, split_prefab_m3,
                              split_residual, slab_cast_rows, caliber_target, caliber_residual))
        dedup_action = "先查整厚与子层体积口径，不得改总量或跳过恒等式。"
    else:
        dedup_gate = "pass"
        dedup_evidence = ("叠合板整厚 %s m3 已拆为补浇层 %s m3 + 预制子层 %s m3（残差 %s）；"
                          "现浇板+板缝+补浇层 %s m3 = 现浇口径 %s m3（残差 %s）；"
                          "预制子层退回装配式采购台账，不进现浇分标号" % (
                              whole_thickness_m3, cast_layer_m3, split_prefab_m3,
                              split_residual, slab_cast_rows, caliber_target, caliber_residual))
        dedup_action = "报现浇量用补浇层口径；装配式构件量单独出表。"
    unconfirmed_ratio = (unconfirmed / total) if total else 0.0
    review_ratio = (review / total) if total else 0.0
    if not weak and review_ratio == 0.0:
        source_gate = "pass"
    elif unconfirmed_ratio > 0.5 or review_ratio > 0.5:
        source_gate = "fail"
    else:
        source_gate = "warn"
    return {
        "schema": SCHEMA_OUT,
        "floor": str(rules.get("floor") or ""),
        "source_rules": rules.get("schema") or "",
        "rows": rows,
        "by_grade": {key: round(value, 4) for key, value in sorted(by_grade.items())},
        "grade_source_types": {key: sorted(value) for key, value in sorted(grade_sources.items())},
        "summary": {
            "row_count": len(rows),
            "counted_total_m3": total,
            "excluded_sublayer_m3": round(excluded, 4),
            "cast_in_place_total_m3": total,
            "prefab_sublayer_row_excluded_m3": round(excluded, 4),
            "prefab_sublayer_split_excluded_m3": round(sublayer_share_excluded, 4),
            "prefab_sublayer_note": (
                "规则行里的预制子层与整厚拆分出的是同一笔体积，报量只剔一次；"
                "两个计数分别记账，不叠加成一个总数"),
            "composite_whole_thickness_m3": whole_thickness_m3,
            "composite_cast_layer_m3": cast_layer_m3,
            "composite_prefab_sublayer_m3": split_prefab_m3,
            "slab_cast_caliber_m3": slab_cast_rows,
            "slab_cast_caliber_target_m3": caliber_target,
            "prefab_sublayer_input_m3": round(prefab_sublayer_m3, 4),
            "unconfirmed_m3": round(unconfirmed, 4),
            "unconfirmed_ratio": round(unconfirmed / total, 6) if total else None,
            "needs_review_m3": round(review, 4),
            "joint_zone_m3": round(joint_zone, 4),
            "rule_notes": _as_dict(rules.get("rule_notes")),
            "needs_review_ratio": round(review / total, 6) if total else None,
            "expected_total_m3": round(base, 4),
            "identity_baseline_source": (
                baseline_source if expected_total is not None
                and expected_total > 0 else "self"),
            "identity_residual_m3": identity,
            "grade_partition_residual_m3": residual,
            "grades_with_weak_source": weak,
        },
        "gates": [
            {
                "id": "grade-ledger-identity",
                "title": "分标号合计恒等式",
                "status": "pass" if abs(identity) <= 0.001 and abs(residual) <= 0.001 else "fail",
                "evidence": "Σ分级 %s m3 对分账基准 %s m3，残差 %s m3；分级内部残差 %s m3" % (
                    total, round(base, 4), identity, residual),
                "action": "残差不为 0 时先查行口径（子层重复、未分解残差），不得改总量。",
            },
            {
                "id": "grade-source-evidence",
                "title": "等级来源证据等级",
                "status": source_gate,
                "evidence": "未定/推定 %s m3（占 %s%%）；需回图确认 %s m3（占 %s%%）；" \
                            "来源偏弱的等级：%s" % (
                                round(unconfirmed, 4),
                                round(unconfirmed_ratio * 100, 2),
                                round(review, 4), round(review_ratio * 100, 2),
                                "、".join(weak) or "无"),
                "action": "把推定档换成图面直接证据：层高表逐层范围、墙柱表混凝土列或构件标注。",
            },
            {
                "id": "grade-sublayer-double-count",
                "title": "预制子层不得与整厚相加",
                "status": "pass" if excluded > 0 else "warn",
                "evidence": "剔除子层 %s m3（预制底板等），未计入分级合计" % round(excluded, 4),
                "action": "现浇报量取叠合板补浇部分；预制构件另立装配式采购台账。",
            },
            {
                "id": "prefab-sublayer-dedup-applied",
                "title": "预制子层去重已落进分账",
                "status": dedup_gate,
                "evidence": dedup_evidence,
                "action": dedup_action,
            },
        ],
        "formal_ready": False,
        "applied_to_formal_quantity": False,
    }


def render_csv(payload: dict[str, Any], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["构件", "分组", "体积m3", "强度等级", "来源类型", "证据", "计入", "需复核"])
        for row in payload["rows"]:
            writer.writerow([
                row["component"], row["member_group"], row["volume_m3"], row["grade"],
                row["source_type"], row["source_ref"],
                "否" if row["treatment"] in SUBLAYER or row["treatment"] == "exclude" else "是",
                "是" if row["needs_review"] else "否",
            ])
        writer.writerow([])
        writer.writerow(["强度等级", "体积m3", "来源类型"])
        for key, value in payload["by_grade"].items():
            writer.writerow([key, value, "、".join(payload["grade_source_types"].get(key, []))])
        summary = payload["summary"]
        writer.writerow([])
        writer.writerow(["计入合计", summary["counted_total_m3"],
                         "剔除子层", summary["excluded_sublayer_m3"],
                         "推定/未定", summary["unconfirmed_m3"]])


def render_md(payload: dict[str, Any], path: Path) -> None:
    summary = payload["summary"]
    lines = ["# 混凝土分标号台账（%s）" % payload["floor"], ""]
    lines += ["- 计入合计 `%s` m3，剔除子层 `%s` m3，推定/未定 `%s` m3（%s%%）。" % (
        summary["counted_total_m3"], summary["excluded_sublayer_m3"],
        summary["unconfirmed_m3"],
        round((summary["unconfirmed_ratio"] or 0.0) * 100, 2))]
    if _num(summary.get("prefab_sublayer_input_m3")) > 0:
        lines += ["- 叠合板整厚 `%s` m3 已拆：补浇层 `%s` m3 进现浇分账，预制子层 `%s` m3 "
                  "退回装配式采购台账（拆分份额与行级剔除是同一笔体积，不相加）。" % (
                      summary["composite_whole_thickness_m3"],
                      summary["composite_cast_layer_m3"],
                      summary["composite_prefab_sublayer_m3"])]
        lines += ["- 现浇板+板缝+补浇层 `%s` m3 对现浇口径 `%s` m3。" % (
            summary["slab_cast_caliber_m3"], summary["slab_cast_caliber_target_m3"])]
    lines += ["- 需回图确认 `%s` m3（%s%%）。" % (
        summary["needs_review_m3"],
        round((summary["needs_review_ratio"] or 0.0) * 100, 2))]
    lines += ["- 恒等式残差 `%s` m3；分级内部残差 `%s` m3。" % (
        summary["identity_residual_m3"], summary["grade_partition_residual_m3"]), ""]
    lines += ["| 强度等级 | 体积m3 | 来源类型 |", "|---|---:|---|"]
    for key, value in payload["by_grade"].items():
        lines.append("| %s | %s | %s |" % (
            key, value, "、".join(payload["grade_source_types"].get(key, []))))
    split_on = _num(payload["summary"].get("prefab_sublayer_input_m3")) > 0
    header = "| 构件 | 体积m3 |"
    rule = "|---|---:|"
    if split_on:
        header += " 计入现浇m3 | 其中预制子层m3 |"
        rule += "---:|---:|"
    header += " 等级 | 来源 | 计入 | 需复核 |"
    rule += "---|---|---|---|"
    lines += ["", header, rule]
    for row in payload["rows"]:
        line = "| %s | %s |" % (row["component"], row["volume_m3"])
        if split_on:
            cast = row.get("cast_in_place_volume_m3")
            prefab = row.get("prefab_sublayer_volume_m3")
            counted = (row["volume_m3"]
                       if row["treatment"] not in SUBLAYER and row["treatment"] != "exclude"
                       else 0.0)
            line += " %s | %s |" % (
                "-" if cast is None and row.get("member_group") != "composite-whole"
                else (cast if cast is not None else row["volume_m3"]),
                prefab if prefab is not None else "-")
        line += " %s | %s | %s | %s |" % (
            row["grade"], row["source_type"],
            "否" if row["treatment"] in SUBLAYER or row["treatment"] == "exclude" else "是",
            "是" if row["needs_review"] else "否")
        lines.append(line)
    lines += ["", "## 门槛", ""]
    for gate in payload["gates"]:
        lines.append("- `%s` = **%s**：%s" % (gate["id"], gate["status"], gate["evidence"]))
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rules-json", required=True)
    parser.add_argument("--ledger-report-json")
    parser.add_argument("--material-split-json",
                        help="现浇/预制材料分账结果（口径分解 JSON），用于把叠合板整厚"
                             "拆成补浇层与预制子层，现浇报量不再重复计入预制体积")
    parser.add_argument("--expected-total-m3", type=float)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--format", default="all", choices=["all", "json", "csv", "md"])
    args = parser.parse_args()

    rules = load(args.rules_json)
    if not rules.get("rows"):
        raise SystemExit("规则文件缺少 rows")
    report = load(args.ledger_report_json)
    if not str(rules.get("floor") or "").strip():
        rules = dict(rules)
        rules["floor"] = str(report.get("floor")
                             or report.get("floor_label")
                             or (report.get("meta") or {}).get("floor_label")
                             or "")
    expected = args.expected_total_m3
    baseline_source = "cli" if expected is not None else "self"
    if expected is None and rules.get("expected_total_m3") is not None:
        expected = rules.get("expected_total_m3")
        baseline_source = "rules-json"
    if expected is None:
        expected = report_candidate_total(report)
        if expected is not None:
            baseline_source = "ledger-report"
    payload = build_ledger(rules, report,
                           _num(expected) if expected is not None else None,
                           baseline_source, load(args.material_split_json))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1))
    if args.format in ("all", "csv"):
        render_csv(payload, out.with_suffix(".csv"))
    if args.format in ("all", "md"):
        render_md(payload, out.with_suffix(".md"))
    digests = []
    for suffix in (".json", ".csv", ".md"):
        path = out.with_suffix(suffix)
        if path.exists():
            digests.append("%s  %s" % (
                hashlib.sha256(path.read_bytes()).hexdigest(), path))
    out.with_suffix(".sha256").write_text("\n".join(digests) + "\n")
    print(json.dumps({"by_grade": payload["by_grade"], "summary": payload["summary"],
                      "gates": {g["id"]: g["status"] for g in payload["gates"]}},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
