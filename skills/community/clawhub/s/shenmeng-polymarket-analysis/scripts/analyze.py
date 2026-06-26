#!/usr/bin/env python3
"""
Polymarket 市场数据获取与分析脚本
用法: python3 analyze.py [mode] [args]

Modes:
  trending            获取热门市场
  category <cat>      按分类获取 (crypto/trump/btc/sports/politics)
  market <slug>      单市场详情
  volume              成交量排行榜
  analyze <slug>      综合分析一个市场
"""

import sys
import json
import os

# SkillPay 扣费集成
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from skillpay import billing_check
    BILLING_OK = billing_check(
        user_id=os.environ.get("SKILLPAY_USER_ID", "anonymous_user"),
        amount=0.001
    )
    if not BILLING_OK:
        print("[SkillPay] ❌ 余额不足，退出。充值后再试：https://skillpay.me")
        sys.exit(1)
except Exception as e:
    # 扣费失败不阻止执行（允许未配置时演示）
    print(f"[SkillPay] ⚠️  扣费检查跳过（演示模式）: {e}")
import urllib.request
import urllib.error
from datetime import datetime

BASE_GAMMA = "https://gamma.polymarket.com"
BASE_CLOB = "https://clob.polymarket.com"
BASE_WEB = "https://polymarket.com"

CATEGORIES = {
    "crypto": "predictions/crypto",
    "trump": "predictions/trump",
    "btc": "predictions/bitcoin",
    "sports": "predictions/sports",
    "politics": "predictions/politics",
    "weekly": "predictions/weekly",
    "all": "predictions",
}


def fetch(url: str) -> dict | None:
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=15) as r:
            ct = r.headers.get("Content-Type", "")
            if "json" in ct:
                return json.loads(r.read())
            return {"html": r.read().decode("utf-8", errors="replace")}
    except Exception as e:
        print(f"[WARN] fetch failed: {url} -> {e}", file=sys.stderr)
        return None


def get_trending(limit: int = 10) -> list:
    """获取热门市场（通过 CLOB API）"""
    data = fetch(f"{BASE_CLOB}/markets?limit={limit}&closed=false")
    if not data:
        return []
    markets = data if isinstance(data, list) else data.get("data", [])
    result = []
    for m in markets[:limit]:
        result.append({
            "question": m.get("question", "N/A"),
            "slug": m.get("slug", ""),
            "yes_price": m.get("yesPrice", "N/A"),
            "no_price": m.get("noPrice", "N/A"),
            "volume": m.get("volume", 0),
            "liquidity": m.get("liquidity", 0),
            "end_date": m.get("endDate", "N/A"),
            "url": f"{BASE_WEB}/event/{m.get('slug', '')}",
        })
    return result


def get_category(category: str, limit: int = 15) -> list:
    """按分类获取市场"""
    path = CATEGORIES.get(category, "predictions")
    # gamma API
    data = fetch(f"{BASE_GAMMA}/markets?limit={limit}&closed=false&category={path}")
    if not data:
        return []
    markets = data if isinstance(data, list) else data.get("data", data.get("markets", []))
    result = []
    for m in markets[:limit]:
        if isinstance(m, dict):
            result.append({
                "question": m.get("question", "N/A"),
                "slug": m.get("slug", ""),
                "yes_price": m.get("yesPrice", m.get("outcomePrices", ["N/A"])[0] if m.get("outcomePrices") else "N/A"),
                "volume": m.get("volume", m.get("volume24h", 0)),
                "liquidity": m.get("liquidity", 0),
                "url": f"{BASE_WEB}/event/{m.get('slug', '')}",
            })
    return result


def get_market_detail(slug: str) -> dict:
    """获取单个市场详情"""
    data = fetch(f"{BASE_CLOB}/markets/{slug}")
    if not data:
        # fallback to gamma
        data = fetch(f"{BASE_GAMMA}/events/{slug}")
    return data if data else {}


def format_market(m, indent: int = 2):
    sp = " " * indent
    yes_p = float(m.get("yes_price", 0) or 0)
    no_p = float(m.get("no_price", 0) or 0)
    vol = float(m.get("volume", 0) or 0)
    liq = float(m.get("liquidity", 0) or 0)

    print(f"{sp}📌 {m.get('question', 'N/A')}")
    print(f"{sp}   概率: 是 {yes_p*100:.1f}% / 否 {no_p*100:.1f}%")
    if vol > 1_000_000:
        print(f"{sp}   成交量: ${vol/1_000_000:.2f}M")
    elif vol > 1000:
        print(f"{sp}   成交量: ${vol/1000:.1f}K")
    else:
        print(f"{sp}   成交量: ${vol:.0f}")
    if liq > 1_000_000:
        print(f"{sp}   流动性: ${liq/1_000_000:.2f}M")
    elif liq > 0:
        print(f"{sp}   流动性: ${liq/1000:.1f}K")
    print(f"{sp}   链接: {m.get('url', 'N/A')}")
    print()


def cmd_trending(args):
    limit = int(args[0]) if args else 10
    print(f"\n🔥 Polymarket 热门市场 (Top {limit})\n")
    markets = get_trending(limit)
    if not markets:
        print("获取失败，请检查网络或 VPN 状态")
        return
    for i, m in enumerate(markets, 1):
        print(f"[{i}]", end=" ")
        format_market(m, indent=3)


def cmd_category(args):
    if not args:
        print("用法: analyze.py category <crypto|trump|btc|sports|politics|weekly|all>")
        return
    cat = args[0].lower()
    if cat not in CATEGORIES:
        print(f"未知分类: {cat}")
        print(f"可选: {list(CATEGORIES.keys())}")
        return
    print(f"\n📂 Polymarket {cat} 市场\n")
    markets = get_category(cat)
    if not markets:
        print("获取失败，请检查网络或 VPN 状态")
        return
    for i, m in enumerate(markets, 1):
        print(f"[{i}]", end=" ")
        format_market(m, indent=3)


def cmd_volume(args):
    print("\n📊 Polymarket 成交量排行 (周榜)\n")
    markets = get_trending(20)
    if not markets:
        print("获取失败")
        return
    sorted_markets = sorted(markets, key=lambda x: float(x.get("volume", 0) or 0), reverse=True)
    for i, m in enumerate(sorted_markets[:10], 1):
        print(f"[{i}]", end=" ")
        format_market(m, indent=3)


def cmd_analyze(args):
    if not args:
        print("用法: analyze.py analyze <market-slug>")
        return
    slug = args[0]
    print(f"\n🔍 深度分析: {slug}\n")
    detail = get_market_detail(slug)
    if not detail:
        print("获取失败，请检查 slug 是否正确")
        return
    print(json.dumps(detail, indent=2, ensure_ascii=False))


def main():
    if len(sys.argv) < 2:
        # 默认输出热门
        cmd_trending([])
        return

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    if cmd == "trending":
        cmd_trending(args)
    elif cmd == "category":
        cmd_category(args)
    elif cmd == "volume":
        cmd_volume(args)
    elif cmd == "market":
        cmd_analyze(args)
    elif cmd == "analyze":
        cmd_analyze(args)
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
