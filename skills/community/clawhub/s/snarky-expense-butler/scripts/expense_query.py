#!/usr/bin/env python3
# 消费记录查询工具

import json
import sys
import os
import datetime
from datetime import timedelta

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.environ.get('EXPENSE_DATA_FILE', os.path.join(_SCRIPT_DIR, 'expense_records.json'))

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

def show_today():
    """显示今日消费"""
    data = load_data()
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    for record in data['records']:
        if record['date'] == today:
            total = round(sum(-item['amount'] for item in record['items']), 2)
            print(f"📅 今日消费 ({today}):")
            print(f"   总计: ¥{total}")
            print("   明细:")
            for item in record['items']:
                note = f" ({item['note']})" if item['note'] else ""
                if item['amount'] > 0:
                    print(f"     • ✅ {item['category']}: +¥{round(item['amount'], 2)} (退款){note}")
                else:
                    print(f"     • 💸 {item['category']}: ¥{round(abs(item['amount']), 2)}{note}")
            return

    print(f"📅 今日 ({today}) 暂无消费记录")

def show_week():
    """显示本周汇总"""
    data = load_data()
    today = datetime.datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    week_dates = [(start_of_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    week_records = [r for r in data['records'] if r['date'] in week_dates]
    total = round(sum(sum(-item['amount'] for item in r['items']) for r in week_records), 2)

    print(f"📅 本周汇总 ({week_dates[0]} 至 {week_dates[-1]}):")
    print(f"   总计: ¥{total}")
    print(f"   日均: ¥{round(total/7, 1)}")
    print("   每日明细:")
    for date in week_dates:
        record = next((r for r in week_records if r['date'] == date), None)
        amount = round(sum(-item['amount'] for item in record['items']), 2) if record else 0
        print(f"     • {date}: ¥{amount}")

    # 预算状态
    budget = data['settings'].get('budget', {})
    weekly_budget = budget.get('weekly')
    if weekly_budget:
        remaining = weekly_budget - total
        percentage = (total / weekly_budget * 100) if weekly_budget > 0 else 0
        if percentage > 100:
            status = "🚨 超支"
        elif percentage > 80:
            status = "⚠️ 接近预算"
        else:
            status = "✅ 正常"
        print(f"\n💰 本周预算: ¥{round(weekly_budget, 2)} | 已用: ¥{round(total, 2)} | 剩余: ¥{round(remaining, 2)}")
        print(f"   状态: {status} ({round(percentage, 1)}%)")

def show_month():
    """显示本月汇总"""
    data = load_data()
    today = datetime.datetime.now()
    month_str = today.strftime('%Y-%m')

    month_records = [r for r in data['records'] if r['date'].startswith(month_str)]
    total = round(sum(sum(-item['amount'] for item in r['items']) for r in month_records), 2)

    print(f"📅 本月汇总 ({month_str}):")
    print(f"   总计: ¥{total}")
    print(f"   记录天数: {len(month_records)}天")

    # 预算状态
    budget = data['settings'].get('budget', {})
    monthly_budget = budget.get('monthly')
    if monthly_budget:
        remaining = monthly_budget - total
        percentage = (total / monthly_budget * 100) if monthly_budget > 0 else 0
        if percentage > 100:
            status = "🚨 超支"
        elif percentage > 80:
            status = "⚠️ 接近预算"
        else:
            status = "✅ 正常"
        print(f"\n💰 本月预算: ¥{round(monthly_budget, 2)} | 已用: ¥{round(total, 2)} | 剩余: ¥{round(remaining, 2)}")
        print(f"   状态: {status} ({round(percentage, 1)}%)")

def show_stats():
    """显示统计信息"""
    data = load_data()

    print("📊 消费统计:")
    print(f"   总记录天数: {data['metadata'].get('total_days', 0)}天")
    print(f"   总消费金额: ¥{round(data['metadata'].get('total_amount', 0), 2)}")
    print(f"   最后更新: {data['metadata'].get('last_updated', '从未')}")

def show_help():
    """显示帮助"""
    print("📋 消费记录查询工具")
    print("用法: python3 expense_query.py <命令>")
    print()
    print("命令:")
    print("  today     - 今日消费")
    print("  week      - 本周汇总")
    print("  month     - 本月汇总")
    print("  stats     - 统计信息")
    print("  help      - 显示此帮助")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == "today":
        show_today()
    elif command == "week":
        show_week()
    elif command == "month":
        show_month()
    elif command == "stats":
        show_stats()
    elif command == "help":
        show_help()
    else:
        print(f"❌ 未知命令: {command}")
        show_help()

if __name__ == "__main__":
    main()
