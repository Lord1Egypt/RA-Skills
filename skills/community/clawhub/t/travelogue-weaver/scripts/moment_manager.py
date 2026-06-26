#!/usr/bin/env python3
"""
素材管理脚本
用于添加、查询、更新和删除旅行素材
"""

import argparse
import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional
import uuid

# 数据存储路径
DATA_DIR = "./travelogue_data"
MOMENTS_FILE = os.path.join(DATA_DIR, "moments.json")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")


def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    if not os.path.exists(MOMENTS_FILE):
        with open(MOMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def load_moments() -> List[Dict]:
    """加载所有素材"""
    ensure_data_dir()
    with open(MOMENTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_moments(moments: List[Dict]):
    """保存素材"""
    ensure_data_dir()
    with open(MOMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(moments, f, ensure_ascii=False, indent=2)


def get_ongoing_trip_id() -> Optional[str]:
    """获取当前进行中的旅行ID"""
    trips_file = os.path.join(DATA_DIR, "trips.json")
    if not os.path.exists(trips_file):
        return None
    
    with open(trips_file, 'r', encoding='utf-8') as f:
        trips = json.load(f)
    
    ongoing = [t for t in trips if t['status'] == 'ongoing']
    return ongoing[0]['tripId'] if ongoing else None


def get_trip_by_id(trip_id: str) -> Optional[Dict]:
    """根据ID获取旅行记录"""
    trips_file = os.path.join(DATA_DIR, "trips.json")
    if not os.path.exists(trips_file):
        return None
    
    with open(trips_file, 'r', encoding='utf-8') as f:
        trips = json.load(f)
    
    for t in trips:
        if t['tripId'] == trip_id:
            return t
    return None


def add_moment(trip_id: Optional[str], moment_type: str, content: str,
               raw_path: Optional[str] = None, location: Optional[str] = None,
               timestamp: Optional[str] = None, exif: Optional[Dict] = None,
               force_add: bool = False) -> Dict:
    """
    添加新素材
    
    参数：
        force_add: 是否强制添加（用于补充记录到已结束的旅行）
    """
    ensure_data_dir()
    
    # 如果未指定 trip_id，尝试获取当前进行中的旅行
    if not trip_id:
        trip_id = get_ongoing_trip_id()
        if not trip_id:
            return {
                "success": False,
                "error": "没有进行中的旅行，无法添加素材。请先说'开始XX旅行'来创建游记档案。"
            }
    
    # 验证旅行是否存在，并检查状态
    trip = get_trip_by_id(trip_id)
    if not trip:
        return {
            "success": False,
            "error": f"未找到旅行记录：{trip_id}"
        }
    
    # 检查旅行状态
    if trip['status'] == 'ended' and not force_add:
        return {
            "success": False,
            "error": f"旅行【{trip['title']}】已结束，不再接受新素材。如需补充记录，请明确说'补充到{trip['title']}中'。",
            "trip_title": trip['title'],
            "trip_status": trip['status']
        }
    
    moment_id = str(uuid.uuid4())
    
    # 处理文件上传
    stored_path = None
    if raw_path and os.path.exists(raw_path):
        # 生成存储文件名
        ext = os.path.splitext(raw_path)[1]
        stored_filename = f"{moment_id}{ext}"
        stored_path = os.path.join(UPLOADS_DIR, stored_filename)
        shutil.copy2(raw_path, stored_path)
    
    # 使用当前时间作为默认时间戳
    if not timestamp:
        timestamp = datetime.now().isoformat()
    
    moment = {
        "momentId": moment_id,
        "tripId": trip_id,
        "type": moment_type,
        "content": content,
        "rawUrl": stored_path,
        "timestamp": timestamp,
        "location": location,
        "exif": exif
    }
    
    moments = load_moments()
    moments.append(moment)
    save_moments(moments)
    
    return {
        "success": True,
        "moment": moment,
        "message": f"已成功添加{moment_type}素材"
    }


def list_moments(trip_id: Optional[str] = None, 
                 moment_type: Optional[str] = None,
                 location: Optional[str] = None) -> Dict:
    """查询素材"""
    moments = load_moments()
    
    if trip_id:
        moments = [m for m in moments if m['tripId'] == trip_id]
    
    if moment_type:
        moments = [m for m in moments if m['type'] == moment_type]
    
    if location:
        moments = [m for m in moments if m.get('location') and location in m['location']]
    
    # 按时间戳排序
    moments = sorted(moments, key=lambda m: m['timestamp'])
    
    return {
        "success": True,
        "moments": moments,
        "count": len(moments)
    }


def get_moment_stats(trip_id: Optional[str] = None) -> Dict:
    """获取素材统计信息"""
    moments = load_moments()
    
    if trip_id:
        moments = [m for m in moments if m['tripId'] == trip_id]
    
    type_counts = {}
    for m in moments:
        t = m['type']
        type_counts[t] = type_counts.get(t, 0) + 1
    
    locations = list(set(m.get('location') for m in moments if m.get('location')))
    
    return {
        "success": True,
        "total_count": len(moments),
        "type_counts": type_counts,
        "locations": locations
    }


def delete_moment(moment_id: str) -> Dict:
    """删除素材"""
    moments = load_moments()
    
    moment = None
    for m in moments:
        if m['momentId'] == moment_id:
            moment = m
            break
    
    if not moment:
        return {
            "success": False,
            "error": f"未找到素材：{moment_id}"
        }
    
    # 删除关联的文件
    if moment.get('rawUrl') and os.path.exists(moment['rawUrl']):
        os.remove(moment['rawUrl'])
    
    moments = [m for m in moments if m['momentId'] != moment_id]
    save_moments(moments)
    
    return {
        "success": True,
        "message": f"已删除素材：{moment_id}"
    }


def update_moment(moment_id: str, content: Optional[str] = None,
                  location: Optional[str] = None, 
                  timestamp: Optional[str] = None) -> Dict:
    """更新素材信息"""
    moments = load_moments()
    
    for m in moments:
        if m['momentId'] == moment_id:
            if content:
                m['content'] = content
            if location:
                m['location'] = location
            if timestamp:
                m['timestamp'] = timestamp
            
            save_moments(moments)
            return {
                "success": True,
                "moment": m,
                "message": f"已更新素材：{moment_id}"
            }
    
    return {
        "success": False,
        "error": f"未找到素材：{moment_id}"
    }


def get_moments_by_date(trip_id: str) -> Dict:
    """按日期分组获取素材"""
    result = list_moments(trip_id=trip_id)
    
    if not result['success']:
        return result
    
    moments = result['moments']
    
    # 按日期分组
    date_groups = {}
    for m in moments:
        # 从时间戳提取日期
        ts = m['timestamp']
        if 'T' in ts:
            date_str = ts.split('T')[0]
        else:
            date_str = ts.split(' ')[0] if ' ' in ts else ts
        
        if date_str not in date_groups:
            date_groups[date_str] = []
        date_groups[date_str].append(m)
    
    return {
        "success": True,
        "date_groups": date_groups,
        "total_count": len(moments)
    }


def main():
    parser = argparse.ArgumentParser(description='素材管理工具')
    parser.add_argument('--action', required=True, 
                       choices=['add', 'list', 'stats', 'delete', 'update', 'group-by-date'],
                       help='操作类型')
    parser.add_argument('--trip-id', help='旅行ID')
    parser.add_argument('--moment-id', help='素材ID')
    parser.add_argument('--type', choices=['text', 'image', 'audio', 'video'],
                       help='素材类型')
    parser.add_argument('--content', help='素材内容')
    parser.add_argument('--raw-path', help='原始文件路径')
    parser.add_argument('--location', help='地点')
    parser.add_argument('--timestamp', help='时间戳')
    parser.add_argument('--exif', help='EXIF元数据（JSON格式）')
    parser.add_argument('--force', action='store_true',
                       help='强制添加（用于补充记录到已结束的旅行）')
    
    args = parser.parse_args()
    
    result = None
    
    if args.action == 'add':
        if not args.type:
            result = {"success": False, "error": "缺少素材类型"}
        elif not args.content:
            result = {"success": False, "error": "缺少素材内容"}
        else:
            exif_data = None
            if args.exif:
                try:
                    exif_data = json.loads(args.exif)
                except:
                    pass
            
            result = add_moment(
                trip_id=args.trip_id,
                moment_type=args.type,
                content=args.content,
                raw_path=args.raw_path,
                location=args.location,
                timestamp=args.timestamp,
                exif=exif_data,
                force_add=args.force
            )
    
    elif args.action == 'list':
        result = list_moments(
            trip_id=args.trip_id,
            moment_type=args.type,
            location=args.location
        )
    
    elif args.action == 'stats':
        result = get_moment_stats(trip_id=args.trip_id)
    
    elif args.action == 'delete':
        if not args.moment_id:
            result = {"success": False, "error": "缺少素材ID"}
        else:
            result = delete_moment(moment_id=args.moment_id)
    
    elif args.action == 'update':
        if not args.moment_id:
            result = {"success": False, "error": "缺少素材ID"}
        else:
            result = update_moment(
                moment_id=args.moment_id,
                content=args.content,
                location=args.location,
                timestamp=args.timestamp
            )
    
    elif args.action == 'group-by-date':
        if not args.trip_id:
            result = {"success": False, "error": "缺少旅行ID"}
        else:
            result = get_moments_by_date(trip_id=args.trip_id)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
