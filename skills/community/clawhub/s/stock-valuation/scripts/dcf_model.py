#!/usr/bin/env python3
"""10-year DCF model with terminal value. Bear/base/bull scenarios."""
import argparse
import json
import sys


def run_dcf(fcf, growth_rate, wacc, terminal_growth, years=10):
    """Run a single DCF scenario. Returns projected FCFs, terminal value, and intrinsic value."""
    projected = []
    current_fcf = fcf
    for year in range(1, years + 1):
        current_fcf *= (1 + growth_rate)
        pv = current_fcf / ((1 + wacc) ** year)
        projected.append({
            "year": year,
            "fcf": round(current_fcf, 0),
            "pv_fcf": round(pv, 0),
        })

    # Terminal value using Gordon Growth Model
    terminal_fcf = projected[-1]["fcf"] * (1 + terminal_growth)
    terminal_value = terminal_fcf / (wacc - terminal_growth)
    pv_terminal = terminal_value / ((1 + wacc) ** years)

    total_pv_fcf = sum(p["pv_fcf"] for p in projected)
    enterprise_value = total_pv_fcf + pv_terminal

    return {
        "growth_rate": round(growth_rate * 100, 2),
        "wacc": round(wacc * 100, 2),
        "terminal_growth": round(terminal_growth * 100, 2),
        "projected_fcf": projected,
        "terminal_value": round(terminal_value, 0),
        "pv_terminal_value": round(pv_terminal, 0),
        "total_pv_fcf": round(total_pv_fcf, 0),
        "enterprise_value": round(enterprise_value, 0),
    }


def main():
    parser = argparse.ArgumentParser(description="10-year DCF model with bear/base/bull scenarios.")
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--wacc", type=float, default=0.10, help="Weighted avg cost of capital (default: 0.10)")
    parser.add_argument("--growth-high", type=float, default=None, help="Bull case growth rate")
    parser.add_argument("--growth-base", type=float, default=None, help="Base case growth rate")
    parser.add_argument("--growth-low", type=float, default=None, help="Bear case growth rate")
    parser.add_argument("--terminal", type=float, default=0.03, help="Terminal growth rate (default: 0.03)")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run with: uv run --with yfinance", file=sys.stderr)
        sys.exit(1)

    ticker = args.ticker.upper()
    t = yf.Ticker(ticker)
    info = t.info

    # Get FCF
    fcf = info.get("freeCashflow")
    if fcf is None:
        # Try from cash flow statement
        cf = t.quarterly_cashflow
        if cf is not None and not cf.empty:
            for label in ["Free Cash Flow", "FreeCashFlow"]:
                if label in cf.index:
                    # Sum last 4 quarters for TTM
                    vals = cf.loc[label].dropna().head(4)
                    fcf = float(vals.sum())
                    break
    if fcf is None or fcf <= 0:
        print(json.dumps({"error": f"No positive FCF found for {ticker}. FCF={fcf}"}))
        sys.exit(1)

    shares = info.get("sharesOutstanding")
    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    market_cap = info.get("marketCap")
    total_debt = info.get("totalDebt", 0) or 0
    total_cash = info.get("totalCash", 0) or 0

    # Estimate historical growth from revenue if not provided
    revenue_growth = info.get("revenueGrowth")
    if revenue_growth is None:
        revenue_growth = 0.08  # fallback

    growth_base = args.growth_base if args.growth_base is not None else round(revenue_growth, 4)
    growth_high = args.growth_high if args.growth_high is not None else round(growth_base * 1.5, 4)
    growth_low = args.growth_low if args.growth_low is not None else round(growth_base * 0.5, 4)

    scenarios = {}
    for name, rate in [("bear", growth_low), ("base", growth_base), ("bull", growth_high)]:
        scenario = run_dcf(fcf, rate, args.wacc, args.terminal)

        ev = scenario["enterprise_value"]
        equity_value = ev - total_debt + total_cash
        per_share = equity_value / shares if shares else None

        scenario["equity_value"] = round(equity_value, 0)
        scenario["per_share_value"] = round(per_share, 2) if per_share else None
        scenario["upside_pct"] = round((per_share / current_price - 1) * 100, 2) if per_share and current_price else None
        # Drop verbose projected_fcf from output to keep it concise
        scenario.pop("projected_fcf", None)
        scenarios[name] = scenario

    result = {
        "ticker": ticker,
        "current_price": current_price,
        "market_cap": market_cap,
        "ttm_fcf": round(fcf, 0),
        "shares_outstanding": shares,
        "total_debt": total_debt,
        "total_cash": total_cash,
        "wacc": round(args.wacc * 100, 2),
        "terminal_growth": round(args.terminal * 100, 2),
        "scenarios": scenarios,
    }

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
