"""Dividend history and simple heuristics via yfinance (US-oriented)."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import pandas as pd
import yfinance as yf


def dividend_summary(ticker: str) -> dict[str, Any]:
    """
    Summarize trailing dividend history for ``ticker``.

    Returns keys: ``ticker``, ``annualized_yield_proxy`` (float or None),
    ``years_of_history``, ``payments_per_year_guess``, ``notes`` (list[str]),
    and ``error`` if fetch fails.

    Yields from yfinance are approximate; ex-dates and splits are not modeled.
    """
    sym = ticker.upper().strip()
    out: dict[str, Any] = {
        "ticker": sym,
        "annualized_yield_proxy": None,
        "years_of_history": 0,
        "payments_per_year_guess": None,
        "notes": [],
        "error": None,
    }
    try:
        t = yf.Ticker(sym)
        divs = t.dividends
        if divs is None or len(divs) == 0:
            out["notes"].append(
                "No dividend history returned (may be non-dividend stock)."
            )
            return out

        series = divs.sort_index()
        if len(series) == 0:
            out["notes"].append("Empty dividend series after sort.")
            return out
        end = series.index.max()
        cutoff = end - pd.DateOffset(months=13)
        last_year = series[series.index >= cutoff]
        trailing = float(last_year.sum()) if len(last_year) else 0.0
        info = t.info or {}
        price = float(info.get("regularMarketPrice") or info.get("currentPrice") or 0)
        if price > 0 and trailing > 0:
            out["annualized_yield_proxy"] = round(trailing / price, 4)

        idx = series.index
        if len(idx) >= 2:
            span_years = (idx[-1] - idx[0]).days / 365.25
            out["years_of_history"] = max(0, int(round(span_years)))
        if len(series) >= 3:
            idx_series = pd.Series(series.index)
            gaps = idx_series.diff().dt.days.dropna()
            med = float(gaps.median()) if len(gaps) else 0.0
            if med > 300:
                out["payments_per_year_guess"] = 1
            elif med > 80:
                out["payments_per_year_guess"] = 4
            else:
                out["payments_per_year_guess"] = 12
        if out.get("annualized_yield_proxy") and out["annualized_yield_proxy"] > 0.12:
            out["notes"].append(
                "Very high yield proxy — verify sustainability and one-offs."
            )
    except Exception as e:  # noqa: BLE001
        out["error"] = str(e)
    return out


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description="Dividend history summary (yfinance)")
    p.add_argument("ticker", nargs="?", default="AAPL")
    args = p.parse_args(argv)
    out = dividend_summary(args.ticker)
    print(json.dumps(out, indent=2, default=str))
    return 1 if out.get("error") else 0
