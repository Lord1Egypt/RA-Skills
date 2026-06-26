#!/usr/bin/env python3
"""
深蓝企业情报 API 客户端
Shenlan Company Intelligence API Client

用于 AI Agent Skill 的 API 封装，提供企业档案、舆情追踪、公告监控等能力。
"""

import json
import sys
import urllib.request
import urllib.parse

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
        "User-Agent": "ShenlanCompanyIntel-Skill/1.0"
    })

    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_companies(per_page=20, page=1):
    """获取企业列表"""
    return fetch("/companies", {"per_page": per_page, "page": page})


def get_company(company_id: int):
    """按ID获取企业详情"""
    return fetch(f"/companies/{company_id}")


def get_company_by_slug(slug: str):
    """按Slug获取企业详情"""
    return fetch(f"/companies/slug/{slug}")


def get_company_by_stock(stock_code: str):
    """按股票代码获取企业详情"""
    return fetch(f"/companies/stock/{stock_code}")


def get_company_contents(company_id: int):
    """获取企业关联内容"""
    return fetch(f"/companies/{company_id}/contents")


def get_company_mentions(company_id: int):
    """获取企业舆情（全平台提及）"""
    return fetch(f"/companies/{company_id}/mentions")


def get_company_followers(company_id: int):
    """获取企业关注者"""
    return fetch(f"/companies/{company_id}/followers")


def get_trending_companies():
    """获取热门企业排行"""
    return fetch("/trending/companies")


def get_stock_announcements(stock_code: str):
    """按股票代码获取公告"""
    return fetch(f"/stocks/{stock_code}/announcements")


def search_announcements(keyword: str):
    """搜索公告"""
    return fetch("/announcements/search", {"keyword": keyword})


def get_important_announcements():
    """获取重要公告"""
    return fetch("/announcements/important")


def get_announcement(announcement_id: int):
    """获取公告详情"""
    return fetch(f"/announcements/{announcement_id}")


# ---- CLI 入口 ----
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python api.py <command> [args...]")
        print("命令:")
        print("  companies                        企业列表")
        print("  company <id>                     企业详情（按ID）")
        print("  company-stock <股票代码>          企业详情（按股票代码）")
        print("  company-slug <slug>              企业详情（按Slug）")
        print("  contents <company_id>            企业关联内容")
        print("  mentions <company_id>            企业舆情追踪")
        print("  followers <company_id>           企业关注者")
        print("  trending                         热门企业排行")
        print("  announcements <stock_code>       按股票代码获取公告")
        print("  search-announcements <keyword>   搜索公告")
        print("  important-announcements          重要公告")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "companies":
        result = get_companies()
    elif cmd == "company":
        result = get_company(int(sys.argv[2]))
    elif cmd == "company-stock":
        result = get_company_by_stock(sys.argv[2])
    elif cmd == "company-slug":
        result = get_company_by_slug(sys.argv[2])
    elif cmd == "contents":
        result = get_company_contents(int(sys.argv[2]))
    elif cmd == "mentions":
        result = get_company_mentions(int(sys.argv[2]))
    elif cmd == "followers":
        result = get_company_followers(int(sys.argv[2]))
    elif cmd == "trending":
        result = get_trending_companies()
    elif cmd == "announcements":
        result = get_stock_announcements(sys.argv[2])
    elif cmd == "search-announcements":
        result = search_announcements(sys.argv[2])
    elif cmd == "important-announcements":
        result = get_important_announcements()
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))
