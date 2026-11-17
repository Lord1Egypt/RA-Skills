"""分阶段施工平面布置图：派生 DXF/PNG、图签与自检。

只读 base-map 与设施模型，输出到独立目录；模型空间 1:1、单位 mm。
final_check 恒 false，图签必带 DRAFT。

0.6.0 起出图内核补齐：
- 真 DIMENSION 实体（净距/道路/消防车道/塔吊半径/电梯距结构边）；
- 红线角点 + 主要设施定位点坐标表（CSV + 图内表格）；
- 指北针、比例尺、分区图例；
- 标注失败降级 manual，并在 selfcheck 中留原因。

0.6.1 起：
- 设施图块与 PNG 同一套图元（`symbols.SHAPES`），塔吊/施工电梯为可辨认类型示意；
- 文字标注统一走 `annotate.TextPlacer` 四级降级（直放/引线/换位/缩小/编号入图例），
  DXF 与 PNG 共用同一份排版结果，selfcheck 第 11 条复检“无文字重叠”。
"""
from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    import ezdxf  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise ImportError("缺少 ezdxf；请安装 ezdxf>=1.4 或设置 SITE_LAYOUT_VENDOR") from exc

from . import __version__
from .dimensions import (KIND_NAMES, applicable_kinds, build_coordinate_rows,
                         build_dimension_specs, select_table_rows, structure_edges)
from .draw import _pick_font, _png_safe, finalize_doc_extents
from .siteplan import SitePlanError, _bbox, _centroid
from .annotate import Box as TextBox
from .annotate import TextPlacer, summarize as layout_summary, text_width
from .symbols import (block_name, categories_in, draw_pictogram,
                      ensure_symbol_blocks, insert_symbol, symbol_size)
from .taxonomy import FACILITIES, STAGE_NAMES, meta

VERSION = __version__
SELFCHECK_SCHEMA = "site-stage-selfcheck/v1"
TITLE_SCHEMA = "site-stage-titleblock/v1"
DIMSTYLE = "SLP-DIM"
SCALE_BAR_MM = 20000.0


class StageDrawError(SitePlanError):
    exit_code = 5


def _layer_of(category: str) -> str:
    return meta(category)["layer"]


def _color_of(category: str) -> int:
    return int(meta(category)["color"])


def _base_layers(model: Dict[str, Any]) -> List[Tuple[str, int, str]]:
    layers: List[Tuple[str, int, str]] = [
        ("BASE-底图", 8, "Continuous"),
        ("BOUNDARY-红线", 1, "Continuous"),
        ("CRANE-塔吊", 1, "Continuous"),
        ("CRANE-覆盖", 5, "DASHED"),
        ("TEXT-标注", 7, "Continuous"),
        ("DIM-尺寸", 2, "Continuous"),
        ("COORD-坐标", 4, "Continuous"),
        ("META-图签", 7, "Continuous"),
        ("LEG-图例", 7, "Continuous"),
    ]
    seen = {name for name, _c, _l in layers}
    for row in model["facilities"]:
        name = _layer_of(row["category"])
        if name not in seen:
            layers.append((name, _color_of(row["category"]), "Continuous"))
            seen.add(name)
    return layers


def _create_doc(layers: Sequence[Tuple[str, int, str]]) -> Any:
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    doc.header["$INSUNITS"] = 4
    doc.header["$MEASUREMENT"] = 1
    if not doc.styles.has_entry("LAYOUT-TEXT"):
        doc.styles.add("LAYOUT-TEXT", font="simsun.ttc")
    for name, color, linetype in layers:
        if not doc.layers.has_entry(name):
            doc.layers.add(name, color=color, linetype=linetype)
    return doc


def _ensure_dimstyle(doc: Any, text_h: float) -> None:
    if doc.dimstyles.has_entry(DIMSTYLE):
        style = doc.dimstyles.get(DIMSTYLE)
    else:
        style = doc.dimstyles.add(DIMSTYLE)
    attrs = style.dxf
    attrs.dimtxt = max(text_h * 0.8, 80.0)
    attrs.dimasz = max(text_h * 0.35, 35.0)
    attrs.dimexe = max(text_h * 0.3, 30.0)
    attrs.dimexo = max(text_h * 0.25, 25.0)
    attrs.dimgap = max(text_h * 0.15, 15.0)
    attrs.dimtad = 1
    attrs.dimdec = 2
    attrs.dimlunit = 2
    attrs.dimtxsty = "LAYOUT-TEXT"
    attrs.dimclrd = 7
    attrs.dimclre = 7
    attrs.dimclrt = 7


def _add_text(msp: Any, text: str, x: float, y: float, height: float,
              layer: str = "TEXT-标注", color: int = 7) -> None:
    msp.add_text(text, height=height,
                 dxfattribs={"layer": layer, "color": color, "style": "LAYOUT-TEXT"}
                 ).set_placement((x, y))


def _site_window(model: Dict[str, Any], base_map: Dict[str, Any],
                 pad_mm: float = 50_000.0) -> Optional[Tuple[float, float, float, float]]:
    """红线外扩窗口：只用于底图线与出图范围，不改变设施/标注判定。"""
    ring = model.get("redline") or base_map.get("redline") or []
    pts: List[Tuple[float, float]] = []
    for point in ring:
        try:
            pts.append((float(point[0]), float(point[1])))
        except (TypeError, ValueError, IndexError):
            continue
    if not pts:
        ext = base_map.get("extents_mm")
        if isinstance(ext, (list, tuple)) and len(ext) >= 4:
            return (float(ext[0]) - pad_mm, float(ext[1]) - pad_mm,
                    float(ext[2]) + pad_mm, float(ext[3]) + pad_mm)
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs) - pad_mm, min(ys) - pad_mm, max(xs) + pad_mm, max(ys) + pad_mm)


def _segment_hits_box(gx0: float, gy0: float, gx1: float, gy1: float,
                      box: Tuple[float, float, float, float]) -> bool:
    """线段包围盒与矩形是否相交，用于丢弃窗口外/图框外底图线（含穿越情况）。"""
    return (min(gx0, gx1) <= box[2] and max(gx0, gx1) >= box[0]
            and min(gy0, gy1) <= box[3] and max(gy0, gy1) >= box[1])


def _clip_segment_to_box(gx0: float, gy0: float, gx1: float, gy1: float,
                         box: Tuple[float, float, float, float]
                         ) -> Optional[Tuple[float, float, float, float]]:
    """Liang-Barsky 裁剪：保留窗口内线段，返回 (x0,y0,x1,y1) 或 None。

    仅靠“线段包围盒碰窗口”会把跨越窗口的 1km 长线整根带进图框，既拉大
    出图范围又把红线压成一小块；这里真正裁剪到红线外扩窗口。
    """
    xmin, ymin, xmax, ymax = box
    dx, dy = gx1 - gx0, gy1 - gy0
    p = (-dx, dx, -dy, dy)
    q = (gx0 - xmin, xmax - gx0, gy0 - ymin, ymax - gy0)
    u1, u2 = 0.0, 1.0
    for pi, qi in zip(p, q):
        if abs(pi) <= 1e-12:
            if qi < 0.0:
                return None
            continue
        ratio = qi / pi
        if pi < 0.0:
            if ratio > u2:
                return None
            if ratio > u1:
                u1 = ratio
        else:
            if ratio < u1:
                return None
            if ratio < u2:
                u2 = ratio
    if u2 < u1:
        return None
    return (gx0 + u1 * dx, gy0 + u1 * dy, gx0 + u2 * dx, gy0 + u2 * dy)


def _content_frame(model: Dict[str, Any], base_map: Dict[str, Any]) -> Tuple[float, float, float, float]:
    points: List[Tuple[float, float]] = []
    window = _site_window(model, base_map)
    for row in base_map.get("site_geometry") or []:
        geom = row.get("geometry")
        if isinstance(geom, list) and len(geom) >= 4:
            gx0, gy0, gx1, gy1 = (float(geom[0]), float(geom[1]),
                                  float(geom[2]), float(geom[3]))
            if window:
                clipped = _clip_segment_to_box(gx0, gy0, gx1, gy1, window)
                if clipped is None:
                    continue
                gx0, gy0, gx1, gy1 = clipped
            points += [(gx0, gy0), (gx1, gy1)]
    for point in base_map.get("structure_outline") or []:
        try:
            x, y = float(point[0]), float(point[1])
        except (TypeError, ValueError, IndexError):
            continue
        if window and not (window[0] <= x <= window[2] and window[1] <= y <= window[3]):
            continue
        points.append((x, y))
    for row in model["facilities"]:
        points += [tuple(p) for p in row["geometry"]["points_mm"]]
    for crane in model["cranes"]:
        cx, cy = crane["center_mm"]
        r = crane.get("jib_mm") or 0.0
        if window:
            points += [(max(window[0], cx - r), max(window[1], cy - r)),
                       (min(window[2], cx + r), min(window[3], cy + r))]
        else:
            points += [(cx - r, cy - r), (cx + r, cy + r)]
    if not points:
        points = [(0.0, 0.0), (100000.0, 60000.0)]
    x0, y0, x1, y1 = _bbox(points)
    span = max(x1 - x0, y1 - y0, 1000.0)
    pad = max(span * 0.04, 2000.0)
    return x0 - pad, y0 - pad, x1 + pad, y1 + pad


# 兼容 0.5.0 内部命名
_frame_of = _content_frame


# ---------- 图例 ----------

def _draw_legend(msp: Any, model: Dict[str, Any], map_frame: Tuple[float, float, float, float],
                 legend_right: float, legend_w: float, text_h: float,
                 dim_count: int, coord_count: int,
                 layout_stats: Optional[Dict[str, Any]] = None) -> None:
    """右侧图例：设施（两列）/ 线型 / 标注 / 编号 / 说明。

    图例图标直接复用 DXF 的 SLP_* 图块，和主图、PNG 使用同一套图元；
    入图例编号来自 TextPlacer 的 index 降级项，避免“图上只有编号、图例无解释”。
    """
    _x0, y0, _x1, y1 = map_frame
    layout_stats = layout_stats or {}
    items = categories_in(model)
    line_rows = []
    seen = set()
    for row in model["facilities"]:
        if row["geometry"]["type"] != "line" or row["category"] in seen:
            continue
        seen.add(row["category"])
        line_rows.append(row)
    index_entries = list(layout_stats.get("index_entries") or [])
    notes = ("塔吊/施工电梯为类型示意",
             "臂长与导轨长度以参数为准",
             "图块非厂家尺寸",
             "坐标为场地局部坐标",
             "候选设施须逐项确认",
             "DRAFT 不替代审批")

    def estimate(h: float) -> float:
        per_col = max(1, math.ceil(len(items) / (2 if len(items) > 10 else 1)))
        return (2.6 + 2.0 + per_col * 2.1 + 0.6
                + 1.9 + (len(line_rows) + (1 if model.get("cranes") else 0)) * 1.7
                + 1.9 + 2 * 1.7 + 0.2
                + ((1.9 + len(index_entries) * 1.5 + 0.3) if index_entries else 0.0)
                + 1.8 + len(notes) * 1.45) * h

    available = max(0.0, (y1 - y0) - text_h * 1.0)
    local_h = text_h
    while local_h > text_h * 0.58 and estimate(local_h) > available:
        local_h *= 0.94

    left = legend_right - legend_w + local_h * 0.6
    right = legend_right - local_h * 0.6
    msp.add_lwpolyline([(legend_right - legend_w + local_h * 0.3, y0 + local_h * 0.4),
                        (legend_right - local_h * 0.3, y0 + local_h * 0.4),
                        (legend_right - local_h * 0.3, y1 - local_h * 0.4),
                        (legend_right - legend_w + local_h * 0.3, y1 - local_h * 0.4)],
                       close=True, dxfattribs={"layer": "LEG-图例", "color": 7})
    y = y1 - local_h * 1.9
    _add_text(msp, "图 例", left, y, local_h * 1.5, "LEG-图例")
    y -= local_h * 2.6

    _add_text(msp, "【设施】", left, y, local_h, "LEG-图例")
    y -= local_h * 2.0
    columns = 2 if len(items) > 10 else 1
    per_column = max(1, math.ceil(len(items) / columns))
    column_w = max(1.0, (right - left) / columns)
    pitch = local_h * 2.1
    top = y
    for index, item in enumerate(items):
        col = index // per_column
        row = index % per_column
        ix = left + col * column_w
        iy = top - row * pitch
        insert_symbol(msp, item["category"], ix + local_h * 1.15, iy + local_h * 0.2,
                      "LEG-图例", 7, size_mm=local_h * 2.25)
        _add_text(msp, "{} ×{}".format(item["name"], item["count"]),
                  ix + local_h * 2.95, iy - local_h * 0.25, local_h * 0.85, "LEG-图例")
    y = top - per_column * pitch - local_h * 0.6

    _add_text(msp, "【线 型】", left, y, local_h, "LEG-图例")
    y -= local_h * 1.9
    for row in line_rows:
        color = _color_of(row["category"])
        width = row.get("width_mm")
        label = row["category_name"] + (" {:.1f}m".format(width / 1000.0) if width else "")
        msp.add_line((left, y + local_h * 0.3), (left + local_h * 2.4, y + local_h * 0.3),
                     dxfattribs={"layer": "LEG-图例", "color": color})
        _add_text(msp, label, left + local_h * 2.8, y, local_h * 0.8, "LEG-图例")
        y -= local_h * 1.7
    if model.get("cranes"):
        msp.add_circle((left + local_h * 1.2, y + local_h * 0.3), local_h * 0.8,
                       dxfattribs={"layer": "LEG-图例", "color": 5, "linetype": "DASHED"})
        _add_text(msp, "塔吊回转覆盖（示意）", left + local_h * 2.8, y,
                  local_h * 0.8, "LEG-图例")
        y -= local_h * 1.7

    _add_text(msp, "【标 注】", left, y, local_h, "LEG-图例")
    y -= local_h * 1.9
    msp.add_line((left, y + local_h * 0.3), (left + local_h * 2.4, y + local_h * 0.3),
                 dxfattribs={"layer": "LEG-图例", "color": 2})
    _add_text(msp, "尺寸标注 {} 处".format(dim_count), left + local_h * 2.8, y,
              local_h * 0.8, "LEG-图例")
    y -= local_h * 1.7
    msp.add_lwpolyline([(left, y), (left + local_h * 1.4, y),
                        (left + local_h * 1.4, y + local_h * 0.8), (left, y + local_h * 0.8)],
                       close=True, dxfattribs={"layer": "LEG-图例", "color": 4})
    _add_text(msp, "坐标点 {} 个（见下方表）".format(coord_count), left + local_h * 2.8, y,
              local_h * 0.8, "LEG-图例")
    y -= local_h * 1.9

    if index_entries:
        _add_text(msp, "【入图例编号】", left, y, local_h, "LEG-图例")
        y -= local_h * 1.9
        for entry in index_entries:
            _add_text(msp, "{} = {}".format(entry.get("tag") or "?", entry.get("text") or ""),
                      left, y, local_h * 0.72, "LEG-图例")
            y -= local_h * 1.5
        y -= local_h * 0.3

    _add_text(msp, "【说 明】", left, y, local_h, "LEG-图例")
    y -= local_h * 1.8
    for note in notes:
        _add_text(msp, note, left, y, local_h * 0.7, "LEG-图例")
        y -= local_h * 1.45


def _draw_north_arrow(msp: Any, x: float, y: float, size: float) -> None:
    msp.add_circle((x, y), size, dxfattribs={"layer": "META-图签", "color": 7})
    msp.add_lwpolyline([(x, y + size * 0.9), (x - size * 0.32, y - size * 0.45),
                        (x + size * 0.32, y - size * 0.45), (x, y + size * 0.2)],
                       close=True, dxfattribs={"layer": "META-图签", "color": 7})
    _add_text(msp, "N", x - size * 0.18, y + size * 1.15, size * 0.75, "META-图签")
    _add_text(msp, "指北针（默认正北向上，须按总图核对）", x - size * 2.1,
              y - size * 1.55, size * 0.34, "META-图签")


def _draw_scale_bar(msp: Any, x: float, y: float, text_h: float) -> None:
    segment = SCALE_BAR_MM / 4.0
    bar_h = text_h * 0.55
    for index in range(4):
        x1 = x + index * segment
        x2 = x1 + segment
        dxf = {"layer": "META-图签", "color": 7 if index % 2 == 0 else 255}
        msp.add_lwpolyline([(x1, y), (x2, y), (x2, y + bar_h), (x1, y + bar_h)],
                           close=True, dxfattribs=dxf)
        if index % 2 == 0:
            msp.add_solid([(x1, y), (x2, y), (x2, y + bar_h), (x1, y + bar_h)],
                          dxfattribs={"layer": "META-图签", "color": 7})
    for label, offset in (("0", 0), ("10", 2), ("20m", 4)):
        _add_text(msp, label, x + offset * segment - text_h * 0.25, y - text_h * 0.9,
                  text_h * 0.55, "META-图签")
    _add_text(msp, "比例尺（模型 1:1，出图比例见图签）", x, y - text_h * 1.8,
              text_h * 0.55, "META-图签")


# ---------- 坐标表 ----------

def _column_widths(headers: Sequence[str], values: Sequence[Sequence[str]],
                   cell_h: float) -> List[float]:
    widths = []
    for index, header in enumerate(headers):
        need = max([text_width(header, cell_h)]
                   + [text_width(row[index], cell_h) for row in values] or [0.0])
        widths.append(need + cell_h * 0.8)
    return widths


def _draw_coordinate_table(msp: Any, rows: Sequence[Dict[str, Any]],
                           band: Tuple[float, float, float, float],
                           text_h: float,
                           total_rows: Optional[int] = None) -> Dict[str, Any]:
    """图内关键点坐标表：按列宽自适应，放不下就减点，绝不横向挤压。

    全量坐标在 coordinates-<stage>.csv；图内只保证“看得清”。
    """
    bx0, by0, bx1, by1 = band
    avail_w = max(1.0, bx1 - bx0)
    info: Dict[str, Any] = {"rows": 0, "total": int(total_rows or len(rows)),
                            "dropped": 0, "blocks": 0, "fits": True,
                            "block_width_mm": 0.0, "available_width_mm": round(avail_w, 1)}
    if not rows:
        _add_text(msp, "坐标表：无可用点（manual）", bx0 + text_h, by1 - text_h * 1.2,
                  text_h * 0.8, "COORD-坐标")
        return info
    cell_h = text_h * 0.62
    header_h = text_h * 1.4
    row_h = max(cell_h * 1.55, text_h * 0.95)
    per_block = max(1, int((by1 - by0 - header_h - text_h * 0.3) / row_h))

    def build(include_type: bool):
        heads = ("编号", "类型", "X(m)", "Y(m)") if include_type else ("编号", "X(m)", "Y(m)")
        vals = []
        for row in rows:
            base = [str(row["id"]), "{:.2f}".format(row["x_m"]), "{:.2f}".format(row["y_m"])]
            vals.append([base[0], row["type"], base[1], base[2]] if include_type else base)
        return heads, vals, _column_widths(heads, vals, cell_h)

    headers, values, col_w = build(True)
    if sum(col_w) > avail_w:
        headers, values, col_w = build(False)
    block_w = sum(col_w)
    max_blocks = max(1, int(avail_w // max(block_w, 1.0)))
    capacity = per_block * max_blocks
    shown = list(rows[:capacity])
    dropped = len(rows) - len(shown)
    values = values[:len(shown)]
    blocks = max(1, math.ceil(len(shown) / per_block))
    actual_block_w = avail_w / blocks
    fits = block_w <= actual_block_w + 1e-6

    for block in range(blocks):
        chunk_vals = values[block * per_block:(block + 1) * per_block]
        if not chunk_vals:
            continue
        left = bx0 + block * actual_block_w
        right = left + block_w
        msp.add_lwpolyline([(left, by1), (right, by1), (right, by0), (left, by0)],
                           close=True, dxfattribs={"layer": "COORD-坐标", "color": 4})
        cols = [left]
        for width in col_w[:-1]:
            cols.append(cols[-1] + width)
        for x in cols[1:]:
            msp.add_line((x, by0), (x, by1), dxfattribs={"layer": "COORD-坐标", "color": 4})
        msp.add_line((left, by1 - header_h), (right, by1 - header_h),
                     dxfattribs={"layer": "COORD-坐标", "color": 4})
        for col, header in enumerate(headers):
            _add_text(msp, header, cols[col] + cell_h * 0.35,
                      by1 - header_h + (header_h - cell_h) / 2.0, cell_h, "COORD-坐标")
        for index, row in enumerate(chunk_vals):
            top = by1 - header_h - (index + 1) * row_h
            msp.add_line((left, top), (right, top),
                         dxfattribs={"layer": "COORD-坐标", "color": 4})
            for col, value in enumerate(row):
                _add_text(msp, str(value), cols[col] + cell_h * 0.35,
                          top + (row_h - cell_h) / 2.0, cell_h, "COORD-坐标")
    caption = ("关键点坐标表（m，场地局部坐标；全量 {} 点见 CSV；"
               "须与项目测量控制点联测复核）").format(info["total"])
    if dropped:
        caption = ("关键点坐标表（m；图内 {} 点，另 {} 点见 CSV；"
                   "须与项目测量控制点联测复核）").format(len(shown), dropped)
    _add_text(msp, caption, bx0, by1 + text_h * 0.4, text_h * 0.55, "COORD-坐标")
    info.update({"rows": len(shown), "dropped": dropped, "blocks": blocks,
                 "per_block": per_block, "block_width_mm": round(block_w, 1),
                 "fits": fits})
    return info


def _mark_coordinates(msp: Any, rows: Sequence[Dict[str, Any]], text_h: float) -> None:
    for row in rows:
        x = row["x_m"] * 1000.0
        y = row["y_m"] * 1000.0
        size = text_h * 0.55
        msp.add_line((x - size, y), (x + size, y), dxfattribs={"layer": "COORD-坐标", "color": 4})
        msp.add_line((x, y - size), (x, y + size), dxfattribs={"layer": "COORD-坐标", "color": 4})
        _add_text(msp, row["id"], x + size * 1.2, y + size * 0.6,
                  text_h * 0.5, "COORD-坐标", 4)


# ---------- 主绘制 ----------

def _render_dimensions(msp: Any, dim_specs: Sequence[Dict[str, Any]]
                       ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """逐条渲染真 DIMENSION；失败项必须留痕，不能静默跳过。"""
    rendered: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []
    for spec in dim_specs:
        try:
            dimension = msp.add_aligned_dim(
                p1=(float(spec["p1"][0]), float(spec["p1"][1])),
                p2=(float(spec["p2"][0]), float(spec["p2"][1])),
                distance=float(spec["offset"]),
                dimstyle=DIMSTYLE,
                text=str(spec["text"]),
                dxfattribs={"layer": "DIM-尺寸", "color": 2},
            )
            dimension.render()
            rendered.append(spec)
        except Exception as exc:
            failures.append({
                "kind": str(spec.get("kind") or "unknown"),
                "text": str(spec.get("text") or ""),
                "refs": list(spec.get("refs") or []),
                "reason": "{}: {}".format(type(exc).__name__, exc),
            })
    return rendered, failures


def _facility_label(row: Dict[str, Any]) -> str:
    """图面短标签：优先设施名，过长时退回类型名；道路补宽度。"""
    category_name = str(row.get("category_name") or "")
    name = str(row.get("name") or "")
    label = category_name
    if name and name != category_name and len(name) <= 10:
        label = name
    if row["geometry"]["type"] == "line":
        label = category_name
    width = row.get("width_mm")
    if width:
        label += " {:.1f}m".format(float(width) / 1000.0)
    return label


def _symbol_render_size(category: str, text_h: float, kind: str,
                        span: Optional[float] = None,
                        span_y: Optional[float] = None) -> float:
    """图块在图面上的类型示意尺寸，不冒充厂家真实尺寸。"""
    base = symbol_size(category)
    if category == "tower_crane":
        # 类型示意可放大，不冒充 12m 真机尺寸；图签/图例注明“不按比例”。
        return min(max(base, text_h * 5.0), 22000.0)
    if category == "construction_elevator":
        # 电梯本体只有 2~4m 宽，按真实跨度画在图上是几个像素；放大到可辨认。
        return min(max(base, text_h * 1.8), 12000.0)
    if category == "weighbridge":
        # 地磅图块本身 1.4:0.54 的长宽比与占位区一致，按长边套入占位区
        length = max(1000.0, float(span or base))
        width = max(1000.0, float(span_y or base))
        return max(3000.0, min(length / 1.4, width / 0.54))
    if kind == "area":
        limit = max(1200.0, float(span or base) * 0.52)
        return max(min(base, limit), min(text_h * 2.8, limit))
    if kind == "line":
        return max(text_h * 2.1, base * 0.70)
    return max(text_h * 1.45, base * 0.85)


def _center_of(row: Dict[str, Any]) -> Tuple[float, float]:
    point = _centroid(row)
    if point:
        return float(point[0]), float(point[1])
    first = row["geometry"]["points_mm"][0]
    return float(first[0]), float(first[1])


def _longest_edge(points: Sequence[Sequence[float]]) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    best = ((-1.0, -1.0), (-1.0, -1.0))
    best_len = -1.0
    for index in range(len(points) - 1):
        a = (float(points[index][0]), float(points[index][1]))
        b = (float(points[index + 1][0]), float(points[index + 1][1]))
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        if length > best_len:
            best_len, best = length, (a, b)
    return best


def _notice_panel_ticks(points: Sequence[Sequence[float]], count: int = 9
                        ) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """九牌一图长条区域按 count 块等分，返回每块之间的短分隔线（模型坐标）。"""
    pts = [(float(p[0]), float(p[1])) for p in points]
    if len(pts) < 3 or count < 2:
        return []
    edges = [(math.hypot(pts[(i + 1) % len(pts)][0] - pts[i][0],
                                pts[(i + 1) % len(pts)][1] - pts[i][1]), i)
                 for i in range(len(pts))]
    length, index = max(edges)
    if length <= 1e-9:
        return []
    a, b = pts[index], pts[(index + 1) % len(pts)]
    ux, uy = (b[0] - a[0]) / length, (b[1] - a[1]) / length
    # 深度方向：取长边两端各自的对边中点差，保证指向矩形内部
    c = pts[(index + 2) % len(pts)]
    vx, vy = c[0] - b[0], c[1] - b[1]
    depth = math.hypot(vx, vy)
    if depth <= 1e-9:
        return []
    vx, vy = vx / depth, vy / depth
    ticks = []
    for i in range(1, count):
        t = length * i / float(count)
        base = (a[0] + ux * t, a[1] + uy * t)
        ticks.append((base, (base[0] + vx * depth, base[1] + vy * depth)))
    return ticks


def _symbol_box(cx: float, cy: float, size: float) -> TextBox:
    return TextBox(cx - size / 2.0, cy - size / 2.0,
                   cx + size / 2.0, cy + size / 2.0)


def _polygon_box(points: Sequence[Sequence[float]]) -> TextBox:
    return TextBox(min(float(p[0]) for p in points), min(float(p[1]) for p in points),
                   max(float(p[0]) for p in points), max(float(p[1]) for p in points))


def _dimension_obstacle(spec: Dict[str, Any], text_h: float) -> Tuple[TextBox, Tuple[Tuple[float, float], Tuple[float, float]]]:
    p1 = (float(spec["p1"][0]), float(spec["p1"][1]))
    p2 = (float(spec["p2"][0]), float(spec["p2"][1]))
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    length = max(math.hypot(dx, dy), 1e-9)
    nx, ny = -dy / length, dx / length
    offset = float(spec.get("offset") or 0.0)
    a = (p1[0] + nx * offset, p1[1] + ny * offset)
    b = (p2[0] + nx * offset, p2[1] + ny * offset)
    text = str(spec.get("text") or "")
    width = text_width(text, text_h * 0.78)
    cx, cy = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
    return (TextBox(cx - width / 2.0, cy - text_h * 0.85,
                    cx + width / 2.0, cy + text_h * 0.55), (a, b))


def _add_placement_text(msp: Any, placement: Any) -> bool:
    if placement.level == "unplaced":
        return False
    _add_text(msp, placement.text, placement.box.x0, placement.box.y0,
              placement.height, placement.layer, placement.color)
    if placement.leader:
        msp.add_line(placement.leader[0], placement.leader[1],
                     dxfattribs={"layer": placement.layer, "color": placement.color})
    return True


def _draw_stage(doc: Any, model: Dict[str, Any], base_map: Dict[str, Any],
                map_frame: Tuple[float, float, float, float],
                sheet: Tuple[float, float, float, float],
                table_band: Tuple[float, float, float, float],
                title: Dict[str, Any], draft_label: str, legend_w: float,
                dim_specs: Sequence[Dict[str, Any]], coord_rows: Sequence[Dict[str, Any]],
                text_h: float) -> Dict[str, Any]:
    msp = doc.modelspace()
    drawn = {"base": 0, "facility": 0, "text": 0, "crane": 0, "symbol": 0,
             "dimension": 0, "dimension_kinds": [], "dimension_failures": [],
             "coordinate_rows": 0, "north_arrow": 0, "scale_bar": 0,
             "placements": [], "symbols": [], "text_layout": {}}
    x0, y0, x1, y1 = map_frame
    _ensure_dimstyle(doc, text_h)

    placer = TextPlacer(TextBox(x0 + text_h * 0.9, y0 + text_h * 0.9,
                                x1 - text_h * 0.9, y1 - text_h * 0.9))
    # 固定图面元素先占位，设施标签不得压指北针或比例尺。
    placer.add_footprint(TextBox(x0 + text_h * 0.4, y1 - text_h * 5.0,
                                 x0 + text_h * 5.4, y1 - text_h * 0.4), "north-arrow")
    placer.add_footprint(TextBox(x0 + text_h * 0.4, y0 + text_h * 0.2,
                                 x0 + text_h * 16.0, y0 + text_h * 4.7), "scale-bar")

    base_window = _site_window(model, base_map)
    for index, row in enumerate(base_map.get("site_geometry") or []):
        geom = row.get("geometry")
        if not isinstance(geom, list) or len(geom) < 4:
            continue
        gx0, gy0, gx1, gy1 = (float(geom[0]), float(geom[1]), float(geom[2]), float(geom[3]))
        if base_window:
            clipped = _clip_segment_to_box(gx0, gy0, gx1, gy1, base_window)
            if clipped is None:
                continue  # 原点详图/其他图幅，不进本图
            gx0, gy0, gx1, gy1 = clipped
        p1 = (gx0, gy0)
        p2 = (gx1, gy1)
        msp.add_line(p1, p2, dxfattribs={"layer": "BASE-底图", "color": 8})
        placer.add_segment(p1, p2, "base:{}".format(index))
        drawn["base"] += 1

    outline = base_map.get("structure_outline") or []
    if isinstance(outline, list) and len(outline) >= 3:
        pts = [(float(p[0]), float(p[1])) for p in outline]
        msp.add_lwpolyline(pts, close=True,
                           dxfattribs={"layer": "BASE-底图", "color": 8, "linetype": "DASHED"})
        for index in range(len(pts)):
            placer.add_segment(pts[index], pts[(index + 1) % len(pts)],
                               "structure:{}".format(index))
        drawn["base"] += 1

    redline = model.get("redline") or []
    if len(redline) >= 2:
        pts = [(float(p[0]), float(p[1])) for p in redline]
        msp.add_lwpolyline(pts, close=bool(model.get("redline_closed")),
                           dxfattribs={"layer": "BOUNDARY-红线", "color": 1})
        for index in range(len(pts) - 1):
            placer.add_segment(pts[index], pts[index + 1], "redline:{}".format(index))
        if model.get("redline_closed"):
            placer.add_segment(pts[-1], pts[0], "redline:close")
        drawn["base"] += 1

    # 真 DIMENSION 实体：不炸开，保留可编辑的标注；失败项进入 selfcheck。
    rendered_specs, dimension_failures = _render_dimensions(msp, dim_specs)
    drawn["dimension"] = len(rendered_specs)
    drawn["dimension_kinds"] = sorted({str(spec["kind"]) for spec in rendered_specs})
    drawn["dimension_failures"] = dimension_failures
    for spec in rendered_specs:
        obstacle, segment = _dimension_obstacle(spec, text_h)
        placer.add_footprint(obstacle, "dim:{}".format(spec["kind"]))
        placer.add_segment(segment[0], segment[1], "dim:{}".format(spec["kind"]))

    crane_labels: List[Tuple[str, Tuple[float, float], str, int]] = []
    for index, crane in enumerate(model["cranes"]):
        cx, cy = (float(crane["center_mm"][0]), float(crane["center_mm"][1]))
        r = crane.get("jib_mm")
        if r:
            msp.add_circle((cx, cy), float(r),
                           dxfattribs={"layer": "CRANE-覆盖", "color": 5, "linetype": "DASHED"})
        size = _symbol_render_size("tower_crane", text_h, "point")
        rotation = float(crane.get("rotation_deg") or 0.0)
        if insert_symbol(msp, "tower_crane", cx, cy, "CRANE-塔吊", 1,
                         size_mm=size, rotation=rotation):
            drawn["symbol"] += 1
            drawn["symbols"].append({"id": crane["id"], "category": "tower_crane",
                                     "center": [cx, cy], "size_mm": size,
                                     "rotation": rotation, "color": 1, "kind": "crane"})
        placer.add_symbol(_symbol_box(cx, cy, size), "crane:{}".format(crane["id"]))
        tag = "T{}".format(index + 1)
        label = "{} {} 臂长{}m".format(
            crane["id"], crane.get("model") or "",
            "—" if not r else "{:.0f}".format(float(r) / 1000.0))
        crane_labels.append((tag, (cx, cy), label, 1))
        drawn["crane"] += 1

    labels: List[Dict[str, Any]] = []
    facility_items = sorted(
        enumerate(model["facilities"]),
        key=lambda item: (0 if item[1]["category"] == "construction_elevator" else
                          1 if item[1]["geometry"]["type"] == "point" else
                          2 if item[1]["geometry"]["type"] == "area" else 3,
                          item[0]))
    for order, (_original, row) in enumerate(facility_items, start=1):
        layer = _layer_of(row["category"])
        color = _color_of(row["category"])
        geom = row["geometry"]
        pts = [(float(p[0]), float(p[1])) for p in geom["points_mm"]]
        if not pts:
            continue
        symbol = block_name(row["category"])
        center = _center_of(row)
        rotation = 0.0
        symbol_size_mm = 0.0
        if geom["type"] == "area":
            msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer, "color": color})
            box = _polygon_box(pts)
            placer.add_footprint(box, row["id"])
            if row["category"] == "notice_board":
                # 九牌一图：不再插单点“九”字块，按 9 块板在长条内画分隔线
                for tick_a, tick_b in _notice_panel_ticks(pts, 9):
                    msp.add_line(tick_a, tick_b, dxfattribs={"layer": layer, "color": color})
            elif symbol:
                if row["category"] == "weighbridge":
                    # 地磅长轴顺行车方向：长边套图块长边，短边套图块短边
                    span_long = max(box.width, box.height)
                    span_short = min(box.width, box.height)
                    a, b = _longest_edge(pts)
                    rotation = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
                else:
                    span_long = max(1000.0, min(box.width, box.height))
                    span_short = max(box.width, box.height)
                symbol_size_mm = _symbol_render_size(row["category"], text_h, "area",
                                                     span_long, span_short)
                insert_symbol(msp, row["category"], center[0], center[1], layer, color,
                              size_mm=symbol_size_mm, rotation=rotation)
                placer.add_symbol(_symbol_box(center[0], center[1], symbol_size_mm),
                                  "symbol:{}".format(row["id"]))
                drawn["symbol"] += 1
                drawn["symbols"].append({"id": row["id"], "category": row["category"],
                                         "center": [center[0], center[1]],
                                         "size_mm": symbol_size_mm, "rotation": rotation,
                                         "color": color, "kind": "area"})
        elif geom["type"] == "line":
            msp.add_lwpolyline(pts, dxfattribs={"layer": layer, "color": color})
            for index in range(len(pts) - 1):
                placer.add_segment(pts[index], pts[index + 1],
                                   "line:{}:{}".format(row["id"], index))
            if symbol:
                a, b = _longest_edge(pts)
                center = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
                rotation = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) - 90.0
                symbol_size_mm = _symbol_render_size(row["category"], text_h, "line")
                insert_symbol(msp, row["category"], center[0], center[1], layer, color,
                              size_mm=symbol_size_mm, rotation=rotation)
                placer.add_symbol(_symbol_box(center[0], center[1], symbol_size_mm),
                                  "symbol:{}".format(row["id"]))
                drawn["symbol"] += 1
                drawn["symbols"].append({"id": row["id"], "category": row["category"],
                                         "center": [center[0], center[1]],
                                         "size_mm": symbol_size_mm, "rotation": rotation,
                                         "color": color, "kind": "line"})
        else:
            x, y = pts[0]
            center = (x, y)
            if symbol:
                symbol_size_mm = _symbol_render_size(row["category"], text_h, "point")
                insert_symbol(msp, row["category"], x, y, layer, color,
                              size_mm=symbol_size_mm)
                placer.add_symbol(_symbol_box(x, y, symbol_size_mm),
                                  "symbol:{}".format(row["id"]))
                drawn["symbol"] += 1
                drawn["symbols"].append({"id": row["id"], "category": row["category"],
                                         "center": [x, y], "size_mm": symbol_size_mm,
                                         "rotation": 0.0, "color": color, "kind": "point"})
            else:
                msp.add_circle((x, y), text_h * 0.55,
                               dxfattribs={"layer": layer, "color": color})
                placer.add_symbol(_symbol_box(x, y, text_h * 1.1),
                                  "symbol:{}".format(row["id"]))
        placer.add_footprint(TextBox(center[0] - text_h * 0.2, center[1] - text_h * 0.2,
                                     center[0] + text_h * 0.2, center[1] + text_h * 0.2),
                             row["id"])
        labels.append({"tag": "{:02d}".format(order), "anchor": center, "row": row,
                       "text": _facility_label(row), "height": text_h * (0.90 if geom["type"] != "line" else 0.82),
                       "color": color})
        drawn["facility"] += 1

    placements = []
    for tag, anchor, label, color in crane_labels:
        placements.append(placer.place(label, anchor, text_h * 0.95, ref=tag,
                                       layer="CRANE-塔吊", color=color,
                                       short=tag, scale_hint=1.0))
    for item in labels:
        # ref 用设施 id：允许标签压自身轮廓/自身线段，但仍避让图块和其他设施。
        placements.append(placer.place(item["text"], item["anchor"], item["height"],
                                       ref=item["row"]["id"], layer="TEXT-标注",
                                       color=item["color"], short=item["tag"], scale_hint=1.0))

    # 坐标点编号与角点/设施标记同源；只标图内关键点，全量点看 CSV。
    table_rows = select_table_rows(coord_rows)
    drawn["coordinate_table_rows"] = table_rows
    coord_height = text_h * 0.58
    for row in table_rows:
        if not row.get("map"):
            continue
        x = float(row["x_m"]) * 1000.0
        y = float(row["y_m"]) * 1000.0
        size = text_h * 0.55
        msp.add_line((x - size, y), (x + size, y),
                     dxfattribs={"layer": "COORD-坐标", "color": 4})
        msp.add_line((x, y - size), (x, y + size),
                     dxfattribs={"layer": "COORD-坐标", "color": 4})
        placer.add_segment((x - size, y), (x + size, y), "coordmark:{}".format(row["id"]))
        placer.add_segment((x, y - size), (x, y + size), "coordmark:{}".format(row["id"]))
        placements.append(placer.place(str(row["id"]), (x + size * 1.25, y + size * 0.55),
                                       coord_height, ref=str(row["id"]),
                                       layer="COORD-坐标", color=4,
                                       short=str(row["id"]), scale_hint=1.0))

    for placement in placements:
        if _add_placement_text(msp, placement):
            drawn["text"] += 1
    drawn["placements"] = placements
    drawn["text_layout"] = layout_summary(placements)

    drawn["coordinate_table"] = _draw_coordinate_table(
        msp, table_rows, table_band, text_h, total_rows=len(coord_rows))
    drawn["coordinate_rows"] = int(drawn["coordinate_table"]["rows"])

    _draw_north_arrow(msp, x0 + text_h * 2.2, y1 - text_h * 3.2, text_h * 1.3)
    drawn["north_arrow"] = 1
    _draw_scale_bar(msp, x0 + text_h * 1.2, y0 + text_h * 1.2, text_h)
    drawn["scale_bar"] = 1

    _draw_legend(msp, model, map_frame, sheet[2], legend_w, text_h,
                 drawn["dimension"], len(coord_rows), drawn["text_layout"])

    sb_x0, sb_y0, _sb_x1, _sb_y1 = sheet
    tb_height = text_h * 7.0
    tb_top = sb_y0 + tb_height
    msp.add_lwpolyline([(sb_x0, sb_y0), (sheet[2], sb_y0), (sheet[2], tb_top), (sb_x0, tb_top)],
                       close=True, dxfattribs={"layer": "META-图签"})
    tb_texts = [
        title.get("title") or "施工平面布置图",
        "阶段: {}    图号: {}    比例: {}".format(
            STAGE_NAMES[model["stage"]], title.get("drawing_no") or "—", title.get("scale") or "1:500"),
        "contract_id: {}    技能版本: {}    日期: {}".format(
            title.get("contract_id") or "缺失", VERSION, title.get("date") or ""),
        "{}    单位: mm    1:1 模型空间    尺寸 {} 处 / 坐标 {} 点".format(
            draft_label, drawn["dimension"], len(coord_rows)),
        (title.get("disclaimer") or "")[:120],
    ]
    for index, line in enumerate(tb_texts):
        _add_text(msp, line, sb_x0 + text_h * 0.5,
                  tb_top - text_h * (1.1 + index * 1.05), text_h * 0.7, "META-图签")
        drawn["text"] += 1
    return drawn


# ---------- PNG ----------

def _overlap_area(a, b) -> float:
    width = min(a[2], b[2]) - max(a[0], b[0])
    height = min(a[3], b[3]) - max(a[1], b[1])
    return max(0.0, width) * max(0.0, height)


def _boxes_overlap(a, b) -> bool:
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def _draw_png_north(draw: Any, x: float, y: float, size: float, font: Any) -> None:
    draw.ellipse((x - size, y - size, x + size, y + size), outline="#222222", width=3)
    draw.polygon([(x, y - size * 0.9), (x - size * 0.32, y + size * 0.45),
                  (x + size * 0.32, y + size * 0.45)], fill="#222222")
    draw.text((x - 10, y - size - 34), "N", fill="#111111", font=font)


def _draw_png_scale(draw: Any, x: float, y: float, scale: float, font: Any,
                    degraded: bool) -> float:
    segment = SCALE_BAR_MM / 4.0
    bar_h = 12
    for index in range(4):
        x1 = x + index * segment * scale
        x2 = x1 + segment * scale
        draw.rectangle((x1, y, x2, y + bar_h), outline="#222222",
                       fill="#222222" if index % 2 == 0 else "#ffffff")
    for label, offset in (("0", 0), ("10", 2), ("20m", 4)):
        draw.text((x + offset * segment * scale - 8, y + bar_h + 4),
                  _png_safe(label, degraded), fill="#222222", font=font)
    draw.text((x, y - 22), _png_safe("比例尺（模型 1:1）", degraded),
              fill="#222222", font=font)
    return segment * 4 * scale


def _draw_png_coordinate_table(draw: Any, font: Any,
                               rows: Sequence[Dict[str, Any]],
                               box: Tuple[float, float, float, float],
                               degraded: bool,
                               total_rows: Optional[int] = None) -> Dict[str, Any]:
    """PNG 关键点坐标表：按像素字宽自适应分栏；信息不足时宁可少画点。"""
    x0, y0, x1, y1 = box
    avail_w = max(1.0, x1 - x0 - 28)
    header_y = y0 + 32
    line_h = 21
    per_col = max(1, int((y1 - header_y - 12) / line_h))
    info: Dict[str, Any] = {"rows": 0, "total": len(rows), "dropped": 0,
                            "columns": 0, "fits": True}
    if not rows:
        return info

    def build(include_type: bool):
        heads = ("编号", "类型", "X(m)", "Y(m)") if include_type else ("编号", "X(m)", "Y(m)")
        vals = []
        for row in rows:
            base = [str(row["id"]), "{:.2f}".format(row["x_m"]), "{:.2f}".format(row["y_m"])]
            vals.append([base[0], row["type"], base[1], base[2]] if include_type else base)
        widths = []
        for index, head in enumerate(heads):
            need = draw.textlength(head, font=font)
            for row in vals:
                need = max(need, draw.textlength(row[index], font=font))
            widths.append(need + 18)
        return heads, vals, widths

    heads, vals, widths = build(True)
    if sum(widths) > avail_w:
        heads, vals, widths = build(False)
    block_w = sum(widths)
    cols = max(1, int(avail_w // max(block_w, 1.0)))
    capacity = per_col * cols
    shown = list(rows[:capacity])
    vals = vals[:len(shown)]
    ncols = max(1, math.ceil(len(shown) / per_col))
    actual_w = avail_w / ncols
    fits = block_w <= actual_w + 0.5

    draw.text((x0 + 14, y0 + 6), _png_safe(
        "关键点坐标表（m，场地局部坐标；图内 {} 点，全量 {} 点见 CSV；须与测量控制点联测复核）".format(
            len(rows), int(total_rows or len(rows))),
        degraded), fill="#111111", font=font)
    for index, row in enumerate(vals):
        col = index // per_col
        line = index % per_col
        cx = x0 + 14 + col * actual_w
        cy = header_y + line * line_h
        if line == 0:
            if col > 0:
                draw.line((cx - 8, y0, cx - 8, y1), fill="#cccccc", width=1)
            offset = 0.0
            for head, width in zip(heads, widths):
                draw.text((cx + offset, y0 + 20), _png_safe(head, degraded),
                          fill="#333333", font=font)
                offset += width
        offset = 0.0
        for value, width in zip(row, widths):
            draw.text((cx + offset, cy), _png_safe(str(value), degraded),
                      fill="#222222", font=font)
            offset += width
    info.update({"rows": len(shown), "dropped": len(rows) - len(shown),
                 "columns": ncols, "fits": fits})
    return info


def _render_png(model: Dict[str, Any], base_map: Dict[str, Any],
                map_frame: Tuple[float, float, float, float], title: Dict[str, Any],
                draft_label: str, dim_specs: Sequence[Dict[str, Any]],
                coord_rows: Sequence[Dict[str, Any]], drawn: Dict[str, Any],
                path: Path) -> Dict[str, Any]:
    """按 DXF 的同一套图块/文字排版渲染 PNG，不另做一套“找空位”兜底。"""
    from PIL import Image, ImageDraw

    width, height = 2400, 1650
    legend_w = 640
    map_right = width - legend_w
    map_bottom = 1005
    table_top = 1020
    table_bottom = 1230
    title_top = 1248
    margin = 55
    x0, y0, x1, y1 = map_frame
    span_x, span_y = max(1.0, x1 - x0), max(1.0, y1 - y0)
    scale = min((map_right - 2 * margin) / span_x, (map_bottom - 2 * margin) / span_y)
    ox = margin + ((map_right - 2 * margin) - span_x * scale) / 2.0
    oy = margin + ((map_bottom - 2 * margin) - span_y * scale) / 2.0

    def tx(x: float) -> float:
        return ox + (x - x0) * scale

    def ty(y: float) -> float:
        return oy + (y1 - y) * scale

    image = Image.new("RGB", (width, height), "#f7f7f4")
    draw = ImageDraw.Draw(image)
    font_cache: Dict[int, Any] = {}

    def font_for(size: int) -> Any:
        size = max(8, min(96, int(size)))
        if size not in font_cache:
            font_cache[size] = _pick_font(size)[0]
        return font_cache[size]

    font_small_px = max(14, min(19, round(1900.0 * scale)))
    font_small = font_for(font_small_px)
    # 尺寸文字与设施标签同量级，避免 DIMENSION 文字比标注大一圈压住图元。
    font_dim = font_for(max(12, min(18, round(font_small_px * 0.82))))
    font_mid = font_for(max(22, font_small_px + 6))
    font_title = font_for(44)
    font_draft = font_for(64)
    _font_probe, font_status, font_path = _pick_font(18)
    degraded = font_status == "degraded"

    colors = {1: "#b71c1c", 2: "#9a6700", 3: "#1b6b3a", 4: "#1f5f99",
              5: "#5b2c83", 6: "#006d77", 7: "#333333", 8: "#8d8d8d",
              30: "#a84b13", 32: "#5d4037", 40: "#455a64"}

    def color_of(value: int) -> str:
        return colors.get(int(value), "#333333")

    def tint(value: int) -> str:
        rgb = tuple(int(color_of(value)[i:i + 2], 16) for i in (1, 3, 5))
        base = (247, 247, 244)
        mix = tuple(round(base[i] * 0.88 + rgb[i] * 0.12) for i in range(3))
        return "#{:02x}{:02x}{:02x}".format(*mix)

    base_window = _site_window(model, base_map)
    for row in base_map.get("site_geometry") or []:
        geom = row.get("geometry")
        if isinstance(geom, list) and len(geom) >= 4:
            gx0, gy0, gx1, gy1 = (float(geom[0]), float(geom[1]),
                                  float(geom[2]), float(geom[3]))
            if base_window:
                clipped = _clip_segment_to_box(gx0, gy0, gx1, gy1, base_window)
                if clipped is None:
                    continue
                gx0, gy0, gx1, gy1 = clipped
            draw.line((tx(gx0), ty(gy0), tx(gx1), ty(gy1)), fill="#cececa", width=1)

    outline = base_map.get("structure_outline") or []
    if isinstance(outline, list) and len(outline) >= 3:
        pts = [(tx(float(p[0])), ty(float(p[1]))) for p in outline]
        draw.line(pts + [pts[0]], fill="#666666", width=3)

    redline = model.get("redline") or []
    if len(redline) >= 2:
        pts = [(tx(float(p[0])), ty(float(p[1]))) for p in redline]
        draw.line(pts + ([pts[0]] if model.get("redline_closed") else []),
                  fill="#c0392b", width=4)

    # 塔吊回转半径：淡色覆盖 + 虚线圆，保留“示意半径”语义。
    if model["cranes"]:
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        for crane in model["cranes"]:
            cx, cy = crane["center_mm"]
            r = crane.get("jib_mm") or 0.0
            if not r:
                continue
            box = (tx(cx - r), ty(cy + r), tx(cx + r), ty(cy - r))
            odraw.ellipse(box, fill=(192, 57, 43, 15))
            for angle in range(0, 360, 6):
                odraw.arc(box, start=angle, end=angle + 3.4,
                          fill=(160, 45, 38, 190), width=2)
        image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(image)

    # 面/线设施先画几何底色，图块再压在中心，避免图例色块替代类型图标。
    for row in model["facilities"]:
        color = color_of(_color_of(row["category"]))
        pts = [(tx(float(p[0])), ty(float(p[1]))) for p in row["geometry"]["points_mm"]]
        if not pts:
            continue
        if row["geometry"]["type"] == "area":
            if len(pts) >= 3:
                draw.polygon(pts, fill=tint(_color_of(row["category"])))
                draw.line(pts + [pts[0]], fill=color, width=3)
                if row["category"] == "notice_board":
                    # 九牌一图在 PNG 上也画出 9 块分隔，避免只剩一条长边
                    for tick_a, tick_b in _notice_panel_ticks(pts, 9):
                        draw.line((tx(tick_a[0]), ty(tick_a[1]),
                                   tx(tick_b[0]), ty(tick_b[1])),
                                  fill=color, width=2)
        elif row["geometry"]["type"] == "line":
            nominal = float(row.get("width_mm") or 4000.0) * scale * 0.32
            draw.line(pts, fill=color, width=max(3, min(12, round(nominal))))

    # 与 DXF INSERT 一一对应的 PNG 图元（塔吊/施工电梯含桁架、吊钩、吊笼等）。
    for item in drawn.get("symbols") or []:
        cx, cy = item["center"]
        category = str(item.get("category") or "")
        size_px = float(item["size_mm"]) * scale
        if category == "tower_crane":
            size_px = max(size_px, 86.0)
        elif category == "construction_elevator":
            size_px = max(size_px, 62.0)
        elif category in ("wheel_wash", "weighbridge", "notice_board"):
            size_px = max(size_px, 30.0)
        elif item.get("kind") == "area":
            size_px = max(size_px, 22.0)
        else:
            size_px = max(size_px, 14.0)
        color = color_of(item["color"])
        # 塔吊/施工电梯先描白边再上色，避免与底图灰色线条糊在一起。
        if category in ("tower_crane", "construction_elevator"):
            draw_pictogram(draw, category, tx(cx), ty(cy), size_px, "#ffffff",
                           width=max(4, int(round(size_px / 16.0))),
                           rotation=float(item.get("rotation") or 0.0))
        draw_pictogram(draw, category, tx(cx), ty(cy), size_px, color,
                       width=max(1, int(round(size_px / 34.0))),
                       rotation=float(item.get("rotation") or 0.0))

    # 没有对应图块的旧数据点设施，保留小圆点而不是消失。
    symbol_ids = {str(item.get("id")) for item in drawn.get("symbols") or []}
    for row in model["facilities"]:
        if row["geometry"]["type"] != "point" or str(row["id"]) in symbol_ids:
            continue
        x, y = row["geometry"]["points_mm"][0]
        px, py = tx(float(x)), ty(float(y))
        draw.ellipse((px - 5, py - 5, px + 5, py + 5),
                     fill=color_of(_color_of(row["category"])))

    # 坐标标记：主图只画定位控制点；全量点在图下坐标表与 CSV，避免编号铺满图面。
    map_rows = [row for row in (drawn.get("coordinate_table_rows") or coord_rows)
                if row.get("map")]
    for row in map_rows:
        x, y = tx(row["x_m"] * 1000.0), ty(row["y_m"] * 1000.0)
        draw.line((x - 5, y, x + 5, y), fill="#1f6fb2", width=2)
        draw.line((x, y - 5, x, y + 5), fill="#1f6fb2", width=2)

    # 尺寸标注：与 DXF 的 DIMENSION 同源。
    png_dimension_failures: List[Dict[str, Any]] = []
    for spec in dim_specs:
        p1 = (tx(float(spec["p1"][0])), ty(float(spec["p1"][1])))
        p2 = (tx(float(spec["p2"][0])), ty(float(spec["p2"][1])))
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        length = math.hypot(dx, dy)
        if length <= 1e-6:
            png_dimension_failures.append({
                "kind": str(spec.get("kind") or "unknown"),
                "text": str(spec.get("text") or ""),
                "refs": list(spec.get("refs") or []),
                "reason": "ZeroLengthDimension: 图面投影长度为 0",
            })
            continue
        nx, ny = -dy / length, dx / length
        offset = float(spec["offset"]) * scale
        a = (p1[0] + nx * offset, p1[1] + ny * offset)
        b = (p2[0] + nx * offset, p2[1] + ny * offset)
        draw.line((p1[0], p1[1], a[0], a[1]), fill="#b8860b", width=1)
        draw.line((p2[0], p2[1], b[0], b[1]), fill="#b8860b", width=1)
        draw.line((a[0], a[1], b[0], b[1]), fill="#b8860b", width=2)
        for point, other in ((a, b), (b, a)):
            ux, uy = (other[0] - point[0]) / length, (other[1] - point[1]) / length
            draw.line((point[0], point[1], point[0] + ux * 9 - ny * 4,
                       point[1] + uy * 9 + nx * 4), fill="#b8860b", width=2)
            draw.line((point[0], point[1], point[0] + ux * 9 + ny * 4,
                       point[1] + uy * 9 - nx * 4), fill="#b8860b", width=2)
        label = _png_safe(spec["text"], degraded)
        mid = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
        box = draw.textbbox((0, 0), label, font=font_dim)
        tw, th = box[2] - box[0], box[3] - box[1]
        draw.rectangle((mid[0] - tw / 2 - 3, mid[1] - th - 8,
                        mid[0] + tw / 2 + 3, mid[1] - 1), fill="#f7f7f4")
        draw.text((mid[0] - tw / 2, mid[1] - th - 4), label,
                  fill="#7a5c00", font=font_dim)

    _draw_png_north(draw, margin + 42, margin + 52, 34, font_mid)
    _draw_png_scale(draw, margin + 10, map_bottom - 58, scale, font_small, degraded)

    # 文字全部使用 DXF TextPlacer 的 placement；unplaced 不硬画。
    for placement in drawn.get("placements") or []:
        if getattr(placement, "level", "") == "unplaced":
            continue
        box = placement.box
        bx0, bx1 = tx(box.x0), tx(box.x1)
        box_top, box_bottom = ty(box.y1), ty(box.y0)
        box_w = max(1.0, bx1 - bx0)
        box_h = max(1.0, box_bottom - box_top)
        target_px = max(8, min(30, round(float(placement.height) * scale * 1.10)))
        target_px = min(target_px, max(8, round(box_h / 1.18)))
        text_px = _png_safe(placement.text, degraded)
        chosen = target_px
        while chosen > 8:
            font = font_for(chosen)
            try:
                text_w = draw.textlength(text_px, font=font)
            except Exception:
                text_w = len(text_px) * chosen * 0.6
            if text_w <= box_w + 1:
                break
            chosen -= 1
        font = font_for(chosen)
        color = color_of(placement.color)
        if placement.leader:
            p1, p2 = placement.leader
            draw.line((tx(p1[0]), ty(p1[1]), tx(p2[0]), ty(p2[1])),
                      fill=color, width=1)
        draw.rectangle((bx0 - 1, box_top - 1, bx1 + 1, box_bottom + 1), fill="#f7f7f4")
        draw.text((bx0, (box_top + box_bottom) / 2.0), text_px, fill=color,
                  font=font, anchor="lm")

    # 右侧图例：图标与 DXF/主图共用 draw_pictogram；不再用彩色方块。
    draw.rectangle((map_right + 10, 55, width - 18, map_bottom - 8),
                   outline="#222222", width=2, fill="#ffffff")
    y = 66
    if draft_label:
        draw.text((map_right + 26, y), _png_safe("DRAFT", degraded),
                  fill=(183, 28, 28), font=font_draft)
        y = draw.textbbox((map_right + 26, y), "DRAFT", font=font_draft)[3] + 6
    draw.text((map_right + 26, y), _png_safe("图 例", degraded),
              fill="#111111", font=font_title)
    y = draw.textbbox((map_right + 26, y), "图 例", font=font_title)[3] + 6
    row_pitch = 22
    facility_pitch = 34
    icon_size = 30

    def section(label: str) -> None:
        nonlocal y
        draw.text((map_right + 26, y), _png_safe(label, degraded),
                  fill="#111111", font=font_mid)
        y += 26

    section("【设施】")
    facility_items = categories_in(model)
    facility_cols = 2
    facility_rows = max(1, math.ceil(len(facility_items) / facility_cols))
    facility_top = y
    for index, item in enumerate(facility_items):
        col = index // facility_rows
        row = index % facility_rows
        ix = map_right + 26 + col * 294
        iy = facility_top + row * facility_pitch
        big = {"tower_crane": 46, "construction_elevator": 42,
               "weighbridge": 38, "wheel_wash": 36,
               "notice_board": 38}.get(item["category"], icon_size)
        draw_pictogram(draw, item["category"], ix + big / 2.0 + 2, iy + big / 2.0 + 1,
                       big, color_of(_color_of(item["category"])), width=1)
        draw.text((ix + big + 12, iy + (big - 16) / 2.0),
                  _png_safe("{} ×{}".format(item["name"], item["count"]), degraded),
                  fill="#222222", font=font_small)
    y = facility_top + facility_rows * facility_pitch + 1

    section("【线 型】")
    seen = set()
    for row in model["facilities"]:
        if row["geometry"]["type"] != "line" or row["category"] in seen:
            continue
        seen.add(row["category"])
        color = color_of(_color_of(row["category"]))
        draw.line((map_right + 26, y + 9, map_right + 80, y + 9), fill=color, width=4)
        width_m = row.get("width_mm")
        label = row["category_name"] + (" {:.1f}m".format(width_m / 1000.0) if width_m else "")
        draw.text((map_right + 90, y), _png_safe(label, degraded),
                  fill="#222222", font=font_small)
        y += row_pitch
    if model.get("cranes"):
        draw.ellipse((map_right + 26, y + 1, map_right + 48, y + 21),
                     outline="#5b2c83", width=2)
        draw.text((map_right + 58, y), _png_safe("塔吊回转覆盖（示意）", degraded),
                  fill="#222222", font=font_small)
        y += row_pitch
    y += 3

    section("【标 注】")
    draw.line((map_right + 26, y + 9, map_right + 72, y + 9), fill="#b8860b", width=3)
    draw.text((map_right + 86, y), _png_safe("尺寸 {} 处".format(len(dim_specs)), degraded),
              fill="#222222", font=font_small)
    y += row_pitch
    draw.rectangle((map_right + 26, y + 2, map_right + 54, y + 20),
                   outline="#1f6fb2", width=2)
    draw.text((map_right + 64, y), _png_safe("坐标点 {} 个".format(len(coord_rows)), degraded),
              fill="#222222", font=font_small)
    y += row_pitch

    text_layout = drawn.get("text_layout") or {}
    index_entries = list(text_layout.get("index_entries") or [])
    if index_entries:
        y += 2
        section("【入图例编号】")
        for entry in index_entries:
            draw.text((map_right + 26, y),
                      _png_safe("{} = {}".format(entry.get("tag") or "?", entry.get("text") or ""), degraded),
                      fill="#222222", font=font_small)
            y += row_pitch

    y += 2
    section("【说 明】")
    # 说明压缩为三条，避免超出图例框压到坐标表；长句按图例内宽自动换行。
    note_width = width - 18 - (map_right + 26) - 6
    for note in ("图元放大示意；臂长/导轨/图块非厂家尺寸，须按机型复核。",
                 "净距/宽度为图面几何量；坐标为场地局部坐标，须与控制点联测。",
                 "候选设施须项目技术负责人逐项确认；DRAFT 不替代审批与现场复核。"):
        line = ""
        for char in note:
            probe = line + char
            if line and draw.textlength(_png_safe(probe, degraded), font=font_small) > note_width:
                draw.text((map_right + 26, y), _png_safe(line, degraded),
                          fill="#555555", font=font_small)
                y += 17
                line = char
            else:
                line = probe
        if line:
            draw.text((map_right + 26, y), _png_safe(line, degraded),
                      fill="#555555", font=font_small)
            y += 17

    # 关键点坐标表（图内表格）：列宽按实际字宽计算，先减列再减行，绝不横向重叠
    png_table_info = _draw_png_coordinate_table(
        draw, font_small, drawn.get("coordinate_table_rows") or coord_rows,
        (30, table_top, width - 30, table_bottom), degraded, total_rows=len(coord_rows))

    draw.rectangle((30, title_top, width - 30, height - 30),
                   outline="#222222", width=3, fill="#ffffff")
    draw.text((55, title_top + 20), _png_safe(title.get("title") or "施工平面布置图", degraded),
              fill="#111111", font=font_title)
    draw.text((width - 900, title_top + 26), _png_safe(
        "{}  {}".format(STAGE_NAMES[model["stage"]], draft_label), degraded),
        fill="#c62828", font=font_mid)
    lines = [
        "图号 {}    比例 {}    版本 {}".format(
            title.get("drawing_no") or "—", title.get("scale") or "1:500", title.get("revision") or "0"),
        "contract_id: {}    技能版本 {}    日期 {}".format(
            title.get("contract_id") or "缺失", VERSION, title.get("date") or ""),
        "设施 {} 项（本阶段生效）    尺寸 {} 处 / 坐标 {} 点".format(
            model["counts"]["active"], len(dim_specs), len(coord_rows)),
        "规则 pass/fail/manual = {}/{}/{}    道路 pass/fail/manual = {}/{}/{}".format(
            model["summary"]["pass"], model["summary"]["fail"], model["summary"]["manual"],
            (model.get("road_summary") or {}).get("pass", 0),
            (model.get("road_summary") or {}).get("fail", 0),
            (model.get("road_summary") or {}).get("manual", 0)),
    ]
    y = title_top + 85
    for line in lines:
        draw.text((55, y), _png_safe(line, degraded), fill="#222222", font=font_mid)
        y += 36
    text = title.get("disclaimer") or ""
    for start in range(0, len(text), 60):
        draw.text((55, y), _png_safe(text[start:start + 60], degraded),
                  fill="#555555", font=font_small)
        y += 24
    image.save(path, "PNG", dpi=(200, 200), optimize=True)
    return {"font_status": font_status, "font_path": font_path, "dpi": 200,
            "pixel_size": [width, height], "degraded": degraded,
            "dimension_failures": png_dimension_failures,
            "text_layout": text_layout, "symbol_count": len(drawn.get("symbols") or [])}


# ---------- 自检 ----------

def _scan_dxf_text_overlaps(doc: Any,
                            map_frame: Tuple[float, float, float, float],
                            extra_frames: Sequence[Tuple[float, float, float, float]] = ()
                            ) -> List[Dict[str, Any]]:
    """独立读取已保存 DXF 的主图/表格 TEXT 实体，复扫矩形重叠。"""
    frames = [map_frame] + list(extra_frames)
    rows = []
    for entity in doc.modelspace().query("TEXT"):
        if entity.dxf.layer not in ("TEXT-标注", "CRANE-塔吊", "COORD-坐标"):
            continue
        try:
            px, py = float(entity.dxf.insert[0]), float(entity.dxf.insert[1])
            h = float(entity.dxf.height or 0.0)
            value = str(entity.dxf.text or "")
        except (AttributeError, TypeError, ValueError):
            continue
        box = TextBox(px, py, px + text_width(value, h), py + h * 1.2)
        inside = False
        for x0, y0, x1, y1 in frames:
            if (box.x1 >= x0 and box.x0 <= x1 and box.y1 >= y0 and box.y0 <= y1):
                inside = True
                break
        if not inside:
            continue
        rows.append((value, entity.dxf.layer, box))
    problems: List[Dict[str, Any]] = []
    for index, (text_a, layer_a, box_a) in enumerate(rows):
        for text_b, layer_b, box_b in rows[index + 1:]:
            area = box_a.overlap_area(box_b)
            if area > 0:
                problems.append({"a": text_a, "b": text_b,
                                 "layers": [layer_a, layer_b],
                                 "area": round(area, 1)})
    return problems[:20]


def _all_failed_checks(model: Dict[str, Any]) -> List[str]:
    """规则、道路 R1~R4、周边硬约束任一 fail 都必须进入图签与自检。"""
    failed = [c["name"] for c in model.get("checks") or [] if c.get("status") == "fail"]
    failed += [str(name) for name in model.get("road_failed") or []]
    failed += [str(name) for name in model.get("context_failed") or []]
    return failed


def _check_counts(model: Dict[str, Any]) -> Dict[str, int]:
    counts = {"pass": 0, "fail": 0, "manual": 0, "review": 0}
    for summary in (model.get("summary"), model.get("road_summary"),
                    model.get("context_summary")):
        for key, value in (summary or {}).items():
            if key in counts:
                counts[key] += int(value or 0)
    return counts


def _write_layers_csv(doc: Any, model: Dict[str, Any], path: Path) -> None:
    msp = doc.modelspace()
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["图层", "分类", "颜色", "实体数"])
        for name, color, _linetype in _base_layers(model):
            category = next((row["category"] for row in model["facilities"]
                             if _layer_of(row["category"]) == name), "")
            writer.writerow([name, category, color, len(list(msp.query('*[layer=="{}"]'.format(name))))])


def _write_coordinates_csv(rows: Sequence[Dict[str, Any]], path: Path) -> int:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["编号", "类型", "名称", "X_m", "Y_m", "说明"])
        for row in rows:
            writer.writerow([row["id"], row["type"], row["name"],
                             "{:.3f}".format(row["x_m"]), "{:.3f}".format(row["y_m"]), row["note"]])
    return len(rows)


def _selfcheck(model: Dict[str, Any], doc: Any, title: Dict[str, Any],
               png_info: Dict[str, Any], draft_label: str,
               annotations: Dict[str, Any]) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = []

    def add(index: int, name: str, status: str, evidence: Dict[str, Any], message: str = "") -> None:
        items.append({"id": index, "name": name, "status": status,
                      "evidence": evidence, "message": message})

    add(1, "红线闭合", "pass" if model["redline_closed"] else "fail",
        {"redline_closed": model["redline_closed"],
         "redline_area_m2": model.get("redline_area_m2")})
    missing_layers = []
    names = {layer.dxf.name for layer in doc.layers}
    for row in model["facilities"]:
        if _layer_of(row["category"]) not in names:
            missing_layers.append(_layer_of(row["category"]))
    missing_blocks = []
    for row in model["facilities"]:
        name = block_name(row["category"])
        if name and not name in doc.blocks:
            missing_blocks.append(name)
    add(2, "设施图层与图块齐全", "fail" if missing_layers or missing_blocks else "pass",
        {"missing": sorted(set(missing_layers)), "missing_blocks": sorted(set(missing_blocks)),
         "required": len(_base_layers(model))})
    add(3, "阶段标识一致", "pass" if title.get("stage") == model["stage"] else "fail",
        {"model_stage": model["stage"], "title_stage": title.get("stage")})
    try:
        insunits = int(doc.header.get("$INSUNITS", 0))
    except (TypeError, ValueError):
        insunits = 0
    add(4, "单位一致（mm）", "pass" if insunits == 4 and model["coord_unit"] == "mm" else "fail",
        {"insunits": insunits, "expected": 4, "coord_unit": model["coord_unit"]})
    failed_all = _all_failed_checks(model)
    add(5, "规则、道路与周边校核无 fail",
        "fail" if failed_all else "pass",
        {"rule_summary": model.get("summary"), "road_summary": model.get("road_summary"),
         "context_summary": model.get("context_summary"),
         "failed": failed_all})
    add(6, "PNG 可读性（字体）",
        "manual" if png_info.get("degraded") else "pass",
        {"font_status": png_info.get("font_status"), "font_path": png_info.get("font_path")})
    add(7, "DRAFT 标识", "pass" if draft_label and title.get("draft") == draft_label else "fail",
        {"expected": draft_label, "actual": title.get("draft")})

    # 8 尺寸标注覆盖：实际渲染成功的 DIMENSION 才能计入覆盖
    kinds = list(annotations.get("dimension_kinds") or [])
    applicable = list(annotations.get("applicable") or [])
    blocked = list(annotations.get("blocked") or [])
    skipped = list(annotations.get("skipped") or [])
    failures = list(annotations.get("dimension_failures") or [])
    missing = [kind for kind in applicable if kind not in kinds]
    explained = set(blocked)
    explained.update(str(item.get("kind")) for item in skipped
                     if str(item.get("kind")) in applicable)
    unexplained = [kind for kind in missing if kind not in explained]
    rendered_count = int(annotations.get("dimension_rendered", 0))
    entity_count = int(annotations.get("dimension_count", 0))
    manual_reasons: List[str] = []
    for kind in blocked:
        manual_reasons.append("{}缺输入，降级 manual".format(KIND_NAMES.get(kind, kind)))
    for item in skipped:
        if str(item.get("kind")) in applicable:
            manual_reasons.append("{}：{}".format(
                KIND_NAMES.get(str(item.get("kind")), str(item.get("kind"))),
                item.get("reason") or "未说明"))
    for item in failures:
        manual_reasons.append("{}渲染失败（{}）".format(
            KIND_NAMES.get(str(item.get("kind")), str(item.get("kind"))),
            item.get("reason") or "未说明"))
    if entity_count != rendered_count:
        status8 = "fail"
        msg8 = "DIMENSION 实体数 {} 与成功渲染数 {} 不一致".format(entity_count, rendered_count)
    elif unexplained:
        status8 = "fail"
        msg8 = "以下可标注类型没有生成 DIMENSION 且无降级原因：{}".format("、".join(unexplained))
    elif manual_reasons:
        status8 = "manual"
        msg8 = "；".join(manual_reasons)
    else:
        status8 = "pass"
        msg8 = "已覆盖：{}".format("、".join(KIND_NAMES.get(kind, kind) for kind in kinds))
    add(8, "尺寸标注覆盖（DIMENSION）", status8,
        {"dimension_entities": entity_count, "dimension_rendered": rendered_count,
         "kinds": kinds, "applicable": applicable, "blocked": blocked,
         "missing": missing, "unexplained_missing": unexplained,
         "skipped": skipped, "failures": failures},
        msg8)

    # 9 坐标表与 CSV：CSV 必须是全量，图内表只能是关键点子集
    csv_rows = int(annotations.get("coordinate_csv_rows", 0))
    table_rows = int(annotations.get("coordinate_rows", 0))
    model_rows = int(annotations.get("coordinate_model_rows", 0))
    table = annotations.get("coordinate_table") or {}
    ok9 = (model_rows > 0 and csv_rows == model_rows
           and 0 < table_rows <= model_rows)
    add(9, "坐标表与 CSV 一致（图内为关键点子集）",
        "pass" if ok9 else "fail",
        {"csv_rows": csv_rows, "table_rows": table_rows,
         "model_rows": model_rows, "dropped": table.get("dropped"),
         "table": table,
         "csv": annotations.get("coordinate_csv")},
        "图内关键点 {} 个，全量 {} 个见 CSV".format(table_rows, model_rows))

    add(10, "指北针/比例尺/图例分区",
        "pass" if annotations.get("north_arrow") and annotations.get("scale_bar_m")
        and annotations.get("legend_sections") else "fail",
        {"north_arrow": bool(annotations.get("north_arrow")),
         "scale_bar_m": annotations.get("scale_bar_m"),
         "legend_sections": annotations.get("legend_sections") or []})

    layout = annotations.get("text_layout") or png_info.get("text_layout") or {}
    overlaps = int(layout.get("overlaps") or 0)
    unplaced = list(layout.get("unplaced") or [])
    dxf_overlaps = list(annotations.get("dxf_label_overlaps") or [])
    status11 = "fail" if overlaps or unplaced or dxf_overlaps else "pass"
    if status11 == "pass":
        msg11 = "{} 条标注全部入图，未发现文字矩形重叠".format(layout.get("total", 0))
    else:
        reasons = []
        if overlaps:
            reasons.append("排版复检重叠 {} 组".format(overlaps))
        if dxf_overlaps:
            reasons.append("DXF 独立复扫重叠 {} 组".format(len(dxf_overlaps)))
        if unplaced:
            reasons.append("{} 条标注无处放置".format(len(unplaced)))
        msg11 = "；".join(reasons)
    add(11, "无文字重叠/无未放置标注", status11,
        {"total": int(layout.get("total", 0)),
         "direct": int(layout.get("direct", 0)),
         "leader": int(layout.get("leader", 0)),
         "shifted": int(layout.get("shifted", 0)),
         "shrunk": int(layout.get("shrunk", 0)),
         "index": int(layout.get("index", 0)),
         "unplaced": unplaced,
         "unplaced_count": int(layout.get("unplaced_count", len(unplaced))),
         "overlaps": overlaps,
         "problems": list(layout.get("problems") or []),
         "index_entries": list(layout.get("index_entries") or []),
         "dxf_label_overlaps": dxf_overlaps},
        msg11)

    add(12, "坐标表文字适配（无横压）",
        "pass" if table.get("fits") and table_rows > 0 else "fail",
        {"fits": table.get("fits"), "rows": table_rows,
         "blocks": table.get("blocks"), "block_width_mm": table.get("block_width_mm"),
         "available_width_mm": table.get("available_width_mm"),
         "dropped": table.get("dropped")},
        "表宽 {:.0f} mm ≤ 可用 {:.0f} mm".format(
            float(table.get("block_width_mm") or 0.0),
            float(table.get("available_width_mm") or 0.0)))

    summary = {"pass": 0, "fail": 0, "manual": 0}
    for item in items:
        summary[item["status"]] += 1
    return {"schema": SELFCHECK_SCHEMA,
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "items": items, "summary": summary,
            "exit_code": 5 if summary["fail"] else 0}


def draw_stage(model: Dict[str, Any], base_map: Dict[str, Any], out_dir: str | Path,
               *, title_params: Dict[str, Any]) -> Dict[str, Any]:
    out = Path(out_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    stage = model["stage"]
    dxf_path = out / "layout-{}.dxf".format(stage)
    png_path = out / "layout-{}.png".format(stage)
    csv_path = out / "layers-{}.csv".format(stage)
    coord_path = out / "coordinates-{}.csv".format(stage)
    title_path = out / "titleblock-{}.json".format(stage)
    self_path = out / "selfcheck-{}.json".format(stage)
    json_path = out / "stage-{}.json".format(stage)

    content = _content_frame(model, base_map)
    legend_w = max((content[2] - content[0]) * 0.26, 12000.0)
    # 字高按“PNG 可读 ≈ 1.9 mm 出图字高（1:500）”反算：主图 + 图例总宽 / 150。
    text_h = max((content[2] - content[0] + legend_w) / 150.0, 120.0)
    coord_rows = build_coordinate_rows(model)
    dim_specs, skipped = build_dimension_specs(model, base_map, text_h)

    # 表高按“图内关键点”估，不再按全量点撑高图幅；全量点写在 CSV。
    per_table_block = 10
    preview_rows = select_table_rows(coord_rows)
    rows_per_block = min(per_table_block, max(1, len(preview_rows)))
    table_h = text_h * (1.7 + rows_per_block * 1.45 + 0.8)
    gap = max(text_h * 1.0, 400.0)
    title_h = text_h * 7.2

    sheet = (content[0], content[1] - gap - table_h - title_h,
             content[2] + legend_w, content[3])
    table_band = (sheet[0] + text_h * 0.6, sheet[1] + title_h + gap * 0.5,
                  sheet[2] - text_h * 0.6, sheet[1] + title_h + gap * 0.5 + table_h)

    params = {
        "title": title_params.get("title") or "{}施工平面布置图".format(STAGE_NAMES[stage]),
        "drawing_no": title_params.get("drawing_no") or "SLP-{}".format(stage[:1].upper()),
        "scale": title_params.get("scale") or "1:500",
        "revision": title_params.get("revision") or "0",
        "date": title_params.get("date") or datetime.now().strftime("%Y-%m-%d"),
        "contract_id": title_params.get("contract_id") or "",
        "project": title_params.get("project") or model.get("project") or "",
        "disclaimer": title_params.get("disclaimer") or
        "本图为布置草案，须经项目技术负责人审核；不替代施工组织设计审批、设计签章与现场复核。",
        "stage": stage,
        "stage_name": STAGE_NAMES[stage],
    }
    draft_label = "DRAFT" if not _all_failed_checks(model) else "DRAFT-CHECK-FAIL"
    params["draft"] = draft_label

    doc = _create_doc(_base_layers(model))
    ensure_symbol_blocks(doc)
    drawn = _draw_stage(doc, model, base_map, content, sheet, table_band,
                        params, draft_label, legend_w, dim_specs, coord_rows, text_h)
    finalize_doc_extents(doc)
    doc.saveas(dxf_path)
    saved = ezdxf.readfile(str(dxf_path))
    _write_layers_csv(saved, model, csv_path)
    csv_rows = _write_coordinates_csv(coord_rows, coord_path)
    png_info = _render_png(model, base_map, content, params, draft_label,
                           dim_specs, coord_rows, drawn, png_path)

    msp = saved.modelspace()
    dimension_entities = len(list(msp.query("DIMENSION")))
    dimension_kinds = list(drawn.get("dimension_kinds") or [])
    dimension_failures = list(drawn.get("dimension_failures") or [])
    dimension_failures += list(png_info.get("dimension_failures") or [])
    applicable, blocked = applicable_kinds(model, base_map)
    dxf_text_overlaps = _scan_dxf_text_overlaps(saved, content, extra_frames=(table_band,))
    annotations = {
        "dimension_count": dimension_entities,
        "dimension_rendered": int(drawn.get("dimension", 0)),
        "dimension_kinds": dimension_kinds,
        "dimension_failures": dimension_failures,
        "applicable": applicable,
        "blocked": blocked,
        "skipped": skipped,
        "coordinate_rows": drawn.get("coordinate_rows", 0),
        "coordinate_model_rows": len(coord_rows),
        "coordinate_table": drawn.get("coordinate_table") or {},
        "coordinate_csv_rows": csv_rows,
        "coordinate_csv": str(coord_path),
        "north_arrow": bool(drawn.get("north_arrow")),
        "scale_bar_m": SCALE_BAR_MM / 1000.0,
        "legend_sections": ["设施", "线型", "标注", "说明"],
        "text_layout": drawn.get("text_layout") or {},
        "dxf_label_overlaps": dxf_text_overlaps,
    }
    selfcheck = _selfcheck(model, saved, params, png_info, draft_label, annotations)
    self_path.write_text(json.dumps(selfcheck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    title_payload = dict(params)
    title_payload.update({
        "schema": TITLE_SCHEMA,
        "version": VERSION,
        "frame_bbox_mm": [round(v, 3) for v in sheet],
        "map_bbox_mm": [round(v, 3) for v in content],
        "facilities": len(model["facilities"]),
        "checks": model["summary"],
        "png": png_info,
        "annotations": annotations,
        "source_sha256_before": base_map.get("source_sha256"),
        "dxf": str(dxf_path),
        "png_path": str(png_path),
        "coordinates_csv": str(coord_path),
    })
    title_path.write_text(json.dumps(title_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    model_path = dict(model)
    json_drawn = {k: v for k, v in drawn.items() if k != "placements"}
    json_drawn["placements"] = [
        p.as_dict() if hasattr(p, "as_dict") else dict(p)
        for p in (drawn.get("placements") or [])
    ]
    model_path["drawing"] = {
        "dxf": str(dxf_path), "png": str(png_path), "layers_csv": str(csv_path),
        "coordinates_csv": str(coord_path),
        "titleblock": str(title_path), "selfcheck": str(self_path),
        "drawn": json_drawn, "draft_label": draft_label, "annotations": annotations,
    }
    json_path.write_text(json.dumps(model_path, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "stage": stage, "dxf": str(dxf_path), "png": str(png_path),
        "json": str(json_path), "titleblock": str(title_path),
        "selfcheck": str(self_path), "layers_csv": str(csv_path),
        "coordinates_csv": str(coord_path), "annotations": annotations,
        "draft_label": draft_label, "summary": selfcheck["summary"],
        "exit_code": selfcheck["exit_code"], "png_info": png_info,
        "frame_bbox_mm": [round(v, 3) for v in sheet],
    }
