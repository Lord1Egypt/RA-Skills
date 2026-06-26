#!/usr/bin/env python3
"""
龙虾记忆系统 - 记忆摘要脚本
生成每日/每周记忆摘要
"""

import argparse
import os
import re
from datetime import datetime, timedelta
from pathlib import Path


def find_memory_files(memory_dir: str, start_date: str = None, end_date: str = None) -> list:
    """查找指定日期范围的记忆文件"""
    memory_path = Path(memory_dir)
    if not memory_path.exists():
        return []
    
    files = []
    for f in memory_path.glob("*.md"):
        match = re.match(r"(\d{4}-\d{2}-\d{2})\.md", f.name)
        if match:
            file_date = match.group(1)
            if start_date and file_date < start_date:
                continue
            if end_date and file_date > end_date:
                continue
            files.append((f, file_date))
    
    return sorted(files, key=lambda x: x[1])


def extract_content_summary(file_path: Path) -> dict:
    """提取文件内容摘要"""
    content = file_path.read_text(encoding="utf-8")
    
    summary = {
        "date": file_path.stem,
        "topics": [],
        "decisions": [],
        "tasks": [],
        "errors": [],
        "important": [],
        "line_count": len(content.split("\n")),
    }
    
    lines = content.split("\n")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        # 提取各类内容
        if "#决策" in line:
            summary["decisions"].append(line.replace("#决策", "").strip())
        elif "#待处理" in line:
            summary["tasks"].append(line.replace("#待处理", "").strip())
        elif "#错误" in line:
            summary["errors"].append(line.replace("#错误", "").strip())
        elif "#重要" in line:
            summary["important"].append(line.replace("#重要", "").strip())
        elif line.startswith("- ") or line.startswith("* "):
            summary["topics"].append(line[2:].strip())
    
    return summary


def generate_daily_summary(summaries: list) -> str:
    """生成每日摘要"""
    if not summaries:
        return "无记忆内容"
    
    lines = []
    for s in summaries:
        lines.append(f"## 📅 {s['date']}")
        lines.append(f"记录行数: {s['line_count']}")
        
        if s["decisions"]:
            lines.append(f"\n### 决策 ({len(s['decisions'])})")
            for d in s["decisions"][:5]:
                lines.append(f"- {d}")
        
        if s["tasks"]:
            lines.append(f"\n### 待处理 ({len(s['tasks'])})")
            for t in s["tasks"][:5]:
                lines.append(f"- {t}")
        
        if s["important"]:
            lines.append(f"\n### 重要 ({len(s['important'])})")
            for i in s["important"][:5]:
                lines.append(f"- {i}")
        
        if s["errors"]:
            lines.append(f"\n### 错误教训 ({len(s['errors'])})")
            for e in s["errors"][:3]:
                lines.append(f"- {e}")
        
        lines.append("")
    
    return "\n".join(lines)


def generate_weekly_summary(summaries: list) -> str:
    """生成每周摘要"""
    if not summaries:
        return "无记忆内容"
    
    # 汇总统计
    total_lines = sum(s["line_count"] for s in summaries)
    all_decisions = []
    all_tasks = []
    all_errors = []
    all_important = []
    
    for s in summaries:
        all_decisions.extend(s["decisions"])
        all_tasks.extend(s["tasks"])
        all_errors.extend(s["errors"])
        all_important.extend(s["important"])
    
    # 去重
    all_decisions = list(dict.fromkeys(all_decisions))
    all_tasks = list(dict.fromkeys(all_tasks))
    all_errors = list(dict.fromkeys(all_errors))
    all_important = list(dict.fromkeys(all_important))
    
    lines = [
        f"# 周报 ({summaries[0]['date']} ~ {summaries[-1]['date']})",
        "",
        "## 📊 统计",
        f"- 记录天数: {len(summaries)}",
        f"- 总行数: {total_lines}",
        f"- 决策数: {len(all_decisions)}",
        f"- 待处理: {len(all_tasks)}",
        f"- 错误教训: {len(all_errors)}",
        f"- 重要内容: {len(all_important)}",
        "",
    ]
    
    if all_decisions:
        lines.append("## 🎯 本周决策")
        for d in all_decisions[:10]:
            lines.append(f"- {d}")
        lines.append("")
    
    if all_important:
        lines.append("## ⭐ 重要内容")
        for i in all_important[:10]:
            lines.append(f"- {i}")
        lines.append("")
    
    if all_errors:
        lines.append("## ⚠️ 错误教训")
        for e in all_errors[:5]:
            lines.append(f"- {e}")
        lines.append("")
    
    if all_tasks:
        lines.append("## 📋 待处理事项")
        for t in all_tasks[:10]:
            lines.append(f"- {t}")
        lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="生成记忆摘要")
    parser.add_argument("--workspace", default="~/.openclaw/workspace", help="工作空间路径")
    parser.add_argument("--type", choices=["daily", "weekly"], default="daily", help="摘要类型")
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--output", help="输出文件路径")
    args = parser.parse_args()
    
    workspace = Path(args.workspace).expanduser()
    memory_dir = workspace / "memory"
    
    # 确定日期范围
    if args.type == "daily":
        target_date = args.date or datetime.now().strftime("%Y-%m-%d")
        start_date = target_date
        end_date = target_date
    else:  # weekly
        if args.date:
            end = datetime.strptime(args.date, "%Y-%m-%d")
        else:
            end = datetime.now()
        start = end - timedelta(days=7)
        start_date = start.strftime("%Y-%m-%d")
        end_date = end.strftime("%Y-%m-%d")
    
    print(f"🔍 扫描记忆文件: {start_date} ~ {end_date}")
    files = find_memory_files(memory_dir, start_date, end_date)
    print(f"   找到 {len(files)} 个文件")
    
    summaries = []
    for f, date in files:
        s = extract_content_summary(f)
        summaries.append(s)
        print(f"   📄 {f.name}: {s['line_count']} 行, {len(s['decisions'])} 决策, {len(s['tasks'])} 任务")
    
    if args.type == "daily":
        output = generate_daily_summary(summaries)
    else:
        output = generate_weekly_summary(summaries)
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding="utf-8")
        print(f"\n✅ 摘要已保存到: {args.output}")
    else:
        print("\n" + "=" * 50)
        print(output)


if __name__ == "__main__":
    main()
