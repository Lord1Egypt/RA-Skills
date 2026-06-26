"""Data models for tvfetch. All public-facing data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

import pandas as pd


@dataclass(frozen=True)
class Bar:
    """A single OHLCV candlestick bar."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    @classmethod
    def from_tv(cls, raw: list) -> "Bar":
        """Parse a raw TradingView bar: [timestamp, open, high, low, close, volume]."""
        if len(raw) < 6:
            raise ValueError(
                f"Unexpected bar format from TradingView: expected at least 6 fields, "
                f"got {len(raw)}. Raw data: {raw!r}"
            )
        ts, o, h, l, c, v = (float(raw[i]) for i in range(6))
        return cls(
            timestamp=datetime.fromtimestamp(ts, tz=timezone.utc),
            open=o, high=h, low=l, close=c, volume=v,
        )


@dataclass(frozen=True)
class SymbolInfo:
    """Metadata about a TradingView symbol."""

    symbol: str           # Full symbol e.g. "BINANCE:BTCUSDT"
    description: str      # Human name e.g. "Bitcoin / TetherUS"
    exchange: str         # Exchange ID e.g. "BINANCE"
    type: str             # "crypto", "stock", "forex", "futures", "index", "bond", "cfd"
    currency: str         # Quote currency e.g. "USDT"

    @property
    def ticker(self) -> str:
        """Just the ticker part without exchange prefix."""
        return self.symbol.split(":")[-1]


AuthMode = Literal["anonymous", "token"]

TIMEFRAME_LABELS: dict[str, str] = {
    "1": "1 min", "3": "3 min", "5": "5 min", "10": "10 min",
    "15": "15 min", "30": "30 min", "45": "45 min",
    "60": "1 hour", "120": "2 hour", "180": "3 hour", "240": "4 hour",
    "1D": "1 day", "1W": "1 week", "1M": "1 month",
}

VALID_TIMEFRAMES = set(TIMEFRAME_LABELS.keys())


@dataclass
class FetchResult:
    """Result of a historical data fetch."""

    symbol: str
    timeframe: str
    bars: list[Bar]
    source: str        # "tradingview", "yahoo", "ccxt"
    auth_mode: AuthMode

    @property
    def df(self) -> pd.DataFrame:
        """Return OHLCV data as a pandas DataFrame indexed by UTC datetime."""
        if not self.bars:
            return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        rows = [
            {"datetime": b.timestamp, "open": b.open, "high": b.high,
             "low": b.low, "close": b.close, "volume": b.volume}
            for b in sorted(self.bars, key=lambda b: b.timestamp)
        ]
        df = pd.DataFrame(rows)
        df.set_index("datetime", inplace=True)
        return df

    def to_csv(self, path: str) -> None:
        self.df.to_csv(path)

    def to_json(self, path: str) -> None:
        self.df.reset_index().to_json(path, orient="records", date_format="iso", indent=2)

    def to_parquet(self, path: str) -> None:
        self.df.to_parquet(path)

    def __len__(self) -> int:
        return len(self.bars)

    def __repr__(self) -> str:
        if self.bars:
            ts = sorted(b.timestamp for b in self.bars)
            span = f"{ts[0].strftime('%Y-%m-%d')} to {ts[-1].strftime('%Y-%m-%d')}"
        else:
            span = "no data"
        tf_label = TIMEFRAME_LABELS.get(self.timeframe, self.timeframe)
        return f"FetchResult({self.symbol}, {tf_label}, {len(self.bars):,} bars, {span})"
