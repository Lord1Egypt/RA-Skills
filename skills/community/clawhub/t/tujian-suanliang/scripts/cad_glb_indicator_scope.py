#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读广联达模型云指标（清单口径）与按构件导出（构件实物量口径），逐类对账并划出 CAD 结构算量的范围边界。"""



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


SCHEMA = "cad-glb-indicator-scope/v0.1"
MAIN_SHEETS = ("梁", "连梁", "剪力墙", "柱", "现浇板")
ASSEMBLY_SHEETS = ("叠合板(整厚)", "叠合板(预制底板)", "板缝")
SECONDARY_SHEETS = ("构造柱", "圈梁", "过梁")
STAIR_SHEETS = ("直形梯段",)
MISC_SHEETS = ("台阶", "挑檐", "栏板", "坡道")
CLASS_TO_SHEET = {
    ("柱", "框架柱"): "柱",
    ("柱", "构造柱"): "构造柱",
    ("墙", "剪力墙"): "剪力墙",
    ("墙", "连梁"): "连梁",
    ("梁", "梁"): "梁",
    ("梁", "过梁"): "过梁",
    ("梁", "圈梁"): "圈梁",
    ("板", "现浇板"): "现浇板",
    ("楼梯", "直形梯段"): "直形梯段",
    ("零星", "台阶"): "台阶",
    ("零星", "挑檐"): "挑檐",
    ("零星", "栏板"): "栏板",
}
VOLUME_KEYS = ("体积(m3)", "预制部分体积（按模型）(m3)")



def _indent(value: Any) -> int:
    text = _text(value)
    return len(text) - len(text.lstrip())


def read_indicator(path: Path, floor: str) -> tuple[float, dict]:
    """解析 混凝土-构件类型楼层指标表 与 混凝土-部位楼层指标表。"""
    try:
        import openpyxl
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "需要 openpyxl 读取指标报表，请改用 Codex 主运行时的 python3") from exc
    book = openpyxl.load_workbook(str(path), data_only=True, read_only=True)
    try:
        type_sheet = next((name for name in book.sheetnames
                           if "构件类型" in name and "混凝土" in name), None)
        part_sheet = next((name for name in book.sheetnames
                           if "部位楼层" in name and "混凝土" in name), None)
        if not type_sheet or not part_sheet:
            raise SystemExit("指标报表缺少混凝土构件类型表或部位楼层表")
        schedule: dict[tuple, float] = {}
        category = subclass = ""
        for row in book[type_sheet].iter_rows(values_only=True):
            depth = _indent(row[0])
            title = _text(row[0]).strip()
            if not title or "名称" in title or "总量" in title:
                continue
            if depth == 0:
                category, subclass = title, ""
            elif depth <= 2:
                subclass = title
            elif depth == 4 and title == floor:
                schedule[(category, subclass)] = _round(row[1])
        total = 0.0
        for row in book[part_sheet].iter_rows(values_only=True):
            if _text(row[0]).strip() == floor:
                total = _round(row[1])
                break
        if not schedule or not total:
            raise SystemExit("指标报表里没有 %s 的混凝土数据" % floor)
        return total, schedule
    finally:
        book.close()


def read_component_export(payload: dict, floor: str) -> tuple:
    """按构件导出：每张表本层体积/投影面积/块数合计，另回传现浇板明细行。"""
    sheets: dict = {}
    areas: dict = {}
    counts: dict = {}
    slab_rows: list = []
    for name, block in (payload.get("sheets") or {}).items():
        rows = [row for row in (block.get("first_floor_rows") or [])
                if _text(row.get("楼层")) in ("", floor)]
        total = 0.0
        area = 0.0
        count = 0
        for row in rows:
            for key in VOLUME_KEYS:
                if key in row:
                    total += _number(row[key])
            area += _number(row.get('投影面积(m2)'))
            count += int(_number(row.get('数量(块)')))
        sheets[name] = round(total, 4)
        areas[name] = round(area, 4)
        counts[name] = count
        if name == "现浇板":
            slab_rows = rows
    return sheets, areas, counts, slab_rows


def _bucket(names, sheets, title, cad_scope, note, in_schedule):
    return {
        "bucket": title,
        "volume_m3": round(sum(sheets.get(sheet, 0.0) for sheet in names), 4),
        "cad_scope": cad_scope,
        "in_schedule": in_schedule,
        "note": note,
    }


def reconcile(indicator_total, schedule, sheets, areas, counts,
              slab_rows, options) -> dict:
    floor = options.get("floor") or "首层"
    outside_sheets = list(options.get("outside_schedule_sheets")
                          or tuple(ASSEMBLY_SHEETS) + ("坡道",))
    schedule_class_total = round(sum(schedule.values()), 4)
    export_total = round(sum(sheets.values()), 4)
    outside_schedule = round(sum(sheets.get(sheet, 0.0)
                                 for sheet in outside_sheets), 4)
    schedule_only = round(sum(
        qty for key, qty in schedule.items() if key not in CLASS_TO_SHEET), 4)
    residual = round(export_total - indicator_total
                     - outside_schedule + schedule_only, 4)
    main = round(sum(sheets.get(sheet, 0.0) for sheet in MAIN_SHEETS), 4)
    assembly = round(sum(sheets.get(sheet, 0.0)
                         for sheet in ASSEMBLY_SHEETS), 4)
    prefab = _round(sheets.get("叠合板(预制底板)"))
    whole = _round(sheets.get("叠合板(整厚)"))
    seam = _round(sheets.get("板缝"))
    cast = _round(sheets.get("现浇板"))
    secondary = round(sum(sheets.get(sheet, 0.0)
                          for sheet in SECONDARY_SHEETS), 4)
    stair = round(sum(sheets.get(sheet, 0.0) for sheet in STAIR_SHEETS), 4)
    misc = round(sum(sheets.get(sheet, 0.0) for sheet in MISC_SHEETS), 4)
    slab_total_a = round(cast + whole + seam, 4)
    slab_cast_a = round(cast + (whole - prefab) + seam, 4)
    cad_slab = _number(options.get("cad_slab_volume_m3"))
    cad_beam = _number(options.get("cad_beam_independent_m3"))
    cad_vertical = _number(options.get("cad_vertical_candidate_m3"))
    reference_total = _number(options.get("reference_total_m3"))
    deduped_reference = round(main + assembly - prefab, 4)
    cad_core = round(cad_beam + cad_vertical, 4)
    cad_total = round(cad_core + cad_slab, 4)
    class_rows: list = []
    for (category, subclass), qty in sorted(schedule.items(),
                                            key=lambda item: -item[1]):
        sheet = CLASS_TO_SHEET.get((category, subclass))
        own = sheets.get(sheet) if sheet else None
        class_rows.append({
            "schedule_class": category,
            "schedule_subclass": subclass,
            "schedule_m3": qty,
            "export_sheet": sheet or "无对应表",
            "export_m3": own,
            "difference_m3": None if own is None else round(own - qty, 4),
            "in_export": sheet is not None,
            "note": "" if sheet else "清单有、构件实物量导出无",
        })
    for sheet in outside_sheets:
        class_rows.append({
            "schedule_class": "（不在清单口径）",
            "schedule_subclass": sheet,
            "schedule_m3": None,
            "export_sheet": sheet,
            "export_m3": sheets.get(sheet),
            "difference_m3": None,
            "in_export": True,
            "note": "构件实物量有、清单总量不含（装配式板层或零星现浇构件）",
        })
    cast_purity = bool(slab_rows) and all(
        _text(row.get("是否叠合板后浇")) == "否" for row in slab_rows)
    anomalies: dict = {}
    for row in slab_rows:
        name = _text(row.get("名称"))
        match = re.search(r"(\d{2,3})\s*$", name)
        area = _number(row.get("投影面积(m2)"))
        if not match or area <= 0:
            continue
        nominal = int(match.group(1))
        implied = round(_number(row.get("体积(m3)")) / area * 1000.0, 1)
        if abs(implied - nominal) > 5.0:
            anomalies[name] = {
                "nominal_thickness_mm": nominal,
                "implied_thickness_mm": implied,
                "volume_m3": _round(row.get("体积(m3)")),
                "projected_area_m2": area,
            }
    buckets = [
        _bucket(MAIN_SHEETS, sheets,
                "主体结构（梁/连梁/剪力墙/框架柱/现浇板）", "in-scope",
                "与 CAD 结构平面图同源，是算量内核的比对目标", True),
        _bucket(ASSEMBLY_SHEETS, sheets,
                "装配式板层（叠合整厚/预制底板/板缝）",
                "in-scope-material-split",
                "清单总量不含；预制底板是叠合整厚的子层，按材料分账不得叠加", False),
        _bucket(SECONDARY_SHEETS, sheets,
                "二次结构（构造柱/圈梁/过梁）", "out-of-scope",
                "建筑二次设计构件，结构平面图无对应几何，不计入本层结构混凝土", True),
        _bucket(STAIR_SHEETS, sheets,
                "楼梯（直形梯段）", "out-of-scope-partial",
                "当前分账只含楼梯梁，梯段本体未计，需另立台账", True),
        _bucket(MISC_SHEETS, sheets,
                "建筑零星（台阶/挑檐/栏板/坡道）", "out-of-scope",
                "占清单本层比例高，几乎全部落在结构算量范围之外", True),
    ]
    whole_area = _number(areas.get("叠合板(整厚)"))
    prefab_area = _number(areas.get("叠合板(预制底板)"))
    ratio = round(prefab_area / whole_area, 4) if whole_area else None
    whole_count = counts.get("叠合板(整厚)") or 0
    prefab_count = counts.get("叠合板(预制底板)") or 0
    whole_block = round(whole_area / whole_count, 4) if whole_count else None
    prefab_block = round(prefab_area / prefab_count, 4) if prefab_count else None
    cad_count = int(_number(options.get("cad_outline_count")))
    cad_area = _number(options.get("cad_outline_area_m2"))
    cad_block = round(cad_area / cad_count, 4) if cad_count else None
    ratio_within = bool(ratio and 0.75 <= ratio <= 0.98)
    cad_layer_match = bool(cad_block and prefab_block
                           and abs(cad_block - prefab_block) / prefab_block < 0.10)
    basis_ratio = (
        "预制底板投影面积 %s m2 是叠合板整厚 %s m2 的 %.2f%%，余量 %s m2 与板缝同量级，"
        "符合条板铺设加后浇层的子层构造%s" % (
            prefab_area, whole_area, (ratio or 0) * 100.0,
            round(whole_area - prefab_area, 4),
            ("；CAD 叠合板轮廓 %d 块单块均面积 %.4f m2，与预制底板单块 %.4f m2 同量级、"
             "与整厚板单块 %.4f m2 差 %.1f 倍，说明图面画的是预制条板层。") % (
                cad_count, cad_block or 0.0, prefab_block or 0.0,
                whole_block or 0.0,
                (whole_block / cad_block) if (whole_block and cad_block) else 0.0)
            if cad_block else "。"))
    tolerance = _number(options.get("residual_tolerance_m3"), 0.05)
    checks = {
        "schedule_class_sum_equals_total": abs(
            schedule_class_total - indicator_total) < 0.05,
        "bucket_sum_equals_export_total": abs(
            sum(row["volume_m3"] for row in buckets) - export_total) < 0.001,
        "cross_caliber_residual_within_tolerance": abs(residual) <= tolerance,
        "all_cast_in_place_rows_not_composite_topping": cast_purity,
        "previous_reference_equals_main_plus_assembly": (
            abs(main + assembly - reference_total) < 0.001
            if reference_total else None),
    }
    closure = {
        "schedule-class-sum-closed": bool(
            checks["schedule_class_sum_equals_total"]),
        "cross-caliber-reconciled": bool(
            checks["cross_caliber_residual_within_tolerance"]),
        "prefab-sublayer-deduplicated": prefab <= 0.0,
        "prefab-sublayer-ratio-consistent": ratio_within,
        "scope-boundary-declared": bool(buckets),
        "applied-to-formal-quantity": False,
    }
    gates = [
        {"id": "schedule-class-sum", "title": "清单分类合计闭合",
         "status": "pass" if checks[
             "schedule_class_sum_equals_total"] else "fail",
         "evidence": "分类和 %s 对 部位楼层总量 %s" % (
             schedule_class_total, indicator_total)},
        {"id": "cross-caliber-reconcile", "title": "两种广联达口径互相勾稽",
         "status": "pass" if closure["cross-caliber-reconciled"] else "fail",
         "evidence": "构件实物量 %s = 清单 %s + 口径外 %s - 清单独有 %s + 残差 %s" % (
             export_total, indicator_total, outside_schedule,
             schedule_only, residual)},
        {"id": "prefab-sublayer-double-count", "title": "预制底板子层重复计量",
         "status": "pass" if closure[
             "prefab-sublayer-deduplicated"] else "fail",
         "evidence": "现参考量含预制底板 %s m3 叠加在叠合板整厚之上，去重后应为 %s m3" % (
             prefab, deduped_reference)},
        {"id": "scope-boundary", "title": "算量范围边界", "status": "warn",
         "evidence": "二次结构 %s + 楼梯 %s + 零星 %s m3 不在 CAD 结构图范围" % (
             secondary, stair, misc)},
        {"id": "slab-caliber", "title": "叠合板口径判定", "status": "warn",
         "evidence": "判 A 的依据是现浇板行全为非叠合后浇加面积包含关系；"
                     "CAD 现浇板 %s m3 对现浇口径 %s m3 差 %s m3 只作参考不作证据" % (
                         cad_slab, slab_cast_a,
                         round(cad_slab - slab_cast_a, 4))},
    ]
    next_actions = [
        "板体系按材料分账：现浇 %s + 预制 %s，参考总量由 %s 降为 %s。" % (
            slab_cast_a, prefab, reference_total or "-", deduped_reference),
        "CAD 板体系只对标现浇口径 %s，预制底板另立装配式构件台账。" % slab_cast_a,
        "梯段 %s m3 单列；二次结构 %s 与建筑零星 %s 标为范围外，"
        "不得再用来解释 CAD 缺口。" % (stair, secondary, misc),
        "对外固定三条口径：结构主体去重 %s / 广联达清单 %s / 构件实物量 %s。" % (
            deduped_reference, indicator_total, export_total),
    ]
    return {
        "schema": SCHEMA,
        "title": "广联达清单口径分解与混凝土算量范围边界（%s）" % floor,
        "floor": floor,
        "sources": {
            "indicator_xlsx": str(options.get("indicator_path") or ""),
            "component_export_json": str(options.get("export_path") or ""),
            "indicator_md5": _text(options.get("indicator_md5")),
        },
        "summary": {
            "schedule_first_floor_total_m3": indicator_total,
            "schedule_class_sum_m3": schedule_class_total,
            "export_first_floor_total_m3": export_total,
            "schedule_only_m3": schedule_only,
            "outside_schedule_m3": outside_schedule,
            "main_structure_m3": main,
            "assembly_slab_m3": assembly,
            "prefab_sublayer_m3": prefab,
            "slab_caliber_A_total_m3": slab_total_a,
            "slab_cast_in_place_caliber_A_m3": slab_cast_a,
            "secondary_structure_m3": secondary,
            "stair_m3": stair,
            "building_misc_m3": misc,
            "cross_caliber_residual_m3": residual,
            "previous_reference_total_m3": reference_total or None,
            "double_count_prefab_m3": prefab,
            "prefab_area_m2": prefab_area,
            "whole_thickness_area_m2": whole_area,
            "prefab_over_whole_area_ratio": ratio,
            "prefab_mean_block_area_m2": prefab_block,
            "whole_mean_block_area_m2": whole_block,
            "cad_outline_mean_block_area_m2": cad_block,
            "de_duped_reference_total_m3": deduped_reference,
            "cad_slab_independent_m3": cad_slab or None,
            "cad_vs_slab_caliber_A_diff_m3": (
                round(cad_slab - slab_cast_a, 4) if cad_slab else None),
            "beam_cad_independent_m3": cad_beam or None,
            "cad_independent_verifiable_m3": cad_core or None,
            "cad_independent_with_slab_m3": cad_total or None,
            "cad_independent_with_slab_ratio_to_deduped": (
                round(cad_total / deduped_reference, 6)
                if deduped_reference and cad_total else None),
        },
        "identity_checks": checks,
        "class_rows": class_rows,
        "scope_buckets": buckets,
        "slab_caliber": {
            "verdict": "A（预制底板是叠合整厚的子层，不得叠加）"
            if cast_purity and whole > prefab and ratio_within else "unverified",
            "checks": {"cast_row_purity": cast_purity,
                       "prefab_inside_whole": whole > prefab,
                       "area_ratio_consistent": ratio_within,
                       "cad_outline_is_prefab_layer": cad_layer_match},
            "basis": [
                "现浇板行的 是否叠合板后浇 全部为 否，且现浇板合计与清单现浇板相同，"
                "说明后浇层不在现浇板内，只能在叠合板(整厚)内。",
                basis_ratio,
                "CAD 现浇板量与现浇口径的总量吻合只作参考，不作为口径证据："
                "阶段四十一证明 CAD 板面域同时含纯现浇与叠合区整厚，两个方向相反的"
                "误差会互相抵消（纯现浇差 %s m3、叠合区整厚差 %s m3）。" % (
                    "+1.7259", "-16.8615"),
            ],
            "non_evidence": "CAD 与现浇口径的总量巧合不作为证据，"
                            "见阶段四十一的口径拆解。",
            "residual_risk": "逐厚档与逐块仍未闭合，口径判定只解决重复计量，"
                             "不构成板体系闭合。",
            "cast_row_thickness_anomalies": anomalies,
            "area_warning": "广联达现浇板名称标厚与体积/投影面积反算不符，"
                            "不得用体积除面积反算板厚。" if anomalies else "",
        },
        "next_actions": next_actions,
        "closure": closure,
        "gates": gates,
        "formal_ready": False,
    }


def csv_rows(result: dict) -> list:
    rows = [["清单类别", "清单中类", "清单m3", "构件表", "构件m3", "差m3", "备注"]]
    for row in result["class_rows"]:
        rows.append([
            _text(row["schedule_class"]), _text(row["schedule_subclass"]),
            _text(row["schedule_m3"]), _text(row["export_sheet"]),
            _text(row["export_m3"]), _text(row["difference_m3"]),
            _text(row["note"]),
        ])
    rows.append([])
    rows.append(["范围桶", "CAD范围", "m3", "计入清单", "说明", "", ""])
    for row in result["scope_buckets"]:
        rows.append([_text(row["bucket"]), _text(row["cad_scope"]),
                     _text(row["volume_m3"]),
                     "是" if row["in_schedule"] else "否",
                     _text(row["note"]), "", ""])
    rows.append([])
    rows.append(["门槛", "状态", "证据", "", "", "", ""])
    for row in result["gates"]:
        rows.append([_text(row["id"]), _text(row["status"]),
                     _text(row["evidence"]), "", "", "", ""])
    return rows


def render_markdown(result: dict) -> str:
    summary = result["summary"]
    lines = [
        "# " + result["title"], "",
        "- 清单口径总量与构件实物量逐类对账，残差只允许四舍五入量级；"
        "范围外类别不得再用来解释 CAD 缺口。",
        "- 广联达清单口径 **%s m3**，构件实物量 **%s m3**，勾稽残差 **%s m3**。" % (
            summary["schedule_first_floor_total_m3"],
            summary["export_first_floor_total_m3"],
            summary["cross_caliber_residual_m3"]),
        "- 参考量 %s = 主体 %s + 装配式板层 %s，其中预制底板 %s 属子层，"
        "去重后 **%s m3**。" % (
            summary["previous_reference_total_m3"], summary["main_structure_m3"],
            summary["assembly_slab_m3"], summary["prefab_sublayer_m3"],
            summary["de_duped_reference_total_m3"]),
        "- CAD 独立可核 %s m3（梁+墙柱），含 CAD 独立板量 %s m3。" % (
            summary["cad_independent_verifiable_m3"],
            summary["cad_independent_with_slab_m3"]), "",
        "| 范围桶 | m3 | CAD 范围 | 计入清单 |", "|---|---:|---|---|",
    ]
    for row in result["scope_buckets"]:
        lines.append("| %s | %s | %s | %s |" % (
            row["bucket"], row["volume_m3"], row["cad_scope"],
            "是" if row["in_schedule"] else "否"))
    lines += ["", "## 逐类对照", "",
              "| 清单类别 | 清单m3 | 构件表 | 构件m3 | 差m3 |",
              "|---|---:|---|---:|---:|"]
    for row in result["class_rows"]:
        lines.append("| %s/%s | %s | %s | %s | %s |" % (
            row["schedule_class"], row["schedule_subclass"],
            "-" if row["schedule_m3"] is None else row["schedule_m3"],
            row["export_sheet"],
            "-" if row["export_m3"] is None else row["export_m3"],
            "-" if row["difference_m3"] is None else row["difference_m3"]))
    lines += ["", "## 口径判定", ""]
    for text in result["slab_caliber"]["basis"]:
        lines.append("- " + text)
    if result["slab_caliber"]["area_warning"]:
        lines.append("- " + result["slab_caliber"]["area_warning"])
    lines += ["", "## 下一步", ""]
    for index, text in enumerate(result["next_actions"], 1):
        lines.append("%d. %s" % (index, text))
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="广联达清单口径与构件实物量口径逐类对账，输出算量范围边界")
    parser.add_argument("--indicator-xlsx", required=True,
                        help="广联达模型云指标 xlsx")
    parser.add_argument("--component-export-json", required=True,
                        help="按构件导出结果 cad-glb-concrete-reference/v0.1")
    parser.add_argument("--floor", default="首层")
    parser.add_argument("--reference-total-m3", type=float, default=0.0,
                        help="现行台账参考总量，用于判定预制底板是否重复计量")
    parser.add_argument("--cad-slab-volume-m3", type=float, default=0.0)
    parser.add_argument("--cad-beam-independent-m3", type=float, default=0.0)
    parser.add_argument("--cad-vertical-candidate-m3", type=float, default=0.0)
    parser.add_argument("--residual-tolerance-m3", type=float, default=0.05)
    parser.add_argument("--cad-outline-count", type=int, default=0,
                        help="CAD 叠合板轮廓块数，用于比对图面画的是预制层还是整厚层")
    parser.add_argument("--cad-outline-area-m2", type=float, default=0.0,
                        help="CAD 叠合板轮廓总面积 m2")
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()
    indicator = Path(args.indicator_xlsx)
    export_path = Path(args.component_export_json)
    if not indicator.exists():
        parser.error("缺少输入：%s" % indicator)
    if not export_path.exists():
        parser.error("缺少输入：%s" % export_path)
    sheets, areas, counts, slab_rows = read_component_export(
        json.loads(export_path.read_text(encoding="utf-8")), args.floor)
    indicator_total, schedule = read_indicator(indicator, args.floor)
    result = reconcile(indicator_total, schedule, sheets, areas, counts,
                       slab_rows, {
        "floor": args.floor,
        "indicator_path": indicator,
        "export_path": export_path,
        "indicator_md5": hashlib.md5(indicator.read_bytes()).hexdigest(),
        "reference_total_m3": args.reference_total_m3,
        "cad_slab_volume_m3": args.cad_slab_volume_m3,
        "cad_beam_independent_m3": args.cad_beam_independent_m3,
        "cad_vertical_candidate_m3": args.cad_vertical_candidate_m3,
        "residual_tolerance_m3": args.residual_tolerance_m3,
        "cad_outline_count": args.cad_outline_count,
        "cad_outline_area_m2": args.cad_outline_area_m2,
    })
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
        "%s  %s" % (sha256(path), path.resolve())
        for path in (json_path, csv_path, md_path)) + "\n", encoding="utf-8")
    print(json.dumps({"schema": result["schema"], "summary": result["summary"],
                      "closure": result["closure"],
                      "formal_ready": result["formal_ready"]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
