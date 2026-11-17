#!/usr/bin/env python3
"""
质量数据分析导入导出脚本
支持CSV、Excel格式的数据读写
"""

import argparse
import json
import sys
import os
from typing import List, Dict, Any, Optional, Union
import numpy as np


def load_csv(file_path: str, column: Optional[str] = None, has_header: bool = True) -> Dict[str, Any]:
    """
    加载CSV文件
    
    参数:
        file_path: 文件路径
        column: 指定列名
        has_header: 是否有表头
    
    返回:
        数据字典
    """
    import pandas as pd
    
    if has_header:
        df = pd.read_csv(file_path)
    else:
        df = pd.read_csv(file_path, header=None)
        # 为列命名
        df.columns = [f'column_{i}' for i in range(df.shape[1])]
    
    result = {
        "file_path": file_path,
        "rows": len(df),
        "columns": list(df.columns),
        "column_count": len(df.columns)
    }
    
    if column:
        if column in df.columns:
            result["selected_column"] = column
            result["data"] = df[column].dropna().tolist()
        else:
            result["error"] = f"Column '{column}' not found"
            result["available_columns"] = list(df.columns)
    else:
        # 返回所有列
        result["data"] = {col: df[col].dropna().tolist() for col in df.columns}
    
    return result


def load_excel(file_path: str, column: Optional[str] = None, sheet_name: Optional[str] = None) -> Dict[str, Any]:
    """
    加载Excel文件
    
    参数:
        file_path: 文件路径
        column: 指定列名
        sheet_name: 工作表名称
    
    返回:
        数据字典
    """
    import pandas as pd
    
    if sheet_name:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        df = pd.read_excel(file_path)
    
    result = {
        "file_path": file_path,
        "rows": len(df),
        "columns": list(df.columns),
        "column_count": len(df.columns)
    }
    
    if column:
        if column in df.columns:
            result["selected_column"] = column
            result["data"] = df[column].dropna().tolist()
        else:
            result["error"] = f"Column '{column}' not found"
            result["available_columns"] = list(df.columns)
    else:
        result["data"] = {col: df[col].dropna().tolist() for col in df.columns}
    
    return result


def export_to_csv(data: Union[List, Dict], output_path: str, columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    导出数据到CSV
    
    参数:
        data: 数据(列表或字典)
        output_path: 输出路径
        columns: 列名列表
    
    返回:
        操作结果
    """
    import pandas as pd
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if isinstance(data, dict):
        df = pd.DataFrame(data)
    elif isinstance(data, list):
        if columns and len(columns) == len(data[0]) if data else False:
            df = pd.DataFrame(data, columns=columns)
        else:
            df = pd.DataFrame(data)
    else:
        return {"error": "Unsupported data format"}
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    return {
        "output_path": output_path,
        "rows": len(df),
        "columns": list(df.columns),
        "status": "success"
    }


def export_to_excel(data: Union[List, Dict], output_path: str, columns: Optional[List[str]] = None,
                     sheet_name: str = "Sheet1") -> Dict[str, Any]:
    """
    导出数据到Excel
    
    参数:
        data: 数据(列表或字典)
        output_path: 输出路径
        columns: 列名列表
        sheet_name: 工作表名称
    
    返回:
        操作结果
    """
    import pandas as pd
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if isinstance(data, dict):
        df = pd.DataFrame(data)
    elif isinstance(data, list):
        if columns and len(columns) == len(data[0]) if data else False:
            df = pd.DataFrame(data, columns=columns)
        else:
            df = pd.DataFrame(data)
    else:
        return {"error": "Unsupported data format"}
    
    df.to_excel(output_path, sheet_name=sheet_name, index=False, engine='openpyxl')
    
    return {
        "output_path": output_path,
        "rows": len(df),
        "columns": list(df.columns),
        "sheet_name": sheet_name,
        "status": "success"
    }


def export_results(result_data: Dict, output_path: str) -> Dict[str, Any]:
    """
    导出演示分析结果(格式化报告)
    
    参数:
        result_data: 分析结果字典
        output_path: 输出路径
    
    返回:
        操作结果
    """
    import pandas as pd
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 根据输出格式选择写入方式
    if output_path.endswith('.xlsx'):
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # 基本统计
            if 'basic_stats' in result_data:
                stats_df = pd.DataFrame([result_data['basic_stats']])
                stats_df.to_excel(writer, sheet_name='Basic Stats', index=False)
            
            # 能力指标
            if 'capability_indices' in result_data:
                cap_df = pd.DataFrame([result_data['capability_indices']])
                cap_df.to_excel(writer, sheet_name='Capability Indices', index=False)
            
            # PPM
            if 'ppm' in result_data:
                ppm_df = pd.DataFrame([result_data['ppm']])
                ppm_df.to_excel(writer, sheet_name='PPM Analysis', index=False)
            
            # 规格限
            if 'specification_limits' in result_data:
                spec_df = pd.DataFrame([result_data['specification_limits']])
                spec_df.to_excel(writer, sheet_name='Spec Limits', index=False)
    else:
        # JSON格式
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    return {
        "output_path": output_path,
        "status": "success",
        "sheets_written": ["Basic Stats", "Capability Indices", "PPM Analysis", "Spec Limits"] 
                         if output_path.endswith('.xlsx') else []
    }


def validate_data(data: List, min_samples: int = 3) -> Dict[str, Any]:
    """
    验证数据质量
    
    参数:
        data: 数据列表
        min_samples: 最小样本数
    
    返回:
        验证结果
    """
    data = np.array(data)
    
    result = {
        "total_count": len(data),
        "valid_count": int(np.sum(~np.isnan(data))),
        "null_count": int(np.sum(np.isnan(data))),
        "unique_count": len(np.unique(data[~np.isnan(data)])),
    }
    
    # 检查是否满足最小样本数
    result["is_valid"] = result["valid_count"] >= min_samples
    
    if result["is_valid"]:
        result["min"] = float(np.min(data[~np.isnan(data)]))
        result["max"] = float(np.max(data[~np.isnan(data)]))
        result["mean"] = float(np.mean(data[~np.isnan(data)]))
        result["std"] = float(np.std(data[~np.isnan(data)], ddof=1))
    else:
        result["warning"] = f"Sample size ({result['valid_count']}) is less than minimum ({min_samples})"
    
    # 检查异常值(基于3σ原则)
    if result["is_valid"]:
        mean = result["mean"]
        std = result["std"]
        outliers = np.sum((data > mean + 3*std) | (data < mean - 3*std))
        result["outliers_3sigma"] = int(outliers)
        result["outliers_percent"] = round(outliers / result["valid_count"] * 100, 2) if result["valid_count"] > 0 else 0
    
    return result


def main():
    parser = argparse.ArgumentParser(description='质量数据导入导出脚本')
    parser.add_argument('--action', type=str, required=True,
                        choices=['import', 'export', 'validate'],
                        help='操作类型')
    parser.add_argument('--data-path', type=str, help='数据文件路径(导入时)')
    parser.add_argument('--column', type=str, help='指定列名')
    parser.add_argument('--data', type=str, help='JSON格式数据(导出时)')
    parser.add_argument('--format', type=str, choices=['csv', 'xlsx', 'json'], default='csv',
                        help='输出格式')
    parser.add_argument('--output', type=str, help='输出路径')
    parser.add_argument('--columns', type=str, help='列名列表(逗号分隔)')
    parser.add_argument('--sheet-name', type=str, default='Sheet1', help='Excel工作表名')
    parser.add_argument('--min-samples', type=int, default=3, help='最小样本数(验证用)')
    
    args = parser.parse_args()
    
    result = {}
    
    if args.action == 'import':
        if not args.data_path:
            print(json.dumps({"error": "导入操作需要提供 --data-path 参数"}, ensure_ascii=False))
            sys.exit(1)
        
        if args.data_path.endswith('.xlsx') or args.data_path.endswith('.xls'):
            result = load_excel(args.data_path, args.column, args.sheet_name)
        else:
            result = load_csv(args.data_path, args.column)
        
        # 可选：验证数据
        if 'data' in result and isinstance(result['data'], list):
            result['validation'] = validate_data(result['data'], args.min_samples)
    
    elif args.action == 'export':
        if not args.output:
            print(json.dumps({"error": "导出操作需要提供 --output 参数"}, ensure_ascii=False))
            sys.exit(1)
        
        if args.data:
            import ast
            try:
                data = ast.literal_eval(args.data)
            except:
                data = json.loads(args.data)
        else:
            print(json.dumps({"error": "导出操作需要提供 --data 参数"}, ensure_ascii=False))
            sys.exit(1)
        
        columns = args.columns.split(',') if args.columns else None
        
        if args.format == 'csv':
            result = export_to_csv(data, args.output, columns)
        elif args.format == 'xlsx':
            result = export_to_excel(data, args.output, columns, args.sheet_name)
        else:
            result = export_results(data, args.output)
    
    elif args.action == 'validate':
        if not args.data:
            print(json.dumps({"error": "验证操作需要提供 --data 参数"}, ensure_ascii=False))
            sys.exit(1)
        
        import ast
        try:
            data = ast.literal_eval(args.data)
        except:
            data = json.loads(args.data)
        
        result = validate_data(data, args.min_samples)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
