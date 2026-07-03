#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""todo-list skill 定时提醒调度器（双后端：WorkBuddy Automation + cron 降级）。

本模块提供 5 个子命令供定时任务调用：

    - daily-due：推送当天到期的 TODO（每天 09:00）
    - check-overdue：批量标记过期 TODO 为 'overdue'（每天 00:05）
    - upcoming：显示未来 N 天到期的 TODO（默认 7）
    - archive-cleanup：清理 30 天前的 archive 数据（每月 1 号）
    - setup：首次使用配置提醒通道

部署方式：
    - WorkBuddy 环境：通过 automation_update 创建 3 个 recurring automation
    - 非 WorkBuddy 环境：运行 ``./scripts/cron_setup.sh`` 安装 cron 任务

输出格式：
    纯文本（WorkBuddy 对话兼容），高优标记 [HIGH]。

技术决策：
    - 双后端支持：WorkBuddy Automation（优先） / 钉钉（降级）
    - 通道配置存储在 todos/config.json，首次使用通过 setup 命令选择
    - agent 通过 ``schedule_one_time_reminder()`` 获取参数后调用 automation_update

参见：
    - DESIGN.md §4.4（reminder 设计）
    - SKILL.md §WorkBuddy Automation 整合
    - SOUL.md 规则 15（数据源统一原则）

License:
    MIT

Version:
    1.5.0 (WorkBuddy Automation 整合)

Author:
    月海巫师 (Chen Qing)
"""
from __future__ import annotations  # PEP 563：延后求值类型注解

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .store import TodosStore

# ── 配置管理 ──────────────────────────────────────────────────

_SKILL_DIR = Path(__file__).resolve().parent.parent
_TODOS_DIR = _SKILL_DIR / "todos"
_CONFIG_PATH = _TODOS_DIR / "config.json"

DEFAULT_CONFIG = {
    "reminder_channel": "workbuddy",  # "workbuddy" | "dingtalk"
    "setup_completed": False,
    "setup_date": None,
}


def _ensure_todos_dir() -> None:
    """确保 todos 目录存在"""
    _TODOS_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """加载提醒配置。若不存在则返回默认值。"""
    _ensure_todos_dir()
    if not _CONFIG_PATH.exists():
        return dict(DEFAULT_CONFIG)
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        # 合并默认值（新字段兼容）
        merged = dict(DEFAULT_CONFIG)
        merged.update(cfg)
        return merged
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_CONFIG)


def save_config(cfg: dict) -> None:
    """保存提醒配置"""
    _ensure_todos_dir()
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def get_reminder_params(
    todo_id: int,
    content: str,
    due_at: str,
    lead_minutes: int = 60,
) -> dict | None:
    """
    获取一次性自动化提醒参数，供 agent 调用 automation_update 创建。

    Args:
        todo_id: TODO 的 ID
        content: TODO 内容
        due_at: 截止时间（ISO8601）
        lead_minutes: 提前多少分钟提醒（默认 60 分钟）

    Returns:
        automation_update 的参数字典，或 None（如果 due_at 距今 > 7 天则跳过）
    """
    from dateutil.parser import parse as dateparse

    try:
        due_dt = dateparse(due_at)
    except Exception:
        return None

    # 计算提醒时间
    remind_at = due_dt - timedelta(minutes=lead_minutes)
    now = datetime.now()

    # 如果已过期或 7 天后，跳过
    if due_dt < now:
        return None
    if (due_dt - now).days > 7:
        return None
    # 如果提醒时间已过（即快到截止时间了），用当前时间 + 1 分钟
    if remind_at <= now:
        remind_at = now + timedelta(minutes=1)

    return {
        "name": f"Todo提醒: {content[:30]}",
        "scheduleType": "once",
        "scheduledAt": remind_at.strftime("%Y-%m-%dT%H:%M:%S"),
        "prompt": (
            f"待办提醒 #[{todo_id}]「{content}」即将到期。\n"
            f"截止时间：{due_at}\n"
            f"请提醒月海巫师处理此待办，完成后可执行：\n"
            f"在 todo-list 中完成 #{todo_id}「{content}」"
        ),
    }


# ── 数据库查询 ────────────────────────────────────────────────

def get_today_due() -> list[dict]:
    """
    返回今天到期的 TODO 列表

    筛选条件：
    - status IN ('pending', 'in_progress')
    - due_at 距今 0~24 小时
    """
    store = TodosStore()
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    conn = store._get_connection()
    try:
        rows = conn.execute(
            """SELECT * FROM todos
               WHERE status IN ('pending', 'in_progress')
                 AND due_at IS NOT NULL
                 AND due_at >= ?
                 AND due_at < ?
               ORDER BY priority, due_at""",
            (today_start.strftime("%Y-%m-%d %H:%M:%S"),
             today_end.strftime("%Y-%m-%d %H:%M:%S")),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_overdue() -> list[dict]:
    """返回已过期但未标记为 overdue 的 TODO"""
    store = TodosStore()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = store._get_connection()
    try:
        rows = conn.execute(
            """SELECT * FROM todos
               WHERE status IN ('pending', 'in_progress', 'overdue')
                 AND due_at IS NOT NULL
                 AND due_at < ?
               ORDER BY due_at""",
            (now_str,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_upcoming(days: int = 7) -> list[dict]:
    """返回未来 N 天内到期的 TODO（默认 7）"""
    store = TodosStore()
    now = datetime.now()
    end = now + timedelta(days=days)
    conn = store._get_connection()
    try:
        rows = conn.execute(
            """SELECT * FROM todos
               WHERE status IN ('pending', 'in_progress')
                 AND due_at IS NOT NULL
                 AND due_at >= ?
                 AND due_at < ?
               ORDER BY due_at""",
            (now.strftime("%Y-%m-%d %H:%M:%S"),
             end.strftime("%Y-%m-%d %H:%M:%S")),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ── 消息格式化 ────────────────────────────────────────────────

def format_message(todos: list[dict], title: str = "今日待办") -> str:
    """
    格式化为推送消息（纯文本，兼容 WorkBuddy 对话 + 钉钉 Markdown）
    """
    if not todos:
        return f"[info] {title}：无待办事项"

    lines = [f"📋 **{title}** — 共 {len(todos)} 项", ""]

    priority_labels = {"high": "🔴 HIGH", "medium": "🟡 MED", "low": "🟢 LOW"}
    status_labels = {"pending": "⬜", "in_progress": "🔄", "overdue": "⚠️"}

    for todo in todos:
        status = todo.get("status", "pending")
        priority = todo.get("priority", "medium")
        due = todo.get("due_at", "")
        content = todo.get("content", "")

        sl = status_labels.get(status, "⬜")
        pl = priority_labels.get(priority, "🟡 MED")

        lines.append(f"{sl} [{pl}] {content}")
        if due:
            try:
                due_dt = datetime.strptime(due, "%Y-%m-%d %H:%M:%S")
                due_short = due_dt.strftime("%m/%d %H:%M")
                lines.append(f"   ⏰ {due_short}")
            except ValueError:
                lines.append(f"   ⏰ {due}")
        tags = todo.get("tags", "[]")
        if tags and tags != "[]":
            try:
                tag_list = json.loads(tags)
                if tag_list:
                    lines.append(f"   🏷 #{' #'.join(tag_list)}")
            except json.JSONDecodeError:
                pass

    return "\n".join(lines)


# ── 推送通道 ──────────────────────────────────────────────────

def push_to_channel(message: str, channel: str | None = None) -> bool:
    """
    根据配置推送到指定通道。

    - channel="workbuddy"（默认）：输出到 stdout，由 WorkBuddy agent 捕获
    - channel="dingtalk"：尝试 qwenpaw channels send，失败则降级到 stdout
    """
    if channel is None:
        cfg = load_config()
        channel = cfg.get("reminder_channel", "workbuddy")

    if channel == "workbuddy":
        # WorkBuddy 对话内：直接输出，agent 会捕获
        print(f"[todo-list] {message}")
        return True

    elif channel == "dingtalk":
        try:
            result = subprocess.run(
                ["qwenpaw", "channels", "send",
                 "--channel", "dingtalk",
                 "--message", message],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                print(f"[OK] 已推送钉钉")
                return True
            else:
                print(f"[WARN] 钉钉推送失败: {result.stderr}")
                # 降级到 stdout
                print(f"[todo-list] {message}")
                return False
        except FileNotFoundError:
            # qwenpaw 不存在（开发环境或非 QwenPaw 环境）
            print(f"[info] 钉钉通道不可用，降级到对话输出:")
            print(f"[todo-list] {message}")
            return False
        except subprocess.TimeoutExpired:
            print(f"[WARN] 钉钉推送超时，降级到对话输出:")
            print(f"[todo-list] {message}")
            return False
        except Exception as e:
            print(f"[ERR] 推送异常: {e}")
            print(f"[todo-list] {message}")
            return False
    else:
        print(f"[WARN] 未知通道: {channel}，降级到对话输出:")
        print(f"[todo-list] {message}")
        return False


# ── CLI 子命令 ────────────────────────────────────────────────

def cmd_daily_due(args: argparse.Namespace) -> int:
    """daily-due 子命令：推送当天到期的 TODO"""
    todos = get_today_due()
    message = format_message(todos, title="今日待办提醒")
    print(message)
    if not todos:
        return 0
    if args.push:
        push_to_channel(message, channel=args.channel)
    return 0


def cmd_check_overdue(args: argparse.Namespace) -> int:
    """check-overdue 子命令：批量标记过期 + 推送"""
    store = TodosStore()
    overdue = store.check_overdue()

    if overdue:
        # 也检查已处于 overdue 状态的
        all_overdue = get_overdue()
        message = format_message(
            [d for d in all_overdue if d["status"] == "overdue"],
            title="⚠️ 过期待办"
        )
        # 重新格式化为过期专用标题
        newly_marked = len(overdue)
        message = f"⚠️ **过期待办提醒** — 新增 {newly_marked} 项\n\n{format_message(all_overdue, title='全部过期')}"
        print(message)
        if args.push:
            push_to_channel(message, channel=args.channel)
    else:
        print("[info] 无过期 TODO")
    return 0


def cmd_archive_cleanup(args: argparse.Namespace) -> int:
    """archive-cleanup 子命令：清理 30 天前 archive"""
    store = TodosStore()
    count = store.archive_cleanup(days=args.days)
    print(f"[OK] 清理 {count} 条 {args.days} 天前 archive 记录")
    return 0


def cmd_upcoming(args: argparse.Namespace) -> int:
    """upcoming 子命令：未来 N 天待办"""
    todos = get_upcoming(days=args.days)
    message = format_message(todos, title=f"未来 {args.days} 天待办")
    print(message)
    if not todos:
        return 0
    if args.push:
        push_to_channel(message, channel=args.channel)
    return 0


def cmd_setup(args: argparse.Namespace) -> int:
    """setup 子命令：首次使用配置提醒通道"""
    cfg = load_config()

    if cfg.get("setup_completed") and not args.force:
        print(f"[info] 已配置完成。当前通道: {cfg.get('reminder_channel', 'workbuddy')}")
        print(f"        撤回重新配置请加 --force")
        return 0

    # 输出交互式配置提示（由 agent 解析并引导用户选择）
    print("=" * 50)
    print("📋 todo-list 提醒通道配置")
    print("=" * 50)
    print()
    print("请选择提醒推送通道：")
    print("  [1] WorkBuddy 对话内提醒（推荐）")
    print("      提醒直接出现在 WorkBuddy 对话中，无需外部 App")
    print("  [2] 钉钉推送")
    print("      通过 qwenpaw channels 推送到钉钉")
    print()
    print("请输入 1 或 2 选择，或用参数 --channel workbuddy/dingtalk 直接指定")
    print()

    if args.channel:
        chosen = args.channel
    else:
        # 等待 agent 交互式确认
        print("⚡ 请 agent 引导用户选择通道后，用 --channel 参数重新调用")
        return 0

    if chosen not in ("workbuddy", "dingtalk"):
        print(f"[ERR] 无效通道: {chosen}，只支持 workbuddy / dingtalk")
        return 1

    cfg["reminder_channel"] = chosen
    cfg["setup_completed"] = True
    cfg["setup_date"] = datetime.now().isoformat()
    save_config(cfg)

    print()
    print(f"✅ 提醒通道已配置为: {chosen}")
    if chosen == "workbuddy":
        print()
        print("💡 提醒将通过 WorkBuddy Automation 自动推送。")
        print("   需要由 agent 创建以下自动化任务：")
        print("   - 每日 overdue 检查（00:05）")
        print("   - 每日待办提醒（09:00）")
        print("   - 月度归档清理（每月1日）")
    else:
        print()
        print("💡 提醒将通过 qwenpaw cron 推送到钉钉。")
        print("   请运行 scripts/cron_setup.sh 注册 cron 任务。")

    return 0


def cmd_config(args: argparse.Namespace) -> int:
    """config 子命令：查看当前配置"""
    cfg = load_config()
    print(json.dumps(cfg, indent=2, ensure_ascii=False))
    return 0


# ── argparse ──────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """构建 argparse 解析器"""
    parser = argparse.ArgumentParser(
        prog="reminder",
        description="todo-list 定时提醒（v1.5.0 — WorkBuddy Automation）",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ── daily-due ──
    p_dd = subparsers.add_parser("daily-due", help="推送当天到期")
    p_dd.add_argument("--push", action="store_true", help="实际推送到 channel")
    p_dd.add_argument("--channel", default=None, help="推送通道（不指定则使用配置）")
    p_dd.set_defaults(func=cmd_daily_due)

    # ── check-overdue ──
    p_co = subparsers.add_parser("check-overdue", help="批量标记过期")
    p_co.add_argument("--push", action="store_true", help="实际推送到 channel")
    p_co.add_argument("--channel", default=None, help="推送通道（不指定则使用配置）")
    p_co.set_defaults(func=cmd_check_overdue)

    # ── upcoming ──
    p_up = subparsers.add_parser("upcoming", help="未来 N 天")
    p_up.add_argument("--days", type=int, default=7, help="天数（默认 7）")
    p_up.add_argument("--push", action="store_true", help="实际推送")
    p_up.add_argument("--channel", default=None, help="推送通道（不指定则使用配置）")
    p_up.set_defaults(func=cmd_upcoming)

    # ── archive-cleanup ──
    p_ac = subparsers.add_parser("archive-cleanup", help="清理 30 天前 archive")
    p_ac.add_argument("--days", type=int, default=30, help="天数（默认 30）")
    p_ac.set_defaults(func=cmd_archive_cleanup)

    # ── setup ──
    p_setup = subparsers.add_parser(
        "setup",
        help="首次使用配置提醒通道（交互式）",
        description="配置提醒推送通道：workbuddy（对话内） / dingtalk（钉钉）",
    )
    p_setup.add_argument(
        "--channel", default=None,
        help="直接指定通道: workbuddy / dingtalk",
    )
    p_setup.add_argument(
        "--force", action="store_true",
        help="强制重新配置",
    )
    p_setup.set_defaults(func=cmd_setup)

    # ── config ──
    p_cfg = subparsers.add_parser("config", help="查看当前配置")
    p_cfg.set_defaults(func=cmd_config)

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI 入口"""
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
