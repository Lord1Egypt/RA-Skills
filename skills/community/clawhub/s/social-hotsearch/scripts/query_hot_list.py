#!/usr/bin/env python3
"""Query a platform's hot-search list.

Calls social-base MCP tool `query_rank_list` through the proxy.

Usage:
    python3 query_hot_list.py --source 微博
    python3 query_hot_list.py --source 抖音 --keyword 国货 --size 20
    python3 query_hot_list.py --source 知乎 --date 2026-05-14
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from social_client import (
    QuotaExhausted,
    ProxyError,
    call_tool,
    extract_text_content,
    print_quota_help,
)


SUPPORTED_SOURCES = ["微博", "抖音", "知乎", "百度"]


def main() -> int:
    p = argparse.ArgumentParser(description="查询平台热搜榜")
    p.add_argument("--source", required=True, choices=SUPPORTED_SOURCES,
                   help="平台名称")
    p.add_argument("--keyword", default=None,
                   help="可选,过滤包含该关键词的话题")
    p.add_argument("--size", type=int, default=50,
                   help="返回数量,默认 50,最多 100")
    p.add_argument("--date", default=None,
                   help="日期,格式 YYYY-MM-DD,默认今天")
    args = p.parse_args()

    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        d = datetime.now().date()
    start = datetime.combine(d, time(0, 0, 0)).strftime("%Y-%m-%d %H:%M:%S")
    end = datetime.combine(d, time(23, 59, 59)).strftime("%Y-%m-%d %H:%M:%S")

    arguments = {
        "source": args.source,
        "start_time": start,
        "end_time": end,
        "size": min(max(args.size, 1), 100),
    }
    if args.keyword:
        arguments["keyword"] = args.keyword

    try:
        result = call_tool("query_rank_list", arguments)
    except QuotaExhausted as e:
        print_quota_help(e.info)
        return 3
    except ProxyError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2

    text = extract_text_content(result)
    items = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    print(json.dumps({
        "source": args.source,
        "date": d.isoformat(),
        "count": len(items),
        "items": items,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
