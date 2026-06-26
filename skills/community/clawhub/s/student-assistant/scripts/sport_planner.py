#!/usr/bin/env python3
"""
运动计划生成脚本
根据天气、课表空闲、体能情况自动安排运动
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

# 配置
MEMORY_DIR = Path(__file__).parent.parent.parent.parent / "memory" / "student"
SCHEDULE_FILE = MEMORY_DIR / "schedule.json"
SPORT_PLAN_FILE = MEMORY_DIR / "sport-plan.json"
REVIEW_PLAN_FILE = MEMORY_DIR / "review-plan.json"

# 运动类型库
SPORT_TYPES = {
    "low": [
        {"name": "拉伸", "duration": 15, "location": "宿舍", "intensity": "低", "weather": ["any"]},
        {"name": "散步", "duration": 20, "location": "校园", "intensity": "低", "weather": ["晴", "阴"]},
        {"name": "瑜伽", "duration": 25, "location": "宿舍/健身房", "intensity": "低", "weather": ["any"]},
    ],
    "medium": [
        {"name": "慢跑", "duration": 30, "location": "操场", "intensity": "中", "weather": ["晴", "阴"]},
        {"name": "游泳", "duration": 40, "location": "游泳馆", "intensity": "中", "weather": ["any"]},
        {"name": "骑行", "duration": 45, "location": "校园/公园", "intensity": "中", "weather": ["晴", "阴"]},
        {"name": "健身", "duration": 45, "location": "健身房", "intensity": "中", "weather": ["any"]},
    ],
    "high": [
        {"name": "跑步", "duration": 50, "location": "操场", "intensity": "高", "weather": ["晴", "阴"]},
        {"name": "球类运动", "duration": 60, "location": "球场", "intensity": "高", "weather": ["晴", "阴"]},
    ]
}

# 最佳运动时段（优先级排序）
PREFERRED_TIMES = [
    {"start": "17:00", "end": "19:00", "priority": 1, "note": "傍晚最佳运动时间"},
    {"start": "06:00", "end": "07:30", "priority": 2, "note": "晨间轻量运动"},
    {"start": "20:00", "end": "21:00", "priority": 3, "note": "晚间轻度运动"},
    {"start": "14:00", "end": "16:00", "priority": 4, "note": "午后，避免剧烈运动"},
]


def ensure_memory_dir():
    """确保存储目录存在"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def time_to_minutes(time_str: str) -> int:
    """将时间字符串转换为分钟数"""
    hour, minute = map(int, time_str.split(":"))
    return hour * 60 + minute


def minutes_to_time(minutes: int) -> str:
    """将分钟数转换为时间字符串"""
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"


def get_weather() -> str:
    """
    获取天气信息
    实际使用时应该调用天气技能
    这里返回默认值
    """
    # TODO: 集成天气技能
    return "晴"


def is_exam_week() -> bool:
    """检查是否在考试周（考试前7天）"""
    if not REVIEW_PLAN_FILE.exists():
        return False
    
    with open(REVIEW_PLAN_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    exam_date_str = data.get("examDate")
    if not exam_date_str:
        return False
    
    exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
    today = datetime.now()
    
    days_to_exam = (exam_date - today).days
    return 0 < days_to_exam <= 7


def select_sport_type(
    intensity: str,
    weather: str,
    duration_available: int,
    is_exam_week: bool
) -> Optional[Dict]:
    """
    根据条件选择合适的运动类型
    
    Args:
        intensity: 期望强度 ("low", "medium", "high")
        weather: 天气 ("晴", "阴", "雨", "any")
        duration_available: 可用时长（分钟）
        is_exam_week: 是否在考试周
    
    Returns:
        选中的运动类型
    """
    # 考试周降低强度
    if is_exam_week and intensity != "low":
        intensity = "low"
    
    candidates = SPORT_TYPES.get(intensity, SPORT_TYPES["low"])
    
    # 筛选符合条件的运动
    suitable = []
    for sport in candidates:
        # 检查时长
        if sport["duration"] > duration_available:
            continue
        
        # 检查天气
        if "any" not in sport["weather"] and weather not in sport["weather"]:
            continue
        
        suitable.append(sport)
    
    if suitable:
        return suitable[0]  # 返回第一个符合条件的
    
    # 如果没有合适的，返回低强度运动
    for sport in SPORT_TYPES["low"]:
        if sport["duration"] <= duration_available:
            return sport
    
    return None


def find_sport_slot(
    free_slots: List[Dict],
    preferred_times: List[Dict] = None
) -> Optional[Dict]:
    """
    从空闲时段中找到最适合运动的时段
    
    Args:
        free_slots: 空闲时段列表
        preferred_times: 优先时段列表
    
    Returns:
        {"start": "18:00", "end": "19:00", "duration": 60, "priority": 1, "note": "..."}
    """
    preferred_times = preferred_times or PREFERRED_TIMES
    
    best_slot = None
    best_priority = float("inf")
    
    for pref in preferred_times:
        pref_start = time_to_minutes(pref["start"])
        pref_end = time_to_minutes(pref["end"])
        
        for slot in free_slots:
            slot_start = time_to_minutes(slot["start"])
            slot_end = time_to_minutes(slot["end"])
            
            # 检查是否重叠
            overlap_start = max(slot_start, pref_start)
            overlap_end = min(slot_end, pref_end)
            
            if overlap_end > overlap_start:
                duration = overlap_end - overlap_start
                
                # 至少需要30分钟
                if duration >= 30 and pref["priority"] < best_priority:
                    best_slot = {
                        "start": minutes_to_time(overlap_start),
                        "end": minutes_to_time(overlap_end),
                        "duration": duration,
                        "priority": pref["priority"],
                        "note": pref["note"]
                    }
                    best_priority = pref["priority"]
    
    return best_slot


def generate_sport_plan(
    days_ahead: int = 7,
    target_intensity: str = "medium",
    frequency: int = None
) -> Dict:
    """
    生成运动计划
    
    Args:
        days_ahead: 生成未来多少天的计划
        target_intensity: 目标强度
        frequency: 每周运动次数（默认3次，考试周1-2次）
    
    Returns:
        运动计划数据结构
    """
    ensure_memory_dir()
    
    # 确定运动频率
    is_exam = is_exam_week()
    if frequency is None:
        frequency = 2 if is_exam else 3
    
    # 获取天气
    weather = get_weather()
    
    # 读取课表
    free_slots_by_day = {}
    if SCHEDULE_FILE.exists():
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            schedule_data = json.load(f)
            free_slots_by_day = schedule_data.get("freeSlots", {})
    
    # 生成计划
    day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    plan = []
    sport_days = 0
    
    today = datetime.now()
    week_num = today.isocalendar()[1]
    
    for i in range(days_ahead):
        if sport_days >= frequency:
            break
        
        target_date = today + timedelta(days=i)
        day_name = day_names[target_date.weekday()]
        
        # 获取当天空闲时段
        free_slots = free_slots_by_day.get(day_name, [])
        
        # 找到适合运动的时段
        sport_slot = find_sport_slot(free_slots)
        
        if sport_slot:
            # 选择运动类型
            sport = select_sport_type(
                intensity=target_intensity,
                weather=weather,
                duration_available=sport_slot["duration"],
                is_exam_week=is_exam
            )
            
            if sport:
                plan.append({
                    "date": target_date.strftime("%Y-%m-%d"),
                    "day": day_name,
                    "time": f"{sport_slot['start']}-{minutes_to_time(time_to_minutes(sport_slot['start']) + sport['duration'])}",
                    "type": sport["name"],
                    "duration": sport["duration"],
                    "intensity": sport["intensity"],
                    "location": sport["location"],
                    "note": sport_slot["note"] + ("，考试周轻量运动" if is_exam else "")
                })
                sport_days += 1
    
    # 构建结果
    result = {
        "success": True,
        "week": f"{today.year}-W{week_num:02d}",
        "generatedAt": today.isoformat(),
        "isExamWeek": is_exam,
        "weather": weather,
        "frequency": len(plan),
        "plan": plan
    }
    
    # 保存到文件
    with open(SPORT_PLAN_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result


def get_today_sport() -> Optional[Dict]:
    """获取今日运动计划"""
    if not SPORT_PLAN_FILE.exists():
        return None
    
    with open(SPORT_PLAN_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    for item in data.get("plan", []):
        if item["date"] == today:
            return item
    
    return None


def get_sport_plan() -> Optional[Dict]:
    """获取当前的运动计划"""
    if not SPORT_PLAN_FILE.exists():
        return None
    
    with open(SPORT_PLAN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    # 测试用例
    result = generate_sport_plan(days_ahead=7, target_intensity="medium")
    print(json.dumps(result, ensure_ascii=False, indent=2))