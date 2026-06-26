#!/usr/bin/env python3
"""
Fetch market data for a given stock ticker using yfinance.
Outputs a comprehensive JSON file with price history, financial statements, and key metrics.

Usage: python fetch_market_data.py TICKER [--output OUTPUT_DIR]
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import yfinance as yf


def fetch_data(ticker: str) -> dict:
    """Fetch comprehensive market data for a ticker."""
    stock = yf.Ticker(ticker)
    result = {"ticker": ticker, "fetched_at": datetime.now().isoformat(), "errors": []}

    # Basic info
    try:
        info = stock.info
        result["info"] = {
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap"),
            "enterprise_value": info.get("enterpriseValue"),
            "currency": info.get("currency", "USD"),
            "exchange": info.get("exchange", "N/A"),
            "website": info.get("website", "N/A"),
            "summary": info.get("longBusinessSummary", "N/A")[:500],
        }
        result["valuation"] = {
            "pe_trailing": info.get("trailingPE"),
            "pe_forward": info.get("forwardPE"),
            "peg_ratio": info.get("pegRatio"),
            "price_to_book": info.get("priceToBook"),
            "price_to_sales": info.get("priceToSalesTrailing12Months"),
            "ev_to_ebitda": info.get("enterpriseToEbitda"),
            "ev_to_revenue": info.get("enterpriseToRevenue"),
        }
        result["dividends"] = {
            "dividend_yield": info.get("dividendYield"),
            "dividend_rate": info.get("dividendRate"),
            "payout_ratio": info.get("payoutRatio"),
            "ex_dividend_date": info.get("exDividendDate"),
        }
        result["profitability"] = {
            "profit_margin": info.get("profitMargins"),
            "operating_margin": info.get("operatingMargins"),
            "gross_margin": info.get("grossMargins"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
        }
        result["growth"] = {
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "earnings_quarterly_growth": info.get("earningsQuarterlyGrowth"),
        }
        result["financial_health"] = {
            "total_debt": info.get("totalDebt"),
            "total_cash": info.get("totalCash"),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),
            "free_cash_flow": info.get("freeCashflow"),
            "operating_cash_flow": info.get("operatingCashflow"),
        }
        result["targets"] = {
            "target_high": info.get("targetHighPrice"),
            "target_low": info.get("targetLowPrice"),
            "target_mean": info.get("targetMeanPrice"),
            "target_median": info.get("targetMedianPrice"),
            "recommendation": info.get("recommendationKey"),
            "recommendation_mean": info.get("recommendationMean"),
            "number_of_analysts": info.get("numberOfAnalystOpinions"),
        }
    except Exception as e:
        result["errors"].append(f"Failed to fetch info: {e}")

    # Price history (6 months daily)
    try:
        hist = stock.history(period="6mo", interval="1d")
        if not hist.empty:
            recent = hist.tail(60)  # Last ~60 trading days
            result["price_history"] = {
                "current_price": float(hist["Close"].iloc[-1]),
                "previous_close": float(hist["Close"].iloc[-2])
                if len(hist) > 1
                else None,
                "daily_change_pct": float(
                    (hist["Close"].iloc[-1] / hist["Close"].iloc[-2] - 1) * 100
                )
                if len(hist) > 1
                else None,
                "week_high": float(recent.tail(5)["High"].max()),
                "week_low": float(recent.tail(5)["Low"].min()),
                "month_high": float(recent.tail(22)["High"].max()),
                "month_low": float(recent.tail(22)["Low"].min()),
                "avg_volume_20d": int(recent.tail(20)["Volume"].mean()),
                "last_volume": int(hist["Volume"].iloc[-1]),
                "price_data": [
                    {
                        "date": idx.strftime("%Y-%m-%d"),
                        "open": round(float(row["Open"]), 2),
                        "high": round(float(row["High"]), 2),
                        "low": round(float(row["Low"]), 2),
                        "close": round(float(row["Close"]), 2),
                        "volume": int(row["Volume"]),
                    }
                    for idx, row in recent.iterrows()
                ],
            }
            # 52-week data
            hist_1y = stock.history(period="1y", interval="1d")
            if not hist_1y.empty:
                result["price_history"]["week_52_high"] = float(hist_1y["High"].max())
                result["price_history"]["week_52_low"] = float(hist_1y["Low"].min())
    except Exception as e:
        result["errors"].append(f"Failed to fetch price history: {e}")

    # Income statement
    try:
        income = stock.income_stmt
        if income is not None and not income.empty:
            result["income_statement"] = {}
            for col in income.columns[:4]:  # Last 4 periods
                period = (
                    col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)
                )
                result["income_statement"][period] = {
                    k: float(v) if v == v else None  # NaN check
                    for k, v in income[col].items()
                }
    except Exception as e:
        result["errors"].append(f"Failed to fetch income statement: {e}")

    # Balance sheet
    try:
        balance = stock.balance_sheet
        if balance is not None and not balance.empty:
            result["balance_sheet"] = {}
            for col in balance.columns[:4]:
                period = (
                    col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)
                )
                result["balance_sheet"][period] = {
                    k: float(v) if v == v else None for k, v in balance[col].items()
                }
    except Exception as e:
        result["errors"].append(f"Failed to fetch balance sheet: {e}")

    # Cash flow
    try:
        cashflow = stock.cashflow
        if cashflow is not None and not cashflow.empty:
            result["cash_flow"] = {}
            for col in cashflow.columns[:4]:
                period = (
                    col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)
                )
                result["cash_flow"][period] = {
                    k: float(v) if v == v else None for k, v in cashflow[col].items()
                }
    except Exception as e:
        result["errors"].append(f"Failed to fetch cash flow: {e}")

    # Institutional holders
    try:
        holders = stock.institutional_holders
        if holders is not None and not holders.empty:
            result["top_institutional_holders"] = holders.head(10).to_dict(
                orient="records"
            )
    except Exception:
        pass

    # Insider transactions
    try:
        insiders = stock.insider_transactions
        if insiders is not None and not insiders.empty:
            result["recent_insider_transactions"] = insiders.head(10).to_dict(
                orient="records"
            )
    except Exception:
        pass

    return result


def main():
    parser = argparse.ArgumentParser(description="Fetch market data for a stock ticker")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., NVDA, AAPL)")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    args = parser.parse_args()

    ticker = args.ticker.upper()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching market data for {ticker}...")
    data = fetch_data(ticker)

    output_file = output_dir / f"{ticker}_market_data.json"
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"Data saved to {output_file}")
    if data["errors"]:
        print(f"Warnings: {', '.join(data['errors'])}")

    # Print summary
    if "price_history" in data:
        ph = data["price_history"]
        print(f"\nCurrent Price: ${ph.get('current_price', 'N/A')}")
        print(f"Daily Change: {ph.get('daily_change_pct', 'N/A'):.2f}%")
    if "valuation" in data:
        v = data["valuation"]
        print(f"P/E (trailing): {v.get('pe_trailing', 'N/A')}")
        print(f"P/E (forward): {v.get('pe_forward', 'N/A')}")


if __name__ == "__main__":
    main()
