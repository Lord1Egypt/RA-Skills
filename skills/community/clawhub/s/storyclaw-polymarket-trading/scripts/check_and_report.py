#!/usr/bin/env python3
"""
Polymarket Cron Worker - Auto signal check + optional auto-trade + dry-run P&L tracking.

Called by cron every 5 or 15 minutes. Reads strategy config from
state/{USER_ID}.strategy.json, auto-discovers current fast-loop market
token IDs (they change every interval), checks signals, and notifies.

Also records dry-run simulated orders to performance.json so they can be
settled later with: python3 polymarket.py settle

Usage (from cron):
  USER_ID=1234567890 python3 /path/to/check_and_report.py

State file: state/{USER_ID}.strategy.json
{
  "fast_markets": [
    {
      "coin": "btc",
      "timeframe": "15m",
      "side": "BUY",
      "max_size": 10,
      "auto_trade": false
    }
  ],
  "min_signal_threshold": 0.15
}
"""

import sys
import os
import json
import time
import uuid
import subprocess

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
STATE_DIR = os.path.join(SKILL_DIR, "state")
SCRIPT = os.path.join(SCRIPTS_DIR, "polymarket.py")


def get_user_id():
    uid = os.environ.get("USER_ID") or os.environ.get("TELEGRAM_USER_ID")
    if not uid:
        print("❌ USER_ID not set")
        sys.exit(1)
    return uid


def load_strategy(user_id):
    path = os.path.join(STATE_DIR, f"{user_id}.strategy.json")
    if not os.path.exists(path):
        print(f"⚠️  No strategy configured for user {user_id}")
        return None
    with open(path) as f:
        return json.load(f)


def load_performance(user_id):
    path = os.path.join(STATE_DIR, f"{user_id}.performance.json")
    default = {
        "pending": [],   # dry-run orders awaiting settlement
        "settled": [],   # resolved with final P&L
        "stats": {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "total_pnl": 0.0,
            "win_rate": 0.0,
        }
    }
    if not os.path.exists(path):
        return default
    with open(path) as f:
        data = json.load(f)
    # migrate old format
    if "trades" in data and "pending" not in data:
        data["pending"] = []
        data["settled"] = data.pop("trades", [])
    data.setdefault("pending", [])
    data.setdefault("settled", [])
    data.setdefault("stats", default["stats"])
    return data


def save_performance(user_id, perf):
    path = os.path.join(STATE_DIR, f"{user_id}.performance.json")
    with open(path, "w") as f:
        json.dump(perf, f, indent=2)


def run_script(cmd_args, user_id):
    env = os.environ.copy()
    env["USER_ID"] = user_id
    result = subprocess.run(
        ["python3", SCRIPT] + cmd_args,
        capture_output=True, text=True, env=env,
    )
    return result.stdout + result.stderr


def resolve_fast_token_ids(coin, timeframe, user_id):
    """Returns list of (outcome, token_id, end_timestamp) for the current interval."""
    output = run_script(["fast", coin, timeframe], user_id)
    tokens = []
    current_block = False
    end_ts = None

    for line in output.splitlines():
        if "[CURRENT]" in line:
            current_block = True
        elif "[NEXT]" in line:
            current_block = False
        if current_block:
            if "Ends:" in line:
                # parse ISO end time to unix timestamp
                try:
                    import datetime
                    ts_str = line.split("Ends:")[1].strip()
                    dt = datetime.datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
                    end_ts = int(dt.replace(tzinfo=datetime.timezone.utc).timestamp())
                except Exception:
                    pass
            if "token_id=" in line:
                try:
                    outcome = line.split("[")[1].split("]")[0].strip()
                    token_id = line.split("token_id=")[1].strip()
                    tokens.append((outcome, token_id, end_ts))
                except Exception:
                    pass
    return tokens


def parse_signal(output):
    signal = "PASS"
    score = 0.0
    mid = None
    for line in output.splitlines():
        if "SIGNAL: BUY" in line:
            signal = "BUY"
        elif "SIGNAL: SELL" in line:
            signal = "SELL"
        elif "Final score:" in line:
            try:
                score = float(line.split(":")[-1].strip())
            except Exception:
                pass
        elif "Mid price:" in line:
            try:
                mid = float(line.split(":")[-1].strip())
            except Exception:
                pass
    return signal, score, mid


def record_dry_run_order(perf, name, coin, timeframe, token_id, outcome, side, size, entry_price, end_ts):
    """Record a simulated order to pending list."""
    order = {
        "id": str(uuid.uuid4())[:8],
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "name": name,
        "coin": coin,
        "timeframe": timeframe,
        "token_id": token_id,
        "outcome": outcome,
        "side": side,
        "size": size,
        "entry_price": entry_price,
        "end_ts": end_ts,
        "resolved": False,
    }
    perf["pending"].append(order)
    return order


def notify(user_id, message):
    try:
        subprocess.run(
            ["openclaw", "notify", "--user", user_id, "--message", message],
            capture_output=True, timeout=10,
        )
    except Exception:
        print(f"[NOTIFY → {user_id}] {message}")


def main():
    user_id = get_user_id()
    strategy = load_strategy(user_id)
    if not strategy:
        return

    fast_markets = strategy.get("fast_markets", [])
    threshold = strategy.get("min_signal_threshold", 0.15)
    dry_run = strategy.get("dry_run", True)
    max_entry = strategy.get("max_entry_price", 0.65)

    if not fast_markets:
        print("⚠️  No fast_markets in strategy config")
        return

    perf = load_performance(user_id)
    timestamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    report_lines = [f"📊 Polymarket Signal Report - {timestamp}"]

    # Auto-settle any expired dry-run orders first
    if perf.get("pending"):
        settle_output = run_script(["settle"], user_id)
        # Reload perf in case settle updated it
        perf = load_performance(user_id)
        settled_lines = [l for l in settle_output.splitlines() if l.startswith("✅") or l.startswith("❌")]
        if settled_lines:
            report_lines.append("\n📋 Settled orders:")
            for line in settled_lines:
                report_lines.append(f"   {line}")
            stats = perf.get("stats", {})
            report_lines.append(f"   P&L to date: {'+' if stats.get('total_pnl', 0) >= 0 else ''}{stats.get('total_pnl', 0):.2f} USDC ({stats.get('total_trades', 0)} trades, {stats.get('win_rate', 0):.0%} win rate)")

    for market in fast_markets:
        coin = market.get("coin", "btc")
        timeframe = market.get("timeframe", "15m")
        name = f"{coin.upper()} {timeframe} Up/Down"
        mkt_max_entry = market.get("max_entry_price", max_entry)

        tokens = resolve_fast_token_ids(coin, timeframe, user_id)
        if not tokens:
            report_lines.append(f"\n⚠️ {name}: could not resolve token IDs")
            continue

        # Build token map: {"up": (token_id, end_ts), "down": (token_id, end_ts)}
        token_map = {}
        for outcome, tid, ets in tokens:
            token_map[outcome.lower()] = (tid, ets)

        up_tid, end_ts = token_map.get("up", (None, None))
        down_tid, _ = token_map.get("down", (None, None))
        if not up_tid:
            report_lines.append(f"\n⚠️ {name}: could not find Up token")
            continue

        # Always signal on Up token to get direction and mid price
        sig_output = run_script(["signal", up_tid], user_id)
        signal, score, mid_up = parse_signal(sig_output)
        mid_up = mid_up if mid_up else 0.5

        emoji = "🟢" if signal == "BUY" else ("🔴" if signal == "SELL" else "⚪")
        report_lines.append(f"\n{emoji} {name}")
        report_lines.append(f"   Signal: {signal}  (score={score:+.3f})")
        report_lines.append(f"   Up: {mid_up:.3f}  Down: {1-mid_up:.3f}  (max_entry={mkt_max_entry})")

        if not market.get("auto_trade") or signal == "PASS":
            continue

        # Two-sided: trade in signal direction if entry price is acceptable
        if signal == "BUY":
            trade_outcome, trade_token, entry_price = "Up", up_tid, mid_up
        else:  # SELL on Up = BUY on Down
            trade_outcome, trade_token, entry_price = "Down", down_tid, 1.0 - mid_up

        if not trade_token:
            report_lines.append(f"   ⚠️ No {trade_outcome} token available")
            continue

        if entry_price > mkt_max_entry:
            report_lines.append(f"   ⛔ Skip: {trade_outcome} @ {entry_price:.3f} > max_entry {mkt_max_entry:.2f} (bad R:R)")
            continue

        size = market.get("max_size", 5)
        rr = round((1 - entry_price) / entry_price, 2)
        report_lines.append(f"   ✅ {trade_outcome} @ {entry_price:.3f}  R:R = {rr}:1")

        if dry_run:
            order = record_dry_run_order(
                perf, name, coin, timeframe,
                trade_token, trade_outcome,
                "BUY", size, entry_price, end_ts
            )
            report_lines.append(f"   📝 DRY RUN: BUY {trade_outcome} {size} USDC @ {entry_price:.4f}")
            report_lines.append(f"      Order ID: {order['id']}  (settles at {time.strftime('%H:%M UTC', time.gmtime(end_ts)) if end_ts else '?'})")
        else:
            trade_output = run_script(["trade", trade_token, "BUY", str(size)], user_id)
            report_lines.append(f"   🤖 Auto-trade: BUY {trade_outcome} {size} USDC")
            for line in trade_output.splitlines():
                if line.strip():
                    report_lines.append(f"      {line.strip()}")

    save_performance(user_id, perf)
    report = "\n".join(report_lines)
    print(report)
    notify(user_id, report)


if __name__ == "__main__":
    main()
