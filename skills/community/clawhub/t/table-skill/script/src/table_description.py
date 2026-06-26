"""表格描述生成工具。

提供表格描述生成功能：列模式、摘要、样本等。
"""

import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional
from io import StringIO
from tabulate import tabulate
import re


def transfer_to_csv_in_memory(df: pd.DataFrame, is_default_header: bool = False) -> pd.DataFrame:
    """在内存中将DataFrame转为CSV并读回。

    处理重复列名并触发pandas类型推断。

    Args:
        df: 输入DataFrame
        is_default_header: 是否使用默认数字表头

    Returns:
        处理后的DataFrame
    """
    # 保存原始列名，用于后续判断是否为有意义的列名
    original_columns = df.columns.tolist()
    has_meaningful_header = not is_default_header and not all(isinstance(c, int) for c in original_columns)

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, header=False, encoding='utf-8')
    csv_buffer.seek(0)

    if not df.empty:
        # 保存时 header=False，所以读取时也用 header=None
        df = pd.read_csv(csv_buffer, on_bad_lines='warn', header=None)

        # 如果有有意义的列名，恢复列名
        if has_meaningful_header and len(original_columns) == len(df.columns):
            df.columns = original_columns

    return df


def sample_from_column(df: pd.DataFrame, col: str, sample_size: int = 10) -> List[Any]:
    """从列中采样，确保覆盖不同类型。

    Args:
        df: 输入DataFrame
        col: 列名
        sample_size: 样本数量

    Returns:
        样本值列表
    """
    types = df[col].apply(type).unique()
    samples = []

    for t in types:
        mask = df[col].apply(lambda x: isinstance(x, t))
        if mask.any():
            sample = df[mask].sample(1)[col].values[0]
            samples.append(sample)

    remaining_size = sample_size - len(samples)
    if remaining_size > 0 and len(df) > len(samples):
        remaining_df = df[~df[col].isin(samples)]
        samples.extend(list(remaining_df.sample(remaining_size)[col]))

    return samples


async def get_table_schema_origin(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """为每列生成模式描述。

    Args:
        df: 输入DataFrame

    Returns:
        列模式字典列表
    """
    columns_list = df.columns.tolist()
    table_schema = []

    for column in columns_list:
        try:
            col_type = df[column].dtypes
            example = None
            type_list = list(df[column].apply(type))
            type_set = set(type_list)

            if len(type_set) == 1:
                if pd.api.types.is_numeric_dtype(col_type):
                    example = {
                        "最小值": df[column].min(),
                        "最大值": df[column].max(),
                        "中位数": df[column].median(),
                        "平均值": df[column].mean()
                    }
                elif pd.api.types.is_datetime64_any_dtype(col_type):
                    example = {
                        "最早日期": df[column].min().strftime('%Y-%m-%d %H:%M:%S'),
                        "最晚日期": df[column].max().strftime('%Y-%m-%d %H:%M:%S')
                    }
                elif pd.api.types.is_object_dtype(col_type):
                    value_counts = df[column].value_counts()
                    if len(value_counts) <= 15:
                        categories = value_counts.index.tolist()
                        example = {"全部类别": categories}
                    else:
                        top_categories = value_counts.nlargest(6).index.tolist()
                        example = {
                            "类别示例": top_categories,
                            "总类别数量": len(value_counts),
                            "说明": "该列类型较多，展示前6个最常见的类型。"
                        }
            else:
                value_counts = df[column].value_counts()
                if len(value_counts) <= 15:
                    categories = value_counts.index.tolist()
                    example = {"全部类别": categories}
                else:
                    sampled_elements = sample_from_column(df, column, sample_size=10)
                    example = {
                        "类别示例": sampled_elements,
                        "总类别数量": len(value_counts),
                        "说明": "该列类型较多，展示10个常见的类型。"
                    }

            table_schema.append({
                "列名": column,
                "数据类型": str(col_type),
                "示例值": example
            })
        except Exception as e:
            print(f"列 {column} 的模式生成错误: {e}")

    return table_schema


async def get_table_abstract(table_schema_des: List[Dict], llm_service=None) -> str:
    """使用LLM生成表格摘要。

    Args:
        table_schema_des: 表格模式描述
        llm_service: 用于生成的LLM服务

    Returns:
        表格摘要字符串
    """
    prompt = f"""请根据我提供的数据表列内容, 对表格整体进行概述，生成表描述。
    表描述解释了该表的主要内容，可能的用途。

    *表格数据如下：*
            -----------------------------
            {table_schema_des}
            -----------------------------
    *返回样例：*
        该表记录了某网站在一段时间内的访客数、浏览量、推广费用、订单数和销售金额等数据，可用于分析网站的运营情况和营销效果。

    注意仅返回表格描述，不输出任何中间解释结果。"""

    if llm_service:
        response = await llm_service.chat_async('你是一个表格内容总结专家。', prompt)
        return response
    else:
        return ""


def df_to_markdown(df: pd.DataFrame) -> str:
    """将DataFrame转为Markdown格式。

    Args:
        df: 输入DataFrame

    Returns:
        Markdown字符串
    """
    md_string = tabulate(df, headers='keys', tablefmt='github', showindex=False)
    md_string = re.sub(r'[ ]+', ' ', md_string)
    return md_string


async def describe_single_table(
    df: pd.DataFrame,
    size_type: str,
    is_abstract: bool = False,
    name: Optional[str] = None,
    llm_service=None
) -> Dict[str, Any]:
    """为表格生成完整描述。

    Args:
        df: 输入DataFrame
        size_type: 'small' 或 'large'
        is_abstract: 是否生成LLM摘要
        name: 表格名称
        llm_service: LLM服务

    Returns:
        表格描述字典
    """
    if df.empty:
        return {}

    table_description = {
        '文件路径': '',
        '表内容': name or '',
        'size_type': size_type,
        '数据行数': len(df),
        '数据列名': list(df.columns)
    }

    if size_type == 'small':
        table_description['context'] = df_to_markdown(df)

    table_schema = await get_table_schema_origin(df)
    table_description['列描述'] = table_schema

    if is_abstract and llm_service:
        table_abstract = await get_table_abstract(table_schema, llm_service)
        table_description['表描述'] = table_abstract

    rows_desc = []
    rows_desc.append({"第0行": df.columns.to_list()})
    for i in range(min(9, df.shape[0])):
        row = df.iloc[i, :].to_list()
        rows_desc.append({"第{}行".format(i + 1): row})
    table_description['这是前10行的数据展示'] = rows_desc

    columns_desc = []
    columns = df.columns.to_list()
    for i in range(df.shape[1]):
        column = [columns[i]] + df.iloc[:4, i].to_list()
        columns_desc.append({"第{}列".format(i): column})
    table_description['这是每列前5行的数据展示'] = columns_desc

    tail_desc = []
    row_num = df.shape[0]
    for i in range(max(0, row_num - 5), row_num):
        row = df.iloc[i, :].to_list()
        tail_desc.append({"第{}行".format(i + 1): row})
    table_description['这是末尾5行的数据展示'] = tail_desc

    return table_description
