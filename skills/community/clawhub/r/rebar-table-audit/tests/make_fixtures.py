"""用 ezdxf 合成测试夹具：钢筋数量表（LINE 网格 + 居中对齐 TEXT）。

不使用任何真实客户图纸数据；所有编号/位置/规格/重量都是本文件里现造的数字，
数值关系（R001/R002/R003 是否成立）由调用方在构造 rows 时显式决定。
"""
from __future__ import annotations

import ezdxf
from ezdxf.enums import TextEntityAlignment

COL_WIDTH = 30.0
ROW_HEIGHT = 10.0
HEADER_HEIGHT = 12.0
TOTALS_HEIGHT = 14.0
TEXT_HEIGHT = 3.5

DEFAULT_HEADERS = [
    ["编号"],
    ["位置"],
    ["规格"],
    ["单根长", "(m)"],
    ["根数"],
    ["总长", "(m)"],
    ["重量", "(kg)"],
]


def _add_center_text(space, text, x, y, height=TEXT_HEIGHT):
    t = space.add_text(text, dxfattribs={"height": height})
    t.set_placement((x, y), align=TextEntityAlignment.MIDDLE_CENTER)
    return t


def _add_hline(space, x0, x1, y):
    return space.add_line((x0, y), (x1, y))


def _add_vline(space, x, y0, y1):
    return space.add_line((x, y0), (x, y1))


def build_table(
    space,
    origin=(0.0, 0.0),
    title="钢筋数量表",
    headers=None,
    rows=None,
    totals_lines=None,
    totals_split=None,
    scope_notes=None,
    header_total_unit=None,
    title_underline=False,
    draw_grid=True,
):
    """在 space（modelspace 或某个 block 定义）里画一张表，返回一些关键 handle 供测试断言。

    rows: list[list[str]]，每行长度需与 headers 列数一致。
    totals_lines: list[str]，每条合计声明（如 "HRB400:222.0kg"），按行垛在合计带内。
    totals_split: 可选，list[list[str]]，与 totals_lines 一一对应；给定时表示该条声明要拆成
                  多个 TEXT 对象顺序拼接（用于测试"合计拆成两个文字对象"）。
    header_total_unit: 若不为 None，覆盖"总长"表头里括号内标注的单位文字（用于 R006 夹具）。
    scope_notes: 可选，list[str]，标题和网格之间的注释行（如「(适用于C-C剖面)」「(每延米)」），
                 从上到下按给定顺序摆放，紧贴在网格上方。
    title_underline: True 时在标题下方画两条只有标题宽的短横线（模拟真实图纸的标题下划线，
                     用来验证 topline 选择不会把下划线误判成表格上边框）。
    draw_grid: False 时只画标题（+下划线+注释），不画任何网格线/表头/数据/合计——用来构造
               "标题下面根本没有表格"的反例夹具。
    """
    headers = headers or DEFAULT_HEADERS
    rows = rows or []
    totals_lines = totals_lines or []
    scope_notes = scope_notes or []
    ox, oy = origin
    n_cols = len(headers)
    table_width = n_cols * COL_WIDTH
    title_cx = ox + table_width / 2

    col_x = [ox + i * COL_WIDTH for i in range(n_cols + 1)]
    y_top = oy
    y_header_bottom = y_top - HEADER_HEIGHT
    y_rows = [y_header_bottom - (i + 1) * ROW_HEIGHT for i in range(len(rows))]
    y_last_row_bottom = y_rows[-1] if y_rows else y_header_bottom
    y_bottom = y_last_row_bottom - TOTALS_HEIGHT

    # 从网格顶往上摆：注释（离网格最近）-> 标题下划线 -> 标题。
    cursor = y_top + TEXT_HEIGHT * 1.2
    for note in reversed(scope_notes):
        cursor += TEXT_HEIGHT * 1.5
        _add_center_text(space, note, title_cx, cursor)
    if title_underline:
        cursor += TEXT_HEIGHT * 1.0
        half_width = max(len(title) * TEXT_HEIGHT * 0.65 / 2, TEXT_HEIGHT * 2)
        uy1 = cursor
        uy2 = cursor + TEXT_HEIGHT * 0.35
        _add_hline(space, title_cx - half_width, title_cx + half_width, uy1)
        _add_hline(space, title_cx - half_width, title_cx + half_width, uy2)
        cursor = uy2
    cursor += TEXT_HEIGHT * 1.2
    title_handle = _add_center_text(space, title, title_cx, cursor, height=TEXT_HEIGHT * 1.2).dxf.handle

    if not draw_grid:
        return {
            "title_handle": title_handle,
            "header_handles": [],
            "row_handles": [],
            "totals_handles": [],
            "bbox": None,
        }

    # 外框左右两条竖线贯穿到底（包括合计带），内部分栏竖线只到最后一行数据行为止，
    # 这样合计带才能通过左右边框和上下两条横线与主网格连通。
    _add_vline(space, col_x[0], y_top, y_bottom)
    _add_vline(space, col_x[-1], y_top, y_bottom)
    for x in col_x[1:-1]:
        _add_vline(space, x, y_top, y_header_bottom if not y_rows else y_last_row_bottom)

    _add_hline(space, col_x[0], col_x[-1], y_top)
    _add_hline(space, col_x[0], col_x[-1], y_header_bottom)
    for y in y_rows:
        _add_hline(space, col_x[0], col_x[-1], y)
    _add_hline(space, col_x[0], col_x[-1], y_bottom)

    header_handles = []
    for ci, lines in enumerate(headers):
        cx = (col_x[ci] + col_x[ci + 1]) / 2
        lines_to_draw = list(lines)
        if header_total_unit is not None and lines_to_draw and lines_to_draw[0] in ("总长",):
            lines_to_draw = ["总长", f"({header_total_unit})"]
        if len(lines_to_draw) == 1:
            h = _add_center_text(space, lines_to_draw[0], cx, (y_top + y_header_bottom) / 2)
            header_handles.append(h.dxf.handle)
        else:
            n = len(lines_to_draw)
            band_top, band_bottom = y_top, y_header_bottom
            step = (band_top - band_bottom) / (n + 1)
            for i, line in enumerate(lines_to_draw):
                ly = band_top - step * (i + 1)
                h = _add_center_text(space, line, cx, ly)
                header_handles.append(h.dxf.handle)

    row_handles = []
    for ri, row in enumerate(rows):
        band_top = y_header_bottom - ri * ROW_HEIGHT
        band_bottom = band_top - ROW_HEIGHT
        cy = (band_top + band_bottom) / 2
        cells = []
        for ci, text in enumerate(row):
            cx = (col_x[ci] + col_x[ci + 1]) / 2
            h = _add_center_text(space, text, cx, cy)
            cells.append(h.dxf.handle)
        row_handles.append(cells)

    totals_band_top = y_last_row_bottom
    totals_band_bottom = y_bottom
    n_lines = max(len(totals_lines), 1)
    step = (totals_band_top - totals_band_bottom) / (n_lines + 1)
    totals_handles = []
    for i, line in enumerate(totals_lines):
        ly = totals_band_top - step * (i + 1)
        split = totals_split[i] if totals_split and i < len(totals_split) and totals_split[i] else None
        if split:
            x = col_x[0] + 3.0
            hs = []
            for frag in split:
                h = space.add_text(frag, dxfattribs={"height": TEXT_HEIGHT})
                h.set_placement((x, ly), align=TextEntityAlignment.MIDDLE_LEFT)
                hs.append(h.dxf.handle)
                x += len(frag) * TEXT_HEIGHT * 0.65 + 1.0
            totals_handles.append(hs)
        else:
            cx = col_x[0] + table_width * 0.3
            h = space.add_text(line, dxfattribs={"height": TEXT_HEIGHT})
            h.set_placement((cx, ly), align=TextEntityAlignment.MIDDLE_LEFT)
            totals_handles.append([h.dxf.handle])

    return {
        "title_handle": title_handle,
        "header_handles": header_handles,
        "row_handles": row_handles,
        "totals_handles": totals_handles,
        "bbox": (col_x[0], y_bottom, col_x[-1], y_top),
    }


def new_doc():
    return ezdxf.new(setup=False)


def clean_table_rows():
    # HRB400 直径12：单位重 0.888kg/m（GB 名义值）
    # 编号1：单根长2.500m，根数10，总长25.000m，重量 25*0.888=22.2kg
    return [
        ["1", "顶板", "%%13212", "2.500", "10", "25.000", "22.20"],
        ["2", "底板", "%%13216", "3.000", "5", "15.000", "23.70"],  # d16: 1.578*15=23.67≈23.70 within tol
    ]


def clean_table_totals():
    # 22.20+23.70 = 45.90
    return ["HRB400:45.90kg"]
