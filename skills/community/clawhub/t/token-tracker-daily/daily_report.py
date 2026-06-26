#!/usr/bin/env python3
"""
Token 消耗日报生成工具
生成每日 token 消耗报告，包含近7天趋势分析
"""

import json
import os
import sys
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


def get_last_n_days(data, n=7, end_date=None):
    """获取最近 n 天的数据"""
    if end_date is None:
        end_date = datetime.now()
    
    result = []
    for i in range(n-1, -1, -1):
        date = end_date - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        if date_str in data:
            result.append(data[date_str])
        else:
            result.append({
                "date": date_str,
                "input": 0,
                "output": 0,
                "total": 0
            })
    return result


def generate_daily_report():
    """生成日报"""
    data = load_data()
    today = datetime.now().strftime('%Y-%m-%d')
    today_data = data.get(today, {"input": 0, "output": 0, "total": 0})
    
    # 获取昨天数据计算环比
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_data = data.get(yesterday, {"input": 0, "output": 0, "total": 0})
    
    change = calculate_change(today_data.get("total", 0), yesterday_data.get("total", 0))
    trend = get_trend_symbol(change)
    
    # 获取近7天数据
    week_data = get_last_n_days(data, 7)
    
    # 计算本周总计
    week_total = sum(d.get("total", 0) for d in week_data)
    week_avg = week_total / 7 if week_data else 0
    
    # 预估月耗
    month_estimate = week_avg * 30
    
    # 生成报告
    report = []
    report.append("📊 Token 消耗日报")
    report.append(f"📅 {datetime.now().strftime('%Y年%m月%d日')}")
    report.append("")
    report.append("💰 今日汇总")
    report.append(f"• 输入：{format_number(today_data.get('input', 0))} tokens")
    report.append(f"• 输出：{format_number(today_data.get('output', 0))} tokens")
    report.append(f"• 总计：{format_number(today_data.get('total', 0))} tokens")
    if yesterday_data.get("total", 0) > 0:
        report.append(f"• 较昨日：{trend} {change:+.1f}%")
    report.append("")
    
    report.append("📅 近7天消耗明细")
    report.append("")
    report.append("| 日期 | 输入 | 输出 | 总计 | 环比 | 趋势 |")
    report.append("|------|------|------|------|------|------|")
    
    prev_total = 0
    for i, day in enumerate(week_data):
        date_str = day.get("date", "")
        display_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%m/%d')
        input_t = day.get("input", 0)
        output_t = day.get("output", 0)
        total = day.get("total", 0)
        
        if i == 0 or prev_total == 0:
            change_str = "-"
            trend_sym = "📊"
        else:
            change_val = calculate_change(total, prev_total)
            change_str = f"{change_val:+.1f}%"
            trend_sym = get_trend_symbol(change_val)
        
        report.append(f"| {display_date} | {format_number(input_t)} | {format_number(output_t)} | {format_number(total)} | {change_str} | {trend_sym} |")
        prev_total = total
    
    report.append("")
    report.append("📈 趋势分析")
    report.append(f"• 本周总计：{format_number(week_total)} tokens")
    report.append(f"• 日均消耗：{format_number(int(week_avg))} tokens")
    
    # 趋势方向
    if len(week_data) >= 2:
        first_half = sum(d.get("total", 0) for d in week_data[:3])
        second_half = sum(d.get("total", 0) for d in week_data[3:])
        if second_half > first_half * 1.1:
            trend_dir = "📈 上升"
        elif second_half < first_half * 0.9:
            trend_dir = "📉 下降"
        else:
            trend_dir = "📊 平稳"
        report.append(f"• 趋势方向：{trend_dir}")
    
    report.append(f"• 预估月耗：约 {format_number(int(month_estimate))} tokens")
    
    return "\n".join(report)


if __name__ == "__main__":
    report = generate_daily_report()
    print(report)
