#!/usr/bin/env python3
"""
Running Coach - 每周训练计划生成器
基于全频训练法自动生成训练计划并上传到 Intervals.icu
"""

import os
import json
import urllib.request
import base64
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# ============== 配置 ==============
# 优先级: 环境变量 > config.json > 默认值
CONFIG = {
    "API_KEY": os.environ.get("INTERVALS_API_KEY", ""),
    "ATHLETE_ID": os.environ.get("INTERVALS_ATHLETE_ID", ""),
    "THRESHOLD_PACE": int(os.environ.get("INTERVALS_THRESHOLD_PACE", "217")),
    "WEEKLY_TARGET_LOAD": 400,
}

BASE_URL = "https://intervals.icu/api/v1"


def load_config(config_path: str = "config.json"):
    """加载配置文件，覆盖默认值"""
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            user_config = json.load(f)
            for key in ["API_KEY", "ATHLETE_ID", "THRESHOLD_PACE", "WEEKLY_TARGET_LOAD"]:
                if key in user_config and user_config[key]:
                    CONFIG[key] = user_config[key]
    
    # 验证必要配置
    if not CONFIG["API_KEY"] or not CONFIG["ATHLETE_ID"]:
        print("错误: 请配置 API_KEY 和 ATHLETE_ID")
        print("方式A: 设置环境变量 INTERVALS_API_KEY 和 INTERVALS_ATHLETE_ID")
        print("方式B: 修改 config.json 文件")
        return False
    return True


def make_request(method: str, url: str, data: Optional[Dict] = None) -> Optional[Dict]:
    """发送API请求"""
    req = urllib.request.Request(url, method=method)
    auth_string = f"API_KEY:{CONFIG['API_KEY']}"
    auth_b64 = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
    req.add_header("Authorization", f"Basic {auth_b64}")
    req.add_header("Content-Type", "application/json")
    
    if data:
        req.data = json.dumps(data).encode("utf-8")
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_pace_zones(threshold_pace: int) -> Dict[str, str]:
    """计算配速区间"""
    return {
        "Z1": f">{threshold_pace + 63}/km",
        "Z2": f"{threshold_pace - 30}-{threshold_pace + 2}/km",
        "Z3": f"{threshold_pace - 47}-{threshold_pace - 31}/km",
        "Z4": f"{threshold_pace - 50}-{threshold_pace}/km",
    }


def create_workout(name: str, date: str, description: str, distance: int) -> Optional[Dict]:
    """创建单个训练"""
    url = f"{BASE_URL}/athlete/{CONFIG['ATHLETE_ID']}/events?upsertOnUid=true"
    data = {
        "name": name,
        "category": "WORKOUT",
        "type": "Run",
        "start_date_local": date,
        "description": description,
        "distance": distance,
        "athlete_id": CONFIG["ATHLETE_ID"]
    }
    return make_request("POST", url, data)


def generate_weekly_plan(week_start: datetime, threshold_pace: int = 217) -> List[Dict]:
    """生成周训练计划"""
    
    zones = get_pace_zones(threshold_pace)
    pace_ref = f"""
配速区间(Threshold={threshold_pace//60}:{threshold_pace%60:02d}/km):
- Z1: {zones['Z1']}
- Z2: {zones['Z2']}
- Z3: {zones['Z3']}
- Z4: {zones['Z4']}
"""
    
    workouts = [
        {"name": "轻松跑-8K @5:00", "date": week_start.strftime("%Y-%m-%dT06:30:00"),
         "description": pace_ref + "\n- 8km 5:00/km Pace", "distance": 8000},
        
        {"name": "有氧跑-15K @4:30", "date": (week_start + timedelta(days=1)).strftime("%Y-%m-%dT06:30:00"),
         "description": pace_ref + "\n- 15km 4:30-4:15/km Pace", "distance": 15000},
        
        {"name": "间歇跑-8x1K @3:46", "date": (week_start + timedelta(days=2)).strftime("%Y-%m-%dT06:30:00"),
         "description": f"""{pace_ref}

热身:
- 3km easy

间歇:
8x
- 1km 3:46/km Pace
- 3m rest

放松:
- 3km easy""", "distance": 14000},
        
        {"name": "休息日", "date": (week_start + timedelta(days=3)).strftime("%Y-%m-%dT06:30:00"),
         "description": "完全休息或泡沫轴/拉伸", "distance": 0},
        
        {"name": "Tempo-15K @3:40", "date": (week_start + timedelta(days=4)).strftime("%Y-%m-%dT06:30:00"),
         "description": f"""{pace_ref}

热身:
- 3km easy

主训练:
- 15km 3:40/km Pace

放松:
- 2km easy""", "distance": 20000},
        
        {"name": "轻松跑-8K @5:00", "date": (week_start + timedelta(days=5)).strftime("%Y-%m-%dT06:30:00"),
         "description": pace_ref + "\n- 8km 5:00/km Pace", "distance": 8000},
        
        {"name": "LSD-30K @4:30-3:34", "date": (week_start + timedelta(days=6)).strftime("%Y-%m-%dT06:30:00"),
         "description": f"""{pace_ref}

渐进:
- 5km 4:30/km Pace
- 5km 4:15/km Pace
- 5km 4:00/km Pace
- 5km 3:50/km Pace
- 5km 3:40/km Pace
- 5km 3:34/km Pace""", "distance": 30000},
    ]
    
    return workouts


def upload_week(week_start: datetime, threshold_pace: int = 217, dry_run: bool = False):
    """上传周计划到Intervals.icu"""
    
    print(f"\n{'='*50}")
    print(f"生成周计划: {week_start.strftime('%Y-%m-%d')}")
    print(f"Threshold配速: {threshold_pace//60}:{threshold_pace%60:02d}/km")
    print(f"{'='*50}\n")
    
    workouts = generate_weekly_plan(week_start, threshold_pace)
    total_load = 0
    
    for w in workouts:
        print(f"创建: {w['name']}")
        
        if dry_run:
            print(f"  [DRY RUN]")
            continue
        
        result = create_workout(w["name"], w["date"], w["description"], w["distance"])
        
        if result:
            load = result.get("icu_training_load", 0) or 0
            intensity = result.get("icu_intensity", 0) or 0
            print(f"  ✓ Load: {load}, Intensity: {intensity:.1f}%")
            total_load += load
        else:
            print(f"  ✗ Failed")
    
    if not dry_run:
        print(f"\n{'='*50}")
        print(f"本周总负荷: {total_load}")
        print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(description="Running Coach - 训练计划生成器")
    parser.add_argument("--date", type=str, help="周起始日期 (YYYY-MM-DD)", default=None)
    parser.add_argument("--threshold", type=int, help="Threshold配速(秒/km)", default=None)
    parser.add_argument("--dry-run", action="store_true", help="仅显示不上传")
    parser.add_argument("--config", type=str, default="config.json", help="配置文件路径")
    
    args = parser.parse_args()
    
    # 加载配置
    if not load_config(args.config):
        return
    
    # 解析日期
    if args.date:
        week_start = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        today = datetime.now()
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        week_start = today + timedelta(days=days_until_monday)
    
    # 使用命令行参数覆盖
    threshold = args.threshold or CONFIG["THRESHOLD_PACE"]
    
    upload_week(week_start, threshold, args.dry_run)


if __name__ == "__main__":
    main()
