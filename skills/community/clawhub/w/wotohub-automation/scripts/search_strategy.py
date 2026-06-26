#!/usr/bin/env python3
"""Search strategy generation. Model-first, script-fallback."""

from __future__ import annotations

from typing import Any


def generate_search_strategy(product_summary: dict) -> dict:
    """Generate search strategy from product summary."""
    return {
        "keywords": product_summary.get("sellingPoints", [])[:5],
        "categories": product_summary.get("detectedForms", []),
        "regions": product_summary.get("regionHints", ["us"]),
        "languages": product_summary.get("languageHints", ["en"]),
        "minFans": None,
        "maxFans": None,
    }


def compile_payload(strategy: dict) -> dict:
    """Compile strategy into WotoHub API payload.

    This is fallback-only. Keep category mapping and keyword refinement separate.
    """
    from build_search_payload import to_advanced_keywords
    from query_constraints import build_region_list
    from category_inference import load_categories, build_category_ids

    keywords = to_advanced_keywords(strategy.get("keywords", []))
    data, by_code, _children, category_index = load_categories()
    category_query = " ".join(strategy.get("categories", []))
    category_ids, _matches = build_category_ids(category_query, data, by_code, category_index)
    payload = {
        "platform": "tiktok",
        "regionList": build_region_list(strategy.get("regions", [])),
        "blogLangs": strategy.get("languages", []),
        "hasEmail": True,
    }
    if strategy.get("minFans") is not None:
        payload["minFansNum"] = strategy.get("minFans")
    if strategy.get("maxFans") is not None:
        payload["maxFansNum"] = strategy.get("maxFans")
    if category_ids:
        payload["blogCateIds"] = category_ids
    if keywords:
        payload["advancedKeywordList"] = keywords
        payload["searchType"] = "KEYWORD"
    return payload
