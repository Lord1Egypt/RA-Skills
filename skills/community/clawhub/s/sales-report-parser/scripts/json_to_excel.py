#!/usr/bin/env python3
"""
JSON 转 Excel 表格工具
使用方式: python json_to_excel.py --input input.json --output output.xlsx

参数:
    --input/-i  : 输入 JSON 文件路径
    --output/-o : 输出 Excel 文件路径
    --sheet/-s  : 工作表名称（可选，默认 "Sheet1"）
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd


# 销售报表标准字段
IMAGE_FIELDS = [
    "日期",
    "总销售",
    "产品净销售",
    "现烤面包",
    "袋装面包",
    "软点",
    "西点",
    "中点",
    "蛋糕个数",
    "蛋糕金额",
    "卡劵",
    "交易次数"
]


def parse_date(date_str: str) -> datetime:
    """解析日期字符串"""
    if not date_str or date_str == "无":
        return datetime.min

    formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日", "%m/%d", "%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return datetime.min


def json_to_excel(
    input_path: str,
    output_path: str,
    sheet_name: str = "Sheet1",
    transpose: bool = True,
    sort_by_date: bool = True,
) -> None:
    """
    将 JSON 数据转换为 Excel 表格
    
    参数:
        input_path: 输入 JSON 文件路径
        output_path: 输出 Excel 文件路径
        sheet_name: 工作表名称
        transpose: 是否转置（日期作为列名）
        sort_by_date: 是否按日期排序
    """
    # 读取 JSON 文件
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 处理数据
    if isinstance(data, dict):
        if 'data' in data:
            data = data['data']
        else:
            data = [data]
    elif isinstance(data, list):
        pass
    else:
        data = [data]
    
    if not data:
        print("没有数据可转换")
        sys.exit(1)
    
    # 转换为 DataFrame
    df = pd.DataFrame(data)
    
    # 按日期排序
    if sort_by_date and '日期' in df.columns:
        df['日期_排序'] = df['日期'].apply(parse_date)
        df = df.sort_values('日期_排序')
        df = df.drop(columns=['日期_排序'])
    
    # 重新排列列顺序
    available_columns = [col for col in IMAGE_FIELDS if col in df.columns]
    if available_columns:
        df = df[available_columns]
    
    # 转置（日期作为列名）
    if transpose and '日期' in df.columns:
        df_transposed = df.set_index('日期').T
    else:
        df_transposed = df
    
    # 保存到 Excel
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_transposed.to_excel(writer, sheet_name=sheet_name)
    
    print(f"✓ Excel 文件已保存: {output_path}")
    print(f"\n表格预览:")
    print(df_transposed.to_string())


def main():
    parser = argparse.ArgumentParser(description='JSON 转 Excel 表格工具')
    parser.add_argument('--input', '-i', required=True, help='输入 JSON 文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出 Excel 文件路径')
    parser.add_argument('--sheet', '-s', default='Sheet1', help='工作表名称')
    parser.add_argument('--no-transpose', action='store_true', help='不转置表格')
    parser.add_argument('--no-sort', action='store_true', help='不按日期排序')
    
    args = parser.parse_args()
    
    try:
        json_to_excel(
            input_path=args.input,
            output_path=args.output,
            sheet_name=args.sheet,
            transpose=not args.no_transpose,
            sort_by_date=not args.no_sort,
        )
    except FileNotFoundError:
        print(f"错误: 找不到文件 {args.input}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
