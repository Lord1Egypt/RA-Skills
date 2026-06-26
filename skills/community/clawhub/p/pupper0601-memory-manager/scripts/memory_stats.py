#!/usr/bin/env python3
"""
memory_stats.py - 生成记忆系统统计报告（支持多用户 + 公共记忆）

用法:
  python scripts/memory_stats.py [--base-dir PATH] [--uid UID] [--update] [--scope private|shared|all]

选项:
  --uid     用户ID（默认: MEMORY_USER_ID 环境变量或 "default"）
  --update  将统计结果写回 STATS.md（否则仅打印）
  --scope   统计范围: private（仅私人）/ shared（仅公共）/ all（默认）
"""

import os
import sys
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter


def count_entries(filepath):
    if not os.path.exists(filepath):
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return len(re.findall(r"^## ", content, re.MULTILINE))


def count_todos(filepath):
    if not os.path.exists(filepath):
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return len(re.findall(r"^- \[ \]", content, re.MULTILINE))


def extract_tags(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return re.findall(r"#(\w[\w-]*)", content)


def count_lines(filepath):
    if not os.path.exists(filepath):
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def get_file_mtime(filepath):
    if not os.path.exists(filepath):
        return None
    return datetime.fromtimestamp(os.path.getmtime(filepath))


def scan_layer(dir_path, extensions=(".md",)):
    """扫描一个目录，返回文件元数据列表"""
    files = []
    if not os.path.exists(dir_path):
        return files
    for fname in sorted(os.listdir(dir_path), reverse=True):
        if not fname.endswith(extensions):
            continue
        fpath = os.path.join(dir_path, fname)
        files.append({
            "name": fname,
            "path": fpath,
            "lines": count_lines(fpath),
            "entries": count_entries(fpath),
            "todos": count_todos(fpath),
            "tags": extract_tags(fpath),
            "mtime": get_file_mtime(fpath),
        })
    return files


def analyze_user(base_dir, uid):
    """分析单个用户的记忆统计"""
    user_dir = os.path.join(base_dir, "users", uid)
    daily_dir = os.path.join(user_dir, "daily")
    weekly_dir = os.path.join(user_dir, "weekly")
    permanent_dir = os.path.join(user_dir, "permanent")

    stats = {
        "uid": uid,
        "l1": {"files": [], "total_entries": 0, "total_todos": 0, "total_lines": 0},
        "l2": {"files": [], "total_entries": 0, "total_lines": 0},
        "l3": {"categories": {}, "total_entries": 0, "total_lines": 0},
        "habits": {"entries": 0, "mtime": None},
        "tags": Counter(),
        "suggestions": [],
        "health": {},
    }

    l3_categories = ["decisions", "tech-stack", "projects", "people", "knowledge", "lessons", "preferences"]

    # L1
    l1_files = scan_layer(daily_dir)
    for f in l1_files:
        stats["l1"]["files"].append(f)
        stats["l1"]["total_entries"] += f["entries"]
        stats["l1"]["total_todos"] += f["todos"]
        stats["l1"]["total_lines"] += f["lines"]
        stats["tags"].update(f["tags"])
        if f["lines"] > 150:
            stats["suggestions"].append(f"⚠️ {uid}/L1/{f['name']} 超过150行（{f['lines']}行）")

    # L2
    l2_files = scan_layer(weekly_dir)
    for f in l2_files:
        stats["l2"]["files"].append(f)
        stats["l2"]["total_entries"] += f["entries"]
        stats["l2"]["total_lines"] += f["lines"]
        stats["tags"].update(f["tags"])
        if f["lines"] > 200:
            stats["suggestions"].append(f"⚠️ {uid}/L2/{f['name']} 超过200行（{f['lines']}行）")

    # L3
    for cat in l3_categories:
        fpath = os.path.join(permanent_dir, f"{cat}.md")
        if os.path.exists(fpath):
            entries = count_entries(fpath)
            lines = count_lines(fpath)
            mtime = get_file_mtime(fpath)
            tags = extract_tags(fpath)
            stats["l3"]["categories"][cat] = {
                "entries": entries,
                "lines": lines,
                "last_updated": mtime.strftime("%Y-%m-%d") if mtime else "—",
                "tags": tags,
            }
            stats["l3"]["total_entries"] += entries
            stats["l3"]["total_lines"] += lines
            stats["tags"].update(tags)
            if lines > 300:
                stats["suggestions"].append(f"⚠️ {uid}/L3/{cat}.md 超过300行（{lines}行）")

    # HABITS
    habits_path = os.path.join(user_dir, "HABITS.md")
    stats["habits"]["entries"] = count_entries(habits_path)
    stats["habits"]["mtime"] = get_file_mtime(habits_path)

    # 健康度
    l1_max = max((f["lines"] for f in l1_files), default=0)
    l2_max = max((f["lines"] for f in l2_files), default=0)
    stats["health"]["l1"] = "🔴 需立即压缩" if l1_max > 200 else ("⚠️ 建议压缩" if l1_max > 150 else "✅ 正常")
    stats["health"]["l2"] = "🔴 需立即压缩" if l2_max > 250 else ("⚠️ 建议压缩" if l2_max > 200 else "✅ 正常")

    # 索引健康度
    index_path = os.path.join(user_dir, "INDEX.md")
    index_mtime = get_file_mtime(index_path)
    if index_mtime and (datetime.now() - index_mtime).days > 1:
        stats["health"]["index"] = f"⚠️ 过期（{index_mtime.strftime('%Y-%m-%d')}）"
        stats["suggestions"].append(f"💡 {uid}: 更新 INDEX.md")
    else:
        stats["health"]["index"] = "✅ 最新"

    return stats


def analyze_shared(base_dir):
    """分析公共记忆统计"""
    shared_dir = os.path.join(base_dir, "shared")
    daily_dir = os.path.join(shared_dir, "daily")
    weekly_dir = os.path.join(shared_dir, "weekly")
    permanent_dir = os.path.join(shared_dir, "permanent")

    stats = {
        "daily": {"files": scan_layer(daily_dir), "total_entries": 0, "total_todos": 0},
        "weekly": {"files": scan_layer(weekly_dir), "total_entries": 0},
        "l3": {"categories": {}, "total_entries": 0},
        "tags": Counter(),
        "suggestions": [],
        "health": {},
    }

    shared_l3_cats = ["decisions", "tech-stack", "projects", "knowledge"]

    # shared daily
    for f in stats["daily"]["files"]:
        stats["daily"]["total_entries"] += f["entries"]
        stats["daily"]["total_todos"] += f["todos"]
        stats["tags"].update(f["tags"])

    # shared weekly
    for f in stats["weekly"]["files"]:
        stats["weekly"]["total_entries"] += f["entries"]
        stats["tags"].update(f["tags"])

    # shared L3
    for cat in shared_l3_cats:
        fpath = os.path.join(permanent_dir, f"{cat}.md")
        if os.path.exists(fpath):
            entries = count_entries(fpath)
            lines = count_lines(fpath)
            mtime = get_file_mtime(fpath)
            tags = extract_tags(fpath)
            stats["l3"]["categories"][cat] = {
                "entries": entries,
                "lines": lines,
                "last_updated": mtime.strftime("%Y-%m-%d") if mtime else "—",
            }
            stats["l3"]["total_entries"] += entries
            stats["tags"].update(tags)

    return stats


def format_user_report(stats):
    """格式化单个用户的统计报告"""
    uid = stats["uid"]
    l1f = stats["l1"]["files"]
    l2f = stats["l2"]["files"]
    l3c = stats["l3"]["categories"]
    l1_max = max((f["lines"] for f in l1f), default=0)
    l2_max = max((f["lines"] for f in l2f), default=0)
    tags_top = stats["tags"].most_common(10)

    # 最近7天活跃
    today = datetime.now().date()
    recent = sum(
        f["entries"] for f in l1f
        if f["mtime"] and (today - f["mtime"].date()).days <= 7
    )

    report = f"""
## 👤 {uid}

| 指标 | 数值 |
|------|------|
| L1 文件数 | {len(l1f)} |
| L2 文件数 | {len(l2f)} |
| L3 条目总数 | {stats['l3']['total_entries']} |
| 习惯记录条数 | {stats['habits']['entries']} |
| 最近7天新增 | {recent} 条 |
| 未完成任务 | {stats['l1']['total_todos']} 条 |

### L1 状态: {stats['health']['l1']} (最大: {l1_max}行)
### L2 状态: {stats['health']['l2']} (最大: {l2_max}行)
### 索引: {stats['health']['index']}

### L3 永久记忆
| 分类 | 条目 | 最近更新 |
|------|------|----------|
"""
    for cat, data in l3c.items():
        report += f"| {cat} | {data['entries']} | {data['last_updated']} |\nfrom typing import List, Dict, Optional, Union, Any, Tuple\n"

    if tags_top:
        report += "\n**热门标签**: " + " ".join(f"#{t}({c})" for t, c in tags_top[:8]) + "\n"

    return report


def format_shared_report(stats):
    """格式化公共记忆统计报告"""
    tags_top = stats["tags"].most_common(8)
    l3c = stats["l3"]["categories"]

    report = f"""
## 🌐 公共记忆

| 指标 | 数值 |
|------|------|
| 公共 L1 文件数 | {len(stats['daily']['files'])} |
| 公共 L2 文件数 | {len(stats['weekly']['files'])} |
| 公共 L3 条目总数 | {stats['l3']['total_entries']} |
| 公共未完成任务 | {stats['daily']['total_todos']} 条 |

### 公共 L3
| 分类 | 条目 | 最近更新 |
|------|------|----------|
"""
    for cat, data in l3c.items():
        report += f"| {cat} | {data['entries']} | {data['last_updated']} |\n"

    if tags_top:
        report += "\n**公共热门标签**: " + " ".join(f"#{t}({c})" for t, c in tags_top[:8]) + "\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="生成记忆系统统计报告")
    parser.add_argument("--base-dir", default=".", help="记忆仓库根目录")
    parser.add_argument("--uid", help="用户ID（默认: MEMORY_USER_ID 或 'default'）")
    parser.add_argument("--update", action="store_true", help="将统计结果写入 STATS.md")
    parser.add_argument("--scope", default="all", choices=["private", "shared", "all"],
                        help="统计范围")
    args = parser.parse_args()

    base_dir = os.path.abspath(args.base_dir)
    uid = args.uid or os.environ.get("MEMORY_USER_ID", "default")

    print(f"\n📊 记忆统计报告")
    print(f"📁 仓库: {base_dir}")
    print(f"👤 用户: {uid}\n")

    all_suggestions = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    report = f"# Memory Statistics\n_最后更新: {now}_\n\n---\n\n"

    # 私人统计
    if args.scope in ("private", "all"):
        user_dir = os.path.join(base_dir, "users", uid)
        if os.path.exists(user_dir):
            user_stats = analyze_user(base_dir, uid)
            report += format_user_report(user_stats)
            all_suggestions.extend(user_stats["suggestions"])
        else:
            report += f"\n## 👤 {uid}\n_（目录不存在，请先初始化）_\n\n"

    # 公共统计
    if args.scope in ("shared", "all"):
        shared_dir = os.path.join(base_dir, "shared")
        if os.path.exists(shared_dir):
            shared_stats = analyze_shared(base_dir)
            report += format_shared_report(shared_stats)
            all_suggestions.extend(shared_stats["suggestions"])
        else:
            report += "\n## 🌐 公共记忆\n_（目录不存在）_\n\n"

    # 系统建议
    report += "\n---\n\n## 💡 系统建议\n"
    if all_suggestions:
        for s in all_suggestions:
            report += f"- {s}\n"
    else:
        report += "- ✅ 记忆系统状态良好\n"

    print(report)

    if args.update:
        # 写两份：私人 STATS + 公共 STATS
        if args.scope in ("private", "all"):
            stats_path = os.path.join(base_dir, "users", uid, "STATS.md")
            os.makedirs(os.path.dirname(stats_path), exist_ok=True)
            user_report = f"# Memory Statistics ({uid})\n_最后更新: {now}_\n\n---\n\n"
            if os.path.exists(os.path.join(base_dir, "users", uid)):
                user_stats = analyze_user(base_dir, uid)
                user_report += format_user_report(user_stats)
            user_report += "\n---\n\n## 💡 系统建议\n"
            if all_suggestions:
                for s in all_suggestions:
                    user_report += f"- {s}\n"
            else:
                user_report += "- ✅ 状态良好\n"
            with open(stats_path, "w", encoding="utf-8") as f:
                f.write(user_report)
            print(f"\n✅ 个人统计已写入: users/{uid}/STATS.md")

        if args.scope in ("shared", "all"):
            shared_stats_path = os.path.join(base_dir, "shared", "STATS.md")
            if os.path.exists(os.path.join(base_dir, "shared")):
                shared_stats = analyze_shared(base_dir)
                s_report = f"# Shared Memory Statistics\n_最后更新: {now}_\n\n---\n\n"
                s_report += format_shared_report(shared_stats)
                os.makedirs(os.path.dirname(shared_stats_path), exist_ok=True)
                with open(shared_stats_path, "w", encoding="utf-8") as f:
                    f.write(s_report)
                print(f"✅ 公共统计已写入: shared/STATS.md")


if __name__ == "__main__":
    main()
