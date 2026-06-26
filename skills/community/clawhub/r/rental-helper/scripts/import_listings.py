#!/usr/bin/env python3
"""
批量导入房源（支持CSV和Excel）
用法: python import_listings.py --file path/to/file.csv [--format csv|excel]

CSV格式要求：
name,rent,deposit,room_type,area,floor,orientation,decoration,transport,facilities,contact,pros,cons
小区名称,5000,押一付三,两室一厅,85,5层/有电梯,南北通透,精装修,距地铁10号线500米,附近有超市,张中介138xxx,采光好,楼层稍高
"""

import json
import os
import argparse
import csv
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/rental-data")
DATA_FILE = os.path.join(DATA_DIR, "listings.json")

def ensure_data_dir():
    """确保数据目录存在"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_listings():
    """加载现有房源列表"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_listings(listings):
    """保存房源列表"""
    ensure_data_dir()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

def import_from_csv(file_path, listings):
    """从CSV导入"""
    imported = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_id = f"L{len(listings) + imported + 1:03d}"
            listing = {
                "id": new_id,
                "name": row.get("name", ""),
                "address": row.get("address", ""),
                "rent": int(row.get("rent", 0)) if row.get("rent") else 0,
                "deposit": row.get("deposit", "押一付三"),
                "room_type": row.get("room_type", ""),
                "area": float(row.get("area", 0)) if row.get("area") else 0,
                "floor": row.get("floor", ""),
                "orientation": row.get("orientation", ""),
                "decoration": row.get("decoration", ""),
                "transport": row.get("transport", ""),
                "facilities": row.get("facilities", ""),
                "contact": row.get("contact", ""),
                "pros": row.get("pros", ""),
                "cons": row.get("cons", ""),
                "source": row.get("source", ""),
                "url": row.get("url", ""),
                "status": "待考虑",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            listings.append(listing)
            imported += 1
    return imported

def import_from_excel(file_path, listings):
    """从Excel导入"""
    try:
        import pandas as pd
        df = pd.read_excel(file_path)
        imported = 0
        for _, row in df.iterrows():
            new_id = f"L{len(listings) + imported + 1:03d}"
            listing = {
                "id": new_id,
                "name": str(row.get("name", "")),
                "address": str(row.get("address", "")),
                "rent": int(row.get("rent", 0)) if pd.notna(row.get("rent")) else 0,
                "deposit": str(row.get("deposit", "押一付三")),
                "room_type": str(row.get("room_type", "")),
                "area": float(row.get("area", 0)) if pd.notna(row.get("area")) else 0,
                "floor": str(row.get("floor", "")),
                "orientation": str(row.get("orientation", "")),
                "decoration": str(row.get("decoration", "")),
                "transport": str(row.get("transport", "")),
                "facilities": str(row.get("facilities", "")),
                "contact": str(row.get("contact", "")),
                "pros": str(row.get("pros", "")),
                "cons": str(row.get("cons", "")),
                "source": str(row.get("source", "")),
                "url": str(row.get("url", "")),
                "status": "待考虑",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            listings.append(listing)
            imported += 1
        return imported
    except ImportError:
        print("请先安装pandas: pip install pandas openpyxl")
        return 0

def import_listings(args):
    """导入房源"""
    if not os.path.exists(args.file):
        print(f"文件不存在: {args.file}")
        return
    
    listings = load_listings()
    initial_count = len(listings)
    
    # 自动检测格式
    file_format = args.format
    if not file_format:
        if args.file.endswith('.csv'):
            file_format = 'csv'
        elif args.file.endswith(('.xlsx', '.xls')):
            file_format = 'excel'
    
    if file_format == 'csv':
        imported = import_from_csv(args.file, listings)
    elif file_format == 'excel':
        imported = import_from_excel(args.file, listings)
    else:
        print("不支持的文件格式，请使用CSV或Excel")
        return
    
    save_listings(listings)
    
    print(f"✅ 导入完成！")
    print(f"   原有房源: {initial_count} 条")
    print(f"   新增房源: {imported} 条")
    print(f"   当前总计: {len(listings)} 条")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量导入房源")
    parser.add_argument("--file", required=True, help="文件路径")
    parser.add_argument("--format", choices=["csv", "excel"], help="文件格式（自动检测）")
    
    args = parser.parse_args()
    import_listings(args)
