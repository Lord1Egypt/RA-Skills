"""
Fallback data sources when TradingView is unavailable or a symbol isn't found.

Chain: TradingView -> Yahoo Finance (stocks) -> Binance REST API (crypto)

Each source handles a subset of symbols. If TV fails, we try the others.
"""

from __future__ import annotations

import logging
import re

import pandas as pd

from tvfetch.exceptions import TvFetchError, TvSymbolNotFoundError
from tvfetch.models import Bar, FetchResult

log = logging.getLogger(__name__)

# Maps TV timeframe strings to yfinance intervals
_TV_TO_YAHOO_TF = {
    "1": "1m", "5": "5m", "15": "15m", "30": "30m",
    "60": "1h", "1D": "1d", "1W": "1wk", "1M": "1mo",
}

# Maps TV timeframe strings to CCXT timeframe format
_TV_TO_CCXT_TF = {
    "1": "1m", "3": "3m", "5": "5m", "15": "15m", "30": "30m",
    "60": "1h", "120": "2h", "240": "4h", "1D": "1d", "1W": "1w",
}


def _tv_symbol_to_yahoo(symbol: str) -> str | None:
    """Convert EXCHANGE:TICKER to a Yahoo Finance ticker, or None if not applicable."""
    if ":" not in symbol:
        return symbol
    exchange, ticker = symbol.split(":", 1)
    exchange = exchange.upper()
    # Crypto on Yahoo: BTCUSDT -> BTC-USDT
    crypto_exchanges = {"BINANCE", "COINBASE", "BYBIT", "KRAKEN", "OKX"}
    if exchange in crypto_exchanges:
        # e.g. BTCUSDT -> BTC-USDT (only if ends in USDT/USD/BTC/ETH/BUSD)
        for quote in ("USDT", "USD", "BUSD", "BTC", "ETH"):
            if ticker.endswith(quote):
                return f"{ticker[:-len(quote)]}-{quote}"
        return None
    # Forex: FX:EURUSD -> EURUSD=X
    if exchange == "FX":
        return f"{ticker}=X"
    # Futures: skip
    if exchange in ("CME", "CME_MINI", "NYMEX", "COMEX"):
        return None
    # Stocks: just return ticker
    return ticker


def _tv_symbol_to_ccxt(symbol: str) -> tuple[str, str] | None:
    """Convert EXCHANGE:TICKER to (exchange_id, ccxt_symbol) or None."""
    if ":" not in symbol:
        return None
    exchange, ticker = symbol.split(":", 1)
    exchange = exchange.lower()
    ccxt_exchanges = {"binance", "bybit", "coinbase", "kraken", "okx", "bitget"}
    if exchange not in ccxt_exchanges:
        return None
    # BTCUSDT -> BTC/USDT
    for quote in ("USDT", "USD", "BUSD", "BTC", "ETH", "USDC"):
        if ticker.endswith(quote):
            return exchange, f"{ticker[:-len(quote)]}/{quote}"
    return None


def fetch_yahoo(
    symbol: str,
    timeframe: str = "1D",
    bars: int = 5000,
) -> FetchResult | None:
    """Try Yahoo Finance. Returns None if yfinance not installed or symbol not found."""
    try:
        import yfinance as yf
    except ImportError:
        log.debug("yfinance not installed, skipping Yahoo fallback")
        return None

    yahoo_sym = _tv_symbol_to_yahoo(symbol)
    if not yahoo_sym:
        return None

    interval = _TV_TO_YAHOO_TF.get(timeframe)
    if not interval:
        return None

    try:
        ticker = yf.Ticker(yahoo_sym)
        df = ticker.history(period="max", interval=interval)
        if df.empty:
            return None
        df.index = df.index.tz_localize("UTC") if df.index.tzinfo is None else df.index.tz_convert("UTC")
        df = df.rename(columns=str.lower)[["open", "high", "low", "close", "volume"]]
        df = df.tail(bars)

        bars_list = [
            Bar(timestamp=idx, open=r["open"], high=r["high"],
                low=r["low"], close=r["close"], volume=r["volume"])
            for idx, r in df.iterrows()
        ]
        return FetchResult(symbol=symbol, timeframe=timeframe, bars=bars_list,
                           source="yahoo", auth_mode="anonymous")
    except Exception as exc:
        log.debug("Yahoo fallback failed for %s: %s", symbol, exc)
        return None


def fetch_ccxt(
    symbol: str,
    timeframe: str = "1D",
    bars: int = 5000,
) -> FetchResult | None:
    """Try CCXT (crypto exchanges). Returns None if ccxt not installed or symbol not found."""
    try:
        import ccxt
    except ImportError:
        log.debug("ccxt not installed, skipping CCXT fallback")
        return None

    parsed = _tv_symbol_to_ccxt(symbol)
    if not parsed:
        return None

    exchange_id, ccxt_sym = parsed
    ccxt_tf = _TV_TO_CCXT_TF.get(timeframe)
    if not ccxt_tf:
        return None

    try:
        exchange = getattr(ccxt, exchange_id)()
        since = None
        ohlcv = exchange.fetch_ohlcv(ccxt_sym, ccxt_tf, since=since, limit=bars)
        if not ohlcv:
            return None
        from datetime import timezone
        from datetime import datetime
        bars_list = [
            Bar(
                timestamp=datetime.fromtimestamp(c[0] / 1000, tz=timezone.utc),
                open=c[1], high=c[2], low=c[3], close=c[4], volume=c[5],
            )
            for c in ohlcv
        ]
        return FetchResult(symbol=symbol, timeframe=timeframe, bars=bars_list,
                           source="ccxt", auth_mode="anonymous")
    except Exception as exc:
        log.debug("CCXT fallback failed for %s: %s", symbol, exc)
        return None


def fetch_with_fallback(
    symbol: str,
    timeframe: str = "1D",
    bars: int = 5000,
    primary_result: FetchResult | None = None,
    primary_error: Exception | None = None,
) -> FetchResult:
    """
    Try fallback sources in order. Used by TvClient when TV fetch fails.

    Order: Yahoo Finance -> CCXT
    """
    if primary_result and primary_result.bars:
        return primary_result

    log.info("Trying Yahoo Finance fallback for %s", symbol)
    result = fetch_yahoo(symbol, timeframe, bars)
    if result:
        log.info("Yahoo Finance returned %d bars for %s", len(result.bars), symbol)
        return result

    log.info("Trying CCXT fallback for %s", symbol)
    result = fetch_ccxt(symbol, timeframe, bars)
    if result:
        log.info("CCXT returned %d bars for %s", len(result.bars), symbol)
        return result

    # All sources failed
    raise TvSymbolNotFoundError(
        symbol,
        hint=(
            f"Also tried Yahoo Finance and CCXT — no data found. "
            f"Original error: {primary_error}"
        ),
    )
