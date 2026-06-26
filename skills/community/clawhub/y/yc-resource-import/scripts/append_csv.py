#!/usr/bin/env python3
"""
CSV 追加写入脚本 - yc-resource-import 技能专用
功能：读取生产库 CSV 表头，将新数据按锁死字段顺序追加写入
"""

import csv
import sys
import os

def read_production_csv(path, encodings=None):
    """读取生产库 CSV，返回 (headers, encoding, rows)"""
    if encodings is None:
        encodings = ['utf-8-sig', 'gbk', 'utf-8', 'latin1']
    
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc) as f:
                reader = csv.reader(f)
                headers = next(reader)
                rows = list(reader)
            return headers, enc, rows
        except UnicodeDecodeError:
            continue
    
    raise ValueError(f"无法读取 {path}，已尝试编码：{encodings}")

def get_fieldnames(headers):
    """从中文备注式表头提取英文字段名"""
    return [h.split(' (')[0] for h in headers]

def append_to_production(prod_path, new_rows, encodings=None):
    """
    将新数据追加到生产库 CSV
    - 保留原表头和所有数据
    - 追加新数据行（字段与表头对齐）
    - 返回追加行数
    """
    # 读取生产库
    headers, enc, prod_rows = read_production_csv(prod_path, encodings)
    fieldnames = get_fieldnames(headers)
    
    # 写入（保留原数据 + 追加新数据）
    with open(prod_path, 'w', encoding=enc, newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)           # 原表头
        writer.writerows(prod_rows)       # 原数据
        for row in new_rows:
            # 将字典按字段顺序转为行
            out_row = [row.get(fn, '') for fn in fieldnames]
            writer.writerow(out_row)
    
    return len(new_rows)

def validate_fields(new_rows, fieldnames):
    """验证新数据字段是否与生产库一致"""
    for i, row in enumerate(new_rows):
        extra = set(row.keys()) - set(fieldnames)
        missing = set(fieldnames) - set(row.keys())
        if extra:
            print(f"[警告] 第{i+1}行含多余字段: {extra}")
        if missing:
            print(f"[警告] 第{i+1}行缺字段: {missing}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python append_csv.py <生产库路径> <新数据CSV路径>")
        sys.exit(1)
    
    prod_path = sys.argv[1]
    new_path = sys.argv[2]
    
    # 读取新数据
    new_headers, new_enc, new_rows = read_production_csv(new_path)
    fieldnames = get_fieldnames(new_headers)
    
    # 追加写入
    count = append_to_production(prod_path, new_rows)
    print(f"[完成] 追加 {count} 行到 {prod_path}")