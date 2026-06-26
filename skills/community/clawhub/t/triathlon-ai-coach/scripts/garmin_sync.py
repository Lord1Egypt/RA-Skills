#!/usr/bin/env python3
"""
Garmin 数据同步工具 v2
支持海外服务器 (garmin.com)
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta

PYTHON = Path.home() / ".miniconda3/bin/python3"

DATA_DIR = Path(__file__).parent / "data"
CREDENTIALS_FILE = DATA_DIR / "credentials.json"
ACTIVITIES_FILE = DATA_DIR / "activities.json"


def load_credentials():
    """加载 Garmin 凭证"""
    if CREDENTIALS_FILE.exists():
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    return None


def save_credentials(email, password):
    """保存 Garmin 凭证"""
    DATA_DIR.mkdir(exist_ok=True)
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump({"email": email, "password": password}, f)


def sync_with_retry(max_retries=3, wait_seconds=30):
    """带重试的同步"""
    import garth
    
    creds = load_credentials()
    if not creds:
        print("请先设置 Garmin 账号: python3 garmin_sync.py setup <邮箱> <密码>")
        return None
    
    client = garth.Client(domain='garmin.com')  # 海外服务器
    
    for attempt in range(max_retries):
        try:
            print(f"尝试登录 Garmin (第 {attempt+1} 次)...")
            client.login(creds["email"], creds["password"])
            print("✅ 登录成功!")
            break
        except Exception as e:
            error_msg = str(e)
            print(f"❌ 第 {attempt+1} 次失败: {error_msg}")
            
            if "429" in error_msg or "Too Many Requests" in error_msg:
                if attempt < max_retries - 1:
                    wait = wait_seconds * (attempt + 1)
                    print(f"⏳ 服务器限流，等待 {wait} 秒后重试...")
                    time.sleep(wait)
                else:
                    print("❌ 达到最大重试次数，请稍后再试或使用手动导出")
                    return None
            else:
                print(f"❌ 登录失败: {e}")
                return None
    
    try:
        print("正在下载活动数据...")
        activities = client.get_activities(
            startdate=(datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        )
        
        activity_list = []
        for a in activities:
            activity_list.append({
                "activityId": getattr(a, 'activity_id', None),
                "activityName": getattr(a, 'activity_name', None),
                "activityType": getattr(a, 'activity_type', {}).get('type_key', 'unknown') if hasattr(a, 'activity_type') else 'unknown',
                "startTimeGMT": str(getattr(a, 'start_time_gmt', None)),
                "startTimeLocal": str(getattr(a, 'start_time_local', None)),
                "distance": getattr(a, 'distance', 0) or 0,
                "duration": getattr(a, 'duration', 0) or 0,
                "elapsedDuration": getattr(a, 'elapsed_duration', 0) or 0,
                "movingDuration": getattr(a, 'moving_duration', 0) or 0,
                "elevationGain": getattr(a, 'elevation_gain', 0) or 0,
                "averageSpeed": getattr(a, 'average_speed', 0) or 0,
                "maxSpeed": getattr(a, 'max_speed', 0) or 0,
                "averageHR": getattr(a, 'average_hr', 0) or 0,
                "maxHR": getattr(a, 'max_hr', 0) or 0,
                "averagePower": getattr(a, 'average_power', 0) or 0,
                "calories": getattr(a, 'calories', 0) or 0,
                "trainingEffect": getattr(a, 'training_effect', None),
            })
        
        DATA_DIR.mkdir(exist_ok=True)
        with open(ACTIVITIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(activity_list, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 成功同步 {len(activity_list)} 条活动记录")
        return activity_list
        
    except Exception as e:
        print(f"下载失败: {e}")
        return None


def show_summary():
    """显示活动摘要"""
    if not ACTIVITIES_FILE.exists():
        print("暂无活动数据，请先运行 sync 命令")
        return
    
    with open(ACTIVITIES_FILE, 'r', encoding='utf-8') as f:
        activities = json.load(f)
    
    if not activities:
        print("暂无活动数据")
        return
    
    type_count = {"running": 0, "cycling": 0, "swimming": 0, "other": 0}
    total_distance = 0
    total_duration = 0
    total_activities = len(activities)
    
    for a in activities:
        t = a.get('activityType', '').lower()
        if 'run' in t:
            type_count["running"] += 1
        elif 'bike' in t or 'cycl' in t:
            type_count["cycling"] += 1
        elif 'swim' in t:
            type_count["swimming"] += 1
        else:
            type_count["other"] += 1
        total_distance += a.get('distance', 0)
        total_duration += a.get('duration', 0)
    
    print(f"""
🛰️ **Garmin 活动统计**
━━━━━━━━━━━━━━━━━━━━━━
🏃 跑步: {type_count["running"]} 次
🚴 骑行: {type_count["cycling"]} 次  
🏊 游泳: {type_count["swimming"]} 次
📝 其他: {type_count["other"]} 次
━━━━━━━━━━━━━━━━━━━━━━
📏 总距离: {total_distance/1000:.1f} km
⏱️ 总时长: {total_duration/3600:.1f} 小时
📊 总活动: {total_activities} 次
━━━━━━━━━━━━━━━━━━━━━━
""")


def show_recent():
    """显示最近10条活动"""
    if not ACTIVITIES_FILE.exists():
        print("暂无活动数据")
        return
    
    with open(ACTIVITIES_FILE, 'r', encoding='utf-8') as f:
        activities = json.load(f)
    
    activities.sort(key=lambda x: x.get('startTimeGMT', ''), reverse=True)
    
    print("\n📋 **最近活动**\n")
    for a in activities[:10]:
        name = a.get('activityName', '未知')
        date = a.get('startTimeLocal', '')[:10] if a.get('startTimeLocal') else '未知'
        dist = a.get('distance', 0) / 1000
        duration = a.get('duration', 0) / 60
        print(f"  {date} | {name} | {dist:.1f}km | {duration:.0f}min")


def main():
    if len(sys.argv) < 2:
        print("""
🛰️ **Garmin 同步工具 v2**

用法:
  python3 garmin_sync.py setup <邮箱> <密码>
    设置 Garmin 账号

  python3 garmin_sync.py sync
    同步活动数据（带重试）

  python3 garmin_sync.py summary
    查看活动统计

  python3 garmin_sync.py recent
    查看最近活动
""")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "setup":
        if len(sys.argv) < 4:
            print("用法: python3 garmin_sync.py setup <邮箱> <密码>")
        else:
            save_credentials(sys.argv[2], sys.argv[3])
            print(f"✅ 已保存 Garmin 账号: {sys.argv[2]}")
    
    elif cmd == "sync":
        sync_with_retry()
    
    elif cmd == "summary":
        show_summary()
    
    elif cmd == "recent":
        show_recent()
    
    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
