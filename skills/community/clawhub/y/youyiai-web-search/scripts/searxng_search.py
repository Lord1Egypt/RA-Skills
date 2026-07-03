#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SearXNG 元搜索引擎联网搜索。

通过自建 SearXNG 实例聚合百度、Bing 等多个搜索引擎结果，
返回结构化的搜索结果（标题、链接、摘要、来源引擎）。

用法:
  python searxng_search.py "关键词"
  python searxng_search.py "关键词" --limit 8
  python searxng_search.py "关键词" --json
  python searxng_search.py "关键词" --engines baidu,bing
  python searxng_search.py "关键词" --endpoint http://localhost:8890
"""

import argparse
import json
import os
import re
import sys
from html import unescape
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen


DEFAULT_ENDPOINT = "http://175.24.233.186:8890"
DEFAULT_ENGINES = "baidu,bing"
DEFAULT_LANGUAGE = "zh-CN"
MAX_SUMMARY_CHARS = 300
MAX_TITLE_CHARS = 120
REQUEST_TIMEOUT = 30


class SearchError(Exception):
    pass


def normalize_space(value):
    text = unescape(str(value or ""))
    text = text.replace("\r", "\n").replace("\xa0", " ")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clamp_text(value, limit):
    text = normalize_space(value)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def get_endpoint():
    """获取 SearXNG 实例地址，优先使用环境变量。"""
    return (
        os.environ.get("SEARXNG_ENDPOINT", "").strip()
        or os.environ.get("HERMES_SEARXNG_URL", "").strip()
        or DEFAULT_ENDPOINT
    ).rstrip("/")


def build_search_url(endpoint, query, engines, language, pageno=1):
    params = {
        "q": query,
        "format": "json",
        "language": language,
        "pageno": pageno,
    }
    if engines:
        params["engines"] = engines
    return "{}/search?{}".format(endpoint, urlencode(params))


def fetch_search(endpoint, query, engines, language, limit, timeout):
    """请求 SearXNG JSON API 并返回结果列表。"""
    url = build_search_url(endpoint, query, engines, language)
    req = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Hermes-Desktop-SearXNG/1.0",
        },
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read(2 * 1024 * 1024)
            data = json.loads(raw.decode("utf-8", errors="replace"))
    except HTTPError as exc:
        raise SearchError("SearXNG HTTP {} {}".format(exc.code, exc.reason)) from exc
    except URLError as exc:
        raise SearchError("无法连接 SearXNG 实例 {}：{}".format(endpoint, exc.reason or exc)) from exc
    except TimeoutError as exc:
        raise SearchError("SearXNG 请求超时：{}".format(exc)) from exc
    except json.JSONDecodeError as exc:
        raise SearchError("SearXNG 返回非 JSON 响应：{}".format(exc)) from exc

    raw_results = data.get("results") or []
    unresponsive = data.get("unresponsive_engines") or []
    suggestions = data.get("suggestions") or []

    # 去重并格式化结果
    results = []
    seen_urls = set()
    for item in raw_results:
        url = (item.get("url") or "").strip()
        title = clamp_text(item.get("title") or "", MAX_TITLE_CHARS)
        if not title or not url:
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)
        content = clamp_text(item.get("content") or "", MAX_SUMMARY_CHARS)
        engine = item.get("engine") or ""
        results.append({
            "rank": len(results) + 1,
            "title": title,
            "url": url,
            "source": engine,
            "summary": content,
        })
        if len(results) >= limit:
            break

    return results, unresponsive, suggestions


def print_text_output(query, endpoint, engines, results, unresponsive, suggestions):
    if not results:
        print("SEARXNG_SEARCH_STATUS: EMPTY")
        print("QUERY: {}".format(query))
        print("ENDPOINT: {}".format(endpoint))
        if unresponsive:
            print("UNRESPONSIVE_ENGINES: {}".format(
                ", ".join("{} ({})".format(e[0], e[1]) for e in unresponsive)
            ))
        print("MESSAGE: SearXNG 没有返回搜索结果。可能搜索引擎暂时不可用，请换关键词或稍后重试。")
        if suggestions:
            print("SUGGESTIONS: {}".format("、".join(suggestions[:5])))
        return

    print("SEARXNG_SEARCH_STATUS: SUCCESS")
    print("QUERY: {}".format(query))
    print("ENDPOINT: {}".format(endpoint))
    print("ENGINES: {}".format(engines))
    print("RESULTS_COUNT: {}".format(len(results)))
    if unresponsive:
        print("UNRESPONSIVE_ENGINES: {}".format(
            ", ".join("{} ({})".format(e[0], e[1]) for e in unresponsive)
        ))
    print("RESULTS_JSON: {}".format(json.dumps(results, ensure_ascii=False)))
    print("RESULTS:")
    for item in results:
        print("{}. {} [{}]".format(item["rank"], item["title"], item["source"]))
        if item.get("url"):
            print("   链接: {}".format(item["url"]))
        if item.get("summary"):
            print("   摘要: {}".format(item["summary"]))
    if suggestions:
        print("SUGGESTIONS: {}".format("、".join(suggestions[:5])))


def parse_args(argv):
    parser = argparse.ArgumentParser(description="SearXNG 元搜索联网搜索")
    parser.add_argument("query", nargs="+", help="搜索关键词")
    parser.add_argument("--limit", type=int, default=8, help="结果数量，默认 8，最多 20")
    parser.add_argument("--timeout", type=int, default=REQUEST_TIMEOUT, help="请求超时秒数")
    parser.add_argument("--json", action="store_true", help="只输出 JSON")
    parser.add_argument("--engines", type=str, default=DEFAULT_ENGINES,
                        help="搜索引擎，逗号分隔，默认 baidu,bing")
    parser.add_argument("--language", type=str, default=DEFAULT_LANGUAGE,
                        help="搜索语言，默认 zh-CN")
    parser.add_argument("--endpoint", type=str, default="",
                        help="SearXNG 实例地址，默认使用环境变量或内置地址")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    query = normalize_space(" ".join(args.query))
    if not query:
        print("SEARXNG_SEARCH_STATUS: ERROR")
        print("ERROR: 请提供搜索关键词")
        return 1

    limit = max(1, min(args.limit, 20))
    timeout = max(5, min(args.timeout, 60))
    engines = args.engines.strip()
    language = args.language.strip()
    endpoint = args.endpoint.strip() or get_endpoint()

    try:
        results, unresponsive, suggestions = fetch_search(
            endpoint, query, engines, language, limit, timeout
        )
    except SearchError as exc:
        if args.json:
            print(json.dumps({"ok": False, "query": query, "error": str(exc)}, ensure_ascii=False))
        else:
            print("SEARXNG_SEARCH_STATUS: ERROR")
            print("QUERY: {}".format(query))
            print("ENDPOINT: {}".format(endpoint))
            print("ERROR: {}".format(exc))
        return 1

    if args.json:
        print(json.dumps({
            "ok": True,
            "query": query,
            "endpoint": endpoint,
            "engines": engines,
            "results": results,
            "unresponsive_engines": unresponsive,
            "suggestions": suggestions,
        }, ensure_ascii=False))
    else:
        print_text_output(query, endpoint, engines, results, unresponsive, suggestions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
