#!/usr/bin/env python3
"""
Signal cron worker — general-purpose strategy runner.

Runs on a schedule (e.g. every 15 minutes). For each active strategy:
  1. Scans markets matching the strategy filter
  2. Runs the configured signal method on each candidate token
  3. Records dry-run orders (or executes live trades)
  4. Notifies user of signals and actions

Usage (from cron):
  USER_ID=abc123 python3 /path/to/signal_cron.py [strategy_id]

If strategy_id is omitted, runs all active strategies for the user.

Performance data stored at:
  state/{user_id}.{strategy_id}.perf.json
"""

import sys
import os
import json
import time
import uuid
import subprocess

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from strategy_manager import (
    get_user_id, list_strategies, load_strategy,
    load_perf, perf_path, notify, compute_stats,
)
from market_scanner import scan_markets
import signals as signal_lib


# ── CLOB client ──────────────────────────────────────────────────────────────

def get_clob_client(user_id):
    """Load credentials and return a level-0 CLOB client."""
    cred_path = os.path.join(SKILL_DIR, "credentials", f"{user_id}.json")
    if not os.path.exists(cred_path):
        return None
    with open(cred_path) as f:
        cfg = json.load(f)
    from py_clob_client.client import ClobClient
    return ClobClient(
        "https://clob.polymarket.com",
        chain_id=137,
        key=cfg.get("private_key"),
    )


# ── Performance recording ────────────────────────────────────────────────────

def load_perf_full(user_id, strategy_id):
    p = perf_path(user_id, strategy_id)
    default = {"pending": [], "settled": []}
    if not os.path.exists(p):
        return default
    with open(p) as f:
        return json.load(f)


def save_perf(user_id, strategy_id, perf):
    with open(perf_path(user_id, strategy_id), "w") as f:
        json.dump(perf, f, indent=2)


def record_dry_run(perf, strategy, market, token_id, outcome, entry_price, size):
    order = {
        "id": str(uuid.uuid4())[:8],
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "strategy_id": strategy["id"],
        "strategy_version": strategy["version"],
        "market_name": market["name"][:60],
        "token_id": token_id,
        "outcome": outcome,
        "side": "BUY",
        "size": size,
        "entry_price": entry_price,
        "end_ts": market["end_ts"],
        "resolved": False,
    }
    perf["pending"].append(order)
    return order


# ── Settlement ───────────────────────────────────────────────────────────────

def settle_pending(user_id, strategy_id, perf, client):
    """Settle expired dry-run orders via Gamma API outcomePrices."""
    import urllib.request

    now = int(time.time())
    still_pending = []
    newly_settled = []

    for order in perf.get("pending", []):
        end_ts = order.get("end_ts", 0)
        if now < end_ts:
            still_pending.append(order)
            continue

        # Try Gamma API for resolution
        token_id = order["token_id"]
        resolution = None
        try:
            url = f"https://gamma-api.polymarket.com/markets?clob_token_ids={token_id}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read())
            if data:
                gm = data[0]
                prices = json.loads(gm.get("outcomePrices", "[]"))
                ids = json.loads(gm.get("clobTokenIds", "[]"))
                if token_id in ids and prices:
                    idx = ids.index(token_id)
                    p = float(prices[idx])
                    if p > 0.95:
                        resolution = 1.0
                    elif p < 0.05:
                        resolution = 0.0
        except Exception:
            pass

        if resolution is None:
            still_pending.append(order)
            continue

        entry = order.get("entry_price", 0.5)
        size = order.get("size", 10)
        pnl = round((resolution - entry) * size, 4)
        settled_order = {**order, "resolved": True, "resolution": resolution, "pnl": pnl}
        newly_settled.append(settled_order)
        perf["settled"].append(settled_order)

    perf["pending"] = still_pending
    return newly_settled


# ── Main loop ────────────────────────────────────────────────────────────────

def run_strategy(user_id, strategy, client):
    strategy_id = strategy["id"]
    perf = load_perf_full(user_id, strategy_id)

    report_lines = [f"📡 {strategy['name']} — {time.strftime('%H:%M UTC', time.gmtime())}"]

    # Settle expired orders first
    newly_settled = settle_pending(user_id, strategy_id, perf, client)
    if newly_settled:
        wins = sum(1 for o in newly_settled if o.get("pnl", 0) > 0)
        total_pnl = sum(o.get("pnl", 0) for o in newly_settled)
        report_lines.append(f"  📋 Settled {len(newly_settled)} orders: {wins}W {len(newly_settled)-wins}L  ({'+' if total_pnl>=0 else ''}{total_pnl:.2f} USDC)")

    # Scan for markets
    markets = scan_markets(strategy["market_filter"])
    if not markets:
        report_lines.append("  ⚠️ No markets found matching filter")
        save_perf(user_id, strategy_id, perf)
        print("\n".join(report_lines))
        return

    # Signal check on top markets (limit to avoid API spam)
    method = strategy["signal"]["method"]
    params = strategy["signal"]["params"]
    max_entry = params.get("max_entry_price", 0.65)
    size = strategy["sizing"].get("max_size_usdc", 10)
    dry_run = strategy.get("status") != "live"

    checked = 0
    traded = 0

    for market in markets[:10]:  # top 10 by liquidity
        token_id = market["token_id"]
        outcome = market["outcome"]

        try:
            sig, score, mid = signal_lib.run_signal(client, token_id, method, params)
        except Exception:
            continue

        checked += 1
        if sig == "PASS":
            continue

        mid = mid if mid is not None else 0.5

        # Two-sided: BUY = buy this token, SELL = might want opposite
        if sig == "BUY":
            trade_token, trade_outcome, entry = token_id, outcome, mid
        else:
            # SELL on this token → skip (we don't have the opposite token_id easily)
            continue

        if entry > max_entry:
            continue

        rr = round((1 - entry) / entry, 2) if entry > 0 else 0
        report_lines.append(f"\n  🟢 {market['name'][:50]}")
        report_lines.append(f"     [{trade_outcome}] @ {entry:.3f}  score={score:+.3f}  R:R={rr}:1")

        if dry_run:
            order = record_dry_run(perf, strategy, market, trade_token, trade_outcome, entry, size)
            report_lines.append(f"     📝 DRY RUN: BUY {size} USDC  order={order['id']}")
        else:
            # Live trade via polymarket.py
            env = os.environ.copy()
            env["USER_ID"] = user_id
            result = subprocess.run(
                ["python3", os.path.join(SCRIPTS_DIR, "polymarket.py"), "trade", trade_token, "BUY", str(size)],
                capture_output=True, text=True, env=env,
            )
            report_lines.append(f"     🤖 LIVE TRADE: {result.stdout.strip()}")

        traded += 1

    report_lines.append(f"\n  Checked {checked} markets, {traded} signals fired")
    save_perf(user_id, strategy_id, perf)

    report = "\n".join(report_lines)
    print(report)

    # Only notify if something interesting happened
    if traded > 0 or newly_settled:
        notify(user_id, report)


def main():
    user_id = get_user_id()
    args = sys.argv[1:]

    # Optionally run only a specific strategy
    target_id = args[0] if args else None

    if target_id:
        strategy = load_strategy(user_id, target_id)
        if not strategy:
            print(f"❌ Strategy not found: {target_id}")
            return
        strategies = [strategy]
    else:
        strategies = [s for s in list_strategies(user_id) if s["status"] in ("dry_run", "improving", "live")]

    if not strategies:
        print("📭 No active strategies")
        return

    client = get_clob_client(user_id)
    if not client:
        print("❌ No credentials found")
        return

    for strategy in strategies:
        run_strategy(user_id, strategy, client)


if __name__ == "__main__":
    main()
