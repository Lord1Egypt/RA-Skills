"""
Historical OHLCV data fetcher.

Connects to TradingView WebSocket, fetches data with automatic pagination,
and returns a clean pandas DataFrame or FetchResult.
"""

from __future__ import annotations

import logging
from typing import overload

import pandas as pd

from tvfetch.auth import ANONYMOUS_TOKEN, is_anonymous
from tvfetch.cache import Cache
from tvfetch.core.connection import TvConnection
from tvfetch.exceptions import TvNoDataError, TvSymbolNotFoundError, TvTimeoutError
from tvfetch.models import Bar, FetchResult, VALID_TIMEFRAMES

log = logging.getLogger(__name__)

# How long to wait for a fetch to complete
_FETCH_TIMEOUT = 120  # seconds

# Module-level cache instance (shared across all fetch() calls)
_cache = Cache()


def fetch(
    symbol: str,
    timeframe: str = "1D",
    bars: int = 5000,
    auth_token: str = ANONYMOUS_TOKEN,
    adjustment: str = "splits",
    extended_session: bool = False,
    connection: TvConnection | None = None,
    use_cache: bool = True,
) -> FetchResult:
    """
    Fetch historical OHLCV bars for a symbol from TradingView.

    Args:
        symbol:           Full symbol in EXCHANGE:TICKER format, e.g. "BINANCE:BTCUSDT"
        timeframe:        Bar interval — "1","5","15","30","60","240","1D","1W","1M"
        bars:             Number of bars to fetch. Paginated automatically.
                          Free/anonymous limit: ~6.5k for 1min, ~10.8k for 1h, unlimited for 1D.
        auth_token:       Optional auth token for paid plan access (more bars on intraday).
        adjustment:       Price adjustment mode: "splits", "dividends", "none"
        extended_session: Include pre/after market data (stocks only)
        connection:       Reuse an existing TvConnection (faster for multiple fetches)
        use_cache:        Check local SQLite cache before fetching (default True).
                          Set False to force a fresh network fetch.

    Returns:
        FetchResult with .df (DataFrame), .to_csv(), .to_json(), .to_parquet()

    Raises:
        TvSymbolNotFoundError: Symbol doesn't exist
        TvNoDataError:         No data available for this timeframe
        TvTimeoutError:        Request timed out

    Example:
        >>> result = fetch("BINANCE:BTCUSDT", "1D", bars=365)
        >>> print(result.df.tail())
    """
    if timeframe not in VALID_TIMEFRAMES:
        raise ValueError(
            f"Invalid timeframe '{timeframe}'. "
            f"Valid options: {', '.join(sorted(VALID_TIMEFRAMES))}"
        )

    auth_mode = "anonymous" if is_anonymous(auth_token) else "token"

    # --- Cache check ---
    if use_cache and _cache.is_fresh(symbol, timeframe):
        cached_df = _cache.load(symbol, timeframe)
        if cached_df is not None:
            log.debug("Cache hit for %s/%s (%d rows)", symbol, timeframe, len(cached_df))
            cached_bars = [
                Bar(
                    timestamp=row.Index.to_pydatetime(),
                    open=row.open,
                    high=row.high,
                    low=row.low,
                    close=row.close,
                    volume=row.volume,
                )
                for row in cached_df.itertuples()
            ]
            return FetchResult(
                symbol=symbol,
                timeframe=timeframe,
                bars=cached_bars,
                source="cache",
                auth_mode=auth_mode,
            )

    own_connection = connection is None

    if own_connection:
        conn = TvConnection(auth_token)
        conn.start()
    else:
        conn = connection

    try:
        state = conn.create_historical_session(
            symbol=symbol,
            timeframe=timeframe,
            target_bars=bars,
            adjustment=adjustment,
            extended_session=extended_session,
        )

        completed = state.complete.wait(timeout=_FETCH_TIMEOUT)

        if not completed:
            raise TvTimeoutError(
                f"Timed out fetching {symbol} at {timeframe} after {_FETCH_TIMEOUT}s"
            )

        if state.error:
            if "series_error" in state.error or "not found" in state.error.lower():
                raise TvSymbolNotFoundError(
                    symbol,
                    hint="Check the exchange prefix is correct, e.g. BINANCE:BTCUSDT not just BTCUSDT",
                )
            raise TvSymbolNotFoundError(symbol, hint=state.error)

        if not state.bars:
            raise TvNoDataError(symbol, timeframe)

        parsed_bars = [Bar.from_tv(v) for v in state.bars]

        result = FetchResult(
            symbol=symbol,
            timeframe=timeframe,
            bars=parsed_bars,
            source="tradingview",
            auth_mode=auth_mode,
        )

        # --- Save to cache after successful fetch ---
        if use_cache:
            try:
                _cache.save(result)
            except Exception as exc:
                log.warning("Cache save failed (non-fatal): %s", exc)

        return result

    except (TvSymbolNotFoundError, TvNoDataError) as primary_error:
        # Attempt fallback sources (Yahoo Finance, CCXT)
        try:
            from tvfetch.fallback import fetch_with_fallback
            return fetch_with_fallback(symbol, timeframe, bars,
                                       primary_result=None, primary_error=primary_error)
        except Exception as fallback_exc:
            log.debug("Fallback also failed: %s", fallback_exc)
            raise primary_error

    finally:
        if own_connection:
            conn.stop()


def fetch_df(
    symbol: str,
    timeframe: str = "1D",
    bars: int = 5000,
    auth_token: str = ANONYMOUS_TOKEN,
    **kwargs,
) -> pd.DataFrame:
    """
    Convenience wrapper — returns a pandas DataFrame directly.

    Same args as fetch(). DataFrame has datetime index and OHLCV columns.

    Example:
        >>> df = fetch_df("NASDAQ:AAPL", "1D", bars=500)
        >>> df.head()
    """
    return fetch(symbol, timeframe, bars, auth_token, **kwargs).df


def fetch_multi(
    symbols: list[str],
    timeframe: str = "1D",
    bars: int = 5000,
    auth_token: str = ANONYMOUS_TOKEN,
    adjustment: str = "splits",
    extended_session: bool = False,
    use_cache: bool = True,
) -> dict[str, FetchResult]:
    """
    Fetch multiple symbols over a single WebSocket connection (much faster than
    calling fetch() in a loop, which opens a new connection for each symbol).

    Returns a dict mapping symbol -> FetchResult.
    Failed symbols are included with empty bars list rather than raising.

    Args:
        symbols:          List of symbols in EXCHANGE:TICKER format
        timeframe:        Bar interval
        bars:             Number of bars to fetch per symbol
        auth_token:       Optional auth token for paid plan access
        adjustment:       Price adjustment mode: "splits", "dividends", "none"
        extended_session: Include pre/after market data (stocks only)
        use_cache:        Check local SQLite cache before fetching (default True)

    Example:
        >>> results = fetch_multi(["BINANCE:BTCUSDT", "BINANCE:ETHUSDT"], "1D")
    """
    auth_mode = "anonymous" if is_anonymous(auth_token) else "token"

    # Check cache for each symbol first; only fetch what's missing/stale
    results: dict[str, FetchResult] = {}
    symbols_to_fetch: list[str] = []

    if use_cache:
        for sym in symbols:
            if _cache.is_fresh(sym, timeframe):
                cached_df = _cache.load(sym, timeframe)
                if cached_df is not None:
                    log.debug("Cache hit for %s/%s", sym, timeframe)
                    cached_bars = [
                        Bar(
                            timestamp=row.Index.to_pydatetime(),
                            open=row.open,
                            high=row.high,
                            low=row.low,
                            close=row.close,
                            volume=row.volume,
                        )
                        for row in cached_df.itertuples()
                    ]
                    results[sym] = FetchResult(sym, timeframe, cached_bars, "cache", auth_mode)
                    continue
            symbols_to_fetch.append(sym)
    else:
        symbols_to_fetch = list(symbols)

    if not symbols_to_fetch:
        return results

    with TvConnection(auth_token) as conn:
        states = {
            sym: conn.create_historical_session(
                sym, timeframe, bars,
                adjustment=adjustment,
                extended_session=extended_session,
            )
            for sym in symbols_to_fetch
        }

        for sym, state in states.items():
            completed = state.complete.wait(timeout=_FETCH_TIMEOUT)
            if not completed:
                log.warning("Timeout fetching %s", sym)
                results[sym] = FetchResult(sym, timeframe, [], "tradingview", auth_mode)
                continue
            if state.error or not state.bars:
                log.warning("No data for %s: %s", sym, state.error)
                results[sym] = FetchResult(sym, timeframe, [], "tradingview", auth_mode)
                continue

            parsed_bars = [Bar.from_tv(v) for v in state.bars]
            result = FetchResult(
                symbol=sym,
                timeframe=timeframe,
                bars=parsed_bars,
                source="tradingview",
                auth_mode=auth_mode,
            )
            results[sym] = result

            if use_cache:
                try:
                    _cache.save(result)
                except Exception as exc:
                    log.warning("Cache save failed for %s (non-fatal): %s", sym, exc)

    return results
