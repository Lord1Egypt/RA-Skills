"""把 TEXT + LINE 图元还原成结构化「钢筋/材料工程数量表」。

流程：找标题 -> 在标题下方、搜索距离内的水平线里由近到远逐个试«能否长成一张网格»
（结构判据：collect_grid 出来的成员里要有 ≥2 条竖线与这条候选线相接、且总共 ≥2 条
水平线，否则大概率只是标题下划线之类的装饰线，跳过试下一条）-> 从合格的上边框开始
按包围盒连通收集网格线 -> 竖线 x 聚类得列边界、横线 y 聚类得行带 -> 把落在网格内的
文字按 (行带, 列) 分配成单元格 -> 首行带是表头，按关键词映射成列键；其余行带里，
编号列文本匹配「编号」正则的算数据行，其余划入"备注/合计池"，池内文字按 y 聚类成行、
同一行内文字按 x 拼接后交给上层做合计声明抓取。

容差 tol 按每张表自己的标题字高算（0.35×标题字高），标题字高缺失才回退到整张图纸
文字高度中位数——同一张图混排不同比例尺的内容时，全局容差会对小比例尺的表格太粗，
对大比例尺的又太细，必须按表就近取。

找不到编号列时（表结构不是常规钢筋表），不静默跳过：所有非表头行带都按数据行抽取
（mark 留空），并记一条结构性 gap，交由上层判断规则是否适用。标题存在但搜索范围内
找不到合格网格、或网格连通聚合结果异常（列数过多/bbox 离题过大，大概率吸入了不相关
线段）时，同样不静默跳过：产出一条空表 + R005 gap，交由上层统计决定退出码。
"""
from __future__ import annotations

import re
from typing import Optional

from .extract import TextItem, SegmentItem
from .symbols import SymbolTable, decode_spec, EXPLICIT_GRADE_RE
from .rules import load_unit_weights

DEFAULT_TITLE_PATTERNS = [
    re.compile(r"(钢筋|材料|工程).{0,4}(数量|材料|明细)表"),
    re.compile(r"(数量|材料|明细)表"),
]

MARK_RE = re.compile(r"^[NＮnｎ]?\d+[A-Za-z]?$")
CIRCLED_DIGITS = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"

# 顺序即匹配优先级：更具体的键要排在会与之冲突的通用键之前（尤其 unit_weight 要早于 weight，
# 否则"理论重量"里的"重量"会先被 weight 吃掉）。
HEADER_KEY_PRIORITY = ["mark", "position", "spec", "single_length", "count", "unit_weight", "total_length", "weight"]
HEADER_KEYWORDS = {
    "mark": ["钢筋编号", "筋号", "编号"],
    "position": ["位置", "部位", "名称", "类型", "分类"],
    "spec": ["直径", "规格", "型号"],
    "single_length": ["单根长", "单长", "每根长"],
    "count": ["根数", "数量", "数 量", "件数"],
    "unit_weight": ["单位重", "理论重量"],
    "total_length": ["总长度", "总长"],
    "weight": ["总重量", "总重", "重量", "质量"],
}

UNIT_RE = re.compile(r"[（(]\s*(mm|cm|m|kg|t)\s*[）)]", re.IGNORECASE)
LENGTH_FACTORS = {"mm": 0.001, "cm": 0.01, "m": 1.0}
MASS_FACTORS = {"kg": 1.0, "t": 1000.0}

TOTALS_RE = re.compile(
    r"(HPB300|HRB335|HRB400|HRB500|RRB400)\s*[:：,，]?\s*(?:总重)?\s*([\d.]+)\s*(kg|Kg|KG|t)"
)

# 每张表的容差 = 标题字高 × 这个系数；标题下方找候选网格线的搜索距离 = 标题字高 × 这个倍数。
TOL_TITLE_HEIGHT_FACTOR = 0.35
SEARCH_DISTANCE_TITLE_HEIGHT_MULTIPLE = 8

# 网格健全性闸门：真实钢筋数量表列数一般 6~12 列，极少超过 15；连通聚合冒出超过 20 列，
# 基本可以判定是吸入了尺寸标注/图框线之类的不相关线段，不是真表格。
MAX_TABLE_COLUMNS = 20
# 表格 bbox 的宽或高超过"标题字高 × 这个倍数"同样判定为聚合异常；300 是按"20 列 × 每列
# 至多 15 倍标题字高"估出来的宽松上限，宽、高共用同一个阈值。
MAX_TABLE_SPAN_TITLE_HEIGHT_MULTIPLE = 300

# 规格解出来的直径必须落在 GB/T 1499 标准公称直径表内，否则大概率是解析错误（比如把
# 牌号名字面量"HRB400"里的"400"当成了直径）——不是真直径就不猜，diameter=None + gap。
_VALID_DIAMETERS_MM = frozenset(load_unit_weights().keys())

# 形似"H + P/R + B + 三位数字"的牌号写法（如 HPB300/HRB400/HRB300），但不在已知牌号
# 列表（EXPLICIT_GRADE_RE）里的，按"未知牌号"记 gap，原文照录，不猜测归入已知牌号。
GRADE_LIKE_RE = re.compile(r"H[PR]B\d{3}")

# 无编号列的表：命中这些关键词的行视为表体结束（合计/总计声明通常就写在这一行）。
BODY_END_KEYWORDS = ("合计", "总计", "总重")
# 表体结束之后，一行里命中表头关键词的格子数 >= 这个数，判定为疑似子表表头。
SUBTABLE_HEADER_MIN_HITS = 2


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    vals = sorted(values)
    n = len(vals)
    mid = n // 2
    return vals[mid] if n % 2 else (vals[mid - 1] + vals[mid]) / 2.0


def _cluster_1d(values: list[float], tol: float) -> list[float]:
    if not values:
        return []
    vals = sorted(values)
    clusters = [[vals[0]]]
    for v in vals[1:]:
        if v - clusters[-1][-1] <= tol:
            clusters[-1].append(v)
        else:
            clusters.append([v])
    return [sum(c) / len(c) for c in clusters]


def _bbox_of(seg: SegmentItem) -> tuple[float, float, float, float]:
    return (min(seg.x1, seg.x2), min(seg.y1, seg.y2), max(seg.x1, seg.x2), max(seg.y1, seg.y2))


def _bbox_overlap(a, b, tol) -> bool:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    return not (ax1 + tol < bx0 or bx1 + tol < ax0 or ay1 + tol < by0 or by1 + tol < ay0)


def _union_bbox(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def _classify_segments(segments: list[SegmentItem], tol: float):
    horiz, vert = [], []
    for s in segments:
        dx, dy = abs(s.x1 - s.x2), abs(s.y1 - s.y2)
        if dy <= tol and dx > tol:
            horiz.append(s)
        elif dx <= tol and dy > tol:
            vert.append(s)
    return horiz, vert


def _match_title(text: str, patterns) -> bool:
    return any(p.search(text) for p in patterns)


def _connects_to_line(vert_seg: SegmentItem, line: SegmentItem, tol: float) -> bool:
    """竖线的某个端点是否落在 line 上（y 对得上 line 的 y，x 落在 line 的 x 范围内，都带容差）。"""
    line_y = (line.y1 + line.y2) / 2
    lx0, lx1 = min(line.x1, line.x2) - tol, max(line.x1, line.x2) + tol
    for vx, vy in ((vert_seg.x1, vert_seg.y1), (vert_seg.x2, vert_seg.y2)):
        if abs(vy - line_y) <= tol and lx0 <= vx <= lx1:
            return True
    return False


def _find_table_grid(
    title: TextItem,
    horiz: list[SegmentItem],
    all_segments: list[SegmentItem],
    tol: float,
    search_distance: float,
    title_height: float,
    used: set,
):
    """在标题下方、搜索距离内的水平线里由近到远逐个试，收集网格后要求结构判据成立
    （≥2 条竖线与候选线相接，且总共 ≥2 条水平线）才接受，否则试下一条。标题下划线、
    分隔短线因为没有竖线相接，会被自然跳过。返回 (topline, region, members) 或 None。

    横向匹配容差 ≤ 1×标题字高（不再用 30×tol 那么宽，避免隔壁表的顶线被误收进候选池）；
    同一水平位置（y 相近）有多条候选线时，优先试线中心离标题 x 最近的那条——多张同版式
    表左右并排、顶线恰好同 y 时，这样才能各自认领自己下方的网格，而不是全部抢第一条。
    已经被别的标题占用的候选线跳过继续试下一条，不直接放弃整张表。
    """
    margin = title_height  # 容差 ≤ 1×标题字高
    candidates = []
    for s in horiz:
        y = (s.y1 + s.y2) / 2
        if y >= title.y - tol:
            continue
        distance = title.y - y
        if distance > search_distance:
            continue
        x0, x1 = min(s.x1, s.x2), max(s.x1, s.x2)
        if x0 - margin <= title.x <= x1 + margin:
            center_x = (x0 + x1) / 2
            candidates.append((distance, abs(center_x - title.x), s))
    # 由近到远；把 y 距离量化到 tol 的整数倍分档，同一档内按线中心离标题 x 最近排序。
    candidates.sort(key=lambda c: (round(c[0] / max(tol, 1e-9)), c[1]))

    for _distance, _dx, cand in candidates:
        if id(cand) in used:
            continue
        region, members = _collect_grid(cand, all_segments, tol)
        horiz_m, vert_m = _classify_segments(members, tol)
        connecting = [v for v in vert_m if _connects_to_line(v, cand, tol)]
        if len(connecting) >= 2 and len(horiz_m) >= 2:
            return cand, region, members
    return None


def _collect_grid(topline: SegmentItem, all_segments: list[SegmentItem], tol: float):
    region = _bbox_of(topline)
    members = [topline]
    remaining = [s for s in all_segments if s is not topline]
    changed = True
    while changed:
        changed = False
        still = []
        for s in remaining:
            b = _bbox_of(s)
            if _bbox_overlap(region, b, tol):
                region = _union_bbox(region, b)
                members.append(s)
                changed = True
            else:
                still.append(s)
        remaining = still
    return region, members


def _locate_band(bounds_asc: list[float], value: float, tol: float) -> int:
    n = len(bounds_asc)
    for j in range(n - 1):
        lo, hi = bounds_asc[j], bounds_asc[j + 1]
        if lo - tol <= value <= hi + tol:
            return j
    return 0 if value < bounds_asc[0] else n - 2


def _extract_unit(text: str) -> Optional[str]:
    m = UNIT_RE.search(text)
    return m.group(1).lower() if m else None


def _classify_header(text: str) -> tuple[Optional[str], Optional[str]]:
    for key in HEADER_KEY_PRIORITY:
        for kw in HEADER_KEYWORDS[key]:
            if kw in text:
                return key, _extract_unit(text)
    return None, _extract_unit(text)


def _first_number(text: str) -> Optional[float]:
    m = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(m.group(0)) if m else None


def _sorted_cell_items(items: list[TextItem]) -> list[TextItem]:
    return sorted(items, key=lambda t: (-t.y, t.x))


def _validate_diameter(diameter_mm: Optional[float], cell_handles: list[str], gaps: list[dict], text: str) -> Optional[float]:
    """直径必须是 GB/T 1499 标准公称直径之一，否则大概率是解析错误，不猜——置空 + gap。"""
    if diameter_mm is None:
        return None
    if diameter_mm not in _VALID_DIAMETERS_MM:
        gaps.append({
            "rule_id": "R005",
            "message": f"规格解出的直径 {diameter_mm:g}mm 不在标准钢筋公称直径表内（原文 {text!r}），按未识别直径处理",
            "handles": cell_handles,
        })
        return None
    return diameter_mm


def _parse_spec_cell(text: str, cell_handles: list[str], symbol_table: SymbolTable, gaps: list[dict]):
    diameter_mm = None
    grade = None
    grade_source = None

    matches = decode_spec(text, symbol_table)
    if matches:
        first = matches[0]
        diameter_mm = first.diameter_mm
        if first.grade:
            grade, grade_source = first.grade, first.grade_source
        else:
            explicit_match = EXPLICIT_GRADE_RE.search(text)
            if explicit_match:
                grade, grade_source = explicit_match.group(0), "explicit"
            else:
                grade_source = "unspecified"
                gaps.append({"rule_id": "R005", "message": f"规格未指明牌号（仅直径）：{text!r}", "handles": cell_handles})
        diameter_mm = _validate_diameter(diameter_mm, cell_handles, gaps, text)
        return diameter_mm, grade, grade_source

    # 符号编码一无所获：可能是纯文字写法——牌号字面量（已知或形似未知）叠加/不叠加单独
    # 写的直径数字。牌号字面量本身的数字（比如"HRB400"里的"400"）绝不能被当成直径，
    # 所以先把命中的牌号 token 从文本里挖掉，再找直径数字。
    explicit_match = EXPLICIT_GRADE_RE.search(text)
    grade_like_match = None if explicit_match else GRADE_LIKE_RE.search(text)
    grade_span = None
    if explicit_match:
        grade, grade_source = explicit_match.group(0), "explicit"
        grade_span = explicit_match.span()
    elif grade_like_match:
        gaps.append({
            "rule_id": "R005",
            "message": f"未知牌号 {grade_like_match.group(0)!r}（原文 {text!r}），原文照录，不猜测归入已知牌号",
            "handles": cell_handles,
        })
        grade_span = grade_like_match.span()

    remainder = text
    if grade_span is not None:
        remainder = text[: grade_span[0]] + text[grade_span[1] :]

    if "%%" in remainder:
        gaps.append({"rule_id": "R005", "message": f"未识别的符号编码：{text!r}", "handles": cell_handles})
    else:
        num = _first_number(remainder)
        if num is not None:
            diameter_mm = num
        elif grade_span is None:
            gaps.append({"rule_id": "R005", "message": f"规格单元格无法解析：{text!r}", "handles": cell_handles})

    diameter_mm = _validate_diameter(diameter_mm, cell_handles, gaps, text)
    return diameter_mm, grade, grade_source


def _parse_row(columns: list[dict], row_cells: dict[int, dict], symbol_table: SymbolTable):
    parsed = {
        "mark": None, "position": None, "grade": None, "grade_source": None, "diameter_mm": None,
        "single_length_m": None, "count": None,
        "total_length_raw": None, "total_length_unit": None, "total_length_m": None,
        "weight_kg": None, "unit_weight_kg_per_m": None,
    }
    gaps: list[dict] = []
    for ci, col in enumerate(columns):
        cell = row_cells.get(ci, {"text": "", "handles": []})
        text = cell["text"].strip()
        key = col["key"]
        if not text or key is None:
            continue
        if key == "mark":
            parsed["mark"] = text
        elif key == "position":
            parsed["position"] = text
        elif key == "spec":
            d, g, gs = _parse_spec_cell(text, cell["handles"], symbol_table, gaps)
            parsed["diameter_mm"], parsed["grade"], parsed["grade_source"] = d, g, gs
        elif key == "single_length":
            v = _first_number(text)
            if v is not None:
                parsed["single_length_m"] = v * LENGTH_FACTORS.get(col["unit_declared"] or "m", 1.0)
        elif key == "count":
            v = _first_number(text)
            if v is not None:
                parsed["count"] = v
        elif key == "total_length":
            v = _first_number(text)
            if v is not None:
                unit = col["unit_declared"] or "m"
                parsed["total_length_raw"] = v
                parsed["total_length_unit"] = unit
                parsed["total_length_m"] = v * LENGTH_FACTORS.get(unit, 1.0)
        elif key == "weight":
            v = _first_number(text)
            if v is not None:
                unit = col["unit_declared"] or "kg"
                parsed["weight_kg"] = v * MASS_FACTORS.get(unit, 1.0)
        elif key == "unit_weight":
            v = _first_number(text)
            if v is not None:
                parsed["unit_weight_kg_per_m"] = v
    return parsed, gaps


def _extract_declared_totals(pool_texts: list[TextItem], tol: float):
    if not pool_texts:
        return []
    y_clusters = _cluster_1d([t.y for t in pool_texts], max(tol, 1e-6))
    lines: dict[int, list[TextItem]] = {}
    for t in pool_texts:
        idx = min(range(len(y_clusters)), key=lambda i: abs(y_clusters[i] - t.y))
        lines.setdefault(idx, []).append(t)
    totals = []
    for items in lines.values():
        items_sorted = sorted(items, key=lambda t: t.x)
        concat = "".join(t.text for t in items_sorted)  # 归一化后的文字，正则匹配用这个
        raw_concat = "".join(t.raw for t in items_sorted)
        handles = [t.handle_path for t in items_sorted]
        for m in TOTALS_RE.finditer(concat):
            grade, value, unit = m.group(1), float(m.group(2)), m.group(3).lower()
            value_kg = value * (1000.0 if unit == "t" else 1.0)
            totals.append({"grade": grade, "value_kg": value_kg, "handles": handles, "text": concat, "raw_text": raw_concat})
    return totals


def _collect_scope_notes(title: TextItem, topline_y: float, layout_texts: list[TextItem], tol: float, x_range):
    """标题和网格顶线之间的注释行。x 必须落在已接受网格的实际 x 范围内（只留一点点 tol
    级别的容差），不能像老版本那样用一个很宽的边距——两张表并排时会把隔壁表的注释也
    收进来。"""
    notes = []
    margin = tol
    lo_x, hi_x = x_range[0] - margin, x_range[1] + margin
    for t in layout_texts:
        if t is title:
            continue
        if topline_y + tol < t.y < title.y - tol and lo_x <= t.x <= hi_x:
            notes.append({"text": t.text, "raw": t.raw, "handles": [t.handle_path]})
    return notes


def _empty_table_result(table_id: str, layout: str, title: TextItem, gap_message: str, extra_handles: list[str] = None) -> dict:
    return {
        "id": table_id,
        "title": title.text,
        "title_handle": title.handle_path,
        "layout": layout,
        "bbox": [title.x, title.y, title.x, title.y],
        "scope_notes": [],
        "columns": [],
        "rows": [],
        "declared_totals": [],
        "gaps": [{"rule_id": "R005", "message": gap_message, "handles": [title.handle_path] + (extra_handles or [])}],
    }


def _build_table(table_id: str, layout: str, title: TextItem, topline: SegmentItem, region, members, layout_texts, tol, symbol_table):
    horiz, vert = _classify_segments(members, tol)
    gaps: list[dict] = []

    result = {
        "id": table_id,
        "title": title.text,
        "title_handle": title.handle_path,
        "layout": layout,
        "bbox": list(region),
        "scope_notes": _collect_scope_notes(title, topline.y1, layout_texts, tol, (region[0], region[2])),
        "columns": [],
        "rows": [],
        "declared_totals": [],
        "gaps": gaps,
    }

    col_bounds = sorted(_cluster_1d([v.x1 for v in vert] + [v.x2 for v in vert], tol))
    row_bounds = sorted(_cluster_1d([h.y1 for h in horiz] + [h.y2 for h in horiz], tol))
    if len(col_bounds) < 2 or len(row_bounds) < 2:
        gaps.append({"rule_id": "R005", "message": "表格网格线不足以确定列/行边界，未能还原结构化表", "handles": [title.handle_path, topline.handle_path]})
        return result

    num_cols = len(col_bounds) - 1
    num_rows = len(row_bounds) - 1

    title_height = title.height if title.height > 1e-6 else (tol / TOL_TITLE_HEIGHT_FACTOR)
    span_limit = MAX_TABLE_SPAN_TITLE_HEIGHT_MULTIPLE * title_height
    bbox_w, bbox_h = region[2] - region[0], region[3] - region[1]
    if num_cols > MAX_TABLE_COLUMNS or bbox_w > span_limit or bbox_h > span_limit:
        gaps.append({
            "rule_id": "R005",
            "message": (
                f"网格连通聚合结果异常（列数 {num_cols}，bbox 宽 {bbox_w:.0f} × 高 {bbox_h:.0f}，"
                f"标题字高 {title_height:.0f}），大概率吸入了不相关线段，未还原为结构化表"
            ),
            "handles": [title.handle_path, topline.handle_path],
        })
        return result

    margin = tol
    texts_in_bbox = [
        t for t in layout_texts
        if region[0] - margin <= t.x <= region[2] + margin and region[1] - margin <= t.y <= region[3] + margin
    ]
    grid: dict[tuple[int, int], list[TextItem]] = {}
    for t in texts_in_bbox:
        ci = _locate_band(col_bounds, t.x, tol)
        band = _locate_band(row_bounds, t.y, tol)
        ri = (num_rows - 1) - band  # 顶部行带 -> row 0
        grid.setdefault((ri, ci), []).append(t)

    columns = []
    for ci in range(num_cols):
        items = _sorted_cell_items(grid.get((0, ci), []))
        header_text = "\n".join(t.text for t in items)
        header_raw_text = "\n".join(t.raw for t in items)
        key, unit = _classify_header(header_text)
        columns.append({
            "key": key,
            "header_text": header_text,
            "header_raw_text": header_raw_text,
            "header_handles": [t.handle_path for t in items],
            "unit_declared": unit,
            "unit_inferred": unit,
        })
    result["columns"] = columns

    mark_col = next((i for i, c in enumerate(columns) if c["key"] == "mark"), None)
    if mark_col is None:
        gaps.append({
            "rule_id": "R005",
            "message": "未识别到编号/钢筋编号列，按内容切分行带：含「合计/总计/总重」的行视为表体结束，之后按备注/合计池处理",
            "handles": [title.handle_path],
        })

    rows = []
    notes_pool: list[TextItem] = []
    body_ended = False  # 只在 mark_col is None 的分支里使用
    subtable_flagged = False
    for ri in range(1, num_rows):
        row_cells: dict[int, dict] = {}
        any_text = False
        for ci in range(num_cols):
            items = _sorted_cell_items(grid.get((ri, ci), []))
            if items:
                any_text = True
            row_cells[ci] = {
                "text": "\n".join(t.text for t in items),
                "raw": "\n".join(t.raw for t in items),
                "handles": [t.handle_path for t in items],
            }
        if not any_text:
            continue

        if mark_col is not None:
            mark_text = row_cells[mark_col]["text"].strip()
            is_data = bool(MARK_RE.match(mark_text)) or (len(mark_text) == 1 and mark_text in CIRCLED_DIGITS)
            if is_data:
                parsed, row_gaps = _parse_row(columns, row_cells, symbol_table)
                rows.append({
                    "cells": [{"col": ci, "text": row_cells[ci]["text"], "raw": row_cells[ci]["raw"], "handles": row_cells[ci]["handles"]} for ci in range(num_cols)],
                    "parsed": parsed,
                })
                gaps.extend(row_gaps)
            else:
                for ci in range(num_cols):
                    notes_pool.extend(grid.get((ri, ci), []))
            continue

        # mark_col is None：按内容切分。含「合计/总计/总重」视为表体结束（这一行本身也
        # 计入结束之后，因为合计声明通常就写在这一行里，要留给 notes_pool 抓）。
        row_texts = [row_cells[ci]["text"] for ci in range(num_cols) if row_cells[ci]["text"]]
        if not body_ended and any(kw in t for t in row_texts for kw in BODY_END_KEYWORDS):
            body_ended = True

        if body_ended:
            if not subtable_flagged:
                header_like_hits = sum(1 for ci in range(num_cols) if _classify_header(row_cells[ci]["text"])[0] is not None)
                if header_like_hits >= SUBTABLE_HEADER_MIN_HITS:
                    row_handles = [h for ci in range(num_cols) for h in row_cells[ci]["handles"]]
                    gaps.append({
                        "rule_id": "R005",
                        "message": "表内含未识别子表（合计之后又出现类似表头的行，未按数据行解析）",
                        "handles": [title.handle_path] + row_handles,
                    })
                    subtable_flagged = True
            for ci in range(num_cols):
                notes_pool.extend(grid.get((ri, ci), []))
        else:
            parsed, row_gaps = _parse_row(columns, row_cells, symbol_table)
            rows.append({
                "cells": [{"col": ci, "text": row_cells[ci]["text"], "raw": row_cells[ci]["raw"], "handles": row_cells[ci]["handles"]} for ci in range(num_cols)],
                "parsed": parsed,
            })
            gaps.extend(row_gaps)

    result["rows"] = rows
    result["declared_totals"] = _extract_declared_totals(notes_pool, tol)
    return result


def find_tables(texts: list[TextItem], segments: list[SegmentItem], symbol_table: SymbolTable, title_patterns=None):
    title_patterns = title_patterns or DEFAULT_TITLE_PATTERNS
    layouts = sorted(set(t.layout for t in texts) | set(s.layout for s in segments))
    tables = []
    seq = 0
    for layout in layouts:
        layout_texts = [t for t in texts if t.layout == layout]
        layout_segments = [s for s in segments if s.layout == layout]
        if not layout_texts or not layout_segments:
            continue
        heights = [t.height for t in layout_texts if t.height > 0]
        layout_tol_fallback = max(0.5 * _median(heights), 1e-6) if heights else 1.0
        # 这一遍分类只用来给"标题下方候选水平线"搜索提供水平线池，精度要求低（真实网格线
        # 严格轴对齐，dy/dx 本就接近 0），用图纸整体的粗略容差即可；每张表自己的容差在下面
        # 按各自标题字高单独算，避免多比例尺混排时一个全局容差顾不上所有表。
        horiz, _vert = _classify_segments(layout_segments, layout_tol_fallback)
        title_items = [t for t in layout_texts if _match_title(t.text, title_patterns)]
        used = set()
        for title in title_items:
            title_height = title.height if title.height > 1e-6 else (layout_tol_fallback / TOL_TITLE_HEIGHT_FACTOR)
            tol = max(TOL_TITLE_HEIGHT_FACTOR * title_height, 1e-6)
            search_distance = SEARCH_DISTANCE_TITLE_HEIGHT_MULTIPLE * title_height
            seq += 1
            found = _find_table_grid(title, horiz, layout_segments, tol, search_distance, title_height, used)
            if found is None:
                tables.append(_empty_table_result(
                    f"T{seq}", layout, title,
                    "标题下方搜索范围内没有找到与 ≥2 条竖线相接、且总共 ≥2 条水平线的合格网格"
                    "（可能只是标题下划线、该标题误匹配、下方根本没有数量表，或候选线全被"
                    "同一布局里别的标题占用了）",
                ))
                continue
            topline, region, members = found
            used.add(id(topline))
            tables.append(_build_table(f"T{seq}", layout, title, topline, region, members, layout_texts, tol, symbol_table))
    return tables
