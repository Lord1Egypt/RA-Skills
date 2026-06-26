#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Search Script for Agent Skill
==================================

为深度研究代理系统提供网络搜索能力。

用法:
    python scripts/web_search.py "<query>"

支持的搜索后端 (通过 SEARCH_PROVIDER 环境变量配置):
    - duckduckgo  (默认，免费，无需 API Key)
    - tavily      (需设置 TAVILY_API_KEY)
    - bing        (需设置 BING_API_KEY)
    - google      (需设置 GOOGLE_API_KEY 和 GOOGLE_CSE_ID)
    - searxng     (需设置 SEARXNG_URL，默认 http://localhost:8080)

环境变量:
    SEARCH_PROVIDER   - 搜索引擎提供商 (默认: duckduckgo)
    SEARCH_MAX_RESULTS - 最大返回结果数 (默认: 10)
    TAVILY_API_KEY    - Tavily API 密钥
    BING_API_KEY      - Bing Search API 密钥
    GOOGLE_API_KEY    - Google Custom Search API 密钥
    GOOGLE_CSE_ID     - Google 自定义搜索引擎 ID
    SEARXNG_URL       - SearXNG 实例地址
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


# ──────────────────────────────────────────────
# 配置
# ──────────────────────────────────────────────

SEARCH_PROVIDER = os.environ.get("SEARCH_PROVIDER", "duckduckgo").lower().strip()
MAX_RESULTS = int(os.environ.get("SEARCH_MAX_RESULTS", "10"))
REQUEST_TIMEOUT = int(os.environ.get("SEARCH_TIMEOUT", "30"))

# User-Agent for HTTP requests
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


# ──────────────────────────────────────────────
# 搜索结果数据结构
# ──────────────────────────────────────────────

class SearchResult:
    """单条搜索结果"""

    def __init__(self, title: str, url: str, snippet: str):
        self.title = title.strip() if title else ""
        self.url = url.strip() if url else ""
        self.snippet = snippet.strip() if snippet else ""

    def to_dict(self) -> dict:
        return {"title": self.title, "url": self.url, "snippet": self.snippet}

    def __str__(self) -> str:
        parts = []
        if self.title:
            parts.append(f"**{self.title}**")
        if self.url:
            parts.append(f"URL: {self.url}")
        if self.snippet:
            parts.append(self.snippet)
        return "\n".join(parts)


# ──────────────────────────────────────────────
# 网络连通性测试
# ──────────────────────────────────────────────

NETWORK_TEST_URLS = [
    #"https://redteampubtest/realtime_i/default",
    "https://duckduckgo.com",
]


def test_network(timeout: int = 5) -> bool:
    """
    测试网络是否连通。
    
    依次尝试访问多个知名站点，任一成功即视为网络可用。
    
    Args:
        timeout: 每个站点的超时时间（秒）
    
    Returns:
        True 表示网络连通，False 表示不可用
    """
    for url in NETWORK_TEST_URLS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            continue
    return False


# ──────────────────────────────────────────────
# HTTP 工具函数
# ──────────────────────────────────────────────

def http_get(url: str, headers: dict | None = None, timeout: int = REQUEST_TIMEOUT) -> dict | str:
    """发送 HTTP GET 请求并返回响应内容"""
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read().decode("utf-8", errors="replace")
    try:
        return json.loads(data)
    except (json.JSONDecodeError, ValueError):
        return data


def http_post_json(url: str, payload: dict, headers: dict | None = None, timeout: int = REQUEST_TIMEOUT) -> dict:
    """发送 HTTP POST JSON 请求并返回 JSON 响应"""
    req_headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
    }
    if headers:
        req_headers.update(headers)
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=req_headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


# ──────────────────────────────────────────────
# 搜索后端实现
# ──────────────────────────────────────────────

def search_duckduckgo(query: str, max_results: int = MAX_RESULTS) -> list[SearchResult]:
    """
    使用 DuckDuckGo 进行搜索。
    
    优先使用 duckduckgo_search 库（如果已安装），
    否则回退到 DuckDuckGo HTML 解析方式。
    """
    # 尝试使用 duckduckgo_search 库
    try:
        from duckduckgo_search import DDGS

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(SearchResult(
                    title=r.get("title", ""),
                    url=r.get("href", r.get("link", "")),
                    snippet=r.get("body", r.get("snippet", "")),
                ))
        return results
    except ImportError:
        pass

    # 回退方案：使用 DuckDuckGo Lite HTML 版本
    return _search_duckduckgo_lite(query, max_results)


def _search_duckduckgo_lite(query: str, max_results: int) -> list[SearchResult]:
    """通过 DuckDuckGo Lite HTML 页面抓取搜索结果"""
    import html
    import re

    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"
    
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html",
    })

    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        page = resp.read().decode("utf-8", errors="replace")

    results = []

    # 解析搜索结果链接和标题
    link_pattern = re.compile(
        r'<a[^>]+rel="nofollow"[^>]+href="([^"]+)"[^>]*>\s*(.+?)\s*</a>',
        re.DOTALL | re.IGNORECASE,
    )
    # 解析摘要
    snippet_pattern = re.compile(
        r'<td[^>]*class="result-snippet"[^>]*>\s*(.+?)\s*</td>',
        re.DOTALL | re.IGNORECASE,
    )

    links = link_pattern.findall(page)
    snippets = snippet_pattern.findall(page)

    for i, (link_url, title_html) in enumerate(links):
        if i >= max_results:
            break
        title = html.unescape(re.sub(r"<[^>]+>", "", title_html)).strip()
        snippet = ""
        if i < len(snippets):
            snippet = html.unescape(re.sub(r"<[^>]+>", "", snippets[i])).strip()

        if link_url and not link_url.startswith("https://duckduckgo.com"):
            results.append(SearchResult(title=title, url=link_url, snippet=snippet))

    return results


def search_tavily(query: str, max_results: int = MAX_RESULTS) -> list[SearchResult]:
    """使用 Tavily API 进行搜索"""
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if not api_key:
        raise EnvironmentError("缺少环境变量 TAVILY_API_KEY，请设置后重试。")

    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": max_results,
        "include_answer": False,
    }

    data = http_post_json("https://api.tavily.com/search", payload)

    results = []
    for r in data.get("results", []):
        results.append(SearchResult(
            title=r.get("title", ""),
            url=r.get("url", ""),
            snippet=r.get("content", ""),
        ))
    return results


def search_bing(query: str, max_results: int = MAX_RESULTS) -> list[SearchResult]:
    """使用 Bing Web Search API 进行搜索"""
    api_key = os.environ.get("BING_API_KEY", "")
    if not api_key:
        raise EnvironmentError("缺少环境变量 BING_API_KEY，请设置后重试。")

    encoded_query = urllib.parse.quote_plus(query)
    url = (
        f"https://api.bing.microsoft.com/v7.0/search"
        f"?q={encoded_query}&count={max_results}&mkt=zh-CN"
    )

    data = http_get(url, headers={"Ocp-Apim-Subscription-Key": api_key})

    results = []
    if isinstance(data, dict):
        for r in data.get("webPages", {}).get("value", []):
            results.append(SearchResult(
                title=r.get("name", ""),
                url=r.get("url", ""),
                snippet=r.get("snippet", ""),
            ))
    return results


def search_google(query: str, max_results: int = MAX_RESULTS) -> list[SearchResult]:
    """使用 Google Custom Search API 进行搜索"""
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    cse_id = os.environ.get("GOOGLE_CSE_ID", "")
    if not api_key or not cse_id:
        raise EnvironmentError(
            "缺少环境变量 GOOGLE_API_KEY 或 GOOGLE_CSE_ID，请设置后重试。"
        )

    results = []
    # Google CSE 每次最多返回 10 条，需要分页
    for start in range(1, max_results + 1, 10):
        num = min(10, max_results - start + 1)
        encoded_query = urllib.parse.quote_plus(query)
        url = (
            f"https://www.googleapis.com/customsearch/v1"
            f"?key={api_key}&cx={cse_id}&q={encoded_query}"
            f"&start={start}&num={num}"
        )
        data = http_get(url)
        if isinstance(data, dict):
            for r in data.get("items", []):
                results.append(SearchResult(
                    title=r.get("title", ""),
                    url=r.get("link", ""),
                    snippet=r.get("snippet", ""),
                ))
    return results[:max_results]


def search_searxng(query: str, max_results: int = MAX_RESULTS) -> list[SearchResult]:
    """使用 SearXNG 实例进行搜索"""
    base_url = os.environ.get("SEARXNG_URL", "http://localhost:8080").rstrip("/")

    encoded_query = urllib.parse.quote_plus(query)
    url = f"{base_url}/search?q={encoded_query}&format=json&pageno=1"

    data = http_get(url)

    results = []
    if isinstance(data, dict):
        for r in data.get("results", [])[:max_results]:
            results.append(SearchResult(
                title=r.get("title", ""),
                url=r.get("url", ""),
                snippet=r.get("content", ""),
            ))
    return results


# ──────────────────────────────────────────────
# 搜索调度器
# ──────────────────────────────────────────────

PROVIDERS: dict[str, Any] = {
    "duckduckgo": search_duckduckgo,
    "ddg": search_duckduckgo,
    "tavily": search_tavily,
    "bing": search_bing,
    "google": search_google,
    "searxng": search_searxng,
}


def search(query: str, provider: str = SEARCH_PROVIDER, max_results: int = MAX_RESULTS) -> list[SearchResult]:
    """
    执行网络搜索。
    
    Args:
        query:       搜索查询文本
        provider:    搜索引擎提供商名称
        max_results: 最大返回结果数
    
    Returns:
        SearchResult 列表
    """
    search_fn = PROVIDERS.get(provider)
    if search_fn is None:
        supported = ", ".join(sorted(set(PROVIDERS.keys())))
        raise ValueError(
            f"不支持的搜索引擎: '{provider}'。支持的引擎: {supported}"
        )
    return search_fn(query, max_results)


# ──────────────────────────────────────────────
# 输出格式化
# ──────────────────────────────────────────────

def format_results_text(results: list[SearchResult], query: str) -> str:
    """将搜索结果格式化为纯文本（供 LLM 消费）"""
    if not results:
        return f"搜索 \"{query}\" 未找到任何结果。"

    lines = [f"搜索 \"{query}\" 找到 {len(results)} 条结果：\n"]
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r.title}")
        if r.url:
            lines.append(f"    链接: {r.url}")
        if r.snippet:
            lines.append(f"    摘要: {r.snippet}")
        lines.append("")
    return "\n".join(lines)


def format_results_json(results: list[SearchResult], query: str) -> str:
    """将搜索结果格式化为 JSON"""
    output = {
        "query": query,
        "count": len(results),
        "results": [r.to_dict() for r in results],
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


# ──────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────

def print_usage():
    """打印使用说明"""
    print(
        "用法: python web_search.py <query> [--json] [--provider <name>] [--max <n>]\n"
        "\n"
        "参数:\n"
        "  query                要搜索的内容\n"
        "  --json               以 JSON 格式输出结果\n"
        "  --provider <name>    搜索引擎 (duckduckgo/tavily/bing/google/searxng)\n"
        "  --max <n>            最大结果数 (默认: 10)\n"
        "\n"
        "环境变量:\n"
        "  SEARCH_PROVIDER      默认搜索引擎 (默认: duckduckgo)\n"
        "  SEARCH_MAX_RESULTS   默认最大结果数 (默认: 10)\n"
        "  TAVILY_API_KEY       Tavily API 密钥\n"
        "  BING_API_KEY         Bing Search API 密钥\n"
        "  GOOGLE_API_KEY       Google API 密钥\n"
        "  GOOGLE_CSE_ID        Google 自定义搜索引擎 ID\n"
        "  SEARXNG_URL          SearXNG 实例地址\n",
        file=sys.stderr,
    )


def parse_args(argv: list[str]) -> dict:
    """解析命令行参数"""
    args = {
        "query": "",
        "json_output": False,
        "provider": SEARCH_PROVIDER,
        "max_results": MAX_RESULTS,
    }

    positional = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--json":
            args["json_output"] = True
        elif arg == "--provider" and i + 1 < len(argv):
            i += 1
            args["provider"] = argv[i].lower().strip()
        elif arg == "--max" and i + 1 < len(argv):
            i += 1
            try:
                args["max_results"] = int(argv[i])
            except ValueError:
                print(f"警告: 无效的 --max 值 '{argv[i]}'，使用默认值 {MAX_RESULTS}", file=sys.stderr)
        elif arg in ("--help", "-h"):
            print_usage()
            sys.exit(0)
        elif not arg.startswith("--"):
            positional.append(arg)
        i += 1

    if positional:
        args["query"] = " ".join(positional)

    return args


def main():
    # 网络连通性检查
    if not test_network():
        print("错误: 网络不可用，请检查网络连接后重试。", file=sys.stderr)
    args = parse_args(sys.argv[1:])
    query = args["query"]

    if not query:
        print("错误: 请提供搜索查询内容。", file=sys.stderr)
        print_usage()
        sys.exit(1)

    try:
        results = search(
            query=query,
            provider=args["provider"],
            max_results=args["max_results"],
        )
    except EnvironmentError as e:
        print(f"配置错误: {e}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"网络错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"搜索失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if args["json_output"]:
        print(format_results_json(results, query))
    else:
        print(format_results_text(results, query))


if __name__ == "__main__":
    main()
