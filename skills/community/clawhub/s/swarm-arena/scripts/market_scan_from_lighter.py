#!/usr/bin/env python3
"""market_scan_from_lighter.py — full per-symbol scan -> complete proposal | null.

Pipeline (SPEC section 5): candles x3 timeframes (5m timing / 1h signal / 4h
trend) + order book + funding + account -> features -> signal -> ATR bracket
(SL = entry -/+ 1.5xATR, TP = entry +/- 2.5xATR) -> confluence -> leverage ->
sizing -> precision -> min-notional suppression -> liquidity check.

Module:  from market_scan_from_lighter import scan_symbol
CLI:     python3 market_scan_from_lighter.py config.json ETH
         python3 market_scan_from_lighter.py config.json ETH --offline fixture.json
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compute_features import compute_features          # noqa: E402
from compute_signal import compute_signal              # noqa: E402
from compute_confluence import compute_confluence      # noqa: E402
from recommend_leverage import recommend_leverage      # noqa: E402
from size_position import size_position                # noqa: E402
from prepare_order import prepare_order                # noqa: E402
from lighter_rest_client import LighterRestClient, LighterAPIError  # noqa: E402

ATR_SL_MULT = 1.5
ATR_TP_MULT = 2.5
CANDLE_COUNT = {"5m": 120, "1h": 120, "4h": 120}
MAX_SPREAD_PCT = 0.01   # book liquidity guard: best bid/ask spread must be < 1%
LIQUIDITY_DEPTH_PCT = 0.005  # depth window: +/-0.5% of mid must cover 3x notional
LIQUIDITY_DEPTH_MULT = 3.0


def build_bracket(side, entry, atr):
    """SL = entry ∓ 1.5xATR, TP = entry ± 2.5xATR (natural R:R ~ 1.67)."""
    if atr is None or atr <= 0:
        return None, None
    if side == "long":
        return entry - ATR_SL_MULT * atr, entry + ATR_TP_MULT * atr
    return entry + ATR_SL_MULT * atr, entry - ATR_TP_MULT * atr


def liquidity_check(book, side, notional):
    """Top-of-book sanity + depth cover within +/-0.5% of mid."""
    bids, asks = book.get("bids") or [], book.get("asks") or []
    if not bids or not asks:
        return False, "empty order book side"
    best_bid, best_ask = bids[0][0], asks[0][0]
    if best_ask <= 0 or best_bid <= 0 or best_ask < best_bid:
        return False, "crossed or empty book"
    mid = (best_bid + best_ask) / 2.0
    if (best_ask - best_bid) / mid > MAX_SPREAD_PCT:
        return False, "spread %.3f%% too wide" % (100.0 * (best_ask - best_bid) / mid)
    # Buying lifts asks; selling hits bids.
    rows = asks if side == "long" else bids
    limit = mid * (1.0 + LIQUIDITY_DEPTH_PCT) if side == "long" else mid * (1.0 - LIQUIDITY_DEPTH_PCT)
    depth_quote = 0.0
    for price, size in rows:
        if (side == "long" and price > limit) or (side == "short" and price < limit):
            break
        depth_quote += price * size
    needed = notional * LIQUIDITY_DEPTH_MULT
    if depth_quote < needed:
        return False, "book depth $%.2f < %.1fx notional $%.2f" % (depth_quote, LIQUIDITY_DEPTH_MULT, notional)
    return True, "spread and depth ok"


def scan_symbol(symbol, config, state=None, client=None, offline=None):
    """Returns a complete proposal dict, or {"decision": "wait", ...}/None."""
    state = state or {}
    client = client or LighterRestClient(base_url=config.get("base_url"),
                                         gateway=config.get("gateway"))
    symbol = symbol.upper()

    if offline:
        candles_by_tf = offline["candles"]
        funding_rate = offline.get("funding_rate")
        market = offline["market"]
        book = offline.get("book") or {"bids": [], "asks": []}
        account = offline.get("account") or {}
    else:
        market = client.get_market(symbol)
        market_id = market["market_id"]
        candles_by_tf = {}
        for tf, count in CANDLE_COUNT.items():
            candles_by_tf[tf] = client.get_candles(market_id, tf, count)
        funding_rate = client.get_funding_rate(market_id=market_id)
        book = client.get_order_book(market_id, limit=50)
        account = {}
        account_index = os.environ.get("LIGHTER_ACCOUNT_INDEX")
        if account_index:
            try:
                raw = client.get_account(int(account_index))
                account = client.account_summary(raw)
            except LighterAPIError:
                account = {}

    try:
        features = {tf: compute_features(candles_by_tf[tf], funding_rate=funding_rate)
                    for tf in ("5m", "1h", "4h")}
    except ValueError as e:
        return {"decision": "wait", "symbol": symbol,
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "reason": "insufficient market data: %s" % e,
                "market_meta": market}
    signal = compute_signal(features)

    base = {
        "symbol": symbol, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "features": features, "signal_result": signal,
        "market": {"last_price": features["1h"]["last_price"],
                   "mark_price": market.get("mark_price"),
                   "funding_rate": funding_rate},
        "market_meta": market,
    }
    if signal["signal"] == "wait":
        base["decision"] = "wait"
        base["reason"] = signal["reason"]
        return base

    side = signal["signal"]
    entry = features["1h"]["last_price"]
    sl, tp = build_bracket(side, entry, features["1h"].get("atr14"))
    if sl is None:
        base["decision"] = "wait"
        base["reason"] = "ATR unavailable for bracket"
        return base

    # --- sizing needs equity: state account -> fetched account -> fallback
    account_state = state.get("account") or {}
    equity = account_state.get("equity") or account.get("equity") \
        or float(config.get("base_value_per_trade", 100)) * 10
    available_margin = account_state.get("available_margin") or account.get("available_margin")

    metrics = state.get("metrics") or {}
    lev_rec = recommend_leverage(
        signal["confidence"],
        min_leverage=config.get("min_leverage", 2),
        max_leverage=config.get("max_leverage", 10),
        high_volatility=features["1h"].get("high_volatility", False),
        effective_cap=metrics.get("effective_leverage_cap"),
    )

    sized = size_position(
        equity=equity,
        risk_pct=config.get("risk_pct_per_trade", 0.01),
        entry_price=entry, stop_loss=sl, leverage=lev_rec["leverage"],
        price_decimals=market["price_decimals"], size_decimals=market["size_decimals"],
        min_base_amount=market["min_base_amount"],
        min_quote_amount=market["min_quote_amount"],
        max_notional=config.get("max_notional_per_trade", 0),
    )
    if sized["suppressed"]:
        base["decision"] = "wait"
        base["reason"] = "sizing suppressed: " + sized["reason"]
        base["sizing"] = sized
        return base

    confluence = compute_confluence(signal, features, {
        "entry_price": entry, "stop_loss": sl, "take_profit": tp,
        "min_reward_risk": config.get("min_reward_risk", 1.5),
        "current_exposure": _current_exposure(state),
        "max_total_exposure": config.get("max_total_exposure", 0),
        "proposed_notional": sized["notional"],
        "open_positions": len(state.get("known_open_positions") or {}),
        "max_concurrent_positions": config.get("max_concurrent_positions", 0),
    })
    if not confluence["enter"]:
        base["decision"] = "wait"
        base["reason"] = confluence["reason"]
        base["confluence"] = confluence
        return base

    liq_ok, liq_reason = (True, "offline fixture (skipped)") if offline else \
        liquidity_check(book, side, sized["notional"])
    if not liq_ok:
        base["decision"] = "wait"
        base["reason"] = "liquidity: " + liq_reason
        base["confluence"] = confluence
        return base

    plan = prepare_order(symbol, side, entry, sl, tp, sized["quantity"],
                         lev_rec["leverage"], sized["notional"], sized["margin"], market)
    base.update({
        "decision": "enter",
        "side": side,
        "confidence": signal["confidence"],
        "confluence": confluence,
        "leverage_rec": lev_rec,
        "sizing": sized,
        "order_plan": plan,
        "liquidity": liq_reason,
        "account": {"equity": equity, "available_margin": available_margin},
        "reason": signal["reason"],
    })
    return base


def _current_exposure(state):
    exposure = 0.0
    for pos in (state.get("known_open_positions") or {}).values():
        exposure += abs(float(pos.get("quantity", 0) or 0) * float(pos.get("entry_price", 0) or 0))
    return exposure


def main(argv=None):
    parser = argparse.ArgumentParser(description="Full market scan -> trade proposal")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("symbol", help="market symbol, e.g. ETH")
    parser.add_argument("--state", default=None, help="state.json path (default: beside config)")
    parser.add_argument("--offline", default=None,
                        help="fixture JSON with candles/market/book/funding_rate (no exchange calls)")
    args = parser.parse_args(argv)

    with open(args.config) as f:
        config = json.load(f)
    state_path = args.state or os.path.join(os.path.dirname(os.path.abspath(args.config)), "state.json")
    state = {}
    if os.path.exists(state_path):
        with open(state_path) as f:
            state = json.load(f)
    offline = None
    if args.offline:
        with open(args.offline) as f:
            offline = json.load(f)
    try:
        proposal = scan_symbol(args.symbol, config, state=state, offline=offline)
    except (LighterAPIError, ValueError, KeyError) as e:
        print(json.dumps({"decision": "error", "symbol": args.symbol.upper(), "reason": str(e)}))
        return 1
    print(json.dumps(proposal, indent=2, default=str))
    return 0 if proposal.get("decision") == "enter" else 2


if __name__ == "__main__":
    sys.exit(main())
