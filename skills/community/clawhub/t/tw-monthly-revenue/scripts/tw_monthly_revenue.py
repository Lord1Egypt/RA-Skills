#!/usr/bin/env python3
"""
台股月營收抓取腳本 — 使用 FinMind 免費 API
資料來源：https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockMonthRevenue

用法：
  python3 tw_monthly_revenue.py           # 自動抓上個月
  python3 tw_monthly_revenue.py 2026-03   # 指定月份

輸出 JSON（revenue 單位：新台幣元）
"""

import sys, json, datetime, urllib.request, urllib.parse, time

# ── 追蹤標的 ──────────────────────────────────────────────────
WATCHLIST = {
    "2337": "旺宏",
    "4763": "材料-KY",
    "1301": "台塑",
    "1303": "南亞",
    "1326": "台化",
}

# ── 信號閾值 ──────────────────────────────────────────────────
BEAT_YOY  =  10.0   # YoY >= +10% → BEAT
MISS_YOY  = -10.0   # YoY <= -10% → MISS

FINMIND_BASE = "https://api.finmindtrade.com/api/v4/data"
FINMIND_TOKEN = ""   # 免費版不需 token

# ── 工具函式 ──────────────────────────────────────────────────
def get_target_month(arg=None):
    """回傳 (year, month) 的目標月份（預設：上個月）"""
    if arg:
        parts = arg.split("-")
        return int(parts[0]), int(parts[1])
    today = datetime.date.today()
    first = today.replace(day=1)
    last = first - datetime.timedelta(days=1)
    return last.year, last.month

def fetch_finmind(stock_id, start_date="2025-01-01"):
    """抓取 FinMind 月營收資料，回傳 list of dict"""
    params = {
        "dataset": "TaiwanStockMonthRevenue",
        "data_id": stock_id,
        "start_date": start_date,
        "token": FINMIND_TOKEN,
    }
    url = FINMIND_BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            d = json.loads(resp.read().decode("utf-8"))
        if d.get("status") != 200:
            return None, d.get("msg", "API error")
        return d.get("data", []), None
    except Exception as e:
        return None, str(e)

def find_revenue(data, year, month):
    """在資料列表中找特定年月的營收"""
    for row in data:
        if row.get("revenue_year") == year and row.get("revenue_month") == month:
            return row.get("revenue")
    return None

def calc_cumulative_yoy(data, year, month):
    """計算 1~N 月累計年增率"""
    cum_cur = sum(
        r["revenue"] for r in data
        if r["revenue_year"] == year and r["revenue_month"] <= month
    )
    cum_ly = sum(
        r["revenue"] for r in data
        if r["revenue_year"] == year - 1 and r["revenue_month"] <= month
    )
    if cum_ly and cum_ly > 0:
        return round((cum_cur - cum_ly) / cum_ly * 100, 1)
    return None

# ── 主程式 ───────────────────────────────────────────────────
def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    target_year, target_month = get_target_month(arg)
    period = f"{target_year}-{target_month:02d}"

    # 抓取從去年同月起算的資料（多抓一年確保有 YoY 基準）
    start_date = f"{target_year - 1}-01-01"

    results = {"period": period, "stocks": {}, "summary": {"beat": [], "miss": [], "neutral": []}}

    for stock_id, name in WATCHLIST.items():
        time.sleep(0.8)  # 友善請求間隔
        data, err = fetch_finmind(stock_id, start_date)

        if err or data is None:
            results["stocks"][stock_id] = {
                "name": name, "signal": "DATA_UNAVAILABLE", "note": str(err)
            }
            continue

        # 當月、上月、去年同月
        rev_m  = find_revenue(data, target_year, target_month)
        # 上月
        pm_year, pm_month = (target_year, target_month - 1) if target_month > 1 else (target_year - 1, 12)
        rev_m1 = find_revenue(data, pm_year, pm_month)
        rev_ly = find_revenue(data, target_year - 1, target_month)

        # 累計年增率
        cum_yoy = calc_cumulative_yoy(data, target_year, target_month)

        # YoY / MoM
        yoy = round((rev_m - rev_ly) / rev_ly * 100, 1) if rev_m and rev_ly else None
        mom = round((rev_m - rev_m1) / rev_m1 * 100, 1) if rev_m and rev_m1 else None

        # 信號判斷
        if yoy is not None:
            signal = "BEAT" if yoy >= BEAT_YOY else ("MISS" if yoy <= MISS_YOY else "NEUTRAL")
        else:
            signal = "NO_DATA"

        entry = {
            "name": name,
            "revenue_m":  rev_m,
            "revenue_m1": rev_m1,
            "revenue_ly": rev_ly,
            "yoy_pct": yoy,
            "mom_pct": mom,
            "cumulative_yoy": cum_yoy,
            "signal": signal,
        }
        results["stocks"][stock_id] = entry

        # 彙整 summary
        if signal == "BEAT":
            results["summary"]["beat"].append(f"{name}({stock_id}) YoY+{yoy}%")
        elif signal == "MISS":
            results["summary"]["miss"].append(f"{name}({stock_id}) YoY{yoy}%")
        else:
            results["summary"]["neutral"].append(f"{name}({stock_id}) YoY{yoy}%")

    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
