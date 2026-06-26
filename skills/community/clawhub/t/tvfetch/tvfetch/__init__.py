"""
tvfetch — Free TradingView data fetcher
========================================

Fetches historical OHLCV data and live prices for any symbol
TradingView supports — stocks, crypto, forex, futures, indices,
commodities — with no API key required.

Quick start
-----------
    import tvfetch

    # Historical data (no login needed)
    df = tvfetch.fetch("BINANCE:BTCUSDT", "1D", bars=365)

    # Multiple symbols at once (one connection, much faster)
    results = tvfetch.fetch_multi(
        ["BINANCE:BTCUSDT", "NASDAQ:AAPL", "FX:EURUSD"],
        timeframe="1D",
    )

    # Live prices (real-time streaming)
    def on_price(bar):
        print(f"{bar.symbol}: {bar.close:.4f}  {bar.change_pct:+.2f}%")

    tvfetch.stream(["BINANCE:BTCUSDT", "FX:EURUSD"], on_update=on_price)

    # Search for symbols
    results = tvfetch.search("bitcoin", symbol_type="crypto")

    # With auth token (paid plans get more intraday bars)
    df = tvfetch.fetch("BINANCE:BTCUSDT", "1", bars=20000, auth_token="your_jwt_token")

Auth token (optional)
---------------------
Paste your TradingView auth token for more data on paid plans.

To get your token:
  1. Log in to tradingview.com
  2. Open DevTools (F12) -> Console
  3. Run: document.cookie.split('; ').find(c=>c.startsWith('auth_token=')).split('=').slice(1).join('=')
  4. Copy the JWT string

Bar limits (anonymous / free account):
  1 min   ~6,500 bars  (~4 days)
  5 min   ~5,300 bars  (~18 days)
  15 min  ~5,200 bars  (~55 days)
  1 hour  ~10,800 bars (~15 months)
  4 hour  ~7,100 bars  (~3 years)
  1 day   Full history (BTC: back to 2017, stocks: back to IPO)

Bar limits with paid plan:
  Essential: 10,000 bars intraday
  Plus/Premium: 20,000 bars intraday
  Ultimate: 40,000 bars intraday

Disclaimer
----------
This tool is for educational and personal use.
Using it may violate TradingView's Terms of Service.
Users are responsible for compliance with applicable terms.
"""

from __future__ import annotations

import logging
from typing import Callable

from tvfetch.auth import ANONYMOUS_TOKEN, anonymous_token, login
from tvfetch.exceptions import (
    TvAuthError,
    TvConnectionError,
    TvFetchError,
    TvNoDataError,
    TvRateLimitError,
    TvSymbolNotFoundError,
    TvTimeoutError,
)
from tvfetch.historical import fetch as _fetch
from tvfetch.historical import fetch_df, fetch_multi
from tvfetch.live import LiveBar, LiveStream
from tvfetch.live import stream as _stream
from tvfetch.models import Bar, FetchResult, SymbolInfo, TIMEFRAME_LABELS
from tvfetch.symbols import search as _search


__version__ = "0.1.0"
__all__ = [
    # Core fetch functions
    "fetch",
    "fetch_df",
    "fetch_multi",
    "stream",
    "search",
    # Auth
    "login",
    "anonymous_token",
    # Models
    "Bar",
    "FetchResult",
    "SymbolInfo",
    "LiveBar",
    "LiveStream",
    # Exceptions
    "TvFetchError",
    "TvConnectionError",
    "TvAuthError",
    "TvSymbolNotFoundError",
    "TvNoDataError",
    "TvTimeoutError",
    "TvRateLimitError",
    # Constants
    "TIMEFRAME_LABELS",
    "ANONYMOUS_TOKEN",
    "__version__",
]

# ── Public convenience functions ──────────────────────────────────────────────


def fetch(
    symbol: str,
    timeframe: str = "1D",
    bars: int = 5000,
    auth_token: str = ANONYMOUS_TOKEN,
    *,
    adjustment: str = "splits",
    extended_session: bool = False,
) -> FetchResult:
    """
    Fetch historical OHLCV bars for any TradingView symbol.

    Args:
        symbol:           EXCHANGE:TICKER, e.g. "BINANCE:BTCUSDT", "NASDAQ:AAPL"
        timeframe:        "1","5","15","30","60","240","1D","1W","1M"
        bars:             How many bars to fetch (paginated automatically)
        auth_token:       Optional JWT token from your browser for paid plan access
        adjustment:       "splits" | "dividends" | "none"
        extended_session: Include pre/after-market data (stocks only)

    Returns:
        FetchResult — use .df for pandas DataFrame, .to_csv(), .to_json()

    Raises:
        TvSymbolNotFoundError, TvNoDataError, TvTimeoutError, TvConnectionError

    Examples:
        # Anonymous (no login)
        result = tvfetch.fetch("BINANCE:BTCUSDT", "1D", bars=365)
        df = result.df

        # With auth token (paid plan)
        result = tvfetch.fetch("NASDAQ:AAPL", "1", bars=20000, auth_token="eyJ...")
    """
    return _fetch(
        symbol=symbol,
        timeframe=timeframe,
        bars=bars,
        auth_token=auth_token,
        adjustment=adjustment,
        extended_session=extended_session,
    )


def stream(
    symbols: list[str] | str,
    on_update: Callable[[LiveBar], None],
    timeframe: str = "1",
    auth_token: str = ANONYMOUS_TOKEN,
    duration: float | None = None,
) -> LiveStream:
    """
    Stream live real-time price updates for one or more symbols.

    Calls on_update every 1-3 seconds as trades happen on TradingView.
    Works anonymously — no login required.

    Args:
        symbols:   Symbol or list of symbols
        on_update: Callback called with LiveBar on each price update
        timeframe: Bar interval for live updates (default "1" = 1-minute candles)
        auth_token: Optional auth token
        duration:  Auto-stop after N seconds (None = run until Ctrl+C)

    Example:
        def handle(bar: tvfetch.LiveBar):
            print(f"{bar.symbol}: ${bar.close:.2f}  {bar.change_pct:+.2f}%")

        tvfetch.stream(["BINANCE:BTCUSDT", "FX:EURUSD"], on_update=handle)
    """
    return _stream(symbols, on_update, timeframe, auth_token, duration)


def search(
    query: str,
    exchange: str = "",
    symbol_type: str = "",
    limit: int = 20,
) -> list[SymbolInfo]:
    """
    Search TradingView for symbols.

    Args:
        query:       Search term, e.g. "bitcoin", "apple", "EURUSD"
        exchange:    Optional exchange filter, e.g. "BINANCE", "NASDAQ"
        symbol_type: "stock" | "crypto" | "forex" | "futures" | "index" | "bond"
        limit:       Max results (default 20)

    Example:
        results = tvfetch.search("bitcoin", symbol_type="crypto")
        for sym in results:
            print(sym.symbol, sym.description)
    """
    return _search(query, exchange=exchange, symbol_type=symbol_type, limit=limit)


# ── Logging setup ─────────────────────────────────────────────────────────────

logging.getLogger(__name__).addHandler(logging.NullHandler())
