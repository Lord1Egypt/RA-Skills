"""
TvConnection — manages one persistent WebSocket connection to TradingView.

Multiple chart sessions (fetches) can run concurrently over a single connection.
Heartbeats are handled automatically. On unexpected disconnection the connection
attempts to reconnect with exponential backoff and re-subscribes all active sessions.
"""

from __future__ import annotations

import logging
import time
import threading
from dataclasses import dataclass, field
from typing import Callable

import websocket

from tvfetch.core import messages as msgs
from tvfetch.core import protocol
from tvfetch.exceptions import TvConnectionError

log = logging.getLogger(__name__)

WS_URL = "wss://data.tradingview.com/socket.io/websocket"
WS_HEADERS = [
    "Origin: https://www.tradingview.com",
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]
CONNECT_TIMEOUT = 15   # seconds to wait for initial connection
BATCH_SIZE = 5000      # bars per request_more_data call
_MAX_RECONNECT_ATTEMPTS = 5


@dataclass
class _SessionState:
    """State for one in-flight chart session (one fetch)."""
    session_id: str
    symbol: str
    timeframe: str
    target_bars: int
    adjustment: str
    extended_session: bool

    bars: list[list] = field(default_factory=list)
    complete: threading.Event = field(default_factory=threading.Event)
    error: str | None = None
    count_before_batch: int = 0

    # For live sessions: never complete, call this instead
    live_callback: Callable[[list], None] | None = None


class TvConnection:
    """
    Low-level TradingView WebSocket connection.

    Handles:
    - Connection lifecycle (open, close, reconnect)
    - Heartbeat protocol
    - Message routing to sessions by session_id
    - Pagination via request_more_data
    - Auto-reconnect with exponential backoff on unexpected disconnection
    """

    def __init__(self, auth_token: str = "unauthorized_user_token") -> None:
        self._auth = auth_token
        self._ws: websocket.WebSocketApp | None = None
        self._thread: threading.Thread | None = None
        self._ready = threading.Event()
        self._sessions: dict[str, _SessionState] = {}
        self._lock = threading.Lock()
        self._closed = False

    # ── Public API ────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Open WebSocket and block until authenticated."""
        self._ws = self._build_ws_app()
        self._thread = threading.Thread(
            target=self._ws.run_forever,
            kwargs={"ping_interval": 0},
            daemon=True,
            name="tvfetch-ws",
        )
        self._thread.start()

        if not self._ready.wait(timeout=CONNECT_TIMEOUT):
            self.stop()
            raise TvConnectionError(
                f"Could not connect to TradingView within {CONNECT_TIMEOUT}s. "
                "Check your internet connection."
            )
        log.debug("TvConnection ready (auth=%s)", self._auth[:20])

    def stop(self) -> None:
        """Close the WebSocket connection and wait for the thread to finish."""
        self._closed = True
        if self._ws:
            self._ws.close()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
        self._thread = None

    def send(self, data: str) -> None:
        """Send a framed message over the WebSocket."""
        if self._ws and not self._closed:
            try:
                self._ws.send(data)
            except Exception as exc:
                log.warning("Send failed: %s", exc)

    def create_historical_session(
        self,
        symbol: str,
        timeframe: str,
        target_bars: int,
        adjustment: str = "splits",
        extended_session: bool = False,
    ) -> _SessionState:
        """Register a historical data session and kick off symbol resolution."""
        sess_id = msgs.new_chart_session()
        state = _SessionState(
            session_id=sess_id,
            symbol=symbol,
            timeframe=timeframe,
            target_bars=target_bars,
            adjustment=adjustment,
            extended_session=extended_session,
        )
        with self._lock:
            self._sessions[sess_id] = state

        self.send(msgs.chart_create_session(sess_id))
        self.send(msgs.resolve_symbol(sess_id, symbol, adjustment, extended_session))
        return state

    def create_live_session(
        self,
        symbol: str,
        timeframe: str,
        callback: Callable[[list], None],
        adjustment: str = "splits",
    ) -> _SessionState:
        """Register a live streaming session. Callback receives raw bar list [ts,o,h,l,c,v]."""
        sess_id = msgs.new_chart_session()
        state = _SessionState(
            session_id=sess_id,
            symbol=symbol,
            timeframe=timeframe,
            target_bars=1,
            adjustment=adjustment,
            extended_session=False,
            live_callback=callback,
        )
        with self._lock:
            self._sessions[sess_id] = state

        self.send(msgs.chart_create_session(sess_id))
        self.send(msgs.resolve_symbol(sess_id, symbol, adjustment))
        return state

    def close_session(self, session_id: str) -> None:
        """Remove a session and clean up the chart on TradingView's side."""
        with self._lock:
            self._sessions.pop(session_id, None)
        self.send(msgs.delete_session(session_id))

    # ── Context manager ───────────────────────────────────────────────────────

    def __enter__(self) -> "TvConnection":
        self.start()
        return self

    def __exit__(self, *_) -> None:
        self.stop()

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _build_ws_app(self) -> websocket.WebSocketApp:
        """Construct a new WebSocketApp with the current callbacks."""
        return websocket.WebSocketApp(
            WS_URL,
            header=WS_HEADERS,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )

    def _resubscribe_all(self) -> None:
        """Re-send chart session setup for every active session after reconnect."""
        with self._lock:
            active = list(self._sessions.values())
        for state in active:
            log.debug("Re-subscribing session %s for %s", state.session_id, state.symbol)
            self.send(msgs.chart_create_session(state.session_id))
            self.send(msgs.resolve_symbol(
                state.session_id, state.symbol,
                state.adjustment, state.extended_session,
            ))

    def _fail_all_sessions(self, reason: str) -> None:
        """Mark every pending session as failed (called when reconnect gives up)."""
        with self._lock:
            for state in self._sessions.values():
                if not state.complete.is_set():
                    state.error = reason
                    state.complete.set()

    def _reconnect(self, attempt: int = 0) -> None:
        """Reconnect with exponential backoff. Called from _on_close on unexpected drops."""
        if self._closed:
            return
        if attempt >= _MAX_RECONNECT_ATTEMPTS:
            log.error("Reconnect failed after %d attempts — giving up", _MAX_RECONNECT_ATTEMPTS)
            self._fail_all_sessions(
                f"Connection lost after {_MAX_RECONNECT_ATTEMPTS} reconnect attempts"
            )
            return

        delay = 2 ** attempt
        log.info("Reconnecting in %ds (attempt %d/%d)…",
                 delay, attempt + 1, _MAX_RECONNECT_ATTEMPTS)
        time.sleep(delay)

        try:
            self._ready.clear()
            self._ws = self._build_ws_app()
            self._thread = threading.Thread(
                target=self._ws.run_forever,
                kwargs={"ping_interval": 0},
                daemon=True,
                name="tvfetch-ws",
            )
            self._thread.start()

            if not self._ready.wait(timeout=CONNECT_TIMEOUT):
                raise TvConnectionError("Reconnect timed out waiting for ready signal")

            log.info("Reconnected successfully on attempt %d", attempt + 1)
            self._resubscribe_all()

        except Exception as exc:
            log.warning("Reconnect attempt %d failed: %s", attempt + 1, exc)
            self._reconnect(attempt + 1)

    # ── WebSocket callbacks ───────────────────────────────────────────────────

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        ws.send(msgs.auth(self._auth))
        ws.send(msgs.locale())
        self._ready.set()
        log.debug("WebSocket opened and authenticated")

    def _on_message(self, ws: websocket.WebSocketApp, raw: str) -> None:
        # Heartbeat must be echoed immediately
        if protocol.is_heartbeat(raw):
            reply = protocol.extract_heartbeat(raw)
            if reply:
                try:
                    ws.send(reply)
                except Exception as exc:
                    log.warning("Heartbeat echo failed: %s", exc)
            return

        for msg in protocol.decode_json(raw):
            self._route(msg)

    def _on_error(self, ws: websocket.WebSocketApp, error: Exception) -> None:
        log.warning("WebSocket error: %s", error)
        # Unblock any waiting sessions
        with self._lock:
            for state in self._sessions.values():
                if not state.complete.is_set():
                    state.error = str(error)
                    state.complete.set()

    def _on_close(self, ws: websocket.WebSocketApp, code: int | None, msg: str | None) -> None:
        log.debug("WebSocket closed (code=%s)", code)
        self._ready.clear()

        if self._closed:
            # Intentional close — unblock any waiting sessions normally
            with self._lock:
                for state in self._sessions.values():
                    if not state.complete.is_set() and state.error is None:
                        state.error = f"Connection closed (code={code})"
                        state.complete.set()
        else:
            # Unexpected close — attempt reconnect in background thread
            log.warning("Unexpected WebSocket close (code=%s) — attempting reconnect", code)
            t = threading.Thread(target=self._reconnect, daemon=True, name="tvfetch-reconnect")
            t.start()

    # ── Message routing ───────────────────────────────────────────────────────

    def _route(self, msg: dict) -> None:
        mtype: str = msg.get("m", "")
        payload: list = msg.get("p", [])

        # Session ID is always payload[0] for chart session messages
        sess_id = payload[0] if payload else None
        if not sess_id:
            return

        with self._lock:
            state = self._sessions.get(sess_id)

        if state is None:
            return

        if mtype == "symbol_resolved":
            self._handle_symbol_resolved(state)

        elif mtype == "timescale_update":
            self._handle_timescale_update(state, payload)

        elif mtype == "du":
            self._handle_data_update(state, payload)

        elif mtype == "series_completed":
            self._handle_series_completed(state)

        elif mtype == "series_error":
            err = str(payload[1]) if len(payload) > 1 else "unknown"
            state.error = f"series_error: {err}"
            state.complete.set()
            with self._lock:
                self._sessions.pop(sess_id, None)
            log.debug("series_error for %s: %s", state.symbol, err)

        elif mtype == "critical_error":
            err = str(payload[0]) if payload else "unknown"
            log.debug("critical_error (ignored for session %s): %s", sess_id, err)

    def _handle_symbol_resolved(self, state: _SessionState) -> None:
        """Symbol resolved — kick off the data series."""
        log.debug("Symbol resolved: %s", state.symbol)
        state.count_before_batch = 0
        self.send(msgs.create_series(
            state.session_id,
            state.timeframe,
            min(BATCH_SIZE, state.target_bars),
        ))

    def _handle_timescale_update(self, state: _SessionState, payload: list) -> None:
        """Accumulate OHLCV bars arriving from TV."""
        try:
            raw_bars = payload[1].get("sds_1", {}).get("s", [])
            for bar in raw_bars:
                v = bar.get("v", [])
                if len(v) >= 6:
                    state.bars.append(v)
        except (IndexError, AttributeError, TypeError) as exc:
            log.debug("timescale_update parse error: %s", exc)

    def _handle_data_update(self, state: _SessionState, payload: list) -> None:
        """Handle live 'du' (data update) — current bar changed."""
        if state.live_callback is None:
            return
        try:
            raw_bars = payload[1].get("sds_1", {}).get("s", [])
            if raw_bars:
                v = raw_bars[-1].get("v", [])
                if len(v) >= 6:
                    state.live_callback(v)
        except (IndexError, AttributeError, TypeError) as exc:
            log.debug("data_update parse error: %s", exc)

    def _handle_series_completed(self, state: _SessionState) -> None:
        """series_completed — decide whether to paginate or finish."""
        if state.live_callback is not None:
            # Live session: series_completed means streaming started, don't stop
            return

        total = len(state.bars)
        batch_got = total - state.count_before_batch

        if batch_got < BATCH_SIZE or total >= state.target_bars:
            # Reached data limit or requested bar count — we're done
            log.debug(
                "series_completed for %s: %d bars (batch_got=%d)",
                state.symbol, total, batch_got,
            )
            state.complete.set()
            with self._lock:
                self._sessions.pop(state.session_id, None)
        else:
            # More data available — paginate back further
            remaining = state.target_bars - total
            next_batch = min(BATCH_SIZE, remaining)
            state.count_before_batch = total
            log.debug(
                "Paginating %s: %d bars so far, requesting %d more",
                state.symbol, total, next_batch,
            )
            self.send(msgs.request_more_data(state.session_id, next_batch))
