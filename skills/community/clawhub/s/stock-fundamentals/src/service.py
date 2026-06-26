# pyright: reportMissingImports=false

import yfinance as yf

from constants import (
    BALANCE_SHEET_CASH_LABELS,
    BALANCE_SHEET_DEBT_LABELS,
    CASHFLOW_FCF_LABELS,
    HIGHLIGHT_THRESHOLDS,
    INCOME_STATEMENT_NET_INCOME_LABELS,
    INCOME_STATEMENT_REVENUE_LABELS,
    METRIC_INFO_KEYS,
    WATCH_THRESHOLDS,
)
from utils import (
    extract_statement_value,
    format_event_date,
    format_large_number,
    format_number,
    format_percent,
    format_price_value,
    format_yield_percent,
    get_info_value,
    normalize_ratio_percent_value,
    normalize_recommendation,
    normalize_yield_percent_value,
)


def extract_next_earnings_date(calendar, info: dict):
    """Extract the next earnings date from calendar or quote metadata."""
    if isinstance(calendar, dict):
        earnings_date = calendar.get("Earnings Date")
        if isinstance(earnings_date, (list, tuple)) and earnings_date:
            earnings_date = earnings_date[0]
        if earnings_date:
            return format_event_date(earnings_date)

    earnings_timestamp = info.get("earningsTimestamp") or info.get(
        "earningsTimestampStart"
    )
    if earnings_timestamp:
        return format_event_date(earnings_timestamp)

    return "N/A"


def build_metrics(info: dict) -> dict:
    """Build the raw metrics dictionary from quote metadata."""
    return {
        metric_name: get_info_value(info, *keys)
        for metric_name, keys in METRIC_INFO_KEYS.items()
    }


def hydrate_metric_fallbacks(
    metrics: dict, info: dict, income_stmt, balance_sheet, cashflow
):
    """Fill missing metrics from statement data when possible."""
    if metrics["cash"] is None:
        metrics["cash"] = extract_statement_value(
            balance_sheet, BALANCE_SHEET_CASH_LABELS
        )
    if metrics["debt"] is None:
        metrics["debt"] = extract_statement_value(
            balance_sheet, BALANCE_SHEET_DEBT_LABELS
        )
    if metrics["free_cash_flow"] is None:
        metrics["free_cash_flow"] = extract_statement_value(
            cashflow, CASHFLOW_FCF_LABELS
        )
    if metrics["revenue_growth"] is None:
        metrics["revenue_growth"] = get_info_value(info, "earningsQuarterlyGrowth")
    if metrics["profit_margin"] is None:
        net_income = extract_statement_value(
            income_stmt, INCOME_STATEMENT_NET_INCOME_LABELS
        )
        total_revenue = extract_statement_value(
            income_stmt, INCOME_STATEMENT_REVENUE_LABELS
        )
        if net_income is not None and total_revenue not in (None, 0):
            metrics["profit_margin"] = net_income / total_revenue


def derive_fundamental_summary(metrics: dict) -> tuple[list[str], list[str]]:
    """Build a short strengths-and-risks summary from headline metrics."""
    highlights = []
    watch_items = []

    gross_margin = normalize_ratio_percent_value(metrics.get("gross_margin"))
    operating_margin = normalize_ratio_percent_value(metrics.get("operating_margin"))
    profit_margin = normalize_ratio_percent_value(metrics.get("profit_margin"))
    revenue_growth = normalize_ratio_percent_value(metrics.get("revenue_growth"))
    earnings_growth = normalize_ratio_percent_value(metrics.get("earnings_growth"))
    free_cash_flow = metrics.get("free_cash_flow")
    debt_to_equity = metrics.get("debt_to_equity")
    current_ratio = metrics.get("current_ratio")
    forward_pe = metrics.get("forward_pe")
    return_on_equity = normalize_ratio_percent_value(metrics.get("return_on_equity"))
    dividend_yield = normalize_yield_percent_value(metrics.get("dividend_yield"))

    if (
        gross_margin is not None
        and gross_margin >= HIGHLIGHT_THRESHOLDS["gross_margin"]
    ):
        highlights.append("Margins remain strong relative to many large-cap peers.")
    if (
        operating_margin is not None
        and operating_margin >= HIGHLIGHT_THRESHOLDS["operating_margin"]
    ):
        highlights.append(
            "Operating leverage appears healthy at the current margin profile."
        )
    if (
        revenue_growth is not None
        and revenue_growth >= HIGHLIGHT_THRESHOLDS["revenue_growth"]
    ):
        highlights.append("Revenue growth remains solid on a year-over-year basis.")
    if (
        earnings_growth is not None
        and earnings_growth >= HIGHLIGHT_THRESHOLDS["earnings_growth"]
    ):
        highlights.append("Earnings growth is still trending positively.")
    if free_cash_flow is not None and free_cash_flow > 0:
        highlights.append("Free cash flow is positive, supporting internal funding.")
    if (
        current_ratio is not None
        and current_ratio >= HIGHLIGHT_THRESHOLDS["current_ratio"]
    ):
        highlights.append(
            "Near-term liquidity looks comfortable based on the current ratio."
        )
    if (
        return_on_equity is not None
        and return_on_equity >= HIGHLIGHT_THRESHOLDS["return_on_equity"]
    ):
        highlights.append("Returns on equity indicate efficient capital deployment.")
    if (
        dividend_yield is not None
        and dividend_yield >= HIGHLIGHT_THRESHOLDS["dividend_yield"]
    ):
        highlights.append(
            "The dividend yield contributes a meaningful cash return profile."
        )

    if profit_margin is not None and profit_margin < WATCH_THRESHOLDS["profit_margin"]:
        watch_items.append(
            "Net margins are thin, leaving less room for execution misses."
        )
    if revenue_growth is not None and revenue_growth < 0:
        watch_items.append("Revenue is contracting versus the prior period.")
    if earnings_growth is not None and earnings_growth < 0:
        watch_items.append("Earnings growth is negative, which can pressure sentiment.")
    if free_cash_flow is not None and free_cash_flow < 0:
        watch_items.append(
            "Free cash flow is negative, which can tighten financial flexibility."
        )
    if (
        debt_to_equity is not None
        and debt_to_equity > WATCH_THRESHOLDS["debt_to_equity"]
    ):
        watch_items.append("Debt levels are elevated relative to equity.")
    if current_ratio is not None and current_ratio < WATCH_THRESHOLDS["current_ratio"]:
        watch_items.append(
            "Current ratio is below 1.0, which may signal tighter short-term liquidity."
        )
    if forward_pe is not None and forward_pe > WATCH_THRESHOLDS["forward_pe"]:
        watch_items.append("Valuation sits above a typical mature-company range.")

    if not highlights:
        highlights.append(
            "No outsized fundamental strengths stood out from the available metrics."
        )
    if not watch_items:
        watch_items.append(
            "No major balance-sheet or earnings-quality red flags stood out from the available metrics."
        )

    return highlights[:4], watch_items[:4]


def get_stock_fundamentals(symbol: str) -> dict:
    """Get core stock fundamentals, balance-sheet context, and quick interpretation."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info or {}

        company_name = get_info_value(info, "longName", "shortName") or symbol
        income_stmt = ticker.income_stmt
        balance_sheet = ticker.balance_sheet
        cashflow = ticker.cashflow
        calendar = ticker.calendar

        metrics = build_metrics(info)
        hydrate_metric_fallbacks(metrics, info, income_stmt, balance_sheet, cashflow)
        highlights, watch_items = derive_fundamental_summary(metrics)

        return {
            "symbol": symbol,
            "company_name": company_name,
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "metrics": metrics,
            "next_earnings": extract_next_earnings_date(calendar, info),
            "highlights": highlights,
            "watch_items": watch_items,
        }
    except Exception as exc:
        return {"error": f"Could not get stock fundamentals for {symbol}: {str(exc)}"}


def format_output(data: dict) -> str:
    """Format all fundamentals data into the final human-readable output."""
    if "error" in data:
        return f"Error: {data['error']}"

    metrics = data["metrics"]
    recommendation = normalize_recommendation(metrics.get("recommendation"))

    return (
        f"{data['symbol']}: {data['company_name']}\n"
        f"Sector: {data.get('sector') or 'N/A'} | Industry: {data.get('industry') or 'N/A'} | Mkt Cap: {format_large_number(data.get('market_cap'))}\n"
        f"\n"
        f"Valuation:\n"
        f"Trailing P/E: {format_number(metrics.get('trailing_pe'))}\n"
        f"Forward P/E: {format_number(metrics.get('forward_pe'))}\n"
        f"PEG Ratio: {format_number(metrics.get('peg_ratio'))}\n"
        f"Price/Sales: {format_number(metrics.get('price_to_sales'))}\n"
        f"Price/Book: {format_number(metrics.get('price_to_book'))}\n"
        f"EV/EBITDA: {format_number(metrics.get('ev_to_ebitda'))}\n"
        f"\n"
        f"Profitability:\n"
        f"Gross Margin: {format_percent(metrics.get('gross_margin'))}\n"
        f"Operating Margin: {format_percent(metrics.get('operating_margin'))}\n"
        f"Net Margin: {format_percent(metrics.get('profit_margin'))}\n"
        f"ROE: {format_percent(metrics.get('return_on_equity'))}\n"
        f"ROA: {format_percent(metrics.get('return_on_assets'))}\n"
        f"\n"
        f"Growth:\n"
        f"Revenue Growth: {format_percent(metrics.get('revenue_growth'))}\n"
        f"Earnings Growth: {format_percent(metrics.get('earnings_growth'))}\n"
        f"\n"
        f"Financial Health:\n"
        f"Cash: {format_large_number(metrics.get('cash'))}\n"
        f"Debt: {format_large_number(metrics.get('debt'))}\n"
        f"Debt/Equity: {format_number(metrics.get('debt_to_equity'), 1)}\n"
        f"Current Ratio: {format_number(metrics.get('current_ratio'), 2)}\n"
        f"Free Cash Flow: {format_large_number(metrics.get('free_cash_flow'))}\n"
        f"\n"
        f"Shareholder Return:\n"
        f"Dividend Yield: {format_yield_percent(metrics.get('dividend_yield'))}\n"
        f"Payout Ratio: {format_percent(metrics.get('payout_ratio'))}\n"
        f"\n"
        f"Forward View:\n"
        f"Analyst Target: {format_price_value(metrics.get('target_mean_price'))}\n"
        f"Recommendation: {recommendation}\n"
        f"Next Earnings: {data.get('next_earnings', 'N/A')}\n"
        f"\n"
        f"Fundamental Highlights:\n"
        + "\n".join(f"- {line}" for line in data["highlights"])
        + "\n\n"
        + "Potential Watch Items:\n"
        + "\n".join(f"- {line}" for line in data["watch_items"])
    )
