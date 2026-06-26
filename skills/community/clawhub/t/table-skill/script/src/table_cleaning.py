"""表格清洗工具。

提供表格清洗功能：移除空白行列、处理复杂表头等。
"""

import pandas as pd
import json
import re
from typing import List


def remove_blank_rows_and_columns(df: pd.DataFrame) -> pd.DataFrame:
    """移除DataFrame开头和结尾的空白行列。

    Args:
        df: 输入DataFrame

    Returns:
        清洗后的DataFrame
    """
    def is_blank(cell):
        if pd.isna(cell):
            return True
        if isinstance(cell, str):
            stripped = cell.strip()
            if stripped == '' or stripped == 'None':
                return True
        return False

    def is_blank_row(row):
        return row.apply(is_blank).all()

    def is_blank_col(col):
        return col.apply(is_blank).all()

    if not df.empty:
        start_row = 0
        while start_row < len(df) and is_blank_row(df.iloc[start_row]):
            start_row += 1

        end_row = len(df) - 1
        while end_row >= 0 and is_blank_row(df.iloc[end_row]):
            end_row -= 1

        if start_row > end_row:
            df = pd.DataFrame()
        else:
            df = df.iloc[start_row:end_row + 1]

    if not df.empty:
        start_col = 0
        while start_col < len(df.columns) and is_blank_col(df.iloc[:, start_col]):
            start_col += 1

        end_col = len(df.columns) - 1
        while end_col >= 0 and is_blank_col(df.iloc[:, end_col]):
            end_col -= 1

        if start_col > end_col:
            df = pd.DataFrame()
        else:
            df = df.iloc[:, start_col:end_col + 1]

    if not df.empty:
        df = df.reset_index(drop=True)

    return df


async def detect_header_row_new(df_head: pd.DataFrame, llm_service=None) -> int:
    """使用LLM检测表头行数。

    Args:
        df_head: 包含前几行的DataFrame
        llm_service: 用于表头检测的LLM服务

    Returns:
        表头行数
    """
    data_str = '\n'.join([
        f"第{i+1}行： " + '; '.join([str(item) for item in df_head.iloc[i][:5]])
        for i in range(len(df_head))
    ])

    prompt = f'''你是一个表格数据处理专家，需要根据表格的前10行内容，智能判断前几行是表头（标题行）。
请遵循以下规则：
1. **表头特征**：表头通常包含列名、字段描述或汇总信息（如"姓名""年龄""总计"等），而非具体数据；即使这些行看起来像是分类说明、标题、或内容重复，也要判定为表头。
2. **对比分析**：检查前几行与后续行的内容差异，表头行通常与其他行格式或语义不同。
3. **疑惑提醒**：即使这些行看起来像是分类说明、标题、或内容重复，也要判定为表头；表头上边的几行一定是表头。
4. **输出格式**：返回一个JSON对象，表头到第几行 "header_row"。

输出示例：
{{"header_row": 2}}

请分析以下表格前10行：

{data_str}

先输出你的解释，再最终输出类似{{"header_row": 2}} 。'''

    for col in df_head.columns:
        df_head[col] = df_head[col].apply(
            lambda x: x.replace(' ', '').replace('\n', '').replace('\r', '')
            if isinstance(x, str) else x
        )

    if llm_service:
        response = await llm_service.chat_async('', prompt)
    else:
        return 1

    print(response)

    try:
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            json_str = match.group(0)
            header_row_num = json.loads(json_str)['header_row']
    except Exception as e:
        print(f"表头检测错误: {e}")
        header_row_num = 1

    print(f'表头行数: {header_row_num}')
    return header_row_num


def flattern_top_n_rows(df_head: pd.DataFrame, header_rows_num: int) -> List[str]:
    """将前N行扁平化为单行表头。

    Args:
        df_head: 包含表头行的DataFrame
        header_rows_num: 表头行数

    Returns:
        扁平化后的列名列表
    """
    column_headers = [
        df_head.iloc[list(range(header_rows_num)), i].tolist()
        for i in range(len(df_head.columns))
    ]

    column_headers = [
        [item.replace(' ', '').replace('\n', '').replace('\r', '')
         if isinstance(item, str) else item for item in column]
        for column in column_headers
    ]

    new_column_headers = []

    for ix_col, col_header in enumerate(column_headers):
        new_col_header = []
        cur_cell = ''

        for ix_row, cell in enumerate(col_header):
            if pd.isna(cell):
                if cur_cell != '':
                    col_header[ix_row] = cur_cell
                else:
                    ix_col_tmp = ix_col - 1
                    while ix_col_tmp >= 0:
                        if pd.isna(column_headers[ix_col_tmp][ix_row]):
                            ix_col_tmp -= 1
                        else:
                            col_header[ix_row] = column_headers[ix_col_tmp][ix_row]
                            new_col_header.append(column_headers[ix_col_tmp][ix_row])
                            break
            else:
                cur_cell = cell
                new_col_header.append(cell)

        new_col_header_no_repeat = [
            new_col_header[i]
            for i in range(len(new_col_header))
            if i == 0 or new_col_header[i] != new_col_header[i-1]
        ]
        new_column_headers.append(new_col_header_no_repeat)

    flattened_header = [
        '-'.join([str(i).strip() for i in item if str(i).strip()])
        for item in new_column_headers
    ]

    return flattened_header


async def merge_top_rows_as_header(df: pd.DataFrame, llm_service=None) -> pd.DataFrame:
    """检测并合并多行表头。

    Args:
        df: 输入DataFrame
        llm_service: 用于表头检测的LLM服务

    Returns:
        合并表头后的DataFrame
    """
    df_head = df.head(10)
    header_rows_num = await detect_header_row_new(df_head, llm_service)

    if header_rows_num == 1:
        df_new = df
    else:
        flattened_header = flattern_top_n_rows(df_head, header_rows_num)
        # 设置合并后的表头为列名
        df.columns = flattened_header
        # 跳过原始表头行，保留数据行
        df_new = df[header_rows_num:].reset_index(drop=True)

    return df_new


async def process_complex_header_table(df: pd.DataFrame, llm_service=None) -> pd.DataFrame:
    """处理复杂表头的表格。

    Args:
        df: 输入DataFrame
        llm_service: 用于表头检测的LLM服务

    Returns:
        处理后的DataFrame
    """
    if df.empty:
        return df

    df = await merge_top_rows_as_header(df, llm_service)
    return df
