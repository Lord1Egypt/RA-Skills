#!/usr/bin/env python3
"""
今日日程汇总脚本
汇总今日上课、空闲、复习任务、运动计划
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 配置
MEMORY_DIR = Path(__file__).parent.parent.parent.parent / "memory" / "student"
SCHEDULE_FILE = MEMORY_DIR / "schedule.json"
REVIEW_PLAN_FILE = MEMORY_DIR / "review-plan.json"
SPORT_PLAN_FILE = MEMORY_DIR / "sport-plan.json"

DAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def time_to_minutes(time_str: str) -> int:
    """将时间字符串转换为分钟数"""
    try:
        hour, minute = map(int, time_str.split(":"))
        return hour * 60 + minute
    except:
        return 0


def format_duration(minutes: int) -> str:
    """格式化时长"""
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0 and mins > 0:
        return f"{hours}小时{mins}分钟"
    elif hours > 0:
        return f"{hours}小时"
    else:
        return f"{mins}分钟"


def get_today_schedule() -> Optional[Dict]:
    """获取今日课表"""
    if not SCHEDULE_FILE.exists():
        return None
    
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    today = datetime.now()
    day_name = DAY_NAMES[today.weekday()]
    
    courses = [c for c in data.get("courses", []) if c["day"] == day_name]
    courses.sort(key=lambda c: time_to_minutes(c["start"]))
    
    return {
        "date": today.strftime("%Y-%m-%d"),
        "day": day_name,
        "courses": courses
    }


def get_today_review_tasks() -> List[Dict]:
    """获取今日复习任务"""
    if not REVIEW_PLAN_FILE.exists():
        return []
    
    with open(REVIEW_PLAN_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    for day_plan in data.get("plan", []):
        if day_plan["date"] == today:
            return day_plan.get("tasks", [])
    
    return []


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


def generate_daily_summary() -> Dict:
    """
    生成今日日程汇总
    
    Returns:
        包含所有日程项的字典
    """
    today = datetime.now()
    day_name = DAY_NAMES[today.weekday()]
    
    # 收集所有日程项
    schedule_items = []
    
    # 1. 课程
    schedule_data = get_today_schedule()
    if schedule_data and schedule_data.get("courses"):
        for course in schedule_data["courses"]:
            schedule_items.append({
                "type": "course",
                "start": course["start"],
                "end": course["end"],
                "title": course["name"],
                "location": course.get("location", ""),
                "icon": "📖"
            })
    
    # 2. 复习任务
    review_tasks = get_today_review_tasks()
    for task in review_tasks:
        schedule_items.append({
            "type": "review",
            "start": task.get("start", ""),
            "end": task.get("end", ""),
            "title": task.get("content", ""),
            "icon": "📚"
        })
    
    # 3. 运动计划
    sport = get_today_sport()
    if sport:
        time_parts = sport.get("time", "").split("-")
        schedule_items.append({
            "type": "sport",
            "start": time_parts[0] if time_parts else "",
            "end": time_parts[1] if len(time_parts) > 1 else "",
            "title": f"{sport['type']} ({sport['duration']}分钟)",
            "location": sport.get("location", ""),
            "icon": "🏃"
        })
    
    # 按时间排序
    schedule_items.sort(key=lambda x: time_to_minutes(x.get("start", "00:00")))
    
    # 计算统计信息
    stats = {
        "courseHours": 0,
        "studyHours": 0,
        "sportHours": 0
    }
    
    for item in schedule_items:
        duration = time_to_minutes(item.get("end", "00:00")) - time_to_minutes(item.get("start", "00:00"))
        if item["type"] == "course":
            stats["courseHours"] += duration
        elif item["type"] == "review":
            stats["studyHours"] += duration
        elif item["type"] == "sport":
            stats["sportHours"] += duration
    
    # 转换为小时
    stats["courseHours"] = round(stats["courseHours"] / 60, 1)
    stats["studyHours"] = round(stats["studyHours"] / 60, 1)
    stats["sportHours"] = round(stats["sportHours"] / 60, 1)
    
    return {
        "success": True,
        "date": today.strftime("%Y-%m-%d"),
        "day": day_name,
        "items": schedule_items,
        "stats": stats
    }


def format_summary_text(summary: Dict) -> str:
    """
    格式化为文本输出
    
    Args:
        summary: 日程汇总数据
    
    Returns:
        格式化的文本
    """
    lines = []
    
    # 标题
    lines.append(f"📆 今日日程 ({summary['day']} {summary['date']})")
    lines.append("")
    
    if not summary.get("items"):
        lines.append("今日暂无安排 🎉")
        return "\n".join(lines)
    
    # 日程项
    for item in summary["items"]:
        time_range = f"{item['start']}-{item['end']}" if item.get("start") else ""
        icon = item.get("icon", "📌")
        title = item.get("title", "")
        location = f" ({item['location']})" if item.get("location") else ""
        
        lines.append(f"{time_range}  {icon} {title}{location}")
    
    # 统计信息
    stats = summary.get("stats", {})
    if any(v > 0 for v in stats.values()):
        lines.append("")
        lines.append("📊 今日统计：")
        if stats.get("courseHours", 0) > 0:
            lines.append(f"  • 上课：{stats['courseHours']}课时")
        if stats.get("studyHours", 0) > 0:
            lines.append(f"  • 自习：{stats['studyHours']}小时")
        if stats.get("sportHours", 0) > 0:
            lines.append(f"  • 运动：{stats['sportHours']}小时")
    
    return "\n".join(lines)


if __name__ == "__main__":
    summary = generate_daily_summary()
    print(format_summary_text(summary))