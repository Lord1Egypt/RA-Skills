#!/usr/bin/env python3
"""
Token 消耗周报生成工具
生成每周 token 消耗报告，包含周对比和月度预测
"""

import json
import os
from datetime import datetime, timedelta

# 数据文件路径
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
DATA_FILE = os.path.join(DATA_DIR, 'token_log.json')


def load_data():
    """加载数据文件"""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


def format_number(num):
    """格式化数字，添加千分位"""
    return f"{num:,}"


def calculate_change(current, previous):
    """计算环比变化"""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100


def get_trend_symbol(change):
    """根据变化率获取趋势符号"""
    if change > 5:
        return "📈"
    elif change < -5:
        return "📉"
    else:
        return "📊"


def get_week_number(date):
    """获取周数"""
    return date.isocalendar()[1]


def get_week_data(data, year, week_num):
    """获取指定周的数据"""
    week_total = {"input": 0, "output": 0, "total": 0}
    
    for date_str, day_data in data.items():
        date = datetime.strptime(date_str, '%Y-%m-%d')
        if date.year == year and get_week_number(date) == week_num:
            week_total["input"] += day_data.get("input", 0)
            week_total["output"] += day_data.get("output", 0)
            week_total["total"] += day_data.get("total", 0)
    
    return week_total


def generate_weekly_report():
    """生成周报"""
    data = load_data()
    now = datetime.now()
    current_year = now.year
    current_week = get_week_number(now)
    
    # 获取最近3周的数据
    weeks_data = []
    for i in range(2, -1, -1):
        week_num = current_week - i
        year = current_year
        if week_num <= 0:
            week_num += 52
            year -= 1
        
        week_data = get_week_data(data, year, week_num)
        week_data["year"] = year
        week_data["week"] = week_num
        weeks_data.append(week_data)
    
    # 本周数据
    this_week = weeks_data[-1]
    last_week = weeks_data[-2] if len(weeks_data) > 1 else {"total": 0}
    
    # 计算环比
    change = calculate_change(this_week.get("total", 0), last_week.get("total", 0))
    trend = get_trend_symbol(change)
    
    # 计算本月累计
    month_start = now.replace(day=1)
    month_total = {"input": 0, "output": 0, "total": 0}
    for date_str, day_data in data.items():
        date = datetime.strptime(date_str, '%Y-%m-%d')
        if date.year == now.year and date.month == now.month:
            month_total["input"] += day_data.get("input", 0)
            month_total["output"] += day_data.get("output", 0)
            month_total["total"] += day_data.get("total", 0)
    
    # 预估月总
    days_passed = now.day
    days_in_month = (month_start.replace(month=now.month+1 if now.month < 12 else 1) - timedelta(days=1)).day
    if days_passed > 0:
        daily_avg = month_total["total"] / days_passed
        month_estimate = daily_avg * days_in_month
    else:
        month_estimate = 0
    
    # 生成报告
    report = []
    report.append(f"📈 Token 消耗周报 - {current_year}年第{current_week}周")
    report.append("")
    report.append("💰 本周汇总")
    report.append(f"• 输入：{format_number(this_week.get('input', 0))} tokens")
    report.append(f"• 输出：{format_number(this_week.get('output', 0))} tokens")
    report.append(f"• 总计：{format_number(this_week.get('total', 0))} tokens")
    if last_week.get("total", 0) > 0:
        report.append(f"• 较上周：{trend} {change:+.1f}%")
    report.append("")
    
    report.append("📊 周对比")
    report.append("")
    report.append("| 周次 | 输入 | 输出 | 总计 | 环比 | 趋势 |")
    report.append("|------|------|------|------|------|------|")
    
    prev_total = 0
    for i, week in enumerate(weeks_data):
        week_label = f"W{week['week']}"
        input_t = week.get("input", 0)
        output_t = week.get("output", 0)
        total = week.get("total", 0)
        
        if i == 0 or prev_total == 0:
            change_str = "-"
            trend_sym = "📊"
        else:
            change_val = calculate_change(total, prev_total)
            change_str = f"{change_val:+.1f}%"
            trend_sym = get_trend_symbol(change_val)
        
        report.append(f"| {week_label} | {format_number(input_t)} | {format_number(output_t)} | {format_number(total)} | {change_str} | {trend_sym} |")
        prev_total = total
    
    report.append("")
    report.append("📈 月度预测")
    report.append(f"• 本月累计：{format_number(month_total.get('total', 0))} tokens")
    report.append(f"• 预估月总：约 {format_number(int(month_estimate))} tokens")
    
    # 建议
    if change > 20:
        report.append("• 建议关注：⚠️ 本周消耗大幅上涨，请检查是否有异常使用")
    elif change > 10:
        report.append("• 建议关注：📈 消耗呈上升趋势，建议适当优化使用方式")
    elif change < -10:
        report.append("• 建议关注：📉 消耗下降，使用效率提升")
    else:
        report.append("• 建议关注：📊 消耗平稳，保持良好使用习惯")
    
    return "\n".join(report)


if __name__ == "__main__":
    report = generate_weekly_report()
    print(report)
