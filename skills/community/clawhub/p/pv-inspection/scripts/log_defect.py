#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光伏电站缺陷记录脚本
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

# 数据目录
DATA_DIR = Path("/home/admin/.openclaw/workspace/pv-inspection/data")

def log_defect(station: str, defect_type: str, level: str, description: str, location: str = ""):
    """记录缺陷"""
    
    # 缺陷 ID 生成
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    defect_id = f"DEF-{timestamp}"
    
    # 缺陷记录
    defect = {
        "id": defect_id,
        "station": station,
        "type": defect_type,
        "level": level,
        "location": location,
        "description": description,
        "report_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "待整改",
        "deadline": get_deadline(level),
        "assignee": "",
        "completion_time": "",
        "notes": ""
    }
    
    # 保存到文件
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    defects_file = DATA_DIR / "defects.json"
    
    # 读取现有缺陷
    defects = []
    if defects_file.exists():
        with open(defects_file, 'r', encoding='utf-8') as f:
            defects = json.load(f)
    
    # 添加新缺陷
    defects.append(defect)
    
    # 保存
    with open(defects_file, 'w', encoding='utf-8') as f:
        json.dump(defects, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 缺陷已记录：{defect_id}")
    print(f"📍 电站：{station}")
    print(f"📋 类型：{defect_type}")
    print(f"⚠️ 等级：{level}")
    print(f"📝 描述：{description}")
    print(f"⏰ 整改期限：{defect['deadline']}")
    
    return defect_id


def get_deadline(level: str) -> str:
    """根据严重程度计算整改期限"""
    from datetime import timedelta
    
    now = datetime.now()
    
    if level == "紧急":
        deadline = now + timedelta(hours=24)
    elif level == "重要":
        deadline = now + timedelta(days=7)
    else:  # 一般
        deadline = now + timedelta(days=30)
    
    return deadline.strftime("%Y-%m-%d")


def main():
    parser = argparse.ArgumentParser(description="光伏电站缺陷记录")
    parser.add_argument("--station", required=True, help="电站名称")
    parser.add_argument("--type", required=True, help="缺陷类型（设备缺陷/环境隐患/安全问题）")
    parser.add_argument("--level", required=True, choices=["紧急", "重要", "一般"], help="严重程度")
    parser.add_argument("--desc", required=True, help="缺陷描述")
    parser.add_argument("--location", default="", help="具体位置")
    
    args = parser.parse_args()
    
    log_defect(args.station, args.type, args.level, args.desc, args.location)


if __name__ == "__main__":
    main()
