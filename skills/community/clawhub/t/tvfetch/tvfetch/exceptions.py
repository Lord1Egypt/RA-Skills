"""Custom exceptions for tvfetch. Every failure has a distinct type and helpful message."""

from __future__ import annotations


class TvFetchError(Exception):
    """Base exception for all tvfetch errors."""


class TvConnectionError(TvFetchError):
    """Could not establish or maintain WebSocket connection to TradingView."""


class TvAuthError(TvFetchError):
    """Authentication failed. Token may be invalid or expired."""


class TvSymbolNotFoundError(TvFetchError):
    """Symbol does not exist on TradingView or on the specified exchange."""

    def __init__(self, symbol: str, hint: str = ""):
        msg = f"Symbol not found: {symbol}"
        if hint:
            msg += f". {hint}"
        super().__init__(msg)
        self.symbol = symbol


class TvNoDataError(TvFetchError):
    """Symbol exists but TradingView has no data for this timeframe/date range."""

    def __init__(self, symbol: str, timeframe: str):
        super().__init__(
            f"No data available for {symbol} at timeframe '{timeframe}'. "
            "Try a larger timeframe or check the symbol is actively traded."
        )
        self.symbol = symbol
        self.timeframe = timeframe


class TvRateLimitError(TvFetchError):
    """Request was rate-limited by TradingView. Wait before retrying."""


class TvTimeoutError(TvFetchError):
    """Request timed out waiting for TradingView response."""


class TvFallbackExhaustedError(TvFetchError):
    """All data sources (TradingView + fallbacks) failed for this symbol."""
