#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纠正自动记录系统
检测到用户纠正 → 立即写入 pending.md → 下次 heartbeat 合并到 LEARNINGS.md

使用方式:
    python auto_learn.py                     # 交互式添加记录
    python auto_learn.py "错误做法" "正确做法" "区域"  # 快速记录
    python auto_learn.py --flush             # 手动触发合并
    python auto_learn.py --status            # 查看当前状态
"""

import os
import sys
import json
import argparse
from datetime import datetime

# ============================================================
# 路径配置
# ============================================================
def _resolve_workspace():
    return os.path.expanduser(os.environ.get("QW_WORKSPACE", "~/.qclaw/workspace"))

WORKSPACE     = _resolve_workspace()
LEARNINGS_DIR = os.path.join(WORKSPACE, ".learnings")
SCRIPTS_DIR   = os.path.join(WORKSPACE, "scripts")
os.makedirs(LEARNINGS_DIR, exist_ok=True)

PENDING_FILE   = os.path.join(LEARNINGS_DIR, "pending.md")
LEARNINGS_FILE = os.path.join(LEARNINGS_DIR, "LEARNINGS.md")
ERRORS_FILE    = os.path.join(LEARNINGS_DIR, "ERRORS.md")

# ============================================================
# 纠正关键词检测
# ============================================================
CORRECTION_KEYWORDS = [
    # 打断/否定
    "不对", "错了", "不是", "等等", "等等等等", "停",
    # 纠正
    "重新", "重新来", "重新做", "你搞错了", "理解错了",
    "不是这样", "搞错了", "错了错了", "说错了",
    # 更正/质疑
    "更正", "纠正", "改正", "我什么时候说了", "我没说过",
    "我什么时候", "我没说",
    # 放弃/拒绝
    "不用了", "不需要", "不对不对", "不行", "不好",
    "错了别", "别说了", "不是这个", "搞反了",
]

def detect_correction(text: str) -> bool:
    """检测文本是否包含纠正关键词"""
    if not text:
        return False
    return any(kw in text for kw in CORRECTION_KEYWORDS)

def extract_context(text: str, max_chars: int = 200) -> str:
    """提取纠正上下文"""
    return text.strip()[:max_chars]

# ============================================================
# 记录操作
# ============================================================
def log_pending(wrong: str, right: str, area: str, priority: str = "中"):
    """写入 pending.md（待合并）"""
    now = datetime.now()
    entry = _format_entry(wrong, right, area, priority, now, status="未处理")
    _append_to_file(PENDING_FILE, entry)
    return entry

def _format_entry(wrong, right, area, priority, now, status="未处理"):
    date = now.strftime("%Y-%m-%d %H:%M")
    return (
        f"| {date} | {wrong} | {right} | {area} | {priority} | {status} |\n"
        f"| | | | | | |\n"
    )

def _ensure_header(file_path, headers):
    """确保文件有表头"""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(headers + "\n")

def _append_to_file(file_path, entry):
    _ensure_header(file_path, "| 时间 | 错误做法 | 正确做法 | 区域 | Priority | Status |")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)

def log_error(command: str, error_msg: str, consequence: str = ""):
    """记录命令失败"""
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M")
    entry = f"| {date} | {command} | {error_msg} | {consequence} |\n"
    _ensure_header(ERRORS_FILE, "| 时间 | 命令 | 错误 | 影响 |")
    with open(ERRORS_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

# ============================================================
# Flush：合并 pending → LEARNINGS
# ============================================================
def flush_pending():
    """将 pending.md 合并到 LEARNINGS.md"""
    if not os.path.exists(PENDING_FILE):
        return 0

    with open(PENDING_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        return 0

    # 追加到 LEARNINGS.md
    _ensure_header(LEARNINGS_FILE, "| 时间 | 错误做法 | 正确做法 | 区域 | Priority | Status |")
    with open(LEARNINGS_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + content)

    # 清空 pending.md（用 Python 写空内容，保留文件）
    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        pass  # 清空

    # 统计本次合并条数
    lines = [l for l in content.split('\n') if l.strip().startswith('|')]
    return len(lines)

# ============================================================
# 状态查看
# ============================================================
def status():
    """查看当前学习系统状态"""
    result = {
        "learnings_count": 0,
        "pending_count": 0,
        "errors_count": 0,
        "last_learnings": None,
    }

    # 统计 LEARNINGS.md
    if os.path.exists(LEARNINGS_FILE):
        with open(LEARNINGS_FILE, "r", encoding="utf-8") as f:
            lines = [l for l in f.read().split('\n') if l.strip().startswith('|')]
        result["learnings_count"] = len(lines)
        if lines:
            result["last_learnings"] = lines[-1][:100]

    # 统计 pending.md
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "r", encoding="utf-8") as f:
            lines = [l for l in f.read().split('\n') if l.strip().startswith('|')]
        result["pending_count"] = len(lines)

    # 统计 ERRORS.md
    if os.path.exists(ERRORS_FILE):
        with open(ERRORS_FILE, "r", encoding="utf-8") as f:
            lines = [l for l in f.read().split('\n') if l.strip().startswith('|')]
        result["errors_count"] = len(lines)

    return result

# ============================================================
# CLI 入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="纠正自动记录")
    parser.add_argument("wrong",   nargs='?', help="错误做法")
    parser.add_argument("right",   nargs='?', help="正确做法")
    parser.add_argument("area",    nargs='?', help="区域")
    parser.add_argument("--priority", default="中", help="优先级：高/中/低")
    parser.add_argument("--flush",  action="store_true", help="合并 pending → learnings")
    parser.add_argument("--status", action="store_true", help="查看状态")
    args = parser.parse_args()

    if args.flush:
        n = flush_pending()
        print(f"✅ 已合并 {n} 条到 LEARNINGS.md")
        return

    if args.status:
        s = status()
        print(f"📊 学习系统状态：")
        print(f"  总学习记录：{s['learnings_count']} 条")
        print(f"  待合并：{s['pending_count']} 条")
        print(f"  错误记录：{s['errors_count']} 条")
        if s['last_learnings']:
            print(f"  最近：{s['last_learnings']}")
        return

    if args.wrong:
        entry = log_pending(args.wrong, args.right or "（待补充）",
                           args.area or "通用", args.priority)
        print(f"✅ 已记录：{entry[:80]}")
        print(f"   下次 heartbeat 时自动合并到 LEARNINGS.md")
        return

    # 无参数：交互式
    print("📝 快速记录纠正")
    wrong = input("错误做法: ").strip()
    if not wrong:
        print("取消")
        return
    right = input("正确做法: ").strip()
    area  = input("区域（可回车跳过）: ").strip() or "通用"
    priority = input("优先级（高/中/低，默认中）: ").strip() or "中"

    entry = log_pending(wrong, right, area, priority)
    print(f"\n✅ 已写入 pending.md")
    print(f"   下次 heartbeat 时自动合并到 LEARNINGS.md")

if __name__ == "__main__":
    main()
