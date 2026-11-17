#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad_geometry_math.py - 纯几何数学与图框定位（无 DXF/DWG 解析）。

从 cad_geometry 拆出的可复用部分：矩阵、点面关系、图框 bbox、颜色/SVG 辅助。
不引入 DXF/DWG 解析库；cad_interpret 只在 find_sheet_bbox 调用时按需导入。
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Optional


def _cad_interpret():
    try:
        import cad_interpret  # noqa: F401
        return cad_interpret
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "缺 cad-file-reader 的 cad_interpret；请先安装底座（cad-file-reader >=0.41.0）"
        ) from exc


def _insert_matrix(row: tuple) -> tuple[float, float, float, float, float, float]:
    ix, iy, iz, sx, sy, sz, rot = [float(x) for x in row[1:8]]
    return (
        sx * math.cos(rot),
        -sy * math.sin(rot),
        sx * math.sin(rot),
        sy * math.cos(rot),
        ix,
        iy,
    )


def _compose(a: tuple, b: tuple) -> tuple:
    return (
        a[0] * b[0] + a[1] * b[2],
        a[0] * b[1] + a[1] * b[3],
        a[2] * b[0] + a[3] * b[2],
        a[2] * b[1] + a[3] * b[3],
        a[0] * b[4] + a[1] * b[5] + a[4],
        a[2] * b[4] + a[3] * b[5] + a[5],
    )


def _apply(pt: tuple, m: tuple) -> tuple:
    return (m[0] * pt[0] + m[1] * pt[1] + m[4],
            m[2] * pt[0] + m[3] * pt[1] + m[5])



def point_in_bbox(pt: tuple, bbox: list[float], margin: float) -> bool:
    x, y = pt
    return (bbox[0] - margin <= x <= bbox[2] + margin and
            bbox[1] - margin <= y <= bbox[3] + margin)


def point_in_polygon(pt: tuple, polygon: list) -> bool:
    """射线法判点在多边形内（凸凹皆可，边界按外处理）。"""
    x, y = float(pt[0]), float(pt[1])
    inside = False
    count = len(polygon)
    for index in range(count):
        x1, y1 = float(polygon[index][0]), float(polygon[index][1])
        x2, y2 = float(polygon[(index + 1) % count][0]), float(polygon[(index + 1) % count][1])
        if (y1 > y) != (y2 > y):
            ratio = (y - y1) / (y2 - y1)
            if x < x1 + ratio * (x2 - x1):
                inside = not inside
    return inside


def distance_to_polygon(pt: tuple, polygon: list) -> float:
    """点到多边形边线的最短距离；点在面域内返回 0。"""
    if point_in_polygon(pt, polygon):
        return 0.0
    x, y = float(pt[0]), float(pt[1])
    best = None
    count = len(polygon)
    for index in range(count):
        x1, y1 = float(polygon[index][0]), float(polygon[index][1])
        x2, y2 = float(polygon[(index + 1) % count][0]), float(polygon[(index + 1) % count][1])
        dx, dy = x2 - x1, y2 - y1
        norm = dx * dx + dy * dy
        ratio = 0.0 if norm <= 1e-12 else max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / norm))
        dist = math.hypot(x - (x1 + ratio * dx), y - (y1 + ratio * dy))
        if best is None or dist < best:
            best = dist
    return best if best is not None else 0.0


def _label_like(text: str, label: str) -> bool:
    """图名级命中：精确相等，或图名嵌在短文本里（带"结施-12："之类前缀）。
    反向子串（text 是图名的一段）会放进说明文字引用和标高数字，必须排除。"""
    text = text.strip()
    if not text:
        return False
    if text == label:
        return True
    return label in text and len(text) <= len(label) + 12


def _sibling_title_re(suffix: str):
    """兄弟图名形态：标高数字开头 + 短汉字 + 同一后缀结尾。
    例："55.000～66.600梁、板平法施工图"；排除"6.现浇板预留洞口…施工图"这类
    以序号开头的说明长句（数字后汉字超过 6 个）。汉字段 {0,6}：后缀本身
    以汉字开头（"梁、板平法施工图"），数字段后可以不再有额外汉字。"""
    return re.compile(
        r"^[-+±0-9.．～~]+\s*[\u4e00-\u9fff、]{0,6}" + re.escape(suffix) + r"$")


def _label_fallback_bbox(data: dict, floor_label: str) -> Optional[list[float]]:
    """cad_interpret 漏检图名时的兜底：text_records 里精确找图名文字推图框。

    为什么不能直接取「包含图名坐标的 sheet 框」：实测 J-5 的 meta.sheets 有一个
    90×400m 的巨框把整列 8 张梁板图吞了进去，两个不同图名会命中同一个框，
    导致两层算出同一片区域。改按真图规律推框：
      1. 目标图名常有多个副本（主图名 + 图内右下角副本 + 邻图引用），
         按 y 聚类取最大组——同图副本 y 相近，跨图至少差一个节距；
      2. 图名在图框底部（sheet13 实测距底 ~0.14 框高），同列相邻图名的
         y 间距＝图框节距（J-5 实测恒定 51000）；
      3. x 取包含命中的最小 sheet 框的 x（sheet 的 x 边界通常准，y 不准）。
    无 sheet 可用时 x 按节距宽推。 """
    texts = data.get("text_records") or []
    sheets = (data.get("meta") or {}).get("sheets") or []
    if not floor_label or not texts:
        return None
    hits: list[tuple[float, float]] = []
    for rec in texts:
        text = str(rec.get("text") or "").strip()
        if not _label_like(text, floor_label):
            continue
        x, y = rec.get("x"), rec.get("y")
        if x is None or y is None:
            continue
        hits.append((float(x), float(y)))
    if not hits:
        return None

    CLUSTER_GAP = 30000.0
    ys = sorted(y for _x, y in hits)
    groups: list[list[float]] = [[ys[0]]]
    for y in ys[1:]:
        (groups[-1].append(y) if y - groups[-1][-1] <= CLUSTER_GAP
         else groups.append([y]))
    main = max(groups, key=len)
    # 主图名：主组内最低 y 的命中（图名靠框底），以其 x 为列中心——
    # 同图右下角副本与邻图引用的 x 都离主图名较远，借此排除。
    y_hit, x_ref = min(((y, x) for x, y in hits
                        if min(main) - CLUSTER_GAP <= y <= max(main) + CLUSTER_GAP))

    # 节距：与目标图名同型的兄弟图名（同一构件段后缀，如"梁、板平法施工图"，
    # 借此区分梁板图与板图——两种图幅节距不同），同列的相邻 y 间距取最小值——
    # 副本间距 < CLUSTER_GAP 已滤，跨图最小间距就是节距；中位数会被
    # 「跳过目标自身」的双倍间距抬高。
    suffix_match = re.search(r"[\u4e00-\u9fff、]{2,}$", floor_label)
    suffix = suffix_match.group(0) if suffix_match else floor_label
    sib_rx = _sibling_title_re(suffix)
    sib = sorted(
        float(r["y"]) for r in texts
        if isinstance(r.get("x"), (int, float)) and isinstance(r.get("y"), (int, float))
        and abs(float(r["x"]) - x_ref) <= 20000.0
        and sib_rx.match(str(r.get("text") or "").strip())
        and str(r.get("text") or "").strip() != floor_label)
    pitch: Optional[float] = None
    if sib:
        gaps = [b - a for a, b in zip(sib, sib[1:]) if b - a > CLUSTER_GAP]
        if gaps:
            pitch = min(gaps)
    if not pitch:
        for sheet in sheets:
            bbox = sheet.get("bbox")
            if not bbox or len(bbox) != 4:
                continue
            bx0, by0, bx1, by1 = (float(v) for v in bbox)
            if any(bx0 <= x <= bx1 and by0 <= y <= by1 for x, y in hits):
                pitch = by1 - by0
                break
    if not pitch:
        return None

    y0 = y_hit - 0.15 * pitch
    y1 = y_hit + 0.85 * pitch
    main_hits = [(x, y) for x, y in hits
                 if min(main) - CLUSTER_GAP <= y <= max(main) + CLUSTER_GAP]
    best_sheet = None
    best_area = None
    for sheet in sheets:
        bbox = sheet.get("bbox")
        if not bbox or len(bbox) != 4:
            continue
        bx0, by0, bx1, by1 = (float(v) for v in bbox)
        if not any(bx0 <= x <= bx1 for x, _y in main_hits):
            continue
        area = (bx1 - bx0) * max(by1 - by0, 1.0)
        if best_area is None or area < best_area:
            best_sheet, best_area = (bx0, bx1), area
    if best_sheet:
        return [best_sheet[0], y0, best_sheet[1], y1]
    xs = [x for x, _y in main_hits]
    half = 0.9 * pitch / 2.0
    return [min(xs) - half, y0, max(xs) + half, y1]


def find_sheet_bbox(scan_json: Optional[Path], detail_json: Optional[Path],
                    floor_label: str) -> Optional[list[float]]:
    data = {}
    if scan_json:
        try:
            data.update(json.loads(scan_json.read_text(encoding="utf-8")))
        except Exception:
            pass
    if detail_json and detail_json.exists():
        try:
            data.update(json.loads(detail_json.read_text(encoding="utf-8")))
        except Exception:
            pass
    labels = _cad_interpret().detect_sheet_labels(data) if data.get("text_records") or data.get("keyword_rows") else {}
    target = None
    for sheet_id, label in labels.items():
        if floor_label in str(label) or str(label) in floor_label:
            target = str(sheet_id)
            break
    if target is None:
        return _label_fallback_bbox(data, floor_label or "")
    for sheet in (data.get("meta") or {}).get("sheets") or []:
        if str(sheet.get("id")) == target and sheet.get("bbox"):
            return [float(v) for v in sheet["bbox"]]
    return _label_fallback_bbox(data, floor_label or "")


def color_for_layer(layer: str) -> int:
    text = str(layer or "")
    if re.search(r"梁.*(实线|虚线)|梁-实线|梁-虚线|BEAM", text, re.I):
        return 1
    if re.search(r"板边线|板.*板边线|降板边线|S-SLAB", text, re.I):
        return 5
    if re.search(r"剪力墙|S-柱|COLU|WALL|砼墙", text, re.I):
        return 3
    return 7


def _svg_color(dxf_color: int) -> str:
    palette = {
        1: "#e23b3b",
        3: "#2d9c4a",
        5: "#3974e0",
        6: "#d84fc4",
        7: "#666666",
    }
    return palette.get(dxf_color, "#888888")


def _dxf_layer_name(layer: str) -> str:
    text = str(layer or "").strip()
    text = re.sub(r"[<>\\/:;?\"*|=,\x00-\x1f]", "_", text)
    text = re.sub(r"[^\w\s\u4e00-\u9fff\-()]+", "_", text)
    text = re.sub(r"\s+", " ", text).strip("._ ")
    if not text:
        text = "layer_0"
    return text[:250]


def _svg_escape(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&apos;"))


def write_svg(out_path: Path, bbox: list[float],
              segments: list[dict[str, Any]],
              layers: dict[int, str]) -> None:
    """把保留几何写成可浏览器直接打开的 SVG，供人工复核。"""
    x0, y0, x1, y1 = bbox
    width = 1600
    height = max(600, int(width * max(0.2, (y1 - y0) / max(1e-6, x1 - x0))))
    sx = width / max(1e-6, x1 - x0)
    sy = height / max(1e-6, y1 - y0)

    def to_xy(pt):
        px, py = pt
        return ((px - x0) * sx, height - (py - y0) * sy)

    body: list[str] = []
    for seg in segments:
        original_layer = str(layers.get(int(seg["handle"]), "0") or "0")
        stroke = _svg_color(color_for_layer(original_layer))
        try:
            xa, ya = to_xy(seg["a"])
            xb, yb = to_xy(seg["b"])
        except (TypeError, ValueError, KeyError):
            continue
        body.append(f'<line x1="{xa:.2f}" y1="{ya:.2f}" '
                    f'x2="{xb:.2f}" y2="{yb:.2f}" '
                    f'stroke="{stroke}" stroke-width="1.1" '
                    f'data-layer="{_svg_escape(_dxf_layer_name(original_layer))}"/>')

    defs = ["<style>svg{background:#fff}line{shape-rendering:geometricPrecision}</style>"]
    svg = "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        *defs,
        '<g transform="translate(0 0)">',
        *body,
        "</g>",
        f'<text x="18" y="{height - 18}" font-size="15" fill="#333">'
        f'CAD expanded geometry: {_svg_escape(str(x0))}, '
        f'{_svg_escape(str(y0))} - {_svg_escape(str(x1))}, '
        f'{_svg_escape(str(y1))}</text>',
        "</svg>",
    ])
    out_path.write_text(svg, encoding="utf-8")


