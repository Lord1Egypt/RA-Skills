#!/usr/bin/env python3
"""获取实时行情数据"""
import requests
import json
import sys

def _load_json(response):
    try:
        return response.json()
    except ValueError:
        raise ValueError("Binance API returned non-JSON response")

def _raise_if_binance_error(data, symbol):
    if isinstance(data, dict) and isinstance(data.get("code"), int) and data.get("code", 0) < 0:
        msg = str(data.get("msg", "unknown error"))
        if "Invalid symbol" in msg:
            raise ValueError(f"Invalid symbol '{symbol}'. Use Binance spot symbol like BTCUSDT.")
        raise ValueError(f"Binance API error: {msg}")

def get_spot_price(symbol="BTCUSDT"):
    """获取现货实时价格"""
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url, params={"symbol": symbol}, timeout=10)
    data = _load_json(response)
    _raise_if_binance_error(data, symbol)
    if "price" not in data:
        raise ValueError("Unexpected Binance response: missing 'price'")
    return float(data["price"])

def get_spot_ticker(symbol="BTCUSDT"):
    """获取现货 24 小时行情"""
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url, params={"symbol": symbol}, timeout=10)
    data = _load_json(response)
    _raise_if_binance_error(data, symbol)
    required_keys = ["symbol", "lastPrice", "highPrice", "lowPrice", "priceChangePercent", "volume"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        raise ValueError(f"Unexpected Binance response: missing {', '.join(missing)}")
    return {
        "symbol": data["symbol"],
        "price": float(data["lastPrice"]),
        "high_24h": float(data["highPrice"]),
        "low_24h": float(data["lowPrice"]),
        "change_24h_pct": float(data["priceChangePercent"]),
        "volume_24h": float(data["volume"])
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="获取 Binance 现货行情")
    parser.add_argument("--symbol", default="BTCUSDT", help="交易对")
    parser.add_argument("--type", default="price", choices=["price", "ticker"], help="查询类型")
    args = parser.parse_args()

    try:
        if args.type == "price":
            price = get_spot_price(args.symbol)
            result = {
                "symbol": args.symbol,
                "price": price,
                "success": True
            }
        else:
            ticker = get_spot_ticker(args.symbol)
            result = {
                **ticker,
                "success": True
            }

        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
