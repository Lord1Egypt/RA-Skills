#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验梁实例中心线在图面上有无成对梁线支撑，无支撑者判幻影中心线并退出台账。

背景：按轴线推定的实例中心线可能只是轴网/中心线，图面并没有对应梁。此类实例
既不扣也不加，必须先退出分标号台账，否则实例口径会被当报量依据。
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
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
VENDOR_DIR = SKILL_DIR / "vendor"
if VENDOR_DIR.exists() and str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

from cad_beam_coverage_audit import (  # noqa: E402
    BEAM_LAYERS, _normalize_entities, _read_entities)

SCHEMA = "cad-beam-centerline-support/v0.1"

VERIFIED = "centerline-verified"
PARTIAL = "centerline-partial"
LENGTH_GAP = "centerline-length-unsupported"
SINGLE = "centerline-single-line"
PHANTOM = "centerline-axis-phantom"
EXCLUDED_STATUSES = (LENGTH_GAP, SINGLE, PHANTOM)


def _merge(spans: list[list[float]]) -> list[list[float]]:
    out: list[list[float]] = []
    for low, high in sorted(spans):
        if high <= low:
            continue
        if out and low <= out[-1][1] + 1.0:
            out[-1][1] = max(out[-1][1], high)
        else:
            out.append([low, high])
    return out


def _clip(spans: list[list[float]], low: float, high: float) -> float:
    return sum(max(0.0, min(high, end) - max(low, start)) for start, end in spans)


def _instance_geometry(row: dict[str, Any], basis: str) -> dict[str, Any] | None:
    """把 run/beam 两种口径统一成（朝向, 轴线, 区间, 梁宽）。"""
    if basis == "run":
        orientation = _text(row.get("orientation"))
        axis = _number(row.get("axis_mm"))
        low, high = sorted((_number(row.get("start_mm")), _number(row.get("end_mm"))))
        width = _number(row.get("paired_width_mm")) or _number(row.get("section_b_mm"))
        code, volume = _text(row.get("matched_code")), _number(row.get("volume_m3"))
    else:
        line = row.get("centerline") or {}
        start = line.get("start") or [0.0, 0.0]
        end = line.get("end") or [0.0, 0.0]
        orientation = _text(line.get("orientation")) or (
            "H" if abs(_number(start[1]) - _number(end[1])) <= 1.0 else "V")
        if orientation == "H":
            axis, low, high = _number(start[1]), _number(start[0]), _number(end[0])
        else:
            axis, low, high = _number(start[0]), _number(start[1]), _number(end[1])
        low, high = sorted((low, high))
        width = _number(row.get("section_b_mm"))
        code, volume = _text(row.get("code")), _number(row.get("gross_volume_m3"))
    if orientation not in ("H", "V") or high - low <= 1.0:
        return None
    return {
        "id": _text(row.get("id")), "code": code or "（未编号）", "basis": basis,
        "orientation": orientation, "axis_mm": _round(axis, 1),
        "start_mm": _round(low, 1), "end_mm": _round(high, 1),
        "length_mm": _round(high - low, 1),
        "width_mm": _round(width, 1), "volume_m3": _round(volume),
    }


def _pairs_for_width(
        rows: list[dict[str, Any]],
        width: float,
        options: dict[str, float],
        ) -> list[dict[str, Any]]:
    """同朝向线段按"间距≈梁宽且轴向重叠达标"配对，结果按（朝向, 梁宽）缓存。"""
    key = (rows[0]["orientation"] if rows else "?", _round(width, 0))
    cache = options.setdefault("_pair_cache", {})
    hit = cache.get(key)
    if hit is not None:
        return hit
    pairs: list[dict[str, Any]] = []
    for first_index, first in enumerate(rows):
        for second in rows[first_index + 1:]:
            gap = abs(_number(first["axis_mm"]) - _number(second["axis_mm"]))
            if abs(gap - width) > options["width_tolerance_mm"]:
                continue
            start = max(_number(first["start_mm"]), _number(second["start_mm"]))
            end = min(_number(first["end_mm"]), _number(second["end_mm"]))
            if end - start < options["pair_min_overlap_mm"]:
                continue
            pairs.append({
                "center": (_number(first["axis_mm"]) + _number(second["axis_mm"])) / 2.0,
                "start": start, "end": end,
                "handles": (first["handle"], second["handle"])})
    cache[key] = pairs
    return pairs


def _support(
        instance: dict[str, Any],
        segments: list[dict[str, Any]],
        options: dict[str, float],
        ) -> dict[str, Any]:
    """统计实例区间上的成对梁线覆盖，并给出最近实测线对供中心线纠偏取证。"""
    axis = _number(instance["axis_mm"])
    width = _number(instance["width_mm"]) or options["default_width_mm"]
    low, high = _number(instance["start_mm"]), _number(instance["end_mm"])
    same = [row for row in segments if row["orientation"] == instance["orientation"]]
    pairs = _pairs_for_width(same, width, options)
    matched = [row for row in pairs
               if abs(_number(row["center"]) - axis) <= options["axis_slack_mm"]]
    pair_length = _clip(_merge([[row["start"], row["end"]] for row in matched]), low, high)
    face_band = width / 2.0 + options["face_tolerance_mm"]
    single_length = _clip(_merge([
        [_number(row["start_mm"]), _number(row["end_mm"])] for row in same
        if abs(_number(row["axis_mm"]) - axis) <= face_band]), low, high)
    length = high - low
    pair_ratio = pair_length / length
    single_ratio = single_length / length
    # 分档：覆盖达标 / 部分覆盖 / 该轴有实测线对但本区间没覆盖 / 只有单边线 / 该轴无线对（幻影）
    if pair_ratio >= options["verified_ratio"]:
        status = VERIFIED
    elif pair_ratio >= options["partial_ratio"]:
        status = PARTIAL
    elif matched:
        status = LENGTH_GAP
    elif single_ratio >= options["partial_ratio"]:
        status = SINGLE
    else:
        status = PHANTOM
    covered = _merge([[max(low, row["start"]), min(high, row["end"])] for row in matched])
    gaps: list[list[float]] = []
    cursor = low
    for start, end in covered:
        if start > cursor + options["min_gap_report_mm"]:
            gaps.append([_round(cursor, 1), _round(start, 1)])
        cursor = max(cursor, end)
    if cursor < high - options["min_gap_report_mm"]:
        gaps.append([_round(cursor, 1), _round(high, 1)])
    nearest: dict[str, Any] | None = None
    if status in (PHANTOM, SINGLE):
        usable = [row for row in pairs
                  if min(high, _number(row["end"])) - max(low, _number(row["start"]))
                  >= options["pair_min_overlap_mm"]]
        if usable:
            nearest = min(usable, key=lambda row: abs(_number(row["center"]) - axis))
    return {
        **instance,
        "pair_support_ratio": round(pair_ratio, 4),
        "single_support_ratio": round(single_ratio, 4),
        "pair_supported_length_mm": _round(pair_length, 1),
        "pair_span_count": len(matched),
        "unsupported_length_mm": _round(max(0.0, length - pair_length), 1),
        "unsupported_intervals": [[g[0], g[1]] for g in gaps if g[1] > g[0]],
        "facing_line_count": len(same),
        "measured_pair_count": len(pairs),
        "support_handles": sorted({handle for row in matched for handle in row["handles"]}),
        "nearest_pair_axis_mm": _round(_number(nearest["center"], 0.0), 1) if nearest else None,
        "axis_correction_mm": _round(_number(nearest["center"]) - axis, 1) if nearest else None,
        "centerline_status": status,
        "axis_pair_span_count": sum(
            1 for row in pairs if abs(_number(row["center"]) - axis) <= options["axis_slack_mm"]),
        "ledger_excluded": status in EXCLUDED_STATUSES,
    }


def build_support(
        model: dict[str, Any],
        segments: list[dict[str, Any]],
        options: dict[str, float] | None = None,
        ) -> dict[str, Any]:
    options = dict(options or {})
    options.setdefault("axis_slack_mm", 250.0)
    options.setdefault("face_tolerance_mm", 150.0)
    options.setdefault("width_tolerance_mm", 40.0)
    options.setdefault("pair_min_overlap_mm", 300.0)
    options.setdefault("default_width_mm", 200.0)
    options.setdefault("verified_ratio", 0.90)
    options.setdefault("partial_ratio", 0.50)
    options.setdefault("min_gap_report_mm", 200.0)
    options["_pair_cache"] = {}
    registry = model.get("run_registry") or {}
    instances: list[dict[str, Any]] = []
    for run in registry.get("runs") or []:
        geometry = _instance_geometry(run, "run")
        if geometry:
            instances.append(_support(geometry, segments, options))
    for beam in (model.get("members") or {}).get("beams") or []:
        geometry = _instance_geometry(beam, "instance")
        if geometry:
            instances.append(_support(geometry, segments, options))
    groups: dict[str, dict[str, Any]] = {}
    for row in instances:
        bucket = groups.setdefault(row["centerline_status"], {
            "count": 0, "volume_m3": 0.0, "run_count": 0, "instance_count": 0})
        bucket["count"] += 1
        bucket["volume_m3"] = _round(bucket["volume_m3"] + _number(row["volume_m3"]))
        if row["basis"] == "run":
            bucket["run_count"] += 1
        else:
            bucket["instance_count"] += 1
    runs = [row for row in instances if row["basis"] == "run"]
    insts = [row for row in instances if row["basis"] == "instance"]
    run_total = sum(_number(row["volume_m3"]) for row in runs)
    excluded_run = sum(_number(row["volume_m3"]) for row in runs if row["ledger_excluded"])
    excluded_inst = sum(_number(row["volume_m3"]) for row in insts if row["ledger_excluded"])
    phantom_run = [row for row in runs if row["centerline_status"] == PHANTOM]
    gap_run = [row for row in runs if row["centerline_status"] == LENGTH_GAP]
    phantom_inst = [row for row in insts if row["centerline_status"] == PHANTOM]
    gap_inst = [row for row in insts if row["centerline_status"] == LENGTH_GAP]
    instances.sort(key=lambda row: (row["centerline_status"], -_number(row["volume_m3"]),
                                    row["code"]))
    return {
        "schema": SCHEMA,
        "options": {k: _round(v, 3) for k, v in options.items()
                    if isinstance(v, (int, float))},
        "beam_layers": list(BEAM_LAYERS),
        "beam_line_segment_count": len(segments),
        "instances": instances,
        "summary": {
            "run_instance_count": len(runs),
            "model_instance_count": len(insts),
            "run_volume_m3": _round(run_total),
            "model_volume_m3": _round(sum(_number(row["volume_m3"]) for row in insts)),
            "by_status": groups,
            "ledger_excluded_run_volume_m3": _round(excluded_run),
            "ledger_excluded_model_volume_m3": _round(excluded_inst),
            "phantom_run_count": len(phantom_run),
            "phantom_model_count": len(phantom_inst),
            "length_gap_run_count": len(gap_run),
            "length_gap_model_count": len(gap_inst),
            "length_gap_model_volume_m3": _round(
                sum(_number(row["volume_m3"]) for row in gap_inst)),
            "phantom_model_volume_m3": _round(
                sum(_number(row["volume_m3"]) for row in phantom_inst)),
            "verified_run_ratio": (
                round(sum(1 for row in runs if row["centerline_status"] == VERIFIED)
                      / len(runs), 4) if runs else 0.0),
        },
        "gates": [
            {"id": "centerline-support-closed",
             "status": "pass" if not phantom_run and not gap_run else "fail",
             "evidence": f"算量实例幻影中心线 {len(phantom_run)} 个、区间无覆盖 {len(gap_run)} 个；"
                         f"模型实例幻影 {len(phantom_inst)} 个/"
                         f"{_round(sum(_number(r['volume_m3']) for r in phantom_inst))} m3、"
                         f"区间无覆盖 {len(gap_inst)} 个/"
                         f"{_round(sum(_number(r['volume_m3']) for r in gap_inst))} m3",
             "action": "幻影中心线既不扣也不加，直接退出分标号台账；区间无覆盖转长度与支座闭合"},
            {"id": "centerline-support-single-line",
             "status": "pass" if not [r for r in instances if r["centerline_status"] == SINGLE]
             else "warn",
             "evidence": "只实测到单边梁线的实例 "
                         f"{sum(1 for r in instances if r['centerline_status'] == SINGLE)} 个，"
                         "梁宽无法由图面确定",
             "action": "回图补第二边线或改按轴线推定并标注推定，不得当实测证据"},
        ],
        "formal_ready": False,
        "applied_to_formal_quantity": False,
    }


def cross_check_overlap(payload: dict[str, Any], verdict_path: Path) -> dict[str, Any]:
    """与人工判读对账：幻影/真重复分类必须一致，否则说明校验器容差失真。"""
    data = json.loads(verdict_path.read_text(encoding="utf-8"))
    by_code: dict[str, list[dict[str, Any]]] = {}
    for row in payload["instances"]:
        if row["basis"] != "instance":
            continue
        by_code.setdefault(row["code"], []).append(row)
    rows = []
    for pair in data.get("pairs") or []:
        expected = ("ghost" if "无梁线支撑" in _text(pair.get("verdict")) else "true-overlap")
        axis_y = _number(pair.get("axis_y_mm"))
        members = []
        for code in (pair.get("first"), pair.get("second")):
            for row in by_code.get(_text(code), []):
                if row["orientation"] != "H" or abs(_number(row["axis_mm"]) - axis_y) > 1.0:
                    continue
                if min(_number(row["end_mm"]), _number(pair["overlap_end_mm"])) - max(
                        _number(row["start_mm"]), _number(pair["overlap_start_mm"])) <= 0:
                    continue
                members.append(row)
        statuses = [row["centerline_status"] for row in members]
        # 该轴上有实测线对（哪怕没覆盖本区间）即"轴线真实"，只有完全无线对才判幻影
        actual = "ghost" if all(s == PHANTOM for s in statuses) and statuses else "true-overlap"
        rows.append({
            "axis_y_mm": pair.get("axis_y_mm"), "first": pair.get("first"),
            "second": pair.get("second"), "hand_verdict": expected,
            "kernel_verdict": actual, "statuses": statuses,
            "instance_count": len(members),
            "overlap_volume_m3": pair.get("overlap_volume_m3"),
            "agrees": expected == actual,
        })
    agree = sum(1 for row in rows if row["agrees"])
    payload["overlap_cross_check"] = {
        "source": str(verdict_path),
        "pair_count": len(rows),
        "agree_count": agree,
        "agree_ratio": round(agree / len(rows), 4) if rows else 0.0,
        "note": "人工判读按轴线上有无成对梁线定幻影；内核按重叠区间内的成对线覆盖长度判定，"
                "两者不一致时须回图看重叠区间本身，不得调容差凑一致",
        "pairs": rows,
    }
    payload["gates"].append({
        "id": "centerline-support-cross-check",
        "status": "pass" if rows and agree == len(rows) else "warn",
        "evidence": f"与人工判读重叠对 {agree}/{len(rows)} 一致",
        "action": "逐对回图核重叠区间是否有成对梁线；不得用容差调整反向迁就结论",
    })
    return payload


def csv_rows(payload: dict[str, Any]) -> list[list[Any]]:
    head = ["口径", "实例ID", "编号", "朝向", "轴线mm", "起点mm", "终点mm", "长度mm",
            "梁宽mm", "体积m3", "成对梁线覆盖率", "单边梁线覆盖率", "无支撑长度mm",
            "中心线状态", "是否退出台账", "实测线对数", "最近实测线对轴mm", "中心线应偏移mm",
            "支撑句柄", "无支撑区间"]
    rows = [head]
    for row in payload["instances"]:
        rows.append([
            row["basis"], row["id"], row["code"], row["orientation"], row["axis_mm"],
            row["start_mm"], row["end_mm"], row["length_mm"], row["width_mm"],
            row["volume_m3"], row["pair_support_ratio"], row["single_support_ratio"],
            row["unsupported_length_mm"], row["centerline_status"],
            "是" if row["ledger_excluded"] else "否", row["measured_pair_count"],
            row["nearest_pair_axis_mm"] if row["nearest_pair_axis_mm"] is not None else "",
            row["axis_correction_mm"] if row["axis_correction_mm"] is not None else "",
            ",".join(row["support_handles"])[:120],
            "; ".join(f"{a:.0f}~{b:.0f}" for a, b in row["unsupported_intervals"])[:120],
        ])
    return rows


def render_markdown(payload: dict[str, Any]) -> str:
    s = payload["summary"]
    lines = ["# 梁实例中心线图面支撑审计", ""]
    lines.append(f"图面实测梁线 {payload['beam_line_segment_count']} 段（图层 "
                 f"{'/'.join(payload['beam_layers'])}）；算量实例 {s['run_instance_count']} 个/"
                 f"{s['run_volume_m3']} m3，模型实例 {s['model_instance_count']} 个/"
                 f"{s['model_volume_m3']} m3。")
    lines.append("")
    lines.append("| 中心线状态 | 实例数 | 算量实例 | 模型实例 | 体积合计 m3 |")
    lines.append("|---|---|---|---|---|")
    order = [VERIFIED, PARTIAL, LENGTH_GAP, SINGLE, PHANTOM]
    for key in order:
        bucket = s["by_status"].get(key)
        if not bucket:
            continue
        lines.append(f"| {key} | {bucket['count']} | {bucket['run_count']} | "
                     f"{bucket['instance_count']} | {bucket['volume_m3']} |")
    lines.append("")
    lines.append(f"- 幻影中心线（该轴图面无成对梁线）：算量实例 {s['phantom_run_count']} 个、"
                 f"模型实例 {s['phantom_model_count']} 个/{s['phantom_model_volume_m3']} m3。")
    lines.append(f"- 轴线真实但本区间无梁线覆盖（长度不可信）：算量实例 {s['length_gap_run_count']} 个、"
                 f"模型实例 {s['length_gap_model_count']} 个/{s['length_gap_model_volume_m3']} m3。")
    lines.append(f"- 退出台账体积：算量口径 {s['ledger_excluded_run_volume_m3']} m3、"
                 f"模型口径 {s['ledger_excluded_model_volume_m3']} m3。")
    lines.append(f"- 算量实例中心线支撑率（verified 占比）{s['verified_run_ratio']}。")
    check = payload.get("overlap_cross_check")
    if check:
        lines.append(f"- 与人工判读重叠对账：{check['agree_count']}/{check['pair_count']} 一致。")
        for row in check["pairs"]:
            lines.append(f"  - {row['first']} × {row['second']}（轴 y={row['axis_y_mm']}）"
                         f"人工={row['hand_verdict']} 内核={row['kernel_verdict']} "
                         f"{'一致' if row['agrees'] else '不一致'} 状态={row['statuses']}")
    lines.append("")
    bad = [r for r in payload["instances"]
           if r["centerline_status"] in EXCLUDED_STATUSES][:30]
    if bad:
        lines.append("## 退出台账清单（前 25 条）")
        lines.append("")
        lines.append("| 口径 | 编号 | 轴 mm | 长度 mm | 体积 m3 | 状态 | 成对覆盖 | 最近实测线对轴 mm |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for row in bad:
            nearest = (f"{row['nearest_pair_axis_mm']:.0f}"
                       if row["nearest_pair_axis_mm"] is not None else "图面无")
            lines.append(f"| {row['basis']} | {row['code']} | {row['axis_mm']:.0f} | "
                         f"{row['length_mm']:.0f} | {row['volume_m3']} | "
                         f"{row['centerline_status']} | {row['pair_support_ratio']} | {nearest} |")
    lines.append("")
    for gate in payload["gates"]:
        lines.append(f"- [{gate['status']}] {gate['id']}：{gate['evidence']} 处理：{gate['action']}")
    lines.append("")
    lines.append("说明：本审计只判中心线是否有图面成对梁线支撑，不改体积、不改归属；"
                 "无支撑实例按'既不扣也不加'退出分标号台账。")
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="梁实例中心线图面支撑审计")
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--geometry-dxf", default=None)
    parser.add_argument("--entities-json", default=None)
    parser.add_argument("--segments-json", default=None)
    parser.add_argument("--overlap-verdict-json", default=None)
    parser.add_argument("--beam-layers", default=",".join(BEAM_LAYERS))
    parser.add_argument("--axis-slack-mm", type=float, default=250.0)
    parser.add_argument("--face-tolerance-mm", type=float, default=150.0)
    parser.add_argument("--width-tolerance-mm", type=float, default=40.0)
    parser.add_argument("--pair-min-overlap-mm", type=float, default=300.0)
    parser.add_argument("--verified-ratio", type=float, default=0.90)
    parser.add_argument("--partial-ratio", type=float, default=0.50)
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    model_path = Path(args.model_json)
    if not model_path.exists():
        parser.error(f"缺少结构模型 JSON：{model_path}")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    layers = {layer.strip() for layer in args.beam_layers.split(",") if layer.strip()}
    if args.segments_json:
        segments = json.loads(Path(args.segments_json).read_text(encoding="utf-8"))
        for row in segments:
            row.setdefault("handle", "")
    else:
        if args.geometry_dxf:
            raw = _read_entities(Path(args.geometry_dxf), layers)
        elif args.entities_json:
            payload = json.loads(Path(args.entities_json).read_text(encoding="utf-8"))
            raw = payload.get("entities") if isinstance(payload, dict) else payload
        else:
            parser.error("必须提供 --segments-json、--geometry-dxf 或 --entities-json")
        segments = [
            {**row,
             "axis_mm": row["start"][1] if row["orientation"] == "H" else row["start"][0],
             "start_mm": min(row["start"][0], row["end"][0]) if row["orientation"] == "H"
             else min(row["start"][1], row["end"][1]),
             "end_mm": max(row["start"][0], row["end"][0]) if row["orientation"] == "H"
             else max(row["start"][1], row["end"][1])}
            for row in _normalize_entities(list(raw), layers)]
    options = {
        "axis_slack_mm": args.axis_slack_mm,
        "face_tolerance_mm": args.face_tolerance_mm,
        "width_tolerance_mm": args.width_tolerance_mm,
        "pair_min_overlap_mm": args.pair_min_overlap_mm,
        "verified_ratio": args.verified_ratio,
        "partial_ratio": args.partial_ratio,
    }
    result = build_support(model, segments, options)
    if args.overlap_verdict_json:
        result = cross_check_overlap(result, Path(args.overlap_verdict_json))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    json_path = out.with_suffix(".json")
    csv_path = out.with_suffix(".csv")
    md_path = out.with_suffix(".md")
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle).writerows(csv_rows(result))
    md_path.write_text(render_markdown(result), encoding="utf-8")
    checksums = out.with_name(out.name + ".sha256")
    checksums.write_text("\n".join(
        f"{sha256(path)}  {path.resolve()}"
        for path in (json_path, csv_path, md_path)) + "\n", encoding="utf-8")
    summary = result["summary"]
    print(json.dumps({
        "run_instance_count": summary["run_instance_count"],
        "model_instance_count": summary["model_instance_count"],
        "by_status": {k: v["count"] for k, v in summary["by_status"].items()},
        "phantom_run_count": summary["phantom_run_count"],
        "phantom_model_count": summary["phantom_model_count"],
        "length_gap_model_count": summary["length_gap_model_count"],
        "ledger_excluded_run_volume_m3": summary["ledger_excluded_run_volume_m3"],
        "ledger_excluded_model_volume_m3": summary["ledger_excluded_model_volume_m3"],
        "verified_run_ratio": summary["verified_run_ratio"],
        "overlap_cross_check": (result.get("overlap_cross_check") or {}).get("agree_count"),
        "outputs": [str(json_path), str(csv_path), str(md_path), str(checksums)],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
