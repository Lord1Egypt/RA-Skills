#!/usr/bin/env python3
"""向 Zopia Agent 异步发送消息。

用法:
    python send_message.py --base-id BASE_ID --episode-id EP_ID "生成一个赛博朋克风格的视频"
    python send_message.py --base-id BASE_ID --episode-id EP_ID --session-id SESS_ID "继续生成下一个镜头"

返回:
    {session_id, base_id, ...}

注意:
    此接口为异步模式，返回 session_id 后需使用 query_session.py 轮询结果。
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import build_project_url, print_json, send_message


def main() -> None:
    parser = argparse.ArgumentParser(description="向 Zopia Agent 异步发送消息")
    parser.add_argument("message", help="发送给 Agent 的消息内容")
    parser.add_argument("--base-id", required=True, help="项目 ID")
    parser.add_argument("--episode-id", required=True, help="剧集 ID")
    parser.add_argument("--session-id", default=None, help="会话 ID（可选，续接已有会话）")
    args = parser.parse_args()

    result = send_message(
        base_id=args.base_id,
        episode_id=args.episode_id,
        message=args.message,
        session_id=args.session_id,
    )
    sid = result.get("session_id", "")
    result["projectUrl"] = build_project_url(args.base_id, sid)
    print_json(result)


if __name__ == "__main__":
    main()
