#!/usr/bin/env python3
"""
课表解析脚本
支持多种输入格式，自动识别空闲时段
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# 配置
MEMORY_DIR = Path(__file__).parent.parent.parent.parent / "memory" / "student"
SCHEDULE_FILE = MEMORY_DIR / "schedule.json"

# 常量
DAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
DAY_START = "07:00"
DAY_END = "22:00"
MIN_SLOT_DURATION = 30  # 最小空闲时段（分钟）


def ensure_memory_dir():
    """确保存储目录存在"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def parse_time(time_str: str) -> str:
    """将各种时间格式标准化为 HH:MM"""
    time_str = time_str.strip()
    
    # 已经是标准格式
    if re.match(r"^\d{1,2}:\d{2}$", time_str):
        hour, minute = time_str.split(":")
        return f"{int(hour):02d}:{minute}"
    
    # 中文格式：上午8点、下午2点
    patterns = [
        (r"上午\s*(\d{1,2})\s*点?", lambda m: int(m.group(1))),
        (r"下午\s*(\d{1,2})\s*点?", lambda m: int(m.group(1)) + 12 if int(m.group(1)) != 12 else 12),
        (r"晚上\s*(\d{1,2})\s*点?", lambda m: int(m.group(1)) + 12 if int(m.group(1)) != 12 else 12),
        (r"(\d{1,2})\s*点", lambda m: int(m.group(1))),
    ]
    
    for pattern, extractor in patterns:
        match = re.search(pattern, time_str)
        if match:
            hour = extractor(match)
            return f"{hour:02d}:00"
    
    # 默认返回原值
    return time_str


def parse_course_line(line: str) -> Optional[Dict]:
    """解析单行课程信息"""
    line = line.strip()
    if not line or line.startswith("|") or line.startswith("-"):
        return None
    
    # 格式：周一 8:00-9:35 高等数学 教学楼A101
    pattern = r"(周[一二三四五六日])\s+(\d{1,2}:\d{2})\s*[-~]\s*(\d{1,2}:\d{2})\s+(.+?)\s+(.+)"
    match = re.match(pattern, line)
    
    if match:
        return {
            "day": match.group(1),
            "start": parse_time(match.group(2)),
            "end": parse_time(match.group(3)),
            "name": match.group(4).strip(),
            "location": match.group(5).strip()
        }
    
    # 格式：周一下午2点-4点 高等数学
    pattern2 = r"(周[一二三四五六日])\s*(上午|下午|晚上)?\s*(\d{1,2})\s*点?\s*[-~]\s*(\d{1,2})\s*点?\s+(.+)"
    match2 = re.match(pattern2, line)
    
    if match2:
        day = match2.group(1)
        period = match2.group(2) or ""
        start_hour = int(match2.group(3))
        end_hour = int(match2.group(4))
        name = match2.group(5).strip()
        
        # 处理上午/下午/晚上
        if period == "下午" or period == "晚上":
            if start_hour != 12:
                start_hour += 12
            if end_hour != 12:
                end_hour += 12
        
        return {
            "day": day,
            "start": f"{start_hour:02d}:00",
            "end": f"{end_hour:02d}:00",
            "name": name,
            "location": "待定"
        }
    
    return None


def time_to_minutes(time_str: str) -> int:
    """将时间字符串转换为分钟数"""
    hour, minute = map(int, time_str.split(":"))
    return hour * 60 + minute


def minutes_to_time(minutes: int) -> str:
    """将分钟数转换为时间字符串"""
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"


def calculate_free_slots(courses: List[Dict]) -> Dict[str, List[Dict]]:
    """计算每天的空闲时段"""
    free_slots = {}
    
    for day in DAY_NAMES[:5]:  # 默认周一到周五
        # 获取当天的课程，按开始时间排序
        day_courses = [c for c in courses if c["day"] == day]
        day_courses.sort(key=lambda c: time_to_minutes(c["start"]))
        
        slots = []
        day_start_min = time_to_minutes(DAY_START)
        day_end_min = time_to_minutes(DAY_END)
        
        current_start = day_start_min
        
        for course in day_courses:
            course_start = time_to_minutes(course["start"])
            course_end = time_to_minutes(course["end"])
            
            # 检查课程前的空闲时段
            if course_start > current_start:
                duration = course_start - current_start
                if duration >= MIN_SLOT_DURATION:
                    slots.append({
                        "start": minutes_to_time(current_start),
                        "end": minutes_to_time(course_start),
                        "duration": duration
                    })
            
            current_start = max(current_start, course_end)
        
        # 最后一个课程后的空闲时段
        if current_start < day_end_min:
            duration = day_end_min - current_start
            if duration >= MIN_SLOT_DURATION:
                slots.append({
                    "start": minutes_to_time(current_start),
                    "end": minutes_to_time(day_end_min),
                    "duration": duration
                })
        
        free_slots[day] = slots
    
    return free_slots


def import_schedule(text: str) -> Dict:
    """导入课表文本"""
    ensure_memory_dir()
    
    courses = []
    lines = text.strip().split("\n")
    
    for line in lines:
        course = parse_course_line(line)
        if course:
            courses.append(course)
    
    if not courses:
        return {"success": False, "error": "未能识别任何课程信息"}
    
    # 计算空闲时段
    free_slots = calculate_free_slots(courses)
    
    # 构建数据结构
    schedule_data = {
        "version": "1.0",
        "lastUpdated": datetime.now().isoformat(),
        "courses": courses,
        "freeSlots": free_slots
    }
    
    # 保存到文件
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedule_data, f, ensure_ascii=False, indent=2)
    
    # 统计信息
    total_hours = sum(
        time_to_minutes(c["end"]) - time_to_minutes(c["start"])
        for c in courses
    ) / 60
    
    return {
        "success": True,
        "courseCount": len(courses),
        "totalHours": round(total_hours, 1),
        "freeSlotsSummary": {
            day: len(slots) for day, slots in free_slots.items() if slots
        }
    }


def get_today_schedule() -> Optional[Dict]:
    """获取今日课表"""
    if not SCHEDULE_FILE.exists():
        return None
    
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 获取今天是周几
    today = datetime.now()
    weekday = today.weekday()  # 0=周一
    day_name = DAY_NAMES[weekday]
    
    # 获取今天的课程
    today_courses = [c for c in data["courses"] if c["day"] == day_name]
    
    return {
        "date": today.strftime("%Y-%m-%d"),
        "day": day_name,
        "courses": today_courses,
        "freeSlots": data["freeSlots"].get(day_name, [])
    }


def get_free_slots_for_day(day: str) -> List[Dict]:
    """获取指定日期的空闲时段"""
    if not SCHEDULE_FILE.exists():
        return []
    
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data["freeSlots"].get(day, [])


if __name__ == "__main__":
    # 测试用例
    test_input = """
周一 8:00-9:35 高等数学 教学楼A101
周一 10:00-11:35 大学英语 教学楼B203
周二 14:00-15:35 线性代数 教学楼A102
周三 8:00-9:35 大学物理 实验楼301
"""
    
    result = import_schedule(test_input)
    print(json.dumps(result, ensure_ascii=False, indent=2))
