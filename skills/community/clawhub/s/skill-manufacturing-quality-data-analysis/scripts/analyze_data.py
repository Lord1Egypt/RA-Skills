#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业质量现场数据分析 - 数据分析脚本
不良类型分类统计、按工序/班次/产品拆分、TOP3 高频不良筛选（二八原则）
"""

import argparse
import json
import sys
from typing import Dict, List, Any
from collections import defaultdict

try:
    import pandas as pd
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"缺少必要依赖库: {e}"}))
    sys.exit(1)


def analyze_defect_types(df: pd.DataFrame, field_mapping: Dict[str, str]) -> Dict[str, Any]:
    """
    不良类型分类统计
    """
    analysis = {
        'defect_type_stats': [],
        'total_defect_count': 0,
        'unique_defect_types': 0
    }

    if 'defect_type' not in field_mapping or 'defect_count' not in field_mapping:
        return analysis

    defect_type_col = field_mapping['defect_type']
    defect_count_col = field_mapping['defect_count']

    # 按不良类型分组统计
    group_stats = df.groupby(defect_type_col)[defect_count_col].agg(['sum', 'count']).reset_index()
    group_stats.columns = ['defect_type', 'total_count', 'record_count']
    group_stats = group_stats.sort_values('total_count', ascending=False)

    total_defect_count = group_stats['total_count'].sum()
    analysis['total_defect_count'] = int(total_defect_count)
    analysis['unique_defect_types'] = len(group_stats)

    # 计算占比
    group_stats['percentage'] = (group_stats['total_count'] / total_defect_count * 100).round(2)

    # 转换为列表
    analysis['defect_type_stats'] = group_stats.to_dict(orient='records')

    return analysis


def analyze_by_dimension(df: pd.DataFrame, field_mapping: Dict[str, str], dimension: str) -> List[Dict[str, Any]]:
    """
    按指定维度（工序/班次/产品）拆分分析
    """
    if dimension not in field_mapping or 'defect_count' not in field_mapping:
        return []

    dim_col = field_mapping[dimension]
    defect_count_col = field_mapping['defect_count']

    # 按维度分组统计
    group_stats = df.groupby(dim_col)[defect_count_col].sum().reset_index()
    group_stats.columns = [dimension, 'total_defect_count']
    group_stats = group_stats.sort_values('total_defect_count', ascending=False)

    # 计算占比
    total = group_stats['total_defect_count'].sum()
    group_stats['percentage'] = (group_stats['total_defect_count'] / total * 100).round(2)

    return group_stats.to_dict(orient='records')


def calculate_top3_defects(defect_type_stats: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    筛选 TOP3 高频不良问题（二八原则）
    """
    if not defect_type_stats:
        return {
            'top3': [],
            'accumulated_percentage': 0,
            'pareto_principle_applied': False
        }

    # 按不良数量排序
    sorted_stats = sorted(defect_type_stats, key=lambda x: x['total_count'], reverse=True)

    # 取前 3
    top3 = sorted_stats[:3]

    # 计算累积占比
    total_count = sum(item['total_count'] for item in sorted_stats)
    top3_count = sum(item['total_count'] for item in top3)
    accumulated_percentage = round(top3_count / total_count * 100, 2) if total_count > 0 else 0

    return {
        'top3': top3,
        'accumulated_percentage': accumulated_percentage,
        'pareto_principle_applied': accumulated_percentage >= 80
    }


def calculate_overview(df: pd.DataFrame, field_mapping: Dict[str, str]) -> Dict[str, Any]:
    """
    计算数据概览
    """
    overview = {
        'total_inspection_count': 0,
        'total_defect_count': 0,
        'overall_defect_rate': 0.0
    }

    # 计算总检验数
    if 'total_count' in field_mapping:
        total_count_col = field_mapping['total_count']
        overview['total_inspection_count'] = int(df[total_count_col].sum())
    elif 'defect_count' in field_mapping:
        # 如果没有总数字段，尝试用记录数估计
        overview['total_inspection_count'] = len(df)

    # 计算总不良数
    if 'defect_count' in field_mapping:
        defect_count_col = field_mapping['defect_count']
        overview['total_defect_count'] = int(df[defect_count_col].sum())

    # 计算整体不良率
    if overview['total_inspection_count'] > 0:
        overview['overall_defect_rate'] = round(
            overview['total_defect_count'] / overview['total_inspection_count'] * 100, 2
        )

    return overview


def main():
    parser = argparse.ArgumentParser(description='制造业质量现场数据分析 - 数据分析')
    parser.add_argument('--input_file', required=True, help='清洗后的 JSON 数据文件路径')
    args = parser.parse_args()

    # 读取输入文件
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            clean_result = json.load(f)
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"读取输入文件失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)

    if 'cleaned_data' not in clean_result:
        print(json.dumps({
            "status": "error",
            "message": "输入文件格式错误，缺少 cleaned_data"
        }, ensure_ascii=False))
        sys.exit(1)

    result = {
        'status': 'success',
        'analysis_result': {},
        'summary': {
            'overview': {},
            'top3_defects': {},
            'recommendation_priority': []
        }
    }

    # 合并所有 Sheet 的数据进行分析
    all_data = []
    global_field_mapping = {}

    for sheet_name, sheet_data in clean_result['cleaned_data'].items():
        if sheet_data['row_count'] == 0:
            continue

        df = pd.DataFrame(sheet_data['data'])
        all_data.append(df)
        global_field_mapping.update(sheet_data['field_mapping'])

    if not all_data:
        print(json.dumps({
            "status": "error",
            "message": "无有效数据可供分析"
        }, ensure_ascii=False))
        sys.exit(1)

    # 合并所有数据
    combined_df = pd.concat(all_data, ignore_index=True)

    # 1. 数据概览
    overview = calculate_overview(combined_df, global_field_mapping)
    result['summary']['overview'] = overview

    # 2. 不良类型分类统计
    defect_analysis = analyze_defect_types(combined_df, global_field_mapping)
    result['analysis_result']['defect_type_analysis'] = defect_analysis

    # 3. TOP3 高频不良
    top3_result = calculate_top3_defects(defect_analysis['defect_type_stats'])
    result['summary']['top3_defects'] = top3_result

    # 4. 按维度拆分分析
    dimensions = ['process', 'shift', 'product']
    for dim in dimensions:
        dim_analysis = analyze_by_dimension(combined_df, global_field_mapping, dim)
        if dim_analysis:
            result['analysis_result'][f'{dim}_analysis'] = dim_analysis

    # 5. 生成整改优先级建议（基于 TOP3 不良）
    if top3_result['top3']:
        result['summary']['recommendation_priority'] = [
            {
                'rank': i + 1,
                'defect_type': item['defect_type'],
                'defect_count': item['total_count'],
                'percentage': item['percentage'],
                'priority': '高' if i == 0 else ('中' if i == 1 else '低')
            }
            for i, item in enumerate(top3_result['top3'])
        ]

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
