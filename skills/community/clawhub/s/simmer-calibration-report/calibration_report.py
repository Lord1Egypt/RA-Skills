#!/usr/bin/env python3
"""
Simmer Calibration Report - Know where your edge lives.

Usage:
    python calibration_report.py              # Analyze sim journal
    python calibration_report.py --live       # Analyze live journal
    python calibration_report.py --config     # Show config

Requires:
    SIMMER_API_KEY environment variable
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta
from collections import defaultdict

# Force line-buffered stdout (required for cron/Docker/OpenClaw visibility)
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
from simmer_sdk.skill import load_config, update_config, get_config_path

SKILL_SLUG = "simmer-calibration-report"
TRADE_SOURCE = "sdk:calibration-report"

CONFIG_SCHEMA = {
    "journal_path": {"env": "CALIB_JOURNAL_PATH", "default": "", "type": str},
    "min_trades": {"env": "CALIB_MIN_TRADES", "default": 10, "type": int},
    "lookback_days": {"env": "CALIB_LOOKBACK_DAYS", "default": 30, "type": int},
    "include_unresolved": {"env": "CALIB_INCLUDE_UNRESOLVED", "default": "false", "type": str},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)

# ---------------------------------------------------------------------------
# Client singleton (needed for automaton config even though we don't trade)
# ---------------------------------------------------------------------------
_client = None

def get_client(live=True):
    global _client
    if _client is None:
        try:
            from simmer_sdk import SimmerClient
        except ImportError:
            print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
            sys.exit(1)
        api_key = os.environ.get("SIMMER_API_KEY")
        if not api_key:
            print("Error: SIMMER_API_KEY environment variable not set")
            sys.exit(1)
        venue = os.environ.get("TRADING_VENUE", "polymarket")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    return _client

# ---------------------------------------------------------------------------
# Journal loading
# ---------------------------------------------------------------------------

def find_journal(config, live=False):
    """Find journal path from config or defaults."""
    path = config["journal_path"]
    if path and os.path.exists(path):
        return path
    # Try relative to workspace
    workspace = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
    if live:
        candidates = [
            os.path.join(workspace, "data/live/trade_journal.jsonl"),
        ]
    else:
        candidates = [
            os.path.join(workspace, "data/sim/sim_trade_journal.jsonl"),
            os.path.join(workspace, "data/sim/trade_journal.jsonl"),
        ]
    # Always fall back to live if sim not found
    candidates.append(os.path.join(workspace, "data/live/trade_journal.jsonl"))
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def load_journal(path, lookback_days, include_unresolved):
    """Load and filter journal entries."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    trades = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            # Parse timestamp
            ts_str = entry.get("timestamp", "")
            try:
                ts = datetime.fromisoformat(ts_str)
            except (ValueError, TypeError):
                continue
            if ts < cutoff:
                continue
            # Filter resolved
            resolved = entry.get("resolved", False)
            if not include_unresolved and not resolved:
                continue
            entry["_ts"] = ts
            trades.append(entry)
    return trades

# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------

def is_win(trade):
    """Detect win from journal fields."""
    if "won" in trade:
        return bool(trade["won"])
    outcome = trade.get("outcome", "")
    if outcome:
        return outcome.lower() == "win"
    pnl = trade.get("pnl", 0)
    return pnl > 0


def get_pnl(trade):
    """Get PnL value."""
    return float(trade.get("pnl", 0))


def get_entry_price(trade):
    """Get entry price (cost per share)."""
    cost = trade.get("cost", 0)
    shares = trade.get("shares", 0)
    if cost and shares and shares > 0:
        return cost / shares
    return trade.get("entry_price", 0.5)


def infer_market_type(trade):
    """Infer market type from question or tags."""
    q = (trade.get("market_question", "") or "").lower()
    tags = [t.lower() for t in (trade.get("tags", []) or [])]
    all_text = q + " " + " ".join(tags)
    if any(w in all_text for w in ["bitcoin", "btc", "ethereum", "eth", "crypto", "solana", "sol", "xrp", "dogecoin"]):
        return "crypto"
    if any(w in all_text for w in ["temperature", "weather", "degrees", "°f", "°c"]):
        return "weather"
    if any(w in all_text for w in ["trump", "biden", "election", "president", "congress", "senate", "political"]):
        return "politics"
    if any(w in all_text for w in ["nba", "nfl", "mlb", "soccer", "football", "game", "match", "score"]):
        return "sports"
    return "other"


def hour_bucket(hour):
    if hour < 6:
        return "00-06"
    elif hour < 12:
        return "06-12"
    elif hour < 18:
        return "12-18"
    else:
        return "18-24"


PRICE_BANDS = [
    (0.05, 0.20), (0.20, 0.35), (0.35, 0.50),
    (0.50, 0.65), (0.65, 0.80), (0.80, 0.95),
]

def price_band(price):
    for lo, hi in PRICE_BANDS:
        if lo <= price < hi:
            return f"{lo:.2f}-{hi:.2f}"
    if price >= 0.95:
        return "0.80-0.95"
    return "0.05-0.20"


DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def compute_stats(trades):
    """Compute WR% and EV for a list of trades."""
    n = len(trades)
    if n == 0:
        return {"n": 0, "wr": 0, "ev": 0}
    wins = sum(1 for t in trades if is_win(t))
    total_pnl = sum(get_pnl(t) for t in trades)
    return {"n": n, "wr": wins / n * 100, "ev": total_pnl / n}

# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def ev_bar(ev, max_ev):
    """ASCII bar proportional to EV."""
    if max_ev <= 0:
        return ""
    width = max(1, int(16 * abs(ev) / max_ev))
    if ev >= 0:
        return "█" * width
    return "▒" * width


def print_section(title, groups, min_trades, order=None):
    """Print a breakdown section."""
    # Filter by min_trades
    filtered = {k: v for k, v in groups.items() if v["n"] >= min_trades}
    if not filtered:
        return
    if order:
        keys = [k for k in order if k in filtered]
    else:
        keys = sorted(filtered.keys(), key=lambda k: -filtered[k]["ev"])
    max_ev = max(abs(v["ev"]) for v in filtered.values()) if filtered else 1
    print(f"\nBY {title}")
    for k in keys:
        s = filtered[k]
        bar = ev_bar(s["ev"], max_ev)
        ev_sign = "+" if s["ev"] >= 0 else ""
        print(f"  {k:<20s} n={s['n']:<4d} WR={s['wr']:5.1f}%  EV={ev_sign}{s['ev']:.3f}  {bar}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_report(live=False, show_config=False, quiet=False):
    """Run the calibration report."""
    config = _config

    if show_config:
        print("📊 Simmer Calibration Report — Config")
        print("=" * 50)
        for k, v in CONFIG_SCHEMA.items():
            print(f"  {k}: {config[k]} (env: {v['env']}, default: {v['default']})")
        print(f"\nConfig file: {get_config_path(__file__)}")
        return

    journal_path = find_journal(config, live=live)
    if not journal_path:
        print("❌ No journal found. Set CALIB_JOURNAL_PATH or ensure data/live/trade_journal.jsonl exists.")
        return

    include_unresolved = str(config["include_unresolved"]).lower() in ("true", "1", "yes")
    trades = load_journal(journal_path, config["lookback_days"], include_unresolved)
    total = len(trades)

    if total == 0:
        print(f"📊 No trades found in last {config['lookback_days']} days.")
        print(f"   Journal: {journal_path}")
        return

    # Overall stats
    overall = compute_stats(trades)
    ev_str = f"+${overall['ev']:.3f}" if overall["ev"] >= 0 else f"-${abs(overall['ev']):.3f}"

    print(f"📊 Calibration Report — Last {config['lookback_days']} days")
    print("━" * 50)
    print(f"Total: {total} trades | {overall['wr']:.1f}% WR | {ev_str} EV/trade")
    print(f"Journal: {journal_path}")

    if quiet:
        return {"signals": total, "trades_attempted": 0, "trades_executed": 0, "skip_reason": "analytics_only"}

    min_t = config["min_trades"]

    # By strategy
    by_strat = defaultdict(list)
    for t in trades:
        by_strat[t.get("strategy", "unknown")].append(t)
    print_section("STRATEGY", {k: compute_stats(v) for k, v in by_strat.items()}, min_t)

    # By hour
    by_hour = defaultdict(list)
    for t in trades:
        by_hour[hour_bucket(t["_ts"].hour)].append(t)
    print_section("HOUR (UTC)", {k: compute_stats(v) for k, v in by_hour.items()}, min_t,
                  order=["00-06", "06-12", "12-18", "18-24"])

    # By day of week
    by_dow = defaultdict(list)
    for t in trades:
        by_dow[DAY_NAMES[t["_ts"].weekday()]].append(t)
    print_section("DAY OF WEEK", {k: compute_stats(v) for k, v in by_dow.items()}, min_t,
                  order=DAY_NAMES)

    # By entry price band
    by_price = defaultdict(list)
    for t in trades:
        by_price[price_band(get_entry_price(t))].append(t)
    print_section("ENTRY PRICE", {k: compute_stats(v) for k, v in by_price.items()}, min_t,
                  order=[f"{lo:.2f}-{hi:.2f}" for lo, hi in PRICE_BANDS])

    # By market type
    by_type = defaultdict(list)
    for t in trades:
        by_type[infer_market_type(t)].append(t)
    print_section("MARKET TYPE", {k: compute_stats(v) for k, v in by_type.items()}, min_t)

    # Best segment
    all_segments = {}
    for section_data in [by_strat, by_hour, by_dow, by_price, by_type]:
        for k, v in section_data.items():
            stats = compute_stats(v)
            if stats["n"] >= min_t:
                all_segments[k] = stats
    if all_segments:
        best_key = max(all_segments, key=lambda k: all_segments[k]["ev"])
        best = all_segments[best_key]
        ev_s = "+" if best["ev"] >= 0 else ""
        print(f"\n🏆 Best segment: {best_key} (EV={ev_s}{best['ev']:.3f}, WR={best['wr']:.1f}%)")

    return {"signals": total, "trades_attempted": 0, "trades_executed": 0, "skip_reason": "analytics_only"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simmer Calibration Report")
    parser.add_argument("--live", action="store_true", help="Use live journal (default: sim)")
    parser.add_argument("--config", action="store_true", help="Show config")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE", help="Set config value")
    parser.add_argument("--quiet", "-q", action="store_true", help="Summary only")
    args = parser.parse_args()

    # Handle --set
    if args.set:
        updates = {}
        for item in args.set:
            if "=" in item:
                key, value = item.split("=", 1)
                if key in CONFIG_SCHEMA:
                    type_fn = CONFIG_SCHEMA[key].get("type", str)
                    try:
                        if type_fn == bool:
                            value = value.lower() in ("true", "1", "yes")
                        else:
                            value = type_fn(value)
                    except (ValueError, TypeError):
                        pass
                updates[key] = value
        if updates:
            updated = update_config(updates, __file__)
            print(f"Config updated: {updates}")
            print(f"Saved to: {get_config_path(__file__)}")
            _config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)

    result = run_report(live=args.live, show_config=args.config, quiet=args.quiet)

    # Single automaton report
    if os.environ.get("AUTOMATON_MANAGED"):
        if result and isinstance(result, dict):
            print(json.dumps({"automaton": result}))
        else:
            print(json.dumps({"automaton": {"signals": 0, "trades_attempted": 0, "trades_executed": 0, "skip_reason": "no_signal"}}))
