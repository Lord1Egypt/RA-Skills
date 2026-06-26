#!/usr/bin/env python3
"""
Yahoo Finance 数据获取工具
通过 mihomo 代理获取美股数据
"""
import requests
import sys

PROXY = {
    'http': 'http://127.0.0.1:7891',
    'https': 'http://127.0.0.1:7891'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}


def get_stock_price(symbol):
    """获取单只股票/ETF 最新价格"""
    session = requests.Session()
    session.proxies = PROXY
    session.headers.update(HEADERS)

    url = f'https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d'
    r = session.get(url, timeout=15)

    if r.status_code == 200:
        d = r.json()
        result = d['chart']['result'][0]['meta']
        prev = result.get('regularMarketPreviousClose') or result.get('chartPreviousClose') or result['regularMarketPrice']
        return {
            'symbol': symbol,
            'price': result['regularMarketPrice'],
            'prev_close': prev,
            'change': result['regularMarketPrice'] - prev,
            'change_pct': ((result['regularMarketPrice'] / prev) - 1) * 100,
            'currency': result.get('currency', 'USD')
        }
    elif r.status_code == 429:
        raise Exception("Rate limited")
    else:
        raise Exception(f"HTTP {r.status_code}")


def get_crypto_price(symbol):
    """获取加密货币价格 (Binance)"""
    session = requests.Session()
    session.proxies = PROXY
    session.headers.update(HEADERS)

    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    r = session.get(url, timeout=10)

    if r.status_code == 200:
        d = r.json()
        return {
            'symbol': symbol,
            'price': float(d['price'])
        }
    else:
        raise Exception(f"Binance HTTP {r.status_code}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python yahoo_finance.py <SYMBOL>")
        print("Example: python yahoo_finance.py AAPL SPY QQQ BTC-USD ETH-USD")
        sys.exit(1)

    for symbol in sys.argv[1:]:
        try:
            # 加密货币 symbol 转换 (BTC-USD -> BTCUSDT)
            is_crypto = '-' in symbol and not symbol.startswith('^')
            if is_crypto:
                binance_symbol = symbol.replace('-', '')  # BTC-USD -> BTCUSDT
                data = get_crypto_price(binance_symbol)
                print(f"{symbol}: ${data['price']:,.2f}")
            else:
                data = get_stock_price(symbol)
                arrow = '↑' if data['change'] > 0 else '↓'
                print(f"{symbol}: ${data['price']:.2f} ({arrow}{abs(data['change_pct']):.2f}%)")
        except Exception as e:
            print(f"{symbol}: ERROR - {str(e)}")
