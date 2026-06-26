#!/usr/bin/env python3
"""管理 Zopia 项目的剧集。

用法:
    # 列出剧集
    python manage_episodes.py list --base-id BASE_ID

    # 创建新剧集
    python manage_episodes.py create --base-id BASE_ID

    # 删除剧集
    python manage_episodes.py delete --episode-id EPISODE_ID
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import create_episode, delete_episode, list_episodes, print_json


def main() -> None:
    parser = argparse.ArgumentParser(description="管理 Zopia 项目的剧集")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # list
    list_parser = subparsers.add_parser("list", help="列出剧集")
    list_parser.add_argument("--base-id", required=True, help="项目 ID")

    # create
    create_parser = subparsers.add_parser("create", help="创建新剧集")
    create_parser.add_argument("--base-id", required=True, help="项目 ID")

    # delete
    delete_parser = subparsers.add_parser("delete", help="删除剧集")
    delete_parser.add_argument("--episode-id", required=True, help="剧集 ID")

    args = parser.parse_args()

    if args.action == "list":
        result = list_episodes(args.base_id)
        print_json(result)
    elif args.action == "create":
        result = create_episode(args.base_id)
        print_json(result)
    elif args.action == "delete":
        result = delete_episode(args.episode_id)
        print_json(result)


if __name__ == "__main__":
    main()
