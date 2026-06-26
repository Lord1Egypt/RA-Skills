"""
Real-time live price streaming via TradingView WebSocket.

Uses 'du' (data update) messages — TV pushes the current candle state
every 1-3 seconds as trades happen. This gives you live close price,
running volume, and high/low for the current bar.

No login required. Works for any symbol TradingView supports.
"""

from __future__ import annotations

import logging
import time
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from tvfetch.auth import ANONYMOUS_TOKEN
from tvfetch.core.connection import TvConnection
from tvfetch.core import messages as msgs
from tvfetch.exceptions import TvConnectionError

log = logging.getLogger(__name__)


@dataclass
class LiveBar:
    """Current state of the live candle being streamed."""

    symbol: str
    timestamp: datetime    # bar open time
    open: float
    high: float
    low: float
    close: float           # current price (updates every tick)
    volume: float          # accumulated volume for this bar
    bar_close_time: datetime | None = None  # when this bar will close

    @property
    def change(self) -> float:
        """Price change from bar open to current close."""
        return self.close - self.open

    @property
    def change_pct(self) -> float:
        """Percent change from bar open."""
        return (self.change / self.open * 100) if self.open else 0.0

    def __repr__(self) -> str:
        direction = "+" if self.change >= 0 else ""
        return (
            f"LiveBar({self.symbol}  {self.close:.4f}  "
            f"{direction}{self.change_pct:.2f}%  vol={self.volume:.4f})"
        )


OnBarCallback = Callable[[LiveBar], None]


class LiveStream:
    """
    Streams real-time price updates for one or more symbols.

    Each time a trade happens on TradingView, the current candle
    is updated and your callback is called with the new LiveBar.

    Usage:
        def on_update(bar: LiveBar):
            print(bar)

        stream = LiveStream(["BINANCE:BTCUSDT", "FX:EURUSD"])
        stream.on_update(on_update)
        stream.start()
        # ... runs until stream.stop() is called
    """

    def __init__(
        self,
        symbols: list[str],
        timeframe: str = "1",
        auth_token: str = ANONYMOUS_TOKEN,
        adjustment: str = "splits",
    ) -> None:
        self.symbols = symbols
        self.timeframe = timeframe
        self._auth = auth_token
        self._adjustment = adjustment
        self._callbacks: list[OnBarCallback] = []
        self._conn: TvConnection | None = None
        self._session_to_symbol: dict[str, str] = {}
        self._session_ids: list[str] = []   # track all active session IDs for cleanup
        self._running = False

    def on_update(self, callback: OnBarCallback) -> "LiveStream":
        """Register a callback to be called on every price update. Chainable."""
        self._callbacks.append(callback)
        return self

    def start(self, block: bool = False) -> "LiveStream":
        """
        Start streaming.

        Args:
            block: If True, block the calling thread (useful for scripts).
                   If False (default), stream runs in background thread.
        """
        if self._running:
            return self

        self._conn = TvConnection(self._auth)
        self._conn.start()
        self._running = True
        self._session_ids = []

        for sym in self.symbols:
            state = self._conn.create_live_session(
                symbol=sym,
                timeframe=self.timeframe,
                callback=self._make_handler(sym),
                adjustment=self._adjustment,
            )
            self._session_to_symbol[state.session_id] = sym
            self._session_ids.append(state.session_id)

        log.info("LiveStream started for: %s", ", ".join(self.symbols))

        if block:
            try:
                while self._running:
                    time.sleep(0.5)
            except KeyboardInterrupt:
                self.stop()

        return self

    def stop(self) -> None:
        """Stop streaming, close all active sessions, and shut down the connection."""
        self._running = False
        if self._conn:
            # Explicitly close each TV chart session before dropping the connection
            for session_id in list(self._session_ids):
                try:
                    self._conn.close_session(session_id)
                except Exception as exc:
                    log.debug("Error closing session %s: %s", session_id, exc)
            self._session_ids = []
            self._session_to_symbol = {}
            self._conn.stop()
            self._conn = None
        log.info("LiveStream stopped")

    def __enter__(self) -> "LiveStream":
        self.start()
        return self

    def __exit__(self, *_) -> None:
        self.stop()

    def _make_handler(self, symbol: str) -> Callable[[list], None]:
        """Create a raw-bar handler that converts to LiveBar and calls user callbacks."""
        def handler(raw: list) -> None:
            if not self._callbacks:
                return
            try:
                ts, o, h, l, c, v = (float(x) for x in raw[:6])
                bar = LiveBar(
                    symbol=symbol,
                    timestamp=datetime.fromtimestamp(ts, tz=timezone.utc),
                    open=o, high=h, low=l, close=c, volume=v,
                )
                for cb in self._callbacks:
                    cb(bar)
            except Exception as exc:
                log.warning("LiveBar handler error: %s", exc)

        return handler


def stream(
    symbols: list[str] | str,
    on_update: OnBarCallback,
    timeframe: str = "1",
    auth_token: str = ANONYMOUS_TOKEN,
    duration: float | None = None,
) -> LiveStream:
    """
    Convenience function to start a live stream.

    Args:
        symbols:   Symbol or list of symbols to stream
        on_update: Callback called on every price update
        timeframe: Bar interval (default "1" = 1 minute)
        auth_token: Optional auth token
        duration:  Stop after N seconds (None = run forever until Ctrl+C)

    Returns:
        The running LiveStream instance (can be .stop()-ped)

    Example:
        def handle(bar):
            print(f"{bar.symbol}: {bar.close:.2f}")

        stream(["BINANCE:BTCUSDT", "FX:EURUSD"], on_update=handle)
    """
    if isinstance(symbols, str):
        symbols = [symbols]

    ls = LiveStream(symbols, timeframe=timeframe, auth_token=auth_token)
    ls.on_update(on_update)

    if duration is not None:
        ls.start(block=False)
        try:
            time.sleep(duration)
        finally:
            ls.stop()
    else:
        ls.start(block=True)

    return ls
