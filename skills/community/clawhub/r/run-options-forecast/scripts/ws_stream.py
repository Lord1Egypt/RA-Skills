"""
LSE Options WebSocket Streaming Client
======================================
Real-time options flow via WebSocket with tick aggregation.

Protocol:
  connect wss://data-ws.londonstrategicedge.com
  <- {"type": "welcome"}
  -> {"action": "auth", "api_key": "<KEY>"}
  <- {"type": "authenticated", "tier": "...", "symbols": [...]}
  -> {"action": "subscribe_options", "underlying": "MU"}
  <- {"type": "options_subscribed", "contracts": N, ...}
  <- {"type": "tick", "symbol": "OSI_TICKER", "price":.., "volume":.., ...}

Replay mode (for off-hours testing):
  -> {"action": "subscribe_options", "underlying": "MU", "start": "2026-07-24T13:00:00"}
  <- {"type": "replay_started"}
  <- ticks with "replay": true
  <- {"type": "replay_complete"}
  <- live ticks (if market open)
"""
from __future__ import annotations

import os
import json
import time
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable

import websocket
from dotenv import load_dotenv

load_dotenv()

WS_URL = "wss://data-ws.londonstrategicedge.com"
PING_INTERVAL = 20
PING_TIMEOUT = 10
DEFAULT_REPLAY_HOURS = 24


@dataclass
class OptionTick:
    """Parsed options tick from the WebSocket stream."""
    ticker: str
    underlying: str
    strike: float
    expiry: str
    contract_type: str
    price: float
    volume: int
    bid: float | None
    ask: float | None
    iv: float | None
    delta: float | None
    gamma: float | None
    theta: float | None
    vega: float | None
    underlying_price: float | None
    ts: str
    replay: bool = False

    @classmethod
    def from_ws(cls, msg: dict) -> "OptionTick | None":
        """Parse a WS tick message. Returns None if not an options tick."""
        if msg.get("type") != "tick":
            return None
        symbol = msg.get("symbol", "")
        underlying = msg.get("underlying") or msg.get("name", "")

        parsed = cls(
            ticker=symbol,
            underlying=underlying,
            strike=float(msg.get("strike", 0)),
            expiry=msg.get("expiry", ""),
            contract_type=msg.get("contract_type", msg.get("type_field", "")),
            price=float(msg.get("price", 0)),
            volume=int(msg.get("volume", 0)),
            bid=msg.get("bid"),
            ask=msg.get("ask"),
            iv=msg.get("iv"),
            delta=msg.get("delta"),
            gamma=msg.get("gamma"),
            theta=msg.get("theta"),
            vega=msg.get("vega"),
            underlying_price=msg.get("underlying_price"),
            ts=msg.get("ts", ""),
            replay=bool(msg.get("replay", False)),
        )
        return parsed


@dataclass
class FlowState:
    """
    Running aggregation of options flow ticks.
    Updated incrementally as new ticks arrive.
    """
    ticks: list[OptionTick] = field(default_factory=list)
    by_strike: dict[float, dict] = field(default_factory=dict)
    total_call_vol: int = 0
    total_put_vol: int = 0
    total_call_prem: float = 0.0
    total_put_prem: float = 0.0
    latest_spot: float = 0.0
    tick_count: int = 0

    def add_tick(self, tick: OptionTick):
        self.ticks.append(tick)
        self.tick_count += 1

        if tick.underlying_price:
            self.latest_spot = tick.underlying_price

        prem = tick.price * tick.volume * 100
        vol = tick.volume

        s = round(tick.strike, 2)
        d = self.by_strike.setdefault(s, {
            "call_vol": 0, "put_vol": 0,
            "call_prem": 0.0, "put_prem": 0.0,
            "latest_iv": None, "latest_delta": None,
            "latest_gamma": None,
            "contract_type": tick.contract_type,
            "expiry": tick.expiry,
        })

        if tick.contract_type == "call":
            self.total_call_vol += vol
            self.total_call_prem += prem
            d["call_vol"] += vol
            d["call_prem"] += prem
        else:
            self.total_put_vol += vol
            self.total_put_prem += prem
            d["put_vol"] += vol
            d["put_prem"] += prem

        if tick.iv is not None:
            d["latest_iv"] = tick.iv
        if tick.delta is not None:
            d["latest_delta"] = tick.delta
        if tick.gamma is not None:
            d["latest_gamma"] = tick.gamma

    def to_flow_list(self) -> list[dict]:
        """Convert aggregated state to the flow-list format used by lse_options."""
        flow = []
        for t in self.ticks:
            flow.append({
                "ticker": t.ticker,
                "underlying": t.underlying,
                "strike": t.strike,
                "expiry": t.expiry,
                "contract_type": t.contract_type,
                "last_price": t.price,
                "volume": t.volume,
                "premium": t.price * t.volume * 100,
                "iv": t.iv,
                "delta": t.delta,
                "gamma": t.gamma,
                "theta": t.theta,
                "vega": t.vega,
                "underlying_price": t.underlying_price,
                "ts": t.ts,
            })
        return flow


class LSEOptionsStream:
    """
    WebSocket client for LSE options streaming.

    Usage:
        stream = LSEOptionsStream()
        stream.on_tick = my_callback  # called per tick
        stream.on_state_update = my_callback  # called every N ticks
        stream.connect("MU", replay_hours=24)  # blocks
    """

    def __init__(self, api_key: str | None = None):
        self._key = api_key or os.environ.get("LONDON_STRATEGIC_EDGE_API_KEY")
        if not self._key:
            raise ValueError("LONDON_STRATEGIC_EDGE_API_KEY not set")

        self.state = FlowState()
        self.on_tick: Callable[[OptionTick], None] | None = None
        self.on_state_update: Callable[[FlowState], None] | None = None
        self.on_status: Callable[[str], None] | None = None

        self._ws: websocket.WebSocketApp | None = None
        self._update_interval = 50
        self._stop_flag = threading.Event()
        self._pending_subscribe: dict | None = None

    def _log(self, msg: str):
        if self.on_status:
            self.on_status(msg)

    def _on_open(self, ws):
        self._log(f"Connected to {WS_URL}")

    def _on_message(self, ws, message):
        msg = json.loads(message)
        mtype = msg.get("type", "")

        if mtype == "welcome":
            self._log("Authenticating...")
            ws.send(json.dumps({"action": "auth", "api_key": self._key}))

        elif mtype == "authenticated":
            tier = msg.get("tier", "?")
            syms = msg.get("symbols", [])
            self._log(f"Authenticated (tier={tier}, {len(syms)} symbols)")
            if self._pending_subscribe:
                ws.send(json.dumps(self._pending_subscribe))
                self._log(f"Subscribed to {self._pending_subscribe.get('underlying', '?')}")
                self._pending_subscribe = None

        elif mtype == "options_subscribed":
            contracts = msg.get("contracts", 0)
            self._log(f"Subscribed: {contracts} contracts")

        elif mtype == "replay_started":
            self._log("Replay started...")

        elif mtype == "replay_complete":
            self._log("Replay complete. Transitioning to live.")

        elif mtype == "tick":
            tick = OptionTick.from_ws(msg)
            if tick and tick.strike > 0:
                self.state.add_tick(tick)
                if self.on_tick:
                    self.on_tick(tick)
                if self.state.tick_count % self._update_interval == 0:
                    if self.on_state_update:
                        self.on_state_update(self.state)

        elif mtype == "error":
            self._log(f"ERROR: {msg}")

    def _on_error(self, ws, error):
        self._log(f"WS error: {error}")

    def _on_close(self, ws, code, msg):
        self._log(f"Disconnected (code={code})")

    def connect(
        self,
        underlying: str,
        replay_hours: int | None = DEFAULT_REPLAY_HOURS,
        duration: float | None = None,
    ):
        """
        Connect and stream options data.

        Args:
            underlying: ticker symbol (e.g. "MU")
            replay_hours: hours of history to replay (max 24). None = live only.
            duration: max seconds to run before auto-disconnect. None = run forever.
        """
        self._stop_flag.clear()

        sub_msg = {"action": "subscribe_options", "underlying": underlying}
        if replay_hours:
            start = (datetime.utcnow() - timedelta(hours=replay_hours)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
            sub_msg["start"] = start
            self._log(f"Queuing subscribe to {underlying} (replay from {start})")
        else:
            self._log(f"Queuing subscribe to {underlying} (live only)")
        self._pending_subscribe = sub_msg

        if duration:
            def stop_timer():
                self._stop_flag.wait(duration)
                if not self._stop_flag.is_set():
                    self._log(f"Auto-disconnect after {duration}s")
                    if self._ws:
                        self._ws.close()
            threading.Thread(target=stop_timer, daemon=True).start()

        self._ws = websocket.WebSocketApp(
            WS_URL,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self._ws.run_forever(ping_interval=PING_INTERVAL, ping_timeout=PING_TIMEOUT)

    def disconnect(self):
        self._stop_flag.set()
        if self._ws:
            self._ws.close()
