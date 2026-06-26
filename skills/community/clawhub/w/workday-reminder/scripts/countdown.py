#!/usr/bin/env python3
"""
下班倒计时计算脚本
计算当前时间到下班时间的剩余时间（支持工作日和周末区分）
"""

import sys
import json
from datetime import datetime, timedelta, date

def get_next_workday_offtime(off_time_str="17:30"):
    """
    计算下一个工作日的下班时间
    """
    today = date.today()
    weekday = today.weekday()  # 0=Monday, 6=Sunday

    # 如果是周六或周日，下一个工作日是周一
    if weekday >= 5:  # Saturday or Sunday
        days_until_monday = (7 - weekday) % 7
        next_workday = today + timedelta(days=days_until_monday if days_until_monday > 0 else 7)
        off_datetime = datetime.combine(next_workday, datetime.strptime(off_time_str, "%H:%M").time())
        return off_datetime, "weekend"
    else:
        # 今天是工作日
        off_datetime = datetime.combine(today, datetime.strptime(off_time_str, "%H:%M").time())
        return off_datetime, "workday"

def format_countdown(seconds):
    """
    格式化剩余时间
    """
    if seconds < 0:
        return "已经下班"

    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    if days > 0:
        return f"{days}天{hours}小时{minutes}分钟"
    elif hours > 0:
        return f"{hours}小时{minutes}分钟"
    else:
        return f"{minutes}分钟"

def main():
    # 解析参数
    offtime = "17:30"
    for arg in sys.argv[1:]:
        if arg.startswith("--offtime="):
            offtime = arg.split("=", 1)[1]
        elif arg.startswith("--offtime"):
            if "=" in arg:
                offtime = arg.split("=", 1)[1]

    # 获取当前时间（上海时区）
    now = datetime.now()
    off_datetime, day_type = get_next_workday_offtime(offtime)

    # 计算剩余时间
    if day_type == "workday":
        # 检查是否已经过了今天的下班时间
        if now.time() >= off_datetime.time():
            # 已经过下班时间，计算下一个工作日的下班时间
            weekday = date.today().weekday()
            days_until_next = 1 if weekday < 4 else 7 - weekday  # Mon-Thu: +1, Fri: +3 (to Monday)
            next_workday = date.today() + timedelta(days=days_until_next)
            off_datetime = datetime.combine(next_workday, off_datetime.time())
            delta = off_datetime - now
            already_off = True
        else:
            delta = datetime.combine(date.today(), off_datetime.time()) - now
            already_off = False
    else:  # weekend
        delta = off_datetime - now
        already_off = False

    seconds = int(delta.total_seconds())

    # 获取星期几
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_str = weekdays[now.weekday()]

    # 获取日期
    date_str = now.strftime("%Y年%m月%d日")

    # 生成消息
    if day_type == "workday":
        if already_off:
            message = f"🎉 今天已经下班啦！\n📅 {date_str} {weekday_str}\n💤 好好休息，明天见~"
        else:
            countdown_str = format_countdown(seconds)
            message = f"🕐 {date_str} {weekday_str}，下班时间 {offtime}\n⏰ 距离下班还有：{countdown_str}\n💪 加油，马上就可以下班啦！"
    else:  # weekend
        countdown_str = format_countdown(seconds)
        message = f"😌 {date_str} {weekday_str}，不用上班哦~\n📅 距离下个工作日下班还有：{countdown_str}"

    # 返回 JSON 结果
    result = {
        "today": "工作日" if day_type == "workday" else "周末",
        "date": date_str,
        "weekday": weekday_str,
        "current_time": now.strftime("%H:%M"),
        "off_time": offtime,
        "countdown": format_countdown(seconds),
        "already_off": already_off if day_type == "workday" else False,
        "message": message
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
