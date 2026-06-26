#!/usr/bin/env python3
"""触发并查询 Zopia episode 视频合成渲染。

用法:
    # 触发渲染（异步，立即返回 render_id）
    python render_episode.py trigger --base-id BASE_ID --episode-id EPISODE_ID

    # 触发渲染并添加水印
    python render_episode.py trigger --base-id BASE_ID --episode-id EPISODE_ID --watermark

    # 查询最新渲染状态
    python render_episode.py status --base-id BASE_ID --episode-id EPISODE_ID

    # 查询指定渲染状态
    python render_episode.py status --base-id BASE_ID --episode-id EPISODE_ID --render-id RENDER_ID

    # 自动轮询直到渲染完成
    python render_episode.py status --base-id BASE_ID --episode-id EPISODE_ID --render-id RENDER_ID --poll

返回结构:
    trigger: {"render_id": "...", "status": "processing"}
    status:  {"status": "not_started" | "processing" | "completed" | "failed",
              "render_id": "...", "progress": 0.0~1.0, "video_url": "..."}
"""

from __future__ import annotations

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from _common import get_render_status, print_json, trigger_render

POLL_INTERVAL = 8    # 秒
POLL_TIMEOUT = 600   # 最长轮询时间（秒），渲染比 Agent 慢，给 10 分钟


def main() -> None:
    parser = argparse.ArgumentParser(description="Zopia episode 视频渲染")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # trigger
    t = subparsers.add_parser("trigger", help="触发渲染（异步）")
    t.add_argument("--base-id", required=True, help="项目 ID")
    t.add_argument("--episode-id", required=True, help="剧集 ID")
    t.add_argument("--watermark", action="store_true", help="添加水印（默认不加）")

    # status
    s = subparsers.add_parser("status", help="查询渲染状态")
    s.add_argument("--base-id", required=True, help="项目 ID")
    s.add_argument("--episode-id", required=True, help="剧集 ID")
    s.add_argument("--render-id", default=None, help="渲染 ID（省略则查最新）")
    s.add_argument("--poll", action="store_true", help="自动轮询直到完成")

    args = parser.parse_args()

    if args.action == "trigger":
        result = trigger_render(args.base_id, args.episode_id, args.watermark)
        print_json(result)
        return

    # status
    if not args.poll:
        result = get_render_status(args.base_id, args.episode_id, args.render_id)
        print_json(result)
        return

    # 自动轮询模式
    render_id = args.render_id
    start_time = time.time()

    while True:
        if time.time() - start_time > POLL_TIMEOUT:
            print(f"渲染轮询超时（{POLL_TIMEOUT}秒）", file=sys.stderr)
            sys.exit(1)

        result = get_render_status(args.base_id, args.episode_id, render_id)
        print_json(result)

        status = result.get("status", "")

        # 补全 render_id（首次查到后固定住）
        if not render_id and result.get("render_id"):
            render_id = result["render_id"]

        if status == "completed":
            break
        if status == "failed":
            print("渲染失败", file=sys.stderr)
            sys.exit(1)
        if status == "not_started":
            print("尚未触发渲染，请先执行 trigger", file=sys.stderr)
            sys.exit(1)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
