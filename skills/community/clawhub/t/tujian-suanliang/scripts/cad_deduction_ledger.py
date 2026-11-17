#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一扣减台账：构件相交与板洞口走一套归属规则，同一空间只扣一次。

相交审计回答"这一格归谁"，洞口审计回答"这块面积扣不扣板"。两本账分开跑会出两类错：
一段对角线既挂复核洞口又挂已扣洞口；洞口格与节点格在平面里压在一起，板扣一次梁再扣一次。
本脚本只做归属与对平，不改任何构件原值，也不改写候选合计。
"""



from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

from cad_common import to_number as _number, to_text as _text  # noqa: E402,F401

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA = "cad-deduction-ledger/v0.1"
CONFIRMED_APERTURE_STATUSES = {"rectangle-x", "closed-polyline", "closed-line-ring"}
EXPLAINED_NOT_OPENING_STATUSES = {
    "annotation-leader", "adjacent-to-confirmed-opening", "out-of-frame",
}
UNRESOLVED_NODE_RULE = "vertical-ownership-unresolved"


def _round(value: Any, places: int = 4) -> float:
    return round(_number(value), places)


def _load(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _handle_key(handles: Any) -> str:
    return "+".join(sorted(_text(item) for item in (handles or []) if _text(item)))


def _bbox_overlap(first: Any, second: Any) -> float:
    """两个 bbox 的重叠面积（m2）；两处存法都是 [x0, y0, x1, y1]。"""
    if not first or not second:
        return 0.0
    dx = min(_number(first[2]), _number(second[2])) - max(_number(first[0]), _number(second[0]))
    dy = min(_number(first[3]), _number(second[3])) - max(_number(first[1]), _number(second[1]))
    if dx <= 0 or dy <= 0:
        return 0.0
    return round(dx * dy / 1.0e6, 6)


def _node_rows(net: dict[str, Any]) -> list[dict[str, Any]]:
    cells = list(net.get("decisions") or [])
    shared_area = sum(_number(cell.get("area_m2")) for cell in cells
                      if _text(cell.get("owner_rule")) != UNRESOLVED_NODE_RULE)
    applied = _number(net.get("applied_deduction_m3"))
    rows = []
    allocated = 0.0
    last_deduct_index = -1
    for index, cell in enumerate(cells):
        if _text(cell.get("owner_rule")) != UNRESOLVED_NODE_RULE:
            last_deduct_index = index
    for index, cell in enumerate(cells):
        unresolved = _text(cell.get("owner_rule")) == UNRESOLVED_NODE_RULE
        area = _number(cell.get("area_m2"))
        if unresolved or shared_area <= 0:
            volume = 0.0
        elif index == last_deduct_index:
            volume = round(applied - allocated, 4)  # 末格吃舍入残差，保证合计与审计值全等
        else:
            volume = _round(area * applied / shared_area)
            allocated = round(allocated + volume, 4)
        rows.append({
            "book": "intersection",
            "id": f"NODE{index + 1:03d}",
            "rule": "node-ownership-unresolved" if unresolved
                    else _text(cell.get("owner_rule")),
            "status": "/".join(_text(item) for item in (cell.get("pair_types") or [])),
            "codes": list(cell.get("codes") or []),
            "bbox_mm": list(cell.get("bbox_mm") or []),
            "area_m2": _round(area),
            "thickness_mm": None,
            "deducted_member_ids": list(cell.get("deducted_member_ids") or []),
            "deduction_volume_m3": volume,
            "applied_in_this_book": not unresolved,
            "review_required": unresolved,
            "evidence": "构件相交审计节点格",
        })
    return rows


def _aperture_rows(records: list[dict[str, Any]],
                   verdict_map: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for index, record in enumerate(records):
        verdict = verdict_map.get(_handle_key(record.get("handles"))) or {}
        judgement = _text(verdict.get("verdict"))
        deduct_area = _number(record.get("deduct_area_m2"))
        envelope = _number(record.get("envelope_area_m2"))
        thickness = _number(record.get("panel_thickness_mm"))
        status = _text(record.get("status"))
        if judgement == "opening":
            area = deduct_area or envelope
            rule = "aperture-user-confirmed"
            applied = bool(verdict.get("applied_in_sheet"))
            review = False
        elif judgement == "not-opening":
            area = 0.0
            rule = "aperture-not-an-opening"
            applied = False
            review = False
        elif status in CONFIRMED_APERTURE_STATUSES:
            area = deduct_area
            rule = "aperture-cad-confirmed"
            applied = False
            review = False
        elif status in EXPLAINED_NOT_OPENING_STATUSES:
            area = 0.0
            rule = "aperture-explained-not-opening"
            applied = False
            review = False
        else:
            area = 0.0
            rule = "aperture-unjudged"
            applied = False
            review = bool(record.get("review_required"))
        rows.append({
            "book": "slab-opening",
            "id": f"AP{index + 1:03d}",
            "rule": rule,
            "status": status,
            "handles": list(record.get("handles") or []),
            "panel_id": _text(record.get("panel_id")),
            "bbox_mm": list(record.get("bbox") or []),
            "area_m2": _round(area),
            "thickness_mm": _round(thickness, 1),
            "deduction_volume_m3": _round(area * thickness / 1000.0),
            "upper_bound_volume_m3": _round(record.get("potential_volume_upper_bound_m3")),
            "applied_in_this_book": applied,
            "review_required": review,
            "evidence": _text(verdict.get("note")) or _text(record.get("evidence")),
        })
    return rows


def build_ledger(intersection: dict[str, Any], opening: dict[str, Any],
                 verdicts: list[dict[str, Any]], sheet: dict[str, Any],
                 options: dict[str, Any] | None = None) -> dict[str, Any]:
    options = dict(options or {})
    tolerance = _number(options.get("tolerance_m3"), 0.0001)
    net = dict(intersection.get("net_quantity") or {})
    verdict_map = {_handle_key(row.get("handles")): row for row in (verdicts or [])}
    nodes = _node_rows(net)
    apertures = _aperture_rows(list(opening.get("records") or []), verdict_map)
    rows = nodes + apertures

    def book_volume(book: str, rule: str | None = None) -> float:
        return round(sum(_number(row.get("deduction_volume_m3")) for row in rows
                         if row["book"] == book
                         and (rule is None or row["rule"] == rule)), 4)

    unresolved_m3 = round(sum(_number(row.get("potential_deduction_volume_m3"))
                              for row in (intersection.get("overlaps") or [])
                              if _text(row.get("pair_type")) == "vertical-vertical"), 4)
    cad_aperture_m3 = book_volume("slab-opening", "aperture-cad-confirmed")
    user_aperture_m3 = book_volume("slab-opening", "aperture-user-confirmed")
    still_review = [row for row in apertures if row["review_required"]]
    sheet_deduction_m3 = round(sum(abs(_number(row.get("volume_m3")))
                                   for row in (sheet.get("rows") or [])
                                   if _text(row.get("treatment")) == "deduction"), 4)
    sheet_residual_m3 = round(sheet_deduction_m3 - user_aperture_m3, 4)
    remaining_gap_m3 = _number(options.get("remaining_gap_m3"))
    gap_share_ratio = round(cad_aperture_m3 / remaining_gap_m3, 4) if remaining_gap_m3 > 0 else 0.0

    deducted_apertures = [row for row in apertures if _number(row.get("area_m2")) > 0]
    applied_nodes = [row for row in nodes if row["applied_in_this_book"]]
    cross_pairs = []
    for aperture in deducted_apertures:
        for cell in applied_nodes:
            area = _bbox_overlap(aperture.get("bbox_mm"), cell.get("bbox_mm"))
            if area > 0:
                cross_pairs.append({
                    "aperture_id": aperture["id"], "node_id": cell["id"],
                    "panel_id": aperture.get("panel_id"),
                    "aperture_handles": aperture.get("handles"),
                    "codes": cell.get("codes"),
                    "overlap_area_m2": area,
                    "double_deduct_volume_m3": _round(
                        area * _number(aperture.get("thickness_mm")) / 1000.0),
                })
    cross_pairs.sort(key=lambda row: -row["overlap_area_m2"])
    cross_double_m3 = round(sum(row["double_deduct_volume_m3"] for row in cross_pairs), 4)

    summary = {
        "row_count": len(rows),
        "intersection_cell_count": len(nodes),
        "aperture_record_count": len(apertures),
        "node_deduction_applied_m3": book_volume("intersection"),
        "node_ownership_unresolved_m3": unresolved_m3,
        "aperture_cad_confirmed_m3": cad_aperture_m3,
        "aperture_user_confirmed_m3": user_aperture_m3,
        "aperture_not_opening_count": len(
            [row for row in apertures if row["rule"] == "aperture-not-an-opening"]),
        "aperture_unjudged_count": len(
            [row for row in apertures if row["rule"] == "aperture-unjudged"]),
        "aperture_explained_not_opening_count": len(
            [row for row in apertures if row["rule"] == "aperture-explained-not-opening"]),
        "aperture_review_pending_count": len(still_review),
        "aperture_review_upper_bound_m3": round(sum(
            _number(row.get("upper_bound_volume_m3")) for row in still_review), 4),
        "sheet_opening_deduction_m3": sheet_deduction_m3,
        "sheet_deduction_residual_m3": sheet_residual_m3,
        "ledger_deducted_total_m3": round(user_aperture_m3 + sheet_residual_m3
                                          * 0 + book_volume("intersection"), 4),
        "remaining_gap_m3": remaining_gap_m3,
        "cad_confirmed_share_of_gap_ratio": gap_share_ratio,
        "cross_book_overlap_pair_count": len(cross_pairs),
        "cross_book_double_deduct_m3": cross_double_m3,
        "total_deduction_candidate_m3": round(
            book_volume("intersection") + unresolved_m3
            + cad_aperture_m3 + user_aperture_m3, 4),
        "applied_to_formal_quantity": False,
    }
    gates = [
        {"id": "deduction-ownership-single-rule",
         "status": "pass" if unresolved_m3 <= tolerance else "warn",
         "evidence": (f"{len(nodes)} 个节点格按一套互斥规则归属"
                      f"（竖向保留节点格、浅梁让深梁），已扣 "
                      f"{summary['node_deduction_applied_m3']} m3；"
                      f"同类竖向构件重叠 {unresolved_m3} m3 只审计不扣"),
         "action": "竖向构件之间归属未定前不得自动扣减，只能挂账等设计口径。"},
        {"id": "deduction-aperture-verdict-closed",
         "status": "pass" if not still_review else "warn",
         "evidence": (f"{len(apertures)} 组开洞图线全部落规则：CAD 自证 {cad_aperture_m3} m3、"
                      f"看图确认 {user_aperture_m3} m3、判非洞口 "
                      f"{summary['aperture_not_opening_count'] + summary['aperture_explained_not_opening_count']} 组"
                      f"（其中图线自证解释 "
                      f"{summary['aperture_explained_not_opening_count']} 组）、"
                      f"未判定 {len(still_review)} 组（上限 "
                      f"{summary['aperture_review_upper_bound_m3']} m3）"),
         "action": "未判定的开洞图线一律不扣板面积；判定结论必须带句柄与原因入台账。"},
        {"id": "deduction-applied-once-across-books",
         "status": "pass" if abs(sheet_residual_m3) <= 0.0005 else "fail",
         "evidence": (f"报量表洞口扣减 {sheet_deduction_m3} m3 对本台账看图确认 "
                      f"{user_aperture_m3} m3，残差 {sheet_residual_m3} m3"),
         "action": "同一笔洞口扣减只能出现在一张表里；残差不为 0 先查哪本账多扣。"},
        {"id": "deduction-slab-opening-attribution-pending",
         "status": "pass" if cad_aperture_m3 <= tolerance else "warn",
         "evidence": (f"CAD 自证洞口 {cad_aperture_m3} m3（{len(deducted_apertures)} 处含已确认格）"
                      f"未进报量表扣减行，占分账剩余量 {remaining_gap_m3} m3 的 "
                      f"{round(gap_share_ratio * 100, 2)}%；是否已含在参考模型板量里"
                      f"未经原模型核对，先挂账不扣"),
         "action": "先确认参考模型的板是否已按同一洞口开洞；已开洞则不重复扣，未开洞才补进扣减行。"},
        {"id": "deduction-no-cross-book-double-count",
         "status": "pass" if not cross_pairs else "fail",
         "evidence": (f"洞口格与节点格重叠 {len(cross_pairs)} 对、"
                      f"潜在重复扣减 {cross_double_m3} m3"
                      + ("" if not cross_pairs else
                         f"；最大 {cross_pairs[0]['overlap_area_m2']} m2"
                         f"（{cross_pairs[0]['aperture_id']}×{cross_pairs[0]['node_id']}）")),
         "action": "重叠格先定归属再扣，否则板和梁会把同一空间各扣一次。"},
    ]
    tally: dict[str, list[float]] = {}
    for row in rows:
        bucket = tally.setdefault(row["rule"], [0.0, 0.0])
        bucket[0] += 1
        bucket[1] = round(bucket[1] + _number(row.get("deduction_volume_m3")), 4)
    rule_tally = [{"rule": key, "row_count": int(count), "deduction_volume_m3": volume}
                  for key, (count, volume) in sorted(tally.items(),
                                                     key=lambda item: -item[1][1])]
    return {"schema": SCHEMA,
            "floor": _text(opening.get("floor") or intersection.get("floor")),
            "summary": summary, "rows": rows, "rule_tally": rule_tally,
            "cross_book_overlaps": cross_pairs[:20],
            "verdicts": list(verdicts or []), "gates": gates,
            "formal_ready": False}


def csv_rows(payload: dict[str, Any]) -> list[list[Any]]:
    head = ["账本", "行ID", "归属规则", "状态/类型", "句柄或构件", "板ID",
            "扣减面积m2", "板厚mm", "扣减体积m3", "已在本账扣", "需复核", "证据"]
    rows = [head]
    for row in payload["rows"]:
        who = "+".join(row.get("handles") or []) or "/".join(row.get("codes") or [])
        rows.append([row["book"], row["id"], row["rule"], row.get("status"),
                     who, row.get("panel_id") or "", row.get("area_m2"),
                     row.get("thickness_mm"), row.get("deduction_volume_m3"),
                     "是" if row.get("applied_in_this_book") else "否",
                     "是" if row.get("review_required") else "否",
                     row.get("evidence")])
    return rows


def render_markdown(payload: dict[str, Any]) -> str:
    s = payload["summary"]
    lines = ["# 统一扣减台账（构件相交 + 板洞口）", ""]
    lines.append(f"节点格 {s['intersection_cell_count']} 格、开洞图线 "
                 f"{s['aperture_record_count']} 组，扣减候选合计 "
                 f"{s['total_deduction_candidate_m3']} m3；跨账潜在重复扣减 "
                 f"{s['cross_book_double_deduct_m3']} m3（{s['cross_book_overlap_pair_count']} 对）。")
    lines.append("")
    lines.append(f"- 相交已扣 {s['node_deduction_applied_m3']} m3；"
                 f"同类竖向未定归属 {s['node_ownership_unresolved_m3']} m3（只审计不扣）")
    lines.append(f"- 洞口：CAD 自证 {s['aperture_cad_confirmed_m3']} m3、"
                 f"看图确认 {s['aperture_user_confirmed_m3']} m3、"
                 f"判非洞口 {s['aperture_not_opening_count']} 组、"
                 f"未判定 {s['aperture_review_pending_count']} 组"
                 f"（上限 {s['aperture_review_upper_bound_m3']} m3）")
    lines.append(f"- 报量表洞口扣减 {s['sheet_opening_deduction_m3']} m3，"
                 f"与本台账看图确认残差 {s['sheet_deduction_residual_m3']} m3")
    lines.append("")
    lines.append("| 归属规则 | 行数 | 扣减体积 m3 |")
    lines.append("|---|---:|---:|")
    for row in payload["rule_tally"]:
        lines.append(f"| {row['rule']} | {row['row_count']} | {row['deduction_volume_m3']} |")
    if payload["cross_book_overlaps"]:
        lines += ["", "## 跨账重叠格（先定归属再扣）", "",
                  "| 洞口 | 节点格 | 重叠 m2 | 潜在重复扣 m3 |", "|---|---|---:|---:|"]
        for row in payload["cross_book_overlaps"]:
            lines.append(f"| {row['aperture_id']}({row['panel_id']}) | "
                         f"{row['node_id']}({'/'.join(row['codes'])}) | "
                         f"{row['overlap_area_m2']} | {row['double_deduct_volume_m3']} |")
    lines.append("")
    for gate in payload["gates"]:
        lines.append(f"- [{gate['status']}] {gate['id']}：{gate['evidence']} "
                     f"处理：{gate['action']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="统一扣减台账（构件相交 + 板洞口）")
    parser.add_argument("--intersection-json", required=True)
    parser.add_argument("--opening-json", required=True)
    parser.add_argument("--verdict-json", default=None,
                        help="开洞看图结论 JSON 列表：handles/verdict/applied_in_sheet/note")
    parser.add_argument("--sheet-json", default=None,
                        help="报量表 JSON，用于核对同一笔洞口扣减是否重复入账")
    parser.add_argument("--tolerance-m3", type=float, default=0.0001)
    parser.add_argument("--remaining-gap-m3", type=float, default=0.0,
                        help="分账剩余不确定量，用于判断未入账洞口的量级")
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    verdicts: list[dict[str, Any]] = []
    if args.verdict_json:
        data = json.loads(Path(args.verdict_json).read_text(encoding="utf-8"))
        verdicts = data if isinstance(data, list) else (
            data.get("verdicts") or data.get("items") or [])
    payload = build_ledger(_load(args.intersection_json), _load(args.opening_json),
                           verdicts, _load(args.sheet_json),
                           {"tolerance_m3": args.tolerance_m3,
                            "remaining_gap_m3": args.remaining_gap_m3})
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    json_path = out.with_suffix(".json")
    csv_path = out.with_suffix(".csv")
    md_path = out.with_suffix(".md")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle).writerows(csv_rows(payload))
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    out.with_name(out.name + ".sha256").write_text("\n".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.resolve()}"
        for path in (json_path, csv_path, md_path)) + "\n", encoding="utf-8")
    print(json.dumps({"summary": payload["summary"],
                      "gates": {row["id"]: row["status"] for row in payload["gates"]},
                      "outputs": [str(json_path), str(csv_path), str(md_path)]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
