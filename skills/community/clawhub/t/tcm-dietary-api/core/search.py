"""
core/search.py — 知识检索 API 客户端

POST /api/search → 全文检索 9 个知识库

Usage:
    from core.search import search, get_ingredient
    results = search("ingredients", ["生姜"])  # 免费
"""

import json
import urllib.request
import urllib.error
from . import API_BASE, api_key, _api_request

# 有效分类
VALID_CATEGORIES = [
    "tcm-theory", "ingredients", "dishes", "chronic-diseases",
    "symptoms", "food-therapy-cases", "cosmetic_formulas",
    "daoyin_module", "nutrition",
]


def search(category: str, keywords: list) -> list:
    """
    全文检索知识库.

    通过 HTTPS 发送检索关键词到 api.tcmplate.com.
    请勿在 keywords 中包含个人信息.

    Args:
        category: 知识库分类名
        keywords: 搜索词列表

    Returns:
        匹配的知识条目列表 (最多 20 条)
    """
    if category not in VALID_CATEGORIES:
        raise ValueError(f"无效分类 '{category}'. 有效值: {VALID_CATEGORIES}")
    return _api_request("POST", "/api/search", {
        "category": category,
        "keywords": keywords,
    }).get("results", [])


def get_ingredient(name: str) -> dict:
    """查询单个食材属性. 返回 dict 或 None."""
    results = search("ingredients", [name])
    for r in results:
        if isinstance(r, dict) and r.get("name", "").strip() == name.strip():
            return r
    return None
