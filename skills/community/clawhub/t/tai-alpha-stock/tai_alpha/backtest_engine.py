"""VectorBT backtests: RSI, MACD, Bollinger — shared by scripts and tests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd
import vectorbt as vbt
import yfinance as yf

from tai_alpha.schema import empty_backtest
from tai_alpha.storage_sqlite import (
    connect,
    get_collect_dict,
    init_db,
    update_run_backtest,
)
from tai_alpha.yfinance_utils import close_series, ensure_datetime_index

StrategyName = Literal["rsi", "macd", "bb"]


def _yf_symbol(raw: dict[str, Any]) -> str:
    """Yahoo download symbol (resolved) vs display ticker in ``raw``."""
    meta = raw.get("adapter_meta") or {}
    return str(meta.get("symbol_resolved") or raw.get("ticker", ""))


def _stats_dict(pf: vbt.Portfolio) -> dict[str, Any]:
    try:
        st = pf.stats()
        return {
            "CAGR [%]": (
                float(st["CAGR [%]"]) if not pd.isna(st["CAGR [%]"]) else float("nan")
            ),
            "Sharpe Ratio": (
                float(st["Sharpe Ratio"])
                if not pd.isna(st["Sharpe Ratio"])
                else float("nan")
            ),
            "Max Drawdown [%]": (
                float(st["Max Drawdown [%]"])
                if not pd.isna(st["Max Drawdown [%]"])
                else float("nan")
            ),
            "Win Rate [%]": (
                float(st["Win Rate [%]"])
                if not pd.isna(st.get("Win Rate [%]", np.nan))
                else float("nan")
            ),
            "# Trades": (
                float(st["# Trades"]) if not pd.isna(st["# Trades"]) else float("nan")
            ),
        }
    except Exception:
        return {
            "CAGR [%]": float("nan"),
            "Sharpe Ratio": float("nan"),
            "Max Drawdown [%]": float("nan"),
            "Win Rate [%]": float("nan"),
            "# Trades": float("nan"),
        }


def build_signals(
    close: pd.Series,
    strategy: StrategyName = "rsi",
    rsi_low: float = 35.0,
    rsi_high: float = 75.0,
) -> tuple[pd.Series, pd.Series]:
    """Return (entries, exits) boolean series aligned to ``close``."""
    close = ensure_datetime_index(close).dropna()
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    if strategy == "rsi":
        entries = rsi < rsi_low
        exits = rsi > rsi_high
        return entries, exits

    if strategy == "macd":
        exp1 = close.ewm(span=12).mean()
        exp2 = close.ewm(span=26).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=9).mean()
        entries = macd > signal_line
        exits = macd < signal_line
        return entries, exits

    # Bollinger: buy at lower band, sell at upper
    mid = close.rolling(20).mean()
    std = close.rolling(20).std()
    lower = mid - 2 * std
    upper = mid + 2 * std
    entries = close < lower
    exits = close > upper
    return entries, exits


def run_backtest_from_collect(
    raw: dict[str, Any],
    strategy: StrategyName = "rsi",
    rsi_low: float = 35.0,
    rsi_high: float = 75.0,
) -> dict[str, Any]:
    """Run VectorBT backtest from a collect payload dict (no DB)."""
    if raw.get("error"):
        bt = empty_backtest()
        bt["error"] = raw["error"]
        return bt

    ticker = _yf_symbol(raw)
    hist = yf.download(ticker, period="3y", progress=False)
    close = close_series(hist, ticker)
    close = ensure_datetime_index(close).dropna()
    if close.empty:
        bt = empty_backtest()
        bt["error"] = "No price history for backtest"
        return bt

    entries, exits = build_signals(
        close, strategy=strategy, rsi_low=rsi_low, rsi_high=rsi_high
    )
    pf = vbt.Portfolio.from_signals(close, entries, exits, freq="D")
    stats = _stats_dict(pf)

    bh_pf = vbt.Portfolio.from_signals(
        close,
        pd.Series(True, index=close.index),
        pd.Series(False, index=close.index),
        freq="D",
    )
    bh_stats = _stats_dict(bh_pf)

    spy_hist = yf.download("SPY", period="3y", progress=False)
    spy_close = close_series(spy_hist, "SPY")
    spy_close = ensure_datetime_index(spy_close).dropna()
    spy_bh_pf = vbt.Portfolio.from_signals(
        spy_close,
        pd.Series(True, index=spy_close.index),
        pd.Series(False, index=spy_close.index),
        freq="D",
    )
    spy_stats = _stats_dict(spy_bh_pf)

    bt: dict[str, Any] = {
        "strategy": strategy,
        "rsi_low": rsi_low,
        "rsi_high": rsi_high,
        "strategy_cagr": stats["CAGR [%]"],
        "strategy_sharpe": stats["Sharpe Ratio"],
        "strategy_max_dd": stats["Max Drawdown [%]"],
        "bh_cagr": bh_stats["CAGR [%]"],
        "bh_sharpe": bh_stats["Sharpe Ratio"],
        "bh_max_dd": bh_stats["Max Drawdown [%]"],
        "spy_cagr": spy_stats["CAGR [%]"],
        "alpha_vs_spy": stats["CAGR [%]"] - spy_stats["CAGR [%]"],
        "win_rate": stats["Win Rate [%]"],
        "trades": stats["# Trades"],
    }
    for k, v in bt.items():
        if isinstance(v, float) and (pd.isna(v) or np.isnan(v)):
            bt[k] = None

    return bt


def run_backtest(
    db_path: Path,
    run_id: int,
    *,
    strategy: StrategyName = "rsi",
    rsi_low: float = 35.0,
    rsi_high: float = 75.0,
) -> dict[str, Any]:
    """Load collect for ``run_id``, run backtest, persist ``backtest_json``."""
    init_db(db_path)
    conn = connect(db_path)
    try:
        raw = get_collect_dict(conn, run_id)
        if raw is None:
            bt = empty_backtest()
            bt["error"] = "No collect data for run"
            update_run_backtest(conn, run_id, bt)
            conn.commit()
            return bt
        bt = run_backtest_from_collect(
            raw, strategy=strategy, rsi_low=rsi_low, rsi_high=rsi_high
        )
        update_run_backtest(conn, run_id, bt)
        conn.commit()
        return bt
    finally:
        conn.close()


def multi_strategy_compare_from_collect(raw: dict[str, Any]) -> dict[str, Any]:
    """Return best of RSI / MACD / BB by strategy CAGR."""
    if raw.get("error"):
        return {"error": raw["error"], "top_strat": None, "top_cagr": None}

    ticker = _yf_symbol(raw)
    hist = yf.download(ticker, period="3y", progress=False)
    close = close_series(hist, ticker)
    close = ensure_datetime_index(close).dropna()
    if close.empty:
        return {"error": "No data", "top_strat": None, "top_cagr": None}

    strats: dict[str, float] = {}
    for name in ("rsi", "macd", "bb"):
        entries, exits = build_signals(close, strategy=name)  # type: ignore[arg-type]
        pf = vbt.Portfolio.from_signals(close, entries, exits, freq="D")
        st = _stats_dict(pf)
        strats[name.upper()] = st["CAGR [%]"]

    def _rank(v: float) -> float:
        if v != v or np.isnan(v):  # NaN
            return -1e9
        return float(v)

    top = max(strats, key=lambda k: _rank(strats[k]))
    return {
        "top_strat": top,
        "top_cagr": strats[top],
        "all": strats,
    }


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description="VectorBT backtest")
    p.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="SQLite database path",
    )
    p.add_argument(
        "--run-id",
        type=int,
        required=True,
        help="Run id with collect_json populated",
    )
    p.add_argument(
        "--strategy",
        default="rsi",
        choices=("rsi", "macd", "bb"),
    )
    p.add_argument("--rsi-low", type=float, default=35.0)
    p.add_argument("--rsi-high", type=float, default=75.0)
    args = p.parse_args(argv)

    from tai_alpha.storage_sqlite import default_db_path

    db_path = args.db_path or default_db_path()
    bt = run_backtest(
        db_path,
        args.run_id,
        strategy=args.strategy,  # type: ignore[arg-type]
        rsi_low=args.rsi_low,
        rsi_high=args.rsi_high,
    )
    print(json.dumps(bt, default=str))
    return 0 if not bt.get("error") else 1
