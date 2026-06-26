"""Command-line interface for tg-monitor-kit."""

from __future__ import annotations

import argparse
import asyncio
import sys


def main() -> None:
    parser = argparse.ArgumentParser(prog="tg-monitor", description="Telegram monitor & tools")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("monitor", help="关键词监控（长驻）")
    sub.add_parser("search", help="群搜索定时任务（长驻）")
    p_join = sub.add_parser("join", help="从清单定时批量加群（长驻）")
    p_join.add_argument(
        "--once",
        action="store_true",
        help="只执行一轮后退出（不调度等待）",
    )
    sub.add_parser("send-schedule", help="按配置执行定时群发（长驻）")
    sub.add_parser("groups", help="列出已加入的群")
    sub.add_parser("account-info", help="打印当前登录账号信息")

    p_members = sub.add_parser("members", help="列出指定群成员")
    p_members.add_argument("--group", "-g", required=True, help="群名称（与 Telegram 中一致）")

    p_history = sub.add_parser("history", help="导出群最近消息")
    p_history.add_argument("--group", "-g", required=True, help="群名称")
    p_history.add_argument("--limit", "-n", type=int, default=100, help="条数")

    sub.add_parser("auth", help="请求短信验证码")
    sub.add_parser("login", help="用 TG_CODE + TG_PHONE_CODE_HASH 登录")

    args = parser.parse_args()

    if args.command == "monitor":
        from tg_monitor_kit.config import load_config
        from tg_monitor_kit.lockfile import acquire_monitor_lock
        from tg_monitor_kit.monitoring import run_monitor

        cfg = load_config()
        acquire_monitor_lock(cfg.project_root)
        asyncio.run(run_monitor())
    elif args.command == "search":
        from tg_monitor_kit.search import run_search_daemon

        asyncio.run(run_search_daemon())
    elif args.command == "join":
        from tg_monitor_kit.config import load_config
        from tg_monitor_kit.join import run_join_daemon
        from tg_monitor_kit.lockfile import acquire_monitor_lock

        cfg = load_config()
        acquire_monitor_lock(cfg.project_root, "tg_join_from_list.lock")
        asyncio.run(run_join_daemon(once=args.once))
    elif args.command == "send-schedule":
        from tg_monitor_kit.send import run_send_daemon

        asyncio.run(run_send_daemon())
    elif args.command == "groups":
        from tg_monitor_kit.group_query import print_group_list, get_all_joined_groups
        # 强制刷新最新群列表
        groups = get_all_joined_groups(refresh=True)
        print_group_list(groups)
    elif args.command == "account-info":
        from tg_monitor_kit.tools.account_info import main as m

        m()
    elif args.command == "members":
        from tg_monitor_kit.tools.get_members import main as m

        m(args.group)
    elif args.command == "history":
        from tg_monitor_kit.tools.get_history import main as m

        m(args.group, args.limit)
    elif args.command == "auth":
        from tg_monitor_kit.auth import main as m

        m()
    elif args.command == "login":
        from tg_monitor_kit.login import main as m

        m()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
