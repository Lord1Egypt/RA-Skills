#!/usr/bin/env python3
"""
store-hopper: 多平台攻略搜索脚本
用法: python3 search.py <城市> [--type 美食] [--tags 人均100] [--max-results 10]
输出: JSON 格式的搜索结果列表

搜索引擎优先级:
  1. DDGS（deedy5/ddgs，多引擎聚合，质量最高，无需API Key）
  2. Bing 网页抓取
  3. 百度网页抓取

依赖安装:
  pip install ddgs requests beautifulsoup4 lxml
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup


def summary(msg: str):
    """输出一行关键摘要到 stderr"""
    sys.stderr.write(f"[搜索] {msg}\n")
    sys.stderr.flush()


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def build_queries(city: str, category: str, tags: str, year: int) -> list[dict]:
    """构建多平台搜索关键词"""
    queries = [
        {"label": "综合攻略", "q": f"{city} {category}攻略 必吃必玩 推荐 {year}"},
        {"label": "排行热门", "q": f"{city} {category} 排行 热门 推荐 {year}"},
        {"label": "本地推荐", "q": f"{city} {category} 本地人推荐 值得去 {year}"},
        {"label": "探店", "q": f"{city} {category} 探店 打卡 推荐 {year}"},
    ]
    if tags:
        queries.append({"label": "标签补充", "q": f"{city} {tags} 推荐 {year}"})
    return queries


# ───────────────── 搜索引擎实现 ─────────────────


# 检查 ddgs 是否可用（核心依赖）
try:
    from ddgs import DDGS
except ImportError:
    print(
        json.dumps(
            {
                "error": "缺少必需依赖 ddgs，请先安装: pip install ddgs",
                "install_command": "pip install ddgs",
            },
            ensure_ascii=False,
        )
    )
    summary("错误: 缺少 ddgs 依赖，请执行 pip install ddgs")
    sys.exit(1)


def search_ddgs(query: str, max_results: int = 5, backend: str = "google") -> list[dict]:
    """
    DDGS 多引擎聚合搜索（首选，质量最高）
    使用 deedy5/ddgs 库。

    backend 优先级: google > bing（auto 在部分网络环境下会卡死，不推荐）
    内置 8 秒超时保护，避免卡死整个脚本。
    """
    import signal

    results = []

    def _timeout_handler(signum, frame):
        raise TimeoutError("DDGS search timed out")

    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(8)  # 8 秒硬超时
    try:
        ddgs = DDGS(timeout=6)
        search_results = ddgs.text(
            query,
            region="cn-zh",
            safesearch="moderate",
            timelimit="y",
            max_results=max_results,
            backend=backend,
        )

        for r in search_results:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", r.get("link", "")),
                "snippet": r.get("body", r.get("snippet", ""))[:300],
                "source": f"ddgs:{backend}",
            })
    except Exception:
        pass
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

    return results


def search_bing(query: str, max_results: int = 5) -> list[dict]:
    """Bing 搜索（备选，国内稳定可用）"""
    url = f"https://cn.bing.com/search?q={quote(query)}&count={max_results}&ensearch=0"
    results = []
    try:
        resp = requests.get(url, timeout=10, headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select("li.b_algo")[:max_results]:
            title_el = item.select_one("h2 a")
            snippet_el = item.select_one(".b_caption p") or item.select_one("p")
            if title_el:
                results.append({
                    "title": title_el.get_text(strip=True),
                    "url": title_el.get("href", ""),
                    "snippet": snippet_el.get_text(strip=True)[:300] if snippet_el else "",
                    "source": "bing"
                })
    except Exception:
        pass
    return results


def search_baidu(query: str, max_results: int = 5) -> list[dict]:
    """百度搜索（备选二）"""
    url = f"https://www.baidu.com/s?wd={quote(query)}&rn={max_results}"
    results = []
    try:
        resp = requests.get(url, timeout=10, headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select("div.result, div.c-container")[:max_results]:
            title_el = item.select_one("h3 a")
            snippet_el = (item.select_one("span.content-right_2s-H4")
                          or item.select_one("div.c-abstract")
                          or item.select_one("span.c-color-text"))
            if title_el:
                href = title_el.get("href", "")
                results.append({
                    "title": title_el.get_text(strip=True),
                    "url": href,
                    "snippet": snippet_el.get_text(strip=True)[:300] if snippet_el else "",
                    "source": "baidu"
                })
    except Exception:
        pass
    return results




# ───────────────── 搜索调度 ─────────────────


# DDGS backend 优先级: google 质量最好, bing 作为备选
_DDGS_BACKENDS = ["google", "bing"]


def search_with_fallback(query: str, max_results: int = 5) -> tuple[list[dict], str]:
    """
    按优先级尝试搜索引擎，返回 (结果列表, 引擎名称)。
    优先走 DDGS（逐个 backend 尝试），全部失败再降级到 Bing/百度网页抓取。
    """
    # 1) DDGS 多 backend 尝试
    for backend in _DDGS_BACKENDS:
        results = search_ddgs(query, max_results, backend=backend)
        if results:
            return results, f"DDGS:{backend}"

    # 2) 网页抓取兜底
    for name, func in [("Bing", search_bing), ("百度", search_baidu)]:
        results = func(query, max_results)
        if results:
            return results, name

    return [], ""


def search_guides(city: str, category: str = "美食", tags: str = "",
                  max_results: int = 5) -> dict:
    """执行多组搜索并汇总结果"""
    year = datetime.now().year
    queries = build_queries(city, category, tags, year)
    all_results = []
    seen_urls = set()
    engines_used = set()

    for group in queries:
        results, engine = search_with_fallback(group["q"], max_results)
        if engine:
            engines_used.add(engine)

        for r in results:
            url = r.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_results.append({
                    "title": r.get("title", ""),
                    "url": url,
                    "snippet": r.get("snippet", ""),
                    "source_group": group["label"],
                })

        if not results:
            all_results.append({
                "title": f"[搜索无结果: {group['label']}]",
                "url": "",
                "snippet": f"关键词: {group['q']}，建议尝试其他关键词",
                "source_group": group["label"],
            })

    return {
        "city": city,
        "category": category,
        "tags": tags,
        "total": len(all_results),
        "engines_used": sorted(engines_used),
        "results": all_results,
    }


def main():
    parser = argparse.ArgumentParser(description="多平台攻略搜索")
    parser.add_argument("city", help="目标城市")
    parser.add_argument("--type", dest="category", default="美食", help="探店类型（默认: 美食）")
    parser.add_argument("--tags", default="", help="偏好标签，逗号分隔")
    parser.add_argument("--max-results", type=int, default=5, help="每组搜索最大结果数（默认5）")
    args = parser.parse_args()

    result = search_guides(args.city, args.category, args.tags, args.max_results)

    # 输出摘要到 stderr
    valid = [r for r in result.get("results", []) if r.get("url")]
    engines = ", ".join(result.get("engines_used", [])) or "无"
    summary(f"{args.city} {args.category} | {len(valid)}条有效结果 | 引擎: {engines}")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
