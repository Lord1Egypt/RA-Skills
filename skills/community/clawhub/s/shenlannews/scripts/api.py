#!/usr/bin/env python3
"""
深蓝财经新闻 API 客户端
Shenlan Finance News API Client

用于 AI Agent Skill 的 API 封装，提供实时快讯、头条文章、热门内容和全文搜索。
"""

import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime

BASE_URL = "https://www.shenlannews.com/api/v2"

def fetch(endpoint: str, params: dict = None) -> dict:
    """发起 GET 请求并返回 JSON 响应"""
    url = f"{BASE_URL}{endpoint}"
    if params:
        params = {k: v for k, v in params.items() if v is not None}
        if params:
            url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "ShenlanNews-Skill/1.0"
    })

    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_dispatches(search=None, is_major=None, sort="latest", per_page=20, page=1):
    """获取实时快讯"""
    return fetch("/dispatches", {
        "search": search,
        "is_major": 1 if is_major else None,
        "sort": sort,
        "per_page": per_page,
        "page": page,
        "status": "published"
    })


def get_articles(search=None, sort="latest", category_id=None, per_page=20, page=1):
    """获取头条文章"""
    return fetch("/articles", {
        "search": search,
        "sort": sort,
        "category_id": category_id,
        "per_page": per_page,
        "page": page,
        "status": "published"
    })


def get_article(article_id: int):
    """获取文章详情"""
    return fetch(f"/articles/{article_id}")


def get_dispatch(dispatch_id: int):
    """获取快讯详情"""
    return fetch(f"/dispatches/{dispatch_id}")


def get_trending_articles():
    """获取热门文章"""
    return fetch("/trending/articles")


def search_announcements(keyword: str):
    """搜索上市公司公告"""
    return fetch("/announcements/search", {"keyword": keyword})


def get_latest_announcements():
    """获取最新公告"""
    return fetch("/announcements/latest")


def get_important_announcements():
    """获取重要公告"""
    return fetch("/announcements/important")


def get_stock_announcements(stock_code: str):
    """按股票代码获取公告"""
    return fetch(f"/stocks/{stock_code}/announcements")


def get_rss_articles(per_page=20, page=1):
    """获取 RSS 聚合文章"""
    return fetch("/rss/articles", {"per_page": per_page, "page": page})


def get_rss_sources():
    """获取 RSS 来源列表"""
    return fetch("/rss/sources")


def get_categories():
    """获取内容分类"""
    return fetch("/categories")


def get_popular_tags():
    """获取热门标签"""
    return fetch("/tags/popular")


def search_tags(query: str):
    """搜索标签"""
    return fetch("/tags/search", {"q": query})


# ---- CLI 入口 ----
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python api.py <command> [args...]")
        print("命令:")
        print("  dispatches [--search=关键词] [--major] [--sort=latest|popular|headline]")
        print("  articles [--search=关键词] [--sort=latest|popular|featured|recommend]")
        print("  trending")
        print("  announcements [--keyword=关键词]")
        print("  stock-announcements <股票代码>")
        print("  rss")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "dispatches":
        kwargs = {}
        for arg in sys.argv[2:]:
            if arg.startswith("--search="):
                kwargs["search"] = arg.split("=", 1)[1]
            elif arg == "--major":
                kwargs["is_major"] = True
            elif arg.startswith("--sort="):
                kwargs["sort"] = arg.split("=", 1)[1]
        result = get_dispatches(**kwargs)

    elif cmd == "articles":
        kwargs = {}
        for arg in sys.argv[2:]:
            if arg.startswith("--search="):
                kwargs["search"] = arg.split("=", 1)[1]
            elif arg.startswith("--sort="):
                kwargs["sort"] = arg.split("=", 1)[1]
        result = get_articles(**kwargs)

    elif cmd == "trending":
        result = get_trending_articles()

    elif cmd == "announcements":
        keyword = None
        for arg in sys.argv[2:]:
            if arg.startswith("--keyword="):
                keyword = arg.split("=", 1)[1]
        if keyword:
            result = search_announcements(keyword)
        else:
            result = get_latest_announcements()

    elif cmd == "stock-announcements":
        if len(sys.argv) < 3:
            print("请提供股票代码，例如: python api.py stock-announcements 600519")
            sys.exit(1)
        result = get_stock_announcements(sys.argv[2])

    elif cmd == "rss":
        result = get_rss_articles()

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))
