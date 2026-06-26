#!/usr/bin/env python3
"""
旅行记录管理脚本
用于创建、查询、更新和删除旅行记录
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import uuid

# 数据存储路径
DATA_DIR = "./travelogue_data"
TRIPS_FILE = os.path.join(DATA_DIR, "trips.json")


def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(TRIPS_FILE):
        with open(TRIPS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def load_trips() -> List[Dict]:
    """加载所有旅行记录"""
    ensure_data_dir()
    with open(TRIPS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_trips(trips: List[Dict]):
    """保存旅行记录"""
    ensure_data_dir()
    with open(TRIPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(trips, f, ensure_ascii=False, indent=2)


def create_trip(name: str, start_location: Optional[str] = None, 
                start_event: Optional[str] = None, 
                style_preference: str = "文艺") -> Dict:
    """创建新的旅行记录"""
    trips = load_trips()
    
    # 检查是否已有进行中的旅行
    ongoing = [t for t in trips if t['status'] == 'ongoing']
    if ongoing:
        return {
            "success": False,
            "error": "已有进行中的旅行，请先结束当前旅行",
            "ongoing_trip": ongoing[0]
        }
    
    trip_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    trip = {
        "tripId": trip_id,
        "status": "ongoing",
        "title": name,
        "startTime": now,
        "startLocation": start_location,
        "startEvent": start_event,
        "endTime": None,
        "endLocation": None,
        "endEvent": None,
        "stylePreference": style_preference,
        "createdAt": now
    }
    
    trips.append(trip)
    save_trips(trips)
    
    return {
        "success": True,
        "trip": trip,
        "message": f"已成功创建旅行记录：{name}"
    }


def end_trip(trip_id: str, end_location: Optional[str] = None, 
             end_event: Optional[str] = None) -> Dict:
    """结束旅行记录"""
    trips = load_trips()
    
    trip = None
    for t in trips:
        if t['tripId'] == trip_id:
            trip = t
            break
    
    if not trip:
        return {
            "success": False,
            "error": f"未找到旅行记录：{trip_id}"
        }
    
    if trip['status'] != 'ongoing':
        return {
            "success": False,
            "error": "该旅行已经结束"
        }
    
    now = datetime.now().isoformat()
    trip['status'] = 'ended'
    trip['endTime'] = now
    trip['endLocation'] = end_location
    trip['endEvent'] = end_event
    
    save_trips(trips)
    
    return {
        "success": True,
        "trip": trip,
        "message": f"旅行已结束：{trip['title']}"
    }


def get_trip_status(trip_id: Optional[str] = None) -> Dict:
    """查询旅行状态"""
    trips = load_trips()
    
    if trip_id:
        # 查询指定旅行
        for t in trips:
            if t['tripId'] == trip_id:
                return {
                    "success": True,
                    "trip": t
                }
        return {
            "success": False,
            "error": f"未找到旅行记录：{trip_id}"
        }
    else:
        # 查询当前进行中的旅行
        ongoing = [t for t in trips if t['status'] == 'ongoing']
        if ongoing:
            return {
                "success": True,
                "trip": ongoing[0],
                "message": f"当前进行中的旅行：{ongoing[0]['title']}"
            }
        else:
            return {
                "success": True,
                "trip": None,
                "message": "当前没有进行中的旅行"
            }


def list_trips(status: Optional[str] = None) -> Dict:
    """列出所有旅行记录"""
    trips = load_trips()
    
    if status:
        filtered = [t for t in trips if t['status'] == status]
        return {
            "success": True,
            "trips": filtered,
            "count": len(filtered)
        }
    
    return {
        "success": True,
        "trips": trips,
        "count": len(trips)
    }


def delete_trip(trip_id: str) -> Dict:
    """删除旅行记录"""
    trips = load_trips()
    
    initial_count = len(trips)
    trips = [t for t in trips if t['tripId'] != trip_id]
    
    if len(trips) == initial_count:
        return {
            "success": False,
            "error": f"未找到旅行记录：{trip_id}"
        }
    
    save_trips(trips)
    
    # 删除相关的素材记录
    moments_file = os.path.join(DATA_DIR, "moments.json")
    if os.path.exists(moments_file):
        with open(moments_file, 'r', encoding='utf-8') as f:
            moments = json.load(f)
        moments = [m for m in moments if m['tripId'] != trip_id]
        with open(moments_file, 'w', encoding='utf-8') as f:
            json.dump(moments, f, ensure_ascii=False, indent=2)
    
    return {
        "success": True,
        "message": f"已删除旅行记录：{trip_id}"
    }


def update_trip_style(trip_id: str, style: str) -> Dict:
    """更新游记风格偏好"""
    trips = load_trips()
    
    for t in trips:
        if t['tripId'] == trip_id:
            t['stylePreference'] = style
            save_trips(trips)
            return {
                "success": True,
                "trip": t,
                "message": f"已更新游记风格为：{style}"
            }
    
    return {
        "success": False,
        "error": f"未找到旅行记录：{trip_id}"
    }


def find_trip_by_name(trip_name: str) -> Dict:
    """根据旅行名称查找旅行记录（支持模糊匹配）"""
    trips = load_trips()
    
    # 精确匹配
    for t in trips:
        if t['title'] == trip_name:
            return {
                "success": True,
                "trip": t,
                "match_type": "exact"
            }
    
    # 模糊匹配
    matched = []
    for t in trips:
        if trip_name in t['title'] or t['title'] in trip_name:
            matched.append(t)
    
    if len(matched) == 1:
        return {
            "success": True,
            "trip": matched[0],
            "match_type": "fuzzy"
        }
    elif len(matched) > 1:
        return {
            "success": False,
            "error": f"找到多个匹配的旅行：{', '.join([t['title'] for t in matched])}，请提供更精确的名称",
            "matched_trips": matched
        }
    else:
        return {
            "success": False,
            "error": f"未找到名称包含'{trip_name}'的旅行记录"
        }


def main():
    parser = argparse.ArgumentParser(description='旅行记录管理工具')
    parser.add_argument('--action', required=True, 
                       choices=['create', 'end', 'status', 'list', 'delete', 'update-style', 'find'],
                       help='操作类型')
    parser.add_argument('--name', help='旅行名称')
    parser.add_argument('--trip-id', help='旅行ID')
    parser.add_argument('--start-location', help='起始地点')
    parser.add_argument('--start-event', help='开始事件描述')
    parser.add_argument('--end-location', help='结束地点')
    parser.add_argument('--end-event', help='结束感言')
    parser.add_argument('--status-filter', choices=['ongoing', 'ended'], help='状态筛选')
    parser.add_argument('--style', default='文艺', help='游记风格')
    
    args = parser.parse_args()
    
    result = None
    
    if args.action == 'create':
        if not args.name:
            result = {"success": False, "error": "缺少旅行名称"}
        else:
            result = create_trip(
                name=args.name,
                start_location=args.start_location,
                start_event=args.start_event,
                style_preference=args.style
            )
    
    elif args.action == 'end':
        if not args.trip_id:
            # 尝试获取当前进行中的旅行
            status_result = get_trip_status()
            if status_result['success'] and status_result.get('trip'):
                args.trip_id = status_result['trip']['tripId']
            else:
                result = {"success": False, "error": "没有进行中的旅行"}
        
        if not result:
            result = end_trip(
                trip_id=args.trip_id,
                end_location=args.end_location,
                end_event=args.end_event
            )
    
    elif args.action == 'status':
        result = get_trip_status(trip_id=args.trip_id)
    
    elif args.action == 'list':
        result = list_trips(status=args.status_filter)
    
    elif args.action == 'delete':
        if not args.trip_id:
            result = {"success": False, "error": "缺少旅行ID"}
        else:
            result = delete_trip(trip_id=args.trip_id)
    
    elif args.action == 'update-style':
        if not args.trip_id or not args.style:
            result = {"success": False, "error": "缺少旅行ID或风格参数"}
        else:
            result = update_trip_style(trip_id=args.trip_id, style=args.style)
    
    elif args.action == 'find':
        if not args.name:
            result = {"success": False, "error": "缺少旅行名称"}
        else:
            result = find_trip_by_name(trip_name=args.name)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
