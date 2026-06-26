#!/usr/bin/env python3
"""Local store search using Google Maps / web search."""

import argparse, json, sys, urllib.parse


def search_local(query, location="nearby"):
    """Generate local store search links and suggestions."""
    encoded_q = urllib.parse.quote(f"{query} store near {location}")

    results = {
        "query": query,
        "location": location,
        "search_links": {
            "google_maps": f"https://www.google.com/maps/search/{urllib.parse.quote(query + ' near ' + location)}",
            "google_shopping": f"https://www.google.com/search?q={encoded_q}&tbm=shop&tbs=mr:1,local_avail:1",
            "yelp": f"https://www.yelp.com/search?find_desc={urllib.parse.quote(query)}&find_loc={urllib.parse.quote(location)}",
        },
        "tips": [
            f"在 Google Maps 搜索 \"{query}\" 查看附近门店",
            "查看门店营业时间和库存情况",
            "对比线上价格再决定是否到店购买",
            "部分商品支持线上下单、到店自提",
        ],
        "common_stores": _suggest_stores(query),
    }
    return results


def _suggest_stores(query):
    """Suggest common store types based on product category."""
    q = query.lower()
    stores = []

    if any(w in q for w in ["phone", "电子", "laptop", "电脑", "耳机", "charger", "cable"]):
        stores = [
            {"name": "Best Buy", "type": "电子产品", "icon": "🔵"},
            {"name": "Apple Store", "type": "苹果产品", "icon": "🍎"},
            {"name": "Walmart Electronics", "type": "综合电子", "icon": "🟦"},
        ]
    elif any(w in q for w in ["clothes", "衣服", "shirt", "dress", "鞋", "shoes", "fashion"]):
        stores = [
            {"name": "Target", "type": "服装综合", "icon": "🔴"},
            {"name": "H&M", "type": "快时尚", "icon": "🟥"},
            {"name": "Uniqlo", "type": "基础款", "icon": "⬜"},
            {"name": "Zara", "type": "时尚", "icon": "⬛"},
        ]
    elif any(w in q for w in ["food", "grocery", "食品", "水果", "零食"]):
        stores = [
            {"name": "Whole Foods", "type": "有机食品", "icon": "🟢"},
            {"name": "Trader Joe's", "type": "特色食品", "icon": "🌺"},
            {"name": "Costco", "type": "批发", "icon": "🏪"},
        ]
    elif any(w in q for w in ["furniture", "家具", "home", "家居", "decor"]):
        stores = [
            {"name": "IKEA", "type": "家具家居", "icon": "🟨"},
            {"name": "HomeGoods", "type": "家居装饰", "icon": "🏠"},
            {"name": "Walmart Home", "type": "综合家居", "icon": "🟦"},
        ]
    else:
        stores = [
            {"name": "Walmart", "type": "综合超市", "icon": "🟦"},
            {"name": "Target", "type": "综合百货", "icon": "🔴"},
            {"name": "Costco", "type": "会员批发", "icon": "🏪"},
        ]
    return stores


def format_output(data):
    lines = [f"📍 本地搜索: \"{data['query']}\" @ {data['location']}", ""]

    lines.append("🔗 搜索链接:")
    for name, url in data["search_links"].items():
        lines.append(f"   {name}: {url}")
    lines.append("")

    lines.append("🏪 推荐门店:")
    for s in data["common_stores"]:
        lines.append(f"   {s['icon']} {s['name']} ({s['type']})")
    lines.append("")

    lines.append("💡 小贴士:")
    for t in data["tips"]:
        lines.append(f"   • {t}")

    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--query", required=True)
    p.add_argument("--location", default="nearby")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    data = search_local(a.query, a.location)
    print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else format_output(data))
