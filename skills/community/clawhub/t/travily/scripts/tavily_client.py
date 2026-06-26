#!/usr/bin/env python3
"""
Tavily Search API - 从 .env 加载配置
"""
import os
import sys
from pathlib import Path

# 尝试从 .env 加载
ENV_FILE = Path(__file__).parent.parent / ".env"
if ENV_FILE.exists():
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

# 现在导入并使用
from tavily import TavilyClient

import argparse
import json

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")


def search(query: str, max_results: int = 10, search_depth: str = "advanced",
           time_range: str = None, include_domains: list = None,
           exclude_domains: list = None, include_raw_content: bool = False) -> dict:
    """执行搜索"""
    if not TAVILY_API_KEY:
        print("错误: 请在 .env 文件中设置 TAVILY_API_KEY")
        sys.exit(1)

    client = TavilyClient(api_key=TAVILY_API_KEY)
    kwargs = {"query": query, "max_results": max_results, "search_depth": search_depth}
    if time_range:
        kwargs["time_range"] = time_range
    if include_domains:
        kwargs["include_domains"] = include_domains
    if exclude_domains:
        kwargs["exclude_domains"] = exclude_domains
    if include_raw_content:
        kwargs["include_raw_content"] = True

    try:
        return client.search(**kwargs)
    except Exception as e:
        print(f"搜索出错: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Tavily Search')
    parser.add_argument('query', nargs='?', help='搜索内容')
    parser.add_argument('--max-results', '-n', type=int, default=10)
    parser.add_argument('--search-depth', '-d', choices=['ultra-fast', 'fast', 'basic', 'advanced'], default='advanced')
    parser.add_argument('--time-range', '-t', choices=['day', 'week', 'month', 'year'])
    parser.add_argument('--include-domains', '-i', nargs='+')
    parser.add_argument('--exclude-domains', '-e', nargs='+')
    parser.add_argument('--raw-content', '-r', action='store_true')
    parser.add_argument('--json', '-j', action='store_true')

    args = parser.parse_args()
    if not args.query:
        parser.print_help()
        sys.exit(1)

    results = search(args.query, args.max_results, args.search_depth, args.time_range,
                    args.include_domains, args.exclude_domains, args.raw_content)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"\n搜索结果: {args.query}")
        print(f"找到 {len(results.get('results', []))} 个结果\n")
        print("-" * 60)
        for i, r in enumerate(results.get('results', []), 1):
            print(f"\n[{i}] {r.get('title', '无标题')}")
            print(f"    链接: {r.get('url', 'N/A')}")
            print(f"    相关度: {r.get('score', 'N/A')}")
            content = r.get('content', '')
            if content:
                print(f"    内容: {content[:200]}...")
        print(f"\n响应时间: {results.get('response_time', 'N/A')}s")


if __name__ == '__main__':
    main()
