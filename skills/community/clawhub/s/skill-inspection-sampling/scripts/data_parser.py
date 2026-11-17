#!/usr/bin/env python3
"""
数据解析器
支持CSV、Excel、JSON格式的数据文件解析
"""

import argparse
import json
import os
import pandas as pd


def parse_csv(file_path):
    """解析CSV文件"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
    
    for enc in encodings:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise ValueError(f"CSV解析失败: {str(e)}")
    
    raise ValueError(f"无法解析CSV文件，已尝试编码: {encodings}")


def parse_excel(file_path):
    """解析Excel文件"""
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        return df
    except Exception as e:
        try:
            df = pd.read_excel(file_path, engine='xlrd')
            return df
        except Exception as e2:
            raise ValueError(f"Excel解析失败: {str(e2)}")


def parse_json(file_path):
    """解析JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        # 单个对象转为单行DataFrame
        df = pd.DataFrame([data])
    else:
        raise ValueError("JSON格式不支持，仅支持数组或对象")
    
    return df


def detect_format(file_path):
    """自动检测文件格式"""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.csv':
        return 'csv'
    elif ext in ['.xlsx', '.xls']:
        return 'excel'
    elif ext == '.json':
        return 'json'
    else:
        raise ValueError(f"不支持的文件格式: {ext}")


def df_to_records(df):
    """DataFrame转记录列表"""
    records = df.to_dict('records')
    # 处理NaN值
    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None
    return records


def main():
    parser = argparse.ArgumentParser(description='数据解析器')
    parser.add_argument('--input', required=True, help='输入文件路径')
    parser.add_argument('--format', choices=['csv', 'excel', 'json'], 
                       help='文件格式(不指定则自动检测)')
    parser.add_argument('--output', required=True, help='输出JSON文件路径')
    parser.add_argument('--limit', type=int, help='限制返回记录数(用于预览)')
    
    args = parser.parse_args()
    
    # 检查文件存在
    if not os.path.exists(args.input):
        print(json.dumps({"error": f"文件不存在: {args.input}"}))
        return
    
    # 检测格式
    fmt = args.format or detect_format(args.input)
    
    # 解析数据
    try:
        if fmt == 'csv':
            df = parse_csv(args.input)
        elif fmt == 'excel':
            df = parse_excel(args.input)
        elif fmt == 'json':
            df = parse_json(args.input)
        else:
            raise ValueError(f"不支持的格式: {fmt}")
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return
    
    # 数据验证
    if df.empty:
        print(json.dumps({"error": "数据文件为空"}))
        return
    
    # 限制记录数
    if args.limit and args.limit > 0:
        df = df.head(args.limit)
    
    # 构建结果
    result = {
        "status": "success",
        "format": fmt,
        "source": args.input,
        "record_count": len(df),
        "fields": list(df.columns),
        "data": df_to_records(df)
    }
    
    # 保存结果
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(json.dumps({"success": True, "output": args.output, "record_count": len(df)}, 
                    ensure_ascii=False))


if __name__ == "__main__":
    main()
