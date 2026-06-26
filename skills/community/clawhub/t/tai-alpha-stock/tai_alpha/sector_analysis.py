"""Ticker vs sector ETF relative performance (alpha proxy)."""

from __future__ import annotations

import json
import sys
from typing import Any

import numpy as np
import pandas as pd
import yfinance as yf

from tai_alpha.sector_map import sector_etf
from tai_alpha.yfinance_utils import close_series, ensure_datetime_index


def _cagr(series: pd.Series) -> float:
    s = ensure_datetime_index(series).dropna()
    if len(s) < 2:
        return float("nan")
    total = float(s.iloc[-1] / s.iloc[0] - 1.0)
    years = (s.index[-1] - s.index[0]).days / 365.25
    if years <= 0:
        return float("nan")
    return float((1 + total) ** (1 / years) - 1)


def sector_alpha(
    ticker: str, etf: str | None = None, period: str = "3y"
) -> dict[str, Any]:
    """
    Compare ticker total return vs sector ETF (CAGR difference as alpha proxy).
    If ``etf`` is omitted, infer from Yahoo ``sector`` on the ticker.
    """
    t = ticker.upper().strip()
    stock = yf.Ticker(t)
    info = stock.info or {}
    sector = info.get("sector")
    etf_sym = (etf or sector_etf(sector) or "SPY").upper()

    th = yf.download(t, period=period, progress=False)
    eh = yf.download(etf_sym, period=period, progress=False)
    tc = close_series(th, t)
    ec = close_series(eh, etf_sym)
    tc = ensure_datetime_index(tc).dropna()
    ec = ensure_datetime_index(ec).dropna()

    c_t = _cagr(tc)
    c_e = _cagr(ec)
    alpha = c_t - c_e if not (np.isnan(c_t) or np.isnan(c_e)) else float("nan")

    return {
        "ticker": t,
        "sector": sector,
        "etf": etf_sym,
        "ticker_cagr": c_t,
        "etf_cagr": c_e,
        "alpha_cagr_vs_etf": alpha,
        "score_lift_estimate": min(15, max(-15, int(round(alpha * 100)))),
    }


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) < 1:
        print("Usage: sector.py TICKER [ETF]", file=sys.stderr)
        return 2
    ticker = argv[0]
    etf = argv[1] if len(argv) > 1 else None
    out = sector_alpha(ticker, etf)
    print(json.dumps(out, indent=2, default=str))
    return 0
