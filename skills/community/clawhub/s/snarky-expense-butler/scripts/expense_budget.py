#!/usr/bin/env python3
# 消费预算检查工具

import json
import sys
import os
import datetime
from datetime import timedelta

DATA_FILE = os.environ.get('EXPENSE_DATA_FILE', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expense_records.json'))

def load_data():
    """加载消费记录数据"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ 消费记录文件不存在")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ 消费记录文件格式错误")
        sys.exit(1)

def get_status_emoji(percentage):
    """根据百分比返回状态emoji"""
    if percentage > 100:
        return "🚨 超支"
    elif percentage > 80:
        return "⚠️ 接近预算"
    else:
        return "✅ 正常"

def check_today():
    """检查今日预算"""
    data = load_data()
    budget = data['settings'].get('budget', {})
    daily_budget = budget.get('daily', 500)

    today = datetime.datetime.now()
    today_str = today.strftime('%Y-%m-%d')

    today_total = 0
    for record in data['records']:
        if record['date'] == today_str:
            today_total = round(sum(-item['amount'] for item in record['items']), 2)
            break

    remaining = round(daily_budget - today_total, 2)
    percentage = round((today_total / daily_budget * 100), 1) if daily_budget > 0 else 0
    status = get_status_emoji(percentage)

    # 计算今日预计（基于当前时间和已消费）
    current_hour = today.hour + today.minute / 60.0
    day_progress = current_hour / 24.0 if current_hour > 0 else 0.01
    if day_progress > 0:
        projected = today_total / day_progress
    else:
        projected = today_total

    hours_left = 24 - current_hour
    daily_avg_suggest = remaining / hours_left if hours_left > 0 else 0

    print(f"📊 今日预算状态 ({today_str})")
    print(f"━━━━━━━━━━━━━━━━━━")
    print(f"预算: ¥{round(daily_budget, 2)} | 已用: ¥{round(abs(today_total), 2)} | 剩余: ¥{round(remaining, 2)}")
    print(f"状态: {status} ({percentage}%)")
    print(f"若保持当前节奏，今日预计: ¥{round(projected, 0)}")

def check_week():
    """检查本周预算"""
    data = load_data()
    budget = data['settings'].get('budget', {})
    weekly_budget = budget.get('weekly', 3000)

    today = datetime.datetime.now()
    # 本周一
    start_of_week = today - timedelta(days=today.weekday())
    week_dates = [(start_of_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    week_total = 0
    days_with_record = 0
    for record in data['records']:
        if record['date'] in week_dates:
            week_total += record['total']
            days_with_record += 1

    remaining = weekly_budget - week_total
    percentage = (week_total / weekly_budget * 100) if weekly_budget > 0 else 0
    status = get_status_emoji(percentage)

    days_passed = today.weekday() + 1  # 周一=1 ... 周日=7
    days_left = 7 - days_passed

    if days_passed > 0:
        projected = week_total / days_passed * 7
    else:
        projected = week_total

    daily_avg = remaining / days_left if days_left > 0 else 0

    print(f"📊 本周预算状态 ({week_dates[0]} ~ {week_dates[-1]})")
    print(f"━━━━━━━━━━━━━━━━━━")
    print(f"预算: ¥{weekly_budget} | 已用: ¥{abs(week_total):.1f} | 剩余: ¥{remaining:.1f}")
    print(f"状态: {status} ({percentage:.1f}%)")
    print(f"已过 {days_passed} 天 / 剩余 {days_left} 天")
    print(f"日均可用: ¥{daily_avg:.0f} | 若保持节奏，本周预计: ¥{projected:.0f}")

def check_month():
    """检查本月预算"""
    data = load_data()
    budget = data['settings'].get('budget', {})
    monthly_budget = budget.get('monthly', 12000)

    today = datetime.datetime.now()
    month_str = today.strftime('%Y-%m')

    month_total = 0
    days_with_record = set()
    for record in data['records']:
        if record['date'].startswith(month_str):
            month_total += record['total']
            days_with_record.add(record['date'])

    remaining = monthly_budget - month_total
    percentage = (month_total / monthly_budget * 100) if monthly_budget > 0 else 0
    status = get_status_emoji(percentage)

    # 本月天数
    import calendar
    _, days_in_month = calendar.monthrange(today.year, today.month)
    days_passed = today.day
    days_left = days_in_month - days_passed

    if days_passed > 0:
        projected = month_total / days_passed * days_in_month
    else:
        projected = month_total

    daily_avg = remaining / days_left if days_left > 0 else 0

    print(f"📊 本月预算状态 ({month_str})")
    print(f"━━━━━━━━━━━━━━━━━━")
    print(f"预算: ¥{monthly_budget} | 已用: ¥{abs(month_total):.1f} | 剩余: ¥{remaining:.1f}")
    print(f"状态: {status} ({percentage:.1f}%)")
    print(f"已过 {days_passed} 天 / 共 {days_in_month} 天 / 剩余 {days_left} 天")
    print(f"日均可用: ¥{daily_avg:.0f} | 若保持节奏，本月预计: ¥{projected:.0f}")

def show_help():
    print("📊 消费预算检查工具")
    print("用法: python3 expense_budget.py <命令>")
    print()
    print("命令:")
    print("  today   - 今日预算状态")
    print("  week    - 本周预算状态")
    print("  month   - 本月预算状态")
    print("  help    - 显示此帮助")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == "today":
        check_today()
    elif command == "week":
        check_week()
    elif command == "month":
        check_month()
    elif command == "help":
        show_help()
    else:
        print(f"❌ 未知命令: {command}")
        show_help()

if __name__ == "__main__":
    main()
