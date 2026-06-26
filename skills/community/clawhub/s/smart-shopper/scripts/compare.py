#!/usr/bin/env python3
"""Compare products across platforms side-by-side."""

import argparse, json, sys, urllib.parse

PLATFORMS = {
    "amazon": {"name": "Amazon", "icon": "🟠", "base": "https://www.amazon.com/s?k="},
    "temu": {"name": "Temu", "icon": "🟡", "base": "https://www.temu.com/search_result.html?search_key="},
    "shein": {"name": "SHEIN", "icon": "🩷", "base": "https://www.shein.com/pdsearch/"},
}

# Platform characteristics for comparison
TRAITS = {
    "amazon": {"shipping": "1-2天(Prime)", "return": "30天", "trust": "⭐⭐⭐⭐⭐", "price_tier": "中-高", "strength": "品质保障、快速配送、评论真实"},
    "temu": {"shipping": "7-15天", "return": "90天", "trust": "⭐⭐⭐", "price_tier": "低", "strength": "极致低价、免费退货、新用户优惠"},
    "shein": {"shipping": "7-12天", "return": "45天", "trust": "⭐⭐⭐⭐", "price_tier": "低-中", "strength": "时尚潮流、款式多样、定期折扣"},
}


def compare(query, platforms=None):
    if not platforms:
        platforms = list(PLATFORMS.keys())

    results = []
    for plat in platforms:
        p = PLATFORMS.get(plat)
        t = TRAITS.get(plat, {})
        if not p:
            continue
        encoded = urllib.parse.quote(query)
        url = f"{p['base']}{encoded}" if "shein" not in plat else f"{p['base']}{encoded}/"

        results.append({
            "platform": p["name"],
            "icon": p["icon"],
            "search_url": url,
            "shipping": t.get("shipping", "N/A"),
            "return_policy": t.get("return", "N/A"),
            "trust_score": t.get("trust", "N/A"),
            "price_tier": t.get("price_tier", "N/A"),
            "strength": t.get("strength", ""),
        })

    # Recommendation
    rec = "Temu" if "temu" in platforms else "Amazon"
    rec_reason = "最低价格" if rec == "Temu" else "品质保障"

    return {
        "query": query,
        "comparison": results,
        "recommendation": {"platform": rec, "reason": rec_reason},
    }


def format_output(data):
    lines = [f"⚖️ 价格对比: \"{data['query']}\"", ""]

    for r in data["comparison"]:
        lines.append(f"{r['icon']} **{r['platform']}**")
        lines.append(f"   💰 价位: {r['price_tier']}")
        lines.append(f"   🚚 配送: {r['shipping']}")
        lines.append(f"   🔄 退货: {r['return_policy']}")
        lines.append(f"   ⭐ 信任: {r['trust_score']}")
        lines.append(f"   💪 优势: {r['strength']}")
        lines.append(f"   🔗 {r['search_url']}")
        lines.append("")

    rec = data["recommendation"]
    lines.append(f"🏆 推荐: {rec['platform']} ({rec['reason']})")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--query", required=True)
    p.add_argument("--platforms", default=None, help="Comma-separated")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    plats = a.platforms.split(",") if a.platforms else None
    data = compare(a.query, plats)
    print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else format_output(data))
