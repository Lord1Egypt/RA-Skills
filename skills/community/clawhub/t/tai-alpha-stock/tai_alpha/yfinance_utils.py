"""Helpers for yfinance DataFrame shape inconsistencies (MultiIndex columns)."""

from __future__ import annotations

import pandas as pd


def close_series(hist: pd.DataFrame, ticker: str | None = None) -> pd.Series:
    """Return a 1D Close series from yfinance history or download output."""
    if hist.empty:
        return pd.Series(dtype=float)
    close = hist["Close"]
    if isinstance(close, pd.DataFrame):
        if ticker and ticker in close.columns:
            s = close[ticker]
        else:
            s = close.iloc[:, 0]
        return s.squeeze()
    return close.squeeze()


def ensure_datetime_index(s: pd.Series) -> pd.Series:
    """Drop duplicate index labels (can occur with bad provider data)."""
    if s.index.has_duplicates:
        s = s[~s.index.duplicated(keep="last")]
    return s.sort_index()
