#!/usr/bin/env python3
"""
Crypto Market Data Fetcher - OpenClaw Skill Script
Fetches real-time and historical cryptocurrency prices from multiple data sources
with automatic fallback: Binance → CoinGecko → CoinCap → CryptoCompare

SECURITY MANIFEST:
- This script makes GET requests to public cryptocurrency APIs only
- No filesystem writes except stdout
- No shell execution
- Requires: requests (pip install requests)

Usage:
    python fetch_market.py --user USER_ID --coins BTC,ETH,SOL
    python fetch_market.py --user USER_ID --coins BTC --historical --days 30
    python fetch_market.py --coins BTC,ETH --test-mode
"""

import requests
import json
import sys
import argparse
import time
from typing import Dict, List, Optional

# ============ Configuration ============

SUPPORTED_COINS = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'DOGE']

BINANCE_API_URL = "https://api.binance.com/api/v3"
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
COINCAP_API_URL = "https://api.coincap.io/v2"
CRYPTOCOMPARE_API_URL = "https://min-api.cryptocompare.com/data"

BINANCE_SYMBOLS = {
    'BTC': 'BTCUSDT', 'ETH': 'ETHUSDT', 'SOL': 'SOLUSDT',
    'BNB': 'BNBUSDT', 'XRP': 'XRPUSDT', 'DOGE': 'DOGEUSDT'
}

COINGECKO_MAPPING = {
    'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana',
    'BNB': 'binancecoin', 'XRP': 'ripple', 'DOGE': 'dogecoin'
}

COINCAP_MAPPING = {
    'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana',
    'BNB': 'binance-coin', 'XRP': 'xrp', 'DOGE': 'dogecoin'
}


# ============ Price Fetchers ============

def get_prices_from_binance(coins: List[str]) -> Optional[Dict]:
    """Fetch prices from Binance API (fastest, most reliable)"""
    try:
        symbols = [BINANCE_SYMBOLS[c] for c in coins if c in BINANCE_SYMBOLS]
        if not symbols:
            return None

        symbols_param = '[' + ','.join([f'"{s}"' for s in symbols]) + ']'
        response = requests.get(
            f"{BINANCE_API_URL}/ticker/24hr",
            params={'symbols': symbols_param},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

        prices = {}
        for item in data:
            symbol = item['symbol']
            for coin, binance_symbol in BINANCE_SYMBOLS.items():
                if binance_symbol == symbol and coin in coins:
                    prices[coin] = {
                        'price': float(item['lastPrice']),
                        'change_24h': float(item['priceChangePercent']),
                        'high_24h': float(item['highPrice']),
                        'low_24h': float(item['lowPrice']),
                        'volume_24h': float(item['quoteVolume']),
                        'source': 'binance'
                    }
                    break
        return prices if prices else None
    except Exception:
        return None


def get_prices_from_coingecko(coins: List[str]) -> Optional[Dict]:
    """Fetch prices from CoinGecko API"""
    try:
        coin_ids = [COINGECKO_MAPPING.get(c, c.lower()) for c in coins]
        response = requests.get(
            f"{COINGECKO_API_URL}/simple/price",
            params={
                'ids': ','.join(coin_ids),
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true',
                'include_high_24hr': 'true',
                'include_low_24hr': 'true'
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        prices = {}
        for coin in coins:
            coin_id = COINGECKO_MAPPING.get(coin, coin.lower())
            if coin_id in data:
                prices[coin] = {
                    'price': data[coin_id].get('usd', 0),
                    'change_24h': data[coin_id].get('usd_24h_change', 0),
                    'high_24h': data[coin_id].get('usd_24h_high', 0),
                    'low_24h': data[coin_id].get('usd_24h_low', 0),
                    'volume_24h': data[coin_id].get('usd_24h_vol', 0),
                    'source': 'coingecko'
                }
        return prices if prices else None
    except Exception:
        return None


def get_prices_from_coincap(coins: List[str]) -> Optional[Dict]:
    """Fetch prices from CoinCap API"""
    try:
        ids = [COINCAP_MAPPING.get(c) for c in coins if c in COINCAP_MAPPING]
        if not ids:
            return None

        response = requests.get(
            f"{COINCAP_API_URL}/assets",
            params={'ids': ','.join(ids)},
            timeout=10
        )
        response.raise_for_status()
        data = response.json().get('data', [])

        reverse_map = {v: k for k, v in COINCAP_MAPPING.items()}
        prices = {}
        for item in data:
            coin = reverse_map.get(item['id'])
            if coin and coin in coins:
                prices[coin] = {
                    'price': float(item.get('priceUsd', 0)),
                    'change_24h': float(item.get('changePercent24Hr', 0)),
                    'high_24h': 0,
                    'low_24h': 0,
                    'volume_24h': float(item.get('volumeUsd24Hr', 0)),
                    'source': 'coincap'
                }
        return prices if prices else None
    except Exception:
        return None


def get_prices_from_cryptocompare(coins: List[str]) -> Optional[Dict]:
    """Fetch prices from CryptoCompare API (last resort)"""
    try:
        response = requests.get(
            f"{CRYPTOCOMPARE_API_URL}/pricemultifull",
            params={
                'fsyms': ','.join(coins),
                'tsyms': 'USD'
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json().get('RAW', {})

        prices = {}
        for coin in coins:
            if coin in data and 'USD' in data[coin]:
                info = data[coin]['USD']
                prices[coin] = {
                    'price': float(info.get('PRICE', 0)),
                    'change_24h': float(info.get('CHANGEPCT24HOUR', 0)),
                    'high_24h': float(info.get('HIGH24HOUR', 0)),
                    'low_24h': float(info.get('LOW24HOUR', 0)),
                    'volume_24h': float(info.get('TOTALVOLUME24HTO', 0)),
                    'source': 'cryptocompare'
                }
        return prices if prices else None
    except Exception:
        return None


# ============ Historical Data ============

def get_historical_from_binance(coin: str, days: int) -> Optional[List[Dict]]:
    """Fetch historical prices from Binance (most stable)"""
    try:
        symbol = BINANCE_SYMBOLS.get(coin)
        if not symbol:
            return None

        interval = '1d' if days > 7 else '1h'
        limit = days if days > 7 else days * 24

        response = requests.get(
            f"{BINANCE_API_URL}/klines",
            params={'symbol': symbol, 'interval': interval, 'limit': limit},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        prices = []
        for kline in data:
            prices.append({
                'timestamp': kline[0],
                'open': float(kline[1]),
                'high': float(kline[2]),
                'low': float(kline[3]),
                'close': float(kline[4]),
                'volume': float(kline[5])
            })
        return prices if prices else None
    except Exception:
        return None


def get_historical_from_coingecko(coin: str, days: int) -> Optional[List[Dict]]:
    """Fetch historical prices from CoinGecko"""
    try:
        coin_id = COINGECKO_MAPPING.get(coin, coin.lower())
        response = requests.get(
            f"{COINGECKO_API_URL}/coins/{coin_id}/market_chart",
            params={'vs_currency': 'usd', 'days': days},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        prices = []
        for point in data.get('prices', []):
            prices.append({
                'timestamp': point[0],
                'close': point[1],
                'open': point[1],
                'high': point[1],
                'low': point[1],
                'volume': 0
            })
        return prices if prices else None
    except Exception:
        return None


# ============ Main Logic ============

def fetch_current_prices(coins: List[str]) -> Dict:
    """Get current prices with multi-source fallback"""
    # Validate coins
    valid_coins = [c.upper() for c in coins if c.upper() in SUPPORTED_COINS]
    if not valid_coins:
        return {"error": f"No valid coins. Supported: {', '.join(SUPPORTED_COINS)}"}

    # Try sources in order
    for fetcher_name, fetcher in [
        ("Binance", get_prices_from_binance),
        ("CoinGecko", get_prices_from_coingecko),
        ("CoinCap", get_prices_from_coincap),
        ("CryptoCompare", get_prices_from_cryptocompare)
    ]:
        result = fetcher(valid_coins)
        if result and len(result) > 0:
            return {
                "status": "success",
                "data": result,
                "coins_requested": valid_coins,
                "timestamp": int(time.time())
            }

    return {"error": "All data sources failed. Please try again later."}


def fetch_historical_prices(coin: str, days: int) -> Dict:
    """Get historical prices with fallback"""
    coin = coin.upper()
    if coin not in SUPPORTED_COINS:
        return {"error": f"Unsupported coin: {coin}. Supported: {', '.join(SUPPORTED_COINS)}"}

    # Try Binance first, then CoinGecko
    for fetcher_name, fetcher in [
        ("Binance", get_historical_from_binance),
        ("CoinGecko", get_historical_from_coingecko)
    ]:
        result = fetcher(coin, days)
        if result:
            return {
                "status": "success",
                "coin": coin,
                "days": days,
                "data_points": len(result),
                "data": result,
                "timestamp": int(time.time())
            }

    return {"error": f"Failed to get historical data for {coin}. Please try again later."}


def main():
    parser = argparse.ArgumentParser(description="Crypto Market Data Fetcher")
    parser.add_argument("--coins", required=True, help="Comma-separated coin symbols (e.g. BTC,ETH,SOL)")
    parser.add_argument("--historical", action="store_true", help="Fetch historical data instead of current prices")
    parser.add_argument("--days", type=int, default=30, help="Days of historical data (default: 30)")
    parser.add_argument("--user", type=str, default="", help="User ID for billing")
    parser.add_argument("--test-mode", action="store_true", help="Skip billing for testing")

    args = parser.parse_args()

    # Billing check (skip in test mode)
    if args.user and not args.test_mode:
        from billing import charge_user
        billing_result = charge_user(args.user)
        if not billing_result["ok"]:
            output = {
                "error": "Payment required",
                "message": billing_result.get("message", "Insufficient balance"),
                "payment_url": billing_result.get("payment_url")
            }
            print(json.dumps(output, indent=2))
            sys.exit(1)

    coins = [c.strip().upper() for c in args.coins.split(",")]

    if args.historical:
        # Historical mode: fetch for first coin only
        result = fetch_historical_prices(coins[0], args.days)
    else:
        result = fetch_current_prices(coins)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
