#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cad_beam_objects.py - 从展开后的梁边界图层生成可复核的梁对象。

输入路径：
  cad_geometry.sh 图纸.dwg --scan 图纸.scan.json --detail 图纸.detail.json \
      --floor-label "二层梁平法施工图" -o 二层几何
  cad_beam_objects.sh --dxf 二层几何.dxf \
      --scan 图纸.scan.json --detail 图纸.detail.json \
      --floor-label "二层梁平法施工图" -o 二层梁对象

本脚本把梁平法图里的梁边界线（如 S-梁-虚线）按垂直距离配对成中心线候选，
再与图中集中标注位置绑定，输出每根梁的编号、截面、长度、体积和复核缺口。
长度是中心线合并粗长，尚未扣除支座和叠合板，不能替代模型净跨。
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
import math
import os
import re
import sys
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

import cad_geometry  # noqa: E402
import cad_interpret  # noqa: E402
import cad_quantity  # noqa: E402
import cad_scan  # noqa: E402


BEAM_HEAD_RE = re.compile(
    r"(WKL|XL|LL|JZL|JGL|TXL|KL|DL|TL|WL|ZHL|QL|L)\d{1,3}[a-f]?", re.I)
SEC_RE = re.compile(r"(\d{2,3})\s*[xX×]\s*(\d{2,3})")


def _round(value: Any, digits: int = 3) -> float:
    try:
        return round(float(value), digits)
    except (TypeError, ValueError):
        return 0.0


def load_data(scan: Path, detail: Optional[Path]) -> dict[str, Any]:
    data: dict[str, Any] = {}
    try:
        data.update(json.loads(scan.read_text(encoding="utf-8")))
    except Exception as exc:
        raise SystemExit(f"读取 --scan 失败：{exc}") from exc
    if detail and detail.exists():
        try:
            data.update(json.loads(detail.read_text(encoding="utf-8")))
        except Exception as exc:
            raise SystemExit(f"读取 --detail 失败：{exc}") from exc
    elif not data.get("text_records"):
        side = scan.with_name(scan.stem + ".detail.json")
        if side.exists():
            try:
                data.update(json.loads(side.read_text(encoding="utf-8")))
            except Exception:
                pass
    return data


def load_expanded_dxf(path: Path, bbox: list[float],
                      margin: float, layer_pattern: str) -> list[dict[str, Any]]:
    """读取 cad_geometry 写出的展开 DXF，只保留目标图框范围与匹配图层。"""
    from dev_dxf import readfile
    doc = readfile(str(path))
    msp = doc.modelspace()
    pat = re.compile(layer_pattern, re.I)
    x0, y0, x1, y1 = bbox
    out = []
    for e in msp:
        if e.dxftype() != "LINE":
            continue
        layer = str(e.dxf.layer or "")
        if layer == "__SHEET_BBOX" or not pat.search(layer):
            continue
        a = e.dxf.start
        b = e.dxf.end
        if (x0 - margin <= a.x <= x1 + margin and
                y0 - margin <= a.y <= y1 + margin and
                x0 - margin <= b.x <= x1 + margin and
                y0 - margin <= b.y <= y1 + margin):
            out.append({
                "layer": layer,
                "a": (float(a.x), float(a.y)),
                "b": (float(b.x), float(b.y)),
            })
    return out


def _point_segment_distance(px: float, py: float,
                            ax: float, ay: float,
                            bx: float, by: float) -> float:
    dx, dy = bx - ax, by - ay
    if abs(dx) + abs(dy) < 1e-9:
        return math.hypot(px - ax, py - ay)
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def _annotation_pattern(code: str) -> re.Pattern[str]:
    return re.compile(
        r"(?<![A-Z0-9])" + re.escape(str(code or "")) + r"(?![0-9A-Z])",
        re.I,
    )


def attach_annotation_text_positions(
        instances: list[dict[str, Any]],
        data: dict[str, Any],
        cluster_step_mm: float = 1500.0) -> dict[str, int]:
    """把文字簇锚点还原到编号文字的实际插入点，供引线绑定使用。

    cad_scan 的 CLUSTER 坐标是网格左下角，不是文字位置；直接拿它找引线时，
    相隔一个网格的多个集中标注会被错误合并。这里只按同图框、同编号文字选点。
    """
    records: list[dict[str, Any]] = []
    for rec in data.get("text_records") or []:
        try:
            x, y = float(rec.get("x")), float(rec.get("y"))
        except (TypeError, ValueError):
            continue
        text = cad_scan.clean_mtext(
            cad_scan.normalize(str(rec.get("text") or "")))
        if not text:
            continue
        records.append({
            "x": x,
            "y": y,
            "text": text,
            "sheet": rec.get("sheet"),
            "file": rec.get("file"),
        })

    stats = {"same-cell": 0, "nearest-sheet": 0, "missing": 0}
    step = max(float(cluster_step_mm), 1.0)
    for inst in instances:
        code = str(inst.get("code") or "")
        try:
            anchor_x = float(inst.get("x"))
            anchor_y = float(inst.get("y"))
        except (TypeError, ValueError):
            stats["missing"] += 1
            continue
        pattern = _annotation_pattern(code)
        candidates = [
            rec for rec in records
            if rec.get("sheet") == inst.get("sheet")
            and pattern.search(rec["text"])
        ]
        if not candidates:
            stats["missing"] += 1
            continue

        same_cell = [
            rec for rec in candidates
            if math.floor(rec["x"] / step) == math.floor(anchor_x / step)
            and math.floor(rec["y"] / step) == math.floor(anchor_y / step)
        ]
        pool = same_cell or candidates
        if same_cell:
            stats["same-cell"] += 1
        else:
            stats["nearest-sheet"] += 1

        def score(rec: dict[str, Any]) -> tuple[float, int, int, float]:
            distance = math.hypot(rec["x"] - anchor_x, rec["y"] - anchor_y)
            starts = 0 if pattern.match(rec["text"]) else 1
            has_section = 0 if SEC_RE.search(rec["text"]) else 1
            return (distance, starts, has_section, rec["y"])

        chosen = min(pool, key=score)
        inst["annotation_x"] = round(chosen["x"], 1)
        inst["annotation_y"] = round(chosen["y"], 1)
        inst["annotation_text"] = chosen["text"][:120]
        inst["annotation_source"] = (
            "cluster-cell" if same_cell else "nearest-sheet")
    return stats


def annotate_rows_with_leaders(
        rows: list[dict[str, Any]],
        leaders: list[dict[str, Any]],
        max_distance_mm: float = 800.0,
        group_tolerance_mm: float = 10.0) -> dict[str, list[str]]:
    """把梁标注绑定到集中标注引线，并返回同点编号别名。

    一条引线最多绑定一个实际文字位置；同一位置解析出的多个编号才视为别名，
    避免长引线穿过上下两个集中标注时把不同构件错误合并。
    """
    leader_codes: dict[str, list[str]] = defaultdict(list)
    ordered_leaders = sorted(
        leaders,
        key=lambda item: (
            min(float(item["a"][0]), float(item["b"][0])),
            min(float(item["a"][1]), float(item["b"][1])),
            max(float(item["a"][0]), float(item["b"][0])),
            max(float(item["a"][1]), float(item["b"][1])),
        ),
    )
    for idx, leader in enumerate(ordered_leaders, 1):
        leader["id"] = f"L{idx:04d}"

    groups: list[dict[str, Any]] = []
    for row in rows:
        try:
            x = float(row.get("annotation_x", row.get("x")))
            y = float(row.get("annotation_y", row.get("y")))
        except (TypeError, ValueError):
            row["leader_assignment_status"] = "no-annotation-position"
            continue
        group = next(
            (item for item in groups
             if math.hypot(item["x"] - x, item["y"] - y)
             <= group_tolerance_mm),
            None,
        )
        if group is None:
            group = {"x": x, "y": y, "rows": [], "candidates": []}
            groups.append(group)
        group["rows"].append(row)

    candidates: list[tuple[float, int, int]] = []
    for group_idx, group in enumerate(groups):
        for leader_idx, leader in enumerate(ordered_leaders):
            ax, ay = leader["a"]
            bx, by = leader["b"]
            distance = _point_segment_distance(
                group["x"], group["y"], ax, ay, bx, by)
            if distance <= max_distance_mm:
                group["candidates"].append((distance, leader_idx))
                candidates.append((distance, group_idx, leader_idx))

    used_groups: set[int] = set()
    used_leaders: set[int] = set()
    for distance, group_idx, leader_idx in sorted(
            candidates, key=lambda item: (item[0], item[1], item[2])):
        if group_idx in used_groups or leader_idx in used_leaders:
            continue
        group = groups[group_idx]
        leader = ordered_leaders[leader_idx]
        used_groups.add(group_idx)
        used_leaders.add(leader_idx)
        for row in group["rows"]:
            row["leader_id"] = leader["id"]
            row["leader_distance_mm"] = _round(distance, 1)
            row["leader_assignment_status"] = "leader-bound"
        for row in group["rows"]:
            code = _base_code(
                row.get("base_code") or row.get("code") or "")
            if code and code not in leader_codes[leader["id"]]:
                leader_codes[leader["id"]].append(code)

    for group_idx, group in enumerate(groups):
        if group_idx in used_groups:
            continue
        status = (
            "leader-conflict" if group["candidates"] else "no-leader")
        for row in group["rows"]:
            row["leader_assignment_status"] = status
    return dict(leader_codes)


def resolve_leader_targets(
        leaders: list[dict[str, Any]],
        candidates: list[dict[str, Any]],
        max_distance_mm: float = 300.0) -> dict[str, dict[str, Any]]:
    """把引线远离文字的一端解析成梁中心线目标。

    集中标注引线通常一端靠近编号文字、另一端落到梁中心线或轴线节点。保存
    目标点比继续使用文字簇网格锚点可靠，可避免 KL3/KL8 这类相邻标注串线。
    """
    targets: dict[str, dict[str, Any]] = {}
    for leader in leaders:
        leader_id = str(leader.get("id") or "")
        if not leader_id:
            continue
        matches: list[tuple[float, int, dict[str, Any]]] = []
        for endpoint_idx, endpoint in enumerate((leader["a"], leader["b"])):
            px, py = float(endpoint[0]), float(endpoint[1])
            for candidate in candidates:
                if candidate["orientation"] == "H":
                    ax = float(candidate["start"])
                    bx = float(candidate["end"])
                    ay = by = float(candidate["center"])
                else:
                    ay = float(candidate["start"])
                    by = float(candidate["end"])
                    ax = bx = float(candidate["center"])
                distance = _point_segment_distance(px, py, ax, ay, bx, by)
                if distance <= max_distance_mm:
                    matches.append((distance, endpoint_idx, candidate))
        if not matches:
            continue
        distance, endpoint_idx, candidate = min(
            matches,
            key=lambda item: (
                item[0],
                -float(item[2].get("length_mm") or
                       (float(item[2]["end"]) - float(item[2]["start"]))),
                item[1],
                float(item[2]["center"]),
            ),
        )
        endpoint = leader["a"] if endpoint_idx == 0 else leader["b"]
        targets[leader_id] = {
            "x": _round(endpoint[0], 1),
            "y": _round(endpoint[1], 1),
            "distance_mm": _round(distance, 1),
            "orientation": candidate["orientation"],
            "axis_mm": _round(candidate["center"], 1),
            "start_mm": _round(candidate["start"], 1),
            "end_mm": _round(candidate["end"], 1),
        }
    return targets


def _point_run_distance(
        x: float, y: float, run: dict[str, Any]) -> float:
    if run["orientation"] == "H":
        return _point_segment_distance(
            x, y,
            float(run["start_mm"]), float(run["axis_mm"]),
            float(run["end_mm"]), float(run["axis_mm"]))
    return _point_segment_distance(
        x, y,
        float(run["axis_mm"]), float(run["start_mm"]),
        float(run["axis_mm"]), float(run["end_mm"]))


def _norm_segments(
        segments: list[dict[str, Any]]
        ) -> list[tuple[str, float, float, float, str]]:
    rows = []
    for seg in segments:
        ax, ay = seg["a"]
        bx, by = seg["b"]
        dx, dy = bx - ax, by - ay
        if abs(dx) + abs(dy) < 1e-4:
            continue
        layer = str(seg.get("layer") or "")
        if abs(dy) <= abs(dx) * 0.02:
            rows.append(("H", ay, min(ax, bx), max(ax, bx), layer))
        elif abs(dx) <= abs(dy) * 0.02:
            rows.append(("V", ax, min(ay, by), max(ay, by), layer))
    return rows


def pair_beam_centerlines(
        segments: list[dict[str, Any]],
        known_widths: list[float],
        lateral_tol: float = 12.5,
        overlap_min: float = 300.0,
        max_width: float = 1200.0) -> tuple[list[dict[str, Any]], Counter]:
    """梁边界线配对成中心线候选。known_widths 来自本图截面 b 值。"""
    rows = _norm_segments(segments)
    groups: dict[tuple[str, int], list[tuple[float, float, float, str]]] = defaultdict(list)
    for kind, const, lo, hi, layer in rows:
        groups[(kind, int(round(const / lateral_tol)))].append((lo, hi, const, layer))

    def allowed(delta: float) -> bool:
        if not known_widths:
            return 100.0 <= delta <= max_width
        return any(abs(delta - w) <= lateral_tol for w in known_widths)

    out: list[dict[str, Any]] = []
    seen: set[tuple] = set()
    keys = sorted(groups)
    for i, key1 in enumerate(keys):
        for key2 in keys[i + 1:]:
            if key1[0] != key2[0]:
                continue
            delta = abs((key1[1] - key2[1]) * lateral_tol)
            if not allowed(delta):
                continue
            for s1 in groups[key1]:
                for s2 in groups[key2]:
                    lo = max(s1[0], s2[0])
                    hi = min(s1[1], s2[1])
                    if hi - lo < overlap_min:
                        continue
                    center = (s1[2] + s2[2]) / 2.0
                    key = (key1[0], round(center / 50.0),
                           round(lo / 100.0), round(hi / 100.0),
                           round(delta))
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append({
                        "orientation": key1[0],
                        "center": center,
                        "start": lo,
                        "end": hi,
                        "width_mm": delta,
                        "layers": sorted({s1[3], s2[3]} - {""}),
                    })
    counts = Counter(str(x.get("orientation")) + "-" + str(round(float(x.get("width_mm") or 0)))
                     for x in out)
    return out, counts


def _to_lines(centerlines: list[dict[str, Any]]) -> list[list[float]]:
    lines = []
    for c in centerlines:
        if c["orientation"] == "H":
            lines.append([c["start"], c["center"], c["end"], c["center"]])
        else:
            lines.append([c["center"], c["start"], c["center"], c["end"]])
    return lines


def axis_chain_details(lines: list[list[float]], x: float, y: float,
                       orientation: str,
                       join_gap_mm: float = 400.0,
                       max_perpendicular_mm: float = 1000.0,
                       max_annotation_distance_mm: float = 1200.0
                       ) -> Optional[dict[str, Any]]:
    """沿已判定方向寻找与标注位置相连的多跨中心线链。

    梁平法标注通常只靠近其中一跨，不能按“中心点距离 3.5m”截断整根梁。
    本函数按无限轴线、标注投影和相邻跨小间隙组装，支座宽度的正式扣减仍由
    结构模型完成。
    """
    if not lines:
        return None
    groups: dict[int, list[tuple[float, float, float]]] = defaultdict(list)
    for x1, y1, x2, y2 in lines:
        if orientation == "H" and abs(y2 - y1) <= 1.0:
            const = (y1 + y2) / 2.0
            groups[int(round(const / 20.0))].append(
                (const, min(x1, x2), max(x1, x2)))
        elif orientation == "V" and abs(x2 - x1) <= 1.0:
            const = (x1 + x2) / 2.0
            groups[int(round(const / 20.0))].append(
                (const, min(y1, y2), max(y1, y2)))

    annotation_axis = y if orientation == "H" else x
    annotation_along = x if orientation == "H" else y
    candidates: list[dict[str, Any]] = []
    for values in groups.values():
        const = sum(v[0] for v in values) / len(values)
        perpendicular = abs(const - annotation_axis)
        if perpendicular > max_perpendicular_mm:
            continue
        intervals = sorted((v[1], v[2]) for v in values)
        clusters: list[list[tuple[float, float]]] = []
        for lo, hi in intervals:
            if (not clusters
                    or lo - max(b for _a, b in clusters[-1]) > join_gap_mm):
                clusters.append([(lo, hi)])
            else:
                clusters[-1].append((lo, hi))
        for cluster in clusters:
            lo = min(a for a, _ in cluster)
            hi = max(b for _, b in cluster)
            distance = 0.0
            if annotation_along < lo:
                distance = lo - annotation_along
            elif annotation_along > hi:
                distance = annotation_along - hi
            if distance > max_annotation_distance_mm:
                continue
            length = hi - lo
            score = length - distance * 2.0 - perpendicular * 0.2
            candidates.append({
                "score": score,
                "axis_const": const,
                "start": lo,
                "end": hi,
                "length_mm": length,
                "annotation_distance_mm": distance,
                "axis_offset_mm": perpendicular,
                "component_count": len(cluster),
            })
    if not candidates:
        return None
    best = max(candidates, key=lambda row: (
        row["score"], row["length_mm"], -row["axis_offset_mm"]))
    if orientation == "H":
        start = (best["start"], best["axis_const"])
        end = (best["end"], best["axis_const"])
    else:
        start = (best["axis_const"], best["start"])
        end = (best["axis_const"], best["end"])
    return {
        "length_mm": round(float(best["length_mm"]), 1),
        "axis_angle_deg": 0.0 if orientation == "H" else 90.0,
        "start": [round(float(v), 1) for v in start],
        "end": [round(float(v), 1) for v in end],
        "orientation": orientation,
        "length_basis": "axis-chain",
        "axis_chain_components": best["component_count"],
        "axis_chain_gap_mm": join_gap_mm,
        "axis_offset_mm": round(float(best["axis_offset_mm"]), 1),
        "annotation_distance_mm": round(
            float(best["annotation_distance_mm"]), 1),
    }


def beam_run_details(lines: list[list[float]], x: float, y: float,
                     radius: float = 3500.0,
                     min_length: float = 500.0,
                     run_mode: str = "axis-chain",
                     chain_gap_mm: float = 400.0,
                     max_perpendicular_mm: float = 1000.0,
                     max_annotation_distance_mm: float = 1200.0,
                     expected_spans: Optional[int] = None,
                     ) -> Optional[dict[str, Any]]:
    """返回与现有 beam_run_length 同口径的中心线区间，供输出复核。"""
    if not lines or x is None or y is None:
        return None
    try:
        import numpy as np
        S = np.asarray(lines, dtype=float)
        if S.ndim != 2 or S.shape[1] < 4:
            return None
        mx = (S[:, 0] + S[:, 2]) / 2.0
        my = (S[:, 1] + S[:, 3]) / 2.0
        ang = np.degrees(np.arctan2(S[:, 3] - S[:, 1],
                                    S[:, 2] - S[:, 0])) % 180.0
        ln = np.hypot(S[:, 2] - S[:, 0], S[:, 3] - S[:, 1])
        near = np.nonzero((np.hypot(mx - x, my - y) <= radius) &
                          (ln > min_length))[0]
        if near.size == 0:
            return None
        base = near[int(np.argmax(ln[near]))]
        a0 = float(ang[base])
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
        merged = cad_interpret._interval_merge(intervals)
        best = max(merged, key=lambda z: z[1] - z[0])
        # best 是该标注对应的实际合并区间；不能用同一方向全部线段的 min/max，
        # 否则邻近同名梁会把端点和长度撑大。
        start = (x + ux * float(best[0]), y + uy * float(best[0]))
        end = (x + ux * float(best[1]), y + uy * float(best[1]))
        orientation = "H" if abs(uy) <= abs(ux) else "V"
        local = {
            "length_mm": round(float(best[1] - best[0]), 1),
            "axis_angle_deg": round(a0, 1),
            "start": [round(v, 1) for v in start],
            "end": [round(v, 1) for v in end],
            "orientation": orientation,
            "length_basis": "local",
        }
        if run_mode == "axis-chain" and (expected_spans is None or expected_spans > 1):
            chained = axis_chain_details(
                lines, x, y, orientation,
                join_gap_mm=chain_gap_mm,
                max_perpendicular_mm=max_perpendicular_mm,
                max_annotation_distance_mm=max_annotation_distance_mm,
            )
            if (chained
                    and float(chained["length_mm"]) > float(local["length_mm"]) + 1.0):
                return chained
        return local
    except Exception:
        return None


def beam_instances_for_label(data: dict[str, Any],
                             floor_label: str,
                             bbox: Optional[list[float]] = None
                             ) -> list[dict[str, Any]]:
    instances = cad_interpret.beam_instances(data)
    selected = [
        r for r in instances if r.get("sheet_label") == floor_label]
    if bbox:
        x0, y0, x1, y1 = (float(v) for v in bbox)
        selected = [
            row for row in selected
            if isinstance(row.get("x"), (int, float))
            and isinstance(row.get("y"), (int, float))
            and x0 <= float(row["x"]) <= x1
            and y0 <= float(row["y"]) <= y1
        ]
        if not selected:
            # cad_interpret 漏检该图名时 sheet_label 归不了属（实测 J-5 十个
            # 真图名只认出 7 个，251/407 个梁标注 label 为空）——图框互不
            # 重叠，按 bbox 直接选是安全的兜底。
            selected = [
                row for row in instances
                if isinstance(row.get("x"), (int, float))
                and isinstance(row.get("y"), (int, float))
                and x0 <= float(row["x"]) <= x1
                and y0 <= float(row["y"]) <= y1
            ]
    return selected


def section_by_instance(instances: list[dict[str, Any]]) -> dict[str, tuple[int, int]]:
    exact: dict[str, tuple[int, int]] = {}
    base: dict[str, tuple[int, int]] = {}
    for inst in instances:
        code = str(inst.get("code") or "")
        m = SEC_RE.search(str(inst.get("section") or inst.get("raw") or ""))
        if not m:
            continue
        sec = (int(m.group(1)), int(m.group(2)))
        exact.setdefault(code, sec)
        base.setdefault(_base_code(code), sec)
    merged = dict(exact)
    for code in set(list(exact) + list(base)):
        if code not in merged and _base_code(code) in base:
            merged[code] = base[_base_code(code)]
    return merged


def _base_code(code: str) -> str:
    return re.sub(r"\(\s*\d+\s*[AB]?\s*\)", "", str(code or "")).upper()


def beam_span_count(code: str) -> Optional[int]:
    match = re.search(r"\(\s*(\d+)\s*[AB]?\s*\)", str(code or ""), re.I)
    return int(match.group(1)) if match else None


def section_widths(instances: list[dict[str, Any]]) -> list[float]:
    widths: list[float] = []
    for inst in instances:
        m = SEC_RE.search(str(inst.get("section") or inst.get("raw") or ""))
        if m:
            widths.append(float(m.group(1)))
    return sorted(set(round(w) for w in widths))


def resolve_section(code: str, section_map: dict[str, tuple[int, int]]) -> tuple:
    sec = section_map.get(code)
    if sec:
        return sec, "same-floor"
    base = section_map.get(_base_code(code))
    if base:
        return base, "same-floor-base"
    return (None, None), "missing-section"


def floor_number_from_label(floor_label: str) -> Optional[int]:
    a, _b, kind = cad_quantity.floor_label_kind(floor_label)
    return a


def _merge_intervals(items: list[tuple[float, float]],
                     gap: float = 10.0) -> list[tuple[float, float]]:
    out: list[list[float]] = []
    for lo, hi in sorted(items):
        if not out or lo - out[-1][1] > gap:
            out.append([lo, hi])
        else:
            out[-1][1] = max(out[-1][1], hi)
    return [(round(a, 1), round(b, 1)) for a, b in out]


def _candidate_overlap_ratio(a: dict[str, Any],
                             b: dict[str, Any]) -> float:
    overlap = max(0.0, min(float(a["end"]), float(b["end"]))
                  - max(float(a["start"]), float(b["start"])))
    shorter = min(
        float(a["end"]) - float(a["start"]),
        float(b["end"]) - float(b["start"]),
    )
    return overlap / shorter if shorter > 0 else 0.0


def _dedupe_centerline_candidates(
        primary: list[dict[str, Any]],
        secondary: list[dict[str, Any]],
        center_tol_mm: float = 150.0,
        secondary_center_tol_mm: float = 450.0) -> list[dict[str, Any]]:
    """保留截面宽度明确的配对，只用通配配对补近旁未覆盖中心线。"""
    out = [dict(row) for row in primary]
    for candidate in secondary:
        duplicate = False
        for kept in out:
            if candidate["orientation"] != kept["orientation"]:
                continue
            if (abs(float(candidate["center"]) - float(kept["center"]))
                    > secondary_center_tol_mm):
                continue
            if _candidate_overlap_ratio(candidate, kept) >= 0.8:
                duplicate = True
                break
        if not duplicate:
            out.append(dict(candidate))
    return out


def _candidate_in_bbox(candidate: dict[str, Any],
                       bbox: list[float]) -> bool:
    if len(bbox) != 4:
        return True
    x0, y0, x1, y1 = [float(v) for v in bbox]
    lo, hi = float(candidate["start"]), float(candidate["end"])
    axis = float(candidate["center"])
    if candidate["orientation"] == "H":
        return x0 <= lo <= hi <= x1 and y0 <= axis <= y1
    return y0 <= lo <= hi <= y1 and x0 <= axis <= x1


def _detect_mirror_axes(runs: list[dict[str, Any]],
                        min_pairs: int = 3,
                        length_tol_mm: float = 20.0,
                        axis_tol_mm: float = 25.0,
                        cluster_tol_mm: float = 50.0
                        ) -> list[dict[str, Any]]:
    """从等长重复梁段投票估计竖向镜像轴，用于未标注重复区的截面传播。"""
    votes: list[float] = []
    for i, a in enumerate(runs):
        for b in runs[i + 1:]:
            if a["orientation"] != b["orientation"]:
                continue
            if abs(float(a["length_mm"]) - float(b["length_mm"])) > length_tol_mm:
                continue
            if a["orientation"] == "H":
                if abs(float(a["axis_mm"]) - float(b["axis_mm"])) > axis_tol_mm:
                    continue
                m1 = (float(a["start_mm"]) + float(b["end_mm"])) / 2.0
                m2 = (float(a["end_mm"]) + float(b["start_mm"])) / 2.0
                if abs(m1 - m2) > length_tol_mm:
                    continue
                mirror = (m1 + m2) / 2.0
            else:
                if (abs(float(a["start_mm"]) - float(b["start_mm"])) > length_tol_mm
                        or abs(float(a["end_mm"]) - float(b["end_mm"])) > length_tol_mm):
                    continue
                mirror = (float(a["axis_mm"]) + float(b["axis_mm"])) / 2.0
            votes.append(mirror)
    clusters: list[list[float]] = []
    for value in sorted(votes):
        if not clusters or value - clusters[-1][-1] > cluster_tol_mm:
            clusters.append([value])
        else:
            clusters[-1].append(value)
    return [
        {
            "axis_mm": _round(sum(values) / len(values), 1),
            "match_count": len(values),
        }
        for values in sorted(
            clusters,
            key=lambda rows: (-len(rows), sum(rows) / len(rows)))
        if len(values) >= min_pairs
    ]


def _axis_mirror_candidates(
        candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """把中心线候选转换为镜像轴投票所需的统一字段。"""
    out = []
    for candidate in candidates:
        lo = float(candidate["start"])
        hi = float(candidate["end"])
        out.append({
            "orientation": candidate["orientation"],
            "axis_mm": float(candidate["center"]),
            "start_mm": lo,
            "end_mm": hi,
            "length_mm": hi - lo,
        })
    return out


def build_beam_run_registry(
        primary_candidates: list[dict[str, Any]],
        secondary_candidates: list[dict[str, Any]],
        rows: list[dict[str, Any]],
        bbox: list[float],
        leader_codes: Optional[dict[str, list[str]]] = None,
        leader_targets: Optional[dict[str, dict[str, Any]]] = None,
        leader_target_max_distance_mm: float = 300.0,
        run_gap_mm: float = 400.0,
        axis_tolerance_mm: float = 75.0,
        label_perpendicular_mm: float = 2000.0,
        label_along_gap_mm: float = 3000.0,
        mirror_tolerance_mm: float = 100.0,
        mirror_span_tolerance_mm: float = 450.0,
        default_height_mm: float = 500.0) -> dict[str, Any]:
    """建立全图中心线拓扑库，并按标注、镜像和低置信默认截面分级计方量。

    该台账补的是“同一编号只标注一次、但平面重复出现”的梁段。它仍使用中心线
    粗长，不扣支座和节点，只用于从编号级粗算走向拓扑级粗算的差异定位。
    """
    axis_candidates = [
        row for row in _dedupe_centerline_candidates(
            primary_candidates,
            secondary_candidates)
        if _candidate_in_bbox(row, bbox)
    ]
    candidates = [
        row for row in _dedupe_centerline_candidates(
            primary_candidates,
            secondary_candidates,
            secondary_center_tol_mm=450.0)
        if _candidate_in_bbox(row, bbox)
    ]

    groups: list[dict[str, Any]] = []
    for candidate in sorted(
            candidates,
            key=lambda row: (row["orientation"], float(row["center"]),
                             float(row["start"]))):
        group = next(
            (item for item in groups
             if item["orientation"] == candidate["orientation"]
             and abs(float(item["axis"]) - float(candidate["center"]))
             <= axis_tolerance_mm),
            None,
        )
        if group is None:
            groups.append({
                "orientation": candidate["orientation"],
                "axis": float(candidate["center"]),
                "items": [candidate],
            })
        else:
            group["items"].append(candidate)
            group["axis"] = sum(
                float(item["center"]) for item in group["items"]
            ) / len(group["items"])

    runs: list[dict[str, Any]] = []
    for group in groups:
        intervals: list[list[float]] = []
        for lo, hi in sorted(
                (float(item["start"]), float(item["end"]))
                for item in group["items"]):
            if not intervals or lo - intervals[-1][1] > run_gap_mm:
                intervals.append([lo, hi])
            else:
                intervals[-1][1] = max(intervals[-1][1], hi)
        for lo, hi in intervals:
            if hi - lo < 100.0:
                continue
            widths = [float(item["width_mm"]) for item in group["items"]]
            runs.append({
                "id": f"R{len(runs) + 1:04d}",
                "type": "beam-run",
                "orientation": group["orientation"],
                "axis_mm": _round(group["axis"], 1),
                "start_mm": _round(lo, 1),
                "end_mm": _round(hi, 1),
                "length_mm": _round(hi - lo, 1),
                "paired_width_mm": _round(
                    sum(widths) / len(widths) if widths else 200.0, 1),
                "source_candidate_count": len(group["items"]),
                "leader_extent_candidate_count": 0,
                "section_b_mm": None,
                "section_h_mm": None,
                "section": "",
                "volume_m3": None,
                "section_status": "unresolved",
                "confidence": "unresolved",
                "matched_code": "",
                "competing_codes": [],
                "code_assignment_status": "unresolved",
                "matched_leader_id": "",
                "leader_ids": [],
                "leader_distances_mm": [],
                "leader_target_distance_mm": None,
                "annotation_codes": [],
                "mirror_axis_mm": None,
            })

    # 用可靠引线对应的集中标注区间，只补长该引线已经命中的拓扑段。
    # 不在建段前注入候选，避免两个相邻编号在同轴线上因短缺口被错误合并。
    for row in rows:
        target = (leader_targets or {}).get(
            str(row.get("leader_id") or ""))
        detail = row.get("detail") or {}
        orientation = detail.get("orientation")
        start, end = detail.get("start"), detail.get("end")
        if (not target or orientation != target.get("orientation")
                or not start or not end
                or not row.get("section_b_mm")):
            continue
        if orientation == "H":
            label_lo, label_hi = sorted(
                (float(start[0]), float(end[0])))
        else:
            label_lo, label_hi = sorted(
                (float(start[1]), float(end[1])))
        if label_hi - label_lo <= 100.0:
            continue
        candidates_for_extent = []
        for run in runs:
            if run["orientation"] != orientation:
                continue
            target_distance = _point_run_distance(
                float(target["x"]), float(target["y"]), run)
            overlap = max(
                0.0,
                min(float(run["end_mm"]), label_hi)
                - max(float(run["start_mm"]), label_lo),
            )
            if (target_distance > leader_target_max_distance_mm
                    and overlap <= 100.0):
                continue
            candidates_for_extent.append(
                (target_distance, -overlap, float(run["start_mm"]), run))
        if not candidates_for_extent:
            continue
        _distance, _negative_overlap, _start, run = min(
            candidates_for_extent, key=lambda item: item[:3])
        old_lo = float(run["start_mm"])
        old_hi = float(run["end_mm"])
        new_lo = min(old_lo, label_lo)
        new_hi = max(old_hi, label_hi)
        if new_lo == old_lo and new_hi == old_hi:
            continue
        run["start_mm"] = _round(new_lo, 1)
        run["end_mm"] = _round(new_hi, 1)
        run["length_mm"] = _round(new_hi - new_lo, 1)
        run["leader_extent_candidate_count"] += 1

    # 先用标注实际命中的中心线区间绑定截面。
    for run in runs:
        matches: list[tuple[int, float, float, float, dict[str, Any]]] = []
        for row in rows:
            leader_id = str(row.get("leader_id") or "")
            target = (leader_targets or {}).get(leader_id)
            if target:
                target_distance = _point_run_distance(
                    float(target["x"]), float(target["y"]), run)
                if (target["orientation"] == run["orientation"]
                        and target_distance <= leader_target_max_distance_mm
                        and row.get("section_b_mm")
                        and row.get("section_h_mm")):
                    matches.append((
                        3, 1.0, 0.0, -target_distance, row))
                # 有明确引线目标的编号不再回退到文字簇锚点，防止串到邻梁。
                continue
            detail = row.get("detail") or {}
            orientation = detail.get("orientation")
            start, end = detail.get("start"), detail.get("end")
            if (orientation != run["orientation"] or not start or not end
                    or not row.get("section_b_mm")
                    or not row.get("section_h_mm")):
                continue
            if orientation == "H":
                lo, hi = sorted((float(start[0]), float(end[0])))
                perpendicular = abs(float(run["axis_mm"]) - float(row.get("y") or 0))
            else:
                lo, hi = sorted((float(start[1]), float(end[1])))
                perpendicular = abs(float(run["axis_mm"]) - float(row.get("x") or 0))
            overlap = max(
                0.0,
                min(float(run["end_mm"]), hi) - max(float(run["start_mm"]), lo),
            )
            shorter = min(float(run["length_mm"]), hi - lo)
            ratio = overlap / shorter if shorter > 0 else 0.0
            if (overlap > 100.0 and ratio > 0.7
                    and perpendicular <= label_perpendicular_mm + 500.0):
                matches.append((1, ratio, overlap, -perpendicular, row))
        if matches:
            ordered = sorted(
                matches,
                key=lambda item: (item[0], item[1], item[2], item[3]),
                reverse=True)
            evidence, _ratio, _overlap, _negative_perpendicular, row = ordered[0]
            run["section_b_mm"] = row["section_b_mm"]
            run["section_h_mm"] = row["section_h_mm"]
            run["section"] = f"{row['section_b_mm']}x{row['section_h_mm']}"
            run["volume_m3"] = _round(
                float(run["length_mm"])
                * float(row["section_b_mm"])
                * float(row["section_h_mm"]) / 1e9,
                4,
            )
            run["section_status"] = "label-overlap"
            run["confidence"] = "high"
            run["matched_code"] = row.get("code") or ""
            run["code_assignment_status"] = (
                "leader-target" if evidence == 3 else "direct-label")
            run["matched_leader_id"] = str(row.get("leader_id") or "")
            target = (leader_targets or {}).get(
                str(row.get("leader_id") or ""))
            if target:
                run["leader_target_distance_mm"] = target.get("distance_mm")
            competing = []
            annotation_codes = []
            for candidate in ordered:
                candidate_row = candidate[4]
                candidate_code = str(candidate_row.get("code") or "")
                if candidate_code and candidate_code not in annotation_codes:
                    annotation_codes.append(candidate_code)
                leader_id = str(candidate_row.get("leader_id") or "")
                if leader_id and leader_id not in run["leader_ids"]:
                    run["leader_ids"].append(leader_id)
                    if candidate_row.get("leader_distance_mm") is not None:
                        run["leader_distances_mm"].append(
                            candidate_row.get("leader_distance_mm"))
            run["annotation_codes"] = annotation_codes
            top_evidence = ordered[0][0]
            top_ratio = ordered[0][1]
            top_perpendicular = -ordered[0][3]
            for other in ordered[1:]:
                other_evidence = other[0]
                other_ratio = other[1]
                other_perpendicular = -other[3]
                if top_evidence == 3 and other_evidence != 3:
                    continue
                if (top_evidence != 3
                        and (top_ratio - other_ratio > 0.15
                             or other_perpendicular
                             > top_perpendicular
                             + max(200.0, top_perpendicular * 0.5))):
                    continue
                other_code = str(other[4].get("code") or "")
                if (other_code and other_code != run["matched_code"]
                        and other_code not in competing):
                    competing.append(other_code)
            run["competing_codes"] = competing

    # 同图框内最近的带截面标注作为中置信候选。
    for run in runs:
        if run["section_h_mm"]:
            continue
        matches: list[tuple[float, dict[str, Any]]] = []
        for row in rows:
            if not row.get("section_b_mm") or not row.get("section_h_mm"):
                continue
            if run["orientation"] == "H":
                perpendicular = abs(
                    float(run["axis_mm"]) - float(row.get("y") or 0))
                along = float(row.get("x") or 0)
            else:
                perpendicular = abs(
                    float(run["axis_mm"]) - float(row.get("x") or 0))
                along = float(row.get("y") or 0)
            along_gap = 0.0
            if along < float(run["start_mm"]):
                along_gap = float(run["start_mm"]) - along
            elif along > float(run["end_mm"]):
                along_gap = along - float(run["end_mm"])
            if (perpendicular <= label_perpendicular_mm
                    and along_gap <= label_along_gap_mm):
                matches.append((perpendicular + along_gap * 0.15, row))
        if matches:
            _score, row = min(matches, key=lambda item: item[0])
            run["section_b_mm"] = row["section_b_mm"]
            run["section_h_mm"] = row["section_h_mm"]
            run["section"] = f"{row['section_b_mm']}x{row['section_h_mm']}"
            run["volume_m3"] = _round(
                float(run["length_mm"])
                * float(row["section_b_mm"])
                * float(row["section_h_mm"]) / 1e9,
                4,
            )
            run["section_status"] = "nearest-label"
            run["confidence"] = "medium"
            run["matched_code"] = row.get("code") or ""
            run["code_assignment_status"] = "nearest-label"

    mirror_axes = _detect_mirror_axes(
        _axis_mirror_candidates(axis_candidates))
    for _ in range(5):
        changed = 0
        for run in runs:
            if run["section_h_mm"]:
                continue
            candidates_for_mirror: list[tuple[float, float, dict[str, Any]]] = []
            for mirror in mirror_axes:
                axis = float(mirror["axis_mm"])
                for other in runs:
                    if other is run or not other["section_h_mm"]:
                        continue
                    if run["orientation"] != other["orientation"]:
                        continue
                    if run["orientation"] == "H":
                        reflected_axis = float(run["axis_mm"])
                        reflected_lo = 2.0 * axis - float(run["end_mm"])
                        reflected_hi = 2.0 * axis - float(run["start_mm"])
                    else:
                        reflected_axis = 2.0 * axis - float(run["axis_mm"])
                        reflected_lo = float(run["start_mm"])
                        reflected_hi = float(run["end_mm"])
                    axis_error = abs(
                        reflected_axis - float(other["axis_mm"]))
                    span_error = (
                        abs(reflected_lo - float(other["start_mm"]))
                        + abs(reflected_hi - float(other["end_mm"]))
                    )
                    error = axis_error + span_error
                    if (axis_error <= mirror_tolerance_mm
                            and span_error <= mirror_span_tolerance_mm):
                        candidates_for_mirror.append((error, axis, other))
            if candidates_for_mirror:
                _error, axis, other = min(
                    candidates_for_mirror, key=lambda item: item[0])
                run["section_b_mm"] = other["section_b_mm"]
                run["section_h_mm"] = other["section_h_mm"]
                run["section"] = other["section"]
                run["volume_m3"] = _round(
                    float(run["length_mm"])
                    * float(other["section_b_mm"])
                    * float(other["section_h_mm"]) / 1e9,
                    4,
                )
                run["section_status"] = "mirror-label"
                run["confidence"] = "medium"
                run["matched_code"] = other.get("matched_code") or ""
                run["code_assignment_status"] = "mirror-label"
                run["matched_leader_id"] = (
                    other.get("matched_leader_id") or "")
                run["mirror_axis_mm"] = _round(axis, 1)
                changed += 1
        if not changed:
            break

    for run in runs:
        if run["section_h_mm"]:
            continue
        width = float(run["paired_width_mm"])
        if width < 100.0 or width > 1200.0:
            width = 200.0
        run["section_b_mm"] = _round(width, 0)
        run["section_h_mm"] = default_height_mm
        run["section"] = f"{_round(width, 0):.0f}x{default_height_mm:.0f}"
        run["volume_m3"] = _round(
            float(run["length_mm"]) * width * default_height_mm / 1e9, 4)
        run["section_status"] = "assumed-default-section"
        run["confidence"] = "low"

    status_counts: dict[str, dict[str, Any]] = {}
    for status in (
            "label-overlap", "nearest-label", "mirror-label",
            "assumed-default-section"):
        selected = [run for run in runs if run["section_status"] == status]
        status_counts[status] = {
            "count": len(selected),
            "length_mm": _round(sum(float(run["length_mm"]) for run in selected), 1),
            "volume_m3": _round(
                sum(float(run["volume_m3"] or 0.0) for run in selected), 4),
        }

    code_groups: dict[str, dict[str, Any]] = {}
    for row in rows:
        code = _base_code(row.get("base_code") or row.get("code") or "")
        group = code_groups.setdefault(code or "__unassigned__", {
            "code": code or "",
            "annotation_count": 0,
            "annotation_length_mm": 0.0,
            "annotation_volume_m3": 0.0,
            "run_count": 0,
            "centerline_length_mm": 0.0,
            "estimated_volume_m3": 0.0,
            "ambiguous_run_count": 0,
            "source_counts": {},
            "run_ids": [],
            "alias_leader_ids": [],
            "leader_ids": [],
        })
        group["annotation_count"] += 1
        group["annotation_length_mm"] += float(row.get("length_mm") or 0.0)
        group["annotation_volume_m3"] += float(row.get("volume_m3") or 0.0)
        leader_id = str(row.get("leader_id") or "")
        if leader_id and leader_id not in group["leader_ids"]:
            group["leader_ids"].append(leader_id)
        if (leader_id
                and leader_id not in group["alias_leader_ids"]):
            group["alias_leader_ids"].append(leader_id)

    for run in runs:
        code = _base_code(run.get("matched_code") or "")
        group = code_groups.setdefault(code or "__unassigned__", {
            "code": code or "",
            "annotation_count": 0,
            "annotation_length_mm": 0.0,
            "annotation_volume_m3": 0.0,
            "run_count": 0,
            "centerline_length_mm": 0.0,
            "estimated_volume_m3": 0.0,
            "ambiguous_run_count": 0,
            "source_counts": {},
            "run_ids": [],
            "alias_leader_ids": [],
            "leader_ids": [],
        })
        group["run_count"] += 1
        group["centerline_length_mm"] += float(run.get("length_mm") or 0.0)
        group["estimated_volume_m3"] += float(run.get("volume_m3") or 0.0)
        if run.get("competing_codes"):
            group["ambiguous_run_count"] += 1
        source = str(run.get("section_status") or "unresolved")
        group["source_counts"][source] = (
            group["source_counts"].get(source, 0) + 1)
        group["run_ids"].append(run.get("id"))
        for leader_id in run.get("leader_ids") or []:
            if leader_id not in group["leader_ids"]:
                group["leader_ids"].append(leader_id)
        matched_leader_id = str(run.get("matched_leader_id") or "")
        if (matched_leader_id
                and matched_leader_id not in group["alias_leader_ids"]):
            group["alias_leader_ids"].append(matched_leader_id)
    for group in code_groups.values():
        group["annotation_length_mm"] = _round(
            group["annotation_length_mm"], 1)
        group["annotation_volume_m3"] = _round(
            group["annotation_volume_m3"], 4)
        group["centerline_length_mm"] = _round(
            group["centerline_length_mm"], 1)
        group["estimated_volume_m3"] = _round(
            group["estimated_volume_m3"], 4)
        aliases = set()
        for leader_id in group.get("alias_leader_ids") or []:
            for alias in (leader_codes or {}).get(leader_id) or []:
                if alias and alias != group["code"]:
                    aliases.add(alias)
        group["alias_of_codes"] = sorted(aliases)
        if group["annotation_count"] and group["run_count"]:
            group["coverage_status"] = "both"
        elif group["annotation_count"] and aliases:
            group["coverage_status"] = "leader-alias"
        elif group["annotation_count"]:
            group["coverage_status"] = "annotation-only"
        else:
            group["coverage_status"] = "topology-only"

    return {
        "schema": "cad-beam-run-registry/v0.3",
        "bbox": bbox,
        "parameters": {
            "run_gap_mm": run_gap_mm,
            "axis_tolerance_mm": axis_tolerance_mm,
            "label_perpendicular_mm": label_perpendicular_mm,
            "label_along_gap_mm": label_along_gap_mm,
            "mirror_tolerance_mm": mirror_tolerance_mm,
            "mirror_span_tolerance_mm": mirror_span_tolerance_mm,
            "default_height_mm": default_height_mm,
            "leader_target_max_distance_mm": leader_target_max_distance_mm,
        },
        "leader_codes": leader_codes or {},
        "leader_targets": leader_targets or {},
        "mirror_axes": mirror_axes,
        "quantities": {
            "run_count": len(runs),
            "centerline_length_mm": _round(
                sum(float(run["length_mm"]) for run in runs), 1),
            "estimated_volume_m3": _round(
                sum(float(run["volume_m3"] or 0.0) for run in runs), 4),
            "status_counts": status_counts,
        },
        "code_quantities": dict(sorted(code_groups.items())),
        "runs": runs,
        "status": "全图中心线拓扑粗算；含镜像/近邻截面传播和低置信默认截面，不扣支座",
    }


def support_intervals_at_line(
        dxf_path: Path, orientation: str, axis_value: float,
        transform: tuple[float, float] = (0.0, 0.0),
        layer_pattern: str = r"S-剪力墙|S-柱|S-剪力墙-边缘构件|砼墙",
        max_width: float = 1200.0) -> list[tuple[float, float]]:
    """沿梁中心线提取墙柱轮廓占用区间，用于支座节点提示。"""
    from dev_dxf import readfile
    pat = re.compile(layer_pattern, re.I)
    doc = readfile(dxf_path)
    hs: list[tuple[float, float, float]] = []
    vs: list[tuple[float, float, float]] = []
    for e in doc.modelspace():
        if e.dxftype() != "LINE" or not pat.search(str(e.dxf.layer or "")):
            continue
        a = e.dxf.start
        b = e.dxf.end
        ax, ay = a.x + transform[0], a.y + transform[1]
        bx, by = b.x + transform[0], b.y + transform[1]
        if abs(by - ay) <= abs(bx - ax) * 0.02:
            hs.append((min(ay, by), min(ax, bx), max(ax, bx)))
        elif abs(bx - ax) <= abs(by - ay) * 0.02:
            vs.append((min(ax, bx), min(ay, by), max(ay, by)))

    intervals: list[tuple[float, float]] = []
    if orientation == "H":
        # 竖向成对边：支座沿水平梁方向的宽度段。
        for i, a in enumerate(vs):
            for b in vs[i + 1:]:
                thickness = abs(a[0] - b[0])
                if thickness < 50 or thickness > max_width:
                    continue
                if max(a[1], b[1]) <= axis_value <= min(a[2], b[2]):
                    intervals.append((min(a[0], b[0]), max(a[0], b[0])))
        # 水平成对边：上下轮廓夹住水平梁中心线时的纵向区间。
        for i, a in enumerate(hs):
            for b in hs[i + 1:]:
                thickness = abs(a[0] - b[0])
                if thickness < 50 or thickness > max_width:
                    continue
                lo = max(a[1], b[1])
                hi = min(a[2], b[2])
                if hi - lo > 0 and min(a[0], b[0]) < axis_value < max(a[0], b[0]):
                    intervals.append((lo, hi))
    else:
        # 水平成对边：上下边形成竖向支座长度段。
        for i, a in enumerate(hs):
            for b in hs[i + 1:]:
                thickness = abs(a[0] - b[0])
                if thickness < 50 or thickness > max_width:
                    continue
                lo = max(a[1], b[1])
                hi = min(a[2], b[2])
                if lo <= axis_value <= hi:
                    intervals.append((min(a[0], b[0]), max(a[0], b[0])))
        # 竖向成对边：左右轮廓夹住竖向梁中心线时的纵向区间。
        for i, a in enumerate(vs):
            for b in vs[i + 1:]:
                thickness = abs(a[0] - b[0])
                if thickness < 50 or thickness > max_width:
                    continue
                if min(a[0], b[0]) < axis_value < max(a[0], b[0]) and \
                        max(a[1], b[1]) <= min(a[2], b[2]):
                    intervals.append((max(a[1], b[1]), min(a[2], b[2])))
    return _merge_intervals(intervals)


def write_dxf_objects(out_path: Path, rows: list[dict[str, Any]],
                      bbox: list[float]) -> None:
    from dev_dxf import new as new_dxf
    doc = new_dxf("R2010")
    msp = doc.modelspace()
    if "AUTO_BEAM_CENTER" not in doc.layers:
        doc.layers.add("AUTO_BEAM_CENTER", color=1)
    if "AUTO_BEAM_LABEL" not in doc.layers:
        doc.layers.add("AUTO_BEAM_LABEL", color=3)
    for row in rows:
        detail = row.get("detail")
        if not detail or row.get("volume_status") != "ok":
            continue
        start, end = detail.get("start"), detail.get("end")
        if not start or not end:
            continue
        msp.add_line(start, end, dxfattribs={"layer": "AUTO_BEAM_CENTER"})
        mid = ((start[0] + end[0]) / 2.0, (start[1] + end[1]) / 2.0)
        msp.add_text(str(row.get("code") or ""), height=180,
                     dxfattribs={"layer": "AUTO_BEAM_LABEL"}).set_placement(mid)
    doc.layers.add("__SHEET_BBOX", color=6)
    x0, y0, x1, y1 = bbox
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for i in range(4):
        msp.add_line(corners[i], corners[(i + 1) % 4],
                     dxfattribs={"layer": "__SHEET_BBOX"})
    doc.saveas(str(out_path))


def render_md(result: dict[str, Any]) -> str:
    o = ["# CAD 梁中心线对象复核", ""]
    o.append(f"- 图纸：{result.get('floor_label')}")
    o.append(f"- 图层：{result.get('beam_layer_pattern')}")
    o.append(f"- 边界线段：{result.get('beam_segments')}")
    o.append(f"- 中心线候选：{result.get('centerline_candidates')}")
    o.append(f"- 梁标注对象：{result.get('instance_count')}")
    o.append(f"- 有长度/截面对象：{result.get('resolved_count')}")
    o.append(f"- 自动梁体积：{result.get('total_beam_concrete_m3')} m3")
    registry = result.get("run_registry") or {}
    registry_quantities = registry.get("quantities") or {}
    if registry_quantities:
        o.append(
            f"- 全图中心线拓扑库：{registry_quantities.get('run_count')} 段，"
            f"{registry_quantities.get('estimated_volume_m3')} m3（粗算，含截面传播）"
        )
    if result.get("concrete_grade"):
        o.append(f"- 混凝土等级：{result.get('concrete_grade')}（层高表绑定）")
    if result.get("support_intervals"):
        o.append(f"- 支座轮廓区间：{len(result['support_intervals'])} 个（来自展开墙柱/柱图层）")
    o.append("")
    with_support = bool(result.get("support_intervals"))
    o.append("| 编号 | 截面 | 梁高mm | 长度mm | 体积m3 | 方向"
             + (" | 支座数" if with_support else "")
             + " | X | Y |")
    o.append("|---|---:|---:|---:|---:|:--:"
             + ("|---:" if with_support else "")
             + "|---:|---:|")
    for row in result.get("rows") or []:
        detail = row.get("detail") or {}
        direction = detail.get("orientation") or "-"
        support_cell = f"{row.get('support_count') or '-'} | " if with_support else ""
        o.append(f"| {row.get('code') or '-'} | {row.get('section') or '-'} | "
                 f"{row.get('section_h_mm') or '-'} | {row.get('length_mm') or '-'} | "
                 f"{row.get('volume_m3') or '-'} | {direction} | {support_cell}"
                 f"{round(row.get('x') or 0)} | {round(row.get('y') or 0)} |")
    o += [
        "",
        "## 口径与边界",
        "",
        "- 中心线来自展开后的梁边界图层，按本图截面宽度配对；长度是中心线合并粗长。",
    ]
    if result.get("support_intervals"):
        o.append("- 支座数是墙柱轮廓占用区间提示，仍未完成逐跨净跨和梁端节点扣减。")
    else:
        o.append("- 未接入支座轮廓时只输出中心线粗长，不能当作净跨。")
    o += [
        "- 板厚、叠合板和墙柱单层拆分仍需另行建模核对。",
        "- 自动结果用于人工复核和能力测试，不作为结算或翻样交付。",
        "",
    ]
    if registry_quantities:
        o += [
            "## 全图中心线拓扑库",
            "",
            "该表用于补出“同一编号只标注一次、平面重复出现”的梁段；长度仍为中心线粗长，"
            "截面按标注命中、镜像传播、近邻传播、默认截面四级标注。",
            "",
            "| 截面来源 | 段数 | 中心线长度mm | 粗方量m3 |",
            "|---|---:|---:|---:|",
        ]
        labels = {
            "label-overlap": "标注直接命中",
            "nearest-label": "近邻标注传播",
            "mirror-label": "镜像轴传播",
            "assumed-default-section": "默认截面",
        }
        for status, row in (registry_quantities.get("status_counts") or {}).items():
            o.append(
                f"| {labels.get(status, status)} | {row.get('count')} | "
                f"{row.get('length_mm')} | {row.get('volume_m3')} |")
        code_rows = list((registry.get("code_quantities") or {}).values())
        if code_rows:
            o += [
                "",
                "### 拓扑段按编号归属",
                "",
                "| 编号 | 标注数 | 拓扑段数 | 有竞争段 | 标注粗方量m3 | "
                "拓扑粗方量m3 | 覆盖状态 | 引线别名 | 截面来源 | 段号 |",
                "|:--|---:|---:|---:|---:|---:|:--|:--|:--|:--|",
            ]
            for row in code_rows:
                sources = "、".join(
                    f"{labels.get(key, key)}x{value}"
                    for key, value in sorted(
                        (row.get("source_counts") or {}).items())
                ) or "-"
                o.append(
                    f"| {row.get('code') or '未归属'} | "
                    f"{row.get('annotation_count')} | {row.get('run_count')} | "
                    f"{row.get('ambiguous_run_count') or 0} | "
                    f"{row.get('annotation_volume_m3')} | "
                    f"{row.get('estimated_volume_m3')} | "
                    f"{row.get('coverage_status') or '-'} | "
                    f"{'、'.join(row.get('alias_of_codes') or []) or '-'} | "
                    f"{sources} | "
                    f"{'、'.join(row.get('run_ids') or [])} |")
        o += [
            "",
            "| 段号 | 方向 | 轴线mm | 起点mm | 终点mm | 长度mm | 截面 | "
            "粗方量m3 | 截面来源 | 编号来源 | 匹配编号 | 竞争编号 | "
            "引线 | 标注距引线mm | 引线目标距mm | 镜像轴mm |",
            "|:--|:--:|---:|---:|---:|---:|---:|:--|:--|:--|:--|:--|---:|---:|---:|",
        ]
        for run in registry.get("runs") or []:
            o.append(
                f"| {run.get('id')} | {run.get('orientation')} | "
                f"{run.get('axis_mm')} | {run.get('start_mm')} | "
                f"{run.get('end_mm')} | {run.get('length_mm')} | "
                f"{run.get('section') or '-'} | {run.get('volume_m3') or 0:.4f} | "
                f"{labels.get(run.get('section_status'), run.get('section_status'))} | "
                f"{run.get('code_assignment_status') or '-'} | "
                f"{run.get('matched_code') or '-'} | "
                f"{'、'.join(run.get('competing_codes') or []) or '-'} | "
                f"{'、'.join(run.get('leader_ids') or []) or '-'} | "
                f"{'、'.join(str(v) for v in (run.get('leader_distances_mm') or [])) or '-'} | "
                f"{run.get('leader_target_distance_mm') if run.get('leader_target_distance_mm') is not None else '-'} | "
                f"{run.get('mirror_axis_mm') if run.get('mirror_axis_mm') is not None else '-'} |")
        o.append("")
    return "\n".join(o)


def csv_lines(result: dict[str, Any]) -> list[list[str]]:
    with_support = bool(result.get("support_intervals"))
    headers = [
        "编号", "基础编号", "截面", "梁高mm", "长度mm", "体积m3",
        "中心线方向", "角度",
    ]
    if with_support:
        headers.append("支座数")
    headers += ["X", "Y", "状态", "缺口"]
    headers += [
        "标注X", "标注Y", "标注来源", "引线", "引线距离mm", "引线绑定状态",
    ]
    out = [headers]
    for row in result.get("rows") or []:
        d = row.get("detail") or {}
        line = [
            row.get("code") or "", row.get("base_code") or "",
            row.get("section") or "", str(row.get("section_h_mm") or ""),
            str(row.get("length_mm") or ""), str(row.get("volume_m3") or ""),
            d.get("orientation") or "",
            "" if d.get("axis_angle_deg") is None else str(d.get("axis_angle_deg")),
        ]
        if with_support:
            line.append(str(row.get("support_count") or ""))
        line += [
            str(row.get("x") or ""), str(row.get("y") or ""),
            row.get("volume_status") or "", row.get("issue") or "",
            str(row.get("annotation_x") or ""),
            str(row.get("annotation_y") or ""),
            row.get("annotation_source") or "",
            row.get("leader_id") or "",
            str(row.get("leader_distance_mm") or ""),
            row.get("leader_assignment_status") or "",
        ]
        out.append(line)
    return out


def run_registry_csv_lines(registry: dict[str, Any]) -> list[list[str]]:
    headers = [
        "段号", "方向", "轴线mm", "起点mm", "终点mm", "长度mm",
        "配对宽度mm", "截面", "截面b_mm", "截面h_mm", "粗方量m3",
        "截面来源", "置信度", "编号来源", "匹配编号", "竞争编号",
        "引线", "标注距引线mm", "引线目标距mm", "镜像轴mm", "来源候选数",
    ]
    out = [headers]
    for row in registry.get("runs") or []:
        out.append([
            row.get("id") or "", row.get("orientation") or "",
            str(row.get("axis_mm") or ""), str(row.get("start_mm") or ""),
            str(row.get("end_mm") or ""), str(row.get("length_mm") or ""),
            str(row.get("paired_width_mm") or ""), row.get("section") or "",
            str(row.get("section_b_mm") or ""), str(row.get("section_h_mm") or ""),
            str(row.get("volume_m3") or ""), row.get("section_status") or "",
            row.get("confidence") or "",
            row.get("code_assignment_status") or "",
            row.get("matched_code") or "",
            "、".join(row.get("competing_codes") or []),
            "、".join(row.get("leader_ids") or []),
            "、".join(
                str(v) for v in (row.get("leader_distances_mm") or [])),
            "" if row.get("leader_target_distance_mm") is None
            else str(row.get("leader_target_distance_mm")),
            "" if row.get("mirror_axis_mm") is None else str(row.get("mirror_axis_mm")),
            str(row.get("source_candidate_count") or ""),
        ])
    return out


def run_registry_code_csv_lines(
        registry: dict[str, Any]) -> list[list[str]]:
    headers = [
        "编号", "标注数", "拓扑段数", "有竞争编号段",
        "标注粗方量m3", "拓扑中心线长度mm", "拓扑粗方量m3", "覆盖状态",
        "引线", "引线别名",
        "直接标注段", "近邻传播段", "镜像传播段", "默认截面段", "段号",
    ]
    out = [headers]
    for row in (registry.get("code_quantities") or {}).values():
        sources = row.get("source_counts") or {}
        out.append([
            row.get("code") or "",
            str(row.get("annotation_count") or 0),
            str(row.get("run_count") or ""),
            str(row.get("ambiguous_run_count") or 0),
            str(row.get("annotation_volume_m3") or ""),
            str(row.get("centerline_length_mm") or ""),
            str(row.get("estimated_volume_m3") or ""),
            row.get("coverage_status") or "",
            "、".join(row.get("leader_ids") or []),
            "、".join(row.get("alias_of_codes") or []),
            str(sources.get("label-overlap", 0)),
            str(sources.get("nearest-label", 0)),
            str(sources.get("mirror-label", 0)),
            str(sources.get("assumed-default-section", 0)),
            "、".join(row.get("run_ids") or []),
        ])
    return out


def leader_audit_csv_lines(
        rows: list[dict[str, Any]],
        leaders: list[dict[str, Any]],
        targets: dict[str, dict[str, Any]],
        leader_codes: dict[str, list[str]]) -> list[list[str]]:
    headers = [
        "引线", "起点X", "起点Y", "终点X", "终点Y", "绑定编号",
        "编号别名", "绑定标注数", "目标X", "目标Y", "目标方向",
        "目标轴线mm", "目标起mm", "目标终mm", "目标距mm",
    ]
    rows_by_leader: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        leader_id = str(row.get("leader_id") or "")
        if leader_id:
            rows_by_leader[leader_id].append(row)
    out = [headers]
    for leader in sorted(leaders, key=lambda item: str(item.get("id") or "")):
        leader_id = str(leader.get("id") or "")
        codes = leader_codes.get(leader_id) or []
        target = targets.get(leader_id) or {}
        out.append([
            leader_id,
            str(leader["a"][0]), str(leader["a"][1]),
            str(leader["b"][0]), str(leader["b"][1]),
            "、".join(codes),
            "、".join(codes[1:]) if len(codes) > 1 else "",
            str(len(rows_by_leader.get(leader_id) or [])),
            "" if target.get("x") is None else str(target.get("x")),
            "" if target.get("y") is None else str(target.get("y")),
            target.get("orientation") or "",
            "" if target.get("axis_mm") is None else str(target.get("axis_mm")),
            "" if target.get("start_mm") is None else str(target.get("start_mm")),
            "" if target.get("end_mm") is None else str(target.get("end_mm")),
            "" if target.get("distance_mm") is None
            else str(target.get("distance_mm")),
        ])
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="CAD 梁中心线对象生成与复核")
    ap.add_argument("--dxf", required=True, help="cad_geometry 输出的展开几何 DXF")
    ap.add_argument("--scan", required=True, help="cad_scan 的 JSON")
    ap.add_argument("--detail", default=None, help="cad_scan --detail-json")
    ap.add_argument("--bbox", default=None,
                    help="覆盖图框范围，格式 x0,y0,x1,y1")
    ap.add_argument("--floor-label", required=True,
                    help="如：二层梁平法施工图")
    ap.add_argument("--layer-pattern",
                    # 原为 "梁-虚线|梁-实线|BEAM"，只认连字符写法。实测同一批图纸
                    # 里既有 "梁-实线" 也有 "结_梁_实线"/"梁__虚线"（下划线），
                    # 硬编码连字符会让后者一条线都取不到、量直接为 0。
                    default=r"梁[-_]{1,2}(?:实线|虚线)|BEAM")
    ap.add_argument("--leader-layer-pattern",
                    default=r"S-梁-配筋-集中标注",
                    help="集中标注引线图层正则")
    ap.add_argument("--leader-max-distance-mm", type=float, default=800.0,
                    help="编号实际文字位置到引线的最大绑定距离")
    ap.add_argument("--leader-target-max-distance-mm", type=float, default=300.0,
                    help="引线端点落到梁中心线候选的最大距离")
    ap.add_argument("--leader-group-tolerance-mm", type=float, default=10.0,
                    help="同一位置多个编号文字合并为别名的最大距离")
    ap.add_argument("--annotation-cluster-mm", type=float, default=1500.0,
                    help="cad_scan --cluster 的网格尺寸，用于还原文字实际位置")
    ap.add_argument("--support-dxf", default=None,
                    help="墙柱平法展开 DXF；用于提取支座轮廓区间")
    ap.add_argument("--support-transform", default=None,
                    help="墙柱 DXF 到梁平法 DXF 的平移，格式 dx,dy")
    ap.add_argument("--run-mode", default="axis-chain",
                    choices=["axis-chain", "local"],
                    help="中心线长度口径；axis-chain 会连接同一轴线的多跨短间隙")
    ap.add_argument("--chain-gap-mm", type=float, default=400.0,
                    help="axis-chain 允许连接的最大跨间断长度")
    ap.add_argument("--chain-max-perp-mm", type=float, default=1000.0,
                    help="axis-chain 搜索轴线距标注的最大垂直距离")
    ap.add_argument("--chain-max-annotation-mm", type=float, default=1200.0,
                    help="axis-chain 标注投影距中心线链端部的最大距离")
    ap.add_argument("--run-registry", action=argparse.BooleanOptionalAction,
                    default=True,
                    help="输出全图中心线拓扑库，补出未重复标注的梁段")
    ap.add_argument("--run-registry-gap-mm", type=float, default=400.0,
                    help="拓扑库同一轴线连接短空隙的最大长度")
    ap.add_argument("--run-registry-axis-tol-mm", type=float, default=75.0,
                    help="拓扑库同一轴线聚类的横向容差")
    ap.add_argument("--run-registry-label-perp-mm", type=float, default=2000.0,
                    help="拓扑库从标注传播截面时的最大垂直距离")
    ap.add_argument("--run-registry-label-along-mm", type=float, default=3000.0,
                    help="拓扑库从标注传播截面时的最大沿轴距离")
    ap.add_argument("--run-registry-mirror-tol-mm", type=float, default=100.0,
                    help="镜像中心线区间匹配容差")
    ap.add_argument("--run-registry-mirror-span-tol-mm", type=float,
                    default=450.0,
                    help="镜像轴相同但端部因图线截断产生的长度容差")
    ap.add_argument("--run-registry-default-height-mm", type=float, default=500.0,
                    help="无法传播截面时使用的低置信默认梁高")
    ap.add_argument("--format", default="all", choices=["all", "json", "csv", "md"])
    ap.add_argument("-o", "--out", default="cad_beam_objects")
    args = ap.parse_args()

    scan_path = Path(args.scan)
    detail_path = Path(args.detail) if args.detail else None
    data = load_data(scan_path, detail_path)
    bbox = None
    if args.bbox:
        try:
            vals = [float(v) for v in str(args.bbox).split(",")]
            if len(vals) == 4:
                bbox = vals
        except ValueError:
            pass
    if not bbox:
        bbox = cad_geometry.find_sheet_bbox(
            scan_path, detail_path, args.floor_label)
    if not bbox:
        print(f"未找到图框：{args.floor_label}", file=sys.stderr)
        return 2

    instances = beam_instances_for_label(data, args.floor_label, bbox)
    if not instances:
        print(f"该图框未解析到梁标注：{args.floor_label}", file=sys.stderr)
        return 2
    section_map = section_by_instance(instances)
    known_widths = section_widths(instances)
    annotation_source_counts = attach_annotation_text_positions(
        instances, data, args.annotation_cluster_mm)

    segments = load_expanded_dxf(Path(args.dxf), bbox, 25000.0,
                                 args.layer_pattern)
    centerlines, width_counts = pair_beam_centerlines(
        segments, known_widths)
    lines = _to_lines(centerlines)
    generic_centerlines, generic_width_counts = pair_beam_centerlines(
        segments, [])

    rows = []
    total = 0.0
    ok = 0
    support_dxf = Path(args.support_dxf) if args.support_dxf else None
    support_transform = (0.0, 0.0)
    if args.support_transform:
        try:
            vals = [float(v) for v in str(args.support_transform).split(",")]
            if len(vals) == 2:
                support_transform = (vals[0], vals[1])
        except ValueError:
            pass
    support_intervals_all: list[tuple[float, float]] = []
    for inst in instances:
        code = str(inst.get("code") or "")
        section_raw = str(inst.get("section") or "")
        (b, h), sec_status = resolve_section(code, section_map)
        if b and h and not section_raw:
            section_raw = f"{b}x{h}"
        detail = beam_run_details(
            lines,
            inst.get("x"),
            inst.get("y"),
            run_mode=args.run_mode,
            chain_gap_mm=args.chain_gap_mm,
            max_perpendicular_mm=args.chain_max_perp_mm,
            max_annotation_distance_mm=args.chain_max_annotation_mm,
            expected_spans=beam_span_count(code),
        )
        length = float(detail["length_mm"]) if detail else None
        volume = 0.0
        issue = ""
        status = "ok"
        if not (b and h):
            status = "no-section"
            issue = "本图未找到可绑定截面"
        elif not length:
            status = "no-length"
            issue = "中心线未匹配到梁边界几何"
        else:
            volume = b * h * length / 1e9
            ok += 1
            total += volume
        support_count = 0
        support_intervals: list[list[float]] = []
        if detail and support_dxf and length:
            axis_value = detail["start"][1] if detail["orientation"] == "H" else detail["start"][0]
            intervals = support_intervals_at_line(
                support_dxf, detail["orientation"], axis_value, support_transform)
            if detail["orientation"] == "H":
                s0, s1 = sorted([detail["start"][0], detail["end"][0]])
            else:
                s0, s1 = sorted([detail["start"][1], detail["end"][1]])
            filtered = [iv for iv in intervals
                        if min(iv[1], s1) - max(iv[0], s0) > 0]
            support_count = len(filtered)
            support_intervals = [[round(v, 1) for v in iv] for iv in filtered]
            support_intervals_all.extend(filtered)
        rows.append({
            "code": code,
            "base_code": _base_code(code),
            "section": section_raw,
            "section_b_mm": b,
            "section_h_mm": h,
            "section_status": sec_status,
            "length_mm": round(length, 1) if length else None,
            "volume_m3": round(volume, 4) if volume else 0.0,
            "volume_status": status,
            "issue": issue,
            "x": inst.get("x"),
            "y": inst.get("y"),
            "annotation_x": inst.get("annotation_x"),
            "annotation_y": inst.get("annotation_y"),
            "annotation_source": inst.get("annotation_source"),
            "detail": detail,
            "support_count": support_count,
            "support_intervals": support_intervals,
        })

    floor_no = floor_number_from_label(args.floor_label)
    grade = ""
    grade_status = "not-used"
    try:
        story = cad_quantity.parse_story_rows(data)
        if floor_no is not None:
            grade, grade_status = cad_quantity.story_grade_for_floor(
                story, floor_no, "beam")
    except Exception:
        pass

    run_registry = None
    leader_segments = []
    leader_codes: dict[str, list[str]] = {}
    leader_targets: dict[str, dict[str, Any]] = {}
    if args.run_registry:
        leader_segments = load_expanded_dxf(
            Path(args.dxf), bbox, 25000.0, args.leader_layer_pattern)
        leader_codes = annotate_rows_with_leaders(
            rows,
            leader_segments,
            max_distance_mm=args.leader_max_distance_mm,
            group_tolerance_mm=args.leader_group_tolerance_mm,
        )
        leader_targets = resolve_leader_targets(
            leader_segments,
            _dedupe_centerline_candidates(
                centerlines, generic_centerlines,
                secondary_center_tol_mm=450.0),
            max_distance_mm=args.leader_target_max_distance_mm,
        )
        run_registry = build_beam_run_registry(
            centerlines,
            generic_centerlines,
            rows,
            bbox,
            leader_codes=leader_codes,
            leader_targets=leader_targets,
            leader_target_max_distance_mm=(
                args.leader_target_max_distance_mm),
            run_gap_mm=args.run_registry_gap_mm,
            axis_tolerance_mm=args.run_registry_axis_tol_mm,
            label_perpendicular_mm=args.run_registry_label_perp_mm,
            label_along_gap_mm=args.run_registry_label_along_mm,
            mirror_tolerance_mm=args.run_registry_mirror_tol_mm,
            mirror_span_tolerance_mm=args.run_registry_mirror_span_tol_mm,
            default_height_mm=args.run_registry_default_height_mm,
        )

    result = {
        "floor_label": args.floor_label,
        "bbox": bbox,
        "beam_layer_pattern": args.layer_pattern,
        "beam_segments": len(segments),
        "leader_segment_count": len(leader_segments),
        "leader_annotation_count": sum(
            1 for row in rows if row.get("leader_id")),
        "leader_alias_count": sum(
            max(0, len(codes) - 1) for codes in leader_codes.values()),
        "leader_target_count": len(leader_targets),
        "annotation_source_counts": annotation_source_counts,
        "centerline_candidates": len(centerlines),
        "centerline_width_counts": dict(width_counts),
        "generic_centerline_candidates": len(generic_centerlines),
        "generic_centerline_width_counts": dict(generic_width_counts),
        "instance_count": len(instances),
        "resolved_count": ok,
        "total_beam_concrete_m3": round(total, 3),
        "support_dxf": str(support_dxf) if support_dxf else None,
        "support_transform": list(support_transform),
        "support_intervals": _merge_intervals(support_intervals_all),
        "concrete_grade": grade,
        "grade_status": grade_status,
        "run_registry": run_registry,
        "rows": rows,
        "status": "梁中心线自动粗算并给出支座轮廓提示；未完成净跨/叠合板，需人工逐条复核",
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.format in ("md", "all"):
        out.with_suffix(".md").write_text(render_md(result), encoding="utf-8")
        print(f"已写出 {out.with_suffix('.md')}", file=sys.stderr)
    if args.format in ("json", "all"):
        out.with_suffix(".json").write_text(
            json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"已写出 {out.with_suffix('.json')}", file=sys.stderr)
    if args.format in ("csv", "all"):
        with out.with_suffix(".csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(csv_lines(result))
        print(f"已写出 {out.with_suffix('.csv')}", file=sys.stderr)
        if run_registry:
            runs_csv = out.with_name(out.name + ".runs.csv")
            with runs_csv.open(
                    "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(run_registry_csv_lines(run_registry))
            print(f"已写出 {runs_csv}", file=sys.stderr)
            codes_csv = out.with_name(out.name + ".codes.csv")
            with codes_csv.open(
                    "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(
                    run_registry_code_csv_lines(run_registry))
            print(f"已写出 {codes_csv}", file=sys.stderr)
            leaders_csv = out.with_name(out.name + ".leaders.csv")
            with leaders_csv.open(
                    "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(
                    leader_audit_csv_lines(
                        rows, leader_segments, leader_targets, leader_codes))
            print(f"已写出 {leaders_csv}", file=sys.stderr)
    if args.format in ("all", "json"):
        try:
            dxf_path = out.with_suffix(".objects.dxf")
            write_dxf_objects(dxf_path, rows, bbox)
            print(f"已写出 {dxf_path}", file=sys.stderr)
        except Exception as exc:
            print(f"中心线 DXF 写出失败：{exc}", file=sys.stderr)
        if run_registry:
            runs_json = out.with_name(out.name + ".runs.json")
            runs_json.write_text(
                json.dumps(run_registry, ensure_ascii=False, indent=1),
                encoding="utf-8",
            )
            print(f"已写出 {runs_json}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
