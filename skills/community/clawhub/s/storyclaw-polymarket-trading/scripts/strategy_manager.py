#!/usr/bin/env python3
"""
Strategy lifecycle manager for the self-evolving Polymarket trading system.

Commands:
  create  --json '{...}'   Create a new strategy from JSON config
  review  [strategy_id]    Analyze performance, auto-improve if needed
  status  [strategy_id]    Show current state of a strategy
  list                     List all strategies for this user

Strategy file lives at:
  strategies/{user_id}/{strategy_id}.json

Strategy schema:
{
  "id": "politics-001",
  "name": "US Politics Sentiment",
  "status": "dry_run",       // draft|dry_run|improving|pending_live|live|paused
  "version": 1,
  "market_filter": {
    "keywords": ["trump", "congress"],
    "min_liquidity_usdc": 2000,
    "max_days_to_expiry": 14,
    "min_days_to_expiry": 1
  },
  "signal": {
    "method": "orderbook_imbalance",
    "params": {
      "threshold": 0.15,
      "max_entry_price": 0.65
    }
  },
  "sizing": { "max_size_usdc": 10 },
  "targets": {
    "min_sample_size": 30,
    "target_win_rate": 0.60
  },
  "stats": { "trades": 0, "wins": 0, "win_rate": 0.0, "pnl": 0.0 },
  "changelog": [],
  "created_at": "2026-02-21T00:00:00Z",
  "updated_at": "2026-02-21T00:00:00Z"
}
"""

import sys
import os
import json
import time
import uuid
import subprocess

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRATEGIES_DIR = os.path.join(SKILL_DIR, "strategies")
os.makedirs(STRATEGIES_DIR, exist_ok=True)


# ── User / path helpers ──────────────────────────────────────────────────────

def get_user_id():
    uid = os.environ.get("USER_ID") or os.environ.get("TELEGRAM_USER_ID")
    if not uid:
        print("❌ USER_ID not set")
        sys.exit(1)
    return uid


def strategies_dir(user_id):
    d = os.path.join(STRATEGIES_DIR, user_id)
    os.makedirs(d, exist_ok=True)
    return d


def strategy_path(user_id, strategy_id):
    return os.path.join(strategies_dir(user_id), f"{strategy_id}.json")


def perf_path(user_id, strategy_id):
    state_dir = os.path.join(SKILL_DIR, "state")
    os.makedirs(state_dir, exist_ok=True)
    return os.path.join(state_dir, f"{user_id}.{strategy_id}.perf.json")


# ── Load / save ──────────────────────────────────────────────────────────────

def load_strategy(user_id, strategy_id):
    p = strategy_path(user_id, strategy_id)
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)


def save_strategy(user_id, strategy):
    strategy["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    p = strategy_path(user_id, strategy["id"])
    with open(p, "w") as f:
        json.dump(strategy, f, indent=2)


def load_perf(user_id, strategy_id):
    p = perf_path(user_id, strategy_id)
    if not os.path.exists(p):
        return {"pending": [], "settled": []}
    with open(p) as f:
        return json.load(f)


def list_strategies(user_id):
    d = strategies_dir(user_id)
    results = []
    for fname in sorted(os.listdir(d)):
        if fname.endswith(".json"):
            with open(os.path.join(d, fname)) as f:
                results.append(json.load(f))
    return results


# ── Stats ────────────────────────────────────────────────────────────────────

def compute_stats(user_id, strategy_id, last_n=None):
    """
    Compute performance stats from settled trades (optionally last N).

    Key metric: edge = win_rate - avg_entry_price
      - edge > 0  means positive expected value (profitable)
      - edge >= min_edge means strategy is ready for live trading
    """
    perf = load_perf(user_id, strategy_id)
    settled = perf.get("settled", [])
    if last_n:
        settled = settled[-last_n:]
    if not settled:
        return {"trades": 0, "wins": 0, "win_rate": 0.0, "avg_entry": 0.0, "edge": 0.0, "pnl": 0.0}
    wins = sum(1 for t in settled if t.get("pnl", 0) > 0)
    pnl = sum(t.get("pnl", 0) for t in settled)
    win_rate = round(wins / len(settled), 4)
    avg_entry = round(sum(t.get("entry_price", 0.5) for t in settled) / len(settled), 4)
    edge = round(win_rate - avg_entry, 4)  # EV per dollar: positive means profitable
    return {
        "trades": len(settled),
        "wins": wins,
        "win_rate": win_rate,
        "avg_entry": avg_entry,
        "edge": edge,      # primary metric: must be > 0 to be profitable
        "pnl": round(pnl, 4),
    }


# ── Auto-improvement logic ────────────────────────────────────────────────────

IMPROVEMENT_STEPS = [
    # Each step: (condition_fn, apply_fn, description_fn)
    # condition_fn(edge, min_edge, params) -> bool
    # apply_fn(params) -> new_params
    # description_fn(old_params, new_params) -> str
    #
    # edge = win_rate - avg_entry_price  (positive = profitable)
    # Two levers:
    #   1. Raise threshold → fewer but higher-conviction signals → improves win_rate → raises edge
    #   2. Lower max_entry_price → cheaper entries → directly raises edge (same win_rate, lower P)
    {
        "condition": lambda edge, min_edge, p: edge < min_edge - 0.10,
        "apply": lambda p: {**p, "threshold": min(round(p.get("threshold", 0.15) + 0.05, 2), 0.40)},
        "describe": lambda old, new: f"threshold {old.get('threshold', 0.15):.2f}→{new.get('threshold'):.2f} (edge too low, tighten signal to improve win rate)",
    },
    {
        "condition": lambda edge, min_edge, p: edge < min_edge - 0.03,
        "apply": lambda p: {**p, "max_entry_price": max(round(p.get("max_entry_price", 0.65) - 0.05, 2), 0.40)},
        "describe": lambda old, new: f"max_entry_price {old.get('max_entry_price', 0.65):.2f}→{new.get('max_entry_price'):.2f} (lower entry price to directly improve edge)",
    },
]


def auto_improve(strategy, stats):
    """
    Attempt one parameter adjustment. Returns (changed: bool, description: str).
    Only changes ONE parameter per review to isolate effect.

    Target metric: edge = win_rate - avg_entry_price >= min_edge
    """
    min_edge = strategy["targets"].get("min_edge", 0.05)
    actual_edge = stats["edge"]
    params = strategy["signal"]["params"]

    for step in IMPROVEMENT_STEPS:
        if step["condition"](actual_edge, min_edge, params):
            new_params = step["apply"](params)
            # Check if anything actually changed
            if new_params == params:
                continue
            desc = step["describe"](params, new_params)
            strategy["signal"]["params"] = new_params
            strategy["version"] += 1
            strategy["changelog"].append({
                "v": strategy["version"],
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "change": desc,
                "stats_before": stats,
            })
            return True, desc

    return False, None


# ── Notify ───────────────────────────────────────────────────────────────────

def notify(user_id, message):
    try:
        subprocess.run(
            ["openclaw", "notify", "--user", user_id, "--message", message],
            capture_output=True, timeout=10,
        )
    except Exception:
        print(f"[NOTIFY → {user_id}] {message}")


# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_create(user_id, config_json):
    """Create a new strategy from a JSON config dict."""
    config = json.loads(config_json) if isinstance(config_json, str) else config_json

    strategy_id = config.get("id") or f"strategy-{str(uuid.uuid4())[:8]}"
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    strategy = {
        "id": strategy_id,
        "name": config.get("name", "Unnamed Strategy"),
        "status": "dry_run",
        "version": 1,
        "market_filter": config.get("market_filter", {
            "keywords": [],
            "min_liquidity_usdc": 1000,
            "max_days_to_expiry": 30,
            "min_days_to_expiry": 1,
        }),
        "signal": config.get("signal", {
            "method": "orderbook_imbalance",
            "params": {"threshold": 0.15, "max_entry_price": 0.65},
        }),
        "sizing": config.get("sizing", {"max_size_usdc": 10}),
        "targets": config.get("targets", {
            "min_sample_size": 30,
            "min_edge": 0.05,   # win_rate - avg_entry_price >= 0.05 to go live
        }),
        "stats": {"trades": 0, "wins": 0, "win_rate": 0.0, "avg_entry": 0.0, "edge": 0.0, "pnl": 0.0},
        "changelog": [],
        "created_at": now,
        "updated_at": now,
    }

    save_strategy(user_id, strategy)
    min_edge = strategy["targets"].get("min_edge", 0.05)
    print(f"✅ Strategy created: {strategy_id}")
    print(f"   Name:    {strategy['name']}")
    print(f"   Status:  {strategy['status']}")
    print(f"   Method:  {strategy['signal']['method']}")
    print(f"   Target:  edge ≥ {min_edge*100:.0f}%  over {strategy['targets']['min_sample_size']} trades")
    print(f"            (edge = win_rate − avg_entry_price, must be positive to be profitable)")
    print(f"   Filter:  {strategy['market_filter'].get('keywords', [])}")
    print(f"   File:    {strategy_path(user_id, strategy_id)}")
    return strategy


def cmd_review(user_id, strategy_id):
    """
    Review strategy performance. Auto-improve if underperforming.
    Notify user of any changes or milestones.
    """
    strategy = load_strategy(user_id, strategy_id)
    if not strategy:
        print(f"❌ Strategy not found: {strategy_id}")
        return

    if strategy["status"] in ("draft", "paused", "pending_live", "live"):
        print(f"⏸  Strategy {strategy_id} is in '{strategy['status']}' state — skipping review")
        return

    min_sample = strategy["targets"]["min_sample_size"]
    min_edge = strategy["targets"].get("min_edge", 0.05)
    stats = compute_stats(user_id, strategy_id, last_n=min_sample)

    edge_sign = "+" if stats["edge"] >= 0 else ""
    pnl_sign = "+" if stats["pnl"] >= 0 else ""
    print(f"\n📊 Review: {strategy['name']} (v{strategy['version']})")
    print(f"   Status:     {strategy['status']}")
    print(f"   Trades:     {stats['trades']} / {min_sample} required")
    print(f"   Win rate:   {stats['win_rate']*100:.1f}%")
    print(f"   Avg entry:  {stats['avg_entry']:.3f}")
    print(f"   Edge:       {edge_sign}{stats['edge']*100:.1f}%  (target ≥ {min_edge*100:.0f}%)")
    print(f"   P&L:        {pnl_sign}{stats['pnl']:.2f} USDC")

    # Update embedded stats
    strategy["stats"] = stats
    save_strategy(user_id, strategy)

    if stats["trades"] < min_sample:
        remaining = min_sample - stats["trades"]
        days_est = remaining // max(stats["trades"] // 7, 1) if stats["trades"] > 0 else "?"
        print(f"   ⏳ Insufficient data — need {remaining} more trades (~{days_est} days at current rate)")
        return

    # Enough data — evaluate: need positive edge AND above min_edge threshold
    if stats["edge"] >= min_edge and stats["pnl"] > 0:
        strategy["status"] = "pending_live"
        save_strategy(user_id, strategy)
        name = strategy["name"]
        edge_pct = f"{stats['edge']*100:+.1f}%"
        pnl_sign = "+" if stats["pnl"] >= 0 else ""
        msg = (
            f"🎯 策略 {name!r} 达标！\n"
            f"   {stats['trades']} 笔 | 胜率 {stats['win_rate']*100:.1f}% | 均入场 {stats['avg_entry']:.3f} | Edge {edge_pct}\n"
            f"   P&L {pnl_sign}{stats['pnl']:.2f} USDC\n"
            f"   准备好切换真钱交易了吗？回复'切换真钱'确认。"
        )
        print("\n🎉 Target met! Strategy marked pending_live")
        notify(user_id, msg)
        return

    # Underperforming — try auto-improvement
    changed, desc = auto_improve(strategy, stats)
    if changed:
        strategy["status"] = "improving"
        save_strategy(user_id, strategy)
        name = strategy["name"]
        edge_pct = f"{stats['edge']*100:+.1f}%"
        msg = (
            f"🔧 策略 {name!r} 自动调整 (v{strategy['version']}):\n"
            f"   {desc}\n"
            f"   当前: {stats['trades']} 笔 | Edge {edge_pct} | 目标 edge ≥ {min_edge*100:.0f}%\n"
            f"   继续 dry-run 收集数据..."
        )
        print(f"\n🔧 Auto-improved: {desc}")
        notify(user_id, msg)
    else:
        print("\n⚠️  Underperforming but no improvement available — consider redesigning strategy")
        consecutive_fails = sum(1 for c in strategy["changelog"] if "stats_before" in c and c["stats_before"].get("edge", 0) < min_edge)
        if consecutive_fails >= 3:
            name = strategy["name"]
            msg = (
                f"⚠️ 策略 {name!r} 连续 {consecutive_fails} 次调整仍未达标\n"
                f"   Edge {stats['edge']*100:+.1f}% vs 目标 {min_edge*100:.0f}%\n"
                f"   建议重新考虑策略方向或市场选择。"
            )
            notify(user_id, msg)


def cmd_status(user_id, strategy_id=None):
    """Show status of one or all strategies."""
    if strategy_id:
        strategies = [load_strategy(user_id, strategy_id)]
        strategies = [s for s in strategies if s]
    else:
        strategies = list_strategies(user_id)

    if not strategies:
        print("📭 No strategies found")
        return

    for s in strategies:
        stats = compute_stats(user_id, s["id"])
        target = s["targets"]
        status_emoji = {
            "draft": "📝", "dry_run": "🔬", "improving": "🔧",
            "pending_live": "🎯", "live": "💰", "paused": "⏸",
        }.get(s["status"], "❓")
        print(f"\n{status_emoji} {s['name']} [{s['id']}] v{s['version']}")
        print(f"   Status:   {s['status']}")
        print(f"   Method:   {s['signal']['method']}  params={s['signal']['params']}")
        print(f"   Filter:   {s['market_filter'].get('keywords', [])}")
        min_edge = target.get("min_edge", 0.05)
        edge_pct = f"{stats['edge']*100:+.1f}%"
        print(f"   Progress: {stats['trades']}/{target['min_sample_size']} trades  |  edge {edge_pct} (target ≥ {min_edge*100:.0f}%)  |  win {stats['win_rate']*100:.1f}% @ avg {stats['avg_entry']:.3f}  |  P&L {'+' if stats['pnl']>=0 else ''}{stats['pnl']:.2f} USDC")
        if s["changelog"]:
            last = s["changelog"][-1]
            print(f"   Last change: {last['ts'][:10]}  {last['change']}")


def cmd_list(user_id):
    cmd_status(user_id)


def cmd_activate_live(user_id, strategy_id):
    """Switch a pending_live strategy to live trading."""
    strategy = load_strategy(user_id, strategy_id)
    if not strategy:
        print(f"❌ Strategy not found: {strategy_id}")
        return
    if strategy["status"] != "pending_live":
        print(f"❌ Strategy is '{strategy['status']}', must be 'pending_live' to activate")
        return
    strategy["status"] = "live"
    save_strategy(user_id, strategy)
    print(f"💰 Strategy '{strategy['name']}' is now LIVE")
    notify(user_id, f"💰 策略 '{strategy['name']}' 已切换真钱交易模式！")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    user_id = get_user_id()
    args = sys.argv[1:]

    if not args:
        print("Usage: strategy_manager.py <create|review|status|list|activate-live> [args]")
        return

    cmd = args[0]

    if cmd == "create":
        if "--json" not in args:
            print("Usage: strategy_manager.py create --json '{...}'")
            return
        idx = args.index("--json")
        config_json = args[idx + 1]
        cmd_create(user_id, config_json)

    elif cmd == "review":
        strategy_id = args[1] if len(args) > 1 else None
        if strategy_id:
            cmd_review(user_id, strategy_id)
        else:
            for s in list_strategies(user_id):
                cmd_review(user_id, s["id"])

    elif cmd == "status":
        strategy_id = args[1] if len(args) > 1 else None
        cmd_status(user_id, strategy_id)

    elif cmd == "list":
        cmd_list(user_id)

    elif cmd == "activate-live":
        if len(args) < 2:
            print("Usage: strategy_manager.py activate-live <strategy_id>")
            return
        cmd_activate_live(user_id, args[1])

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
