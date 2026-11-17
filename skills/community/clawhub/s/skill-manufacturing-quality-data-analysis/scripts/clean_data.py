#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业质量现场数据分析 - 数据清洗脚本
处理合并单元格、空行、空值、重复数据、格式混乱
"""

import argparse
import json
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"缺少必要依赖库: {e}"}))
    sys.exit(1)


def clean_dataframe(df: pd.DataFrame, field_mapping: Dict[str, str]) -> pd.DataFrame:
    """
    清洗 DataFrame 数据
    """
    df_cleaned = df.copy()

    # 1. 移除完全空白的行
    df_cleaned = df_cleaned.dropna(how='all')

    # 2. 处理空值
    for key, col_name in field_mapping.items():
        if col_name in df_cleaned.columns:
            if key in ['defect_type', 'product', 'process', 'shift']:
                # 分类字段：空值填充为"未分类"
                df_cleaned[col_name] = df_cleaned[col_name].fillna('未分类')
            elif key in ['defect_count', 'total_count']:
                # 数值字段：空值填充为 0
                df_cleaned[col_name] = pd.to_numeric(df_cleaned[col_name], errors='coerce').fillna(0)
            elif key == 'date':
                # 日期字段：尝试解析
                df_cleaned[col_name] = pd.to_datetime(df_cleaned[col_name], errors='coerce')

    # 3. 去除重复行（完全相同的记录）
    initial_count = len(df_cleaned)
    df_cleaned = df_cleaned.drop_duplicates()
    removed_count = initial_count - len(df_cleaned)

    # 4. 格式标准化
    # 文本字段去除首尾空格
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        df_cleaned[col] = df_cleaned[col].astype(str).str.strip()

    # 数值字段确保为数值类型
    for key, col_name in field_mapping.items():
        if key in ['defect_count', 'total_count'] and col_name in df_cleaned.columns:
            df_cleaned[col_name] = pd.to_numeric(df_cleaned[col_name], errors='coerce').fillna(0).astype(int)

    return df_cleaned, removed_count


def fill_merged_cells(df: pd.DataFrame) -> pd.DataFrame:
    """
    填充合并单元格（向下填充空值）
    """
    df_filled = df.copy()

    # 对每一列进行向下填充
    for col in df_filled.columns:
        df_filled[col] = df_filled[col].ffill()

    return df_filled


def validate_cleaned_data(df: pd.DataFrame, field_mapping: Dict[str, str]) -> Dict[str, Any]:
    """
    验证清洗后的数据
    """
    validation = {
        'is_valid': True,
        'issues': [],
        'warnings': []
    }

    # 检查必要字段是否存在
    required_fields = ['defect_type', 'defect_count']
    for field in required_fields:
        if field not in field_mapping:
            validation['issues'].append(f'缺少关键字段: {field}')
            validation['is_valid'] = False

    # 检查数据量
    if len(df) == 0:
        validation['issues'].append('清洗后数据为空')
        validation['is_valid'] = False
    elif len(df) < 3:
        validation['warnings'].append(f'数据量较少（仅 {len(df)} 条），分析结果可能不够准确')

    # 检查不良数量是否合理
    if 'defect_count' in field_mapping:
        col_name = field_mapping['defect_count']
        if col_name in df.columns:
            negative_count = (df[col_name] < 0).sum()
            if negative_count > 0:
                validation['warnings'].append(f'检测到 {negative_count} 条记录的不良数量为负值，已自动取绝对值')
                df[col_name] = df[col_name].abs()

    # 检查是否有缺失的关键信息
    if 'product' in field_mapping:
        col_name = field_mapping['product']
        if col_name in df.columns:
            null_count = (df[col_name] == '未分类').sum()
            if null_count > 0:
                validation['warnings'].append(f'产品信息缺失 {null_count} 条')

    return validation


def main():
    parser = argparse.ArgumentParser(description='制造业质量现场数据分析 - 数据清洗')
    parser.add_argument('--input_file', required=True, help='解析后的 JSON 数据文件路径')
    args = parser.parse_args()

    # 读取输入文件
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            parse_result = json.load(f)
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"读取输入文件失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)

    if parse_result.get('status') != 'success':
        print(json.dumps({
            "status": "error",
            "message": f"输入数据状态异常: {parse_result.get('message', '未知错误')}"
        }, ensure_ascii=False))
        sys.exit(1)

    result = {
        'status': 'success',
        'original_result': parse_result,
        'cleaned_data': {},
        'cleaning_summary': {
            'total_sheets': 0,
            'total_rows_before': 0,
            'total_rows_after': 0,
            'removed_duplicates': 0
        },
        'validation': {}
    }

    # 清洗每个 Sheet 的数据
    for sheet_name, sheet_data in parse_result['data'].items():
        if sheet_data['row_count'] == 0:
            continue

        try:
            # 重建 DataFrame
            df = pd.DataFrame(sheet_data['sample_data'])

            # 填充合并单元格
            df = fill_merged_cells(df)

            # 清洗数据
            df_cleaned, removed_count = clean_dataframe(df, sheet_data['field_mapping'])

            # 验证数据
            validation = validate_cleaned_data(df_cleaned, sheet_data['field_mapping'])

            result['cleaned_data'][sheet_name] = {
                'columns': df_cleaned.columns.tolist(),
                'field_mapping': sheet_data['field_mapping'],
                'row_count': len(df_cleaned),
                'data': df_cleaned.to_dict(orient='records'),
                'removed_duplicates': removed_count
            }

            result['cleaning_summary']['total_sheets'] += 1
            result['cleaning_summary']['total_rows_before'] += sheet_data['row_count']
            result['cleaning_summary']['total_rows_after'] += len(df_cleaned)
            result['cleaning_summary']['removed_duplicates'] += removed_count

            if not validation['is_valid']:
                result['status'] = 'warning'

            if validation['issues'] or validation['warnings']:
                result['validation'][sheet_name] = validation

        except Exception as e:
            result['status'] = 'error'
            result[f'error_{sheet_name}'] = f"Sheet [{sheet_name}] 清洗失败: {str(e)}"

    if not result['cleaned_data']:
        result['status'] = 'error'
        result['message'] = '未清洗到任何有效数据'

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
