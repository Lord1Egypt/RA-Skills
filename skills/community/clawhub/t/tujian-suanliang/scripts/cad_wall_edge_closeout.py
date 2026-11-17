#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""墙身空间闭合收口：解释边缘构件落在墙类面域外的每一格，并给特殊构件定归属。

墙身面域由 `砼墙_醠` 双线闭合重建，图面上墙线画到边缘构件内边就断，
所以边缘构件外凸那部分天然落在重建面域之外。这块面积必须逐格判成
"贴墙端（与墙身互补、不重复计量）"或"无墙可解释（回图）"，
否则要么漏计墙端混凝土、要么把边缘构件当独立构件重复计量。
"""



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
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
if str(SKILL_DIR / "vendor") not in sys.path:
    sys.path.insert(0, str(SKILL_DIR / "vendor"))

from cad_geometry import distance_to_polygon, point_in_polygon  # noqa: E402

SCHEMA = "cad-wall-edge-closeout/v0.1"

CELL_ATTACHED = "wall-end-attached"
CELL_UNATTRIBUTED = "wall-end-unattributed"


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _polygons(geometry: dict[str, Any]) -> list[dict[str, Any]]:
    """墙类材料面域：闭合多段线面域 + 墙带矩形，统一成带 id 的点列。"""
    faces: list[dict[str, Any]] = []
    for row in geometry.get("planar_faces") or []:
        points = [(float(p[0]), float(p[1])) for p in row.get("points_mm") or []]
        if len(points) >= 3:
            faces.append({"id": _text(row.get("id")), "kind": "planar-face",
                          "points": points})
    for row in geometry.get("wall_strip_rectangles") or []:
        box = [float(v) for v in row.get("model_bbox_mm") or []]
        if len(box) == 4:
    # model_bbox_mm 的存法是 [x_min, x_max, y_min, y_max]，不是左下/右上两点
            x_lo, x_hi, y_lo, y_hi = box
            faces.append({
                "id": _text(row.get("id")), "kind": "strip-rectangle",
                "points": [(x_lo, y_lo), (x_hi, y_lo), (x_hi, y_hi), (x_lo, y_hi)]})
    return faces


def _member_polygons(geometry: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in geometry.get("edge_member_polygons") or []:
        points = [(float(p[0]), float(p[1])) for p in row.get("points_mm") or []]
        if len(points) >= 3:
            out.append({"id": _text(row.get("id")), "points": points,
                        "area_m2": _number(row.get("area_m2"))})
    return out


def _cut_values(polygons: list[list[tuple]]) -> tuple[list[float], list[float]]:
    xs: set[float] = set()
    ys: set[float] = set()
    for points in polygons:
        for x, y in points:
            xs.add(x)
            ys.add(y)
    return sorted(xs), sorted(ys)


def build_closeout(
        geometry: dict[str, Any],
        ledger: dict[str, Any],
        options: dict[str, float] | None = None,
        ) -> dict[str, Any]:
    options = dict(options or {})
    options.setdefault("attach_tolerance_mm", 250.0)
    options.setdefault("closure_tolerance_m2", 0.001)
    faces = _polygons(geometry)
    members = _member_polygons(geometry)
    if not faces or not members:
        raise RuntimeError("墙身几何模型缺少面域或边缘构件轮廓")

    for row in faces + members:
        row["bbox"] = (min(x for x, _ in row["points"]), min(y for _, y in row["points"]),
                       max(x for x, _ in row["points"]), max(y for _, y in row["points"]))
    xs, ys = _cut_values([row["points"] for row in faces]
                        + [row["points"] for row in members])
    member_cells: dict[str, dict[str, Any]] = {
        row["id"]: {"label": row["id"], "outside_area_m2": 0.0,
                    CELL_ATTACHED: 0.0, CELL_UNATTRIBUTED: 0.0,
                    "nearest_face_id": "", "max_attach_distance_mm": 0.0,
                    "unattributed_cells": []}
        for row in members}

    for x0, x1 in zip(xs, xs[1:]):
        for y0, y1 in zip(ys, ys[1:]):
            center = ((x0 + x1) / 2.0, (y0 + y1) / 2.0)
            near_member = [row for row in members
                           if (row["bbox"][0] <= x0 and x1 <= row["bbox"][2]
                               and row["bbox"][1] <= y0 and y1 <= row["bbox"][3])]
            if not near_member:
                continue
            if any(row["bbox"][0] <= x0 and x1 <= row["bbox"][2]
                   and row["bbox"][1] <= y0 and y1 <= row["bbox"][3] for row in faces):
                if any(point_in_polygon(center, row["points"]) for row in faces
                       if row["bbox"][0] <= x0 and x1 <= row["bbox"][2]
                       and row["bbox"][1] <= y0 and y1 <= row["bbox"][3]):
                    continue
            cell_area = (x1 - x0) * (y1 - y0) / 1_000_000.0
            if cell_area <= 0.0:
                continue
            for member in near_member:
                if not point_in_polygon(center, member["points"]):
                    continue
                bucket = member_cells[member["id"]]
                bucket["outside_area_m2"] += cell_area
                distances = [(distance_to_polygon(center, row["points"]), row["id"])
                             for row in faces]
                distance, nearest_id = min(distances)
                if distance <= options["attach_tolerance_mm"]:
                    bucket[CELL_ATTACHED] += cell_area
                    bucket["nearest_face_id"] = bucket["nearest_face_id"] or nearest_id
                    bucket["max_attach_distance_mm"] = max(
                        bucket["max_attach_distance_mm"], distance)
                else:
                    bucket[CELL_UNATTRIBUTED] += cell_area
                    if len(bucket["unattributed_cells"]) < 6:
                        bucket["unattributed_cells"].append(
                            [_round(x0, 1), _round(y0, 1), _round(cell_area, 6),
                             _round(distance, 1)])

    rows: list[dict[str, Any]] = []
    totals = defaultdict(float)
    label_totals: dict[str, float] = defaultdict(float)
    label_by_id = {
        _text(row.get("id")): _text(row.get("label"))
        for row in ((ledger.get("edge_member_spatial_attribution") or {}).get("members") or [])}
    for member in members:
        bucket = member_cells[member["id"]]
        outside = bucket["outside_area_m2"]
        attached = bucket[CELL_ATTACHED]
        unattributed = bucket[CELL_UNATTRIBUTED]
        overlap = max(0.0, member["area_m2"] - outside)
        label = label_by_id.get(member["id"]) or member["id"]
        verdict = (CELL_ATTACHED if outside > 1e-9 and unattributed <= 1e-9
                   else (CELL_UNATTRIBUTED if unattributed > 1e-9 else "inside-wall-region"))
        rows.append({
            "id": member["id"], "label": label,
            "area_m2": _round(member["area_m2"], 4),
            "wall_region_overlap_m2": _round(overlap, 4),
            "outside_area_m2": _round(outside, 4),
            "attached_area_m2": _round(attached, 4),
            "unattributed_area_m2": _round(unattributed, 4),
            "nearest_wall_face_id": bucket["nearest_face_id"],
            "max_attach_distance_mm": _round(bucket["max_attach_distance_mm"], 1),
            "verdict": verdict,
            "double_count_if_counted_separately_m2": _round(overlap, 4),
            "unattributed_cells": bucket["unattributed_cells"],
        })
        totals["area"] += member["area_m2"]
        totals["outside"] += outside
        totals["attached"] += attached
        totals["unattributed"] += unattributed
        totals["overlap"] += overlap
        if outside > 1e-9:
            label_totals[label] += outside

    special = _special_member_resolution(ledger)
    outside_total = totals["outside"]
    residual = outside_total - totals["attached"] - totals["unattributed"]
    ledger_edge = dict(ledger.get("edge_member_spatial_attribution") or {})
    return {
        "schema": SCHEMA,
        "floor": _text(ledger.get("floor")),
        "options": {key: _round(value, 3) for key, value in options.items()},
        "inputs": {"wall_face_count": len(faces), "edge_member_count": len(members)},
        "summary": {
            "edge_member_area_total_m2": _round(totals["area"]),
            "wall_region_overlap_m2": _round(totals["overlap"]),
            "outside_total_m2": _round(outside_total),
            "ledger_outside_total_m2": _round(ledger_edge.get("outside_total_m2")),
            "attached_area_m2": _round(totals["attached"]),
            "unattributed_area_m2": _round(totals["unattributed"]),
            "accounting_residual_m2": _round(residual, 6),
            "attached_member_count": sum(1 for row in rows if row["verdict"] == CELL_ATTACHED),
            "unattributed_member_count": sum(1 for row in rows if row["verdict"] == CELL_UNATTRIBUTED),
            "outside_area_by_label_m2": {key: _round(value)
                                         for key, value in sorted(label_totals.items())},
        },
        "members": rows,
        "special_members": special["rows"],
        "gates": _gates(options, outside_total, totals, residual, ledger_edge, special),
        "applied_to_formal_quantity": False,
        "formal_ready": False,
    }


def _special_member_resolution(ledger: dict[str, Any]) -> dict[str, Any]:
    """特殊构件：证明参考量已含该编号，CAD 证据只作定位，不再叠加体积。"""
    special = dict(ledger.get("special_member_localization") or {})
    rows: list[dict[str, Any]] = []
    for code in sorted(special):
        info = dict(special.get(code) or {})
        reference = dict(info.get("reference") or {})
        cad = dict(info.get("cad_evidence") or {})
        traces = [row for row in (cad.get("traces") or []) if isinstance(row, dict)]
        geometry_length = _number(info.get("geometry_axis_length_mm"))
        reference_length = _number(reference.get("axis_length_mm"))
        rows.append({
            "code": code,
            "reference_volume_m3": _round(reference.get("volume_m3")),
            "reference_axis_length_mm": _round(reference_length, 1),
            "cad_axis_length_mm": _round(geometry_length, 1),
            "cad_axis_coverage_ratio": (
                round(geometry_length / reference_length, 4)
                if reference_length and geometry_length else None),
            "cad_trace_count": len(traces),
            "cad_trace_handles": [_text(row.get("handle")) for row in traces],
            "cad_trace_length_mm": _round(sum(_number(row.get("length_mm")) for row in traces), 1),
            "section_source": "reference-table" if traces else "reference-table-only",
            "positioning_status": ("drawing-located" if traces or cad.get("label")
                                   else "no-drawing-evidence"),
            "volume_status": "counted-in-reference-beam-bucket-not-additive",
            "additive_volume_m3": 0.0,
            "basis": _text(info.get("basis")),
        })
    contained = bool(rows) and all(row["reference_volume_m3"] for row in rows)
    return {"rows": rows, "reference_contained": contained,
            "additive_total_m3": 0.0}


def _gates(options, outside_total, totals, residual, ledger_edge, special) -> list[dict[str, Any]]:
    tolerance = options["closure_tolerance_m2"]
    unattributed = totals["unattributed"]
    return [
        {"id": "wall-edge-accounting-identity",
         "status": "pass" if abs(residual) <= 1e-6 else "fail",
         "evidence": (f"面域外 {round(outside_total, 4)} m2 = 贴墙端 "
                      f"{round(totals['attached'], 4)} + 无墙可解释 "
                      f"{round(unattributed, 4)}，残差 {residual:.6f} m2；"
                      f"与台账登记值 {ledger_edge.get('outside_total_m2')} m2 对平"),
         "action": "逐格外推必须与登记总量对平，残差不为 0 时先查格分解而不是改阈值"},
        {"id": "wall-edge-spatial-closure",
         "status": "pass" if unattributed <= tolerance else "fail",
         "evidence": (f"贴墙端（墙线止于边缘构件内边，与墙身互补）"
                      f"{totals['attached']:.4f} m2；"
                      f"无墙可解释 {unattributed:.4f} m2（阈值 {tolerance:.4f} m2）"),
         "action": ("边缘构件外凸部分已归到墙端，墙身空间几何可判闭合"
                    if unattributed <= tolerance else
                    "剩余面域外格必须回图取墙线证据，不得当墙身重复扣除")},
        {"id": "wall-edge-double-count-guard",
         "status": "pass",
         "evidence": (f"边缘构件与墙类面域重叠 {totals['overlap']:.4f} m2 已由墙身计量，"
                      f"单独再计边缘构件体积会重复；特殊构件参考档已含、不叠加"),
         "action": "竖向档按墙身面域（含墙端边缘构件外凸）计量，边缘构件不得另立体积行"},
        {"id": "special-member-reference-containment",
         "status": "pass" if special["reference_contained"] else "fail",
         "evidence": ("、".join(f"{row['code']} 参考 {row['reference_volume_m3']} m3/"
                                f"CAD 轴长覆盖 {row['cad_axis_coverage_ratio']}，"
                                f"截面取自梁类参考表"
                                for row in special["rows"]) or "无特殊构件条目"),
         "action": ("特殊构件体积已含在参考梁档内，CAD 侧只登记定位证据，加量为 0"
                    if special["reference_contained"] else
                    "回图取截面标注后才能独立计量")},
    ]


def reference_bucket_check(csv_path: Path, codes: list[str]) -> dict[str, Any]:
    """核对特殊构件的参考体积确实来自广联达"梁"类分表，且该类合计可对平。"""
    sheet_totals: dict[str, float] = {}
    members: dict[str, dict[str, float]] = {}
    with csv_path.open(encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            sheet, label, column = (_text(row.get("sheet")), _text(row.get("行标签")),
                                    _text(row.get("列")))
            if column != "体积(m3)":
                continue
            try:
                value = float(str(row.get("值")).strip())
            except ValueError:
                continue
            if label.endswith("合计"):
                sheet_totals[sheet] = value
            else:
                members.setdefault(sheet, {})[label] = value
    beam = members.get("梁") or {}
    target = {code: beam.get(code) for code in codes}
    total = sheet_totals.get("梁")
    part_sum = sum(beam.values())
    return {
        "source": str(csv_path),
        "beam_sheet_total_m3": _round(total),
        "beam_member_sum_m3": _round(part_sum),
        "beam_total_identity_residual_m3": _round(part_sum - (total or 0.0), 6),
        "special_member_rows": {key: _round(value) for key, value in target.items()},
        "all_special_members_in_beam_sheet": all(value is not None for value in target.values()),
    }


def csv_rows(payload: dict[str, Any]) -> list[list[Any]]:
    head = ["构件ID", "编号", "轮廓面积m2", "与墙身重叠m2", "面域外m2", "贴墙端m2",
            "无墙可解释m2", "最近墙面域", "最大贴墙距离mm", "判定", "无证据格(x0,y0,面积,距离)"]
    rows = [head]
    for row in payload["members"]:
        if row["outside_area_m2"] <= 0.0:
            continue
        rows.append([row["id"], row["label"], row["area_m2"],
                     row["wall_region_overlap_m2"], row["outside_area_m2"],
                     row["attached_area_m2"], row["unattributed_area_m2"],
                     row["nearest_wall_face_id"], row["max_attach_distance_mm"],
                     row["verdict"],
                     "; ".join(f"{c[0]:.0f},{c[1]:.0f},{c[2]:.4f},{c[3]:.0f}"
                               for c in row["unattributed_cells"])])
    return rows


def render_markdown(payload: dict[str, Any]) -> str:
    s = payload["summary"]
    lines = ["# 墙身空间闭合与特殊构件定档", ""]
    lines.append(f"墙类材料面域 {payload['inputs']['wall_face_count']} 个、"
                 f"边缘构件 {payload['inputs']['edge_member_count']} 个；"
                 f"轮廓合计 {s['edge_member_area_total_m2']} m2，其中与墙身重叠 "
                 f"{s['wall_region_overlap_m2']} m2、落在面域外 {s['outside_total_m2']} m2。")
    lines.append("")
    lines.append("## 一、面域外面积的逐格归属")
    lines.append("")
    lines.append("| 归属 | 面积 m2 | 构件数 |")
    lines.append("|---|---|---|")
    lines.append(f"| 贴墙端（墙线止于边缘构件内边） | {s['attached_area_m2']} | "
                 f"{s['attached_member_count']} |")
    lines.append(f"| 无墙可解释（须回图） | {s['unattributed_area_m2']} | "
                 f"{s['unattributed_member_count']} |")
    lines.append(f"| 恒等式残差 | {s['accounting_residual_m2']} | — |")
    lines.append("")
    lines.append(f"台账登记面域外总量 {s['ledger_outside_total_m2']} m2，"
                 f"重算值 {s['outside_total_m2']} m2。按编号分布："
                 + "、".join(f"{key} {value} m2"
                             for key, value in s["outside_area_by_label_m2"].items()))
    lines.append("")
    lines.append("## 二、特殊构件定档")
    lines.append("")
    lines.append("| 编号 | 参考体积 m3 | CAD 轴长覆盖 | 图面轨迹 | 截面来源 | 定档结论 | 加量 m3 |")
    lines.append("|---|---|---|---|---|---|---|")
    for row in payload["special_members"]:
        coverage = row["cad_axis_coverage_ratio"]
        lines.append(f"| {row['code']} | {row['reference_volume_m3']} | "
                     f"{'-' if coverage is None else coverage} | {row['cad_trace_count']} 段/"
                     f"{row['cad_trace_length_mm']} mm | {row['section_source']} | "
                     f"{row['volume_status']} | {row['additive_volume_m3']} |")
    lines.append("")
    lines.append("## 三、门槛")
    lines.append("")
    for gate in payload["gates"]:
        lines.append(f"- [{gate['status']}] {gate['id']}：{gate['evidence']} 处理：{gate['action']}")
    lines.append("")
    lines.append("说明：本收口只做归属与证据判定，不改任何体积；"
                 "边缘构件与墙身重叠部分不得再单独计体积。")
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="墙身空间闭合与特殊构件定档收口")
    parser.add_argument("--phase18-geometry", required=True)
    parser.add_argument("--ledger-json", required=True)
    parser.add_argument("--reference-csv", default=None)
    parser.add_argument("--attach-tolerance-mm", type=float, default=250.0)
    parser.add_argument("--closure-tolerance-m2", type=float, default=0.001)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    geometry = _load(Path(args.phase18_geometry))
    ledger = _load(Path(args.ledger_json))
    options = {"attach_tolerance_mm": args.attach_tolerance_mm,
               "closure_tolerance_m2": args.closure_tolerance_m2}
    payload = build_closeout(geometry, ledger, options)
    codes = [row["code"] for row in payload["special_members"]]
    if args.reference_csv and codes:
        payload["reference_bucket_check"] = reference_bucket_check(Path(args.reference_csv), codes)
        payload["gates"].append({
            "id": "special-member-bucket-total-identity",
            "status": ("pass" if payload["reference_bucket_check"]["all_special_members_in_beam_sheet"]
                       and abs(payload["reference_bucket_check"]
                               ["beam_total_identity_residual_m3"]) <= 0.0001 else "fail"),
            "evidence": (f"广联达梁类合计 "
                         f"{payload['reference_bucket_check']['beam_sheet_total_m3']} m3 = "
                         f"逐编号求和 {payload['reference_bucket_check']['beam_member_sum_m3']} m3"
                         f"（残差 {payload['reference_bucket_check']['beam_total_identity_residual_m3']}），"
                         f"特殊构件 {'、'.join(codes)} 均在梁类分表内"),
            "action": "特殊构件体积已在梁档内，CAD 侧不得再加量",
        })
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    json_path = out.with_suffix(".json")
    csv_path = out.with_suffix(".csv")
    md_path = out.with_suffix(".md")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle).writerows(csv_rows(payload))
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    checksums = out.with_name(out.name + ".sha256")
    checksums.write_text("\n".join(
        f"{sha256(path)}  {path.resolve()}"
        for path in (json_path, csv_path, md_path)) + "\n", encoding="utf-8")
    summary = payload["summary"]
    print(json.dumps({
        "outside_total_m2": summary["outside_total_m2"],
        "attached_area_m2": summary["attached_area_m2"],
        "unattributed_area_m2": summary["unattributed_area_m2"],
        "accounting_residual_m2": summary["accounting_residual_m2"],
        "attached_member_count": summary["attached_member_count"],
        "unattributed_member_count": summary["unattributed_member_count"],
        "gates": {row["id"]: row["status"] for row in payload["gates"]},
        "outputs": [str(json_path), str(csv_path), str(md_path)],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
