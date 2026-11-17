#!/usr/bin/env python3
"""
客诉质量数据分析脚本
功能：解析Excel/CSV文件，识别字段结构，执行客诉统计分析
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd


def analyze_file(file_path, field_mapping=None):
    """
    分析客诉数据文件

    Args:
        file_path: 文件路径（Excel/CSV）
        field_mapping: 字段映射字典，如 {'客户名称': 'customer', '产品型号': 'product'}

    Returns:
        dict: 分析结果
    """
    result = {
        'file_path': file_path,
        'analysis_time': datetime.now().isoformat(),
        'sheets': [],
        'statistics': None
    }

    try:
        # 读取文件
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            sheets = [{'name': 'Sheet1', 'data': df}]
        else:
            # Excel文件，读取所有工作表
            excel_file = pd.ExcelFile(file_path)
            sheets = []
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                sheets.append({'name': sheet_name, 'data': df})
    except Exception as e:
        return {
            'error': f'文件读取失败: {str(e)}',
            'file_path': file_path
        }

    # 分析每个工作表
    for sheet_info in sheets:
        sheet_name = sheet_info['name']
        df = sheet_info['data']

        sheet_result = {
            'name': sheet_name,
            'row_count': len(df),
            'column_count': len(df.columns),
            'fields': [],
            'data_preview': df.head(3).to_dict('records'),
            'missing_values': {}
        }

        # 字段分析
        for col in df.columns:
            field_info = {
                'name': col,
                'type': str(df[col].dtype),
                'non_null_count': df[col].count(),
                'null_count': df[col].isnull().sum(),
                'unique_count': df[col].nunique(),
                'sample_values': df[col].dropna().head(5).tolist()
            }
            sheet_result['fields'].append(field_info)
            sheet_result['missing_values'][col] = df[col].isnull().sum()

        result['sheets'].append(sheet_result)
        # 保存DataFrame引用用于后续统计（不序列化）
        result['_data_cache'] = result.get('_data_cache', [])
        result['_data_cache'].append(df)

    # 如果提供了字段映射，执行统计分析
    if field_mapping and len(result.get('_data_cache', [])) > 0:
        # 使用第一个工作表进行分析（默认）
        df_main = result['_data_cache'][0]
        result['statistics'] = perform_statistics(df_main, field_mapping)
        # 删除数据缓存，避免序列化问题
        del result['_data_cache']

    return result


def perform_statistics(df, field_mapping):
    """
    执行客诉统计分析

    Args:
        df: 数据DataFrame
        field_mapping: 字段映射字典

    Returns:
        dict: 统计结果
    """
    stats = {
        'total_complaints': len(df),
        'issue_type_stats': {},
        'customer_distribution': {},
        'product_distribution': {},
        'high_frequency_issues': [],
        'time_range': {},
        'status_distribution': {}
    }

    # 字段名标准化
    def get_mapped_field(field_name):
        """获取映射后的字段名"""
        for cn_name, en_name in field_mapping.items():
            if en_name == field_name:
                # 尝试在原始列名中找到对应的中文列名
                for col in df.columns:
                    if cn_name in col or col == cn_name:
                        return col
        return None

    # 反向映射：英文字段到实际列名
    mapped_columns = {}
    for cn_name, en_name in field_mapping.items():
        for col in df.columns:
            if cn_name in col or col == cn_name:
                mapped_columns[en_name] = col
                break

    # 1. 按问题类型统计
    issue_type_col = mapped_columns.get('issue_type')
    if issue_type_col:
        issue_counts = df[issue_type_col].value_counts()
        for issue, count in issue_counts.items():
            stats['issue_type_stats'][str(issue)] = {
                'count': int(count),
                'percentage': round(count / len(df) * 100, 2)
            }

    # 2. 按客户分布统计
    customer_col = mapped_columns.get('customer')
    if customer_col:
        customer_counts = df[customer_col].value_counts().head(10)
        stats['customer_distribution'] = {
            str(cust): int(count) for cust, count in customer_counts.items()
        }

    # 3. 按产品分布统计
    product_col = mapped_columns.get('product')
    if product_col:
        product_counts = df[product_col].value_counts().head(10)
        stats['product_distribution'] = {
            str(prod): int(count) for prod, count in product_counts.items()
        }

    # 4. 时间范围分析
    date_col = mapped_columns.get('date')
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        valid_dates = df[date_col].dropna()
        if len(valid_dates) > 0:
            stats['time_range'] = {
                'start_date': valid_dates.min().strftime('%Y-%m-%d'),
                'end_date': valid_dates.max().strftime('%Y-%m-%d'),
                'days_span': (valid_dates.max() - valid_dates.min()).days
            }

    # 5. 按处理状态统计
    status_col = mapped_columns.get('status')
    if status_col:
        status_counts = df[status_col].value_counts()
        stats['status_distribution'] = {
            str(status): int(count) for status, count in status_counts.items()
        }

    # 6. 高频重复问题识别（≥3次）
    desc_col = mapped_columns.get('description')
    if desc_col and issue_type_col:
        # 按问题描述分组统计
        desc_counts = df[desc_col].value_counts()
        high_freq = desc_counts[desc_counts >= 3]
        for desc, count in high_freq.items():
            # 获取该描述对应的客户和问题类型
            matched_rows = df[df[desc_col] == desc]
            issue_type = matched_rows[issue_type_col].mode()[0] if len(matched_rows) > 0 else '未知'
            customer = matched_rows[customer_col].mode()[0] if customer_col and len(matched_rows) > 0 else '未知'

            stats['high_frequency_issues'].append({
                'description': str(desc)[:100],  # 限制长度
                'count': int(count),
                'issue_type': str(issue_type),
                'customer': str(customer)
            })

    return stats


def main():
    parser = argparse.ArgumentParser(description='客诉质量数据分析')
    parser.add_argument('--file_path', required=True, help='客诉数据文件路径（Excel/CSV）')
    parser.add_argument('--field_mapping', help='字段映射，格式："客户名称=customer,产品型号=product"')

    args = parser.parse_args()

    # 解析字段映射
    field_mapping = None
    if args.field_mapping:
        try:
            field_mapping = {}
            for item in args.field_mapping.split(','):
                cn, en = item.strip().split('=')
                field_mapping[cn.strip()] = en.strip()
        except Exception as e:
            print(json.dumps({
                'error': f'字段映射格式错误: {str(e)}',
                'format': '客户名称=customer,产品型号=product,投诉日期=date,问题类型=issue_type,异常描述=description,处理状态=status'
            }, ensure_ascii=False))
            sys.exit(1)

    # 执行分析
    result = analyze_file(args.file_path, field_mapping)

    # 输出JSON结果
    # 转换numpy类型为Python原生类型
    def convert_numpy_types(obj):
        import numpy as np
        if isinstance(obj, dict):
            return {k: convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(item) for item in obj]
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return convert_numpy_types(obj.tolist())
        else:
            return obj

    result = convert_numpy_types(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
