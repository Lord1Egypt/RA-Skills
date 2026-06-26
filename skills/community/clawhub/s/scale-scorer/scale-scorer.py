#!/usr/bin/env python3
"""
自动分组量表计分 Skill（支持 CSV / Excel 输入输出）
- 自动识别列名规则：维度前缀 + 末尾数字（如 T1RZTD1, T1RZTD2）
- 按前缀聚合，至少 2 题的组视为一个维度
- 支持反向计分配置文件（JSON）
- 缺失值处理：维度缺失 ≤50% 时用剩余题均值计算，否则结果为 NaN
- 输出：原始列 + 每个维度的均分列（列名为维度前缀）
- 输入支持 .csv / .xlsx，输出默认与输入同格式（可通过 --output 指定）
"""

import pandas as pd
import re
import json
import argparse
import sys
import os


def auto_group_columns(df, min_items=2):
    """自动将列按前缀分组，仅保留符合规则且题目数≥min_items的组"""
    groups = {}
    for col in df.columns:
        base = re.sub(r'\d+$', '', str(col).strip())
        if base and base != str(col).strip():  # 至少去掉了一个末尾数字
            groups.setdefault(base, []).append(str(col))
    return {k: v for k, v in groups.items() if len(v) >= min_items}


def load_reverse_items(config_path):
    """从 JSON 文件加载需反向计分的列名列表"""
    if not config_path or not os.path.exists(config_path):
        return []
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config.get('reverse_items', [])


def reverse_score(series, min_val, max_val):
    """反向计分公式：新值 = (最小值 + 最大值) - 原值"""
    return (min_val + max_val) - series


def compute_dimension_scores(df, groups, reverse_items,
                             min_val=1, max_val=5, missing_threshold=0.5):
    """
    计算各维度均分，添加到 df 最右侧。
    返回处理后的 DataFrame，列序：原始列 + 各维度列（按 groups 顺序）
    """
    df = df.copy()
    original_cols = df.columns.tolist()
    for dim, cols in groups.items():
        dim_data = df[cols].apply(pd.to_numeric, errors='coerce')
        for col in cols:
            if col in reverse_items:
                dim_data[col] = reverse_score(dim_data[col], min_val, max_val)
        missing_ratio = dim_data.isnull().sum(axis=1) / len(cols)
        mean_series = dim_data.mean(axis=1, skipna=True)
        mean_series[missing_ratio > missing_threshold] = float('nan')
        df[dim] = mean_series
    new_cols = original_cols + list(groups.keys())
    return df[new_cols]


def read_data(filepath, encoding='utf-8'):
    """根据扩展名读取 CSV 或 Excel 文件"""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ('.xlsx', '.xls'):
        return pd.read_excel(filepath)
    else:
        # 默认按 CSV 处理
        return pd.read_csv(filepath, encoding=encoding)


def write_data(df, filepath, encoding='utf-8-sig'):
    """根据扩展名写入 CSV 或 Excel 文件"""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ('.xlsx', '.xls'):
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        df.to_excel(filepath, index=False)
    else:
        df.to_csv(filepath, index=False, encoding=encoding)


def main():
    parser = argparse.ArgumentParser(description='自动分组量表计分（支持 CSV/Excel）')
    parser.add_argument('input', help='输入的 CSV 或 Excel 文件路径')
    parser.add_argument('--output', '-o', default=None,
                        help='输出文件路径（默认在输入文件名后加 _scored，保持同格式）')
    parser.add_argument('--reverse', '-r', default=None,
                        help='反向计分配置文件（JSON），包含 "reverse_items" 列表')
    parser.add_argument('--min', type=float, default=1, help='量表最小值（默认1）')
    parser.add_argument('--max', type=float, default=5, help='量表最大值（默认5）')
    parser.add_argument('--min-items', type=int, default=2,
                        help='自动分组时每组最少题目数（默认2）')
    parser.add_argument('--encoding', default='utf-8',
                        help='CSV 文件编码（默认utf-8）')
    args = parser.parse_args()

    # 读取数据
    try:
        df = read_data(args.input, encoding=args.encoding)
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)

    # 自动分组
    groups = auto_group_columns(df, min_items=args.min_items)
    if not groups:
        print("未找到任何符合规则的维度（前缀+数字，且至少包含2题）。程序退出。")
        sys.exit(1)
    print(f"自动识别到 {len(groups)} 个维度：")
    for dim, cols in groups.items():
        print(f"  {dim}: {cols}")

    # 加载反向计分
    reverse_items = load_reverse_items(args.reverse)
    if reverse_items:
        print(f"已加载反向计分题目: {reverse_items}")

    # 计算维度均分
    result_df = compute_dimension_scores(df, groups, reverse_items,
                                         min_val=args.min,
                                         max_val=args.max)

    # 确定输出路径
    if args.output is None:
        base, ext = os.path.splitext(args.input)
        # 输入是什么扩展名，输出就保持相同
        output_path = f"{base}_scored{ext}"
    else:
        output_path = args.output

    # 写入文件
    try:
        write_data(result_df, output_path)
        print(f"\n计分完成，结果已保存至: {output_path}")
    except Exception as e:
        print(f"写入文件失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()