#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""建立独立楼梯梁台账，避免 TL/AT/CT 构件混入主梁拓扑。

本工具只处理指定 TL 编号：
1. 从图纸文字恢复编号实际位置；
2. 从楼梯平面 `S-梁-实线|S-梁-虚线` 配对中心线；
3. 按“垂直距离 + 沿轴缺口 - 梁段长度先验”选择匹配段；
4. 截面表为可选输入，截面来源和粗方量状态完整保留。
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
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import cad_beam_objects as beam  # noqa: E402
import cad_geometry  # noqa: E402


TL_CODE_RE = re.compile(r"(?<![A-Z0-9])(TL\d{1,3}[A-Za-z]?)(?!\d)", re.I)


def _round(value: float, digits: int = 1) -> float:
    return round(float(value), digits)


def _bbox_contains(bbox: list[float], x: float, y: float) -> bool:
    if len(bbox) != 4:
        return False
    x0, x1 = sorted((bbox[0], bbox[2]))
    y0, y1 = sorted((bbox[1], bbox[3]))
    return x0 <= x <= x1 and y0 <= y <= y1


def load_scan_data(scan: Path, detail: Path | None = None) -> dict[str, Any]:
    data = json.loads(scan.read_text(encoding="utf-8"))
    detail_path = detail
    if detail_path is None:
        candidate = scan.with_name(scan.stem + ".detail.json")
        if candidate.exists():
            detail_path = candidate
    if detail_path and detail_path.exists():
        data.update(json.loads(detail_path.read_text(encoding="utf-8")))
    return data


def extract_stair_labels(
        data: dict[str, Any],
        bbox: list[float],
        codes: Iterable[str],
        dedupe_mm: float = 10.0) -> list[dict[str, Any]]:
    """恢复图框内 TL 编号文字位置，并在同一点合并别名文字。"""
    wanted = {str(code).upper() for code in codes}
    grouped: dict[tuple[str, int, int], dict[str, Any]] = {}
    for record in data.get("text_records") or []:
        text = str(record.get("text") or "")
        x, y = record.get("x"), record.get("y")
        if x is None or y is None:
            continue
        if not _bbox_contains(bbox, float(x), float(y)):
            continue
        for match in TL_CODE_RE.finditer(text):
            code = match.group(1).upper()
            if code not in wanted:
                continue
            key = (
                code,
                int(round(float(x) / dedupe_mm)),
                int(round(float(y) / dedupe_mm)),
            )
            row = grouped.setdefault(key, {
                "code": code,
                "x": _round(float(x), 1),
                "y": _round(float(y), 1),
                "sheet": record.get("sheet"),
                "texts": [],
                "layers": [],
            })
            if text not in row["texts"]:
                row["texts"].append(text)
            layer = str(record.get("layer") or "")
            if layer and layer not in row["layers"]:
                row["layers"].append(layer)
    return sorted(
        grouped.values(),
        key=lambda row: (row["code"], float(row["y"]), float(row["x"])),
    )


def score_candidate(
        label: dict[str, Any],
        candidate: dict[str, Any],
        length_prior_factor: float = 0.2,
        near_perpendicular_mm: float = 200.0) -> dict[str, float] | None:
    """计算文字位置到候选中心线的垂直距离、沿轴缺口和综合分。"""
    x = float(label["x"])
    y = float(label["y"])
    start = float(candidate["start"])
    end = float(candidate["end"])
    center = float(candidate["center"])
    length = end - start
    if length <= 0:
        return None
    if candidate["orientation"] == "H":
        perpendicular = abs(y - center)
        along = x
    else:
        perpendicular = abs(x - center)
        along = y
    along_gap = max(start - along, 0.0, along - end)
    length_prior = (
        min(length, 5000.0) * length_prior_factor
        if perpendicular > near_perpendicular_mm else 0.0
    )
    score = (
        perpendicular
        + along_gap * 0.15
        - length_prior
    )
    return {
        "score": score,
        "perpendicular_mm": perpendicular,
        "along_gap_mm": along_gap,
        "length_mm": length,
    }


def associate_labels_to_candidates(
        labels: list[dict[str, Any]],
        candidates: list[dict[str, Any]],
        max_perpendicular_mm: float = 3000.0,
        max_along_gap_mm: float = 1000.0,
        min_width_mm: float = 150.0,
        max_width_mm: float = 300.0,
        length_prior_factor: float = 0.2,
        near_perpendicular_mm: float = 200.0) -> list[dict[str, Any]]:
    """给每个 TL 编号文字选择候选梁段，并保留前三个候选供复核。"""
    out = []
    for label in labels:
        scored = []
        for candidate in candidates:
            width = float(candidate.get("width_mm") or 0.0)
            if width < min_width_mm or width > max_width_mm:
                continue
            score = score_candidate(
                label,
                candidate,
                length_prior_factor=length_prior_factor,
                near_perpendicular_mm=near_perpendicular_mm,
            )
            if score is None:
                continue
            if (score["perpendicular_mm"] > max_perpendicular_mm
                    or score["along_gap_mm"] > max_along_gap_mm):
                continue
            scored.append((score["score"], candidate, score))
        near_candidates = [
            item for item in scored
            if item[2]["perpendicular_mm"] <= near_perpendicular_mm
        ]
        if near_candidates:
            scored = near_candidates
        scored.sort(key=lambda item: (item[0], -item[2]["length_mm"]))
        row = {
            "code": label["code"],
            "x": label["x"],
            "y": label["y"],
            "sheet": label.get("sheet"),
            "texts": label.get("texts") or [],
            "layers": label.get("layers") or [],
            "match_status": "unmatched",
            "matched_candidate": None,
            "candidate_audit": [],
        }
        for rank, (_score, candidate, metrics) in enumerate(scored[:3], 1):
            audit = {
                "rank": rank,
                "orientation": candidate["orientation"],
                "axis_mm": _round(candidate["center"], 1),
                "start_mm": _round(candidate["start"], 1),
                "end_mm": _round(candidate["end"], 1),
                "length_mm": _round(metrics["length_mm"], 1),
                "width_mm": _round(candidate["width_mm"], 1),
                "perpendicular_mm": _round(metrics["perpendicular_mm"], 1),
                "along_gap_mm": _round(metrics["along_gap_mm"], 1),
                "score": _round(metrics["score"], 1),
                "layers": candidate.get("layers") or [],
            }
            row["candidate_audit"].append(audit)
        if scored:
            _score, candidate, metrics = scored[0]
            row["match_status"] = "matched"
            row["matched_candidate"] = {
                "orientation": candidate["orientation"],
                "axis_mm": _round(candidate["center"], 1),
                "start_mm": _round(candidate["start"], 1),
                "end_mm": _round(candidate["end"], 1),
                "length_mm": _round(metrics["length_mm"], 1),
                "width_mm": _round(candidate["width_mm"], 1),
                "perpendicular_mm": _round(metrics["perpendicular_mm"], 1),
                "along_gap_mm": _round(metrics["along_gap_mm"], 1),
                "layers": candidate.get("layers") or [],
            }
        out.append(row)
    return out


def expand_matched_candidates(
        instances: list[dict[str, Any]],
        candidates: list[dict[str, Any]],
        merge_gap_mm: float = 400.0,
        axis_tolerance_mm: float = 75.0,
        max_gap_axis_offset_mm: float = 5.0,
        min_width_mm: float = 150.0,
        max_width_mm: float = 300.0) -> list[dict[str, Any]]:
    """把同一编号已命中的中心线与同轴短断口续段合并。"""
    out = []
    for instance in instances:
        row = dict(instance)
        raw = row.get("matched_candidate")
        if not raw:
            out.append(row)
            continue
        match = dict(raw)
        lo = float(match["start_mm"])
        hi = float(match["end_mm"])
        axis = float(match["axis_mm"])
        orientation = match["orientation"]
        candidate_pool: dict[tuple[Any, ...], dict[str, Any]] = {}
        for candidate in candidates:
            key = (
                candidate["orientation"],
                round(float(candidate["center"]), 1),
                round(float(candidate["start"]), 1),
                round(float(candidate["end"]), 1),
                round(float(candidate.get("width_mm") or 0.0), 1),
            )
            candidate_pool[key] = candidate
        components = 1
        changed = True
        while changed:
            changed = False
            for candidate in candidate_pool.values():
                if candidate["orientation"] != orientation:
                    continue
                width = float(candidate.get("width_mm") or 0.0)
                if width < min_width_mm or width > max_width_mm:
                    continue
                axis_offset = abs(float(candidate["center"]) - axis)
                if axis_offset > axis_tolerance_mm:
                    continue
                start = float(candidate["start"])
                end = float(candidate["end"])
                if start > hi:
                    gap = start - hi
                elif end < lo:
                    gap = lo - end
                else:
                    gap = 0.0
                if gap > 0 and axis_offset > max_gap_axis_offset_mm:
                    continue
                if end < lo - merge_gap_mm or start > hi + merge_gap_mm:
                    continue
                new_lo = min(lo, start)
                new_hi = max(hi, end)
                if new_lo == lo and new_hi == hi:
                    continue
                lo, hi = new_lo, new_hi
                if not (
                        abs(start - float(match["start_mm"])) <= 0.1
                        and abs(end - float(match["end_mm"])) <= 0.1):
                    components += 1
                changed = True
        match["start_mm"] = _round(lo, 1)
        match["end_mm"] = _round(hi, 1)
        match["length_mm"] = _round(hi - lo, 1)
        match["component_count"] = components
        row["matched_candidate"] = match
        out.append(row)
    return out


def load_section_map(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("sections") if isinstance(data, dict) else None
    if not isinstance(rows, dict):
        raise SystemExit("--section-json 必须包含 sections 对象")
    return {
        str(code).upper(): dict(value)
        for code, value in rows.items()
        if isinstance(value, dict)
    }


def parse_code_multipliers(value: str | None) -> dict[str, int]:
    """解析 `TL2=2,TL3=2` 形式的构件实例倍率。"""
    out: dict[str, int] = {}
    for item in str(value or "").split(","):
        item = item.strip()
        if not item:
            continue
        if "=" not in item:
            raise SystemExit(f"--member-multipliers 项缺少等号：{item}")
        code, raw_multiplier = item.split("=", 1)
        code = code.strip().upper()
        try:
            multiplier = int(raw_multiplier)
        except ValueError as exc:
            raise SystemExit(
                f"--member-multipliers 倍率不是整数：{item}") from exc
        if not code or multiplier < 1:
            raise SystemExit(
                f"--member-multipliers 编号或倍率无效：{item}")
        out[code] = multiplier
    return out


def build_stair_beam_registry(
        instances: list[dict[str, Any]],
        section_map: dict[str, dict[str, Any]] | None = None,
        merge_gap_mm: float = 400.0,
        axis_tolerance_mm: float = 75.0,
        merge_axis_offset_mm: float = 5.0,
        instance_multiplier: int = 1,
        code_multipliers: dict[str, int] | None = None,
        multiplier_basis: str = "") -> dict[str, Any]:
    """汇总每个 TL 编号的唯一拓扑段、文字数、截面和粗方量。"""
    section_map = section_map or {}
    code_multipliers = {
        str(code).upper(): int(multiplier)
        for code, multiplier in (code_multipliers or {}).items()
    }
    if instance_multiplier < 1:
        raise ValueError("instance_multiplier 必须 >= 1")
    if any(multiplier < 1 for multiplier in code_multipliers.values()):
        raise ValueError("code_multipliers 倍率必须 >= 1")
    groups: dict[str, dict[str, Any]] = {}
    unique_runs: dict[str, set[tuple[Any, ...]]] = defaultdict(set)
    for instance in instances:
        code = str(instance["code"]).upper()
        group = groups.setdefault(code, {
            "code": code,
            "label_count": 0,
            "matched_label_count": 0,
            "run_count": 0,
            "centerline_length_mm": 0.0,
            "instance_multiplier": code_multipliers.get(
                code, int(instance_multiplier)),
            "instance_multiplier_basis": multiplier_basis,
            "quantity_centerline_length_mm": 0.0,
            "section": "",
            "section_b_mm": None,
            "section_h_mm": None,
            "section_status": "unresolved",
            "section_basis": "",
            "gross_volume_m3": None,
            "volume_status": "unresolved",
            "runs": [],
            "unmatched_labels": [],
        })
        group["label_count"] += 1
        candidate = instance.get("matched_candidate")
        if not candidate:
            group["unmatched_labels"].append({
                "x": instance.get("x"),
                "y": instance.get("y"),
                "texts": instance.get("texts") or [],
            })
            continue
        group["matched_label_count"] += 1
        run_key = (
            candidate["orientation"],
            round(float(candidate["axis_mm"]), 1),
            round(float(candidate["start_mm"]), 1),
            round(float(candidate["end_mm"]), 1),
        )
        if run_key in unique_runs[code]:
            continue
        unique_runs[code].add(run_key)
        group["runs"].append({
            "orientation": candidate["orientation"],
            "axis_mm": candidate["axis_mm"],
            "start_mm": candidate["start_mm"],
            "end_mm": candidate["end_mm"],
            "length_mm": candidate["length_mm"],
            "width_mm": candidate["width_mm"],
            "matched_label": {
                "x": instance.get("x"),
                "y": instance.get("y"),
                "texts": instance.get("texts") or [],
            },
            "perpendicular_mm": candidate["perpendicular_mm"],
            "along_gap_mm": candidate["along_gap_mm"],
            "layers": candidate.get("layers") or [],
            "component_count": int(candidate.get("component_count") or 1),
        })

    for code, group in groups.items():
        merged_runs: list[dict[str, Any]] = []
        for run in sorted(
                group["runs"],
                key=lambda item: (
                    item["orientation"], float(item["axis_mm"]),
                    float(item["start_mm"]))):
            merged = next(
                (item for item in merged_runs
                 if item["orientation"] == run["orientation"]
                 and abs(float(item["axis_mm"]) - float(run["axis_mm"]))
                 <= axis_tolerance_mm
                 and float(run["start_mm"])
                 - float(item["end_mm"]) <= merge_gap_mm),
                None,
            )
            if merged is None:
                copied = dict(run)
                merged_runs.append(copied)
                continue
            merged["end_mm"] = _round(max(
                float(merged["end_mm"]), float(run["end_mm"])), 1)
            merged["length_mm"] = _round(
                float(merged["end_mm"]) - float(merged["start_mm"]), 1)
            merged["component_count"] += int(run.get("component_count") or 1)
            merged["matched_label"] = merged.get("matched_label") or {}
        group["runs"] = merged_runs
        group["run_count"] = len(group["runs"])
        group["centerline_length_mm"] = _round(sum(
            float(run["length_mm"]) for run in group["runs"]), 1)
        group["quantity_centerline_length_mm"] = _round(
            group["centerline_length_mm"] * group["instance_multiplier"], 1)
        section = section_map.get(code) or {}
        b = section.get("b_mm")
        h = section.get("h_mm")
        if b and h:
            group["section_b_mm"] = float(b)
            group["section_h_mm"] = float(h)
            group["section"] = f"{float(b):g}x{float(h):g}"
            group["section_status"] = str(
                section.get("status") or "provided")
            group["section_basis"] = str(section.get("basis") or "")
            group["gross_volume_m3"] = _round(
                group["quantity_centerline_length_mm"]
                * float(b) * float(h) / 1e9,
                4,
            )
            group["volume_status"] = (
                "gross-centerline-with-"
                + group["section_status"].replace("_", "-")
                + (
                    f"-x{group['instance_multiplier']}"
                    if group["instance_multiplier"] != 1 else ""
                )
            )
        if group["matched_label_count"] < group["label_count"]:
            group["review_status"] = "partial-match"
        elif not group["runs"]:
            group["review_status"] = "unmatched"
        else:
            group["review_status"] = "matched"
    return {
        "schema": "cad-stair-beam-registry/v0.2",
        "parameters": {
            "instance_multiplier": int(instance_multiplier),
            "code_multipliers": dict(sorted(code_multipliers.items())),
            "multiplier_basis": multiplier_basis,
            "merge_gap_mm": float(merge_gap_mm),
            "axis_tolerance_mm": float(axis_tolerance_mm),
            "merge_axis_offset_mm": float(merge_axis_offset_mm),
        },
        "quantities": {
            "code_count": len(groups),
            "label_count": sum(group["label_count"] for group in groups.values()),
            "matched_label_count": sum(
                group["matched_label_count"] for group in groups.values()),
            "run_count": sum(group["run_count"] for group in groups.values()),
            "component_count": sum(
                int(run.get("component_count") or 1)
                for group in groups.values() for run in group["runs"]),
            "centerline_length_mm": _round(sum(
                group["centerline_length_mm"] for group in groups.values()), 1),
            "quantity_centerline_length_mm": _round(sum(
                group["quantity_centerline_length_mm"]
                for group in groups.values()), 1),
            "gross_volume_m3": _round(sum(
                float(group["gross_volume_m3"] or 0.0)
                for group in groups.values()), 4),
        },
        "codes": dict(sorted(groups.items())),
        "status": (
            "楼梯梁独立台账；不与主梁中心线台账相加；"
            "倍率只放大已识别拓扑数量，不改变单个拓扑段几何"
        ),
    }


def render_md(result: dict[str, Any]) -> str:
    quantities = result["quantities"]
    out = [
        "# CAD 楼梯梁独立台账",
        "",
        f"- 编号：{'、'.join(result['codes']) or '-'}",
        f"- 编号文字：{quantities['label_count']} 个",
        f"- 已匹配文字：{quantities['matched_label_count']} 个",
        f"- 合并拓扑段：{quantities['run_count']} 段"
        f"（原始中心线 {quantities['component_count']} 段）",
        f"- 图面中心线长度：{quantities['centerline_length_mm']} mm",
        f"- 计入实例倍率后中心线长度："
        f"{quantities['quantity_centerline_length_mm']} mm",
        f"- 粗方量：{quantities['gross_volume_m3']} m3"
        f"（倍率、截面或支座来源不足时不代表正式量）",
        "",
        "| 编号 | 文字数 | 匹配文字 | 合并段 | 原始段 | 图面中心线mm | "
        "实例倍率 | 计量中心线mm | 截面 | 粗方量m3 | 截面状态 | 复核状态 |",
        "|:--|---:|---:|---:|---:|---:|---:|---:|:--|---:|:--|:--|",
    ]
    for group in result["codes"].values():
        out.append(
            f"| {group['code']} | {group['label_count']} | "
            f"{group['matched_label_count']} | {group['run_count']} | "
            f"{sum(int(run.get('component_count') or 1) for run in group['runs'])} | "
            f"{group['centerline_length_mm']} | {group['instance_multiplier']} | "
            f"{group['quantity_centerline_length_mm']} | "
            f"{group['section'] or '-'} | "
            f"{group['gross_volume_m3'] if group['gross_volume_m3'] is not None else '-'} | "
            f"{group['section_status']} | {group['review_status']} |")
    out += [
        "",
        "## 拓扑段",
        "",
        "| 编号 | 方向 | 轴线mm | 起点mm | 终点mm | 长度mm | 原始段 | 配对宽mm | "
        "文字距轴mm | 文字沿轴缺口mm | 图层 |",
        "|:--|:--:|---:|---:|---:|---:|---:|---:|---:|---:|:--|",
    ]
    for group in result["codes"].values():
        for run in group["runs"]:
            out.append(
                f"| {group['code']} | {run['orientation']} | {run['axis_mm']} | "
                f"{run['start_mm']} | {run['end_mm']} | {run['length_mm']} | "
                f"{run.get('component_count') or 1} | {run['width_mm']} | "
                f"{run['perpendicular_mm']} | "
                f"{run['along_gap_mm']} | {'、'.join(run['layers']) or '-'} |")
    out += [
        "",
        "## 口径",
        "",
        "- 本台账只收录指定 `TL` 编号，不并入 `cad-beam-run-registry` 主梁段。",
        "- `实例倍率` 只允许显式输入，用于表达图中叠合绘制的上下行梯梁或成对楼梯实例；",
        "  不得根据模型方量反推倍率。",
        "- 楼梯梁截面若来自模型反算或人工输入，`截面状态` 会保留来源，不能替代图纸大样复核。",
        "- 粗方量按“图面中心线长度 × 显式实例倍率 × 输入截面”，"
        "未扣支座、平台节点和梯板交接；正式翻样前必须复查。",
        "",
    ]
    return "\n".join(out)


def csv_lines(result: dict[str, Any]) -> list[list[str]]:
    out = [[
        "编号", "方向", "轴线mm", "起点mm", "终点mm", "长度mm",
        "配对宽mm", "截面", "粗方量m3", "截面状态", "截面依据",
        "实例倍率", "计量中心线mm",
        "文字X", "文字Y", "文字距轴mm", "文字沿轴缺口mm",
        "复核状态", "图层",
    ]]
    for group in result["codes"].values():
        if not group["runs"]:
            out.append([
                group["code"], "", "", "", "", "", "", group["section"] or "",
                "" if group["gross_volume_m3"] is None
                else str(group["gross_volume_m3"]),
                group["section_status"], group["section_basis"],
                str(group["instance_multiplier"]),
                str(group["quantity_centerline_length_mm"]),
                "", "", "", "", group["review_status"], "",
            ])
            continue
        for run in group["runs"]:
            label = run.get("matched_label") or {}
            out.append([
                group["code"], run["orientation"], str(run["axis_mm"]),
                str(run["start_mm"]), str(run["end_mm"]), str(run["length_mm"]),
                str(run["width_mm"]), group["section"] or "",
                "" if group["gross_volume_m3"] is None
                else str(group["gross_volume_m3"]),
                group["section_status"], group["section_basis"],
                str(group["instance_multiplier"]),
                str(group["quantity_centerline_length_mm"]),
                str(label.get("x") or ""), str(label.get("y") or ""),
                str(run["perpendicular_mm"]), str(run["along_gap_mm"]),
                group["review_status"], "、".join(run["layers"]),
            ])
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="建立独立楼梯梁台账")
    parser.add_argument("--dxf", required=True, help="楼梯平面/大样展开 DXF")
    parser.add_argument("--scan", required=True, help="cad-file-reader 识图契约 JSON")
    parser.add_argument("--detail", default=None, help="包含 text_records 的 detail JSON")
    parser.add_argument("--floor-label", default=None,
                        help="用于自动确定图框；未传时使用 --bbox")
    parser.add_argument("--bbox", default=None, help="x0,y0,x1,y1")
    parser.add_argument("--codes", default="TL2,TL3,TL4",
                        help="逗号分隔的楼梯梁编号")
    parser.add_argument("--layer-pattern", default=r"S-梁-实线|S-梁-虚线")
    parser.add_argument("--known-widths", default="200",
                        help="配对宽度白名单，逗号分隔")
    parser.add_argument("--max-perpendicular-mm", type=float, default=3000.0)
    parser.add_argument("--max-along-gap-mm", type=float, default=1000.0)
    parser.add_argument("--length-prior-factor", type=float, default=0.2)
    parser.add_argument("--near-perpendicular-mm", type=float, default=200.0)
    parser.add_argument("--merge-gap-mm", type=float, default=400.0)
    parser.add_argument("--axis-tolerance-mm", type=float, default=75.0)
    parser.add_argument(
        "--merge-axis-offset-mm",
        type=float,
        default=5.0,
        help="跨短断口合并时允许的轴线偏移，默认 5mm",
    )
    parser.add_argument("--instance-multiplier", type=int, default=1,
                        help="所有编号统一实例倍率，默认 1")
    parser.add_argument("--member-multipliers", default=None,
                        help="按编号覆盖倍率，如 TL2=2,TL3=2")
    parser.add_argument("--multiplier-basis", default="",
                        help="实例倍率依据，必须写明图纸证据")
    parser.add_argument("--section-json", default=None,
                        help="可选截面表：{'sections': {'TL3': {'b_mm': 200, ...}}}")
    parser.add_argument("--format", choices=["all", "json", "csv", "md"],
                        default="all")
    parser.add_argument("-o", "--out", default="cad_stair_beam_registry")
    args = parser.parse_args()

    dxf = Path(args.dxf)
    scan = Path(args.scan)
    detail = Path(args.detail) if args.detail else None
    if not dxf.exists() or not scan.exists():
        print("--dxf 或 --scan 文件不存在", file=sys.stderr)
        return 2
    if args.bbox:
        try:
            bbox = [float(value) for value in args.bbox.split(",")]
        except ValueError:
            bbox = []
        if len(bbox) != 4:
            print("--bbox 需要 x0,y0,x1,y1", file=sys.stderr)
            return 2
    else:
        bbox = cad_geometry.find_sheet_bbox(scan, detail, args.floor_label)
    if not bbox:
        print("未找到目标图框", file=sys.stderr)
        return 2

    data = load_scan_data(scan, detail)
    codes = [value.strip().upper() for value in args.codes.split(",") if value.strip()]
    labels = extract_stair_labels(data, bbox, codes)
    widths = []
    for value in args.known_widths.split(","):
        try:
            widths.append(float(value))
        except ValueError:
            continue
    segments = beam.load_expanded_dxf(
        dxf, bbox, 25000.0, args.layer_pattern)
    candidates, width_counts = beam.pair_beam_centerlines(segments, widths)
    instances = associate_labels_to_candidates(
        labels,
        candidates,
        max_perpendicular_mm=args.max_perpendicular_mm,
        max_along_gap_mm=args.max_along_gap_mm,
        min_width_mm=min(widths) if widths else 150.0,
        max_width_mm=max(widths) if widths else 300.0,
        length_prior_factor=args.length_prior_factor,
        near_perpendicular_mm=args.near_perpendicular_mm,
    )
    instances = expand_matched_candidates(
        instances,
        candidates,
        merge_gap_mm=args.merge_gap_mm,
        axis_tolerance_mm=args.axis_tolerance_mm,
        max_gap_axis_offset_mm=args.merge_axis_offset_mm,
        min_width_mm=min(widths) if widths else 150.0,
        max_width_mm=max(widths) if widths else 300.0,
    )
    section_map = load_section_map(
        Path(args.section_json) if args.section_json else None)
    code_multipliers = parse_code_multipliers(args.member_multipliers)
    if (
        (args.instance_multiplier != 1 or code_multipliers)
        and not str(args.multiplier_basis or "").strip()
    ):
        print(
            "实例倍率不为 1 时必须提供 --multiplier-basis",
            file=sys.stderr,
        )
        return 2
    registry = build_stair_beam_registry(
        instances,
        section_map,
        merge_gap_mm=args.merge_gap_mm,
        axis_tolerance_mm=args.axis_tolerance_mm,
        merge_axis_offset_mm=args.merge_axis_offset_mm,
        instance_multiplier=args.instance_multiplier,
        code_multipliers=code_multipliers,
        multiplier_basis=args.multiplier_basis,
    )
    result = {
        "source": str(dxf),
        "bbox": bbox,
        "layer_pattern": args.layer_pattern,
        "geometry_candidate_count": len(candidates),
        "geometry_width_counts": dict(width_counts),
        "section_source": str(args.section_json or ""),
        "multiplier_basis": args.multiplier_basis,
        "instances": instances,
        "registry": registry,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.format in ("md", "all"):
        out.with_suffix(".md").write_text(
            render_md(registry), encoding="utf-8")
        print(f"已写出 {out.with_suffix('.md')}", file=sys.stderr)
    if args.format in ("json", "all"):
        out.with_suffix(".json").write_text(
            json.dumps(result, ensure_ascii=False, indent=1),
            encoding="utf-8")
        print(f"已写出 {out.with_suffix('.json')}", file=sys.stderr)
    if args.format in ("csv", "all"):
        with out.with_suffix(".csv").open(
                "w", encoding="utf-8-sig", newline="") as handle:
            csv.writer(handle).writerows(csv_lines(registry))
        print(f"已写出 {out.with_suffix('.csv')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
