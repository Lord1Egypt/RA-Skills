#!/usr/bin/env python3
"""
汤圆育儿日志管理器

功能：
- append_log: 将姥姥的每日反馈追加到对应日期的日志文件中
- read_log: 读取指定日期的日志
- read_week_logs: 读取指定一周范围内的所有日志
- summarize_week: 汇总一周日志生成结构化摘要

日志存储路径: {base_dir}/tangyuan-logs/YYYY/MM/DD.md

用法:
    python log_manager.py append --date 2026-03-19 --data '{"meals":"吃了两碗饭","mood":"开心","activities":"画画、搭积木","learning":"学了3个新词","health":"正常","notes":"今天特别喜欢画画"}'
    python log_manager.py read --date 2026-03-19
    python log_manager.py read_week --date 2026-03-19
    python log_manager.py summarize_week --date 2026-03-19
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path


def get_log_dir(base_dir=None):
    """获取日志根目录"""
    if base_dir is None:
        base_dir = os.environ.get("TANGYUAN_LOG_DIR", os.getcwd())
    return Path(base_dir) / "tangyuan-logs"


def get_log_path(date_str, base_dir=None):
    """获取指定日期的日志文件路径"""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    log_dir = get_log_dir(base_dir)
    return log_dir / str(date.year) / f"{date.month:02d}" / f"{date.day:02d}.md"


def append_log(date_str, data, base_dir=None):
    """
    将反馈内容追加到指定日期的日志文件中。

    参数:
        date_str: 日期字符串，格式 YYYY-MM-DD
        data: dict，包含以下字段:
            - meals: 饮食情况
            - mood: 情绪状态
            - activities: 活动内容
            - learning: 学习内容
            - health: 身体状况
            - sleep: 睡眠情况（可选）
            - notes: 其他备注（可选）
        base_dir: 日志根目录（可选）
    """
    log_path = get_log_path(date_str, base_dir)

    # 自动创建目录
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # 获取当前时间作为记录时间
    now = datetime.now().strftime("%H:%M")
    date_display = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y年%m月%d日")
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekday_names[datetime.strptime(date_str, "%Y-%m-%d").weekday()]

    # 判断文件是否已存在
    is_new = not log_path.exists()

    with open(log_path, "a", encoding="utf-8") as f:
        if is_new:
            f.write(f"# 汤圆日志 - {date_display}（{weekday}）\n\n")

        f.write(f"## 反馈记录（{now}）\n\n")

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                # 如果不是 JSON，作为纯文本记录
                f.write(f"{data}\n\n")
                print(f"✅ 已记录反馈到 {log_path}")
                return str(log_path)

        fields = [
            ("meals", "🍚 饮食情况"),
            ("mood", "😊 情绪状态"),
            ("activities", "🎮 活动内容"),
            ("learning", "📚 学习内容"),
            ("health", "💪 身体状况"),
            ("sleep", "😴 睡眠情况"),
            ("notes", "📝 其他备注"),
        ]

        for key, label in fields:
            value = data.get(key, "")
            if value:
                f.write(f"### {label}\n{value}\n\n")

        f.write("---\n\n")

    print(f"✅ 已记录反馈到 {log_path}")
    return str(log_path)


def read_log(date_str, base_dir=None):
    """
    读取指定日期的日志内容。

    参数:
        date_str: 日期字符串，格式 YYYY-MM-DD
        base_dir: 日志根目录（可选）

    返回:
        日志内容字符串，如果不存在返回提示信息
    """
    log_path = get_log_path(date_str, base_dir)

    if not log_path.exists():
        return f"📭 {date_str} 暂无日志记录"

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    return content


def read_week_logs(date_str, base_dir=None):
    """
    读取包含指定日期在内的一周（周一到周日）的所有日志。

    参数:
        date_str: 日期字符串，格式 YYYY-MM-DD（该日期所在周的日志）
        base_dir: 日志根目录（可选）

    返回:
        dict，键为日期字符串，值为日志内容
    """
    date = datetime.strptime(date_str, "%Y-%m-%d")
    # 找到本周一
    monday = date - timedelta(days=date.weekday())

    week_logs = {}
    for i in range(7):
        day = monday + timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        content = read_log(day_str, base_dir)
        week_logs[day_str] = content

    return week_logs


def summarize_week(date_str, base_dir=None):
    """
    汇总一周日志，生成结构化摘要。

    参数:
        date_str: 日期字符串，格式 YYYY-MM-DD（该日期所在周）
        base_dir: 日志根目录（可选）

    返回:
        周汇总的 Markdown 字符串
    """
    week_logs = read_week_logs(date_str, base_dir)
    date = datetime.strptime(date_str, "%Y-%m-%d")
    monday = date - timedelta(days=date.weekday())
    sunday = monday + timedelta(days=6)

    monday_str = monday.strftime("%Y年%m月%d日")
    sunday_str = sunday.strftime("%Y年%m月%d日")

    summary = f"# 汤圆周报数据汇总（{monday_str} - {sunday_str}）\n\n"

    # 统计有日志的天数
    logged_days = 0
    for day_str, content in week_logs.items():
        if "暂无日志记录" not in content:
            logged_days += 1

    summary += f"## 概况\n\n"
    summary += f"- 本周共有 **{logged_days}/7** 天有反馈记录\n\n"

    # 逐日列出
    summary += f"## 每日记录\n\n"
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    for i, (day_str, content) in enumerate(week_logs.items()):
        summary += f"### {weekday_names[i]}（{day_str}）\n\n"
        if "暂无日志记录" not in content:
            # 去掉一级标题，只保留内容
            lines = content.split("\n")
            filtered = [line for line in lines if not line.startswith("# ")]
            summary += "\n".join(filtered).strip() + "\n\n"
        else:
            summary += "暂无记录\n\n"

    summary += "---\n\n"
    summary += "*以上数据供周报生成使用，请结合分析给出综合评估和建议。*\n"

    return summary


def list_logs(base_dir=None, limit=30):
    """
    列出最近的日志文件。

    参数:
        base_dir: 日志根目录（可选）
        limit: 返回最多多少条记录

    返回:
        日志文件路径列表
    """
    log_dir = get_log_dir(base_dir)

    if not log_dir.exists():
        return []

    log_files = sorted(log_dir.rglob("*.md"), reverse=True)
    return [str(f) for f in log_files[:limit]]


def main():
    parser = argparse.ArgumentParser(description="汤圆育儿日志管理器")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # append 命令
    append_parser = subparsers.add_parser("append", help="追加日志记录")
    append_parser.add_argument("--date", required=True, help="日期 (YYYY-MM-DD)")
    append_parser.add_argument("--data", required=True, help="反馈数据 (JSON字符串)")
    append_parser.add_argument("--base-dir", help="日志根目录")

    # read 命令
    read_parser = subparsers.add_parser("read", help="读取指定日期日志")
    read_parser.add_argument("--date", required=True, help="日期 (YYYY-MM-DD)")
    read_parser.add_argument("--base-dir", help="日志根目录")

    # read_week 命令
    week_parser = subparsers.add_parser("read_week", help="读取一周日志")
    week_parser.add_argument("--date", required=True, help="日期 (YYYY-MM-DD)")
    week_parser.add_argument("--base-dir", help="日志根目录")

    # summarize_week 命令
    summary_parser = subparsers.add_parser("summarize_week", help="生成周汇总")
    summary_parser.add_argument("--date", required=True, help="日期 (YYYY-MM-DD)")
    summary_parser.add_argument("--base-dir", help="日志根目录")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出最近的日志")
    list_parser.add_argument("--limit", type=int, default=30, help="最多返回条数")
    list_parser.add_argument("--base-dir", help="日志根目录")

    args = parser.parse_args()

    if args.command == "append":
        result = append_log(args.date, args.data, args.base_dir)
        print(f"日志已保存: {result}")

    elif args.command == "read":
        content = read_log(args.date, args.base_dir)
        print(content)

    elif args.command == "read_week":
        logs = read_week_logs(args.date, args.base_dir)
        for day, content in logs.items():
            print(f"\n{'='*40}")
            print(f"📅 {day}")
            print(f"{'='*40}")
            print(content)

    elif args.command == "summarize_week":
        summary = summarize_week(args.date, args.base_dir)
        print(summary)

    elif args.command == "list":
        files = list_logs(args.base_dir, args.limit)
        if files:
            print("最近的日志文件：")
            for f in files:
                print(f"  📄 {f}")
        else:
            print("暂无日志记录")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
