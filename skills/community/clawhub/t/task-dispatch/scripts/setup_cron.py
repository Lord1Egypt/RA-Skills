#!/usr/bin/env python3
"""
Setup cron job for task dispatch.

Usage:
    python setup_cron.py --interval 300000 --channel feishu --to "chat_id"

This script outputs a JSON object that can be used with the OpenClaw cron tool.
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Setup task dispatch cron job")
    parser.add_argument(
        "--interval",
        type=int,
        default=300000,
        help="Interval in milliseconds (default: 300000 = 5 minutes)",
    )
    parser.add_argument(
        "--channel",
        type=str,
        default=None,
        help="Notification channel (feishu, telegram, etc.)",
    )
    parser.add_argument(
        "--to",
        type=str,
        default=None,
        help="Notification target (chat_id, user_id, etc.)",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="Task Dispatch",
        help="Cron job name",
    )
    parser.add_argument(
        "--message",
        type=str,
        default="执行 task-dispatch 调度检查。检查任务看板 API，筛选可派发任务，执行调度。无任务时返回 HEARTBEAT_OK。",
        help="Dispatch message",
    )

    args = parser.parse_args()

    cron_config = {
        "name": args.name,
        "schedule": {"kind": "every", "everyMs": args.interval},
        "payload": {"kind": "agentTurn", "message": args.message},
        "sessionTarget": "isolated",
    }

    if args.channel or args.to:
        cron_config["delivery"] = {}
        if args.channel:
            cron_config["delivery"]["channel"] = args.channel
        if args.to:
            cron_config["delivery"]["to"] = args.to
        cron_config["delivery"]["mode"] = "announce"

    print(json.dumps(cron_config, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()