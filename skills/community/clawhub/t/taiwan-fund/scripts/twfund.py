#!/usr/bin/env python3
"""
Taiwan Fund CLI — query NAV, compare funds, search, watchlist.

Usage:
    python3 twfund.py nav A09022                   # 查淨值（含匯率換算）
    python3 twfund.py compare A36004 A09022        # 比較多檔基金
    python3 twfund.py compare --all                # 比較追蹤中全部基金
    python3 twfund.py compare A36004 --with 00981A.TW ^TWII  # 跟指數/ETF比較
    python3 twfund.py search "關鍵字"               # 搜尋基金（鉅亨網）
    python3 twfund.py watchlist                    # 列出追蹤清單
    python3 twfund.py rate USD                     # 查匯率
    python3 twfund.py cnyes A36004                 # 產鉅亨 URL
    python3 twfund.py tdcc-init                    # 快取 TDCC 境外基金資料
"""

import json, os, re, sys, time
import urllib.parse
import urllib.request

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODES_FILE = os.path.join(SKILL_DIR, "fund_codes.json")
CNYES_BASE = "https://invest.cnyes.com/funds/detail"
TDCC_CACHE = os.path.expanduser("~/.openclaw/cache/taiwan-fund/tdcc_nav.json")
TDCC_TTL = 43200  # 12 h

# ═══════════════════════════════════════════════════════════════════
#  Exchange rate (30-min cache)
# ═══════════════════════════════════════════════════════════════════

_rate_cache = {"ts": 0, "data": None}

CURRENCY_NAMES = {
    "TWD": "台幣", "USD": "美元", "EUR": "歐元", "JPY": "日圓",
    "GBP": "英鎊", "AUD": "澳幣", "ZAR": "南非幣", "CNY": "人民幣",
    "SGD": "新加坡幣", "HKD": "港幣", "KRW": "韓元", "NZD": "紐幣",
    "CHF": "瑞士法郎", "SEK": "瑞典克朗",
}


def load_codes():
    with open(CODES_FILE) as f:
        return json.load(f)


def get_rates():
    now = time.time()
    if now - _rate_cache["ts"] < 1800 and _rate_cache["data"]:
        return _rate_cache["data"]
    try:
        req = urllib.request.Request(
            "https://open.er-api.com/v6/latest/USD",
            headers={"User-Agent": "twfund/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
        if d.get("result") == "success":
            _rate_cache["data"] = d["rates"]
            _rate_cache["ts"] = now
            return d["rates"]
    except Exception as e:
        print(f"⚠️  匯率 API 讀取失敗: {e}", file=sys.stderr)
    return None


def twd_per_unit(currency, rates):
    if currency == "TWD" or not rates:
        return 1.0
    t = rates.get("TWD", 31.5)
    c = rates.get(currency)
    return None if c is None else t / c


def convert_to_twd(amount, currency, rates):
    r = twd_per_unit(currency, rates)
    return None if r is None else amount * r


# ═══════════════════════════════════════════════════════════════════
#  Formatting
# ═══════════════════════════════════════════════════════════════════

def fmt_cur(amount, currency="TWD"):
    return {
        "JPY": f"¥{amount:,.0f}",
        "KRW": f"₩{amount:,.0f}",
        "TWD": f"NT${amount:,.2f}",
        "USD": f"${amount:,.2f}",
    }.get(currency, f"{amount:,.4f} {currency}")


def fmt_twd(amount):
    return f"NT${amount:,.2f}"


def fmt_pct(v):
    return f"{v:+.2f}%" if v is not None else "N/A"


def fmt_date(ts):
    if not ts:
        return "-"
    return time.strftime("%Y/%m/%d", time.gmtime(ts))


# ═══════════════════════════════════════════════════════════════════
#  cnyes — __NEXT_DATA__ parser (境內基金)
# ═══════════════════════════════════════════════════════════════════

_NEXT_RE = re.compile(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)


def fetch_fund_cnyes(code):
    """Fetch fund NAV + returns from cnyes __NEXT_DATA__ overview page.
    Returns dict or None."""
    codes = load_codes()
    info = codes.get(code)
    if not info:
        return None
    name = info["name"]

    url = f"{CNYES_BASE}/{urllib.parse.quote(name, safe='')}/{code}/overview"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8")
    except Exception:
        return None

    m = _NEXT_RE.search(html)
    if not m:
        return None
    try:
        payload = json.loads(m.group(1))
        fund = payload["props"]["pageProps"]["initialState"]["fundOverviewById"][code]["items"]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError):
        return None

    return {
        "source": "cnyes",
        "nav": fund.get("nav"),
        "change": fund.get("change"),
        "change_pct": fund.get("changePercent"),
        "date": fmt_date(fund.get("priceDate")),
        "returns": {
            "1M": fund.get("return1Month"),
            "3M": fund.get("return3Month"),
            "1Y": fund.get("return1Year"),
        },
        "currency": fund.get("classCurrency", "TWD"),
        "net_asset_b": fund.get("netAsset", 0) / 1e8,
        "mgmt_fee": fund.get("managementFee"),
        "star": fund.get("starRating"),
        "category": fund.get("categoryAbbr", ""),
        "cat_rankings": fund.get("categoryRankings", {}),
    }


# ═══════════════════════════════════════════════════════════════════
#  TDCC OpenAPI — 境外基金 (offshore funds, ISIN-based)
# ═══════════════════════════════════════════════════════════════════

_TDCC_DATA = {"ts": 0, "idx": None}  # runtime cache


def ensure_tdcc():
    """Load TDCC offshore fund NAV index, cached to disk (12h TTL).
    Returns dict {ISIN: {nav, date, currency, name}} or None."""
    now = time.time()

    # runtime cache fresh?
    if _TDCC_DATA["idx"] and now - _TDCC_DATA["ts"] < TDCC_TTL:
        return _TDCC_DATA["idx"]

    # disk cache fresh?
    if os.path.exists(TDCC_CACHE) and now - os.path.getmtime(TDCC_CACHE) < TDCC_TTL:
        with open(TDCC_CACHE) as f:
            _TDCC_DATA["idx"] = json.load(f)
            _TDCC_DATA["ts"] = now
            return _TDCC_DATA["idx"]

    # download
    print("📥 下載 TDCC 境外基金淨值資料（~8MB，後續快取）…", file=sys.stderr)
    url = "https://openapi-t.tdcc.com.tw/v1/opendata/3-4"
    req = urllib.request.Request(url, headers={"User-Agent": "twfund/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            records = json.loads(r.read())
    except Exception as e:
        print(f"⚠️  TDCC 下載失敗: {e}", file=sys.stderr)
        # stale disk fallback
        if os.path.exists(TDCC_CACHE):
            with open(TDCC_CACHE) as f:
                _TDCC_DATA["idx"] = json.load(f)
                _TDCC_DATA["ts"] = now
                return _TDCC_DATA["idx"]
        _TDCC_DATA["idx"] = {}
        return _TDCC_DATA["idx"]

    # index by ISIN
    idx = {}
    for rec in records:
        isin = rec.get("ISINCODE", "").strip()
        if isin:
            idx[isin] = {
                "nav": rec.get("基金淨值(金額)", "0"),
                "date": rec.get("日期", ""),
                "currency": rec.get("計價幣別", ""),
                "name": rec.get("基金名稱", ""),
            }

    os.makedirs(os.path.dirname(TDCC_CACHE), exist_ok=True)
    with open(TDCC_CACHE, "w") as f:
        json.dump(idx, f)

    _TDCC_DATA["idx"] = idx
    _TDCC_DATA["ts"] = now
    print(f"✅ TDCC 快取完成: {len(idx)} 檔境外基金", file=sys.stderr)
    return idx


def fetch_fund_tdcc(isin):
    """Lookup offshore fund nav by ISIN from TDCC cache."""
    idx = ensure_tdcc()
    rec = idx.get(isin)
    if not rec:
        return None
    return {
        "source": "tdcc",
        "nav": float(rec["nav"]) if rec["nav"].replace(".", "", 1).isdigit() else None,
        "change": None,
        "change_pct": None,
        "date": rec["date"],
        "returns": {},
        "currency": rec["currency"],
        "net_asset_b": None,
        "mgmt_fee": None,
        "star": None,
        "category": "境外",
        "cat_rankings": {},
    }


# ═══════════════════════════════════════════════════════════════════
#  Unified fund fetch: cnyes → TDCC fallback
# ═══════════════════════════════════════════════════════════════════

def fetch_fund(code):
    """Fetch fund data from cnyes first, fall back to TDCC if ISIN given."""
    codes = load_codes()
    info = codes.get(code)
    if not info:
        return None

    # cnyes first (domestic funds + offshore on cnyes)
    d = fetch_fund_cnyes(code)
    if d:
        return d

    # TDCC fallback (if ISIN in fund_codes.json)
    isin = info.get("isin", "")
    if isin:
        d = fetch_fund_tdcc(isin)
        if d:
            return d

    return None


# ═══════════════════════════════════════════════════════════════════
#  Yahoo Finance — historical performance (5y daily data)
# ═══════════════════════════════════════════════════════════════════

SYMBOL_ALIASES = {
    "^TWII": "^TWII", "加權指數": "^TWII", "大盤": "^TWII",
    "^TWO": "^TWO", "櫃買": "^TWO",
    "^GSPC": "^GSPC", "sp500": "^GSPC", "標普500": "^GSPC",
    "^IXIC": "^IXIC", "nasdaq": "^IXIC", "那斯達克": "^IXIC",
    "0050": "0050.TW", "台灣50": "0050.TW",
    "006208": "006208.TW", "富邦台50": "006208.TW",
}


def resolve_sym(s):
    return SYMBOL_ALIASES.get(s.upper(), s.strip())


def yahoo_perf(symbol):
    """Fetch 1M/3M/6M/1Y/3Y returns from Yahoo Finance chart API."""
    encoded = urllib.parse.quote(symbol, safe="")
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded}?range=5y&interval=1d"
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        result = data["chart"]["result"][0]
        adj = result["indicators"].get("adjclose")
        closes = (adj[0]["adjclose"] if adj and adj[0].get("adjclose")
                  else result["indicators"]["quote"][0]["close"])
        name = result["meta"].get("shortName") or result["meta"].get("symbol", symbol)
        current = closes[-1]
        periods = {"1M": 21, "3M": 63, "6M": 126, "1Y": 252, "3Y": 756}
        perf = {}
        for label, days in periods.items():
            idx = len(closes) - 1 - days
            perf[label] = (current / closes[idx] - 1) * 100 if idx >= 0 and closes[idx] else None
        return {"name": name, "symbol": symbol, "perf": perf, "error": None}
    except Exception as e:
        return {"name": symbol, "symbol": symbol, "perf": {}, "error": str(e)}


# ═══════════════════════════════════════════════════════════════════
#  Commands
# ═══════════════════════════════════════════════════════════════════

def cmd_nav(code):
    codes = load_codes()
    info = codes.get(code)
    if not info:
        print(f"❌ 找不到基金代碼 {code}\n   請先加入 {CODES_FILE}")
        return

    name = info["name"]
    currency = info.get("currency", "TWD")
    cur_label = CURRENCY_NAMES.get(currency, currency)
    cat = info.get("category", "")
    cnyes_url = f"{CNYES_BASE}/{urllib.parse.quote(name, safe='')}/{code}/"

    print(f"📡 {name}  ({code})")
    if cat:
        print(f"   🏷️  {cat}")
    print(f"   💰 計價幣別: {cur_label}")
    if info.get("isin"):
        print(f"   🔑 ISIN: {info['isin']}")
    print(f"\n🔗 鉅亨網: {cnyes_url}")

    d = fetch_fund(code)
    if not d:
        print("⚠️  暫時無法取得資料（cnyes 連線失敗）")
        print(f'\n💡 tavily_extract(url="{cnyes_url}overview", extract_depth="advanced")')
        return

    currency = d["currency"]
    cur_label = CURRENCY_NAMES.get(currency, currency)
    source_label = "TDCC" if d["source"] == "tdcc" else "cnyes"
    print(f"\n📊 最新淨值: {fmt_cur(d['nav'], currency)}  ({d['date']})  [{source_label}]")
    if d["change_pct"] is not None:
        print(f"   日漲跌: {d['change']:+.2f} ({d['change_pct']:+.2f}%)")

    if currency != "TWD":
        rates = get_rates()
        twd_val = convert_to_twd(d["nav"], currency, rates)
        unit_rate = twd_per_unit(currency, rates)
        if twd_val and unit_rate:
            print(f"   💱 台幣等值: {fmt_twd(twd_val)}  (匯率 1 {cur_label} = {fmt_twd(unit_rate)})")

    ret = d["returns"]
    if any(ret.get(k) for k in ("1M", "3M", "1Y")):
        print(f"\n📈 績效")
        parts = [f"{k}: {fmt_pct(ret[k])}" for k in ("1M", "3M", "1Y") if ret.get(k) is not None]
        if parts:
            print(f"   {' | '.join(parts)}")
        ranks = d.get("cat_rankings", {})
        if ranks:
            rp = [f"{k}: {v['surpassRate']}%" for k, v in list(ranks.items())[:5]]
            print(f"   🏆 同組排名: {', '.join(rp)}")

    detail = []
    if d["net_asset_b"]:
        detail.append(f"規模: {d['net_asset_b']:.1f}億")
    if d["mgmt_fee"] is not None:
        detail.append(f"管理費: {d['mgmt_fee']}%")
    if d["star"]:
        detail.append(f"★{d['star']}")
    if d.get("category"):
        detail.append(d["category"])
    if detail:
        print(f"   {' | '.join(detail)}")

    if d["source"] != "tdcc":
        print(f"\n💡 tavily_extract 可取得 6M/3Y/5Y 完整績效:")
        print(f'   tavily_extract(url="{cnyes_url}overview", extract_depth="advanced")')


def cmd_compare(fund_codes, with_symbols):
    codes_db = load_codes()
    rates = get_rates()
    periods = ["1M", "3M", "6M", "1Y", "3Y"]
    fund_rows = []

    # collect auto-benchmarks from fund config
    auto_benchmarks = set()
    for code in fund_codes:
        info = codes_db.get(code)
        if info and info.get("benchmark"):
            auto_benchmarks.add(info["benchmark"])

    for code in fund_codes:
        info = codes_db.get(code)
        if not info:
            print(f"⚠️  略過未知代碼 {code}")
            continue
        name = info["name"]
        currency = info.get("currency", "TWD")
        d = fetch_fund(code)
        fund_rows.append({
            "code": code, "name": name, "currency": currency,
            "cur_label": CURRENCY_NAMES.get(currency, currency),
            "data": d,
        })

    if not fund_rows:
        return

    # benchmarks / extra symbols from Yahoo
    bench_rows = []
    done = set()
    for sym in list(auto_benchmarks) + with_symbols:
        resolved = resolve_sym(sym)
        if resolved in done:
            continue
        done.add(resolved)
        bench_rows.append(yahoo_perf(resolved))

    title = f"📊 基金比較 ({len(fund_rows)} 檔)"
    if bench_rows:
        title += f" + {len(bench_rows)} 檔指數/ETF"
    print("\n" + title)
    print("=" * 80)

    for r in fund_rows:
        print(f"\n🔖 {r['code']}  {r['name']}")
        d = r["data"]
        if d:
            src = f"[{d['source']}]" if d["source"] else ""
            print(f"   淨值: {fmt_cur(d['nav'], r['currency'])}  ({d['date']}){src}")
            if d["change_pct"] is not None:
                print(f"   日漲跌: {d['change']:+.2f} ({d['change_pct']:+.2f}%)")
            if r["currency"] != "TWD":
                twd_val = convert_to_twd(d["nav"], r["currency"], rates)
                if twd_val:
                    print(f"   台幣等值: {fmt_twd(twd_val)}")

            ret = d["returns"]
            parts = [f"{k}: {fmt_pct(ret[k])}" for k in periods if ret.get(k) is not None]
            if parts:
                print(f"   績效: {' | '.join(parts)}")

            # excess vs benchmark
            info = codes_db.get(r["code"], {})
            if info.get("benchmark"):
                b_sym = resolve_sym(info["benchmark"])
                match = next((b for b in bench_rows if b["symbol"] == b_sym), None)
                if match and match["perf"] and any(ret.get(k) for k in periods):
                    xs = [f"{k}: {fmt_pct((ret.get(k) or 0) - (match['perf'].get(k) or 0))}"
                          for k in periods if ret.get(k) is not None and match["perf"].get(k) is not None]
                    if xs:
                        print(f"   📈 超越 {match['name']}: {' | '.join(xs)}")

            detail = []
            if d["net_asset_b"]:
                detail.append(f"規模: {d['net_asset_b']:.1f}億")
            if d["mgmt_fee"] is not None:
                detail.append(f"管理費: {d['mgmt_fee']}%")
            if d["star"]:
                detail.append(f"★{d['star']}")
            if d.get("category"):
                detail.append(d["category"])
            if detail:
                print(f"   {' | '.join(detail)}")
        else:
            print(f"   資料: ⚠️  暫無法取得")
            url = f"{CNYES_BASE}/{urllib.parse.quote(r['name'], safe='')}/{r['code']}/"
            print(f"   🔗 {url}")

    for b in bench_rows:
        name = b.get("name", b["symbol"])
        print(f"\n📈 {name}  ({b['symbol']})")
        if b.get("error"):
            print(f"   ⚠️  {b['error']}")
        elif b.get("perf"):
            parts = [f"{k}: {fmt_pct(b['perf'].get(k))}" for k in periods if b["perf"].get(k) is not None]
            if parts:
                print(f"   績效: {' | '.join(parts)}")

    # summary table
    table = []
    for r in fund_rows:
        if r["data"] and r["data"]["returns"]:
            table.append((r["name"] + " (" + r["code"] + ")", r["data"]["returns"]))
    for b in bench_rows:
        if b.get("perf"):
            table.append((b.get("name", b["symbol"]), b["perf"]))

    if len(table) >= 2:
        print("\n" + "─" * 80)
        print("📋 績效一覽")
        h = f"{'標的':<34}"
        for k in periods:
            h += f"  {k:>8}"
        print(h)
        print("─" * 80)
        for label, returns in table:
            label = label[:32] + "…" if len(label) > 33 else label
            row = f"{label:<34}"
            for k in periods:
                v = returns.get(k)
                row += f"  {fmt_pct(v):>8}" if v is not None else f"  {'N/A':>8}"
            print(row)
        print("─" * 80)

    print("\n💡 詳細持股/費用用 tavily_extract 爬鉅亨頁面")


def cmd_rate(cur):
    cur = cur.upper()
    rates = get_rates()
    if not rates:
        print("❌ 無法取得匯率資料")
        return
    if cur == "TWD":
        print("📊 台幣 (TWD) 為基準幣別")
        return
    label = CURRENCY_NAMES.get(cur, cur)
    if cur not in rates:
        print(f"❌ 不支援 {cur}\n   支援: {', '.join(sorted(CURRENCY_NAMES.keys()))}")
        return
    r = twd_per_unit(cur, rates)
    print(f"📊 匯率: {label} ({cur})")
    print(f"   1 {cur} = {fmt_twd(r)}")
    print(f"   1 TWD = {1/r:.6f} {cur}")


def cmd_tdcc_init():
    """Pre-cache TDCC data."""
    idx = ensure_tdcc()
    if idx:
        print(f"✅ TDCC 快取就緒: {len(idx)} 檔境外基金")
    else:
        print("❌ TDCC 快取失敗")


def cmd_cnyes(code):
    codes = load_codes()
    info = codes.get(code)
    if not info:
        print(f"❌ 找不到基金代碼 {code}")
        return
    print(f"{CNYES_BASE}/{urllib.parse.quote(info['name'], safe='')}/{code}/")


def cmd_search(keyword):
    url = f"https://fund.cnyes.com/search?fundName={urllib.parse.quote(keyword)}"
    print(f"🔍 搜尋: {keyword}\n🔗 {url}")
    print(f"\n💡 tavily_extract(url=\"{url}\")")


def cmd_watchlist():
    codes = load_codes()
    if not codes:
        print("📝 追蹤清單是空的\n   編輯 fund_codes.json 加入基金")
        return
    print(f"📝 追蹤基金 ({len(codes)} 檔)")
    print("=" * 50)
    for code, info in codes.items():
        name = info["name"]
        cur = info.get("currency", "TWD")
        cur_label = CURRENCY_NAMES.get(cur, cur)
        cat = info.get("category", "")
        tags = []
        if cur != "TWD":
            tags.append(cur_label)
        if cat:
            tags.append(cat)
        if info.get("benchmark"):
            tags.append(f"📈{info['benchmark']}")
        if info.get("isin"):
            tags.append(f"🔑ISIN")
        tag_s = f"  [{', '.join(tags)}]" if tags else ""
        print(f"\n🔖 {code} — {name}{tag_s}")

    keys = list(codes.keys())
    print(f"\n💡 查單檔: python3 twfund.py nav {keys[0]}")
    if len(keys) >= 2:
        print(f"💡 比較全部: python3 twfund.py compare " + " ".join(keys))


# ═══════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return

    cmd = sys.argv[1]

    if cmd == "nav" and len(sys.argv) >= 3:
        cmd_nav(sys.argv[2])
    elif cmd == "compare":
        if len(sys.argv) < 3:
            print("請指定至少一個代碼，或 compare --all [--with ...]")
            return
        fund_codes, with_symbols = [], []
        mode = "codes"
        for arg in sys.argv[2:]:
            if arg == "--with":
                mode = "with"
                continue
            (with_symbols if mode == "with" else fund_codes).append(arg)
        if not fund_codes:
            print("請指定基金代碼")
            return
        if fund_codes[0] == "--all":
            fund_codes = list(load_codes().keys())
            if not fund_codes:
                print("追蹤清單是空的")
                return
        cmd_compare(fund_codes, with_symbols)
    elif cmd == "tdcc-init":
        cmd_tdcc_init()
    elif cmd == "cnyes" and len(sys.argv) >= 3:
        cmd_cnyes(sys.argv[2])
    elif cmd == "search" and len(sys.argv) >= 3:
        cmd_search(" ".join(sys.argv[2:]))
    elif cmd == "rate":
        cmd_rate(sys.argv[2] if len(sys.argv) >= 3 else "USD")
    elif cmd == "watchlist":
        cmd_watchlist()
    else:
        print(f"未知指令: {cmd}\n" + __doc__.strip())


if __name__ == "__main__":
    main()
