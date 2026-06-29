#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密货币价格查询脚本
支持 Binance / CoinGecko / CoinCap 多数据源自动降级
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime

# 币种名称映射
COIN_MAP = {
    "btc": "bitcoin", "eth": "ethereum", "sol": "solana",
    "bnb": "binancecoin", "xrp": "ripple", "ada": "cardano",
    "doge": "dogecoin", "avax": "avalanche-2", "dot": "polkadot",
    "matic": "matic-network", "link": "chainlink", "uni": "uniswap",
    "比特币": "bitcoin", "以太坊": "ethereum", "索拉纳": "solana",
}

CURRENCY_SYMBOL = {"usd": "$", "cny": "¥", "eur": "€"}

def fetch_coingecko(coin_id, currency="usd"):
    """CoinGecko 免费 API"""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}&include_24hr_change=true&include_24hr_vol=true"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        if coin_id in data:
            d = data[coin_id]
            return {
                "price": d.get(currency, 0),
                "change_24h": d.get(f"{currency}_24h_change", 0),
                "volume_24h": d.get(f"{currency}_24h_vol", 0),
                "source": "CoinGecko"
            }
    except Exception as e:
        print(f"CoinGecko error: {e}", file=sys.stderr)
    return None

def fetch_coincap(coin_id, currency="usd"):
    """CoinCap 免费 API（备用）"""
    coincap_map = {
        "bitcoin": "bitcoin", "ethereum": "ethereum", "solana": "solana",
        "binancecoin": "binance-coin", "dogecoin": "dogecoin",
    }
    cap_id = coincap_map.get(coin_id, coin_id)
    url = f"https://api.coincap.io/v2/assets/{cap_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        if "data" in data:
            d = data["data"]
            return {
                "price": float(d.get("priceUsd", 0)),
                "change_24h": float(d.get("changePercent24Hr", 0)),
                "volume_24h": float(d.get("volumeUsd24Hr", 0)),
                "source": "CoinCap"
            }
    except Exception as e:
        print(f"CoinCap error: {e}", file=sys.stderr)
    return None

def format_price(price, currency="usd"):
    """格式化价格显示"""
    symbol = CURRENCY_SYMBOL.get(currency, "")
    if price >= 1000:
        return f"{symbol}{price:,.2f}"
    elif price >= 1:
        return f"{symbol}{price:.4f}"
    else:
        return f"{symbol}{price:.8f}"

def format_change(change):
    """格式化涨跌幅"""
    if change >= 0:
        return f"+{change:.2f}%"
    return f"{change:.2f}%"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="加密货币价格查询")
    parser.add_argument("--coin", required=True, help="币种符号，如 btc, eth")
    parser.add_argument("--currency", default="usd", help="法币，默认usd")
    args = parser.parse_args()

    coin_key = args.coin.lower().strip()
    coin_id = COIN_MAP.get(coin_key, coin_key)
    currency = args.currency.lower()

    # 依次尝试数据源
    result = fetch_coingecko(coin_id, currency)
    if not result:
        result = fetch_coincap(coin_id, currency)
    if not result:
        print(f"❌ 无法获取 {coin_key} 价格，所有数据源均失败")
        sys.exit(1)

    price_str = format_price(result["price"], currency)
    change_str = format_change(result["change_24h"])
    vol = result["volume_24h"]
    vol_str = f"${vol/1e9:.1f}B" if vol >= 1e9 else f"${vol/1e6:.1f}M"

    emoji = "📈" if result["change_24h"] >= 0 else "📉"
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    print(f"🪙 {coin_key.upper()}/{currency.upper()}")
    print(f"━━━━━━━━━━━━━━━━━")
    print(f"💰 当前：{price_str}")
    print(f"{emoji} 24h：{change_str}")
    print(f"🔄 24h量：{vol_str}")
    print(f"📡 来源：{result['source']}")
    print(f"📅 更新：{now}")

if __name__ == "__main__":
    main()
