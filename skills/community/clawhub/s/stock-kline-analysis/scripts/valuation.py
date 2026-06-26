"""
valuation.py — Step 5: Fetch valuation and financial data for an A-share symbol.

NOTE: ak.stock_a_lg_indicator / ak.stock_a_indicator_lg do NOT exist in the
current AkShare version. Use stock_yjbb_em and stock_financial_analysis_indicator.

Usage:
    from valuation import fetch_valuation
    val = fetch_valuation("000063")
    print(val)
"""

from __future__ import annotations

import akshare as ak
from datetime import date
import pandas as pd


def _latest_quarter_end() -> str:
    """Return the most recent published quarter-end date as YYYYMMDD string."""
    today_s = date.today().strftime("%Y%m%d")
    # Walk forward through candidate quarter-ends for the past 2 years
    candidates = []
    for year in range(date.today().year - 1, date.today().year + 1):
        for q in ("0331", "0630", "0930", "1231"):
            candidates.append(f"{year}{q}")
    return max(d for d in candidates if d <= today_s)


def fetch_valuation(code: str) -> dict:
    """
    Fetch latest EPS/revenue/profit, compute PE/PB, and pull ROE/margin history.

    Returns a dict with keys:
        eps, revenue, revenue_yoy, net_profit, net_profit_yoy,
        book_value_per_share, roe, gross_margin, industry,
        report_date, pe_ttm, pb,
        fin_df (DataFrame of historical ratios, may be None)
    """
    result: dict = {}

    # ── ① Latest earnings summary ────────────────────────────────────────────
    quarter_end = _latest_quarter_end()
    try:
        yjbb = ak.stock_yjbb_em(date=quarter_end)
        row = yjbb[yjbb["股票代码"] == code]
        if row.empty:
            print(f"[valuation] {code} not found in yjbb for {quarter_end}")
        else:
            r = row.iloc[0]
            result["eps"]             = r.get("每股收益")
            result["revenue"]         = r.get("营业总收入-营业总收入")
            result["revenue_yoy"]     = r.get("营业总收入-同比增长")
            result["net_profit"]      = r.get("净利润-净利润")
            result["net_profit_yoy"]  = r.get("净利润-同比增长")
            result["book_value_per_share"] = r.get("每股净资产")
            result["roe"]             = r.get("净资产收益率")
            result["gross_margin"]    = r.get("销售毛利率")
            result["industry"]        = r.get("所处行业")
            result["report_date"]     = r.get("最新公告日期")
    except Exception as e:
        print(f"[valuation] stock_yjbb_em failed: {e}")

    # ── ② Derive PE (TTM) and PB from last close ─────────────────────────────
    # Caller should pass last_close; we leave these as None here and let
    # run_analysis.py compute them after fetching the price.
    result["pe_ttm"] = None  # computed in run_analysis: last_close / eps
    result["pb"]     = None  # computed in run_analysis: last_close / book_value_per_share

    # ── ③ Historical financial ratios ────────────────────────────────────────
    try:
        start_year = str(date.today().year - 3)
        fin = ak.stock_financial_analysis_indicator(symbol=code, start_year=start_year)
        # Keep only the most useful columns
        keep = [
            "日期",
            "净资产收益率(%)",
            "销售净利率(%)",
            "资产负债率(%)",
            "净利润增长率(%)",
            "主营业务收入增长率(%)",
            "销售毛利率(%)",
        ]
        available = [c for c in keep if c in fin.columns]
        result["fin_df"] = fin[available].sort_values("日期").tail(8)
    except Exception as e:
        print(f"[valuation] stock_financial_analysis_indicator failed: {e}")
        result["fin_df"] = None

    return result


def compute_pe_pb(result: dict, last_close: float) -> dict:
    """Inject PE (TTM) and PB once last_close is known."""
    eps = result.get("eps")
    bvps = result.get("book_value_per_share")
    result["pe_ttm"] = round(last_close / eps, 1) if eps and eps > 0 else None
    result["pb"]     = round(last_close / bvps, 2) if bvps and bvps > 0 else None
    return result


# ── Quick smoke-test ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    symbol = sys.argv[1] if len(sys.argv) > 1 else "000063"
    val = fetch_valuation(symbol)
    val = compute_pe_pb(val, last_close=float(sys.argv[2]) if len(sys.argv) > 2 else 37.12)
    for k, v in val.items():
        if k != "fin_df":
            print(f"  {k}: {v}")
    if val.get("fin_df") is not None:
        print("\nHistorical ratios:")
        print(val["fin_df"].to_string(index=False))
