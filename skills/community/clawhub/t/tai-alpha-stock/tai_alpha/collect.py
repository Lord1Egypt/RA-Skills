"""Fetch and compute fundamentals + technicals for one ticker (yfinance)."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yfinance as yf

from tai_alpha.schema import fear_greed_from_vix, normalize_collect_data
from tai_alpha.sector_map import sector_etf
from tai_alpha.storage_sqlite import (
    connect,
    create_run,
    init_db,
    update_run_collect,
)
from tai_alpha.yfinance_utils import close_series, ensure_datetime_index


def _peer_score_from_sector(
    ticker_roe: float, sector: str | None, spy_mom: float
) -> tuple[str, int]:
    """
    Compare ticker ROE to sector ETF one-year return as a simple peer-relative score.
    Returns (peers_label, score 0–5).
    """
    etf = sector_etf(sector)
    if not etf:
        return (sector or "N/A", 0)
    try:
        sh = yf.Ticker(etf).history(period="1y")
        if sh.empty:
            return (etf, 0)
        c = close_series(sh, etf)
        c = ensure_datetime_index(c).dropna()
        if len(c) < 20:
            return (etf, 0)
        etf_ret = (float(c.iloc[-1]) / float(c.iloc[0]) - 1.0) if len(c) else 0.0
        if ticker_roe > 0.15 and etf_ret > spy_mom / 100.0 * 0.5:
            return (etf, 5)
        if ticker_roe > 0.10:
            return (etf, 3)
        return (etf, 0)
    except Exception:
        return (etf, 0)


def fetch_collect_data(ticker: str, *, fast: bool = False) -> dict[str, Any]:
    """
    Download data for ``ticker`` and return a normalized dict (no persistence).

    ``fast`` skips the sector ETF peer fetch (lighter network use).
    """
    data: dict[str, Any] = {
        "ticker": ticker.upper().strip(),
        "error": None,
        "timestamp": datetime.now().isoformat(),
    }
    try:
        stock = yf.Ticker(data["ticker"])
        info = stock.info or {}
        hist = stock.history(period="3y")
        if hist.empty:
            data["error"] = "No history data"
            return data

        close = close_series(hist, data["ticker"])
        close = ensure_datetime_index(close).dropna()
        if close.empty:
            data["error"] = "No close prices"
            return data

        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        last_loss = loss.iloc[-1]
        rsi = (
            100 - (100 / (1 + rs.iloc[-1]))
            if not pd.isna(last_loss) and last_loss != 0
            else 50.0
        )

        exp1 = close.ewm(span=12).mean()
        exp2 = close.ewm(span=26).mean()
        macd_line = exp1 - exp2
        signal_line = macd_line.ewm(span=9).mean()
        macd_signal = "bull" if macd_line.iloc[-1] > signal_line.iloc[-1] else "bear"

        returns = close.pct_change().dropna()
        sharpe = (
            float(returns.mean() / returns.std() * np.sqrt(252))
            if returns.std() != 0
            else 0.0
        )

        spy_df = yf.download("SPY", period="3y", progress=False)
        spy_close = close_series(spy_df, "SPY")
        spy_close = ensure_datetime_index(spy_close).dropna()
        spy_ret = spy_close.pct_change().dropna()
        aligned_returns = returns.reindex(spy_ret.index).dropna()
        aligned_spy = spy_ret.reindex(aligned_returns.index).dropna()
        beta_raw = (
            aligned_returns.cov(aligned_spy) / aligned_spy.var()
            if len(aligned_spy) > 0
            else 1.0
        )
        beta = (
            float(beta_raw)
            if not isinstance(beta_raw, pd.Series)
            else float(beta_raw.iloc[0])
        )

        vix_df = yf.download("^VIX", period="1mo", progress=False)
        vix_close = close_series(vix_df, "^VIX")
        vix = float(vix_close.iloc[-1]) if not vix_close.empty else 20.0
        spy_mom = (
            (spy_close.iloc[-1] / spy_close.iloc[-21] - 1) * 100
            if len(spy_close) > 21
            else 0.0
        )

        sector = info.get("sector")
        roe = float(info.get("returnOnEquity") or 0)
        if fast:
            peers_label = sector or "N/A"
            peer_score = 0
        else:
            peers_label, peer_score = _peer_score_from_sector(
                roe, sector, float(spy_mom)
            )

        news_raw = stock.news
        news_list = (
            [n.get("title", "") for n in (news_raw or [])[:5]] if news_raw else []
        )

        short_ratio = float(
            info.get("shortPercentOfFloat") or info.get("shortRatio") or 0.1
        )
        implied_vol = float(info.get("impliedVolatility") or 0.3)

        data.update(
            {
                "price": float(
                    info.get("currentPrice") or info.get("regularMarketPrice") or 0
                ),
                "pe": float(info.get("trailingPE") or 999),
                "roe": roe,
                "debt": float(info.get("debtToEquity") or 999),
                "div_yield": float(info.get("dividendYield") or 0),
                "rsi": float(rsi),
                "vol": float(hist["Volume"].mean()),
                "news": news_list,
                "sector": sector,
                "sharpe": sharpe,
                "macd": macd_signal,
                "analyst_target": float(info.get("targetMeanPrice") or 0),
                "rating_mean": float(info.get("recommendationMean") or 3),
                "beta": beta,
                "eps_growth": float(info.get("earningsQuarterlyGrowth") or 0),
                "vix": vix,
                "spy_mom": float(spy_mom),
                "peers": peers_label,
                "peer_score": peer_score,
                "hy_spread": 350.0,
                "yield_curve": 0.25,
                "iv": implied_vol if implied_vol else 0.35,
                "fear_greed": fear_greed_from_vix(vix),
                "shortRatio": short_ratio,
                "impliedVolatility": implied_vol if implied_vol else 0.3,
            }
        )
    except Exception as e:
        data["error"] = str(e)

    if not data.get("error"):
        normalize_collect_data(data)
    return data


def collect_ticker_routed(
    ticker: str,
    db_path: Path,
    *,
    fast: bool = False,
    market: str = "auto",
) -> tuple[dict[str, Any], int]:
    """
    Resolve US/HK/CN symbol for yfinance, fetch via adapter, persist collect.

    ``market`` is ``auto`` or ``us`` / ``hk`` / ``cn``.
    """
    from tai_alpha.data_adapters.yahoo_adapter import fetch_via_yahoo
    from tai_alpha.market_router import detect_market, normalize_for_yfinance

    explicit = None if (market or "").lower() == "auto" else market
    m = detect_market(ticker, explicit)
    sym = normalize_for_yfinance(ticker, m)
    init_db(db_path)
    conn = connect(db_path)
    try:
        run_id = create_run(conn, ticker)
        data = fetch_via_yahoo(
            sym,
            market=m,
            fast=fast,
            display_ticker=ticker,
        )
        update_run_collect(conn, run_id, data)
        conn.commit()
        return data, run_id
    finally:
        conn.close()


def collect_ticker(
    ticker: str,
    db_path: Path,
    *,
    fast: bool = False,
) -> tuple[dict[str, Any], int]:
    """
    Fetch data, insert a new run, and persist ``collect_json``.
    Returns ``(data, run_id)``.

    ``fast`` is passed to ``fetch_collect_data`` (skips sector ETF peer pull).
    """
    init_db(db_path)
    conn = connect(db_path)
    try:
        run_id = create_run(conn, ticker)
        data = fetch_collect_data(ticker, fast=fast)
        update_run_collect(conn, run_id, data)
        conn.commit()
        return data, run_id
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    import argparse

    if argv is None:
        argv = sys.argv[1:]
    p = argparse.ArgumentParser(description="Fetch normalized data for one ticker")
    p.add_argument("ticker", help="Symbol")
    p.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="SQLite database path (default: TAI_ALPHA_DB_PATH or output dir)",
    )
    args = p.parse_args(argv)

    from tai_alpha.storage_sqlite import default_db_path

    db_path = args.db_path or default_db_path()
    data, _ = collect_ticker(args.ticker, db_path)
    print(json.dumps(data, indent=2, default=str))
    return 1 if data.get("error") else 0
