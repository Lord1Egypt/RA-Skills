"""
Export helpers for backtesting framework integration.

Supported outputs:
  - pandas DataFrame (native)
  - CSV
  - JSON
  - Parquet (requires pyarrow)
  - backtrader PandasData feed
  - freqtrade candle format
"""

from __future__ import annotations

import pandas as pd

from tvfetch.models import FetchResult


# ── Raw formats ───────────────────────────────────────────────────────────────

def to_csv(result: FetchResult, path: str) -> None:
    """Export to CSV. Columns: datetime,open,high,low,close,volume"""
    result.df.to_csv(path)


def to_json(result: FetchResult, path: str) -> None:
    """Export to JSON array of records."""
    result.df.reset_index().to_json(path, orient="records", date_format="iso", indent=2)


def to_parquet(result: FetchResult, path: str) -> None:
    """Export to Parquet (requires: pip install tvfetch[parquet])."""
    try:
        result.df.to_parquet(path)
    except ImportError:
        raise ImportError(
            "Parquet export requires pyarrow. Install it with: pip install tvfetch[parquet]"
        )


# ── backtrader ────────────────────────────────────────────────────────────────

def to_backtrader(result: FetchResult):
    """
    Return a backtrader PandasData feed ready to pass to bt.Cerebro().adddata().

    Requires: pip install backtrader

    Example:
        import backtrader as bt
        result = tvfetch.fetch("BINANCE:BTCUSDT", "1D", bars=365)
        feed = tvfetch.exporters.to_backtrader(result)

        cerebro = bt.Cerebro()
        cerebro.adddata(feed)
        cerebro.run()
    """
    try:
        import backtrader as bt
    except ImportError:
        raise ImportError(
            "backtrader not installed. Install it with: pip install backtrader"
        )

    df = result.df.copy()
    # backtrader expects a 'openinterest' column (set to 0 if not present)
    if "openinterest" not in df.columns:
        df["openinterest"] = 0

    return bt.feeds.PandasData(
        dataname=df,
        datetime=None,   # already the index
        open="open",
        high="high",
        low="low",
        close="close",
        volume="volume",
        openinterest="openinterest",
    )


# ── freqtrade ─────────────────────────────────────────────────────────────────

def to_freqtrade(result: FetchResult) -> list[list]:
    """
    Return data in freqtrade's native candle format:
    [[timestamp_ms, open, high, low, close, volume], ...]

    Example:
        from freqtrade.data.history import store_pair_data
        candles = tvfetch.exporters.to_freqtrade(result)
    """
    rows = []
    for bar in sorted(result.bars, key=lambda b: b.timestamp):
        ts_ms = int(bar.timestamp.timestamp() * 1000)
        rows.append([ts_ms, bar.open, bar.high, bar.low, bar.close, bar.volume])
    return rows


# ── vectorbt ─────────────────────────────────────────────────────────────────

def to_vectorbt(result: FetchResult):
    """
    Return data compatible with vectorbt.

    Requires: pip install vectorbt

    Example:
        import vectorbt as vbt
        data = tvfetch.exporters.to_vectorbt(result)
        pf = vbt.Portfolio.from_signals(data.close, entries, exits)
    """
    try:
        import vectorbt as vbt
    except ImportError:
        raise ImportError(
            "vectorbt not installed. Install it with: pip install vectorbt"
        )
    df = result.df
    return vbt.OHLCV.from_df(df)
