#!/usr/bin/env python3
"""
CLI 纯文本可视化模块 - 不引入外部依赖
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict


def generate_weekly_chart(log_files: List[Path], weeks: int = 4) -> str:
    """生成周学习趋势 ASCII 柱状图"""
    if not log_files:
        return "暂无学习数据"
    
    # 统计每周学习天数
    now = datetime.now()
    weekly_data = []
    
    for i in range(weeks - 1, -1, -1):
        week_end = now - timedelta(days=now.weekday() + 7 * i)
        week_start = week_end - timedelta(days=6)
        
        week_count = 0
        for log_file in log_files:
            try:
                log_date = datetime.strptime(log_file.stem, '%Y-%m-%d')
                if week_start <= log_date <= week_end:
                    week_count += 1
            except:
                continue
        
        weekly_data.append({
            'label': f"{week_start.month}/{week_start.day}-{week_end.month}/{week_end.day}",
            'count': week_count
        })
    
    # 生成 ASCII 柱状图
    max_count = max(d['count'] for d in weekly_data) if weekly_data else 0
    max_count = max(max_count, 1)  # 避免除以0
    
    lines = ["📊 近4周学习趋势", "-" * 30]
    
    for data in weekly_data:
        bar_len = int((data['count'] / max_count) * 15)
        bar = "█" * bar_len + "░" * (15 - bar_len)
        lines.append(f"{data['label']:12} {bar} {data['count']}天")
    
    return "\n".join(lines)


def generate_monthly_calendar(log_files: List[Path]) -> str:
    """生成月度学习日历（ASCII）"""
    if not log_files:
        return "暂无学习数据"
    
    # 获取本月学习日期
    now = datetime.now()
    month_start = now.replace(day=1)
    
    study_dates = set()
    for log_file in log_files:
        try:
            log_date = datetime.strptime(log_file.stem, '%Y-%m-%d')
            if log_date.year == now.year and log_date.month == now.month:
                study_dates.add(log_date.day)
        except:
            continue
    
    # 生成日历
    lines = [f"📅 {now.year}年{now.month}月学习日历", "-" * 30]
    lines.append("日 一 二 三 四 五 六")
    
    # 计算月初是周几
    first_day = month_start.weekday()
    if first_day == 6:
        first_day = 0
    else:
        first_day = first_day + 1
    
    # 计算本月天数
    if now.month == 12:
        next_month = now.replace(year=now.year + 1, month=1, day=1)
    else:
        next_month = now.replace(month=now.month + 1, day=1)
    days_in_month = (next_month - month_start).days
    
    # 生成日历行
    current_line = ["  "] * first_day
    for day in range(1, days_in_month + 1):
        if day in study_dates:
            current_line.append(f"✓ ")
        else:
            current_line.append(f"{day:2}")
        
        if len(current_line) == 7:
            lines.append(" ".join(current_line))
            current_line = []
    
    if current_line:
        lines.append(" ".join(current_line))
    
    lines.append("-" * 30)
    lines.append("✓ = 已学习")
    
    return "\n".join(lines)


def generate_streak_visual(streak: int) -> str:
    """生成连续打卡可视化"""
    if streak == 0:
        return "🔥 连续打卡: 0天 (从今天开始！)"
    
    fire_emoji = "🔥"
    streak_bar = "█" * min(streak, 10) + "░" * (10 - min(streak, 10))
    
    if streak >= 30:
        level = "卓越"
    elif streak >= 14:
        level = "优秀"
    elif streak >= 7:
        level = "良好"
    else:
        level = "起步"
    
    return f"{fire_emoji} 连续打卡: {streak}天 [{streak_bar}] {level}"


def generate_week_summary(log_files: List[Path]) -> str:
    """生成本周学习小结"""
    if not log_files:
        return "本周暂无学习记录"
    
    # 本周数据
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    
    week_logs = []
    total_duration = 0
    
    for log_file in log_files:
        try:
            log_date = datetime.strptime(log_file.stem, '%Y-%m-%d')
            if log_date >= week_start:
                with open(log_file, 'r', encoding='utf-8') as f:
                    import json
                    log = json.load(f)
                    if isinstance(log, list):
                        log = log[-1]
                    week_logs.append(log)
                    
                    # 解析时长
                    duration = log.get('duration', '')
                    if '分钟' in duration:
                        try:
                            total_duration += int(duration.replace('分钟', '').strip())
                        except:
                            pass
                    elif '小时' in duration:
                        try:
                            total_duration += int(duration.replace('小时', '').strip()) * 60
                        except:
                            pass
        except:
            continue
    
    if not week_logs:
        return "本周暂无学习记录"
    
    lines = ["📈 本周学习小结", "-" * 30]
    lines.append(f"学习天数: {len(week_logs)} 天")
    lines.append(f"总时长: {total_duration} 分钟 ({total_duration // 60}小时{total_duration % 60}分钟)")
    lines.append(f"日均时长: {total_duration // len(week_logs)} 分钟")
    
    # 学习分布
    days_left = 7 - len(week_logs)
    if days_left > 0:
        lines.append(f"剩余目标: 再学 {days_left} 天完成本周目标")
    else:
        lines.append("🎉 本周目标已完成！")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 测试
    print("CLI 可视化模块测试")
    print("=" * 50)
    
    # 模拟测试数据
    test_files = []
    print("\n周学习趋势示例：")
    print(generate_weekly_chart(test_files))
    
    print("\n连续打卡可视化示例：")
    print(generate_streak_visual(5))
    print(generate_streak_visual(12))
    print(generate_streak_visual(25))
