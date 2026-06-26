#!/usr/bin/env python3
"""
Twitter 接口调用脚本
- detail: POST /twitter/fetch_tweet_detail
- search: POST /twitter/fetch_search_timeline
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional
from urllib import error, request

API_BASE = "https://coze-js-api.devtool.uk"
DETAIL_URL = f"{API_BASE}/twitter/fetch_tweet_detail"
SEARCH_URL = f"{API_BASE}/twitter/fetch_search_timeline"


def get_api_key(arg_key: Optional[str]) -> str:
    key = (arg_key or os.environ.get("AZT_API_KEY", "")).strip()
    return key


def post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"请求失败：{exc.reason}") from exc


def pick_first(value: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    for key in keys:
        if key in value and value[key] not in (None, ""):
            return value[key]
    return default


def normalize_detail(data: Any) -> Dict[str, Any]:
    if isinstance(data, dict):
        tweet = data.get("tweet") if isinstance(data.get("tweet"), dict) else data
        user = tweet.get("user") if isinstance(tweet.get("user"), dict) else {}
        return {
            "tweet_id": pick_first(tweet, ["tweet_id", "id", "rest_id"]),
            "text": pick_first(tweet, ["full_text", "text", "content", "tweet_text"]),
            "author": pick_first(user, ["name", "screen_name", "username"], pick_first(tweet, ["author", "screen_name"])),
            "created_at": pick_first(tweet, ["created_at", "time", "publish_time"]),
            "like_count": pick_first(tweet, ["favorite_count", "like_count", "likes"]),
            "retweet_count": pick_first(tweet, ["retweet_count", "repost_count", "shares"]),
            "reply_count": pick_first(tweet, ["reply_count", "comment_count", "comments"]),
            "raw": data,
        }
    return {"raw": data}


def normalize_search(data: Any) -> List[Dict[str, Any]]:
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = pick_first(data, ["tweets", "items", "list", "statuses", "result", "data"], [])
        if not isinstance(items, list):
            items = []
    else:
        items = []

    normalized: List[Dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        user = item.get("user") if isinstance(item.get("user"), dict) else {}
        normalized.append({
            "tweet_id": pick_first(item, ["tweet_id", "id", "rest_id"]),
            "text": pick_first(item, ["full_text", "text", "content", "tweet_text"]),
            "author": pick_first(user, ["name", "screen_name", "username"], pick_first(item, ["author", "screen_name"])),
            "created_at": pick_first(item, ["created_at", "time", "publish_time"]),
            "link": pick_first(item, ["url", "link", "tweet_url"]),
            "raw": item,
        })
    return normalized


def print_detail_result(result: Dict[str, Any]) -> None:
    code = result.get("code")
    msg = result.get("msg", "")

    if code != 200:
        print(f"❌ 接口返回错误（code={code}）：{msg}")
        sys.exit(1)

    data = result.get("data", {})
    normalized = normalize_detail(data)

    print(f"✅ 请求成功  {msg}")
    print("-" * 60)
    print(f"推文ID：{normalized.get('tweet_id') or '—'}")
    print(f"作者：{normalized.get('author') or '—'}")
    print(f"发布时间：{normalized.get('created_at') or '—'}")
    print(f"点赞：{normalized.get('like_count') or '—'}")
    print(f"转发：{normalized.get('retweet_count') or '—'}")
    print(f"回复：{normalized.get('reply_count') or '—'}")
    print(f"正文：{normalized.get('text') or '—'}")
    print("-" * 60)


def print_search_result(result: Dict[str, Any]) -> None:
    code = result.get("code")
    msg = result.get("msg", "")

    if code != 200:
        print(f"❌ 接口返回错误（code={code}）：{msg}")
        sys.exit(1)

    entries = normalize_search(result.get("data", {}))

    print(f"✅ 请求成功  {msg}")
    print("-" * 60)

    if not entries:
        print("暂无数据，原始响应：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    for idx, item in enumerate(entries, start=1):
        author = item.get("author") or "—"
        created_at = item.get("created_at") or "—"
        text = item.get("text") or "—"
        link = item.get("link") or "—"
        print(f"{idx:>3}. {author} | {created_at}")
        print(f"     {text}")
        print(f"     {link}")
        print()

    print("-" * 60)
    print(f"共 {len(entries)} 条数据")


def run_detail(tweet_id: str, api_key: str, output_json: bool) -> None:
    payload: Dict[str, Any] = {"tweet_id": tweet_id}
    if api_key:
        payload["api_key"] = api_key

    result = post_json(DETAIL_URL, payload)
    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_detail_result(result)


def run_search(keyword: str, search_type: str, cursor: str, api_key: str, output_json: bool) -> None:
    payload: Dict[str, Any] = {"keyword": keyword, "search_type": search_type}
    if cursor:
        payload["cursor"] = cursor
    if api_key:
        payload["api_key"] = api_key

    result = post_json(SEARCH_URL, payload)
    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_search_result(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="调用 Twitter 推文详情和搜索时间线接口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--azt_api_key", default=None, help="API Key（也可通过环境变量 AZT_API_KEY 设置）")
    parser.add_argument("--json", action="store_true", dest="output_json", help="以 JSON 格式输出原始响应")

    subparsers = parser.add_subparsers(dest="mode", required=True)

    detail_parser = subparsers.add_parser("detail", help="获取单条推文详情")
    detail_parser.add_argument("--tweet_id", required=True, help="推文 ID")

    search_parser = subparsers.add_parser("search", help="搜索 Twitter 时间线")
    search_parser.add_argument("--keyword", required=True, help="搜索关键词")
    search_parser.add_argument("--search_type", default="Top", help="搜索类型，默认 Top")
    search_parser.add_argument("--cursor", default="", help="翻页游标，可选")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    api_key = get_api_key(args.azt_api_key)

    if args.mode == "detail":
        print(f"📡 请求接口：{DETAIL_URL}")
        print(f"   参数：tweet_id={args.tweet_id}")
        run_detail(args.tweet_id, api_key, args.output_json)
    elif args.mode == "search":
        print(f"📡 请求接口：{SEARCH_URL}")
        print(f"   参数：keyword={args.keyword}, search_type={args.search_type}", end="")
        if args.cursor:
            print(f", cursor={args.cursor}", end="")
        print()
        run_search(args.keyword, args.search_type, args.cursor, api_key, args.output_json)


if __name__ == "__main__":
    main()
