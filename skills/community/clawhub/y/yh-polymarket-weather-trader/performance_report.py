#!/usr/bin/env python3
"""Performance report for Simmer trading skill.

Usage:
    python performance_report.py                     # Today's report for this skill
    python performance_report.py --date 2026-03-28   # Specific date
    python performance_report.py --skill all          # All skills in trades.jsonl
    python performance_report.py --json               # JSON output
    python performance_report.py --last 7             # Last 7 days
    python performance_report.py --snapshot            # Write snapshot to performance_snapshot.json
    python performance_report.py --quiet              # Suppress table output
"""

import json
import sys
import argparse
import statistics
from pathlib import Path
from datetime import datetime, timezone, timedelta

SKILL_SLUG = "polymarket-weather-trader"
TRADE_SOURCE = "sdk:weather"

# Resolve trade_performance module path (same directory as this script)
sys.path.insert(0, str(Path(__file__).parent))
from trade_performance import aggregate_trades, compute_health_score, read_changelog


def get_trades_path(skill_slug: str = None) -> Path:
    """Get trades.jsonl path. For 'all' or specific skill, look in each skill dir."""
    return Path(__file__).parent / "trades.jsonl"


def compute_edge_distribution(
    trades_path: str, skill: str = None, date: str = None
) -> dict:
    """Compute min, max, median of edge values from signal data."""
    path = Path(trades_path)
    if not path.exists():
        return {"min": 0.0, "max": 0.0, "median": 0.0}

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

            if skill and entry.get("skill") != skill:
                continue
            if date and entry.get("timestamp", "")[:10] != date:
                continue

            edge = entry.get("signal", {}).get("edge")
            if edge is not None:
                edges.append(edge)

    if not edges:
        return {"min": 0.0, "max": 0.0, "median": 0.0}

    return {
        "min": round(min(edges), 4),
        "max": round(max(edges), 4),
        "median": round(statistics.median(edges), 4),
    }


def format_table(metrics: dict, skill: str, date_label: str) -> str:
    """Format metrics as a human-readable table."""
    lines = [
        "=" * 40,
        f"  Performance: {skill}",
        "=" * 40,
        f"  Date:         {date_label}",
        f"  Total trades: {metrics['total_trades']}",
        f"  Successes:    {metrics['successes']} ({metrics['order_success_rate']:.1f}%)",
        f"  Failures:     {metrics['failures']}",
        f"  Live trades:  {metrics['live_trades']}",
        f"  Paper trades: {metrics['paper_trades']}",
        f"  Invested:     ${metrics['total_invested_usd']:.2f}",
        f"  Avg edge:     {metrics['avg_edge']:.2f}%",
    ]

    if "edge_distribution" in metrics:
        ed = metrics["edge_distribution"]
        lines.append(
            f"  Edge range:   {ed['min']:.2f}% - {ed['max']:.2f}% (median {ed['median']:.2f}%)"
        )

    if "trades_today" in metrics:
        lines.append(f"  Today:        {metrics['trades_today']} trades")

    lines.append("=" * 40)
    return "\n".join(lines)


def build_snapshot(skill: str, date_str: str, metrics: dict) -> dict:
    """Build snapshot object for performance_snapshot.json."""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "skill": skill,
        "date": date_str,
        "metrics": metrics,
    }


def write_snapshot(snapshot: dict, trades_dir: Path) -> None:
    """Write snapshot to performance_snapshot.json."""
    snapshot_path = trades_dir / "performance_snapshot.json"
    with open(snapshot_path, "w") as f:
        json.dump(snapshot, f, indent=2)


def collect_all_skills(trades_path: Path) -> list:
    """Find all unique skill slugs in trades.jsonl."""
    skills = set()
    if not trades_path.exists():
        return []
    with open(trades_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if "skill" in entry:
                    skills.add(entry["skill"])
            except json.JSONDecodeError:
                continue
    return sorted(skills)


def main():
    parser = argparse.ArgumentParser(
        description="Performance report for Simmer trading skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        help="Filter by specific date",
    )
    parser.add_argument(
        "--skill",
        default=SKILL_SLUG,
        help=f"Skill slug to report on (default: {SKILL_SLUG}). Use 'all' for all skills.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output raw JSON instead of table",
    )
    parser.add_argument(
        "--last",
        type=int,
        metavar="N",
        help="Show report for last N days",
    )
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="Write performance_snapshot.json after report",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress table output (useful with --snapshot)",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="Show health score with component breakdown",
    )

    args = parser.parse_args()

    # Handle --health flag
    if args.health:
        trades_path = Path(__file__).parent / "trades.jsonl"
        if not trades_path.exists():
            print("No trades recorded yet")
            sys.exit(0)

        skills_to_check = []
        if args.skill == "all":
            skills_to_check = collect_all_skills(trades_path)
        else:
            skills_to_check = [args.skill or SKILL_SLUG]

        for skill_slug in skills_to_check:
            result = compute_health_score(str(trades_path), skill_slug)
            if args.json_output:
                print(json.dumps(result, indent=2))
            else:
                score = result.get("health_score", 0)
                stars = "\u2605" * int(score / 20) + "\u2606" * (5 - int(score / 20))
                print(f"=== Health: {skill_slug} ===")
                print(f"  Score:  {score}/100 [{stars}]")
                comps = result.get("components", {})
                print(f"  Win Rate:    {comps.get('win_rate', 0):.0f}/100")
                print(f"  PnL Score:   {comps.get('pnl_score', 0):.0f}/100")
                print(f"  Consistency: {comps.get('consistency', 0):.0f}/100")
                print(f"  Activity:    {comps.get('activity', 0):.0f}/100")
                print(f"  Trades analyzed: {result.get('trades_analyzed', 0)}")
                if "reason" in result:
                    print(f"  Note: {result['reason']}")
                print()

        sys.exit(0)

    trades_dir = Path(__file__).parent
    trades_path = trades_dir / "trades.jsonl"

    # Handle missing/empty trades.jsonl
    if not trades_path.exists() or trades_path.stat().st_size == 0:
        print("No trades recorded yet")
        sys.exit(0)

    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    date_str = args.date or today_str

    # Multi-day report
    if args.last:
        for day_offset in range(args.last - 1, -1, -1):
            d = (datetime.now(timezone.utc) - timedelta(days=day_offset)).strftime(
                "%Y-%m-%d"
            )
            metrics = aggregate_trades(
                str(trades_path),
                skill=args.skill if args.skill != "all" else None,
                date=d,
            )
            edge_dist = compute_edge_distribution(
                str(trades_path),
                skill=args.skill if args.skill != "all" else None,
                date=d,
            )
            metrics["edge_distribution"] = edge_dist

            if args.json_output:
                print(json.dumps({"date": d, **metrics}))
            else:
                print(format_table(metrics, args.skill, d))
        return

    # Single skill or all skills
    if args.skill == "all":
        skills = collect_all_skills(trades_path)
        if not skills:
            print("No trades recorded yet")
            sys.exit(0)

        for skill_slug in skills:
            metrics = aggregate_trades(
                str(trades_path), skill=skill_slug, date=args.date
            )
            edge_dist = compute_edge_distribution(
                str(trades_path), skill=skill_slug, date=args.date
            )
            metrics["edge_distribution"] = edge_dist

            if args.json_output:
                print(json.dumps({"skill": skill_slug, **metrics}))
            else:
                print(format_table(metrics, skill_slug, date_str))
                print()

        return

    # Single skill report
    metrics = aggregate_trades(str(trades_path), skill=args.skill, date=args.date)
    edge_dist = compute_edge_distribution(
        str(trades_path), skill=args.skill, date=args.date
    )
    metrics["edge_distribution"] = edge_dist

    # Count trades today for this skill
    today_metrics = aggregate_trades(str(trades_path), skill=args.skill, date=today_str)
    metrics["trades_today"] = today_metrics["total_trades"]

    if args.json_output:
        print(json.dumps(metrics, indent=2))
    else:
        print(format_table(metrics, args.skill, date_str))

    # Snapshot
    if args.snapshot or not args.quiet:
        snapshot = build_snapshot(args.skill, date_str, metrics)
        write_snapshot(snapshot, trades_dir)
        if not args.quiet:
            print(f"Snapshot written to {trades_dir / 'performance_snapshot.json'}")


if __name__ == "__main__":
    main()
