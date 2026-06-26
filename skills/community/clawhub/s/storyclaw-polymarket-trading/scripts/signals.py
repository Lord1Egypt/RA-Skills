#!/usr/bin/env python3
"""
Pluggable signal methods for Polymarket strategies.

Each method signature:
  fn(client, token_id, params) -> (signal, score, mid)
  signal: "BUY" | "SELL" | "PASS"
  score:  float (positive = buy pressure, negative = sell)
  mid:    float | None (current mid price of this token)
"""


def _fetch_book(client, token_id):
    book = client.get_order_book(token_id)
    bids = book.bids or []
    asks = book.asks or []

    mid_resp = client.get_midpoint(token_id)
    mid = float(mid_resp.get("mid", 0.5) if isinstance(mid_resp, dict) else getattr(mid_resp, "mid", 0.5))

    spread_resp = client.get_spread(token_id)
    spread = float(spread_resp.get("spread", 1.0) if isinstance(spread_resp, dict) else getattr(spread_resp, "spread", 1.0))

    return bids, asks, mid, spread


def orderbook_imbalance(client, token_id, params):
    """
    Score from bid/ask volume imbalance × spread tightness.

    Params:
      threshold (float):       min |score| to trigger signal (default 0.15)
      max_entry_price (float): skip if entry price exceeds this (default 0.65)
    """
    threshold = params.get("threshold", 0.15)
    max_entry = params.get("max_entry_price", 0.65)

    try:
        bids, asks, mid, spread = _fetch_book(client, token_id)
    except Exception as e:
        return "PASS", 0.0, None

    bid_vol = sum(float(b.size) for b in bids)
    ask_vol = sum(float(a.size) for a in asks)
    total_vol = bid_vol + ask_vol

    if total_vol < 10:
        return "PASS", 0.0, mid  # too thin

    imbalance = (bid_vol - ask_vol) / total_vol          # [-1, +1]
    spread_score = max(0.0, 1.0 - (spread / 0.10))      # 1=tight, 0=wide
    conviction = 1.0 - abs(mid - 0.5) * 2               # 1=50/50, 0=near resolved

    score = round(imbalance * spread_score * conviction, 4)

    if score > threshold:
        signal = "BUY"
    elif score < -threshold:
        signal = "SELL"
    else:
        signal = "PASS"

    return signal, score, mid


# ── Registry ────────────────────────────────────────────────────────────────

METHODS = {
    "orderbook_imbalance": orderbook_imbalance,
}


def run_signal(client, token_id, method_name, params):
    """Run a named signal method. Returns (signal, score, mid)."""
    fn = METHODS.get(method_name)
    if not fn:
        return "PASS", 0.0, None
    return fn(client, token_id, params)


def list_methods():
    return list(METHODS.keys())
