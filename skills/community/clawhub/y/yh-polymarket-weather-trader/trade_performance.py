#!/usr/bin/env python3
"""
Trade Performance Tracking Module

Provides structured JSONL logging, circuit breaker management, and trade aggregation
for polymarket trading skills. Zero external dependencies - stdlib only.

Usage:
    python trade_performance.py --report skill=polymarket-fast-loop
    python trade_performance.py --validate
    python trade_performance.py --resume /path/to/skill/dir
"""

import json
import sys
import argparse
import importlib
import importlib.util
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional
import math
import statistics

# =============================================================================
# Schema Definition
# =============================================================================

TRADING_LOG_SCHEMA = {
    "timestamp": "UTC ISO 8601 timestamp",
    "skill": "Skill slug (e.g., polymarket-fast-loop)",
    "source": "Trade source identifier",
    "success": "bool - trade execution success",
    "trade_id": "str - unique trade identifier",
    "market_id": "str - polymarket market condition ID",
    "side": "str - 'yes' or 'no'",
    "shares_bought": "float - actual shares purchased",
    "shares_requested": "float - requested shares",
    "cost": "float - trade cost in USD",
    "new_price": "float - price after trade",
    "order_status": "str - order fill status",
    "simulated": "bool - paper trade flag",
    "signal": "dict - signal context (source, strength, etc.)",
    "error": "str - error message if failed",
    "consecutive_losses": "int - circuit breaker state snapshot",
    "skill_paused": "bool - circuit breaker paused state",
}

SKILL_SLUG = "polymarket-weather-trader"
TRADE_SOURCE = "sdk:weather"


# =============================================================================
# Trade Logging
# =============================================================================


def get_trades_path() -> Path:
    """Get path to trades.jsonl in the same directory as this module."""
    return Path(__file__).parent / "trades.jsonl"


def write_trade_log(
    trade_result: dict,
    skill_slug: str,
    source: str,
    signal_data: Optional[dict] = None,
    extra: Optional[dict] = None,
) -> None:
    """
    Append a trade record to trades.jsonl.

    Args:
        trade_result: Dict from execute_trade() with keys: success, trade_id,
                     shares_bought, shares (alias), error, simulated
        skill_slug: Identifier for the skill (e.g., "polymarket-fast-loop")
        source: Trade source (e.g., "sdk:fastloop")
        signal_data: Optional dict with signal context
        extra: Optional additional fields
    """
    trades_path = get_trades_path()

    # Extract core trade data with defaults
    success = trade_result.get("success", False)
    trade_id = trade_result.get("trade_id", "")
    shares_bought = trade_result.get("shares_bought", trade_result.get("shares", 0))
    shares_requested = trade_result.get(
        "shares_requested", trade_result.get("shares_requested", shares_bought)
    )
    cost = trade_result.get("cost", 0.0)
    new_price = trade_result.get("new_price", trade_result.get("price_after", 0.0))
    order_status = trade_result.get("order_status", "")
    simulated = trade_result.get("simulated", False)
    error_msg = trade_result.get("error", "")
    market_id = trade_result.get("market_id", "")
    side = trade_result.get("side", "")

    # Capture circuit breaker state snapshot (inline to avoid import issues)
    skill_dir = str(Path(__file__).parent)
    cb_path = Path(skill_dir) / "circuit_breaker.json"
    is_paused = False
    consecutive_losses = 0
    if cb_path.exists():
        try:
            cb_data = json.loads(cb_path.read_text())
            is_paused = cb_data.get("paused", False)
            consecutive_losses = cb_data.get("consecutive_losses", 0)
        except (json.JSONDecodeError, OSError):
            pass

    # Build entry
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "skill": skill_slug,
        "source": source,
        "success": success,
        "trade_id": trade_id,
        "market_id": market_id,
        "side": side,
        "shares_bought": shares_bought,
        "shares_requested": shares_requested,
        "cost": cost,
        "new_price": new_price,
        "order_status": order_status,
        "simulated": simulated,
        "signal": signal_data or {},
        "error": error_msg,
        "consecutive_losses": consecutive_losses,
        "skill_paused": is_paused,
    }

    # Add extra fields
    if extra:
        entry.update(extra)

    # Append as JSON line
    with open(trades_path, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")


# =============================================================================
# Circuit Breaker
# =============================================================================


def get_circuit_breaker_path(skill_dir: str) -> Path:
    """Get path to circuit_breaker.json in skill directory."""
    return Path(skill_dir) / "circuit_breaker.json"


def check_circuit_breaker(
    skill_dir: str,
    threshold: int = 3,
    cooldown_hours: int = 6,
) -> tuple[bool, str]:
    """
    Check circuit breaker status.

    Args:
        skill_dir: Path to skill directory
        threshold: Consecutive losses before triggering pause
        cooldown_hours: Hours to stay paused before auto-resume

    Returns:
        (is_allowed, message) - True if trading allowed, message describes state
    """
    cb_path = get_circuit_breaker_path(skill_dir)

    # No file = not triggered
    if not cb_path.exists():
        return True, ""

    try:
        data = json.loads(cb_path.read_text())
    except (json.JSONDecodeError, OSError):
        # Fail-open on corrupt JSON
        cb_path.unlink()
        return True, ""

    # Check if paused
    if not data.get("paused", False):
        return True, ""

    # Check resume time
    resume_at = data.get("resume_at")
    if resume_at:
        resume_time = datetime.fromisoformat(resume_at)
        now = datetime.now(timezone.utc)
        if now >= resume_time:
            # Auto-resume expired
            cb_path.unlink()
            return True, "auto-resumed"

    # Still paused
    reason = data.get("reason", "consecutive losses exceeded")
    return False, f"PAUSED: {reason}"


# Error patterns that should NOT count as consecutive losses (infra/config issues)
_INFRA_ERROR_PATTERNS = [
    "no polymarket wallet",
    "no wallet",
    "wallet not found",
    "authentication",
    "api key",
    "unauthorized",
    "forbidden",
    "timeout",
    "timed out",
    "connection",
    "network",
    "dns",
    "ssl",
    "certificate",
    "simmer sdk",
    "import failed",
    "module not found",
]


def _is_infra_error(error: str) -> bool:
    """Check if error is a configuration/infra issue (not a market loss)."""
    if not error:
        return False
    error_lower = error.lower()
    return any(p in error_lower for p in _INFRA_ERROR_PATTERNS)


def update_circuit_breaker(
    skill_dir: str,
    trade_success: bool,
    simulated: bool,
    threshold: int = 3,
    cooldown_hours: int = 6,
    error: str = "",
) -> None:
    """
    Update circuit breaker state after a trade.

    Args:
        skill_dir: Path to skill directory
        trade_success: Whether trade succeeded
        simulated: Whether this was a paper trade
        threshold: Consecutive losses before pause
        cooldown_hours: Hours to pause
        error: Error message if trade failed (used to distinguish infra vs market errors)
    """
    # Paper trades don't count
    if simulated:
        return

    # Infra/config errors don't count as losses
    if not trade_success and _is_infra_error(error):
        return

    cb_path = get_circuit_breaker_path(skill_dir)

    # Read existing state
    if cb_path.exists():
        try:
            data = json.loads(cb_path.read_text())
        except (json.JSONDecodeError, OSError):
            data = {"consecutive_losses": 0, "consecutive_wins": 0}
    else:
        data = {"consecutive_losses": 0, "consecutive_wins": 0}

    # Update counters
    if trade_success:
        data["consecutive_losses"] = 0
        data["consecutive_wins"] = data.get("consecutive_wins", 0) + 1
    else:
        data["consecutive_losses"] = data.get("consecutive_losses", 0) + 1
        data["consecutive_wins"] = 0

    # Check threshold
    if data["consecutive_losses"] >= threshold:
        data["paused"] = True
        data["reason"] = (
            f"consecutive losses = {data['consecutive_losses']} >= {threshold}"
        )
        resume_at = datetime.now(timezone.utc) + timedelta(hours=cooldown_hours)
        data["resume_at"] = resume_at.isoformat()
        data["paused_at"] = datetime.now(timezone.utc).isoformat()

    # Write state
    with open(cb_path, "w") as f:
        json.dump(data, f, indent=2)


# =============================================================================
# Trade Aggregation
# =============================================================================


def aggregate_trades(
    trades_path: str,
    skill: Optional[str] = None,
    date: Optional[str] = None,
) -> dict:
    """
    Aggregate trade statistics from trades.jsonl.

    Args:
        trades_path: Path to trades.jsonl file
        skill: Optional skill slug to filter by
        date: Optional date string (YYYY-MM-DD) to filter by

    Returns:
        Dict with: total_trades, successes, failures, live_trades,
        paper_trades, order_success_rate, total_invested_usd, avg_edge
    """
    path = Path(trades_path)
    if not path.exists():
        return {
            "total_trades": 0,
            "successes": 0,
            "failures": 0,
            "live_trades": 0,
            "paper_trades": 0,
            "order_success_rate": 0.0,
            "total_invested_usd": 0.0,
            "avg_edge": 0.0,
        }

    total_trades = 0
    successes = 0
    failures = 0
    live_trades = 0
    paper_trades = 0
    total_invested = 0.0
    edges = []

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Filter by skill
            if skill and entry.get("skill") != skill:
                continue

            # Filter by date
            if date:
                entry_date = entry.get("timestamp", "")[:10]
                if entry_date != date:
                    continue

            total_trades += 1

            # Count successes/failures
            if entry.get("success", False):
                successes += 1
            else:
                failures += 1

            # Count live/paper
            if entry.get("simulated", False):
                paper_trades += 1
            else:
                live_trades += 1

            # Sum invested
            cost = entry.get("cost", 0.0)
            total_invested += cost

            # Track edge if available
            edge = entry.get("signal", {}).get("edge")
            if edge is not None:
                edges.append(edge)

    order_success_rate = (successes / total_trades * 100) if total_trades > 0 else 0.0
    avg_edge = sum(edges) / len(edges) if edges else 0.0

    return {
        "total_trades": total_trades,
        "successes": successes,
        "failures": failures,
        "live_trades": live_trades,
        "paper_trades": paper_trades,
        "order_success_rate": round(order_success_rate, 2),
        "total_invested_usd": round(total_invested, 2),
        "avg_edge": round(avg_edge, 4),
    }


# =============================================================================
# Autotuning Functions
# =============================================================================


def compute_health_score(
    trades_path: str,
    skill: str,
    half_life_days: int = 180,
) -> dict:
    """
    Compute a weighted health score (0-100) for a trading strategy.

    Uses exponential half-life decay to weight recent trades more heavily.
    Components: win_rate (40%), pnl_score (30%), consistency (20%), activity (10%).

    Args:
        trades_path: Path to trades.jsonl file
        skill: Skill slug to filter trades
        half_life_days: Half-life for exponential decay weighting (default 180)

    Returns:
        Dict with: health_score, components, halflife_days, trades_analyzed
        Returns health_score=50 with reason="insufficient data" when < 3 trades
    """
    path = Path(trades_path)
    if not path.exists():
        return {
            "health_score": 50,
            "reason": "insufficient data",
            "components": {},
            "halflife_days": half_life_days,
            "trades_analyzed": 0,
        }

    now = datetime.now(timezone.utc)
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
            # Filter by skill and exclude simulated
            if entry.get("skill") != skill or entry.get("simulated", False):
                continue
            trades.append(entry)

    if len(trades) < 3:
        return {
            "health_score": 50,
            "reason": "insufficient data",
            "components": {},
            "halflife_days": half_life_days,
            "trades_analyzed": len(trades),
        }

    # Compute weights and weighted metrics
    weighted_wins = 0.0
    weighted_total = 0.0
    daily_counts = {}
    recent_7d = 0

    for t in trades:
        ts_str = t.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(ts_str)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            continue

        days_ago = (now - ts).days
        weight = math.exp(-days_ago / half_life_days)

        success = t.get("success", False)
        weighted_total += weight
        if success:
            weighted_wins += weight

        # Group by day for consistency
        day_key = ts.strftime("%Y-%m-%d")
        daily_counts[day_key] = daily_counts.get(day_key, 0) + 1

        # Count recent 7 days
        if days_ago <= 7:
            recent_7d += 1

    if weighted_total == 0:
        return {
            "health_score": 50,
            "reason": "insufficient data",
            "components": {},
            "halflife_days": half_life_days,
            "trades_analyzed": len(trades),
        }

    # Win rate component (40%)
    win_rate_val = (weighted_wins / weighted_total) * 100

    # PnL score component (30%): map win_rate to -1..+1 then to 0..100
    pnl_raw = (win_rate_val / 100) * 2 - 1  # -1 to +1
    pnl_score = (pnl_raw + 1) / 2 * 100  # 0 to 100

    # Consistency component (20%): 1 - CV, clamped 0-100
    counts = list(daily_counts.values())
    if len(counts) > 1 and statistics.mean(counts) > 0:
        cv = statistics.stdev(counts) / statistics.mean(counts)
        consistency = max(0, min(100, (1 - cv) * 100))
    else:
        consistency = 50.0

    # Activity component (10%): min(recent_7d / 5, 1.0) * 100
    activity = min(recent_7d / 5, 1.0) * 100

    # Weighted final score
    health_score = (
        0.40 * win_rate_val + 0.30 * pnl_score + 0.20 * consistency + 0.10 * activity
    )

    return {
        "health_score": round(health_score, 1),
        "components": {
            "win_rate": round(win_rate_val, 1),
            "pnl_score": round(pnl_score, 1),
            "consistency": round(consistency, 1),
            "activity": round(activity, 1),
        },
        "halflife_days": half_life_days,
        "trades_analyzed": len(trades),
    }


def suggest_tuning(
    trades_path: str,
    skill: str,
    config_schema=None,
) -> dict:
    """
    Suggest a single-parameter tuning adjustment based on trade history.

    Implements the autoresearch single-variable principle: only one parameter
    changes per cycle for causal attribution. Cold start guard blocks when < 20 trades.

    Args:
        trades_path: Path to trades.jsonl file
        skill: Skill slug to filter trades
        config_schema: Optional config schema (unused, for future expansion)

    Returns:
        Dict with: parameter, old_value, new_value, reason, confidence
        Returns parameter=None when no clear improvement target
    """
    # Cold start guard
    metrics = aggregate_trades(trades_path, skill=skill)
    total_trades = metrics.get("total_trades", 0)

    if total_trades < 20:
        return {
            "parameter": None,
            "old_value": None,
            "new_value": None,
            "reason": f"insufficient trades ({total_trades} < 20)",
            "confidence": "low",
        }

    win_rate = metrics.get("order_success_rate", 0)
    avg_edge = metrics.get("avg_edge", 0)
    failures = metrics.get("failures", 0)

    # Try to load current config values
    old_threshold = 0.05  # sensible default
    old_position = 5.0  # sensible default
    try:
        from simmer_sdk.skill import load_config, get_config_path

        config = load_config(config_schema, get_config_path(__file__))
        old_threshold = config.get("entry_threshold", old_threshold)
        old_position = config.get(
            "max_position", config.get("max_position_usd", old_position)
        )
    except (ImportError, Exception):
        pass

    # Decision tree (priority order)
    if win_rate < 40:
        new_val = round(old_threshold * 1.10, 4)
        new_val = max(0.01, min(0.50, new_val))
        return {
            "parameter": "entry_threshold",
            "old_value": old_threshold,
            "new_value": new_val,
            "reason": f"win_rate {win_rate:.1f}% below 40%, increase threshold by 10%",
            "confidence": "high",
        }

    if win_rate > 70 and failures > 0:
        new_val = round(old_position * 0.85, 2)
        new_val = max(0.50, min(50.0, new_val))
        return {
            "parameter": "max_position_usd",
            "old_value": old_position,
            "new_value": new_val,
            "reason": f"high win_rate {win_rate:.1f}% but {failures} losses, reduce position by 15%",
            "confidence": "medium",
        }

    if avg_edge < 0.02:
        new_val = round(old_threshold * 1.10, 4)
        new_val = max(0.01, min(0.50, new_val))
        return {
            "parameter": "entry_threshold",
            "old_value": old_threshold,
            "new_value": new_val,
            "reason": f"avg_edge {avg_edge:.4f} too thin (<0.02), increase threshold by 10%",
            "confidence": "medium",
        }

    return {
        "parameter": None,
        "old_value": None,
        "new_value": None,
        "reason": "no clear improvement target",
        "confidence": "low",
    }


def log_param_change(entry: dict) -> None:
    """
    Append a parameter change entry to changelog.jsonl.

    Auto-adds UTC timestamp if not present. Never overwrites existing entries.

    Args:
        entry: Dict with parameter change details (parameter, old_value, new_value,
               reason, status, etc.)
    """
    changelog_path = Path(__file__).parent / "changelog.jsonl"
    if "timestamp" not in entry:
        entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    with open(changelog_path, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")


def read_changelog(
    skill: str = None,
    status: str = None,
    last_n: int = None,
) -> list:
    """
    Read and filter changelog entries from changelog.jsonl.

    Args:
        skill: Filter by skill slug (optional)
        status: Filter by status value (optional)
        last_n: Return only the last N entries (optional)

    Returns:
        List of matching entry dicts, or [] if file doesn't exist
    """
    changelog_path = Path(__file__).parent / "changelog.jsonl"
    if not changelog_path.exists():
        return []

    entries = []
    with open(changelog_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            # Apply filters
            if skill and entry.get("skill") != skill:
                continue
            if status and entry.get("status") != status:
                continue
            entries.append(entry)

    if last_n is not None:
        entries = entries[-last_n:]

    return entries


# =============================================================================
# CLI
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Trade Performance CLI - Reporting, validation, circuit breaker control"
    )
    parser.add_argument(
        "--report",
        nargs="*",
        help="Generate trade report. Optional: skill=X date=YYYY-MM-DD",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate trades.jsonl schema compliance",
    )
    parser.add_argument(
        "--resume",
        metavar="SKILL_DIR",
        help="Force resume by deleting circuit_breaker.json",
    )
    parser.add_argument(
        "--auto-tune",
        nargs="?",
        const=SKILL_SLUG,
        metavar="SKILL",
        help="Run autoresearch suggest_tuning() for skill",
    )
    parser.add_argument(
        "--health-score",
        nargs="?",
        const=SKILL_SLUG,
        metavar="SKILL",
        help="Compute health score for skill (or 'all')",
    )
    parser.add_argument(
        "--changelog",
        action="store_true",
        help="Show changelog",
    )
    parser.add_argument(
        "--last",
        type=int,
        default=10,
        help="Show last N entries (with --changelog)",
    )
    parser.add_argument(
        "--status",
        choices=["pending", "keep", "reverted"],
        help="Filter by status (with --changelog)",
    )
    parser.add_argument(
        "--revert-last",
        nargs="?",
        const=SKILL_SLUG,
        metavar="SKILL",
        help="Revert last parameter change for skill",
    )

    args = parser.parse_args()

    if args.report is not None:
        # Parse filter options
        skill = None
        date = None
        for item in args.report:
            if item.startswith("skill="):
                skill = item.split("=", 1)[1]
            elif item.startswith("date="):
                date = item.split("=", 1)[1]

        # Get trades path
        if skill:
            # Look in skill directory
            base = Path(__file__).parent.parent / skill
            trades_path = base / "trades.jsonl"
        else:
            trades_path = get_trades_path()

        if not trades_path.exists():
            print(json.dumps({"error": f"No trades.jsonl at {trades_path}"}))
            sys.exit(1)

        stats = aggregate_trades(str(trades_path), skill=skill, date=date)
        print(json.dumps(stats, indent=2))
        return

    if args.validate:
        trades_path = get_trades_path()
        if not trades_path.exists():
            print("No trades.jsonl found")
            sys.exit(0)

        # Check last N lines
        with open(trades_path, "r") as f:
            lines = f.readlines()

        valid_count = 0
        invalid_count = 0
        errors = []

        for i, line in enumerate(lines[-10:]):  # Last 10 lines
            line = line.strip()
            if not line:
                continue

            try:
                entry = json.loads(line)
                # Check required fields
                required = ["timestamp", "skill", "source", "success", "simulated"]
                missing = [k for k in required if k not in entry]
                if missing:
                    invalid_count += 1
                    errors.append(f"Line {i + 1}: missing {missing}")
                else:
                    valid_count += 1
            except json.JSONDecodeError as e:
                invalid_count += 1
                errors.append(f"Line {i + 1}: {e}")

        print(f"Valid lines: {valid_count}")
        print(f"Invalid lines: {invalid_count}")
        if errors:
            print("\nErrors:")
            for err in errors[:5]:
                print(f"  {err}")
        return

    if args.resume:
        cb_path = Path(args.resume) / "circuit_breaker.json"
        if cb_path.exists():
            cb_path.unlink()
            print(f"Deleted {cb_path} - circuit breaker force-resumed")
        else:
            print(f"No circuit_breaker.json in {args.resume}")
        return

    if args.revert_last is not None:
        skill_slug = args.revert_last
        # Read changelog, find last entry with status "keep" or "pending"
        entries = read_changelog(skill=skill_slug)
        revertable = [e for e in entries if e.get("status") in ("keep", "pending")]
        if not revertable:
            print(
                json.dumps(
                    {"error": "no revertable entries found", "skill": skill_slug}
                )
            )
            sys.exit(1)
        last = revertable[-1]
        # Create revert entry: swap old/new values, mark as reverted
        revert_entry = {
            "parameter": last.get("parameter"),
            "old_value": last.get("new_value"),
            "new_value": last.get("old_value"),
            "reason": f"revert of: {last.get('reason', '')}",
            "status": "reverted",
            "skill": skill_slug,
            "reverts_timestamp": last.get("timestamp"),
        }
        log_param_change(revert_entry)
        print(json.dumps({"reverted": True, "entry": revert_entry}, indent=2))
        return

    if args.changelog:
        entries = read_changelog(skill=SKILL_SLUG, status=args.status, last_n=args.last)
        print(json.dumps(entries, indent=2))
        return

    if args.health_score is not None:
        skill_slug = args.health_score
        # Resolve trades path from skill slug (same pattern as --report)
        if skill_slug and skill_slug != "all":
            base = Path(__file__).parent.parent / skill_slug
            trades_path = base / "trades.jsonl"
        else:
            trades_path = get_trades_path()
        if skill_slug == "all":
            skills = [SKILL_SLUG]
        else:
            skills = [skill_slug]
        results = []
        for s in skills:
            result = compute_health_score(str(trades_path), s)
            results.append(result)
        if len(results) == 1:
            print(json.dumps(results[0], indent=2))
        else:
            print(json.dumps(results, indent=2))
        return

    if args.auto_tune is not None:
        skill_slug = args.auto_tune
        # Resolve trades path from skill slug (same pattern as --report)
        if skill_slug:
            base = Path(__file__).parent.parent / skill_slug
            trades_path = base / "trades.jsonl"
        else:
            trades_path = get_trades_path()
        # Load config from skill's trader module
        config = None
        try:
            skill_dir = Path(__file__).parent.parent / skill_slug
            trader_name = skill_dir.name.replace("-", "_") + "_trader"
            trader_path = skill_dir / f"{skill_dir.name.replace('-', '_')}_trader.py"
            if trader_path.exists():
                spec = importlib.util.spec_from_file_location(
                    trader_name, str(trader_path)
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    from simmer_sdk.skill import load_config, get_config_path

                    config = load_config(
                        module.CONFIG_SCHEMA,
                        get_config_path(str(trader_path)),
                    )
        except Exception:
            pass  # suggest_tuning will use defaults
        result = suggest_tuning(str(trades_path), skill_slug, config)
        print(json.dumps(result, indent=2))
        # Log as pending if a suggestion was found
        if result.get("parameter"):
            log_param_change({**result, "status": "pending", "skill": skill_slug})
        return

    # No args - show help
    parser.print_help()


if __name__ == "__main__":
    main()
