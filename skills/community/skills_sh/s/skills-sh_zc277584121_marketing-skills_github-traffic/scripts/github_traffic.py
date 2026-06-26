#!/usr/bin/env python3
"""
Fetch and visualize GitHub repository traffic data.

Collects views, clones, referrers, and popular paths from the GitHub API,
stores historical data in a local JSON file, and generates trend charts
using matplotlib (ASCII fallback if matplotlib is unavailable).

Prerequisites:
  - gh CLI (authenticated with repo push access)
  - matplotlib (optional, for PNG chart generation)

Usage:
    # Fetch and display current traffic
    python github_traffic.py zilliztech/memsearch

    # Fetch, store history, and generate charts
    python github_traffic.py zilliztech/memsearch --chart

    # Generate chart for last 7 days
    python github_traffic.py zilliztech/memsearch --chart --days 7

    # Generate chart for last 90 days (requires stored history)
    python github_traffic.py zilliztech/memsearch --chart --days 90

    # Custom history file location
    python github_traffic.py zilliztech/memsearch --chart --history-dir ./data

    # Snapshot only: fetch and store data without display
    python github_traffic.py zilliztech/memsearch --snapshot
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def gh_api(endpoint: str) -> dict | list:
    """Call GitHub API via gh CLI and return parsed JSON."""
    result = subprocess.run(
        ["gh", "api", endpoint],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        error_msg = result.stderr.strip()
        if "Must have push access" in error_msg or "403" in error_msg:
            print(f"Error: insufficient permissions for {endpoint}")
            print("Traffic data requires push (write) access to the repository.")
            print("Make sure your `gh` CLI is authenticated with a token that has repo write access.")
            sys.exit(1)
        raise RuntimeError(f"gh api failed: {error_msg}")
    return json.loads(result.stdout)


def fetch_traffic(repo: str) -> dict:
    """Fetch all traffic data for a repository."""
    views = gh_api(f"repos/{repo}/traffic/views")
    clones = gh_api(f"repos/{repo}/traffic/clones")
    referrers = gh_api(f"repos/{repo}/traffic/popular/referrers")
    paths = gh_api(f"repos/{repo}/traffic/popular/paths")
    stats = gh_api(f"repos/{repo}")

    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "repo": repo,
        "stars": stats.get("stargazers_count", 0),
        "forks": stats.get("forks_count", 0),
        "open_issues": stats.get("open_issues_count", 0),
        "views": {
            "total": views.get("count", 0),
            "unique": views.get("uniques", 0),
            "daily": [
                {
                    "date": v["timestamp"][:10],
                    "views": v["count"],
                    "unique": v["uniques"],
                }
                for v in views.get("views", [])
            ],
        },
        "clones": {
            "total": clones.get("count", 0),
            "unique": clones.get("uniques", 0),
            "daily": [
                {
                    "date": c["timestamp"][:10],
                    "clones": c["count"],
                    "unique": c["uniques"],
                }
                for c in clones.get("clones", [])
            ],
        },
        "referrers": [
            {"referrer": r["referrer"], "views": r["count"], "unique": r["uniques"]}
            for r in referrers
        ],
        "paths": [
            {"path": p["path"], "views": p["count"], "unique": p["uniques"]}
            for p in paths
        ],
    }


# ---------------------------------------------------------------------------
# History persistence
# ---------------------------------------------------------------------------

def _history_file(repo: str, history_dir: str) -> Path:
    """Return the path to the history JSON file for a repo."""
    safe_name = repo.replace("/", "_")
    return Path(history_dir) / f"{safe_name}_traffic.json"


def load_history(repo: str, history_dir: str) -> dict:
    """Load historical traffic data from disk."""
    path = _history_file(repo, history_dir)
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"repo": repo, "views": {}, "clones": {}, "stars": {}, "snapshots": []}


def save_history(repo: str, history_dir: str, traffic: dict, history: dict) -> None:
    """Merge current traffic into history and persist to disk."""
    os.makedirs(history_dir, exist_ok=True)

    # Merge daily views
    for day in traffic["views"]["daily"]:
        history["views"][day["date"]] = {"views": day["views"], "unique": day["unique"]}

    # Merge daily clones
    for day in traffic["clones"]["daily"]:
        history["clones"][day["date"]] = {"clones": day["clones"], "unique": day["unique"]}

    # Record stars snapshot
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    history["stars"][today] = traffic["stars"]

    # Keep last snapshot metadata
    history["snapshots"].append({
        "fetched_at": traffic["fetched_at"],
        "views_total_14d": traffic["views"]["total"],
        "clones_total_14d": traffic["clones"]["total"],
        "stars": traffic["stars"],
        "forks": traffic["forks"],
    })
    # Keep only last 200 snapshots
    history["snapshots"] = history["snapshots"][-200:]

    path = _history_file(repo, history_dir)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print(f"History saved to {path}")


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def display_traffic(traffic: dict) -> None:
    """Print a formatted traffic summary to stdout."""
    repo = traffic["repo"]
    print(f"\n{'=' * 60}")
    print(f"  GitHub Traffic: {repo}")
    print(f"{'=' * 60}")

    # Repo stats
    print(f"\n  Stars: {traffic['stars']}  |  Forks: {traffic['forks']}  |  Open Issues: {traffic['open_issues']}")

    # Views summary
    v = traffic["views"]
    print(f"\n  Views (14-day): {v['total']} total, {v['unique']} unique")
    if v["daily"]:
        print(f"  {'Date':<12} {'Views':>8} {'Unique':>8}")
        print(f"  {'-' * 28}")
        for day in v["daily"]:
            print(f"  {day['date']:<12} {day['views']:>8} {day['unique']:>8}")

    # Clones summary
    c = traffic["clones"]
    print(f"\n  Clones (14-day): {c['total']} total, {c['unique']} unique")
    if c["daily"]:
        print(f"  {'Date':<12} {'Clones':>8} {'Unique':>8}")
        print(f"  {'-' * 28}")
        for day in c["daily"]:
            print(f"  {day['date']:<12} {day['clones']:>8} {day['unique']:>8}")

    # Referrers
    if traffic["referrers"]:
        print(f"\n  Top Referrers:")
        print(f"  {'Source':<25} {'Views':>8} {'Unique':>8}")
        print(f"  {'-' * 41}")
        for r in traffic["referrers"]:
            print(f"  {r['referrer']:<25} {r['views']:>8} {r['unique']:>8}")

    # Popular paths
    if traffic["paths"]:
        print(f"\n  Popular Pages:")
        print(f"  {'Path':<50} {'Views':>8} {'Unique':>8}")
        print(f"  {'-' * 66}")
        for p in traffic["paths"][:10]:
            path_short = p["path"][-48:] if len(p["path"]) > 48 else p["path"]
            print(f"  {path_short:<50} {p['views']:>8} {p['unique']:>8}")

    print()


# ---------------------------------------------------------------------------
# Chart generation
# ---------------------------------------------------------------------------

def _filter_days(data: dict, days: int) -> list[tuple[str, dict]]:
    """Return sorted (date, values) pairs filtered to the last N days."""
    sorted_items = sorted(data.items())
    if days > 0:
        sorted_items = sorted_items[-days:]
    return sorted_items


def generate_chart(
    history: dict,
    output_path: str,
    days: int = 30,
    repo: str = "",
) -> bool:
    """Generate a traffic trend chart as PNG. Returns True on success."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        print("Warning: matplotlib not installed. Install with: pip install matplotlib")
        print("Falling back to ASCII chart.")
        return False

    views_data = _filter_days(history.get("views", {}), days)
    clones_data = _filter_days(history.get("clones", {}), days)
    stars_data = _filter_days(history.get("stars", {}), days)

    if not views_data and not clones_data:
        print("No historical data available for chart generation.")
        print("Run with --snapshot periodically to accumulate data (GitHub only provides 14-day windows).")
        return False

    # Determine subplot count
    has_stars = len(stars_data) > 1
    n_plots = 3 if has_stars else 2

    fig, axes = plt.subplots(n_plots, 1, figsize=(14, 4 * n_plots), sharex=False)
    if n_plots == 2:
        axes = list(axes) + [None]

    fig.suptitle(f"GitHub Traffic — {repo} (last {days} days)", fontsize=14, fontweight="bold")

    # --- Views chart ---
    if views_data:
        ax = axes[0]
        dates = [datetime.strptime(d, "%Y-%m-%d") for d, _ in views_data]
        views = [v["views"] for _, v in views_data]
        unique = [v["unique"] for _, v in views_data]

        ax.fill_between(dates, views, alpha=0.3, color="#4285f4", label="Total views")
        ax.plot(dates, views, color="#4285f4", linewidth=1.5)
        ax.fill_between(dates, unique, alpha=0.3, color="#34a853", label="Unique visitors")
        ax.plot(dates, unique, color="#34a853", linewidth=1.5)
        ax.set_ylabel("Views")
        ax.set_title("Page Views")
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    # --- Clones chart ---
    if clones_data:
        ax = axes[1]
        dates = [datetime.strptime(d, "%Y-%m-%d") for d, _ in clones_data]
        clones = [v["clones"] for _, v in clones_data]
        unique = [v["unique"] for _, v in clones_data]

        ax.bar(dates, clones, alpha=0.7, color="#ea4335", label="Total clones", width=0.8)
        ax.plot(dates, unique, color="#fbbc04", linewidth=2, marker="o", markersize=4, label="Unique cloners")
        ax.set_ylabel("Clones")
        ax.set_title("Git Clones")
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    # --- Stars chart ---
    if has_stars and axes[2] is not None:
        ax = axes[2]
        dates = [datetime.strptime(d, "%Y-%m-%d") for d, _ in stars_data]
        stars = [v for _, v in stars_data]

        ax.plot(dates, stars, color="#9c27b0", linewidth=2, marker="o", markersize=4)
        ax.fill_between(dates, stars, alpha=0.2, color="#9c27b0")
        ax.set_ylabel("Stars")
        ax.set_title("Star Growth")
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Chart saved to {output_path}")
    return True


def ascii_chart(history: dict, days: int = 14, metric: str = "views") -> None:
    """Print a simple ASCII bar chart as fallback when matplotlib is unavailable."""
    data = history.get(metric, {})
    items = _filter_days(data, days)
    if not items:
        print(f"No {metric} data available.")
        return

    key = "views" if metric == "views" else "clones"
    values = [(d, v[key]) for d, v in items]
    max_val = max(v for _, v in values) if values else 1

    print(f"\n  {metric.upper()} (last {len(values)} days)")
    print(f"  {'Date':<12} {'Count':>6}  {'Bar'}")
    print(f"  {'-' * 50}")
    for date, val in values:
        bar_len = int(val / max_val * 30) if max_val > 0 else 0
        bar = "#" * bar_len
        print(f"  {date:<12} {val:>6}  {bar}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fetch and visualize GitHub repository traffic data.",
        epilog="Note: Traffic API requires push (write) access to the repository.",
    )
    parser.add_argument("repo", help="Repository in owner/name format (e.g. zilliztech/memsearch)")
    parser.add_argument(
        "--chart",
        action="store_true",
        help="Generate trend chart (PNG with matplotlib, ASCII fallback)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days to show in chart (default: 30). Use 7, 14, 30, 90, etc.",
    )
    parser.add_argument(
        "--history-dir",
        default=None,
        help="Directory to store historical data (default: ~/.github-traffic/)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output path for chart image (default: <repo>_traffic.png in current dir)",
    )
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="Fetch and store data only, no display or chart",
    )
    parser.add_argument(
        "--ascii",
        action="store_true",
        help="Force ASCII chart output instead of PNG",
    )

    args = parser.parse_args()

    # Validate repo format
    if "/" not in args.repo:
        print(f"Error: repo must be in owner/name format, got: {args.repo}")
        sys.exit(1)

    history_dir = args.history_dir or os.path.expanduser("~/.github-traffic")

    # Fetch traffic data
    print(f"Fetching traffic data for {args.repo}...")
    traffic = fetch_traffic(args.repo)

    # Load and update history
    history = load_history(args.repo, history_dir)
    save_history(args.repo, history_dir, traffic, history)

    if args.snapshot:
        print("Snapshot saved. Run without --snapshot to see the report.")
        return

    # Display summary
    display_traffic(traffic)

    # Generate chart
    if args.chart or args.ascii:
        if args.ascii:
            ascii_chart(history, args.days, "views")
            ascii_chart(history, args.days, "clones")
        else:
            output_path = args.output or f"{args.repo.replace('/', '_')}_traffic.png"
            success = generate_chart(history, output_path, days=args.days, repo=args.repo)
            if not success:
                # Fallback to ASCII
                ascii_chart(history, args.days, "views")
                ascii_chart(history, args.days, "clones")


if __name__ == "__main__":
    main()
