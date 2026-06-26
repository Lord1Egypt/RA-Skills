#!/usr/bin/env python3
"""
使用统计模块
- 每日统计记录
- 7天趋势分析
- 稳定性评估
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# 导入配置
try:
    from config_manager import STATS_DIR
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config_manager import STATS_DIR


def get_day_stats(date_str):
    """获取指定日期的统计"""
    stats_file = STATS_DIR / f"{date_str}.json"

    if stats_file.exists():
        with open(stats_file, 'r') as f:
            return json.load(f)
    return None


def get_recent_stats(days=7):
    """获取最近N天的统计"""
    stats = {}
    today = datetime.now()

    for i in range(days):
        date = today - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')

        day_stats = get_day_stats(date_str)
        if day_stats:
            stats[date_str] = day_stats

    # 添加今日统计
    today_str = today.strftime('%Y-%m-%d')
    stats["today"] = get_day_stats(today_str)

    return stats


def calculate_success_rate(stats):
    """计算成功率"""
    if not stats:
        return 0

    total = stats.get("total_requests", 0)
    success = stats.get("success_count", 0)

    if total == 0:
        return 0

    return round((success / total) * 100, 2)


def calculate_avg_latency(stats):
    """计算平均延迟"""
    latencies = stats.get("latencies", [])

    if not latencies:
        return 0

    return round(sum(latencies) / len(latencies), 2)


def analyze_trend(stats_dict):
    """分析成功率趋势"""
    rates = []

    for date_str, day_stats in stats_dict.items():
        if date_str == "today" or not day_stats:
            continue
        rates.append(calculate_success_rate(day_stats))

    if len(rates) < 2:
        return "insufficient_data", "数据不足"

    # 计算波动
    avg_rate = sum(rates) / len(rates)
    variance = sum((r - avg_rate) ** 2 for r in rates) / len(rates)
    std_dev = variance ** 0.5

    # 评估稳定性
    if avg_rate >= 90 and std_dev < 5:
        return "stable", "稳定"
    elif std_dev <= 10:
        return "fluctuating", "波动"
    else:
        return "risk", "风险"


def generate_report():
    """生成统计报告"""
    stats = get_recent_stats(days=7)

    if not stats or all(v is None for v in stats.values()):
        return {
            "success": False,
            "error": "无统计数据，请先使用代理服务"
        }

    # 今日统计
    today_str = datetime.now().strftime('%Y-%m-%d')
    today_stats = stats.get("today")
    today_report = None

    if today_stats:
        today_report = {
            "date": today_str,
            "total_requests": today_stats.get("total_requests", 0),
            "success_count": today_stats.get("success_count", 0),
            "fail_count": today_stats.get("fail_count", 0),
            "success_rate": calculate_success_rate(today_stats),
            "avg_latency_ms": calculate_avg_latency(today_stats)
        }

    # 7天汇总
    total_requests = 0
    total_success = 0
    total_fail = 0
    all_latencies = []

    for date_str, day_stats in stats.items():
        if date_str == "today" or not day_stats:
            continue
        total_requests += day_stats.get("total_requests", 0)
        total_success += day_stats.get("success_count", 0)
        total_fail += day_stats.get("fail_count", 0)
        all_latencies.extend(day_stats.get("latencies", []))

    weekly_report = {
        "period": "最近7天",
        "total_requests": total_requests,
        "success_count": total_success,
        "fail_count": total_fail,
        "success_rate": round((total_success / total_requests * 100) if total_requests else 0, 2),
        "avg_latency_ms": round(sum(all_latencies) / len(all_latencies), 2) if all_latencies else 0,
        "days_with_data": len([v for v in stats.values() if v and v != stats.get("today")])
    }

    # 趋势分析
    trend_status, trend_text = analyze_trend(stats)

    return {
        "success": True,
        "today": today_report,
        "weekly": weekly_report,
        "trend": {
            "status": trend_status,
            "text": trend_text
        },
        "generated_at": datetime.now().isoformat()
    }


def show_stats():
    """显示统计"""
    report = generate_report()

    if not report["success"]:
        return report

    # 格式化输出
    lines = ["\n[使用统计报告]"]

    if report["today"]:
        t = report["today"]
        lines.append(f"\n今日统计 ({t['date']})")
        lines.append(f"  请求数: {t['total_requests']}")
        lines.append(f"  成功: {t['success_count']} | 失败: {t['fail_count']}")
        lines.append(f"  成功率: {t['success_rate']}%")
        lines.append(f"  平均延迟: {t['avg_latency_ms']}ms")

    w = report["weekly"]
    lines.append(f"\n7天汇总")
    lines.append(f"  总请求: {w['total_requests']}")
    lines.append(f"  成功: {w['success_count']} | 失败: {w['fail_count']}")
    lines.append(f"  成功率: {w['success_rate']}%")
    lines.append(f"  平均延迟: {w['avg_latency_ms']}ms")
    lines.append(f"  有效天数: {w['days_with_data']}")

    lines.append(f"\n稳定性: {report['trend']['text']}")

    return {
        "success": True,
        "report": report,
        "output": "\n".join(lines)
    }


# 命令行入口
if __name__ == '__main__':
    result = show_stats()

    if result["success"]:
        print(result["output"])
    else:
        print(f"[提示] {result['error']}")