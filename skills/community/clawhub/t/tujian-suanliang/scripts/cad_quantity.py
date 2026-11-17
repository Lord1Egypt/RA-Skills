#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cad_quantity.py - 把 CAD 识别结果整理成“单层混凝土初算/缺口报告”。

本脚本不把启发式结果伪装成模型算量。它读取 cad_scan.py 的文字/构件/图层几何结果，
按楼层整理梁、板、墙柱图纸，尽量绑定层高表和混凝土等级，并明确列出哪些构件
仍因几何缺失而不能计算。

推荐输入：
  cad_scan.sh 图纸.dwg --with-mtext --with-geom --with-geom-layer \
      --detail-json 图纸.detail.json --format json -o 图纸.scan
  cad_quantity.sh --scan 图纸.scan.json --detail 图纸.detail.json --floor 一层
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
import io
import json
import math
import os
import re
import sys

import i18n
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Optional

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
VENDOR_DIR = SKILL_DIR / "vendor"
if VENDOR_DIR.exists():
    sys.path.insert(0, str(VENDOR_DIR))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import cad_scan  # noqa: E402
import cad_interpret  # noqa: E402


# ---------------------------------------------------------------- 楼层/图纸名
CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
          "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
          "十一": 11, "十二": 12, "十三": 13, "十四": 14, "十五": 15,
          "十六": 16, "十七": 17, "十八": 18, "十九": 19, "二十": 20,
          "二十一": 21, "二十二": 22, "二十三": 23, "二十四": 24,
          "二十五": 25, "二十六": 26, "二十七": 27, "二十八": 28,
          "二十九": 29, "三十": 30}
CN_NUM_PAT = re.compile("|".join(sorted(CN_NUM, key=len, reverse=True)))


def _cn_to_no(text: str) -> Optional[int]:
    text = str(text or "").strip().replace(" ", "")
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        pass
    if text in ("-1", "负一层", "地下一层", "地下室"):
        return -1
    if text == "屋面":
        return 99
    if text == "机房层":
        return 100
    m = CN_NUM_PAT.match(text)
    if m:
        return CN_NUM[m.group(0)]
    return None


def floor_label_kind(label: str) -> tuple[Optional[int], Optional[int], str]:
    """解析“一层梁平法施工图 / 三层~五层板结构施工图 / 标高xx~xx墙柱...”。

    返回 (起层, 止层, 图纸类型)。无法解析时起止层为 None。
    """
    text = str(label or "").replace(" ", "")
    kind = ""
    for k in ("墙柱平法施工图", "板结构施工图", "梁平法施工图", "基础平面布置图"):
        if k in text:
            kind = k
            break
    if kind == "墙柱平法施工图":
        m = re.search(r"标高(-?\d+(?:\.\d+)?)~(-?\d+(?:\.\d+)?)", text)
        return (None, None, kind) if m else (None, None, kind)
    m = re.search(r"(\d{1,2})层~(\d{1,2})层", text)
    if m:
        return int(m.group(1)), int(m.group(2)), kind
    m = re.search(r"([一二十三四五六七八九零〇]+)层~([一二十三四五六七八九零〇]+)层", text)
    if m:
        a, b = _cn_to_no(m.group(1)), _cn_to_no(m.group(2))
        return a, b, kind
    m = re.search(r"(\d{1,2})层", text)
    if m:
        return int(m.group(1)), int(m.group(1)), kind
    for match in re.finditer(CN_NUM_PAT, text):
        if match.end() < len(text) and text[match.end():match.end() + 1] == "层":
            n = CN_NUM[match.group(0)]
            return n, n, kind
    if "屋面" in text:
        return 99, 99, kind
    if "机房" in text:
        return 100, 100, kind
    return None, None, kind


def sheet_labels(data: dict[str, Any]) -> dict[str, str]:
    return cad_interpret.detect_sheet_labels(data)


def _rec_sheet_key(rec: dict[str, Any]) -> tuple[str, str]:
    return (str(rec.get("file") or ""), str(rec.get("sheet") or ""))


def group_text_by_sheet(data: dict[str, Any]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for rec in data.get("text_records") or []:
        groups[_rec_sheet_key(rec)].append(rec)
    return groups


# ---------------------------------------------------------------- 层高表
def _norm_no_space(text: str) -> str:
    return re.sub(r"\s+", "", str(text or ""))


def find_story_sheet(data: dict[str, Any]) -> Optional[tuple[str, str]]:
    """找含“层号 + 标高 + 层高 + 混凝土强度等级”的图框。"""
    groups = group_text_by_sheet(data)
    best: Optional[tuple[tuple[str, str], int]] = None
    for key, recs in groups.items():
        text = "\n".join(_norm_no_space(r.get("text")) for r in recs)
        score = sum(1 for word in ("层号", "标高(m)", "层高(m)", "混凝土强度等级",
                                   "墙、柱、连梁", "梁、板")
                    if word in text)
        if score >= 4 and (best is None or score > best[1]):
            best = (key, score)
    return best[0] if best else None


def _header_text(data: dict[str, Any], key: tuple[str, str], header_y: float,
                 aliases: tuple[str, ...]) -> Optional[dict[str, Any]]:
    groups = group_text_by_sheet(data)
    recs = groups.get(key, [])
    candidates = []
    for rec in recs:
        txt = _norm_no_space(str(rec.get("text") or ""))
        if any(txt == a or a in txt for a in aliases):
            candidates.append(rec)
    if not candidates:
        return None
    return min(candidates, key=lambda r: abs(float(r.get("y") or 0) - header_y))


def parse_story_rows(data: dict[str, Any]) -> dict[str, Any]:
    """把层高表按 CAD 坐标还原成行；这是后续混凝土等级绑定的基础。"""
    key = find_story_sheet(data)
    if not key:
        return {"sheet": None, "rows": [], "status": "no-story-table"}
    groups = group_text_by_sheet(data)
    recs = groups.get(key, [])

    layer_hdr = None
    elev_hdr = None
    height_hdr = None
    wall_hdr = None
    beam_hdr = None
    grade_hdr = None
    for rec in recs:
        txt = _norm_no_space(str(rec.get("text") or ""))
        if txt == "层号":
            layer_hdr = rec
    if layer_hdr is None:
        return {"sheet": list(key), "rows": [], "status": "no-layer-header"}
    header_y = float(layer_hdr.get("y") or 0)
    elev_hdr = _header_text(data, key, header_y, ("标高(m)", "标高（m）", "结构楼层标高"))
    height_hdr = _header_text(data, key, header_y, ("层高(m)", "层高（m）", "结构层高"))
    wall_hdr = _header_text(data, key, header_y, ("墙、柱、连梁", "墙柱连梁"))
    beam_hdr = _header_text(data, key, header_y, ("梁、板",))
    grade_hdr = _header_text(data, key, header_y, ("混凝土强度等级",))

    layer_x = float(layer_hdr.get("x") or 0)
    elev_x = float(elev_hdr.get("x") or 0) if elev_hdr else None
    height_x = float(height_hdr.get("x") or 0) if height_hdr else None
    wall_x = float(wall_hdr.get("x") or 0) if wall_hdr else None
    beam_x = float(beam_hdr.get("x") or 0) if beam_hdr else None

    # 行锚点：层号列中位于表头下方、内容像楼层号/屋面/机房层的记录。
    anchors = []
    for rec in recs:
        try:
            x, y = float(rec.get("x")), float(rec.get("y"))
        except (TypeError, ValueError):
            continue
        if abs(x - layer_x) > 1500 or y <= header_y + 200:
            continue
        txt = _norm_no_space(str(rec.get("text") or ""))
        if _cn_to_no(txt) is not None:
            anchors.append((y, txt, rec))
    anchors = sorted(anchors)
    merged: list[tuple[float, list[tuple[float, str, dict]]]] = []
    for item in anchors:
        if merged and item[0] - merged[-1][0] < 300:
            merged[-1][1].append(item)
        else:
            merged.append((item[0], [item]))
    rows_meta: list[tuple[float, str]] = []
    for y, items in merged:
        best = min(items, key=lambda z: abs(z[0] - y))
        rows_meta.append((y, best[1]))

    def recs_near(x_anchor: Optional[float], y: float, max_dx: float,
                  max_dy: float, pattern: Optional[re.Pattern] = None,
                  text_not: Optional[re.Pattern] = None) -> list[dict[str, Any]]:
        if x_anchor is None:
            return []
        out = []
        for rec in recs:
            try:
                xx, yy = float(rec.get("x")), float(rec.get("y"))
            except (TypeError, ValueError):
                continue
            if abs(xx - x_anchor) > max_dx or abs(yy - y) > max_dy:
                continue
            txt = str(rec.get("text") or "").strip()
            if not txt:
                continue
            if pattern and not pattern.search(txt):
                continue
            if text_not and text_not.search(txt):
                continue
            out.append(rec)
        return out

    # 混凝土等级常见跨多行合并单元格，按同列相邻“Cxx”的中点切开，再分给所在楼层行。
    wall_grades: list[tuple[float, str]] = []
    beam_grades: list[tuple[float, str]] = []
    for rec in recs:
        try:
            xx, yy = float(rec.get("x")), float(rec.get("y"))
        except (TypeError, ValueError):
            continue
        m = re.search(r"(?<![A-Za-z0-9])(C\d{2})(?!\d)", str(rec.get("text") or "").upper())
        if not m or yy <= header_y + 200:
            continue
        if wall_x is not None and beam_x is not None:
            if abs(xx - wall_x) <= abs(xx - beam_x) and abs(xx - wall_x) <= 2500:
                wall_grades.append((yy, m.group(1)))
            elif abs(xx - beam_x) <= 2500:
                beam_grades.append((yy, m.group(1)))
        elif grade_hdr is not None:
            try:
                if abs(xx - float(grade_hdr.get("x") or 0)) <= 2500:
                    wall_grades.append((yy, m.group(1)))
            except (TypeError, ValueError):
                pass

    def vertical_assign(items: list[tuple[float, str]], y: float,
                        header_y: float) -> str:
        if not items:
            return ""
        items = sorted(items)
        boundaries = [header_y]
        for i in range(1, len(items)):
            boundaries.append((items[i - 1][0] + items[i][0]) / 2.0)
        boundaries.append(float("inf"))
        for idx, (yy, grade) in enumerate(items):
            if boundaries[idx] <= y < boundaries[idx + 1]:
                return grade
        # 最后一段延伸到表底；若行已超过最后一个 Cxx，仍沿用最后等级。
        return items[-1][1]

    rows = []
    for y, label in rows_meta:
        floor_no = _cn_to_no(label)
        elev_src = recs_near(elev_x, y, 1000, 500, re.compile(r"\d+\.\d+"))
        height_src = recs_near(height_x, y, 600, 500, re.compile(r"\d+\.\d+"))
        wall_src = [r for r in recs_near(wall_x, y, 2600, 500) if re.search(r"C\d{2}", str(r.get("text") or ""), re.I)]
        beam_src = [r for r in recs_near(beam_x, y, 2600, 500) if re.search(r"C\d{2}", str(r.get("text") or ""), re.I)]
        row: dict[str, Any] = {
            "floor_label": label,
            "floor_no": floor_no,
            "structural_elevation_m": _first_float([r.get("text") for r in elev_src]),
            "floor_height_m": _first_float([r.get("text") for r in height_src]),
            "wall_column_concrete": vertical_assign(wall_grades, y, header_y),
            "beam_slab_concrete": vertical_assign(beam_grades, y, header_y),
            "grade_method": "vertical-cell-span [推测]",
            "source_texts": {
                "elevation": " ".join(str(r.get("text")) for r in elev_src)[:80],
                "height": " ".join(str(r.get("text")) for r in height_src)[:80],
                "wall_column": " ".join(str(r.get("text")) for r in wall_src)[:80],
                "beam_slab": " ".join(str(r.get("text")) for r in beam_src)[:80],
            },
        }
        rows.append(row)

    rows.sort(key=lambda r: (r["floor_no"] is None, r["floor_no"] if r["floor_no"] is not None else 9999))
    return {
        "sheet": {"file": key[0], "sheet_id": key[1]},
        "rows": rows,
        "status": "parsed",
        "header_y": header_y,
        "raw_count": len(recs),
    }


def _first_float(texts: list[str]) -> Optional[float]:
    for text in texts:
        m = re.search(r"[-+]?\d+(?:\.\d+)?", str(text))
        if m:
            try:
                return float(m.group(0))
            except ValueError:
                continue
    return None


def _first_c(texts: list[str]) -> str:
    for text in texts:
        m = re.search(r"(?<![A-Za-z0-9])(C\d{2})(?!\d)", str(text).upper())
        if m:
            return m.group(1)
    return ""


def story_grade_for_floor(story: dict[str, Any], floor_no: Optional[int],
                          component: str) -> tuple[str, str]:
    if story.get("status") != "parsed":
        return "", "no-story-table"
    if floor_no is None:
        return "", "floor-not-numbered"
    rows = story.get("rows") or []
    row = next((r for r in rows if r.get("floor_no") == floor_no), None)
    if not row:
        return "", "floor-not-in-table"
    if component in ("beam", "slab"):
        grade = row.get("beam_slab_concrete") or ""
    else:
        grade = row.get("wall_column_concrete") or ""
    return grade, "story-table" if grade else "grade-missing"


# ---------------------------------------------------------------- 楼层图纸
def plan_registry(data: dict[str, Any]) -> list[dict[str, Any]]:
    labels = sheet_labels(data)
    sheets = data.get("meta") or {}
    out = []
    for sid, label in labels.items():
        sheet_meta = next((s for s in sheets.get("sheets") or [] if str(s.get("id")) == str(sid)), {})
        lo, hi, kind = floor_label_kind(label)
        out.append({
            "sheet": str(sid),
            "label": label,
            "file": sheet_meta.get("file", ""),
            "kind": kind,
            "floor_from": lo,
            "floor_to": hi,
            "bbox": sheet_meta.get("bbox"),
        })
    out.sort(key=lambda x: (x["kind"], x["floor_from"] if x["floor_from"] is not None else 999))
    return out


def _matches_floor(plan: dict[str, Any], floor_no: Optional[int]) -> bool:
    if plan.get("kind") not in ("梁平法施工图", "板结构施工图"):
        return False
    a, b = plan.get("floor_from"), plan.get("floor_to")
    return a is not None and floor_no is not None and a <= floor_no <= b


def selected_sheets(plans: list[dict[str, Any]], floor_no: Optional[int],
                    kind: str) -> list[dict[str, Any]]:
    return [p for p in plans if p.get("kind") == kind and _matches_floor(p, floor_no)]


# ---------------------------------------------------------------- 几何
def _sheet_bbox(data: dict[str, Any], sheet: str) -> Optional[list[float]]:
    for s in (data.get("meta") or {}).get("sheets") or []:
        if str(s.get("id")) == str(sheet):
            b = s.get("bbox")
            return list(b) if b else None
    return None


def clip_geometry_by_sheet(data: dict[str, Any], sheet: str,
                           margin: float = 25000.0) -> tuple[list[list[float]], list[str]]:
    bbox = _sheet_bbox(data, sheet)
    if not bbox:
        return [], []
    x0, y0, x1, y1 = bbox
    geom = data.get("geometry_segments") or []
    layers = data.get("geometry_layers") or []
    if not geom:
        return [], []
    segs: list[list[float]] = []
    layer_names: list[str] = []
    for fi, file_segs in enumerate(geom):
        file_layers = layers[fi] if fi < len(layers) else []
        for i, seg in enumerate(file_segs):
            try:
                mx = (float(seg[0]) + float(seg[2])) / 2.0
                my = (float(seg[1]) + float(seg[3])) / 2.0
            except (TypeError, ValueError, IndexError):
                continue
            if x0 - margin <= mx <= x1 + margin and y0 - margin <= my <= y1 + margin:
                segs.append([float(v) for v in seg[:4]])
                layer_names.append(str(file_layers[i] or "") if i < len(file_layers) else "")
    return segs, layer_names


def component_layer_counts(segs: list[list[float]], layers: list[str],
                           component: str) -> Counter:
    hints = {
        "beam": ("梁-实线", "梁-虚线", "梁实线", "梁虚线", "BEAM"),
        "slab": ("板边线", "板板边线", "降板边线", "S-SLAB"),
        "wall_column": ("剪力墙", "S-柱", "COLU", "WALL", "砼墙"),
    }[component]
    return Counter(
        layer for layer in layers
        if any(h.lower() in str(layer).lower() for h in hints)
    )


def closed_loop_count(segs: list[list[float]]) -> int:
    """极粗的板/墙轮廓闭合提示：统计近似首尾相接的多段线数量，不替代区域建模。"""
    if not segs:
        return 0
    vertices = []
    for seg in segs:
        try:
            vertices.append(((float(seg[0]), float(seg[1])), (float(seg[2]), float(seg[3]))))
        except (TypeError, ValueError, IndexError):
            continue
    pts = []
    for a, b in vertices:
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) <= 100:
            continue
        pts.append(a)
        pts.append(b)
    from collections import Counter as _C
    counts = _C(pts)
    endpoints = sum(v for v in counts.values() if v == 1)
    if not pts:
        return 0
    return int(round(len(set(pts)) * endpoints / max(1, len(pts)) / 8))


def _interval_merge(items: list[list[float]]) -> list[list[float]]:
    items = sorted(items)
    out: list[list[float]] = []
    for a, b in items:
        if not out or a - out[-1][1] > 200:
            out.append([a, b])
        else:
            out[-1][1] = max(out[-1][1], b)
    return out


def beam_run_length(segments: list[list[float]], x: float, y: float) -> Optional[float]:
    """沿梁标注附近最长共线线段合并出图面梁长证据；不是支座净跨。"""
    if not segments or x is None or y is None:
        return None
    try:
        import numpy as np
    except Exception:
        return None
    try:
        S = np.asarray(segments, float)
        if S.ndim != 2 or S.shape[1] < 4:
            return None
        mx = (S[:, 0] + S[:, 2]) / 2.0
        my = (S[:, 1] + S[:, 3]) / 2.0
        ang = np.degrees(np.arctan2(S[:, 3] - S[:, 1], S[:, 2] - S[:, 0])) % 180.0
        ln = np.hypot(S[:, 2] - S[:, 0], S[:, 3] - S[:, 1])
        near = np.nonzero((np.hypot(mx - x, my - y) <= 3500.0) & (ln > 500.0))[0]
        if near.size == 0:
            return None
        base = near[int(np.argmax(ln[near]))]
        a0 = ang[base]
        same = near[np.abs(((ang[near] - a0 + 90.0) % 180.0) - 90.0) <= 3.0]
        if same.size == 0:
            return None
        ux = math.cos(math.radians(a0))
        uy = math.sin(math.radians(a0))
        intervals = []
        for i in same:
            p1 = (S[i, 0] - x) * ux + (S[i, 1] - y) * uy
            p2 = (S[i, 2] - x) * ux + (S[i, 3] - y) * uy
            intervals.append([min(p1, p2), max(p1, p2)])
        merged = _interval_merge(intervals)
        if not merged:
            return None
        best = max(merged, key=lambda z: z[1] - z[0])
        return best[1] - best[0]
    except Exception:
        return None


def floor_beam_concrete(data: dict[str, Any], floor_label: Optional[str] = None) -> dict[str, Any]:
    """按梁平法施工图初算该层梁混凝土；属于土建算量层，不含板、墙、柱。"""
    instances = cad_interpret.beam_instances(data)
    if floor_label:
        instances = [r for r in instances if r.get("sheet_label") == floor_label]
    else:
        instances = [r for r in instances if r.get("is_beam_plan")]
    geom_files = data.get("geometry_segments") or []
    rows = []
    by_floor: dict[str, dict[str, float]] = defaultdict(lambda: {"total_m3": 0.0, "with_section": 0.0,
                                                                  "with_length": 0.0, "count": 0.0})
    for r in instances:
        by_floor[r.get("sheet_label") or "-"]["count"] += 1
        section = r.get("section") or ""
        b = h = None
        try:
            b, h = (int(x) for x in section.split("x"))
        except Exception:
            pass
        if not (b and h):
            member = (data.get("members") or {}).get("梁", {}).get(r.get("code") or "")
            if member:
                try:
                    b = int(member.get("b"))
                    h = int(member.get("h"))
                    section = f"{b}x{h}"
                except (TypeError, ValueError):
                    pass
        if b and h:
            by_floor[r.get("sheet_label") or "-"]["with_section"] += 1
        length = None
        file_idx = next((i for i, f in enumerate(data.get("files") or []) if f.get("name") == r.get("file")), 0)
        segs = geom_files[file_idx] if file_idx < len(geom_files) else None
        if segs:
            length = beam_run_length(segs, r.get("x"), r.get("y"))
        if length:
            by_floor[r.get("sheet_label") or "-"]["with_length"] += 1
        vol = b * h * length / 1e9 if b and h and length else 0.0
        if vol:
            by_floor[r.get("sheet_label") or "-"]["total_m3"] += vol
        rows.append({
            "code": r.get("code"),
            "sheet_label": r.get("sheet_label"),
            "section": section,
            "length_mm": round(length, 1) if length else None,
            "concrete_grade": "未自动判定",
            "volume_m3": round(vol, 4) if vol else 0.0,
            "volume_status": "ok" if vol else ("no-section" if not (b and h) else "no-length"),
            "x": r.get("x"),
            "y": r.get("y"),
        })
    floors = []
    for label, stats in sorted(by_floor.items()):
        floors.append({
            "sheet_label": label,
            "beam_instances": int(stats["count"]),
            "with_section": int(stats["with_section"]),
            "with_length": int(stats["with_length"]),
            "beam_concrete_m3": round(stats["total_m3"], 2),
            "note": "仅梁混凝土初算，不含板、墙、柱；长度按图面共线线段合并",
        })
    return {"floors": floors, "rows": rows}


# ---------------------------------------------------------------- 汇总
def beam_rows_with_grade(data: dict[str, Any], plan: dict[str, Any],
                         story: dict[str, Any]) -> list[dict[str, Any]]:
    result = floor_beam_concrete(data, plan["label"])
    floor_no = plan.get("floor_from")
    grade, grade_status = story_grade_for_floor(story, floor_no, "beam")
    rows = []
    for row in result.get("rows") or []:
        r = dict(row)
        r["concrete_grade"] = grade or r.get("concrete_grade") or ""
        r["grade_status"] = grade_status
        r["sheet"] = plan["sheet"]
        r["sheet_label"] = plan["label"]
        rows.append(r)
    return rows


def plate_region_texts(data: dict[str, Any], sheet: str) -> list[dict[str, Any]]:
    """取板图文字里像区域说明/板厚的行，只作覆盖度报告。"""
    out = []
    for rec in data.get("text_records") or []:
        if str(rec.get("sheet") or "") != str(sheet):
            continue
        text = str(rec.get("text") or "").strip()
        if not text:
            continue
        if re.search(r"(板厚|板配筋|双层双向|板顶标高)", text):
            out.append({
                "text": cad_scan.clean_mtext(text)[:180],
                "x": rec.get("x"), "y": rec.get("y"),
            })
    return out[:500]


def component_summary(data: dict[str, Any], plan: dict[str, Any],
                      story: dict[str, Any], component: str) -> dict[str, Any]:
    if component == "beam":
        rows = beam_rows_with_grade(data, plan, story)
        total = sum(float(r.get("volume_m3") or 0) for r in rows)
        by_grade: dict[str, float] = defaultdict(float)
        for r in rows:
            by_grade[r.get("concrete_grade") or "未判定"] += float(r.get("volume_m3") or 0)
        return {
            "component": "梁",
            "sheet": plan["sheet"],
            "sheet_label": plan["label"],
            "status": "粗略CAD梁体积，未扣支座/叠合板扣减",
            "rows": rows,
            "total_m3": round(total, 3),
            "by_concrete_m3": {k: round(v, 3) for k, v in sorted(by_grade.items())},
        }
    if component == "slab":
        segs, layers = clip_geometry_by_sheet(data, plan["sheet"])
        texts = plate_region_texts(data, plan["sheet"])
        grade, grade_status = story_grade_for_floor(story, plan.get("floor_from"), "slab")
        return {
            "component": "板",
            "sheet": plan["sheet"],
            "sheet_label": plan["label"],
            "status": "只能报告文字/轮廓线索，不能直接给可靠面积方量",
            "rows": [],
            "total_m3": None,
            "text_clues": len(texts),
            "geometry_segments": len(segs),
            "slab_layer_segments": sum(component_layer_counts(segs, layers, "slab").values()),
            "closed_loop_hint": closed_loop_count(segs),
            "grade": grade,
            "grade_status": grade_status,
            "notes": "需要闭合板边界 + 板厚 + 洞口扣减后才可计算",
        }
    return {
        "component": "墙柱",
        "sheet": plan["sheet"],
        "sheet_label": plan["label"],
        "status": "墙柱图按标高范围出图，单层拆分未建模",
        "rows": [],
        "total_m3": None,
        "notes": "需要墙柱轮廓 + 层高 + 混凝土等级 + 门窗/洞口扣减",
    }


def build_report(data: dict[str, Any], floor: Optional[str] = None) -> dict[str, Any]:
    labels = sheet_labels(data)
    plans = plan_registry(data)
    story = parse_story_rows(data)

    # 楼层匹配：中文/数字/图纸名均可。
    floor_no: Optional[int] = _cn_to_no(floor or "")
    if floor_no is None and floor:
        lowered = re.sub(r"\s+", "", floor or "")
        if "屋面" in lowered:
            floor_no = 99
        elif "机房" in lowered:
            floor_no = 100
    if floor_no is None:
        # 自动选一层梁平法图作为演示层；调用方也可传 --floor。
        first_beam = next((p for p in plans if p.get("kind") == "梁平法施工图" and p.get("floor_from") is not None), None)
        floor_no = first_beam.get("floor_from") if first_beam else None
        floor = "自动"

    beam_plans = selected_sheets(plans, floor_no, "梁平法施工图")
    slab_plans = selected_sheets(plans, floor_no, "板结构施工图")
    wall_plans = [p for p in plans if p.get("kind") == "墙柱平法施工图"]

    components = []
    for plan in beam_plans:
        components.append(component_summary(data, plan, story, "beam"))
    for plan in slab_plans:
        components.append(component_summary(data, plan, story, "slab"))
    for plan in wall_plans:
        components.append(component_summary(data, plan, story, "wall_column"))

    story_row = next((r for r in story.get("rows") or [] if r.get("floor_no") == floor_no), None)
    report = {
        "floor_query": floor,
        "floor_no": floor_no,
        "story_table": story,
        "story_row_for_floor": story_row,
        "sheet_count": len((data.get("meta") or {}).get("sheets") or []) or len(labels),
        "sheet_labels": labels,
        "plan_registry": plans,
        "beam_plan_sheets": beam_plans,
        "slab_plan_sheets": slab_plans,
        "wall_column_plan_sheets": wall_plans,
        "components": components,
        "status": "初算/缺口报告",
        "disclaimer": "仅基于CAD自动识别，未做净跨、扣减和模型拓扑验证；不能替代广联达模型或结算。",
    }
    return report


def render_md(report: dict[str, Any]) -> str:
    o = ["# CAD 单层混凝土初算与缺口报告", ""]
    o.append(f"- 查询楼层：`{report['floor_query']}`，解析为楼层 `{report['floor_no']}`")
    o.append(f"- 图框数：{report['sheet_count']}")
    o.append(f"- 状态：{report['status']}")
    o.append(f"- 口径：{report['disclaimer']}")
    o.append("")
    story = report.get("story_table") or {}
    o.append("## 层高表识别")
    o.append("")
    if story.get("status") == "parsed":
        o.append("| 楼层 | 标高(m) | 层高(m) | 墙柱连梁混凝土 | 梁板混凝土 |")
        o.append("|---|---:|---:|---|---|")
        for row in story.get("rows") or []:
            o.append(f"| {row.get('floor_label')} | {row.get('structural_elevation_m') or '-'} | "
                     f"{row.get('floor_height_m') or '-'} | {row.get('wall_column_concrete') or '-'} | "
                     f"{row.get('beam_slab_concrete') or '-'} |")
    else:
        o.append(f"未识别层高表：`{story.get('status')}`")
    if story.get("status") == "parsed":
        o.append("")
        o.append("> 层高表若存在跨行合并单元格，混凝土等级按相邻 Cxx 中点分摊，为自动推测，需按图核对。")
    o.append("")
    o.append("## 本层图纸与可算构件")
    o.append("")
    for comp in report.get("components") or []:
        o.append(f"### {comp['component']} · {comp['sheet_label']}")
        o.append("")
        o.append(f"- 图框：{comp.get('sheet')}")
        o.append(f"- 状态：{comp.get('status')}")
        if comp.get("total_m3") is not None:
            o.append(f"- 自动体积合计：{comp['total_m3']} m3")
            if comp.get("by_concrete_m3"):
                grade_txt = "；".join(f"{k} {v}m3" for k, v in comp["by_concrete_m3"].items())
                o.append(f"- 按混凝土等级：{grade_txt}")
        if comp.get("grade"):
            o.append(f"- 混凝土等级（层高表绑定）：{comp.get('grade')} / {comp.get('grade_status')}")
        if comp.get("text_clues") is not None:
            o.append(f"- 板图文字线索：{comp.get('text_clues')} 条")
            o.append(f"- 图框内几何段：{comp.get('geometry_segments')} 条，板轮廓图层段：{comp.get('slab_layer_segments')} 条")
            o.append(f"- 闭合轮廓粗提示：{comp.get('closed_loop_hint')}")
        if comp.get("notes"):
            o.append(f"- 缺口：{comp.get('notes')}")
        o.append("")
    story_row = report.get("story_row_for_floor")
    if story_row:
        o.append("## 本层设计参数")
        o.append("")
        o.append(f"- 结构标高：{story_row.get('structural_elevation_m')} m")
        o.append(f"- 层高：{story_row.get('floor_height_m')} m")
        o.append(f"- 墙柱混凝土：{story_row.get('wall_column_concrete') or '未识别'}")
        o.append(f"- 梁板混凝土：{story_row.get('beam_slab_concrete') or '未识别'}")
        o.append("")
    o.append("> 本报告由 cad_quantity.py 自动生成，供能力验证和人工复核，不作为工程量交付。")
    return "\n".join(o)


def csv_rows(report: dict[str, Any]) -> list[list[str]]:
    out = []
    for comp in report.get("components") or []:
        if not comp.get("rows"):
            out.append([comp["component"], comp["sheet_label"], comp.get("sheet", ""),
                        "", "", comp.get("status") or "", comp.get("notes") or ""])
            continue
        for row in comp.get("rows") or []:
            out.append([
                comp["component"], comp["sheet_label"], comp.get("sheet", ""),
                row.get("code") or "", row.get("section") or "",
                str(row.get("length_mm") or ""), str(row.get("concrete_grade") or ""),
                str(row.get("volume_m3") or ""), row.get("volume_status") or "",
                row.get("grade_status") or "",
            ])
    return out


def _start_mem_guard(name: str = "tujian_quantity内存闸") -> str:
    """挂 cad-file-reader 的进程内内存看门狗；底座不在时降级返回原因，不阻断主流程。"""
    root = Path.home()
    candidates = []
    override = os.environ.get("CAD_SKILL_DIR", "").strip()
    if override:
        candidates.append(Path(override).expanduser() / "scripts")
    for parent in list(Path(__file__).resolve().parents)[1:4]:
        candidates.append(parent / "cad-file-reader" / "scripts")
    candidates.extend([
        root / ".workbuddy" / "skills" / "cad-file-reader" / "scripts",
        root / ".codex" / "skills" / "cad-file-reader" / "scripts",
    ])
    for candidate in candidates:
        if (candidate / "cad_common.py").is_file():
            try:
                if str(candidate) not in sys.path:
                    sys.path.insert(0, str(candidate))
                from cad_common import start_mem_guard
                return start_mem_guard(name=name)
            except Exception as exc:
                return f"degraded:{type(exc).__name__}:{exc}"
    return "unavailable:cad-file-reader 未找到"


def main() -> int:
    mem_guard = _start_mem_guard()
    raw = sys.argv[1:]
    lang = i18n.argv_lang(raw)
    desc = ("CAD single-floor concrete estimate & gap report." if lang == "en" else "CAD 单层混凝土初算与缺口报告")
    ap = argparse.ArgumentParser(description=desc)
    i18n.add_lang_arg(ap, default=lang)
    ap.add_argument("--scan", required=True, help="cad_scan JSON" if lang == "en" else "cad_scan 的 JSON")
    ap.add_argument("--detail", default=None, help="cad_scan --detail-json" if lang == "en" else "cad_scan --detail-json")
    ap.add_argument("--floor", default=None, help="e.g. first/second/roof floor" if lang == "en" else "如：一层/1/屋面层")
    ap.add_argument("--format", default="md", choices=["md", "json", "csv", "all"])
    ap.add_argument("-o", "--out", default=None, help="output prefix" if lang == "en" else "输出前缀")
    args = ap.parse_args(raw)

    wn = ("written" if lang == "en" else "已写出")
    rd = "read --scan failed" if lang == "en" else "读取 --scan 失败"
    ddf = "read --detail failed" if lang == "en" else "读取 --detail 失败"

    try:
        data = json.loads(Path(args.scan).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"{rd}：{exc}", file=sys.stderr)
        return 2
    if args.detail and Path(args.detail).exists():
        try:
            data.update(json.loads(Path(args.detail).read_text(encoding="utf-8")))
        except Exception as exc:
            print(f"{ddf}：{exc}", file=sys.stderr)
            return 2
    elif not data.get("text_records"):
        side = Path(args.scan).with_name(Path(args.scan).stem + ".detail.json")
        if side.exists():
            try:
                data.update(json.loads(side.read_text(encoding="utf-8")))
            except Exception:
                pass

    report = build_report(data, args.floor)
    if args.format in ("md", "all"):
        text = render_md(report)
        if args.out:
            path = Path(args.out).with_suffix(".md")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print(f"{wn} {path}", file=sys.stderr)
        else:
            print(text)
    if args.format in ("json", "all"):
        report_with_meta = dict(report)
        report_with_meta.setdefault("status", "ok")
        report_with_meta.setdefault("message", "generated" if lang == "en" else "已生成")
        report_with_meta["message"] = "generated" if lang == "en" else "已生成"
        text = json.dumps(report_with_meta, ensure_ascii=False, indent=1)
        if args.out:
            path = Path(args.out).with_suffix(".json")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print(f"{wn} {path}", file=sys.stderr)
        else:
            print(text)
    if args.format in ("csv", "all"):
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["构件", "图纸", "图框", "编号", "截面", "长度mm", "混凝土", "体积m3",
                    "体积状态", "等级状态"])
        w.writerows(csv_rows(report))
        if args.out:
            path = Path(args.out).with_suffix(".csv")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(buf.getvalue(), encoding="utf-8-sig")
            print(f"{wn} {path}", file=sys.stderr)
        else:
            sys.stdout.write(buf.getvalue())
    return 0


if __name__ == "__main__":
    sys.exit(main())
