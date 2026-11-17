#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按图例填充把每块面板拆成厚度子面域，闭合板厚证据链并给出分档体积。

图面同时给了三档证据：板厚尺寸直接标注、"图中[图案]填充部分未标注的板厚为XXmm"
图例句、"未标注的板厚为130mm" 说明句。一块面板可能同时压在填充区和非填充区上，
整块取一个厚度就会与图例冲突。本脚本用 100 mm 网格把面板切成子面域，
逐块按"直接标注 > 图例填充 > 说明默认"定档，并保证分档面积与面板面积对平。
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
import re
import json
import sys
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
if str(SKILL_DIR / "vendor") not in sys.path:
    sys.path.insert(0, str(SKILL_DIR / "vendor"))
from cad_geometry import point_in_polygon  # noqa: E402

SCHEMA = "cad-slab-thickness-partition/v0.1"

LABEL_CLAIM_TEXT = {"verified": "有归属标注", "unverified": "无归属标注已降级",
                    "no-text-ledger": "未传文字台账", "not-claimed": "未主张标注"}

LABEL = "dimension-label"
LEGEND = "legend-hatch-rule"
NOTE = "drawing-note-rule"
ELEVATION = "elevation-only"


def _load(path: str | Path | None) -> dict[str, Any]:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _fill_regions(model: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """按图例规则分桶：140 / 120 / 只改标高不计厚。"""
    buckets: dict[str, list[dict[str, Any]]] = {}
    for row in ((model.get("topology") or {}).get("hatch_regions") or []):
        rule = _text(row.get("fill_rule")).strip()
        points = [(float(p[0]), float(p[1])) for p in row.get("points") or []]
        if len(points) < 3:
            continue
        key = rule if rule.replace(".", "").isdigit() else (
            ELEVATION if rule.startswith("drop") else "unclassified")
        buckets.setdefault(key, []).append({
            "id": _text(row.get("id")), "handle": _text(row.get("handle")),
            "points": points,
            "bbox": (min(p[0] for p in points), min(p[1] for p in points),
                     max(p[0] for p in points), max(p[1] for p in points)),
        })
    return buckets


def _inside(regions: list[dict[str, Any]], x: float, y: float) -> str:
    for row in regions:
        box = row["bbox"]
        if box[0] <= x <= box[2] and box[1] <= y <= box[3] and point_in_polygon((x, y), row["points"]):
            return row["id"]
    return ""


def build_partition(model: dict[str, Any], notes: list[dict[str, Any]],
                    options: dict[str, Any] | None = None) -> dict[str, Any]:
    options = dict(options or {})
    step = options.get("grid_step_mm", 100.0)
    label_priority = bool(options.get("label_priority", True))
    panel_texts = list(options.get("panel_texts") or [])
    verify_radius = _number(options.get("label_verify_radius_mm"), 1000.0)
    panels = [row for row in ((model.get("members") or {}).get("slab_panels") or [])
              if len(row.get("points") or []) >= 3]
    # 空文字台账时不做降级，否则会把上游的标注档全部误判成无证据
    label_owners = _label_owners(panel_texts, panels, verify_radius) if panel_texts else None
    fills = _fill_regions(model)
    numeric = {key: float(key) for key in fills if key.replace(".", "").isdigit()}
    fill_classes = sorted(numeric, key=lambda key: -numeric[key])
    # 说明默认档只认"未标注的板厚为XXmm"这类整板规则句；
    # 带"填充部分"的句子属于图例句，其厚度由填充区域承载，不能当默认档
    note_defaults = sorted({_number(row.get("thickness_mm")) for row in notes
                            if _number(row.get("thickness_mm")) > 0
                            and "填充" not in _text(row.get("text"))})
    legend_note_handles = [_text(row.get("handle")) for row in notes
                           if "填充" in _text(row.get("text"))]
    legend_rules = [row for row in ((model.get("phase15") or {}).get("legend") or [])
                    if _text(row.get("semantic")) == "thickness"]
    options = dict(options)
    options["legend_note_handles"] = legend_note_handles
    elevation_regions = fills.get(ELEVATION, [])

    rows: list[dict[str, Any]] = []
    totals: dict[str, float] = {}
    for panel in panels:
        points = [(float(p[0]), float(p[1])) for p in panel["points"]]
        bbox = (min(p[0] for p in points), min(p[1] for p in points),
                max(p[0] for p in points), max(p[1] for p in points))
        exact_area = _number(panel.get("area_m2"))
        if exact_area <= 0:
            continue
        assigned = _number(panel.get("thickness_mm"))
        source = _text(panel.get("thickness_source")) or NOTE
        label_claim = "not-claimed"
        if source == LABEL:
            # 复核"直接标注"是否真有归属本面板的图面文字承载：查不到就降级为说明默认档
            if label_owners is None:
                label_claim = "no-text-ledger"
            else:
                label_claim = _verify_label(label_owners, _text(panel.get("id")), assigned)
            if label_claim == "unverified":
                source = NOTE
        grid_area = {"grid": 0.0}
        counts: dict[str, int] = {}
        hits: dict[str, set] = {}
        elevation_cells = 0
        grid_cells = 0
        x = bbox[0] + step / 2.0
        while x < bbox[2]:
            y = bbox[1] + step / 2.0
            while y < bbox[3]:
                if point_in_polygon((x, y), points):
                    # 直接标注优先：该档默认认为标注覆盖整块面板
                    if source == LABEL and label_priority:
                        counts[LABEL] = counts.get(LABEL, 0) + 1
                    else:
                        matched = ""
                        for key in fill_classes:
                            if _inside(fills[key], x, y):
                                matched = key
                                break
                        if matched:
                            grade = f"{LEGEND}:{matched}"
                            counts[grade] = counts.get(grade, 0) + 1
                            hits.setdefault(grade, set()).update(
                                hit for hit in [matched] if hit)
                        else:
                            counts[NOTE] = counts.get(NOTE, 0) + 1
                    for key in fills:
                        if key not in fill_classes and key != ELEVATION:
                            continue
                    if _inside(elevation_regions, x, y):
                        elevation_cells += 1
                    grid_area["grid"] += (step / 1000.0) ** 2
                    grid_cells += 1
                y += step
            x += step
        total_cells = grid_cells or 1
        areas: dict[str, float] = {}
        for key, count in counts.items():
            areas[key] = round(exact_area * count / total_cells, 4)
        # 降板填充只作标高叠加：面积按同一比例折算，不进厚度档
        elevation_area = round(exact_area * elevation_cells / total_cells, 4)
        note_default = _number(note_defaults[0]) if note_defaults else assigned
        if label_priority is False and source == LABEL:
            note_default = assigned
        thickness_of = {}
        for key in areas:
            if key.startswith(f"{LEGEND}:"):
                thickness_of[key] = numeric[key.split(":", 1)[1]]
            elif key == LABEL:
                thickness_of[key] = assigned if label_priority else note_default
            elif key == NOTE:
                thickness_of(key) if False else None
                thickness_of[key] = note_default
        volume_current = round(exact_area * assigned / 1000.0, 4)
        volume_split = round(sum(area * thickness_of[key] / 1000.0
                                 for key, area in areas.items()), 4)
        area_sum = round(sum(areas.values()), 4)
        rows.append({
            "id": _text(panel.get("id")),
            "code": _text(panel.get("code") or panel.get("id")),
            "material_system": _text(panel.get("material_system")),
            "assigned_thickness_mm": assigned,
            "assigned_source": source,
            "area_m2": round(exact_area, 4),
            "grid_area_m2": round(grid_area["grid"], 4),
            "area_by_grade_m2": areas,
            "thickness_by_grade_mm": thickness_of,
            "elevation_only_area_m2": elevation_area,
            "volume_as_assigned_m3": volume_current,
            "volume_partitioned_m3": volume_split,
            "volume_delta_m3": round(volume_split - volume_current, 4),
            "partition_conflict": len(areas) > 1,
            "label_claim": label_claim,
            "identity_residual_m2": round(area_sum - round(exact_area, 4), 6),
        })
        for key, area in areas.items():
            totals[key] = round(totals.get(key, 0.0) + (
                0.0 if key == ELEVATION else area), 4)
        totals["_volume_current"] = round(
            totals.get("_volume_current", 0.0) + volume_current, 4)
        totals["_volume_split"] = round(
            totals.get("_volume_split", 0.0) + volume_split, 4)
        totals["_area"] = round(totals.get("_area", 0.0) + exact_area, 4)
    unverified = [row for row in rows if row.get("label_claim") == "unverified"]
    verified = [row for row in rows if row.get("label_claim") == "verified"]
    no_ledger = [row for row in rows if row.get("label_claim") == "no-text-ledger"]
    rows.sort(key=lambda row: -abs(row["volume_delta_m3"]))
    return _package(rows, totals, fills, notes, legend_rules, note_defaults,
                    elevation_regions, options, panels, unverified, verified,
                    no_ledger)


def _thickness_values_in_text(text: Any) -> set[int]:
    """从图面文字里取"可能是板厚"的独立数字。

    只认 50~400 mm 的独立数字：钢筋间距（@150）、尺寸标注数字（900、3800）
    和配筋串都不算板厚证据。
    """
    raw = _text(text).replace(" ", "")
    values: set[int] = set()
    for match in re.finditer(r"(?<![\d.@])(\d{2,4})(?![\d.])", raw):
        value = int(match.group(1))
        if 50 <= value <= 400:
            values.add(value)
    return values


def _is_thickness_label(row: dict[str, Any]) -> bool:
    """尺寸标注层上的数字是轴距，不是板厚；只有写明板厚的文字才算标注证据。"""
    layer = _text(row.get("layer")).upper().replace(" ", "")
    raw = _text(row.get("text")).replace(" ", "")
    if "板厚" in raw or re.search(r"(?i)h\s*=\s*\d", raw):
        return True
    return "DIM" not in layer


def _polygon_area(points: list[tuple]) -> float:
    total = 0.0
    for index, (x, y) in enumerate(points):
        other = points[(index + 1) % len(points)]
        total += x * other[1] - other[0] * y
    return abs(total) / 2.0 / 1.0e6


def _label_owners(panel_texts: list[dict[str, Any]], panels: list[dict[str, Any]],
                  radius: float) -> dict[str, list[dict[str, Any]]]:
    """每处板厚文字只归一块面板：包含它的面板优先，否则给半径内最近的那块。

    一块板厚标注不能同时给多块面板当"直接标注"证据，否则一处文字就能
    把整片板面都升级成标注档，图面并没有给出这个结论。
    """
    polygons: dict[str, list[tuple]] = {}
    for row in panels:
        points = [(float(p[0]), float(p[1])) for p in (row.get("points") or [])]
        if len(points) >= 3:
            polygons[_text(row.get("id"))] = points
    owners: dict[str, list[dict[str, Any]]] = {}
    for row in panel_texts:
        if not _is_thickness_label(row):
            continue
        values = _thickness_values_in_text(row.get("text"))
        if not values:
            continue
        x = _number(row.get("model_x", row.get("x")))
        y = _number(row.get("model_y", row.get("y")))
        if x <= 0 and y <= 0:
            continue
        containing = [pid for pid, pts in polygons.items()
                      if point_in_polygon((x, y), pts)]
        if containing:
            host = min(containing, key=lambda pid: _polygon_area(polygons[pid]))
            distance = 0.0
        else:
            host, distance = "", radius + 1.0
            for pid, pts in polygons.items():
                near = min(_distance_to_segment((x, y), pts[index],
                                                pts[(index + 1) % len(pts)])
                           for index in range(len(pts)))
                if near < distance:
                    host, distance = pid, near
            if not host or distance > radius:
                continue
        owners.setdefault(host, []).append({
            "text": _text(row.get("text")),
            "layer": _text(row.get("layer")),
            "thickness_values": sorted(values),
            "distance_mm": round(distance, 1),
        })
    return owners


def _verify_label(owners: dict[str, list[dict[str, Any]]], panel_id: str,
                  thickness_mm: float) -> str:
    """面板是否真的有一处归属自己的板厚文字写明该厚度。"""
    for row in owners.get(panel_id) or []:
        if int(thickness_mm) in row["thickness_values"]:
            return "verified"
    return "unverified"


def _distance_to_segment(point, start, end) -> float:
    px, py = point
    sx, sy = start
    ex, ey = end
    dx, dy = ex - sx, ey - sy
    norm = dx * dx + dy * dy
    ratio = 0.0 if norm <= 1e-12 else max(0.0, min(1.0, ((px - sx) * dx + (py - sy) * dy) / norm))
    return ((px - (sx + ratio * dx)) ** 2 + (py - (sy + ratio * dy)) ** 2) ** 0.5


def _package(rows, totals, fills, notes, legend_rules, note_defaults,
             elevation_regions, options, panels, unverified=None,
             verified=None, no_ledger=None) -> dict[str, Any]:
    area_total = round(totals.get("_area", 0.0), 4)
    volume_current = round(totals.get("_volume_current", 0.0), 4)
    volume_split = round(totals.get("_volume_split", 0.0), 4)
    residual = round(sum(row["identity_residual_m2"] for row in rows), 6)
    covered = round(sum(row["area_m2"] for row in rows), 4)
    grades = {key: value for key, value in sorted(totals.items()) if not key.startswith("_")}
    evidence_by_grade: dict[str, float] = {}
    for row in rows:
        for key, area in row["area_by_grade_m2"].items():
            if key == ELEVATION:
                continue
            head = key.split(":", 1)[0]
            evidence_by_grade[head] = round(evidence_by_grade.get(head, 0.0) + area, 4)
    coverage = round(sum(evidence_by_grade.values()) / covered, 4) if covered else 0.0
    label_priority = bool((options or {}).get("label_priority", True))
    summary = {
        "panel_count": len(rows),
        "panel_area_total_m2": area_total,
        "grid_step_mm": options.get("grid_step_mm", 100.0),
        "label_verify_radius_mm": _number(options.get("label_verify_radius_mm"), 1000.0),
        "area_by_grade_m2": grades,
        "area_by_evidence_m2": evidence_by_grade,
        "evidence_coverage_ratio": coverage,
        "note_default_thickness_mm": note_defaults,
        "legend_note_handles": list((options or {}).get("legend_note_handles") or []),
        "legend_rule_count": len(legend_rules),
        "legend_note_handles": list((options or {}).get("legend_note_handles") or []),
        "legend_rules": [{"handle": _text(row.get("handle")),
                          "thickness_mm": _number(row.get("thickness_mm")),
                          "source_text": _text(row.get("source_text"))}
                         for row in legend_rules],
        "note_rule_handles": [_text(row.get("handle")) for row in notes
                              if _number(row.get("thickness_mm")) > 0
                              and "填充" not in _text(row.get("text"))],
        "fill_rule_sentence_handles": list(
            (options or {}).get("legend_note_handles") or []),
        "fill_region_count": {key: len(value) for key, value in sorted(fills.items())
                              if key != ELEVATION},
        "elevation_only_region_count": len(elevation_regions),
        "elevation_only_area_m2": round(sum(
            row.get("elevation_only_area_m2", 0.0) for row in rows), 4),
        "partitioned_panel_count": sum(1 for row in rows if row["partition_conflict"]),
        "volume_as_assigned_total_m3": volume_current,
        "volume_partitioned_total_m3": volume_split,
        "volume_delta_m3": round(volume_split - volume_current, 4),
        "identity_residual_m2": residual,
        "label_priority": label_priority,
        "label_claim_unverified_count": len(unverified or []),
        "label_claim_unverified_area_m2": round(sum(
            row["area_m2"] for row in (unverified or [])), 4),
        "label_claim_unverified_ids": [row["id"] for row in (unverified or [])][:20],
        "label_claim_verified_count": len(verified or []),
        "label_claim_verified_area_m2": round(sum(
            row["area_m2"] for row in (verified or [])), 4),
        "label_claim_verified_ids": [row["id"] for row in (verified or [])][:20],
        "label_claim_no_ledger_count": len(no_ledger or []),
        "label_recheck_done": bool((options or {}).get("panel_texts")),
    }
    gates = [
        {"id": "slab-thickness-partition-identity",
         "status": "pass" if abs(residual) <= 0.001 else "fail",
         "evidence": (f"{len(rows)} 块面板分档面积合计对平面板面积，残差 {residual} m2；"
                      f"网格 {summary['grid_step_mm']} mm，"
                      f"网格面积与精确面积最大偏差 "
                      f"{max((abs(row['grid_area_m2'] - row['area_m2']) for row in rows), default=0.0):.4f} m2"),
         "action": "分档面积必须等于面板面积，不等先查网格与多边形取向，不得按比例抹平。"},
        {"id": "slab-thickness-evidence-closed",
         "status": ("pass" if coverage >= 0.999 and note_defaults and legend_rules else "fail"),
         "evidence": (f"板厚证据覆盖率 {coverage}（"
                      + "、".join(f"{key} {value} m2" for key, value in evidence_by_grade.items())
                      + f"）；图例句 {len(legend_rules)} 条、说明默认档 {note_defaults} mm，"
                        f"规则句句柄 {summary['note_rule_handles'][:6]}；"
                        f"原记为直接标注但图面查无厚度文字、已降级为说明默认档的 "
                        f"{summary['label_claim_unverified_count']} 块/"
                        f"{summary['label_claim_unverified_area_m2']} m2"),
         "action": "三档证据全部来自图面文字与图例，缺任一类来源不得判闭合。"},
        {"id": "slab-thickness-conflict-partitioned",
         "status": "pass" if summary["partitioned_panel_count"] == 0 or residual <= 0.001 else "warn",
         "evidence": (f"优先级={'直接标注先于图例' if label_priority else '图例先于直接标注'}；"
                      f"{summary['partitioned_panel_count']} 块面板同时跨两个以上厚度档，"
                      f"已按子面域拆分而非整块取一档；体积由 {volume_current} m3 "
                      f"变到 {volume_split} m3（差 {summary['volume_delta_m3']} m3）"),
         "action": "分档体积只用于 CAD 独立量与分档出量，报量仍按材料分账口径，不得两本账相加。"},
        {"id": "slab-label-claim-ownership",
         "status": ("warn" if not summary["label_recheck_done"] else "pass"),
         "evidence": (f"标注档复核未做：没有传入板图文字台账，{summary['label_claim_no_ledger_count']} 块标注档面板无法核对"
                      if not summary["label_recheck_done"] else
                      f"每处板厚文字只归一块面板（包含优先，否则 {summary['label_verify_radius_mm']} mm 内最近）；"
                      f"复核后有归属文字的直接标注 {summary['label_claim_verified_count']} 块/"
                      f"{summary['label_claim_verified_area_m2']} m2，"
                      f"查无归属文字已降级 {summary['label_claim_unverified_count']} 块/"
                      f"{summary['label_claim_unverified_area_m2']} m2"),
         "action": "一处标注不得给多块面板同时当证据；降级面积改按说明默认档计，体积不变只改证据口径。"},
        {"id": "slab-elevation-only-not-thickness",
         "status": "pass",
         "evidence": (f"降板类填充 {len(elevation_regions)} 个、覆盖 "
                      f"{summary['elevation_only_area_m2']} m2 只进浇筑标高控制分区，"
                      f"不改板厚、不改体积"),
         "action": "标高属性与厚度属性分表管理，禁止把降板面积换算成方量。"},
    ]
    return {"schema": SCHEMA, "floor": _text((options or {}).get("floor")),
            "summary": summary, "panels": rows, "gates": gates,
            "applied_to_formal_quantity": False, "formal_ready": False}


def csv_rows(payload: dict[str, Any]) -> list[list[Any]]:
    head = ["面板ID", "归档厚度mm", "归档来源", "标注复核", "面积m2", "分档面积",
            "分档厚度", "整块体积m3", "拆分体积m3", "体积差m3", "跨档", "恒等式残差m2"]
    rows = [head]
    for row in payload["panels"]:
        rows.append([
            row["id"], row["assigned_thickness_mm"], row["assigned_source"],
            LABEL_CLAIM_TEXT.get(row["label_claim"], row["label_claim"]), row["area_m2"],
            "; ".join(f"{key}={area}" for key, area in sorted(row["area_by_grade_m2"].items())),
            "; ".join(f"{key}={th}" for key, th in sorted(row["thickness_by_grade_mm"].items())),
            row["volume_as_assigned_m3"], row["volume_partitioned_m3"],
            row["volume_delta_m3"], "是" if row["partition_conflict"] else "否",
            row["identity_residual_m2"],
        ])
    return rows


def render_markdown(payload: dict[str, Any]) -> str:
    s = payload["summary"]
    lines = ["# 板厚图例填充子面域拆分", ""]
    lines.append(f"{s['panel_count']} 块面板、合计 {s['panel_area_total_m2']} m2，"
                 f"按 {s['grid_step_mm']} mm 网格拆档。证据来源："
                 + "、".join(f"{key} {value} m2" for key, value in s["area_by_evidence_m2"].items())
                 + f"，覆盖率 {s['evidence_coverage_ratio']}。")
    lines.append("")
    lines.append("| 厚度档 | 面积 m2 |")
    lines.append("|---|---|")
    for key, value in s["area_by_grade_m2"].items():
        if key == ELEVATION:
            continue
        lines.append(f"| {key} | {value} |")
    lines.append("")
    legend_sentence = "；".join(
        f"{row['handle']} {row['source_text']}" for row in s["legend_rules"]
    )
    lines.append(f"- 图例句：{legend_sentence}")
    lines.append(f"- 说明默认档：{s['note_default_thickness_mm']} mm，规则句句柄 {s['note_rule_handles']}")
    lines.append(f"- 整块口径体积 {s['volume_as_assigned_total_m3']} m3 → 拆分后 "
                 f"{s['volume_partitioned_total_m3']} m3（差 {s['volume_delta_m3']} m3）；"
                 f"跨档面板 {s['partitioned_panel_count']} 块")
    lines.append(f"- 降板填充只计标高：{s['elevation_only_region_count']} 个区域、"
                 f"{s['elevation_only_area_m2']} m2，体积影响 0")
    if s.get("label_recheck_done"):
        lines.append(f"- 直接标注复核：有归属文字 {s['label_claim_verified_count']} 块/"
                     f"{s['label_claim_verified_area_m2']} m2（{', '.join(s['label_claim_verified_ids'])}）；"
                     f"查无归属文字降级 {s['label_claim_unverified_count']} 块/"
                     f"{s['label_claim_unverified_area_m2']} m2")
    else:
        lines.append("- 直接标注复核：未传入板图文字台账，标注档未核对")
    lines.append("")
    lines.append("## 差异最大的面板（前 15）")
    lines.append("")
    lines.append("| 面板 | 归档 | 面积 m2 | 分档面积 | 体积差 m3 |")
    lines.append("|---|---|---|---|---|")
    for row in payload["panels"][:15]:
        if not row["partition_conflict"] and abs(row["volume_delta_m3"]) <= 1e-9:
            continue
        lines.append(f"| {row['id']} | {row['assigned_thickness_mm']:.0f}/"
                     f"{row['assigned_source']} | {row['area_m2']} | "
                     + "<br>".join(f"{k} {v}" for k, v in sorted(row["area_by_grade_m2"].items()))
                     + f" | {row['volume_delta_m3']} |")
    lines.append("")
    for gate in payload["gates"]:
        lines.append(f"- [{gate['status']}] {gate['id']}：{gate['evidence']} 处理：{gate['action']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="板厚图例填充子面域拆分")
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--notes-json", default=None,
                        help="图面板厚规则句（含句柄与坐标）JSON 列表")
    parser.add_argument("--frame-bbox", default=None,
                        help="规则句归属图框窗口 x0,y0,x1,y1（图面坐标），只采信框内规则句")
    parser.add_argument("--panel-texts-json", default=None,
                        help="板图文字台账（含 model_x/model_y 与 text），用于复核直接标注")
    parser.add_argument("--label-verify-radius-mm", type=float, default=1000.0)
    parser.add_argument("--grid-step-mm", type=float, default=100.0)
    parser.add_argument("--fill-over-label", action="store_true",
                        help="改按图例填充优先定档（默认直接标注优先）")
    parser.add_argument("-o", "--out", required=True)
    args = parser.parse_args()

    model = _load(args.model_json)
    notes = _read_notes(args.notes_json)
    if args.frame_bbox:
        box = [float(value) for value in args.frame_bbox.split(",")]
        notes = [row for row in notes
                 if box[0] <= _number(row.get("x")) <= box[2]
                 and box[1] <= _number(row.get("y")) <= box[3]]
    base_options = {"grid_step_mm": args.grid_step_mm,
                    "panel_texts": _read_notes(args.panel_texts_json),
                    "label_verify_radius_mm": args.label_verify_radius_mm,
                    "floor": _text(model.get("floor")),
                    "label_priority": not args.fill_over_label}
    payload = build_partition(model, notes, base_options)
    other = dict(base_options)
    other["label_priority"] = not base_options["label_priority"]
    alt = build_partition(model, notes, other)
    mine = payload["summary"]["volume_partitioned_total_m3"]
    theirs = alt["summary"]["volume_partitioned_total_m3"]
    payload["summary"]["priority_sensitivity"] = {
        "label_first_volume_m3": mine if base_options["label_priority"] else theirs,
        "fill_first_volume_m3": theirs if base_options["label_priority"] else mine,
        "run_mode": "label-first" if base_options["label_priority"] else "fill-first",
    }
    payload["summary"]["priority_swing_m3"] = round(abs(mine - theirs), 4)
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
    summary = payload["summary"]
    print(json.dumps({
        "panel_count": summary["panel_count"],
        "evidence_coverage_ratio": summary["evidence_coverage_ratio"],
        "partitioned_panel_count": summary["partitioned_panel_count"],
        "volume_as_assigned_total_m3": summary["volume_as_assigned_total_m3"],
        "volume_partitioned_total_m3": summary["volume_partitioned_total_m3"],
        "volume_delta_m3": summary["volume_delta_m3"],
        "identity_residual_m2": summary["identity_residual_m2"],
        "priority_sensitivity": summary.get("priority_sensitivity"),
        "priority_swing_m3": summary.get("priority_swing_m3"),
        "gates": {row["id"]: row["status"] for row in payload["gates"]},
        "outputs": [str(json_path), str(csv_path), str(md_path)],
    }, ensure_ascii=False))
    return 0


def _read_notes(path: str | None) -> list[dict[str, Any]]:
    if not path:
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("records") or data.get("notes") or []
    return [row for row in data if isinstance(row, dict)]


if __name__ == "__main__":
    raise SystemExit(main())
