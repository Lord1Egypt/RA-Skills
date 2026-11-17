#!/usr/bin/env python3
"""autonomous_runner.py — cron entry point for one full cycle (SPEC section 6).

Cycle order:
  1. validate config (invalid -> error counter, no trading)
  2. halt / circuit-breaker check (either set -> exit quietly, code 3)
  3. daily reset (daily_loss / daily_pnl zeroed when the UTC date rolls over)
  4. position_monitor (reconcile closes, journal, daily_loss)
  5. trade_loop for each allowed symbol
  6. trailing_stop management
  7. persist state (atomic), stamp last_run
  8. every 5 new closed trades -> review + bounded metric update
  9. error accounting: any unhandled error increments consecutive_errors;
     5+ trips the circuit breaker; a clean cycle resets the counter to 0

CLI: python3 autonomous_runner.py config.json [--offline-dir DIR]
"""

import argparse
import json
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import journal_trade                         # noqa: E402
import filelock                              # noqa: E402
from validate_config import validate_config  # noqa: E402
from trade_loop import run_trade_loop        # noqa: E402
from position_monitor import run_position_monitor   # noqa: E402
from trailing_stop import run_trailing_stops        # noqa: E402
from review_trades import review             # noqa: E402
from update_metrics import update_metrics    # noqa: E402

ERROR_TRIP_THRESHOLD = 5
REVIEW_EVERY_N_TRADES = 5


class OfflineClient:
    """Fixture-backed stand-in for LighterRestClient (offline rehearsal only).

    Built from <SYMBOL>.json fixtures: {"candles": {"5m": [...], ...},
    "market": {...}, "book": {...}, "funding_rate": float, "account": {...}}.
    Covers the read methods used by scan / monitor / trailing stops.
    """

    def __init__(self, fixtures):
        self.fixtures = {s.upper(): f for s, f in fixtures.items()}
        self._by_market_id = {}
        for sym, f in self.fixtures.items():
            mid = (f.get("market") or {}).get("market_id")
            if mid is not None:
                self._by_market_id[int(mid)] = sym

    def get_market(self, symbol):
        return dict(self.fixtures[symbol.upper()]["market"])

    def market_id_for(self, symbol):
        return self.get_market(symbol)["market_id"]

    def get_candles(self, market_id, resolution, count_back=100, **_: object):
        sym = self._by_market_id.get(int(market_id))
        candles = (self.fixtures.get(sym) or {}).get("candles", {}).get(resolution, [])
        return list(candles[-int(count_back):]) if count_back else list(candles)

    def get_order_book(self, market_id, limit=50):
        sym = self._by_market_id.get(int(market_id))
        return dict((self.fixtures.get(sym) or {}).get("book") or {"bids": [], "asks": []})

    def get_funding_rate(self, symbol=None, market_id=None):
        sym = symbol.upper() if symbol else self._by_market_id.get(int(market_id))
        return (self.fixtures.get(sym) or {}).get("funding_rate")

    def get_positions(self, account_index, auth=None):
        return []

    def get_account(self, account_index, auth=None):
        for f in self.fixtures.values():
            if f.get("account"):
                return dict(f["account"])
        return {}

    @staticmethod
    def account_summary(account):
        return {"equity": account.get("equity", 0.0),
                "collateral": account.get("equity", 0.0),
                "available_margin": account.get("available_margin", 0.0),
                "unrealized_pnl": 0.0}


def _utc_today():
    return time.strftime("%Y-%m-%d", time.gmtime())


def _daily_reset(state):
    today = _utc_today()
    if state.get("daily_loss_date") != today:
        state["daily_loss"] = 0.0
        state["daily_loss_date"] = today
        if isinstance(state.get("account"), dict):
            state["account"]["daily_pnl"] = 0.0
        return True
    return False


def _save_state(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def _record_error(state, state_path, message):
    state["consecutive_errors"] = int(state.get("consecutive_errors", 0) or 0) + 1
    if state["consecutive_errors"] >= ERROR_TRIP_THRESHOLD:
        state["circuit_breaker"] = True
        message += " | CIRCUIT BREAKER TRIPPED (>= %d consecutive errors)" % ERROR_TRIP_THRESHOLD
    state["last_error"] = {"ts": journal_trade.utcnow(), "message": message}
    try:
        _save_state(state_path, state)
    except OSError:
        pass
    return message


def run_cycle(config_path, offline_dir=None, out=sys.stdout):
    base = os.path.dirname(os.path.abspath(config_path))
    state_path = os.path.join(base, "state.json")
    trades_path = os.path.join(base, "trades.json")
    # One cycle at a time per state file: an overlapping cron run reads stale
    # state and its save would erase positions/journal entries from this one.
    with filelock.held(state_path):
        return _run_cycle(config_path, state_path, trades_path, offline_dir, out)


def _run_cycle(config_path, state_path, trades_path, offline_dir, out):
    with open(config_path) as f:
        config = json.load(f)
    state = {}
    if os.path.exists(state_path):
        with open(state_path) as f:
            state = json.load(f)
    state.setdefault("halt", False)
    state.setdefault("circuit_breaker", False)
    state.setdefault("consecutive_errors", 0)
    state.setdefault("daily_loss", 0.0)
    state.setdefault("known_open_positions", {})
    state.setdefault("metrics", {})

    summary = {"ts": journal_trade.utcnow(), "config": os.path.basename(config_path),
               "mode": config.get("mode", "paper"), "cycles": []}

    verdict = validate_config(config)
    if not verdict["ok"]:
        msg = _record_error(state, state_path, "config invalid: %s" % "; ".join(verdict["errors"]))
        summary["error"] = msg
        print(json.dumps(summary), file=out)
        return 1

    if state.get("halt") or state.get("circuit_breaker"):
        summary["skipped"] = "halt" if state.get("halt") else "circuit_breaker"
        print(json.dumps(summary), file=out)
        return 3

    if _daily_reset(state):
        summary["daily_reset"] = True

    offline = None
    offline_client = None
    if offline_dir:
        offline = {}
        for sym in config.get("allowed_symbols", []):
            fixture = os.path.join(offline_dir, "%s.json" % sym.upper())
            if os.path.exists(fixture):
                with open(fixture) as f:
                    offline[sym.upper()] = json.load(f)
        if offline:
            offline_client = OfflineClient(offline)

    from lighter_rest_client import LighterRestClient
    shared_client = offline_client or LighterRestClient(base_url=config.get("base_url"),
                                                        gateway=config.get("gateway"))

    try:
        monitor = run_position_monitor(config, state, trades_path, client=shared_client)
        summary["position_monitor"] = {"closed": [c["symbol"] for c in monitor["closed"]],
                                       "errors": monitor["errors"]}

        for symbol in config.get("allowed_symbols", []):
            symbol = symbol.upper()
            try:
                result = run_trade_loop(symbol, config, state, state_path,
                                        trades_path, client=shared_client,
                                        offline=offline.get(symbol) if offline else None)
                summary["cycles"].append(result)
            except Exception as e:  # one bad symbol must not kill the cycle
                summary["cycles"].append({"symbol": symbol, "decision": "error",
                                          "reason": str(e)})
                state["consecutive_errors"] = int(state.get("consecutive_errors", 0) or 0) + 1

        trailing = run_trailing_stops(config, state, client=shared_client)
        if trailing["actions"] or trailing["errors"]:
            summary["trailing"] = trailing

        if getattr(shared_client, "gateway_fallback_used", False):
            journal_trade.journal_entry(trades_path, {
                "symbol": "*", "mode": config.get("mode", "paper"),
                "decision": "gateway_fallback", "signal": "wait",
                "signal_reason": "gateway unreachable; used direct venue access "
                                 "(gateway.required is false)",
                "status": "journaled",
            })
            summary["gateway_fallback"] = True

        state["last_run"] = summary["ts"]

        # learning trigger: every 5 newly closed trades
        metrics = state["metrics"]
        closed_total = sum(1 for e in journal_trade.load_journal(trades_path)
                           if e.get("status") == "closed") if os.path.exists(trades_path) else 0
        since_review = int(metrics.get("trades_since_review", 0) or 0)
        new_closed = closed_total - int(metrics.get("closed_at_last_review", 0) or 0)
        if new_closed >= REVIEW_EVERY_N_TRADES or since_review >= REVIEW_EVERY_N_TRADES:
            review_result = review(journal_trade.load_journal(trades_path))
            update_metrics(config, state, review_result)
            state["metrics"]["closed_at_last_review"] = closed_total
            summary["learning"] = {"reviewed": True, "win_rate": review_result["win_rate"],
                                   "total_pnl": review_result["total_pnl"]}
        else:
            state["metrics"]["trades_since_review"] = since_review

        had_errors = bool(summary["position_monitor"]["errors"]
                          or any(c.get("decision") == "error" for c in summary["cycles"])
                          or trailing["errors"])
        if had_errors:
            # Symbol exceptions were already counted one-by-one above; count
            # monitor/trailing failures here, each exactly once.
            extra = (len(summary["position_monitor"]["errors"])
                     + len(trailing["errors"]))
            if extra:
                state["consecutive_errors"] = int(state.get("consecutive_errors", 0) or 0) + extra
            if state["consecutive_errors"] >= ERROR_TRIP_THRESHOLD:
                state["circuit_breaker"] = True
                summary["circuit_breaker"] = "TRIPPED"
        else:
            state["consecutive_errors"] = 0
        _save_state(state_path, state)
        print(json.dumps(summary, default=str), file=out)
        return 0 if not had_errors else 1
    except Exception as e:  # noqa: BLE001 - top-level guard feeds the breaker
        msg = _record_error(state, state_path, "%s: %s" % (type(e).__name__, e))
        traceback.print_exc(file=sys.stderr)
        summary["error"] = msg
        print(json.dumps(summary), file=out)
        return 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="swarmArena autonomous cycle (cron entry)")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("--offline-dir", default=None,
                        help="directory with <SYMBOL>.json fixtures (no exchange calls)")
    args = parser.parse_args(argv)
    return run_cycle(args.config, offline_dir=args.offline_dir)


if __name__ == "__main__":
    sys.exit(main())
