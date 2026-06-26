#!/usr/bin/env python3
"""
A-Share Market Stock Data Fetcher
=================================
Fetch A-share stock fundamentals, price history, financial metrics,
and insider trading data using AKShare (no API key required).

Usage:
    python stock_data.py 600519                       # Basic info (Kweichow Moutai)
    python stock_data.py 600519 --metrics             # Full financial metrics
    python stock_data.py 600519 --history             # Price history
    python stock_data.py 600519 --financials          # Financial statements
    python stock_data.py 600519 --insider             # Insider trades
    python stock_data.py 600519 000858 --screen       # Screen with filters
"""
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.utils import output_json, safe_div, safe_float, error_exit


def _normalize_symbol(symbol: str) -> str:
    """Normalize A-share symbol to 6-digit format."""
    sym = symbol.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    return sym.zfill(6)


def _get_exchange_suffix(symbol: str) -> str:
    """Determine exchange from symbol prefix."""
    sym = _normalize_symbol(symbol)
    if sym.startswith(("6",)):
        return "sh"  # Shanghai
    elif sym.startswith(("0", "3")):
        return "sz"  # Shenzhen
    elif sym.startswith(("4", "8")):
        return "bj"  # Beijing Stock Exchange
    return "sh"


def fetch_basic_info(symbols: list[str]) -> list[dict]:
    """Fetch basic company info for A-share stocks."""
    import akshare as ak

    results = []
    for symbol in symbols:
        sym = _normalize_symbol(symbol)
        try:
            # Get real-time quote
            df = ak.stock_individual_info_em(symbol=sym)
            info = {}
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    key = str(row.iloc[0])
                    val = row.iloc[1]
                    info[key] = val

            results.append({
                "symbol": sym,
                "name": info.get("股票简称", ""),
                "industry": info.get("行业", ""),
                "market_cap": safe_float(info.get("总市值")),
                "circulating_cap": safe_float(info.get("流通市值")),
                "total_shares": safe_float(info.get("总股本")),
                "circulating_shares": safe_float(info.get("流通股")),
                "exchange": _get_exchange_suffix(sym),
                "listing_date": info.get("上市时间", ""),
            })
        except Exception as e:
            results.append({"symbol": sym, "error": str(e)})

    return results


def fetch_financial_metrics(symbol: str) -> dict:
    """
    Fetch comprehensive financial metrics for a single A-share stock.
    Uses AKShare to pull valuation, profitability, leverage, and growth data.
    """
    import akshare as ak

    sym = _normalize_symbol(symbol)

    result = {
        "symbol": sym,
        "name": "",
        "industry": "",
        "current_price": None,
        "market_cap": None,
    }

    # --- Basic info ---
    try:
        df_info = ak.stock_individual_info_em(symbol=sym)
        info = {}
        if df_info is not None and not df_info.empty:
            for _, row in df_info.iterrows():
                info[str(row.iloc[0])] = row.iloc[1]
        result["name"] = info.get("股票简称", "")
        result["industry"] = info.get("行业", "")
        result["market_cap"] = safe_float(info.get("总市值"))
    except Exception:
        pass

    # --- Real-time quote ---
    try:
        df_quote = ak.stock_zh_a_spot_em()
        if df_quote is not None and not df_quote.empty:
            row = df_quote[df_quote["代码"] == sym]
            if not row.empty:
                row = row.iloc[0]
                result["current_price"] = safe_float(row.get("最新价"))
                result["valuation"] = {
                    "pe_ttm": safe_float(row.get("市盈率-动态")),
                    "pb": safe_float(row.get("市净率")),
                    "total_market_cap": safe_float(row.get("总市值")),
                    "circulating_cap": safe_float(row.get("流通市值")),
                }
                result["trading"] = {
                    "change_pct": safe_float(row.get("涨跌幅")),
                    "turnover_rate": safe_float(row.get("换手率")),
                    "volume": safe_float(row.get("成交量")),
                    "amount": safe_float(row.get("成交额")),
                    "amplitude": safe_float(row.get("振幅")),
                }
    except Exception:
        pass

    # --- Financial indicators (profitability, leverage) ---
    try:
        df_fin = ak.stock_financial_abstract_ths(symbol=sym, indicator="按报告期")
        if df_fin is not None and not df_fin.empty:
            latest = df_fin.iloc[-1]
            result["profitability"] = {
                "roe": safe_float(latest.get("净资产收益率")),
                "gross_margin": safe_float(latest.get("销售毛利率")),
                "net_margin": safe_float(latest.get("销售净利率")),
            }
            result["leverage"] = {
                "debt_to_asset_ratio": safe_float(latest.get("资产负债率")),
                "current_ratio": safe_float(latest.get("流动比率")),
                "quick_ratio": safe_float(latest.get("速动比率")),
            }
            result["growth"] = {
                "revenue_growth_yoy": safe_float(latest.get("营业总收入同比增长率")),
                "profit_growth_yoy": safe_float(latest.get("净利润同比增长率")),
            }
            result["per_share"] = {
                "eps": safe_float(latest.get("基本每股收益")),
                "bvps": safe_float(latest.get("每股净资产")),
                "ocf_per_share": safe_float(latest.get("每股经营现金流")),
            }
    except Exception:
        pass

    # --- Dividend data ---
    try:
        df_div = ak.stock_history_dividend_detail(symbol=sym, indicator="分红")
        if df_div is not None and not df_div.empty:
            recent_divs = df_div.head(5)
            dividends = []
            for _, row in recent_divs.iterrows():
                dividends.append({
                    "report_date": str(row.get("公告日期", "")),
                    "dividend_per_share": safe_float(row.get("派息")),
                    "ex_date": str(row.get("除权除息日", "")),
                })
            result["dividends"] = dividends
    except Exception:
        result["dividends"] = []

    return result


def fetch_price_history(symbol: str, period: str = "1y",
                        adjust: str = "qfq") -> dict:
    """
    Fetch historical OHLCV data for an A-share stock.

    Args:
        symbol: A-share stock code (e.g., "600519")
        period: "1m", "3m", "6m", "1y", "2y", "5y", "max"
        adjust: "qfq" (forward-adjusted), "hfq" (backward-adjusted), "" (unadjusted)
    """
    import akshare as ak

    sym = _normalize_symbol(symbol)

    period_map = {
        "1m": 30, "3m": 90, "6m": 180, "1y": 365,
        "2y": 730, "5y": 1825, "max": 7300,
    }
    days = period_map.get(period, 365)
    start = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
    end = datetime.now().strftime("%Y%m%d")

    try:
        df = ak.stock_zh_a_hist(
            symbol=sym, period="daily",
            start_date=start, end_date=end,
            adjust=adjust
        )
    except Exception as e:
        return {"symbol": sym, "error": str(e)}

    if df is None or df.empty:
        return {"symbol": sym, "error": "No price data found"}

    records = []
    for _, row in df.iterrows():
        records.append({
            "date": str(row.get("日期", "")),
            "open": safe_float(row.get("开盘")),
            "high": safe_float(row.get("最高")),
            "low": safe_float(row.get("最低")),
            "close": safe_float(row.get("收盘")),
            "volume": safe_float(row.get("成交量")),
            "amount": safe_float(row.get("成交额")),
            "turnover_rate": safe_float(row.get("换手率")),
        })

    return {
        "symbol": sym,
        "period": period,
        "adjust": adjust,
        "data_points": len(records),
        "start_date": records[0]["date"] if records else "",
        "end_date": records[-1]["date"] if records else "",
        "prices": records,
    }


def fetch_financial_statements(symbol: str) -> dict:
    """Fetch income statement, balance sheet, and cash flow for A-share stocks."""
    import akshare as ak

    sym = _normalize_symbol(symbol)

    result = {"symbol": sym}

    # --- Income Statement ---
    try:
        df = ak.stock_financial_report_sina(stock=sym, symbol="利润表")
        if df is not None and not df.empty:
            records = []
            for col in df.columns[:5]:  # Last 5 periods
                period_data = {"period": str(col)}
                for idx in df.index:
                    val = safe_float(df.loc[idx, col])
                    period_data[str(idx)] = val
                records.append(period_data)
            result["income_statement"] = records
    except Exception:
        result["income_statement"] = []

    # --- Balance Sheet ---
    try:
        df = ak.stock_financial_report_sina(stock=sym, symbol="资产负债表")
        if df is not None and not df.empty:
            records = []
            for col in df.columns[:5]:
                period_data = {"period": str(col)}
                for idx in df.index:
                    val = safe_float(df.loc[idx, col])
                    period_data[str(idx)] = val
                records.append(period_data)
            result["balance_sheet"] = records
    except Exception:
        result["balance_sheet"] = []

    # --- Cash Flow Statement ---
    try:
        df = ak.stock_financial_report_sina(stock=sym, symbol="现金流量表")
        if df is not None and not df.empty:
            records = []
            for col in df.columns[:5]:
                period_data = {"period": str(col)}
                for idx in df.index:
                    val = safe_float(df.loc[idx, col])
                    period_data[str(idx)] = val
                records.append(period_data)
            result["cash_flow"] = records
    except Exception:
        result["cash_flow"] = []

    return result


def _get_exchange_prefix(symbol: str) -> str:
    """Return exchange prefix for insider trade filtering (e.g. 'SH688557')."""
    sym = _normalize_symbol(symbol)
    if sym.startswith("6"):
        return "SH" + sym
    elif sym.startswith(("0", "3")):
        return "SZ" + sym
    elif sym.startswith(("4", "8")):
        return "BJ" + sym
    return "SH" + sym


def fetch_insider_trades(symbol: str) -> dict:
    """Fetch insider trading (董监高增减持) data for an A-share stock."""
    import akshare as ak

    sym = _normalize_symbol(symbol)
    prefixed = _get_exchange_prefix(sym)

    try:
        df = ak.stock_inner_trade_xq()
        if df is None or df.empty:
            return {"symbol": sym, "transactions": [], "note": "No insider trades found"}

        # Filter for our target symbol
        df = df[df["股票代码"] == prefixed]
        if df.empty:
            return {"symbol": sym, "transactions": [], "note": "No insider trades found"}

        trades = []
        for _, row in df.iterrows():
            shares_changed = safe_float(row.get("变动股数"))
            if shares_changed is not None and shares_changed > 0:
                change_type = "增持"
            elif shares_changed is not None and shares_changed < 0:
                change_type = "减持"
            else:
                change_type = "未知"

            trades.append({
                "name": str(row.get("变动人", "")),
                "position": str(row.get("董监高职务", "")),
                "relationship": str(row.get("与董监高关系", "")),
                "change_type": change_type,
                "shares_changed": shares_changed,
                "price": safe_float(row.get("成交均价")),
                "shares_after": safe_float(row.get("变动后持股数")),
                "date": str(row.get("变动日期", "")),
            })

        buys = [t for t in trades if t["change_type"] == "增持"]
        sells = [t for t in trades if t["change_type"] == "减持"]

        return {
            "symbol": sym,
            "total_transactions": len(trades),
            "summary": {
                "total_purchases": len(buys),
                "total_sales": len(sells),
                "unique_buyers": len(set(t["name"] for t in buys)),
            },
            "transactions": trades,
        }
    except Exception as e:
        return {"symbol": sym, "error": str(e)}


def fetch_northbound_flow() -> dict:
    """Fetch northbound capital flow data (北向资金/沪深港通)."""
    import akshare as ak

    try:
        df = ak.stock_hsgt_north_net_flow_in_em(symbol="北向")
        if df is None or df.empty:
            return {"error": "No northbound flow data"}

        # Last 30 days
        records = []
        for _, row in df.tail(30).iterrows():
            records.append({
                "date": str(row.get("日期", "")),
                "net_inflow": safe_float(row.get("当日净流入")),
                "sh_connect": safe_float(row.get("沪股通净流入")),
                "sz_connect": safe_float(row.get("深股通净流入")),
            })

        return {
            "data_points": len(records),
            "flows": records,
        }
    except Exception as e:
        return {"error": str(e)}


def screen_stocks(symbols: list[str], filters: dict | None = None) -> dict:
    """
    Screen A-share stocks against financial filters.

    Default filters:
        max_pe: 30        (P/E below 30)
        max_pb: 5         (P/B below 5)
        min_roe: 8        (ROE above 8%)
        max_debt_ratio: 60 (Debt-to-asset ratio below 60%)
    """
    defaults = {
        "max_pe": 30.0,
        "max_pb": 5.0,
        "min_roe": 8.0,
        "max_debt_ratio": 60.0,
    }
    if filters:
        defaults.update(filters)

    passing = []
    failing = []

    for sym in symbols:
        try:
            m = fetch_financial_metrics(sym)
            if "error" in m:
                failing.append({"symbol": sym, "reason": m["error"]})
                continue

            reasons = []
            pe = (m.get("valuation") or {}).get("pe_ttm")
            if pe is not None and pe <= 0:
                reasons.append(f"PE {pe:.1f} 无效（为零或负值，通常表示亏损）")
            elif pe is not None and pe > defaults["max_pe"]:
                reasons.append(f"PE {pe:.1f} > {defaults['max_pe']:.1f}")

            pb = (m.get("valuation") or {}).get("pb")
            if pb is not None and pb > defaults["max_pb"]:
                reasons.append(f"PB {pb:.1f} > {defaults['max_pb']:.1f}")

            roe = (m.get("profitability") or {}).get("roe")
            if roe is not None and roe < defaults["min_roe"]:
                reasons.append(f"ROE {roe:.1f}% < {defaults['min_roe']:.1f}%")

            debt_ratio = (m.get("leverage") or {}).get("debt_to_asset_ratio")
            if debt_ratio is not None and debt_ratio > defaults["max_debt_ratio"]:
                reasons.append(
                    f"Debt ratio {debt_ratio:.1f}% > {defaults['max_debt_ratio']:.1f}%"
                )

            if reasons:
                failing.append({"symbol": sym, "reasons": reasons})
            else:
                passing.append(m)

        except Exception as e:
            failing.append({"symbol": sym, "reason": str(e)})

    return {
        "filters_applied": defaults,
        "total_screened": len(symbols),
        "passed": len(passing),
        "failed": len(failing),
        "results": passing,
        "rejected": failing,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="A-Share Stock Data Fetcher (AKShare, no API key)"
    )
    parser.add_argument("symbols", nargs="*", help="A-share stock code(s)")
    parser.add_argument("--metrics", action="store_true",
                        help="Full financial metrics")
    parser.add_argument("--history", action="store_true",
                        help="Price history")
    parser.add_argument("--financials", action="store_true",
                        help="Financial statements")
    parser.add_argument("--insider", action="store_true",
                        help="Insider trading data")
    parser.add_argument("--northbound", action="store_true",
                        help="Northbound capital flow")
    parser.add_argument("--screen", action="store_true",
                        help="Screen against default filters")
    parser.add_argument("--period", default="1y",
                        help="History period (1m,3m,6m,1y,2y,5y,max)")
    args = parser.parse_args()

    try:
        if args.northbound:
            data = fetch_northbound_flow()
        elif not args.symbols:
            error_exit("Please provide stock symbol(s) or use --northbound")
            return
        elif args.screen:
            data = screen_stocks(args.symbols)
        elif args.metrics:
            if len(args.symbols) == 1:
                data = fetch_financial_metrics(args.symbols[0])
            else:
                data = [fetch_financial_metrics(s) for s in args.symbols]
        elif args.history:
            data = fetch_price_history(args.symbols[0], period=args.period)
        elif args.financials:
            data = fetch_financial_statements(args.symbols[0])
        elif args.insider:
            data = fetch_insider_trades(args.symbols[0])
        else:
            data = fetch_basic_info(args.symbols)

        output_json(data)

    except ImportError:
        error_exit("akshare is required. Install: pip install akshare")
    except Exception as e:
        error_exit(f"Error fetching data: {e}")


if __name__ == "__main__":
    main()
