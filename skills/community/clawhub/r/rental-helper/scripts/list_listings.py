#!/usr/bin/env python3
"""
列出租源列表（增强版，支持筛选和看房记录）
用法: python list_listings.py [--status 状态] [--min-rent 1000] [--max-rent 5000] [--viewings]
"""

import json
import os
import argparse

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/rental-data")
LISTINGS_FILE = os.path.join(DATA_DIR, "listings.json")
VIEWINGS_FILE = os.path.join(DATA_DIR, "viewings.json")

def load_listings():
    """加载房源列表"""
    if not os.path.exists(LISTINGS_FILE):
        return []
    with open(LISTINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_viewings():
    """加载看房记录"""
    if not os.path.exists(VIEWINGS_FILE):
        return []
    with open(VIEWINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_listings(args):
    """列出租源"""
    listings = load_listings()
    viewings = load_viewings()
    
    if not listings:
        print("暂无房源记录")
        return
    
    # 筛选
    filtered = listings
    if args.status:
        filtered = [l for l in filtered if l.get("status") == args.status]
    if args.min_rent:
        filtered = [l for l in filtered if l.get("rent", 0) >= args.min_rent]
    if args.max_rent:
        filtered = [l for l in filtered if l.get("rent", 0) <= args.max_rent]
    if args.room_type:
        filtered = [l for l in filtered if args.room_type in l.get("room_type", "")]
    if args.decoration:
        filtered = [l for l in filtered if args.decoration in l.get("decoration", "")]
    
    if not filtered:
        print("没有符合条件的房源")
        return
    
    # 输出表格
    print(f"\n{'ID':<6}{'名称':<18}{'租金':<10}{'户型':<10}{'面积':<8}{'状态':<8}")
    print("-" * 65)
    for l in filtered:
        name = l.get("name", "")[:16]
        rent = f"{l.get('rent', 0)}元"
        room_type = l.get("room_type", "")[:8]
        area = f"{l.get('area', 0)}㎡"
        status = l.get("status", "")[:6]
        print(f"{l.get('id', ''):<6}{name:<18}{rent:<10}{room_type:<10}{area:<8}{status:<8}")
    
    print(f"\n共 {len(filtered)} 条记录")
    
    # 输出详细信息（如果指定了ID）
    if args.id:
        listing = next((l for l in listings if l.get("id") == args.id), None)
        if listing:
            print(f"\n{'='*50}")
            print(f"【{listing.get('name')}】详情")
            print(f"{'='*50}")
            
            fields = [
                ("ID", "id"),
                ("名称", "name"),
                ("地址", "address"),
                ("租金", "rent", lambda x: f"{x}元/月"),
                ("押金", "deposit"),
                ("户型", "room_type"),
                ("面积", "area", lambda x: f"{x}㎡"),
                ("楼层", "floor"),
                ("朝向", "orientation"),
                ("装修", "decoration"),
                ("交通", "transport"),
                ("配套", "facilities"),
                ("联系方式", "contact"),
                ("优点", "pros"),
                ("缺点", "cons"),
                ("房源链接", "url"),
                ("房间图片", "images"),
                ("状态", "status"),
                ("创建时间", "created_at"),
            ]
            
            for label, key, *transform in fields:
                value = listing.get(key)
                if value:
                    if transform:
                        value = transform[0](value)
                    print(f"{label}: {value}")
            
            # 显示看房记录
            if args.viewings:
                listing_viewings = [v for v in viewings if v.get("listing_id") == args.id]
                if listing_viewings:
                    print(f"\n📋 看房记录:")
                    for v in listing_viewings:
                        print(f"  - {v.get('viewing_time', '')[:10]} 评分:{v.get('overall_score')}/10 {'🟢考虑签约' if v.get('consider_signing') else '🔴暂不考虑'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="列出租源")
    parser.add_argument("--status", help="按状态筛选")
    parser.add_argument("--min-rent", type=int, help="最低租金")
    parser.add_argument("--max-rent", type=int, help="最高租金")
    parser.add_argument("--room-type", help="户型筛选")
    parser.add_argument("--decoration", help="装修筛选")
    parser.add_argument("--id", help="查看指定ID的详情")
    parser.add_argument("--viewings", action="store_true", help="同时显示看房记录")
    
    args = parser.parse_args()
    list_listings(args)
