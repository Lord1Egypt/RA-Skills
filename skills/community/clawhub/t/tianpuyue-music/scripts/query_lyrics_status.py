# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json

from common import log_params, query_lyrics_task, setup_logging

setup_logging()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="查询天谱乐歌词任务状态")
    parser.add_argument("--item-id", required=True, help="作品 ID")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    log_params("查询歌词状态", item_id=args.item_id)
    item = query_lyrics_task(args.item_id)
    log_params("查询歌词状态完成", item_id=args.item_id)
    print(json.dumps(item, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
