"""
core/tea.py — 茶饮推荐 API 客户端

Usage:
    from core.tea import recommend_tea
    teas = recommend_tea("阳虚质")  # 免费
"""

from . import _api_request


def recommend_tea(constitution: str) -> list:
    """按体质推荐茶饮配方."""
    return _api_request("POST", "/api/search", {
        "category": "ingredients",
        "keywords": [constitution, "茶饮"],
    }).get("results", [])
