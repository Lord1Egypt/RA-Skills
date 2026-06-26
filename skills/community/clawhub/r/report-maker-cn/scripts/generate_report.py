#!/usr/bin/env python3
"""
飞书日报生成器 - 从多个数据源汇总生成结构化日报
用法: python3 generate_report.py --type daily --date 2026-04-10 --output doc
"""

import argparse
import json
import os
from datetime import datetime, timedelta

def get_date_range(report_type, date_str=None):
    """根据报告类型计算日期范围"""
    if date_str:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        target_date = datetime.now()
    
    if report_type == "daily":
        return {
            "start": target_date.strftime("%Y-%m-%d"),
            "end": target_date.strftime("%Y-%m-%d"),
            "display": target_date.strftime("%Y年%m月%d日")
        }
    elif report_type == "weekly":
        # 本周一到今天
        monday = target_date - timedelta(days=target_date.weekday())
        return {
            "start": monday.strftime("%Y-%m-%d"),
            "end": target_date.strftime("%Y-%m-%d"),
            "display": f"{monday.strftime('%m月%d日')} - {target_date.strftime('%m月%d日')}"
        }
    else:
        return {
            "start": target_date.strftime("%Y-%m-%d"),
            "end": target_date.strftime("%Y-%m-%d"),
            "display": target_date.strftime("%Y年%m月%d日")
        }

def generate_daily_report(data, date_info):
    """生成日报内容"""
    completed = data.get("completed", [])
    in_progress = data.get("in_progress", [])
    planned = data.get("planned", [])
    risks = data.get("risks", [])
    
    lines = [
        f"# 📋 日报 | {date_info['display']}",
        "",
        "## ✅ 今日完成",
    ]
    for item in completed:
        lines.append(f"- {item}")
    if not completed:
        lines.append("- （暂无记录）")
    
    lines.extend([
        "",
        "## 🔄 进行中",
    ])
    for item in in_progress:
        lines.append(f"- {item}")
    if not in_progress:
        lines.append("- （暂无）")
    
    lines.extend([
        "",
        "## 📅 明日计划",
    ])
    for item in planned:
        lines.append(f"- {item}")
    if not planned:
        lines.append("- （待规划）")
    
    if risks:
        lines.extend([
            "",
            "## ⚠️ 风险/阻塞",
        ])
        for item in risks:
            lines.append(f"- {item}")
    
    return "\n".join(lines)

def generate_weekly_report(data, date_info):
    """生成周报内容"""
    completed = data.get("completed", [])
    metrics = data.get("metrics", [])
    planned = data.get("planned", [])
    risks = data.get("risks", [])
    
    lines = [
        f"# 📊 周报 | {date_info['display']}",
        "",
        "## 本周完成",
    ]
    for item in completed:
        lines.append(f"- {item}")
    if not completed:
        lines.append("- （暂无记录）")
    
    if metrics:
        lines.extend([
            "",
            "## 数据指标",
            "",
            "| 指标 | 数值 | 环比 |",
            "|------|------|------|",
        ])
        for m in metrics:
            lines.append(f"| {m.get('name', '')} | {m.get('value', '')} | {m.get('change', '')} |")
    
    lines.extend([
        "",
        "## 下周计划",
    ])
    for item in planned:
        lines.append(f"- {item}")
    if not planned:
        lines.append("- （待规划）")
    
    if risks:
        lines.extend([
            "",
            "## 风险与建议",
        ])
        for item in risks:
            lines.append(f"- {item}")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="飞书日报生成器")
    parser.add_argument("--type", choices=["daily", "weekly", "custom"], default="daily", help="报告类型")
    parser.add_argument("--date", help="目标日期 YYYY-MM-DD")
    parser.add_argument("--data", help="数据JSON文件路径")
    parser.add_argument("--output", choices=["doc", "chat", "both"], default="doc", help="输出方式")
    args = parser.parse_args()
    
    # 日期范围
    date_info = get_date_range(args.type, args.date)
    
    # 加载数据
    if args.data and os.path.exists(args.data):
        with open(args.data, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        # 空模板数据
        data = {
            "completed": [],
            "in_progress": [],
            "planned": [],
            "risks": [],
            "metrics": []
        }
    
    # 生成报告
    if args.type == "daily":
        report = generate_daily_report(data, date_info)
    elif args.type == "weekly":
        report = generate_weekly_report(data, date_info)
    else:
        report = generate_daily_report(data, date_info)
    
    # 输出
    print(report)
    print(f"\n---\n报告类型: {args.type} | 日期: {date_info['display']} | 输出: {args.output}")

if __name__ == "__main__":
    main()
