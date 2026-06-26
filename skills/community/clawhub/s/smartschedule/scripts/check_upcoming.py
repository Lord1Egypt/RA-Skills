#!/usr/bin/env python3
"""
QQ 即时提醒检查脚本
查询即将在 15-20 分钟内开始的日程，输出提醒内容。
由 OpenClaw cron 定时调用（每 5 分钟），通过 QQ Bot 通道推送。
"""

import json
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from schedule_manager import init_db, get_due_soon, mark_reminded

DATE_FMT = "%Y-%m-%d %H:%M"


def format_reminder(schedules):
    """格式化即将开始的日程为提醒消息。"""
    if not schedules:
        return None

    lines = ["⏰ 日程提醒！以下日程即将开始：", ""]
    for s in schedules:
        start = datetime.strptime(s["start_time"], DATE_FMT)
        now = datetime.now()
        minutes_left = int((start - now).total_seconds() / 60)
        loc = f" | 📍 {s['location']}" if s.get("location") else ""
        lines.append(f"📅 {s['title']}")
        lines.append(f"   ⏰ {s['start_time']} (约 {minutes_left} 分钟后开始){loc}")
        if s.get("description"):
            lines.append(f"   📝 {s['description']}")
        lines.append("")

    lines.append("请做好准备！")
    return "\n".join(lines)


def main():
    init_db()
    schedules = get_due_soon(minutes=20)

    if not schedules:
        print(json.dumps({"status": "no_upcoming", "time": datetime.now().strftime(DATE_FMT)}, ensure_ascii=False))
        return

    reminder_text = format_reminder(schedules)

    for s in schedules:
        mark_reminded(s["id"])

    result = {
        "status": "reminders_sent",
        "count": len(schedules),
        "message": reminder_text,
        "schedules": [{"id": s["id"], "title": s["title"], "start_time": s["start_time"]} for s in schedules],
        "time": datetime.now().strftime(DATE_FMT),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
