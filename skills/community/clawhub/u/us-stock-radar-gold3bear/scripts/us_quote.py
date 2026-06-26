"""
美股个股实时行情
用法: python us_quote.py NVDA TSLA AAPL
"""
import requests
import sys

MAJOR_STOCKS = {
    "NVDA": "英伟达",
    "AAPL": "苹果",
    "MSFT": "微软",
    "GOOGL": "谷歌",
    "AMZN": "亚马逊",
    "META": "Meta",
    "TSLA": "特斯拉",
    "AMD": "AMD",
    "NFLX": "Netflix",
    "CRM": "Salesforce",
    "AVGO": "博通",
    "ORCL": "甲骨文",
    "COIN": "Coinbase",
}

def get_stock_quote(symbol):
    """获取个股行情"""
    sym = symbol.upper()
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code != 200:
        return None
    d = r.json()
    try:
        meta = d["chart"]["result"][0]["meta"]
        price = meta.get("regularMarketPrice")
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        if price is None or prev is None:
            return None
        chg = price - prev
        pct = chg / prev * 100
        return {"symbol": sym, "name": MAJOR_STOCKS.get(sym, sym),
                "price": price, "chg": chg, "pct": pct}
    except (KeyError, IndexError):
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # 默认显示科技巨头
        symbols = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA"]
    else:
        symbols = sys.argv[1:]

    print("\n=== 🏛️ 美股个股 ===")
    for sym in symbols:
        q = get_stock_quote(sym)
        if q:
            arrow = "🟢" if q["chg"] > 0 else "🔴" if q["chg"] < 0 else "⚪"
            name = q["name"]
            print(f"{arrow} {name:12s}({q['symbol']:6s}) {q['price']:>10.2f}  {q['chg']:>+8.2f}({q['pct']:>+6.2f}%)")
        else:
            print(f"⚪ {sym}: 获取失败")
