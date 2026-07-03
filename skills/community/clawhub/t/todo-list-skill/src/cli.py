#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""todo-list skill 命令行接口。

本模块提供 8 个子命令的 CLI 入口：add / list / done / delete / update /
stats / init / check-overdue。

输出格式：
    - text（默认）：人类可读，带 [OK]/[ ]/[X]/[~]/[!] 图标
    - json：机器可读 JSON（用于脚本）

退出码（参考 sysexits.h 约定）：
    - 0：成功
    - 1：业务错误（未找到 / 歧义）
    - 2：用法错误（参数校验 / 非法参数）
    - 70：系统错误（数据库损坏）

使用示例：
    $ todos add "检查止损" --priority high
    $ todos list --priority high --format json
    $ todos done 1
    $ todos stats

参见：
    - DESIGN.md §4.2（CLI 设计）
    - references/commands.md（完整 CLI 参考）
    - Click 框架：https://click.palletsprojects.com/（业界替代）
    - 12-Factor App §IX：https://12factor.net/disposability

License:
    MIT

Version:
    1.4.0

Author:
    月海巫师 (Chen Qing)
"""
from __future__ import annotations  # PEP 563：延后求值类型注解

import argparse
import json
import sys
from typing import Any

from .exceptions import (
    TodoAmbiguousError,
    TodoDatabaseError,
    TodoNotFoundError,
    TodoValidationError,
)
from .store import TodosStore

# ── 退出码（业界参考：sysexits.h） ────────────────────────────────
EXIT_OK = 0          # 成功
EXIT_USAGE = 2       # 用户错误（参数/校验）
EXIT_DATAERR = 1     # 业务错误（未找到/歧义）
EXIT_SOFTWARE = 70   # 系统错误（DB 损坏）


def format_todo(todo: dict, fmt: str = "text") -> str:
    """
    格式化单条 TODO 输出

    fmt:
      - text: 人类可读（带 [OK]/[ ] 符号）
      - json: JSON 字符串
    """
    if fmt == "json":
        return json.dumps(todo, ensure_ascii=False, indent=2)

    # text 格式
    status = todo.get("status", "pending")
    icon = {
        "pending": "[ ]",
        "in_progress": "[~]",
        "completed": "[OK]",
        "cancelled": "[X]",
        "overdue": "[!]",
    }.get(status, "[?]")

    priority = todo.get("priority", "medium")
    p_icon = {"high": "!!", "medium": "•", "low": "·"}.get(priority, "·")

    due = todo.get("due_at", "") or ""
    tags = todo.get("tags", "[]")

    parts = [
        f"{icon} [{todo['id']}] {p_icon} {todo['content']}",
    ]
    if due:
        parts.append(f"   due: {due}")
    if tags and tags != "[]":
        parts.append(f"   tags: {tags}")

    return "\n".join(parts)


def cmd_add(args: argparse.Namespace) -> int:
    """add 子命令：添加 TODO"""
    store = TodosStore()
    try:
        # 解析 tags（逗号分隔）
        tags = None
        if args.tag:
            tags = [t.strip() for t in args.tag.split(",") if t.strip()]

        todo = store.add(
            content=args.content,
            active_form=args.active_form,
            due_at=args.due,
            priority=args.priority,
            tags=tags,
            source="cli",
            raw_input=args.content,
        )
        print(format_todo(todo, fmt=args.format))
        return EXIT_OK
    except TodoValidationError as e:
        print(f"[FAIL] 校验失败: {e}", file=sys.stderr)
        return EXIT_USAGE
    except TodoDatabaseError as e:
        print(f"[FAIL] 数据库错误: {e}", file=sys.stderr)
        return EXIT_SOFTWARE


def cmd_list(args: argparse.Namespace) -> int:
    """list 子命令：查询 TODO"""
    store = TodosStore()
    try:
        todos = store.list(
            status=args.status,
            tag=args.tag,
            priority=args.priority,
            overdue=args.overdue,
            all=args.all,
        )
        # list 子命令的 format 在子 parser 也有同名参数
        fmt = getattr(args, "format", "text")
        if not todos:
            if fmt == "json":
                print("[]")
            else:
                print("[info] 没有匹配的 TODO")
            return EXIT_OK

        if fmt == "json":
            print(json.dumps(todos, ensure_ascii=False, indent=2))
        else:
            print(f"[list] 共 {len(todos)} 条:")
            print()
            for todo in todos:
                print(format_todo(todo, fmt="text"))
        return EXIT_OK
    except TodoDatabaseError as e:
        print(f"[FAIL] 数据库错误: {e}", file=sys.stderr)
        return EXIT_SOFTWARE


def cmd_done(args: argparse.Namespace) -> int:
    """done 子命令：完成 TODO"""
    store = TodosStore()
    try:
        todo = store.done(args.target)
        print(format_todo(todo, fmt=args.format))
        return EXIT_OK
    except TodoNotFoundError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        return EXIT_DATAERR
    except TodoAmbiguousError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        print("请用 ID 精确指定：", file=sys.stderr)
        for c in e.candidates:
            print(f"  [{c['id']}] {c['content']}", file=sys.stderr)
        return EXIT_DATAERR
    except TodoDatabaseError as e:
        print(f"[FAIL] 数据库错误: {e}", file=sys.stderr)
        return EXIT_SOFTWARE


def cmd_delete(args: argparse.Namespace) -> int:
    """delete 子命令：软删除"""
    store = TodosStore()
    try:
        todo = store.delete(args.target)
        print(f"[OK] 已删除: [{todo['id']}] {todo['content']}")
        return EXIT_OK
    except TodoNotFoundError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        return EXIT_DATAERR
    except TodoAmbiguousError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        for c in e.candidates:
            print(f"  [{c['id']}] {c['content']}", file=sys.stderr)
        return EXIT_DATAERR
    except TodoDatabaseError as e:
        print(f"[FAIL] 数据库错误: {e}", file=sys.stderr)
        return EXIT_SOFTWARE


def cmd_update(args: argparse.Namespace) -> int:
    """update 子命令：更新字段"""
    store = TodosStore()
    try:
        # 收集要更新的字段
        kwargs: dict[str, Any] = {}
        if args.content is not None:
            kwargs["content"] = args.content
        if args.due is not None:
            kwargs["due_at"] = args.due
        if args.priority is not None:
            kwargs["priority"] = args.priority
        if args.tag is not None:
            kwargs["tags"] = [t.strip() for t in args.tag.split(",") if t.strip()]
        if args.status is not None:
            kwargs["status"] = args.status

        if not kwargs:
            print("[FAIL] 至少指定一个要更新的字段", file=sys.stderr)
            return EXIT_USAGE

        todo = store.update(args.id, **kwargs)
        print(format_todo(todo, fmt=args.format))
        return EXIT_OK
    except TodoNotFoundError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        return EXIT_DATAERR
    except TodoValidationError as e:
        print(f"[FAIL] 校验失败: {e}", file=sys.stderr)
        return EXIT_USAGE
    except TodoDatabaseError as e:
        print(f"[FAIL] 数据库错误: {e}", file=sys.stderr)
        return EXIT_SOFTWARE


def cmd_stats(args: argparse.Namespace) -> int:
    """stats 子命令：统计"""
    store = TodosStore()
    try:
        stats = store.stats()
        fmt = getattr(args, "format", "text")
        if fmt == "json":
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print("[stats] TODO 统计:")
            print(f"  总数:       {stats['total']}")
            print(f"  待办:       {stats['pending']}")
            print(f"  进行中:     {stats['in_progress']}")
            print(f"  已完成:     {stats['completed']}")
            print(f"  取消:       {stats['cancelled']}")
            print(f"  过期:       {stats['overdue']}")
            print()
            print(f"  高优先级:   {stats['high_priority']}")
            print(f"  中优先级:   {stats['medium_priority']}")
            print(f"  低优先级:   {stats['low_priority']}")
            print()
            print(f"  本周到期:   {stats['this_week']}")
        return EXIT_OK
    except TodoDatabaseError as e:
        print(f"[FAIL] 数据库错误: {e}", file=sys.stderr)
        return EXIT_SOFTWARE


def cmd_init(args: argparse.Namespace) -> int:
    """init 子命令：初始化数据库"""
    store = TodosStore()
    try:
        store.init_db()
        return EXIT_OK
    except TodoDatabaseError as e:
        print(f"[FAIL] 数据库错误: {e}", file=sys.stderr)
        return EXIT_SOFTWARE


def cmd_check_overdue(args: argparse.Namespace) -> int:
    """check_overdue 子命令：批量标记 overdue"""
    store = TodosStore()
    try:
        overdue = store.check_overdue()
        print(f"[info] 标记了 {len(overdue)} 条过期 TODO")
        for todo in overdue:
            print(f"  [{todo['id']}] {todo['content']} (due: {todo.get('due_at')})")
        return EXIT_OK
    except TodoDatabaseError as e:
        print(f"[FAIL] 数据库错误: {e}", file=sys.stderr)
        return EXIT_SOFTWARE


def build_parser() -> argparse.ArgumentParser:
    """构建 argparse 解析器"""
    parser = argparse.ArgumentParser(
        prog="todos",
        description="TODO 列表管理工具（v1.0）",
    )
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="输出格式（默认 text）",
    )
    parser.add_argument(
        "--db-path", default=None,
        help="数据库路径（默认使用 $TODOS_DB_PATH 或 ./todos.db）",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ── add ──
    p_add = subparsers.add_parser("add", help="添加 TODO")
    p_add.add_argument("content", help="TODO 内容（命令式：'检查止损'）")
    p_add.add_argument("--active-form", help="进行时（默认从 content 推断）")
    p_add.add_argument("--due", help="截止时间（ISO8601 字符串）")
    p_add.add_argument(
        "--priority", choices=["high", "medium", "low"], default="medium",
        help="优先级（默认 medium）",
    )
    p_add.add_argument("--tag", help="标签（逗号分隔）")
    p_add.set_defaults(func=cmd_add)

    # ── list ──
    p_list = subparsers.add_parser("list", help="查询 TODO")
    p_list.add_argument("--status", help="按状态过滤")
    p_list.add_argument("--tag", help="按标签过滤")
    p_list.add_argument(
        "--priority", choices=["high", "medium", "low"],
        help="按优先级过滤",
    )
    p_list.add_argument("--overdue", action="store_true", help="只显示过期")
    p_list.add_argument("--all", action="store_true", help="显示所有状态")
    p_list.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="输出格式（默认 text）",
    )
    p_list.set_defaults(func=cmd_list)

    # ── done ──
    p_done = subparsers.add_parser("done", help="完成 TODO")
    p_done.add_argument("target", help="TODO ID 或 content 模糊匹配")
    p_done.set_defaults(func=cmd_done)

    # ── delete ──
    p_del = subparsers.add_parser("delete", help="软删除 TODO")
    p_del.add_argument("target", help="TODO ID 或 content 模糊匹配")
    p_del.set_defaults(func=cmd_delete)

    # ── update ──
    p_upd = subparsers.add_parser("update", help="更新 TODO")
    p_upd.add_argument("id", type=int, help="TODO ID")
    p_upd.add_argument("--content", help="新内容")
    p_upd.add_argument("--due", help="新截止时间")
    p_upd.add_argument(
        "--priority", choices=["high", "medium", "low"], help="新优先级",
    )
    p_upd.add_argument("--tag", help="新标签（逗号分隔）")
    p_upd.add_argument("--status", help="新状态")
    p_upd.set_defaults(func=cmd_update)

    # ── stats ──
    p_stats = subparsers.add_parser("stats", help="统计")
    p_stats.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="输出格式（默认 text）",
    )
    p_stats.set_defaults(func=cmd_stats)

    # ── init ──
    p_init = subparsers.add_parser("init", help="初始化数据库")
    p_init.set_defaults(func=cmd_init)

    # ── check-overdue ──
    p_co = subparsers.add_parser("check-overdue", help="批量标记过期")
    p_co.set_defaults(func=cmd_check_overdue)

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI 入口"""
    parser = build_parser()
    args = parser.parse_args(argv)

    # 自定义 DB 路径（支持全局和子命令后）
    db_path = getattr(args, "db_path", None)
    if db_path:
        import os
        os.environ["TODOS_DB_PATH"] = db_path
        # 重置单例 + 更新 DB_PATH 以使新路径生效
        from . import store as store_module
        store_module.TodosStore._instance = None
        store_module.DB_PATH = db_path

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())