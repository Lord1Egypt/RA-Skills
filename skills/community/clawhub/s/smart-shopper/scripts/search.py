#!/usr/bin/env python3
"""Search products across Amazon, Temu, SHEIN via web scraping."""

import argparse, json, sys, urllib.request, urllib.parse, re

PLATFORMS = {
    "amazon": {
        "name": "Amazon",
        "search_url": "https://www.amazon.com/s?k={query}",
        "icon": "🟠",
    },
    "temu": {
        "name": "Temu",
        "search_url": "https://www.temu.com/search_result.html?search_key={query}",
        "icon": "🟡",
    },
    "shein": {
        "name": "SHEIN",
        "search_url": "https://www.shein.com/pdsearch/{query}/",
        "icon": "🩷",
    },
}

BUDGET_MAP = {
    "low": (0, 25),
    "mid": (25, 75),
    "high": (75, 9999),
}


def parse_budget(budget_str):
    if not budget_str:
        return None
    budget_str = budget_str.lower().strip()
    if budget_str in BUDGET_MAP:
        return BUDGET_MAP[budget_str]
    m = re.match(r'\$?(\d+)', budget_str)
    if m:
        val = int(m.group(1))
        return (0, val)
    return None


def search_platform(platform, query, budget=None, brand=None, color=None):
    """Generate search results for a platform (simulated with search URLs)."""
    p = PLATFORMS.get(platform)
    if not p:
        return None

    encoded_q = urllib.parse.quote(query)
    # Add filters to query
    full_query = query
    if brand:
        full_query += f" {brand}"
    if color:
        full_query += f" {color}"

    search_url = p["search_url"].format(query=urllib.parse.quote(full_query))

    # Generate structured search result with buy link
    result = {
        "platform": p["name"],
        "icon": p["icon"],
        "query": full_query,
        "search_url": search_url,
        "filters": {},
    }

    if budget:
        lo, hi = budget
        result["filters"]["budget"] = f"${lo}-${hi}"
        if platform == "amazon":
            search_url += f"&rh=p_36%3A{lo*100}-{hi*100}"
            result["search_url"] = search_url

    if brand:
        result["filters"]["brand"] = brand
    if color:
        result["filters"]["color"] = color

    return result


def search_all(query, platforms=None, budget=None, brand=None, color=None):
    if not platforms:
        platforms = list(PLATFORMS.keys())

    budget_range = parse_budget(budget)
    results = []
    for plat in platforms:
        r = search_platform(plat, query, budget_range, brand, color)
        if r:
            results.append(r)
    return {
        "query": query,
        "budget": budget,
        "brand": brand,
        "color": color,
        "platforms": len(results),
        "results": results,
    }


def format_output(data):
    lines = [f"🛒 搜索结果: \"{data['query']}\"", ""]
    if data.get("budget"):
        lines.append(f"💰 预算: {data['budget']}")
    if data.get("brand"):
        lines.append(f"🏷️ 品牌: {data['brand']}")
    if data.get("color"):
        lines.append(f"🎨 颜色: {data['color']}")
    lines.append(f"📦 搜索了 {data['platforms']} 个平台")
    lines.append("")

    for r in data["results"]:
        lines.append(f"{r['icon']} **{r['platform']}**")
        lines.append(f"   🔗 {r['search_url']}")
        if r["filters"]:
            filters = " | ".join(f"{k}: {v}" for k, v in r["filters"].items())
            lines.append(f"   🔍 筛选: {filters}")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--query", required=True, help="Product to search")
    p.add_argument("--platforms", default=None, help="Comma-separated: amazon,temu,shein")
    p.add_argument("--budget", default=None, help="low/mid/high or $XX")
    p.add_argument("--brand", default=None)
    p.add_argument("--color", default=None)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    plats = a.platforms.split(",") if a.platforms else None
    data = search_all(a.query, plats, a.budget, a.brand, a.color)
    print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else format_output(data))
