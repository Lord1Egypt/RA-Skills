"""
美股主要指数 + 期货 + 大宗商品 + 宏观利率实时行情
三数据源：
  1. Yahoo Finance query1（主）
  2. Yahoo Finance query2（备用域名）
  3. Finviz HTML 解析（兜底）
"""
import requests
from datetime import datetime, timezone
import concurrent.futures

SYMBOLS = {
    # 指数
    "^GSPC": "标普500",
    "^DJI": "道琼斯",
    "^IXIC": "纳斯达克",
    "^VIX": "VIX恐慌指数",
    # 期货
    "NQ=F": "纳指期货(NQ)",
    "ES=F": "标普期货(ES)",
    "YM=F": "道指期货(YM)",
    # 大宗商品
    "GC=F": "黄金",
    "CL=F": "WTI原油",
    "SI=F": "白银",
}

NYFED_RATES_URL = "https://markets.newyorkfed.org/api/rates/all/latest.json"
FRED_URL_TMPL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&vintage_date={date}"

# Yahoo Finance 域名池（轮流尝试，绕过单域名限流）
YAHOO_HOSTS = ["query1.finance.yahoo.com", "query2.finance.yahoo.com"]


def _get_quote_from_host(symbol, host):
    url = f"https://{host}/v8/finance/chart/{symbol}?interval=1d&range=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    d = r.json()
    meta = d["chart"]["result"][0]["meta"]
    price = meta.get("regularMarketPrice")
    prev = meta.get("chartPreviousClose") or meta.get("previousClose")
    if price is None or prev in (None, 0):
        return None
    chg = price - prev
    pct = chg / prev * 100
    return {
        "price": price, "chg": chg, "pct": pct,
        "high": meta.get("regularMarketDayHigh"),
        "low": meta.get("regularMarketDayLow"),
    }


def get_quote(symbol):
    """从多个 Yahoo Finance 域名依次尝试，失败则返回 None"""
    for host in YAHOO_HOSTS:
        try:
            result = _get_quote_from_host(symbol, host)
            if result:
                return result
        except Exception:
            continue
    return None


def get_all_quotes():
    results = {}
    for sym, name in SYMBOLS.items():
        q = get_quote(sym)
        if q:
            arrow = "🟢" if q["chg"] > 0 else "🔴" if q["chg"] < 0 else "⚪"
            results[sym] = {
                "name": name, "price": q["price"],
                "chg": q["chg"], "pct": q["pct"], "arrow": arrow
            }

    # Yahoo 全挂时：尝试 Finviz HTML 解析兜底
    if not results:
        results = _get_finviz_fallback()
    return results


def _get_finviz_fallback():
    """
    Finviz HTML 解析兜底（Yahoo Finance 全挂时调用）
    Finviz 无需 API key，直接抓取指数页面
    """
    INDEX_MAP = {
        "^GSPC": ("标普500", "S&P 500"),
        "^DJI": ("道琼斯", "Dow Jones"),
        "^IXIC": ("纳斯达克", "NASDAQ 100"),
        "^VIX": ("VIX恐慌指数", "CBOE Volatility Index"),
        "NQ=F": ("纳指期货(NQ)", "Nasdaq 100 Futures"),
        "ES=F": ("标普期货(ES)", "S&P 500 Futures"),
        "GC=F": ("黄金", "Gold"),
        "CL=F": ("WTI原油", "Crude Oil"),
        "SI=F": ("白银", "Silver"),
    }
    # Finviz 个股/指数页面
    FINVIZ_URL = "https://finviz.com/indices.ashx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.finviz.com/",
    }
    try:
        r = requests.get(FINVIZ_URL, headers=headers, timeout=15)
        r.raise_for_status()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "lxml")
        results = {}
        rows = soup.select("table.screener_table tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 8:
                continue
            # Finviz indices 表格：第0列=名称，第2列=涨跌%，第3列=价格
            name_text = cols[0].get_text(strip=True)
            chg_text = cols[2].get_text(strip=True).replace("%", "")
            price_text = cols[3].get_text(strip=True).replace(",", "")
            for y_sym, (cn_name, en_name) in INDEX_MAP.items():
                if en_name.lower() in name_text.lower() or cn_name in name_text:
                    try:
                        pct = float(chg_text)
                        price = float(price_text)
                        chg = price * pct / 100
                        arrow = "🟢" if pct > 0 else "🔴" if pct < 0 else "⚪"
                        results[y_sym] = {
                            "name": cn_name, "price": price,
                            "chg": chg, "pct": pct, "arrow": arrow
                        }
                    except ValueError:
                        continue
                    break
        return results
    except Exception:
        return {}

def get_macro_rates():
    """获取 NY Fed 宏观利率（SOFR/EFFR/OBFR 等）"""
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    try:
        r = requests.get(NYFED_RATES_URL, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json().get("refRates", [])
        if data:
            results = {}
            labels = {
                "SOFR": "SOFR(担保隔夜融资利率)",
                "EFFR": "EFFR(有效联邦基金利率)",
                "OBFR": "OBFR(银行隔夜融资利率)",
                "TGCR": "TGCR(三方一般抵押利率)",
                "BGCR": "BGCR(广泛一般抵押利率)",
            }
            for item in data:
                t = item.get("type", "")
                eff_date = item.get("effectiveDate", "")
                rate = item.get("percentRate") or item.get("average30day")
                if rate and t in labels:
                    try:
                        results[t] = {"label": labels[t], "rate": float(rate), "date": eff_date}
                    except (TypeError, ValueError):
                        continue
            return results
    except (requests.RequestException, ValueError):
        pass
    return {}

def get_treasury_yields():
    """获取 FRED 10Y 和 2Y 国债收益率"""
    today = datetime.now(timezone.utc).date().isoformat()
    results = {}
    for sid, label in [("DGS10", "10Y国债收益率"), ("DGS2", "2Y国债收益率")]:
        url = FRED_URL_TMPL.format(sid=sid, date=today)
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            lines = [line for line in r.text.strip().split("\n") if line]
            for row in reversed(lines[1:]):
                last = row.split(",")
                if len(last) == 2 and last[1] not in (".", ""):
                    results[sid] = {"label": label, "rate": float(last[1]), "date": last[0]}
                    break
        except (requests.RequestException, ValueError):
            pass
    return results

def print_results():
    indices = ["^GSPC", "^DJI", "^IXIC", "^VIX"]
    futures = ["NQ=F", "ES=F", "YM=F"]
    commodities = ["GC=F", "CL=F", "SI=F"]

    print("\n=== 📊 美股主要指数 ===")
    for sym in indices:
        r = QUOTES.get(sym)
        if r:
            print(f"{r['arrow']} {r['name']:10s} {r['price']:>10.2f}  {r['chg']:>+8.2f}({r['pct']:>+6.2f}%)")

    print("\n=== 📈 期货 ===")
    for sym in futures:
        r = QUOTES.get(sym)
        if r:
            print(f"{r['arrow']} {r['name']:10s} {r['price']:>10.2f}  {r['chg']:>+8.2f}({r['pct']:>+6.2f}%)")

    print("\n=== 🛢️ 大宗商品 ===")
    for sym in commodities:
        r = QUOTES.get(sym)
        if r:
            print(f"{r['arrow']} {r['name']:10s} {r['price']:>10.2f}  {r['chg']:>+8.2f}({r['pct']:>+6.2f}%)")

    # 宏观利率
    print("\n=== 🏛️ 宏观利率 ===")
    rates = MACRO.get("rates", {})
    if rates:
        for t, v in rates.items():
            print(f"  📌 {v['label']}: {v['rate']:.3f}% ( {v['date']})")
    else:
        print("  (NY Fed rates unavailable)")

    # 国债收益率
    treasuries = MACRO.get("treasuries", {})
    if treasuries:
        for t, v in treasuries.items():
            print(f"  📌 {v['label']}: {v['rate']:.3f}% ( {v['date']})")
    else:
        print("  (Treasury yields unavailable)")

if __name__ == "__main__":
    print("正在获取美股数据...")
    QUOTES = get_all_quotes()
    MACRO = {"rates": get_macro_rates(), "treasuries": get_treasury_yields()}
    print_results()
