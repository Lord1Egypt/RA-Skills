#!/usr/bin/env python3
"""
添加新房源记录
用法: python add_listing.py --name "小区名称" --rent 5000 --deposit "押一付三" ...
"""

import json
import os
import argparse
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

def add_listing(args):
    """添加新房源"""
    listings = load_listings()
    
    # 生成ID
    new_id = f"L{len(listings) + 1:03d}"
    
    listing = {
        "id": new_id,
        "name": args.name,
        "address": args.address or "",
        "rent": args.rent,
        "deposit": args.deposit or "押一付三",
        "room_type": args.room_type or "",
        "area": args.area or 0,
        "floor": args.floor or "",
        "orientation": args.orientation or "",
        "decoration": args.decoration or "",
        "transport": args.transport or "",
        "facilities": args.facilities or "",
        "contact": args.contact or "",
        "pros": args.pros or "",
        "cons": args.cons or "",
        "url": args.url or "",
        "images": args.images or "",
        "status": "待考虑",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    listings.append(listing)
    save_listings(listings)
    
    print(f"✅ 房源已记录！ID: {new_id}")
    print(f"   名称: {args.name}")
    print(f"   租金: {args.rent}元/月")
    if args.url:
        print(f"   链接: {args.url}")
    return new_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="添加新房源")
    parser.add_argument("--name", required=True, help="房源名称/小区")
    parser.add_argument("--rent", type=int, required=True, help="月租金")
    parser.add_argument("--deposit", help="押金方式")
    parser.add_argument("--address", help="详细地址")
    parser.add_argument("--room-type", help="户型")
    parser.add_argument("--area", type=float, help="面积")
    parser.add_argument("--floor", help="楼层")
    parser.add_argument("--orientation", help="朝向")
    parser.add_argument("--decoration", help="装修情况")
    parser.add_argument("--transport", help="交通情况")
    parser.add_argument("--facilities", help="周边配套")
    parser.add_argument("--contact", help="联系方式")
    parser.add_argument("--pros", help="优点")
    parser.add_argument("--cons", help="缺点")
    parser.add_argument("--url", help="房源链接（查看房间环境）")
    parser.add_argument("--images", help="房间图片链接（多个用逗号分隔）")
    
    args = parser.parse_args()
    add_listing(args)
