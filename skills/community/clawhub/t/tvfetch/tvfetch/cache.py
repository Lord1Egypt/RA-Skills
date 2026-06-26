"""
SQLite-based local cache for OHLCV data.

Avoids re-fetching data that hasn't changed.
Cache location: ~/.tvfetch/cache.db (configurable)
"""

from __future__ import annotations

import logging
import sqlite3
import time
from pathlib import Path

import pandas as pd

from tvfetch.models import Bar, FetchResult

log = logging.getLogger(__name__)

DEFAULT_CACHE_PATH = Path.home() / ".tvfetch" / "cache.db"

# Seconds before cached data is considered stale
STALE_INTRADAY = 900       # 15 min — for timeframes < 1D
STALE_DAILY = 86400        # 24 hours — for 1D
STALE_WEEKLY = 86400 * 7   # 1 week — for 1W/1M

_INTRADAY = {"1", "3", "5", "10", "15", "30", "45", "60", "120", "180", "240"}

_CREATE_SQL = """
CREATE TABLE IF NOT EXISTS bars (
    symbol    TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    ts        INTEGER NOT NULL,
    open      REAL NOT NULL,
    high      REAL NOT NULL,
    low       REAL NOT NULL,
    close     REAL NOT NULL,
    volume    REAL NOT NULL,
    PRIMARY KEY (symbol, timeframe, ts)
);
CREATE TABLE IF NOT EXISTS fetch_log (
    symbol      TEXT NOT NULL,
    timeframe   TEXT NOT NULL,
    fetched_at  INTEGER NOT NULL,
    bar_count   INTEGER NOT NULL,
    oldest_ts   INTEGER,
    newest_ts   INTEGER,
    PRIMARY KEY (symbol, timeframe)
);
"""


def _stale_seconds(timeframe: str) -> int:
    if timeframe in _INTRADAY:
        return STALE_INTRADAY
    if timeframe == "1D":
        return STALE_DAILY
    return STALE_WEEKLY


class Cache:
    """SQLite OHLCV cache."""

    def __init__(self, path: Path | str = DEFAULT_CACHE_PATH) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self._conn.executescript(_CREATE_SQL)
        self._conn.commit()
        log.debug("Cache opened at %s", self.path)

    def close(self) -> None:
        self._conn.close()

    # ── Read ──────────────────────────────────────────────────────────────────

    def is_fresh(self, symbol: str, timeframe: str) -> bool:
        """Return True if cached data is recent enough to skip a network fetch."""
        row = self._conn.execute(
            "SELECT fetched_at FROM fetch_log WHERE symbol=? AND timeframe=?",
            (symbol, timeframe),
        ).fetchone()
        if not row:
            return False
        age = time.time() - row[0]
        return age < _stale_seconds(timeframe)

    def load(self, symbol: str, timeframe: str) -> pd.DataFrame | None:
        """Return cached DataFrame or None if not cached."""
        rows = self._conn.execute(
            "SELECT ts, open, high, low, close, volume FROM bars "
            "WHERE symbol=? AND timeframe=? ORDER BY ts",
            (symbol, timeframe),
        ).fetchall()
        if not rows:
            return None

        df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
        df["datetime"] = pd.to_datetime(df["ts"], unit="s", utc=True)
        df.set_index("datetime", inplace=True)
        df.drop(columns=["ts"], inplace=True)
        return df

    # ── Write ─────────────────────────────────────────────────────────────────

    def save(self, result: FetchResult) -> None:
        """Persist a FetchResult to the cache (upsert — safe to call repeatedly)."""
        if not result.bars:
            return

        symbol, timeframe = result.symbol, result.timeframe
        rows = [
            (symbol, timeframe, int(b.timestamp.timestamp()), b.open, b.high, b.low, b.close, b.volume)
            for b in result.bars
        ]

        self._conn.executemany(
            "INSERT OR REPLACE INTO bars (symbol, timeframe, ts, open, high, low, close, volume) "
            "VALUES (?,?,?,?,?,?,?,?)",
            rows,
        )

        ts_list = [int(b.timestamp.timestamp()) for b in result.bars]
        self._conn.execute(
            "INSERT OR REPLACE INTO fetch_log (symbol, timeframe, fetched_at, bar_count, oldest_ts, newest_ts) "
            "VALUES (?,?,?,?,?,?)",
            (symbol, timeframe, int(time.time()), len(result.bars), min(ts_list), max(ts_list)),
        )
        self._conn.commit()
        log.debug("Saved %d bars for %s/%s", len(result.bars), symbol, timeframe)

    # ── Management ────────────────────────────────────────────────────────────

    def clear(self, symbol: str | None = None, timeframe: str | None = None) -> int:
        """Delete cached data. Returns number of bar rows deleted."""
        if symbol and timeframe:
            c = self._conn.execute("DELETE FROM bars WHERE symbol=? AND timeframe=?", (symbol, timeframe))
            self._conn.execute("DELETE FROM fetch_log WHERE symbol=? AND timeframe=?", (symbol, timeframe))
        elif symbol:
            c = self._conn.execute("DELETE FROM bars WHERE symbol=?", (symbol,))
            self._conn.execute("DELETE FROM fetch_log WHERE symbol=?", (symbol,))
        else:
            c = self._conn.execute("DELETE FROM bars")
            self._conn.execute("DELETE FROM fetch_log")
        self._conn.commit()
        return c.rowcount

    def stats(self) -> pd.DataFrame:
        """Return a summary of what's in the cache."""
        rows = self._conn.execute(
            "SELECT symbol, timeframe, bar_count, "
            "datetime(oldest_ts, 'unixepoch') as oldest, "
            "datetime(newest_ts, 'unixepoch') as newest, "
            "datetime(fetched_at, 'unixepoch') as fetched_at "
            "FROM fetch_log ORDER BY symbol, timeframe"
        ).fetchall()
        return pd.DataFrame(rows, columns=["symbol", "timeframe", "bars", "oldest", "newest", "fetched_at"])

    def size_mb(self) -> float:
        """Return cache file size in MB."""
        try:
            return self.path.stat().st_size / 1_048_576
        except FileNotFoundError:
            return 0.0
