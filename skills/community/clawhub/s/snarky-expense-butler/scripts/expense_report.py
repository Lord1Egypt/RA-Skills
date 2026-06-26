#!/usr/bin/env python3
# 消费记录自动汇报脚本

import json
import os
import datetime
from datetime import timedelta
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.environ.get('EXPENSE_DATA_FILE', os.path.join(_SCRIPT_DIR, 'expense_records.json'))

def load_data():
    """加载消费记录数据"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"records": [], "categories": [], "settings": {}, "metadata": {}}
    except json.JSONDecodeError:
        return {"records": [], "categories": [], "settings": {}, "metadata": {}}

def calc_total(record):
    """计算实际消费总额（正数退款减少，负数消费增加）"""
    return round(sum(-item['amount'] for item in record['items']), 2)

def fmt_item(item):
    """格式化单条消费明细"""
    note = f" ({item['note']})" if item.get('note') else ""
    if item['amount'] > 0:
        return f"  • ✅ {item['category']}: +¥{round(item['amount'], 2)} (退款){note}"
    else:
        return f"  • 💸 {item['category']}: ¥{round(abs(item['amount']), 2)}{note}"

def generate_daily_report(data):
    """生成每日报告"""
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # 查找今日记录
    today_record = next((r for r in data['records'] if r['date'] == today), None)
    yesterday_record = next((r for r in data['records'] if r['date'] == yesterday), None)

    report = f"📊 每日消费报告 ({today})\n"
    report += "─" * 30 + "\n"

    if today_record:
        today_total = calc_total(today_record)
        report += f"💰 今日总计: ¥{today_total}\n"
        report += "📝 明细:\n"
        for item in today_record['items']:
            report += fmt_item(item) + "\n"

        # 与昨日对比
        if yesterday_record:
            yesterday_total = calc_total(yesterday_record)
            diff = round(today_total - yesterday_total, 2)
            if diff > 0:
                report += f"📈 比昨日增加: +¥{diff}\n"
            elif diff < 0:
                report += f"📉 比昨日减少: ¥{diff}\n"
            else:
                report += f"📊 与昨日持平\n"
        else:
            report += "📊 昨日无记录，无法对比\n"
    else:
        report += "📭 今日暂无消费记录\n"

    return report

def generate_weekly_report(data):
    """生成每周报告"""
    today = datetime.datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    week_dates = [(start_of_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    week_records = [r for r in data['records'] if r['date'] in week_dates]

    # 上周数据
    start_of_last_week = start_of_week - timedelta(days=7)
    last_week_dates = [(start_of_last_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    last_week_records = [r for r in data['records'] if r['date'] in last_week_dates]

    report = f"📅 每周消费报告 ({week_dates[0]} 至 {week_dates[-1]})\n"
    report += "─" * 40 + "\n"

    if week_records:
        week_total = round(sum(calc_total(r) for r in week_records), 2)
        report += f"💰 本周总计: ¥{week_total}\n"
        report += f"📅 日均消费: ¥{round(week_total/7, 1)}\n"

        # 分类统计
        categories = {}
        for record in week_records:
            for item in record['items']:
                cat = item['category']
                categories[cat] = round(categories.get(cat, 0) + (-item['amount']), 2)

        if categories:
            report += "📋 分类统计:\n"
            for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percentage = round((amount / week_total * 100), 1) if week_total > 0 else 0
                report += f"  • {cat}: ¥{abs(amount)} ({percentage}%)\n"

        # 与上周对比
        if last_week_records:
            last_week_total = round(sum(calc_total(r) for r in last_week_records), 2)
            diff = round(week_total - last_week_total, 2)
            if last_week_total > 0:
                percentage = round((diff / last_week_total * 100), 1)
                if diff > 0:
                    report += f"📈 比上周增加: +¥{diff} (+{percentage}%)\n"
                elif diff < 0:
                    report += f"📉 比上周减少: ¥{diff} ({percentage}%)\n"
                else:
                    report += f"📊 与上周持平\n"
            else:
                report += f"📊 上周无记录，无法对比\n"
        else:
            report += "📊 上周无记录，无法对比\n"
    else:
        report += "📭 本周暂无消费记录\n"

    return report

def generate_monthly_report(data):
    """生成每月报告"""
    today = datetime.datetime.now()
    month_str = today.strftime('%Y-%m')

    # 本月记录
    month_records = [r for r in data['records'] if r['date'].startswith(month_str)]

    # 上月数据
    last_month = today.replace(day=1) - timedelta(days=1)
    last_month_str = last_month.strftime('%Y-%m')
    last_month_records = [r for r in data['records'] if r['date'].startswith(last_month_str)]

    report = f"📅 每月消费报告 ({month_str})\n"
    report += "─" * 40 + "\n"

    if month_records:
        month_total = round(sum(calc_total(r) for r in month_records), 2)
        days_in_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        days_count = days_in_month.day
        record_days = len(month_records)

        report += f"💰 本月总计: ¥{month_total}\n"
        report += f"📅 日均消费: ¥{round(month_total/days_count, 1)}\n"
        report += f"📝 记录天数: {record_days}/{days_count}天\n"

        # 分类统计
        categories = {}
        for record in month_records:
            for item in record['items']:
                cat = item['category']
                categories[cat] = round(categories.get(cat, 0) + (-item['amount']), 2)

        if categories:
            report += "📋 分类统计:\n"
            for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percentage = round((amount / month_total * 100), 1) if month_total > 0 else 0
                report += f"  • {cat}: ¥{abs(amount)} ({percentage}%)\n"

        # 与上月对比
        if last_month_records:
            last_month_total = round(sum(calc_total(r) for r in last_month_records), 2)
            diff = round(month_total - last_month_total, 2)
            if last_month_total > 0:
                percentage = round((diff / last_month_total * 100), 1)
                if diff > 0:
                    report += f"📈 比上月增加: +¥{diff} (+{percentage}%)\n"
                elif diff < 0:
                    report += f"📉 比上月减少: ¥{diff} ({percentage}%)\n"
                else:
                    report += f"📊 与上月持平\n"
            else:
                report += f"📊 上月无记录，无法对比\n"
        else:
            report += "📊 上月无记录，无法对比\n"
    else:
        report += "📭 本月暂无消费记录\n"

    return report

def generate_yearly_report(data):
    """生成年度报告"""
    today = datetime.datetime.now()
    year_str = today.strftime('%Y')

    # 本年记录
    year_records = [r for r in data['records'] if r['date'].startswith(year_str)]

    # 去年数据
    last_year = today.replace(year=today.year - 1)
    last_year_str = last_year.strftime('%Y')
    last_year_records = [r for r in data['records'] if r['date'].startswith(last_year_str)]

    report = f"🎉 年度消费报告 ({year_str})\n"
    report += "─" * 40 + "\n"

    if year_records:
        year_total = round(sum(calc_total(r) for r in year_records), 2)
        record_days = len(year_records)

        report += f"💰 本年总计: ¥{year_total}\n"
        report += f"📅 月均消费: ¥{round(year_total/12, 1)}\n"
        report += f"📝 记录天数: {record_days}天\n"

        # 月度趋势
        monthly_totals = {}
        for record in year_records:
            month = record['date'][:7]  # YYYY-MM
            monthly_totals[month] = round(monthly_totals.get(month, 0) + calc_total(record), 2)

        if monthly_totals:
            report += "📈 月度趋势:\n"
            for month in sorted(monthly_totals.keys()):
                report += f"  • {month}: ¥{monthly_totals[month]}\n"

        # 分类统计
        categories = {}
        for record in year_records:
            for item in record['items']:
                cat = item['category']
                categories[cat] = round(categories.get(cat, 0) + (-item['amount']), 2)

        if categories:
            report += "📋 年度分类统计:\n"
            for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percentage = round((amount / year_total * 100), 1) if year_total > 0 else 0
                report += f"  • {cat}: ¥{abs(amount)} ({percentage}%)\n"

        # 与去年对比
        if last_year_records:
            last_year_total = round(sum(calc_total(r) for r in last_year_records), 2)
            diff = round(year_total - last_year_total, 2)
            if last_year_total > 0:
                percentage = round((diff / last_year_total * 100), 1)
                if diff > 0:
                    report += f"📈 比去年增加: +¥{diff} (+{percentage}%)\n"
                elif diff < 0:
                    report += f"📉 比去年减少: ¥{diff} ({percentage}%)\n"
                else:
                    report += f"📊 与去年持平\n"
            else:
                report += f"📊 去年无记录，无法对比\n"
        else:
            report += "📊 去年无记录，无法对比\n"
    else:
        report += "📭 本年暂无消费记录\n"

    return report

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("用法: python3 expense_report.py <daily|weekly|monthly|yearly>")
        sys.exit(1)

    report_type = sys.argv[1]
    data = load_data()

    if report_type == "daily":
        report = generate_daily_report(data)
    elif report_type == "weekly":
        report = generate_weekly_report(data)
    elif report_type == "monthly":
        report = generate_monthly_report(data)
    elif report_type == "yearly":
        report = generate_yearly_report(data)
    else:
        print(f"错误: 未知报告类型 '{report_type}'")
        sys.exit(1)

    print(report)

if __name__ == "__main__":
    main()
