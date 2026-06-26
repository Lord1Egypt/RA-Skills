#!/usr/bin/env python3
"""
智能推荐房源
用法: python recommend_listings.py --location "公司地址" --budget 5000 --commute-type walk --commute-time 15
"""

import json
import os
import argparse

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/rental-data")
DATA_FILE = os.path.join(DATA_DIR, "listings.json")

def load_listings():
    """加载房源列表"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_commute_info(transport_text):
    """从交通信息文本中提取通勤时间和方式"""
    # 简单解析，实际可以更复杂
    walk_time = None
    subway_time = None
    bus_time = None
    
    if transport_text:
        # 提取步行时间
        if "步行" in transport_text or "走路" in transport_text:
            import re
            match = re.search(r'(\d+)\s*分钟', transport_text)
            if match:
                walk_time = int(match.group(1))
        
        # 提取地铁时间
        if "地铁" in transport_text:
            import re
            matches = re.findall(r'(\d+)\s*分钟', transport_text)
            if matches:
                subway_time = int(matches[0])
    
    return {
        "walk_time": walk_time,
        "subway_time": subway_time,
        "bus_time": bus_time
    }

def calculate_match_score(listing, args):
    """计算房源匹配度评分"""
    score = 0
    reasons = []
    
    # 价格匹配
    rent = listing.get("rent", 0)
    if args.budget:
        if rent <= args.budget:
            score += 30
            reasons.append(f"价格在预算内({rent}元)")
        elif rent <= args.budget * 1.1:
            score += 15
            reasons.append(f"价格略超预算({rent}元)")
        else:
            score -= 20
            reasons.append(f"价格超出预算({rent}元)")
    
    # 户型匹配
    if args.room_type:
        room_type = listing.get("room_type", "")
        if args.room_type in room_type:
            score += 20
            reasons.append(f"户型匹配({room_type})")
    
    # 通勤匹配
    if args.commute_time and args.commute_type:
        transport = listing.get("transport", "")
        commute_info = parse_commute_info(transport)
        
        if args.commute_type == "walk" and commute_info["walk_time"]:
            if commute_info["walk_time"] <= args.commute_time:
                score += 30
                reasons.append(f"步行{commute_info['walk_time']}分钟，符合要求")
            elif commute_info["walk_time"] <= args.commute_time + 5:
                score += 15
                reasons.append(f"步行{commute_info['walk_time']}分钟，略超要求")
        
        elif args.commute_type == "subway" and commute_info["subway_time"]:
            if commute_info["subway_time"] <= args.commute_time:
                score += 30
                reasons.append(f"地铁{commute_info['subway_time']}分钟，符合要求")
    
    # 装修评分
    decoration = listing.get("decoration", "")
    if "精装" in decoration or "新装" in decoration:
        score += 10
        reasons.append("装修较好")
    
    # 面积评分
    area = listing.get("area", 0)
    if area > 0:
        if args.room_type and "单间" in args.room_type:
            if area >= 15:
                score += 10
                reasons.append(f"面积合适({area}㎡)")
        elif area >= 50:
            score += 10
            reasons.append(f"面积宽敞({area}㎡)")
    
    return score, reasons

def recommend_listings(args):
    """推荐房源"""
    listings = load_listings()
    
    if not listings:
        print("暂无房源记录，请先添加房源")
        return
    
    # 计算每个房源的匹配度
    scored_listings = []
    for listing in listings:
        score, reasons = calculate_match_score(listing, args)
        scored_listings.append({
            "listing": listing,
            "score": score,
            "reasons": reasons
        })
    
    # 按匹配度排序
    scored_listings.sort(key=lambda x: x["score"], reverse=True)
    
    # 筛选出匹配的房源（分数>0）
    matched = [s for s in scored_listings if s["score"] > 0]
    
    if not matched:
        print("\n暂无完全匹配的房源，以下是所有房源：")
        matched = scored_listings[:5]
    else:
        print(f"\n🎯 找到 {len(matched)} 套匹配房源：")
    
    # 输出推荐结果
    for i, item in enumerate(matched[:5], 1):
        listing = item["listing"]
        print(f"\n{'='*50}")
        print(f"【推荐{i}】{listing.get('name', '')}")
        print(f"{'='*50}")
        print(f"ID: {listing.get('id', '')}")
        print(f"租金: {listing.get('rent', 0)}元/月")
        print(f"户型: {listing.get('room_type', '')}")
        print(f"面积: {listing.get('area', 0)}㎡")
        print(f"交通: {listing.get('transport', '')}")
        print(f"装修: {listing.get('decoration', '')}")
        print(f"匹配度: {item['score']}分")
        print(f"推荐理由: {'; '.join(item['reasons'])}")
        
        if listing.get('pros'):
            print(f"优点: {listing.get('pros')}")
        if listing.get('cons'):
            print(f"缺点: {listing.get('cons')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="智能推荐房源")
    parser.add_argument("--location", help="目标位置（公司/学校等）")
    parser.add_argument("--budget", type=int, help="预算上限")
    parser.add_argument("--commute-type", choices=["walk", "subway", "bus"], help="通勤方式")
    parser.add_argument("--commute-time", type=int, help="通勤时间限制（分钟）")
    parser.add_argument("--room-type", help="户型要求（如：单间、一室一厅、两室）")
    parser.add_argument("--decoration", help="装修要求")
    
    args = parser.parse_args()
    recommend_listings(args)
