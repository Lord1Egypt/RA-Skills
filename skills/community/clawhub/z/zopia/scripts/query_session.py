#!/usr/bin/env python3
"""轮询 Zopia 会话结果。

用法:
    # 查询完整结果
    python query_session.py SESSION_ID

    # 增量查询（仅获取 seq > 5 的新消息）
    python query_session.py SESSION_ID --after-seq 5

    # 自动轮询直到完成
    python query_session.py SESSION_ID --poll

返回结构化结果:
    {
      "status": "completed" | "running" | "idle",
      "messages": [...],
      "workspace": {
        "entities": [...],
        "storyboard": {...}
      }
    }
"""

from __future__ import annotations

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from _common import print_json, query_session

# 轮询参数
POLL_INTERVAL = 8       # 秒
POLL_TIMEOUT = 180      # 最长轮询时间（秒）
MAX_CONSECUTIVE_FAIL = 3


def main() -> None:
    parser = argparse.ArgumentParser(description="轮询 Zopia 会话结果")
    parser.add_argument("session_id", help="会话 ID")
    parser.add_argument("--after-seq", type=int, default=0,
                        help="仅获取 seq 大于此值的消息")
    parser.add_argument("--poll", action="store_true",
                        help="自动轮询直到会话完成")
    args = parser.parse_args()

    if not args.poll:
        result = query_session(args.session_id, args.after_seq)
        print_json(result)
        return

    # 自动轮询模式
    after_seq = args.after_seq
    start_time = time.time()
    consecutive_fails = 0

    while True:
        elapsed = time.time() - start_time
        if elapsed > POLL_TIMEOUT:
            print(f"轮询超时（{POLL_TIMEOUT}秒）", file=sys.stderr)
            sys.exit(1)

        try:
            result = query_session(args.session_id, after_seq)
            consecutive_fails = 0
        except SystemExit:
            consecutive_fails += 1
            if consecutive_fails >= MAX_CONSECUTIVE_FAIL:
                print(f"连续失败 {MAX_CONSECUTIVE_FAIL} 次，停止轮询", file=sys.stderr)
                sys.exit(1)
            time.sleep(POLL_INTERVAL)
            continue

        status = result.get("status", "")
        messages = result.get("messages", [])

        # 更新增量游标
        if messages:
            max_seq = max(m.get("seq", 0) for m in messages)
            if max_seq > after_seq:
                after_seq = max_seq

        # 输出当前状态
        print_json(result)

        if status in ("completed", "idle", "error"):
            break

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
