"""表格分割与Excel处理工具。

提供表格按空行分割、Excel工作表处理等功能。
"""

import pandas as pd
from typing import List, Tuple


def _cell_is_empty(v) -> bool:
    """检查单元格是否为空。"""
    if v is None:
        return True
    s = str(v).strip()
    return (s == "") or (s.lower() == "nan")


def preprocess_merge_spire(sheet):
    """填充合并单元格并取消合并（Spire工作表）。

    Args:
        sheet: Spire工作表对象
    """
    merged_ranges = list(sheet.MergedCells)

    for rng in merged_ranges:
        value = rng.Value
        for r in range(rng.Row, rng.Row + rng.RowCount):
            for c in range(rng.Column, rng.Column + rng.ColumnCount):
                sheet.Range[r, c].Value = value
        rng.UnMerge()


def find_blocks_by_empty_rows(sheet) -> Tuple[List[Tuple[int, int]], int, int]:
    """查找被空行分隔的数据块。

    Args:
        sheet: Spire工作表

    Returns:
        (blocks, start_col, end_col)元组
    """
    used = sheet.AllocatedRange
    sr, sc = used.Row, used.Column
    nrows, ncols = used.RowCount, used.ColumnCount
    er = sr + nrows - 1
    ec = sc + ncols - 1

    blocks, start = [], None
    for r in range(sr, sr + nrows):
        row_vals = [sheet.Range[r, c].Value for c in range(sc, sc + ncols)]
        is_empty = all(_cell_is_empty(v) for v in row_vals)
        if is_empty:
            if start is not None:
                blocks.append((start, r - 1))
                start = None
        else:
            if start is None:
                start = r
    if start is not None:
        blocks.append((start, er))
    return blocks, sc, ec


def crop_sheet_to_block(ws, start_row: int, end_row: int, start_col: int, end_col: int):
    """裁剪工作表到指定块范围。

    Args:
        ws: Spire工作表
        start_row: 起始行
        end_row: 结束行
        start_col: 起始列
        end_col: 结束列
    """
    used = ws.AllocatedRange
    cur_sr, cur_er = used.Row, used.Row + used.RowCount - 1
    cur_sc, cur_ec = used.Column, used.Column + used.ColumnCount - 1

    if end_row < cur_er:
        ws.DeleteRow(end_row + 1, cur_er - end_row)
    if start_row > cur_sr:
        ws.DeleteRow(cur_sr, start_row - cur_sr)

    used = ws.AllocatedRange
    cur_sc, cur_ec = used.Column, used.Column + used.ColumnCount - 1
    if end_col < cur_ec:
        ws.DeleteColumn(end_col + 1, cur_ec - end_col)

    used = ws.AllocatedRange
    cur_sc = used.Column
    if start_col > cur_sc:
        ws.DeleteColumn(cur_sc, start_col - cur_sc)


def split_workbook_all_sheets_return_worksheets(src_path: str) -> List:
    """按工作表和空行块分割工作簿。

    Args:
        src_path: Excel文件路径

    Returns:
        Spire工作表列表
    """
    import spire.xls as xls

    src_wb = xls.Workbook()
    src_wb.LoadFromFile(src_path)

    ws_list = []
    for si in range(src_wb.Worksheets.Count):
        src_ws = src_wb.Worksheets[si]
        preprocess_merge_spire(src_ws)
        blocks, sc, ec = find_blocks_by_empty_rows(src_ws)

        if not blocks:
            out_wb = xls.Workbook()
            out_wb.Worksheets.Clear()
            new_ws = out_wb.Worksheets.AddCopy(src_ws)
            new_ws.Name = f"{src_ws.Name}"
            ws_list.append(new_ws)
            continue

        for i, (sr, er) in enumerate(blocks, 1):
            out_wb = xls.Workbook()
            out_wb.Worksheets.Clear()
            new_ws = out_wb.Worksheets.AddCopy(src_ws)
            crop_sheet_to_block(new_ws, sr, er, sc, ec)
            new_ws.Name = f"{src_ws.Name}_{i}"
            ws_list.append(new_ws)

    return ws_list


def preprocess_merge(ws):
    """预处理openpyxl工作表的合并单元格。

    Args:
        ws: openpyxl工作表
    """
    for merged_range in list(ws.merged_cells.ranges):
        min_row, min_col, max_row, max_col = (
            merged_range.min_row, merged_range.min_col,
            merged_range.max_row, merged_range.max_col
        )
        value = ws.cell(row=min_row, column=min_col).value
        ws.unmerge_cells(str(merged_range))
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                ws.cell(row=r, column=c).value = value


def ws_to_df(ws) -> pd.DataFrame:
    """将 openpyxl 工作表转换为 DataFrame。

    Args:
        ws: openpyxl 工作表

    Returns:
        DataFrame
    """
    data = list(ws.iter_rows(values_only=True))
    return pd.DataFrame(data)


def split_df_by_blank_rows(df: pd.DataFrame, filename: str) -> Tuple[List[pd.DataFrame], List[str]]:
    """按空行分割 DataFrame。

    Args:
        df: 输入 DataFrame
        filename: 基础文件名

    Returns:
        (tables, filenames) 元组
    """
    tables = []
    filenames = []
    current_table = []

    df_str = df.astype(str)
    empty_mask = (df_str == 'nan') | (df_str == 'None') | (df_str == '') | df_str.isnull()
    empty_rows = empty_mask.all(axis=1)

    for idx, row in df.iterrows():
        if empty_rows[idx]:
            if current_table:
                table_df = pd.DataFrame(current_table).dropna(how="all")
                if not table_df.empty:
                    tables.append(table_df)
                current_table = []
        else:
            current_table.append(row.tolist())

    if current_table:
        table_df = pd.DataFrame(current_table).dropna(how="all")
        if not table_df.empty:
            tables.append(table_df)

    if len(tables) == 1:
        filenames = [filename]
    else:
        for ix, table in enumerate(tables):
            first_row = table.iloc[0, :]
            non_empty = [cell for cell in first_row if cell is not None and str(cell).strip() != ""]

            if len(non_empty) == 1:
                table_title = str(non_empty[0]).strip()
                filenames.append(f"{filename}_{table_title}")
                tables[ix] = table.iloc[1:]
            else:
                filenames.append(f"{filename}_{ix + 1}")

    return tables, filenames


def preprocess_merge_xlrd(sheet):
    """预处理xlrd工作表的合并单元格。

    Args:
        sheet: xlrd工作表

    Yields:
        (row, col, value)元组
    """
    for (rlo, rhi, clo, chi) in sheet.merged_cells:
        value = sheet.cell_value(rlo, clo)
        for r in range(rlo, rhi):
            for c in range(clo, chi):
                yield (r, c, value)


def preprocess_excel(sheet, remove_chars: List[str], standard_style=None) -> pd.DataFrame:
    """预处理 Excel 工作表：转换单元格类型并填充合并单元格。

    Args:
        sheet: Spire 工作表
        remove_chars: 需要移除的字符
        standard_style: 标准样式模板

    Returns:
        处理后的 DataFrame

    Note:
        该函数会修改 sheet 对象（取消合并单元格并填充值）。
        如果重复执行，第二次执行时 sheet 已经被修改过，合并单元格已被展开，
        所以不会再有变化。但会重新处理单元格类型转换。
    """
    from spire.xls import Workbook

    if standard_style is None:
        import os
        # 尝试从 skills 目录加载模板
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_path = os.path.join(script_dir, '2012 最新版土地开发整理项目人工预算单价计算表.xls')
        workbook_template = Workbook()
        if os.path.exists(template_path):
            workbook_template.LoadFromFile(template_path)
            standard_style = workbook_template.Worksheets[0]['A1'].Style

    matrix = []
    for row in sheet.Rows:
        new_row = []
        for cell in row:
            try:
                displayed_text = cell.DisplayedText.strip()
            except:
                if standard_style:
                    cell.Style = standard_style
                displayed_text = cell.DisplayedText.strip()

            displayed_text_new = displayed_text
            percentage_flag = False

            for remove_char in remove_chars:
                if remove_char == '%' and displayed_text_new.endswith('%'):
                    percentage_flag = True
                displayed_text_new = displayed_text_new.replace(remove_char, '')

            try:
                if percentage_flag:
                    value = int(displayed_text_new) / 100
                else:
                    value = int(displayed_text_new)
                new_row.append(value)
                continue
            except ValueError:
                pass

            try:
                if percentage_flag:
                    value = float(displayed_text_new) / 100
                else:
                    value = float(displayed_text_new)
                new_row.append(value)
                continue
            except ValueError:
                pass

            new_row.append(displayed_text)
        matrix.append(new_row)

    try:
        for cellrange in sheet.MergedCells:
            min_row = cellrange.Row - 1
            min_col = cellrange.Column - 1
            max_row = cellrange.LastRow - 1
            max_col = cellrange.LastColumn - 1
            start_text = cellrange.DisplayedText

            for row in range(min_row, max_row + 1):
                for col in range(min_col, max_col + 1):
                    if row == min_row and col == min_col:
                        continue
                    matrix[row - sheet.FirstRow + 1][col - sheet.FirstColumn + 1] = start_text
    except Exception as e:
        print(f"填充合并单元格警告：{e}")

    return pd.DataFrame(matrix)


def process_csv(df: pd.DataFrame, remove_chars: List[str]) -> pd.DataFrame:
    """预处理 CSV DataFrame：移除指定字符并转换数值类型。

    与 preprocess_excel 的核心逻辑一致，但适用于 CSV 格式输入。
    由于 CSV 无合并单元格，不处理该部分。

    Args:
        df: 输入 DataFrame（从 CSV 读取）
        remove_chars: 需要移除的字符列表，如 [','] 移除千分位逗号

    Returns:
        处理后的 DataFrame
    """
    if df.empty:
        return df

    result_df = df.copy()

    for col in result_df.columns:
        col_values = []
        for cell in result_df[col]:
            if pd.isna(cell):
                col_values.append(cell)
                continue

            cell_str = str(cell).strip()
            percentage_flag = False

            for remove_char in remove_chars:
                if remove_char == '%' and cell_str.endswith('%'):
                    percentage_flag = True
                cell_str = cell_str.replace(remove_char, '')

            if percentage_flag:
                try:
                    col_values.append(float(cell_str) / 100)
                    continue
                except ValueError:
                    pass

            try:
                if '.' in cell_str:
                    col_values.append(float(cell_str))
                else:
                    col_values.append(int(cell_str))
            except ValueError:
                col_values.append(cell)

        result_df[col] = col_values

    return result_df
