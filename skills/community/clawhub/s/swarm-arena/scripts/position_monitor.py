#!/usr/bin/env python3
"""position_monitor.py — reconcile state.known_open_positions with the venue.

Live/autonomous_live: compares against real positions from the account read.
Paper: marks positions against the current last price — a close is detected
when price touches the recorded stop_loss or take_profit.

On every detected close:
  realized PnL  live: derived from /api/v1/trades matched to the position's
                      close direction after opened_at (fallback: price delta)
                paper: (exit - entry) * qty * side sign
  outcome       win | loss | breakeven (|pnl| < $0.01)
  close_reason  stop_loss | take_profit | trailing_stop | manual | liquidation
  journal       the open entry gets outcome/realised_pnl/close_reason/closed_at
  state         daily_loss += max(0, -pnl); position removed;
                last_close_ts[symbol] = now (drives the cooldown)

Module:  from position_monitor import run_position_monitor
CLI:     python3 position_monitor.py config.json
"""

import argparse
import calendar
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import journal_trade  # noqa: E402
from lighter_rest_client import LighterRestClient, LighterAPIError  # noqa: E402

BREAKEVEN_EPS_USD = 0.01


def _parse_ts(ts):
    if not ts:
        return 0.0
    try:
        return calendar.timegm(time.strptime(ts, "%Y-%m-%dT%H:%M:%SZ"))
    except (ValueError, TypeError):
        return 0.0


def _realized_from_trades(client, account_index, market_id, pos, auth=None):
    """Sum signed PnL of closing trades (reduce-direction) since opened_at."""
    opened_ms = _parse_ts(pos.get("opened_at")) * 1000
    close_side = "sell" if pos.get("side") == "long" else "buy"
    pnl = None
    try:
        trades = client.get_account_trades(account_index, limit=100,
                                           market_id=market_id, auth=auth)
    except LighterAPIError:
        return None
    for t in trades:
        ts_ms = float(t.get("timestamp", 0) or 0)
        if opened_ms and ts_ms and ts_ms < opened_ms:
            continue
        # Taker side identifies direction; account can be maker or taker.
        is_close = _trade_is_close(t, account_index, close_side)
        if not is_close:
            continue
        size = float(t.get("size", 0) or 0)
        price = float(t.get("price", 0) or 0)
        entry = float(pos.get("entry_price", 0) or 0)
        direction = 1 if pos.get("side") == "long" else -1
        chunk = (price - entry) * size * direction
        pnl = (pnl or 0.0) + chunk
    return pnl


def _trade_is_close(trade, account_index, close_side):
    account_index = int(account_index)
    taker_side = "sell" if trade.get("is_maker_ask") else "buy"
    # If our account is the taker, taker side is ours; else infer from ids.
    taker_account = trade.get("ask_account_id") if trade.get("is_maker_ask") else trade.get("bid_account_id")
    if taker_account is not None and int(taker_account) == account_index:
        return taker_side == close_side
    maker_account = trade.get("bid_account_id") if trade.get("is_maker_ask") else trade.get("ask_account_id")
    if maker_account is not None and int(maker_account) == account_index:
        return ("buy" if trade.get("is_maker_ask") else "sell") == close_side
    return False


def _close_position(symbol, pos, exit_price, pnl, reason, state, trades_path):
    outcome = "win" if pnl > BREAKEVEN_EPS_USD else ("loss" if pnl < -BREAKEVEN_EPS_USD else "breakeven")
    closed_at = journal_trade.utcnow()
    journal_trade.update_entry(
        trades_path,
        lambda e: e.get("symbol") == symbol and e.get("decision") == "executed"
        and e.get("status") in ("open", "executed"),
        {"status": "closed", "outcome": outcome, "realised_pnl": round(pnl, 6),
         "close_reason": reason, "closed_at": closed_at},
    )
    if pnl < 0:
        state["daily_loss"] = round(float(state.get("daily_loss", 0) or 0) - pnl, 6)
    account = state.setdefault("account", {})
    if pnl:
        account["daily_pnl"] = round(float(account.get("daily_pnl", 0) or 0) + pnl, 6)
        if account.get("equity") is not None:
            account["equity"] = round(float(account["equity"]) + pnl, 6)
    state.get("known_open_positions", {}).pop(symbol, None)
    # Recompute free margin from equity minus what remaining positions lock;
    # otherwise every close leaks margin until "zero size" blocks all entries.
    remaining = sum(float(p.get("margin") or 0)
                    for p in state.get("known_open_positions", {}).values())
    if account.get("equity") is not None:
        account["available_margin"] = round(float(account["equity"]) - remaining, 6)
    state.setdefault("last_close_ts", {})[symbol] = closed_at
    return {"symbol": symbol, "outcome": outcome, "realised_pnl": round(pnl, 6),
            "close_reason": reason, "closed_at": closed_at, "exit_price": exit_price}


def run_position_monitor(config, state, trades_path, client=None, auth_token=None):
    """Returns {"closed": [...], "still_open": [...], "errors": [...]}."""
    known = dict(state.get("known_open_positions") or {})
    result = {"closed": [], "still_open": [], "errors": []}
    if not known:
        return result
    mode = config.get("mode", "paper")
    client = client or LighterRestClient(base_url=config.get("base_url"),
                                         auth_token=auth_token,
                                         gateway=config.get("gateway"))
    min_hold = int(config.get("minimum_hold_sec", 0) or 0)
    now = time.time()

    if mode in ("live", "autonomous_live"):
        account_index = os.environ.get("LIGHTER_ACCOUNT_INDEX")
        if not account_index:
            result["errors"].append("LIGHTER_ACCOUNT_INDEX not set; cannot reconcile")
            return result
        try:
            live_positions = {p["symbol"].upper(): p
                              for p in client.get_positions(int(account_index), auth=True)}
        except LighterAPIError as e:
            result["errors"].append(str(e))
            return result
        for symbol, pos in known.items():
            if min_hold and now - _parse_ts(pos.get("opened_at")) < min_hold:
                result["still_open"].append(symbol)
                continue
            if symbol in live_positions:
                result["still_open"].append(symbol)
                continue
            market_id = None
            try:
                market_id = client.market_id_for(symbol)
            except LighterAPIError:
                pass
            live_pos = None
            pnl = _realized_from_trades(client, int(account_index), market_id, pos,
                                        auth=True) if market_id is not None else None
            if pnl is None:
                # Fallback: mark vs current price.
                try:
                    last = client.get_market(symbol).get("mark_price") or \
                        client.get_market(symbol).get("last_trade_price")
                    direction = 1 if pos.get("side") == "long" else -1
                    pnl = (last - pos["entry_price"]) * pos["quantity"] * direction
                except (LighterAPIError, TypeError, KeyError) as e:
                    result["errors"].append("%s: cannot price close (%s)" % (symbol, e))
                    continue
            reason = _guess_close_reason(pos, live_pos, exit_price=None)
            result["closed"].append(_close_position(symbol, pos, None, pnl, reason,
                                                    state, trades_path))
        return result

    # ---- paper: mark price vs recorded SL/TP
    for symbol, pos in known.items():
        if min_hold and now - _parse_ts(pos.get("opened_at")) < min_hold:
            result["still_open"].append(symbol)
            continue
        try:
            market = client.get_market(symbol)
        except LighterAPIError as e:
            result["errors"].append("%s: %s" % (symbol, e))
            continue
        last = market.get("mark_price") or market.get("last_trade_price")
        if not last:
            result["errors"].append("%s: no price" % symbol)
            continue
        sl, tp = float(pos["stop_loss"]), float(pos["take_profit"])
        side = pos.get("side")
        hit_sl = (side == "long" and last <= sl) or (side == "short" and last >= sl)
        hit_tp = (side == "long" and last >= tp) or (side == "short" and last <= tp)
        if not (hit_sl or hit_tp):
            result["still_open"].append(symbol)
            continue
        exit_price = sl if hit_sl else tp
        direction = 1 if side == "long" else -1
        pnl = (exit_price - float(pos["entry_price"])) * float(pos["quantity"]) * direction
        reason = "stop_loss" if hit_sl else "take_profit"
        if hit_sl and pos.get("trailing_active"):
            reason = "trailing_stop"
        result["closed"].append(_close_position(symbol, pos, exit_price, pnl, reason,
                                                state, trades_path))
    return result


def _guess_close_reason(pos, live_pos, exit_price=None):
    if exit_price is not None:
        sl, tp = pos.get("stop_loss"), pos.get("take_profit")
        if sl and abs(exit_price - sl) / sl < 0.002:
            return "trailing_stop" if pos.get("trailing_active") else "stop_loss"
        if tp and abs(exit_price - tp) / tp < 0.002:
            return "take_profit"
    return "manual_or_external"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Reconcile open positions, close and journal")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("--state", default=None)
    parser.add_argument("--trades", default=None)
    args = parser.parse_args(argv)
    with open(args.config) as f:
        config = json.load(f)
    base = os.path.dirname(os.path.abspath(args.config))
    state_path = args.state or os.path.join(base, "state.json")
    trades_path = args.trades or os.path.join(base, "trades.json")
    if not os.path.exists(state_path):
        print(json.dumps({"closed": [], "still_open": [], "errors": [], "note": "no state.json yet"}))
        return 0
    import filelock
    with filelock.held(state_path):  # no-op when already held by autonomous_runner
        with open(state_path) as f:
            state = json.load(f)
        result = run_position_monitor(config, state, trades_path)
        tmp = state_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(state, f, indent=2)
            f.write("\n")
        os.replace(tmp, state_path)
    print(json.dumps(result, indent=2, default=str))
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
