#!/usr/bin/env python3
"""Sample representative posts about a topic.

Calls social-base MCP tool `query_raw_posts` through the proxy.

Usage:
    python3 sample_posts.py --topic '瑞幸' --size 20
    python3 sample_posts.py --topic '夏日防晒' --datasource 小红书 --order 互动数 --size 30
    python3 sample_posts.py --topic '618' --search-fields title content video_asr video_ocr
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from social_client import (
    QuotaExhausted,
    ProxyError,
    call_tool,
    extract_text_content,
    normalize_analysis_datasource,
    print_quota_help,
)


SEARCH_FIELD_CHOICES = ["title", "content", "video_asr", "video_ocr", "screenshot"]


def main() -> int:
    p = argparse.ArgumentParser(description="按话题采样原帖")
    p.add_argument("--topic", required=True, help="话题关键词")
    p.add_argument("--days", type=int, default=3, help="时间窗口,天,默认 3")
    p.add_argument("--datasource", nargs="+",
                   default=["微博", "小红书", "短视频"],
                   help="数据源平台列表。可选: 小红书 / 微博 / 短视频 / 视频 / 微信 / 电商 / 博客 / 问答 / 新闻 / 论坛。"
                        "默认 微博+小红书+短视频(覆盖营销/PR 场景三大主力)。"
                        "注意: 用户口中的'抖音'/'快手'在此处归一化为'短视频','B站/哔哩哔哩'归一化为'视频','公众号'归一化为'微信'。")
    p.add_argument("--search-fields", nargs="+", default=["title", "content"],
                   choices=SEARCH_FIELD_CHOICES,
                   help="关键词搜索范围,默认 title+content。"
                        "短视频内容场景建议加 video_asr(语音)video_ocr(画面字幕);"
                        "图文内容场景可加 screenshot(图片 OCR)。")
    p.add_argument("--size", type=int, default=20,
                   help="采样数量,默认 20,最多 100")
    p.add_argument("--order", default="综合",
                   choices=["综合", "发布时间", "互动数", "阅读数", "曝光量"],
                   help="排序方式")
    args = p.parse_args()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=args.days)
    start = start_date.replace(hour=0, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
    end = end_date.strftime("%Y-%m-%d %H:%M:%S")

    datasource = normalize_analysis_datasource(args.datasource)

    arguments = {
        "target_type": "keyword",
        "name": args.topic,
        "anys": [[args.topic]],
        "start_time": start,
        "end_time": end,
        "datasource": datasource,
        "search_fields": args.search_fields,
        "size": min(max(args.size, 1), 100),
        "order_by": args.order,
    }

    try:
        result = call_tool("query_raw_posts", arguments)
    except QuotaExhausted as e:
        print_quota_help(e.info)
        return 3
    except ProxyError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2

    text = extract_text_content(result)
    posts: list = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, list):
            posts.extend(obj)
        else:
            posts.append(obj)

    if not posts:
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                posts = parsed
            elif isinstance(parsed, dict) and "data" in parsed:
                posts = parsed["data"]
        except json.JSONDecodeError:
            pass

    print(json.dumps({
        "topic": args.topic,
        "window": {
            "start": start,
            "end": end,
            "datasource": datasource,
            "search_fields": args.search_fields,
        },
        "count": len(posts),
        "posts": posts,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
