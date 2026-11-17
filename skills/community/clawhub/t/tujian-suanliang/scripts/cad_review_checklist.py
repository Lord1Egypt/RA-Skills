#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从统一算量报告生成"待人工确认清单"：一行一件可核对的事。

报告里的门槛和台账说明"还差多少量"，但现场要的是一张能拿着回图逐条打勾的表。
本脚本把梁、板、洞口、异常记录、特殊构件和门槛按影响量排序合并，
每条给出构件编号、问题、需要确认什么、影响量、图面坐标和句柄，
末尾留空的"确认结果/确认人/日期"三列供现场填写。
"""



from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

from cad_common import to_number as _number  # noqa: E402,F401

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA = "cad-review-checklist/v0.1"
CLOSED_WORDS = ("closed", "confirmed", "independent-cad", "counted")
REVIEW_WORDS = ("not-independent", "reference-only", "not-closed", "partially",
                "candidate", "review", "missing", "unresolved", "pending",
                "unknown", "issue", "assumed", "inferred")
REVIEW_ASK = {
    "anomaly": "按报告说明回图核对该构件状态，确认是否影响计量",
    "slab": "确认该块板的属性（板厚来源、洞口、材料体系）是否需要改档",
    "beam": "核对支座性质与净跨：是柱/墙支座、复核支座还是悬挑自由端",
    "slab-thickness": "确认板厚取自图面标注还是说明默认值，必要时按设计变更改档",
    "slab-opening": "确认该处是否真洞口（风管/井道/楼梯间），量级按洞口面积乘板厚",
    "special-member": "确认特殊梁的截面与根数，能否按 CAD 独立计量",
    "edge-member": "确认边缘构件轮廓与墙类面域的关系，避免重复扣除",
    "intersection": "确认两构件重叠处按谁计量，避免同一空间算两次",
    "beam-conflict": "同一条绘制线上两个编号谁成立：只改编号归属，不改几何",
    "gate": "本门槛未闭合，需按说明回图或补口径",
}

def _text(value: Any) -> str:
    return str(value if value is not None else "").strip()


def _needs_review(value: Any) -> bool:
    text = _text(value).lower()
    if not text:
        return False
    if any(word in text for word in REVIEW_WORDS):
        return True  # 先认未闭合词，避免 not-independent 被 independent-cad 吃掉
    return not any(word in text for word in CLOSED_WORDS)


def _row(category: str, ident: str, issue: str, impact_m3: float,
         where: str = "", handle: str = "", ask: str = "",
         countable: bool = True) -> dict[str, Any]:
    return {"category": category, "item": ident, "issue": issue,
            "impact_m3": round(abs(impact_m3), 4), "where": where,
            "handle": handle, "countable": countable,
            "ask": ask or REVIEW_ASK.get(category, REVIEW_ASK["gate"])}


OPEN_QUANTITY_ITEMS = (
    ("slab_seam_band_volume_m3", "slab-seam", "板缝条带与广联达单列板缝重叠",
     "确认紧邻预制板 350 mm 条带是否就是广联达单列板缝，避免两边都算"),
    ("slab_thickness_volume_swing_m3", "slab-thickness",
     "板厚图例冲突造成的体积摆动", "按设计确认这几块板取图例厚还是归档厚"),
    ("slab_opening_review_volume_upper_bound_m3", "slab-opening",
     "待复核洞口的扣减上限", "逐组回图确认是否真洞口（风管、井道、楼梯间）"),
    ("prefab_gap_volume_at_design_thickness_m3", "prefab-coverage",
     "预制板展开面积对设计书的缺口折算体积",
     "确认预制底板编号展开是否漏图，或设计口径含后浇带"),
    ("grade_ledger_needs_review_m3", "grade", "分标号仍需回图确认的量",
     "确认未定档构件（梁未分解残差）的强度等级归属"),
    ("beam_dedup_missing_instance_volume_m3", "beam-instance",
     "run 口径未配对、模型缺实例的体积", "按编号回图数根数，确认是漏画还是重复标注"),
    ("beam_residual_needing_new_geometry_m3", "beam-geometry",
     "判为确实缺几何需要补画的梁体积", "按坐标回图确认该段梁是否真的没画"),
    ("beam_residual_still_unexplained_m3", "beam-geometry",
     "窗口内仍未解释的梁覆盖缺口", "扩大检索窗口或人工看图确认覆盖范围"),
)
RISK_ONLY_ITEMS = (
    ("glodon_prefab_sublayer_double_count_m3", "prefab-scope",
     "参考量里预制底板叠在叠合板整厚之上的重复量（属口径选择）",
     "与广联达确认按整厚还是整厚加预制两层口径报量"),
    ("beam_dedup_double_count_volume_m3", "beam-instance",
     "梁双口径重复计量风险量", "先按编号定责再决定是否扣减，不与上面相加"),
    ("beam_conflict_double_count_risk_m3", "beam-instance",
     "同轴/同线双标注的重复计量风险量", "逐对确认哪根梁成立，只改归属不改总量"),
)


# 统一扣减台账把洞口图线逐组定性后，"待复核洞口上限"这种整块风险量就该换成
# 台账里真正没落账的那几笔，否则清单会把已经判过的图线再报一遍。
LEDGER_SUPERSEDED_ITEMS = {"slab_opening_review_volume_upper_bound_m3"}
# 逐对定主之后，整块"两口径相加风险"要被归属后剩余风险取代：已定主部分只剩编号归属问题，
# 不再是需要人核对的量；两者并存会把同一笔重叠报两遍。
CONFLICT_SUPERSEDED_ITEMS = {"beam_conflict_double_count_risk_m3"}
# 归属后剩余风险仍是"两口径可能相加"的风险量，不是确定的缺量，所以走风险桶；
# 逐对行只是它的明细，量值写在问题文字里、impact 记 0，避免同一笔被加两遍。
CONFLICT_RISK_ITEMS = (
    ("beam_conflict_residual_risk_m3", "beam-instance",
     "定主后仍未归属的重叠段风险（逐对明细见 beam-conflict 行）",
     "按逐对坐标定跨或定主，未定前两个编号不得相加"),
)
BEAM_CONFLICT_SCHEMA = "cad-beam-attribution-conflict/v0.1"
LEDGER_QUANTITY_ITEMS = (
    ("deduction_aperture_cad_confirmed_m3", "slab-opening",
     "CAD 自证洞口未进报量扣减行",
     "先确认参考模型的板是否已按同一洞口开洞；未开洞才补扣减行"),
    ("deduction_node_unresolved_m3", "intersection",
     "同类竖向构件重叠归属未定", "确认墙、柱、边缘构件相交时按谁计量"),
)


def collect_open_quantities(report: dict[str, Any]) -> list[dict[str, Any]]:
    """把 direct_outputs 里已经算出来的未闭合量逐条搬进清单。"""
    outputs = dict(report.get("direct_outputs") or {})
    ledger_used = "deduction_aperture_cad_confirmed_m3" in outputs
    conflict_used = "beam_conflict_residual_risk_m3" in outputs
    risk_items = list(RISK_ONLY_ITEMS)
    if conflict_used:
        risk_items = [item for item in risk_items
                      if item[0] not in CONFLICT_SUPERSEDED_ITEMS] + list(CONFLICT_RISK_ITEMS)
    items = list(OPEN_QUANTITY_ITEMS) + risk_items
    if ledger_used:
        items = [item for item in items
                 if item[0] not in LEDGER_SUPERSEDED_ITEMS] + list(LEDGER_QUANTITY_ITEMS)
    rows = []
    for key, category, issue, ask in items:
        value = _number(outputs.get(key))
        if abs(value) <= 1e-9:
            continue
        rows.append(_row(category, key, "%s：%.4f" % (issue, value), value,
                         ask=ask, countable=key not in dict(
                             (item[0], item[1]) for item in risk_items)))
    return rows


def collect_beams(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for beam in report.get("beam_schedule") or []:
        status = _text(beam.get("quantity_status")) or _text(beam.get("issue"))
        if not _needs_review(status):
            continue
        volume = _number(beam.get("gross_volume_m3")) - _number(beam.get("clear_volume_m3"))
        rows.append(_row(
            "beam", _text(beam.get("code")) or _text(beam.get("id")),
            "状态 %s；截面 %s，支座 %s 个，中心线 %s mm，净长 %s mm" % (
                status, _text(beam.get("section")),
                _text(beam.get("support_count")),
                _text(beam.get("centerline_length_mm")),
                _text(beam.get("clear_length_mm"))),
            abs(volume),
            "X=%s Y=%s" % (_text(beam.get("x")), _text(beam.get("y"))),
            _text(beam.get("source"))))
    return rows


def collect_slabs(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for panel in report.get("slab_schedule") or []:
        area = _number(panel.get("net_area_m2")) or _number(panel.get("area_m2"))
        thickness = _number(panel.get("thickness_mm"))
        source = _text(panel.get("source"))
        opening = _text(panel.get("opening_status"))
        volume = area * thickness / 1e6
        if _needs_review(source) and "label" not in source.lower():
            rows.append(_row(
                "slab-thickness", _text(panel.get("code")) or _text(panel.get("id")),
                "板厚 %s mm 取自 %s；净面积 %.4f m2" % (
                    _text(panel.get("thickness_mm")), source, area),
                volume, _text(panel.get("status"))))
        if _needs_review(opening) and _number(panel.get("opening_area_m2")) > 0:
            rows.append(_row(
                "slab-opening", _text(panel.get("code")) or _text(panel.get("id")),
                "洞口状态 %s；洞口 %.4f m2，扣减约 %.4f m3" % (
                    opening, _number(panel.get("opening_area_m2")),
                    _number(panel.get("opening_area_m2")) * thickness / 1e6),
                _number(panel.get("opening_area_m2")) * thickness / 1e6,
                "%s 处洞口" % _text(panel.get("opening_count"))))
    return rows


def collect_special(report: dict[str, Any]) -> list[dict[str, Any]]:
    concrete = dict(report.get("concrete") or {})
    ledger = dict(concrete.get("ledger") or concrete)
    rows = []
    for code, info in sorted(dict(ledger.get("special_member_localization") or {}).items()):
        info = dict(info or {})
        status = _text(info.get("volume_status") or info.get("status"))
        if not _needs_review(status):
            continue
        reference = dict(info.get("reference") or {})
        rows.append(_row(
            "special-member", code,
            "状态 %s；参考体积 %s m3，轴长覆盖 %s" % (
                status, _text(reference.get("volume_m3")),
                _text(info.get("axis_coverage_ratio"))),
            _number(reference.get("volume_m3")),
            _text((info.get("cad_evidence") or {}).get("trace_count")) + " 条轨迹",
            _text((info.get("cad_evidence") or {}).get("traces"))))
    edge = dict(ledger.get("edge_member_spatial_attribution") or {})
    if _needs_review(edge.get("status")):
        rows.append(_row(
            "edge-member", "边缘构件合计",
            "面域外面积 %.4f m2（阈值 %.4f m2），完全在面域外 %s 个" % (
                _number(edge.get("outside_total_m2")),
                _number(edge.get("outside_review_tolerance_m2"), 0.001),
                _text(edge.get("fully_outside_member_count"))),
            _number(edge.get("outside_total_m2")),
            "共 %s 根边缘构件" % _text(edge.get("edge_member_count")),
            str(edge.get("remaining_gate") or "")))
    return rows


def collect_beam_conflicts(report: dict[str, Any]) -> list[dict[str, Any]]:
    """未定主的梁编号冲突逐对成行：给 run/梁编号、判据、引线句柄与回图坐标。"""
    rows: list[dict[str, Any]] = []
    for item in (report.get("supplemental_breakdown") or {}).values():
        if _text(item.get("schema")) != BEAM_CONFLICT_SCHEMA:
            continue
        for row in item.get("conflicts") or []:
            owner = dict(row.get("ownership") or {})
            if _text(owner.get("status")) != "review-open":
                continue
            where = ", ".join(_text(value) for value in (row.get("review_xy") or []))
            rows.append(_row(
                "beam-conflict",
                "%s×%s" % (_text(row.get("run_id")), _text(row.get("beam_id"))),
                "%s 与 %s 判 `%s`：%s，重叠 %s mm（重叠比 %s）、风险 %s m3" % (
                    _text(row.get("run_code")), _text(row.get("beam_code")),
                    _text(row.get("verdict")), _text(owner.get("rule")),
                    _text(row.get("overlap_mm")), _text(row.get("overlap_ratio")),
                    _text(row.get("double_count_risk_m3"))),
                0.0, where, "|".join(row.get("label_leader_ids") or []),
                ask="同一条绘制线上两个编号谁成立：按引线落点与支座定主，只改编号不改几何"))
    return rows


def collect_gates(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for gate in (report.get("closure_dashboard") or {}).get("gates") or []:
        if _text(gate.get("status")) in ("pass",):
            continue
        rows.append(_row(
            "gate", _text(gate.get("id")),
            "%s：%s" % (_text(gate.get("title")), _text(gate.get("evidence"))),
            0.0, _text(gate.get("action"))))
    return rows


def collect_anomalies(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in report.get("anomalies") or []:
        if _text(item.get("severity")) not in ("warning", "error", "critical"):
            continue
        rows.append(_row(
            _text(item.get("member_type")) or "anomaly",
            _text(item.get("code")) or _text(item.get("member_id")),
            _text(item.get("message")), 0.0,
            "%s/%s" % (_text(item.get("area")), _text(item.get("status")))))
    return rows


def build_checklist(report: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for collector in (collect_open_quantities, collect_beams, collect_slabs,
                      collect_special, collect_beam_conflicts, collect_anomalies,
                      collect_gates):
        rows.extend(collector(report))
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = (row["category"], row["item"])
        if key in merged:
            merged[key]["issue"] += "；" + row["issue"]
            merged[key]["impact_m3"] = round(
                merged[key]["impact_m3"] + row["impact_m3"], 4)
            merged[key]["countable"] = bool(
                merged[key].get("countable") and row.get("countable"))
            continue
        merged[key] = dict(row)
    ordered = sorted(merged.values(),
                     key=lambda row: (-row["impact_m3"], row["category"], row["item"]))
    by_category: dict[str, dict[str, Any]] = {}
    for row in ordered:
        bucket = by_category.setdefault(row["category"], {"count": 0, "impact_m3": 0.0})
        bucket["count"] += 1
        if row.get("countable"):
            bucket["impact_m3"] = round(bucket["impact_m3"] + row["impact_m3"], 4)
        else:
            bucket.setdefault("non_additive_m3", 0.0)
            bucket["non_additive_m3"] = round(
                bucket["non_additive_m3"] + row["impact_m3"], 4)
    return {
        "schema": SCHEMA,
        "floor": _text(report.get("floor_label")),
        "source_report_schema": _text(report.get("schema")),
        "rows": ordered,
        "summary": {
            "item_count": len(ordered),
            "total_impact_m3": round(sum(
                row["impact_m3"] for row in ordered if row.get("countable")), 4),
            "non_additive_m3": round(sum(
                row["impact_m3"] for row in ordered
                if not row.get("countable")), 4),
            "by_category": by_category,
        },
    }


def render_csv(payload: dict[str, Any], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["序号", "类别", "构件/项目", "问题", "影响量m3",
                         "图面位置", "证据", "需要确认什么", "确认结果", "确认人", "日期"])
        for index, row in enumerate(payload["rows"], 1):
            writer.writerow([index, row["category"], row["item"], row["issue"],
                             row["impact_m3"], row["where"], row["handle"],
                             row["ask"], "", "", ""])
        writer.writerow([])
        writer.writerow(["合计条目", payload["summary"]["item_count"],
                         "影响量合计m3", payload["summary"]["total_impact_m3"]])


def render_md(payload: dict[str, Any], path: Path) -> None:
    lines = ["# 待人工确认清单（%s）" % (payload["floor"] or "未标楼层"), "",
             "- 共 **%d** 条待确认，可量化影响合计 **%.4f m3**。" % (
                 payload["summary"]["item_count"],
                 payload["summary"]["total_impact_m3"]),
             "- 另有 **%.4f m3** 属重复计量风险或口径选择，与其他条目可能重叠，不参与合计。" % (
                 payload["summary"].get("non_additive_m3") or 0.0),
             "- 每行给了图面位置或证据，确认结果列留空待填。", "",
             "| 类别 | 条数 | 影响量m3 |", "|---|---:|---:|"]
    for key, bucket in sorted(payload["summary"]["by_category"].items(),
                              key=lambda item: -item[1]["impact_m3"]):
        lines.append("| %s | %d | %.4f |" % (key, bucket["count"], bucket["impact_m3"]))
    lines += ["", "| # | 类别 | 构件/项目 | 问题 | 影响量m3 | 需要确认什么 |",
              "|---:|---|---|---|---:|---|"]
    for index, row in enumerate(payload["rows"][:60], 1):
        lines.append("| %d | %s | %s | %s | %s | %s |" % (
            index, row["category"], row["item"], row["issue"][:90],
            row["impact_m3"], row["ask"]))
    lines += ["", "（Markdown 只列前 60 条，完整清单见同目录 CSV。）"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, help="统一算量报告 JSON")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--format", default="all", choices=["all", "csv", "md"])
    args = parser.parse_args()

    report = json.loads(Path(args.report).expanduser().read_text(encoding="utf-8"))
    payload = build_checklist(report)
    out = Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
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
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
