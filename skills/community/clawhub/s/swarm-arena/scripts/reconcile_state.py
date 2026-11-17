#!/usr/bin/env python3
"""reconcile_state.py — sync state.account + known positions with the venue.

Two modes:
  stdin   cat snapshot.json | python3 reconcile_state.py config.json
          snapshot: {"account": {...raw account...}, "positions": [...]} or a
          raw /api/v1/account account object on its own
  live    python3 reconcile_state.py config.json --live
          fetches account + positions via the REST client (env
          LIGHTER_ACCOUNT_INDEX required)

Writes state.json account {equity, available_margin, daily_pnl(unchanged)},
replaces known_open_positions' quantities/entries with venue truth for symbols
still open, and drops known positions the venue no longer reports (they are
left for position_monitor to close out — this script NEVER journals closes).

CLI: python3 reconcile_state.py config.json [--live]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import journal_trade  # noqa: E402
from lighter_rest_client import LighterRestClient, LighterAPIError  # noqa: E402


def _normalize_positions(raw_positions):
    out = {}
    for p in raw_positions or []:
        size = float(p.get("position", p.get("size", 0)) or 0)
        if size == 0:
            continue
        sign = int(p.get("sign", 1 if size > 0 else -1))
        out[str(p.get("symbol", "")).upper()] = {
            "side": "long" if sign > 0 else "short",
            "quantity": abs(size),
            "entry_price": float(p.get("avg_entry_price", p.get("entry_price", 0)) or 0),
        }
    return out


def reconcile(config, state, account_obj=None, positions=None):
    """Mutates and returns state. Returns (state, notes)."""
    notes = []
    if account_obj:
        collateral = float(account_obj.get("collateral", 0) or 0)
        available = account_obj.get("available_balance")
        account = state.setdefault("account", {})
        account["equity"] = collateral
        account["available_margin"] = float(available) if available not in (None, "") else collateral
        account["updated_at"] = journal_trade.utcnow()
        notes.append("account equity=%.2f available=%.2f"
                     % (account["equity"], account["available_margin"]))
        if positions is None:
            positions = account_obj.get("positions")

    if positions is not None:
        venue = _normalize_positions(positions)
        known = state.setdefault("known_open_positions", {})
        for symbol, vpos in venue.items():
            if symbol in known:
                known[symbol]["quantity"] = vpos["quantity"]
                known[symbol]["side"] = vpos["side"]
                if vpos["entry_price"]:
                    known[symbol]["entry_price"] = vpos["entry_price"]
                notes.append("synced %s %s %.8f" % (symbol, vpos["side"], vpos["quantity"]))
            else:
                notes.append("venue has %s but state does not track it "
                             "(not journaled; left for operator review)" % symbol)
        missing = [s for s in known if s not in venue]
        for symbol in missing:
            notes.append("state tracks %s but venue shows it flat "
                         "(position_monitor will close it out)" % symbol)
    state["last_reconcile"] = journal_trade.utcnow()
    return state, notes


def main(argv=None):
    parser = argparse.ArgumentParser(description="Reconcile state.json with venue account")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("--state", default=None)
    parser.add_argument("--live", action="store_true", help="fetch from the venue")
    args = parser.parse_args(argv)

    with open(args.config) as f:
        config = json.load(f)
    base = os.path.dirname(os.path.abspath(args.config))
    state_path = args.state or os.path.join(base, "state.json")
    state = {}
    if os.path.exists(state_path):
        with open(state_path) as f:
            state = json.load(f)

    account_obj, positions = None, None
    if args.live:
        account_index = os.environ.get("LIGHTER_ACCOUNT_INDEX")
        if not account_index:
            print(json.dumps({"ok": False, "error": "LIGHTER_ACCOUNT_INDEX not set"}))
            return 1
        client = LighterRestClient(base_url=config.get("base_url"),
                                   gateway=config.get("gateway"))
        try:
            account_obj = client.get_account(int(account_index))
            positions = account_obj.get("positions")
        except LighterAPIError as e:
            print(json.dumps({"ok": False, "error": str(e)}))
            return 1
    elif not sys.stdin.isatty():
        snapshot = json.load(sys.stdin)
        if "account" in snapshot or "positions" in snapshot:
            account_obj = snapshot.get("account")
            positions = snapshot.get("positions")
        else:
            account_obj = snapshot  # bare account object
            positions = account_obj.get("positions") if isinstance(account_obj, dict) else None

    import filelock
    with filelock.held(state_path):
        state, notes = reconcile(config, state, account_obj=account_obj, positions=positions)
        tmp = state_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(state, f, indent=2)
            f.write("\n")
        os.replace(tmp, state_path)
    print(json.dumps({"ok": True, "notes": notes}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
