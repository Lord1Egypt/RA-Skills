#!/usr/bin/env python3
"""Run collection, analysis, and dashboard rendering in one command."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(command: list[str], cwd: Path) -> None:
    print("+ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=str(cwd), check=True)


def run_auto_upgrade_plan(args: argparse.Namespace, root: Path, data_dir: Path, report_dir: Path) -> None:
    if not (args.auto_upgrade_plan or args.auto_upgrade_apply_safe):
        return
    auto_upgrade = [
        sys.executable,
        str(root / "scripts" / "auto_upgrade.py"),
        "--handle",
        args.handle,
        "--data-dir",
        str(data_dir),
        "--skills-root",
        args.skills_root,
        "--out-dir",
        str(report_dir / "auto_upgrade"),
        "--limit",
        str(args.auto_upgrade_limit),
        "--source-cache-dir",
        args.source_cache_dir,
    ]
    if args.github_owner:
        auto_upgrade.extend(["--github-owner", args.github_owner])
    for extra_root in args.extra_skill_root:
        auto_upgrade.extend(["--extra-root", extra_root])
    if args.auto_upgrade_fetch_source:
        auto_upgrade.append("--fetch-source")
    if args.auto_upgrade_apply_safe:
        auto_upgrade.append("--apply-safe")
    run(auto_upgrade, root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handle", default="harrylabsj")
    parser.add_argument("--page-size", type=int, default=200)
    parser.add_argument("--detail-concurrency", type=int, default=8)
    parser.add_argument("--skip-details", action="store_true")
    parser.add_argument("--baseline", action="store_true", help="Treat this run as a new snapshot baseline.")
    parser.add_argument("--auto-upgrade-plan", action="store_true", help="Generate an AI-assisted maintenance plan after analysis.")
    parser.add_argument("--auto-upgrade-apply-safe", action="store_true", help="Apply deterministic append-only SKILL.md improvements for selected candidates.")
    parser.add_argument("--auto-upgrade-fetch-source", action="store_true", help="Fetch missing auto-upgrade sources from GitHub first, then ClawHub.")
    parser.add_argument("--auto-upgrade-limit", type=int, default=5, help="Number of auto-upgrade candidates to plan.")
    parser.add_argument("--skills-root", default="~/.openclaw/skills", help="Local skill source root for maintenance candidate planning.")
    parser.add_argument("--extra-skill-root", action="append", default=[], help="Additional local source root for maintenance candidate planning.")
    parser.add_argument("--source-cache-dir", default=".cache/auto_upgrade_sources", help="Cache directory for fetched auto-upgrade sources.")
    parser.add_argument("--github-owner", default="", help="GitHub owner to probe for missing auto-upgrade sources; defaults to --handle.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    report_dir = root / "reports"

    collect = [
        sys.executable,
        str(root / "scripts" / "collect_clawhub_skills.py"),
        "--handle",
        args.handle,
        "--out-dir",
        str(data_dir),
        "--page-size",
        str(args.page_size),
        "--detail-concurrency",
        str(args.detail_concurrency),
    ]
    if args.skip_details:
        collect.append("--skip-details")

    run(collect, root)
    run(
        [
            sys.executable,
            str(root / "scripts" / "analyze_skills.py"),
            "--handle",
            args.handle,
            "--data-dir",
            str(data_dir),
        ],
        root,
    )
    snapshot = [
        sys.executable,
        str(root / "scripts" / "write_snapshot.py"),
        "--handle",
        args.handle,
        "--data-dir",
        str(data_dir),
    ]
    if args.baseline:
        snapshot.append("--baseline")
    run(snapshot, root)
    run(
        [
            sys.executable,
            str(root / "scripts" / "plan_actions.py"),
            "--handle",
            args.handle,
            "--data-dir",
            str(data_dir),
            "--out-dir",
            str(report_dir / "action_plans"),
            "--approval-dir",
            str(report_dir / "approval_packets"),
        ],
        root,
    )
    run(
        [
            sys.executable,
            str(root / "scripts" / "plan_bulk_cleanup.py"),
            "--handle",
            args.handle,
            "--data-dir",
            str(data_dir),
            "--out-dir",
            str(report_dir / "bulk_cleanup"),
        ],
        root,
    )
    run_auto_upgrade_plan(args, root, data_dir, report_dir)
    run(
        [
            sys.executable,
            str(root / "scripts" / "render_dashboard.py"),
            "--handle",
            args.handle,
            "--data-dir",
            str(data_dir),
            "--out-dir",
            str(report_dir),
        ],
        root,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
