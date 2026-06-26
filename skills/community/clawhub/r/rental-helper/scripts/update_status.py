#!/usr/bin/env python3
"""
更新房源状态
用法: python update_status.py --id L001 --status 有意向
"""

import json
import os
import argparse
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/rental-data")
DATA_FILE = os.path.join(DATA_DIR, "listings.json")

def load_listings():
    """加载房源列表"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_listings(listings):
    """保存房源列表"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

def update_status(args):
    """更新房源状态"""
    listings = load_listings()
    
    listing = next((l for l in listings if l.get("id") == args.id), None)
    if not listing:
        print(f"未找到房源: {args.id}")
        return
    
    old_status = listing.get("status", "")
    listing["status"] = args.status
    listing["updated_at"] = datetime.now().isoformat()
    
    save_listings(listings)
    
    print(f"✅ 状态已更新")
    print(f"房源: {listing.get('name', '')}")
    print(f"状态: {old_status} → {args.status}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="更新房源状态")
    parser.add_argument("--id", required=True, help="房源ID")
    parser.add_argument("--status", required=True, 
                       choices=["待考虑", "已看房", "有意向", "已放弃", "已签约"],
                       help="新状态")
    
    args = parser.parse_args()
    update_status(args)
