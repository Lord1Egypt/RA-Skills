#!/usr/bin/env python3
"""
复习计划生成脚本
根据考试时间、薄弱科目、空闲时长生成可执行的每日复习任务
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

# 配置
MEMORY_DIR = Path(__file__).parent.parent.parent.parent / "memory" / "student"
SCHEDULE_FILE = MEMORY_DIR / "schedule.json"
EXAMS_FILE = MEMORY_DIR / "exams.json"
REVIEW_PLAN_FILE = MEMORY_DIR / "review-plan.json"

# 常量
DEFAULT_DAILY_STUDY_HOURS = 3  # 默认每天学习时长
MIN_SESSION_DURATION = 30  # 最小学习时段（分钟）
TASK_TYPES = {
    "review": {"name": "复习知识点", "duration_ratio": 0.3},
    "practice": {"name": "刷题练习", "duration_ratio": 0.5},
    "summary": {"name": "总结整理", "duration_ratio": 0.2}
}


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


def get_available_study_time(free_slots: List[Dict], max_hours: float = 4) -> List[Dict]:
    """
    从空闲时段中提取适合学习的时段
    返回格式: [{"start": "14:00", "end": "17:00", "duration": 180}, ...]
    """
    study_slots = []
    remaining_max = max_hours * 60
    
    for slot in free_slots:
        if remaining_max <= 0:
            break
        
        duration = min(slot["duration"], remaining_max)
        if duration >= MIN_SESSION_DURATION:
            study_slots.append({
                "start": slot["start"],
                "end": minutes_to_time(time_to_minutes(slot["start"]) + duration),
                "duration": duration
            })
            remaining_max -= duration
    
    return study_slots


def split_into_tasks(duration_minutes: int, subject: str, chapter: str) -> List[Dict]:
    """
    将学习时长拆分为具体任务
    """
    tasks = []
    remaining = duration_minutes
    
    # 按比例分配时间
    for task_type, config in TASK_TYPES.items():
        task_duration = int(duration_minutes * config["duration_ratio"])
        if task_duration >= 15:  # 至少15分钟
            tasks.append({
                "type": task_type,
                "content": f"{chapter} {config['name']}",
                "duration": task_duration
            })
            remaining -= task_duration
    
    # 剩余时间加到最后一个任务
    if remaining > 0 and tasks:
        tasks[-1]["duration"] += remaining
    
    return tasks


def generate_review_plan(
    subject: str,
    exam_date: str,
    chapters: List[str],
    weak_chapters: List[str] = None,
    daily_hours: float = None
) -> Dict:
    """
    生成复习计划
    
    Args:
        subject: 科目名称
        exam_date: 考试日期 (YYYY-MM-DD)
        chapters: 所有章节列表
        weak_chapters: 薄弱章节列表
        daily_hours: 每天学习时长
    
    Returns:
        复习计划数据结构
    """
    ensure_memory_dir()
    
    # 计算剩余天数
    exam = datetime.strptime(exam_date, "%Y-%m-%d")
    today = datetime.now()
    days_remaining = (exam - today).days
    
    if days_remaining <= 0:
        return {"success": False, "error": "考试日期已过或为今天"}
    
    # 确定每天学习时长
    daily_hours = daily_hours or DEFAULT_DAILY_STUDY_HOURS
    
    # 读取课表获取空闲时段
    free_slots_by_day = {}
    if SCHEDULE_FILE.exists():
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            schedule_data = json.load(f)
            free_slots_by_day = schedule_data.get("freeSlots", {})
    
    # 计算总可用时间
    total_available_hours = 0
    day_plans = []
    
    day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    for i in range(days_remaining):
        target_date = today + timedelta(days=i)
        day_name = day_names[target_date.weekday()]
        
        # 获取当天空闲时段
        free_slots = free_slots_by_day.get(day_name, [])
        study_slots = get_available_study_time(free_slots, daily_hours)
        
        if study_slots:
            day_plan = {
                "date": target_date.strftime("%Y-%m-%d"),
                "day": day_name,
                "slots": study_slots,
                "totalMinutes": sum(s["duration"] for s in study_slots)
            }
            total_available_hours += day_plan["totalMinutes"] / 60
            day_plans.append(day_plan)
    
    # 分配章节到每一天
    weak_chapters = weak_chapters or []
    
    # 章节优先级：薄弱 > 普通
    prioritized_chapters = []
    for ch in weak_chapters:
        if ch in chapters:
            prioritized_chapters.append({"name": ch, "priority": 2, "hours": 2})
    
    for ch in chapters:
        if ch not in weak_chapters:
            prioritized_chapters.append({"name": ch, "priority": 1, "hours": 1.5})
    
    # 生成每日任务
    plan = []
    chapter_index = 0
    current_chapter = prioritized_chapters[0] if prioritized_chapters else None
    chapter_remaining = current_chapter["hours"] * 60 if current_chapter else 0
    
    for day_plan in day_plans:
        daily_tasks = []
        for slot in day_plan["slots"]:
            if not current_chapter:
                break
            
            # 为这个时段生成任务
            slot_duration = slot["duration"]
            tasks = split_into_tasks(
                min(slot_duration, chapter_remaining),
                subject,
                current_chapter["name"]
            )
            
            # 添加时间信息
            current_time = time_to_minutes(slot["start"])
            for task in tasks:
                task["start"] = minutes_to_time(current_time)
                task["end"] = minutes_to_time(current_time + task["duration"])
                del task["duration"]
                daily_tasks.append(task)
                current_time += task["duration"] if "duration" in task else 30
            
            chapter_remaining -= slot_duration
            
            # 切换到下一个章节
            if chapter_remaining <= 0:
                chapter_index += 1
                if chapter_index < len(prioritized_chapters):
                    current_chapter = prioritized_chapters[chapter_index]
                    chapter_remaining = current_chapter["hours"] * 60
                else:
                    current_chapter = None
        
        if daily_tasks:
            plan.append({
                "date": day_plan["date"],
                "day": day_plan["day"],
                "tasks": daily_tasks
            })
    
    # 构建结果
    result = {
        "success": True,
        "subject": subject,
        "examDate": exam_date,
        "daysRemaining": days_remaining,
        "totalHours": round(total_available_hours, 1),
        "plan": plan
    }
    
    # 保存到文件
    with open(REVIEW_PLAN_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result


def get_review_plan() -> Optional[Dict]:
    """获取当前的复习计划"""
    if not REVIEW_PLAN_FILE.exists():
        return None
    
    with open(REVIEW_PLAN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def add_exam(
    subject: str,
    date: str,
    time: str = None,
    location: str = None
) -> Dict:
    """添加考试信息"""
    ensure_memory_dir()
    
    exams = []
    if EXAMS_FILE.exists():
        with open(EXAMS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            exams = data.get("exams", [])
    
    # 检查是否已存在
    for exam in exams:
        if exam["subject"] == subject and exam["date"] == date:
            return {"success": False, "error": "该考试已存在"}
    
    exam = {
        "subject": subject,
        "date": date,
        "time": time,
        "location": location,
        "status": "upcoming",
        "addedAt": datetime.now().isoformat()
    }
    
    exams.append(exam)
    exams.sort(key=lambda e: e["date"])
    
    with open(EXAMS_FILE, "w", encoding="utf-8") as f:
        json.dump({"exams": exams}, f, ensure_ascii=False, indent=2)
    
    return {"success": True, "exam": exam}


if __name__ == "__main__":
    # 测试用例
    result = generate_review_plan(
        subject="高等数学",
        exam_date="2024-01-20",
        chapters=["极限与连续", "导数与微分", "积分", "微分方程"],
        weak_chapters=["积分"],
        daily_hours=3
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
