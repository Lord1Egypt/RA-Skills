#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按带宽数把多跨梁在同轴上跨支座续接，量化梁缺口里有多少是链被支座截断造成的。"""



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
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cad-beam-multispan-closure/v0.1"
BEAM_LAYERS = ("S-梁-虚线", "S-梁-实线")
SUPPORT_PREFIXES = ("S-柱", "砼墙", "S-墙")
SPAN_RE = re.compile(r"\((\d+)[A-Za-z]?\)")



def _code_key(value: Any) -> str:
    return _text(value).replace(" ", "").upper()


def _span_count(code: Any) -> int:
    match = SPAN_RE.search(_text(code))
    return int(match.group(1)) if match else 1


def _is_support(layer: str) -> bool:
    return layer.startswith(SUPPORT_PREFIXES)


def _is_beam(layer: str) -> bool:
    return layer in BEAM_LAYERS


def load_segments(dxf_path: Path) -> dict[str, list[dict[str, Any]]]:
    """只读 LINE，按方向、横向位置和沿轴区间归档。"""
    from dev_dxf import readfile

    buckets: dict[str, list[dict[str, Any]]] = {"beam": [], "support": []}
    for entity in readfile(dxf_path).modelspace():
        if entity.dxftype() != "LINE":
            continue
        layer = _text(entity.dxf.layer)
        if not (_is_beam(layer) or _is_support(layer)):
            continue
        start = entity.dxf.start
        end = entity.dxf.end
        if abs(start.y - end.y) <= 1.0:
            orientation, cross = "H", (start.y + end.y) / 2.0
            lo, hi = sorted((start.x, end.x))
        elif abs(start.x - end.x) <= 1.0:
            orientation, cross = "V", (start.x + end.x) / 2.0
            lo, hi = sorted((start.y, end.y))
        else:
            continue
        if hi - lo < 1.0:
            continue
        bucket = "beam" if _is_beam(layer) else "support"
        buckets[bucket].append({
            "handle": _text(entity.dxf.handle), "layer": layer,
            "orientation": orientation, "cross_mm": _round(cross, 1),
            "lo_mm": _round(lo, 1), "hi_mm": _round(hi, 1),
            "length_mm": _round(hi - lo, 1)})
    return buckets


def _near(intervals: list[dict[str, Any]], orientation: str, axis: float,
          tolerance: float) -> list[dict[str, Any]]:
    return [row for row in intervals
            if row["orientation"] == orientation
            and abs(_number(row["cross_mm"]) - axis) <= tolerance]


def close_one_chain(beam: dict[str, Any], buckets: dict[str, list[Any]],
                    options: dict[str, Any]) -> dict[str, Any]:
    """从已建实例两端向外续接，支座算进轴线长，最多补到带宽数。"""
    centerline = beam.get("centerline") or {}
    start = centerline.get("start") or [0.0, 0.0]
    end = centerline.get("end") or [0.0, 0.0]
    orientation = _text(centerline.get("orientation")) or (
        "H" if abs(_number(start[1]) - _number(end[1])) <= 1.0 else "V")
    axis = _number(start[1]) if orientation == "H" else _number(start[0])
    lo, hi = sorted((_number(start[0]) if orientation == "H" else _number(start[1]),
                     _number(end[0]) if orientation == "H" else _number(end[1])))
    axis_tolerance = _number(options.get("axis_tolerance_mm"), 400.0)
    gap_tolerance = _number(options.get("gap_tolerance_mm"), 200.0)
    target_extensions = max(0, _span_count(beam.get("code")) - 1)
    beams = sorted(_near(buckets.get("beam") or [], orientation, axis,
                         axis_tolerance), key=lambda row: _number(row["lo_mm"]))
    supports = sorted(_near(buckets.get("support") or [], orientation, axis,
                            axis_tolerance),
                      key=lambda row: _number(row["lo_mm"]))
    used: set[str] = set()
    added: list[dict[str, Any]] = []
    added_beam_mm = 0.0
    added_support_mm = 0.0
    extensions = 0
    while extensions < target_extensions:
        progressed = False
        for side in ("end", "start"):
            if extensions >= target_extensions:
                break
            if side == "end":
                support = next((row for row in supports
                                if _text(row["handle"]) not in used
                                and _number(row["lo_mm"]) - hi <= gap_tolerance
                                and _number(row["lo_mm"]) >= hi - gap_tolerance),
                               None)
            else:
                support = next((row for row in reversed(supports)
                                if _text(row["handle"]) not in used
                                and lo - _number(row["hi_mm"]) <= gap_tolerance
                                and _number(row["hi_mm"]) <= lo + gap_tolerance),
                               None)
            if support is None:
                continue
            if side == "end":
                nxt = next((row for row in beams
                            if _text(row["handle"]) not in used
                            and abs(_number(row["lo_mm"])
                                    - _number(support["hi_mm"])) <= gap_tolerance
                            and _number(row["hi_mm"]) > hi), None)
            else:
                nxt = next((row for row in reversed(beams)
                            if _text(row["handle"]) not in used
                            and abs(_number(row["hi_mm"])
                                    - _number(support["lo_mm"])) <= gap_tolerance
                            and _number(row["lo_mm"]) < lo), None)
            if nxt is None:
                continue
            used.add(_text(support["handle"]))
            used.add(_text(nxt["handle"]))
            width = _number(support["hi_mm"]) - _number(support["lo_mm"])
            length = _number(nxt["hi_mm"]) - _number(nxt["lo_mm"])
            added.append({"side": side,
                          "support_handle": _text(support["handle"]),
                          "support_layer": _text(support["layer"]),
                          "support_width_mm": _round(width, 1),
                          "beam_handle": _text(nxt["handle"]),
                          "beam_layer": _text(nxt["layer"]),
                          "beam_length_mm": _round(length, 1)})
            added_support_mm += width
            added_beam_mm += length
            if side == "end":
                hi = max(hi, _number(nxt["hi_mm"]))
            else:
                lo = min(lo, _number(nxt["lo_mm"]))
            extensions += 1
            progressed = True
        if not progressed:
            break
    area = _number(beam.get("section_b_mm")) * _number(
        beam.get("section_h_mm")) / 1_000_000.0
    return {
        "beam_id": _text(beam.get("id")),
        "code": _text(beam.get("code")),
        "section": _text(beam.get("section")),
        "orientation": orientation,
        "axis_mm": _round(axis, 1),
        "span_count": _span_count(beam.get("code")),
        "extensions": extensions,
        "current_centerline_mm": _round(_number(
            beam.get("centerline_length_mm")), 1),
        "continued_centerline_mm": _round(hi - lo, 1),
        "added_beam_length_mm": _round(added_beam_mm, 1),
        "added_support_width_mm": _round(added_support_mm, 1),
        "added_axis_length_mm": _round(added_beam_mm + added_support_mm, 1),
        "added_volume_candidate_m3": _round(
            (added_beam_mm + added_support_mm) * area / 1000.0),
        "added_evidence": added,
        "quantity_status": _text(beam.get("quantity_status")),
    }


def build_closure(model: dict[str, Any], buckets: dict[str, list[Any]],
                  reconciliation: dict[str, Any],
                  options: dict[str, Any]) -> dict[str, Any]:
    """只对带宽数 ≥2 的编号做续接，并与参考单实例轴长比较。"""
    reference: dict[str, dict[str, Any]] = {}
    for row in reconciliation.get("beam_code_reconciliation") or []:
        reference[_code_key(row.get("code"))] = row
    rows: list[dict[str, Any]] = []
    for beam in (model.get("members") or {}).get("beams") or []:
        if _span_count(beam.get("code")) < 2:
            continue
        result = close_one_chain(beam, buckets, options)
        ref = reference.get(_code_key(result["code"])) or {}
        single = _number(ref.get("reference_single_axis_length_mm"))
        continued = _number(result["continued_centerline_mm"])
        result["reference_single_axis_length_mm"] = _round(single, 1)
        result["remaining_deficit_mm"] = _round(max(0.0, single - continued), 1)
        result["selected_equivalent_instance_count"] = int(_number(
            ref.get("selected_equivalent_instance_count")))
        result["current_code_difference_m3"] = _round(
            ref.get("current_code_difference_m3"))
        if result["extensions"] == 0:
            result["verdict"] = "no-continuation-found"
        elif single <= 0.0:
            result["verdict"] = "no-reference-single-length"
        elif result["remaining_deficit_mm"] <= 1.0:
            result["verdict"] = "closed-by-continuation"
        else:
            result["verdict"] = "partially-closed-by-continuation"
        rows.append(result)
    added_volume = sum(_number(row["added_volume_candidate_m3"]) for row in rows)
    continued = [row for row in rows if int(row["extensions"]) > 0]
    closed = [row for row in rows if row["verdict"] == "closed-by-continuation"]
    partial = [row for row in rows
               if row["verdict"] == "partially-closed-by-continuation"]
    none = [row for row in rows if row["verdict"] == "no-continuation-found"]
    unreferenced = [row for row in rows
                    if row["verdict"] == "no-reference-single-length"]
    deficit_total = sum(max(0.0, _number(row["reference_single_axis_length_mm"])
                            - _number(row["current_centerline_mm"]))
                        for row in rows)
    deficit_after = sum(_number(row["remaining_deficit_mm"]) for row in rows)
    gates = {
        "multispan-candidates-generated": bool(rows),
        "every-multispan-beam-evaluated": bool(
            rows and len(continued) + len(none) == len(rows)),
        "continuation-covers-deficit": bool(
            rows and deficit_total > 0.0
            and deficit_after <= 0.05 * deficit_total),
        "continuation-evidence-handle-traceable": bool(
            not rows or all(row["added_evidence"] for row in rows
                            if _text(row.get("verdict"))
                            != "no-continuation-found")),
        "applied-to-formal-quantity": False,
    }
    return {
        "schema": SCHEMA,
        "floor": _text(model.get("floor") if isinstance(model.get("floor"), str)
                       else ""),
        "rule": ("带宽数 (n) 的梁允许 n-1 次同轴跨支座续接：支座宽度计入轴线长，"
                 "只登记候选续接量，未经复核不并入混凝土量。"),
        "options": {
            "axis_tolerance_mm": _round(
                options.get("axis_tolerance_mm", 400.0), 1),
            "gap_tolerance_mm": _round(options.get("gap_tolerance_mm", 200.0), 1),
            "geometry_dxf": _text(options.get("geometry_dxf")),
        },
        "summary": {
            "multispan_beam_count": len(rows),
            "codes_covered": len({_code_key(row["code"]) for row in rows}),
            "continued_beam_count": len(continued),
            "closed_beam_count": len(closed),
            "partially_closed_beam_count": len(partial),
            "no_continuation_beam_count": len(none),
            "no_reference_single_beam_count": len(unreferenced),
            "added_beam_length_mm": _round(
                sum(_number(row["added_beam_length_mm"]) for row in rows), 1),
            "added_support_width_mm": _round(
                sum(_number(row["added_support_width_mm"]) for row in rows), 1),
            "added_axis_length_mm": _round(
                sum(_number(row["added_axis_length_mm"]) for row in rows), 1),
            "added_volume_candidate_m3": _round(added_volume),
            "deficit_before_mm": _round(deficit_total, 1),
            "deficit_after_mm": _round(deficit_after, 1),
            "deficit_closed_ratio": _round(
                0.0 if deficit_total <= 0.0
                else (deficit_total - deficit_after) / deficit_total, 4),
        },
        "beams": rows,
        "closure": {"gates": gates},
        "formal_ready": False,
        "applied_to_formal_quantity": False,
    }


def csv_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows: list[list[Any]] = [
        ["section", "beam_id", "code", "span_count", "axis_mm",
         "current_mm", "continued_mm", "added_mm", "added_volume_m3",
         "remaining_deficit_mm", "verdict", "evidence"]]
    for row in result["beams"]:
        evidence = "；".join(
            f"{item['side']}:{item['support_layer']}#{item['support_handle']}"
            f"(+{item['support_width_mm']})→#{item['beam_handle']}"
            f"({item['beam_length_mm']})"
            for item in row["added_evidence"]) or "无续接"
        rows.append(["beam", row["beam_id"], row["code"], row["span_count"],
                     row["axis_mm"], row["current_centerline_mm"],
                     row["continued_centerline_mm"], row["added_axis_length_mm"],
                     row["added_volume_candidate_m3"],
                     row["remaining_deficit_mm"], row["verdict"], evidence])
    return rows


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# 多跨梁跨支座续接候选台账",
        "",
        f"- 规则：{result['rule']}",
        f"- 源文件：`{_text(result['options'].get('geometry_dxf'))}`；"
        f"轴容差 {result['options']['axis_tolerance_mm']} mm、"
        f"端头间隙 {result['options']['gap_tolerance_mm']} mm。",
        f"- 带宽数 ≥2 的梁 {summary['multispan_beam_count']} 根"
        f"（{summary['codes_covered']} 个编号）："
        f"完全闭合 {summary['closed_beam_count']} 根、"
        f"部分闭合 {summary['partially_closed_beam_count']} 根、"
        f"未找到续接 {summary['no_continuation_beam_count']} 根、"
        f"无参考单实例轴长可比 {summary['no_reference_single_beam_count']} 根。",
        f"- 续接补上梁线 "
        f"`{summary['added_beam_length_mm']:.0f}` mm + 支座宽度 "
        f"`{summary['added_support_width_mm']:.0f}` mm = 轴线长 "
        f"`{summary['added_axis_length_mm']:.0f}` mm，"
        f"候选体积 `{summary['added_volume_candidate_m3']:.4f}` m3。",
        f"- 单实例长度缺口从 `{summary['deficit_before_mm']:.0f}` mm 降到 "
        f"`{summary['deficit_after_mm']:.0f}` mm，"
        f"闭合率 {summary['deficit_closed_ratio'] * 100:.1f}%。",
        "",
        "| 实例 | 编号 | 带宽 | 现中心线mm | 续接后mm | 续接补mm | 候选m3 | 剩余缺口mm | 判定 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in result["beams"]:
        lines.append(
            f"| {row['beam_id']} | {row['code']} | {row['span_count']} | "
            f"{row['current_centerline_mm']:.0f} | "
            f"{row['continued_centerline_mm']:.0f} | "
            f"{row['added_axis_length_mm']:.0f} | "
            f"{row['added_volume_candidate_m3']:.4f} | "
            f"{row['remaining_deficit_mm']:.0f} | {row['verdict']} |")
    lines += [
        "",
        "## 续接证据（图面句柄）",
        "",
    ]
    shown = 0
    for row in result["beams"]:
        for item in row["added_evidence"]:
            lines.append(
                f"- `{row['beam_id']}` {row['code']} {item['side']} 端：穿过 "
                f"`{item['support_layer']}#{item['support_handle']}`"
                f"（{item['support_width_mm']:.0f} mm）接 "
                f"`#{item['beam_handle']}`（{item['beam_length_mm']:.0f} mm，"
                f"{item['beam_layer']}）")
            shown += 1
            if shown >= 24:
                break
        if shown >= 24:
            break
    if not shown:
        lines.append("- 未找到可续接的同轴图线。")
    lines += [
        "",
        "## 门槛",
        "",
        "- `" + json.dumps(result["closure"]["gates"], ensure_ascii=False) + "`",
        "- 续接量只作候选：并入混凝土量前须逐条回图确认编号归属与支座性质，"
        "`applied_to_formal_quantity=false`、`formal_ready=false`。",
    ]
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="多跨梁跨支座续接候选台账")
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--geometry-dxf", required=True,
                        help="梁图层展开 DXF（含 S-柱/砼墙 支座线）")
    parser.add_argument("--reconciliation-json", required=True)
    parser.add_argument("--axis-tolerance-mm", type=float, default=400.0)
    parser.add_argument("--gap-tolerance-mm", type=float, default=200.0)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()
    paths = {"model": Path(args.model_json),
             "geometry": Path(args.geometry_dxf),
             "reconciliation": Path(args.reconciliation_json)}
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        parser.error("缺少输入：" + "、".join(missing))
    result = build_closure(
        json.loads(paths["model"].read_text(encoding="utf-8")),
        load_segments(paths["geometry"]),
        json.loads(paths["reconciliation"].read_text(encoding="utf-8")),
        {"axis_tolerance_mm": args.axis_tolerance_mm,
         "gap_tolerance_mm": args.gap_tolerance_mm,
         "geometry_dxf": str(paths["geometry"].resolve())})
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
