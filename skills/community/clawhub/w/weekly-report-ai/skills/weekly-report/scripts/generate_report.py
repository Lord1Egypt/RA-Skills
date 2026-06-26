#!/usr/bin/env python3
"""
周报生成器
将各数据源汇总生成Markdown格式周报
"""

import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any


def get_week_range(date_str: str = None) -> tuple:
    """获取指定日期所在周的日期范围（周一到周日）"""
    if date_str:
        target = datetime.fromisoformat(date_str)
    else:
        target = datetime.now()
    
    # 找到周一
    monday = target - timedelta(days=target.weekday())
    # 找到周日
    sunday = monday + timedelta(days=6)
    
    return monday, sunday


def format_date(d: datetime) -> str:
    return d.strftime("%Y-%m-%d")


def generate_report(
    user_name: str,
    week_start: str,
    week_end: str,
    github_data: Dict = None,
    feishu_data: Dict = None,
    calendar_data: Dict = None,
    manual_input: str = "",
    next_week_plan: str = ""
) -> str:
    """生成Markdown周报"""
    
    # 计算周数
    monday = datetime.fromisoformat(week_start)
    week_num = monday.isocalendar()[1]
    
    lines = []
    lines.append(f"# 周报 - 第{week_num}周 ({week_start} ~ {week_end})")
    lines.append("")
    lines.append(f"**汇报人**: {user_name}")
    lines.append("")
    
    # 概览统计
    lines.append("## 📊 本周概览")
    lines.append("")
    
    commit_count = len(github_data.get("commits", [])) if github_data else 0
    pr_count = len(github_data.get("prs", [])) if github_data else 0
    issue_count = len(github_data.get("issues", [])) if github_data else 0
    doc_count = len(feishu_data.get("docs", [])) + len(feishu_data.get("wiki", [])) if feishu_data else 0
    meeting_count = len(calendar_data.get("events", [])) if calendar_data else 0
    
    lines.append(f"- 代码提交: {commit_count} 次")
    lines.append(f"- 合并PR: {pr_count} 个")
    lines.append(f"- 关闭Issue: {issue_count} 个")
    lines.append(f"- 文档更新: {doc_count} 篇")
    lines.append(f"- 会议数量: {meeting_count} 场")
    lines.append("")
    
    # GitHub贡献
    if github_data and (github_data.get("commits") or github_data.get("prs")):
        lines.append("## 💻 GitHub 贡献")
        lines.append("")
        
        if github_data.get("prs"):
            lines.append("### 合并的PR")
            lines.append("")
            for pr in github_data["prs"]:
                lines.append(f"- [#{pr['number']}] {pr['title']} - {pr['repo']} ({pr.get('merged_at', '')[:10]})")
            lines.append("")
        
        if github_data.get("commits"):
            lines.append("### 提交记录")
            lines.append("")
            for commit in github_data["commits"][:10]:  # 限制显示10条
                lines.append(f"- `{commit['sha']}` {commit['message'][:50]}...")
            lines.append("")
    
    # 飞书文档
    if feishu_data and (feishu_data.get("docs") or feishu_data.get("wiki")):
        lines.append("## 📄 文档更新")
        lines.append("")
        
        for doc in feishu_data.get("docs", []):
            lines.append(f"- [{doc['title']}]({doc['url']})")
        
        for wiki in feishu_data.get("wiki", []):
            lines.append(f"- {wiki['name']}")
        
        lines.append("")
    
    # 日历会议
    if calendar_data and calendar_data.get("events"):
        lines.append("## 📅 会议记录")
        lines.append("")
        
        for event in calendar_data["events"]:
            lines.append(f"- **{event['title']}** - {event.get('start', '')}")
            if event.get("description"):
                lines.append(f"  - {event['description']}")
        
        lines.append("")
    
    # 手动输入
    if manual_input:
        lines.append("## 📝 补充说明")
        lines.append("")
        lines.append(manual_input)
        lines.append("")
    
    # 下周计划
    if next_week_plan:
        lines.append("## 🎯 下周计划")
        lines.append("")
        lines.append(next_week_plan)
        lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="生成周报")
    parser.add_argument("--user", default="User", help="用户名")
    parser.add_argument("--week-start", help="周开始日期 (YYYY-MM-DD)")
    parser.add_argument("--week-end", help="周结束日期 (YYYY-MM-DD)")
    parser.add_argument("--github", help="GitHub数据 (JSON文件)")
    parser.add_argument("--feishu", help="飞书数据 (JSON文件)")
    parser.add_argument("--calendar", help="日历数据 (JSON文件)")
    parser.add_argument("--manual", default="", help="手动输入内容")
    parser.add_argument("--plan", default="", help="下周计划")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 获取本周日期范围
    if args.week_start and args.week_end:
        week_start = args.week_start
        week_end = args.week_end
    else:
        monday, sunday = get_week_range()
        week_start = format_date(monday)
        week_end = format_date(sunday)
    
    # 加载数据
    github_data = {}
    feishu_data = {}
    calendar_data = {}
    
    if args.github:
        with open(args.github) as f:
            github_data = json.load(f)
    
    if args.feishu:
        with open(args.feishu) as f:
            feishu_data = json.load(f)
    
    if args.calendar:
        with open(args.calendar) as f:
            calendar_data = json.load(f)
    
    # 生成周报
    report = generate_report(
        user_name=args.user,
        week_start=week_start,
        week_end=week_end,
        github_data=github_data,
        feishu_data=feishu_data,
        calendar_data=calendar_data,
        manual_input=args.manual,
        next_week_plan=args.plan
    )
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"周报已保存到: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
