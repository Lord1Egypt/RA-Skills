#!/usr/bin/env python3
"""Update watchers' fixed date ranges in seats-aero-monitor storage.

Usage:
  # Update specific watcher by ID
  python update_watcher_dates.py --watcher pvg_sfo_aeroplan_2026summer --start 2026-08-01 --end 2026-08-15

  # Update all watchers matching origin/destination pattern
  python update_watcher_dates.py --origin PVG --start 2026-08-01 --end 2026-08-15

  # Update all watchers (use with caution!)
  python update_watcher_dates.py --all --start 2026-08-01 --end 2026-08-15

  # JSON backend
  python update_watcher_dates.py --state-backend json --state-json ./monitor.json --all --start 2026-08-01 --end 2026-08-15

  # Dry run (preview changes without applying)
  python update_watcher_dates.py --origin PVG --start 2026-08-01 --end 2026-08-15 --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import replace
from pathlib import Path

if __package__ in (None, ""):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    from store import JsonStore, SqliteStore, Store, WatcherConfig, _default_state_db, _normalize_fixed_date  # type: ignore
else:
    from .store import JsonStore, SqliteStore, Store, WatcherConfig, _default_state_db, _normalize_fixed_date


def _matches_watcher(
    watcher: WatcherConfig,
    watcher_id: str | None,
    origin: str | None,
    destination: str | None,
    all_watchers: bool,
) -> bool:
    if all_watchers:
        return True
    if watcher_id and watcher.id != watcher_id:
        return False
    if origin and watcher.origin.upper() != origin.upper():
        return False
    if destination and watcher.destination.upper() != destination.upper():
        return False
    return bool(watcher_id or origin or destination)


def update_watchers(
    store: Store,
    watcher_id: str | None = None,
    origin: str | None = None,
    destination: str | None = None,
    all_watchers: bool = False,
    start_date: str | None = None,
    end_date: str | None = None,
    dry_run: bool = False,
    assume_yes: bool = False,
) -> int:
    if not (watcher_id or origin or destination or all_watchers):
        print("❌ Error: Must specify at least one of --watcher, --origin, --destination, or --all")
        return 1
    if not (start_date or end_date):
        print("❌ Error: Must specify at least one of --start or --end")
        return 1

    normalized_start = _normalize_fixed_date(start_date)
    normalized_end = _normalize_fixed_date(end_date)
    if normalized_start and normalized_end and normalized_end < normalized_start:
        print("❌ Error: --end cannot be earlier than --start")
        return 1

    watchers = store.list_watchers(include_disabled=True)
    selected = [
        watcher
        for watcher in watchers
        if _matches_watcher(watcher, watcher_id, origin, destination, all_watchers)
    ]

    if not selected:
        print("❌ No matching watchers found.")
        return 1

    print(f"📋 Found {len(selected)} watcher(s) to update:\n")
    updated_watchers: list[WatcherConfig] = []
    for watcher in selected:
        new_start = normalized_start if normalized_start is not None else watcher.fixed_start_date
        new_end = normalized_end if normalized_end is not None else watcher.fixed_end_date
        updated_watchers.append(
            replace(
                watcher,
                fixed_start_date=new_start,
                fixed_end_date=new_end,
            )
        )
        print(f"  - {watcher.id}: {watcher.origin}->{watcher.destination} ({watcher.program})")
        print(f"    Current: {watcher.fixed_start_date} to {watcher.fixed_end_date}")
        print(f"    New:     {new_start} to {new_end}")
        print()

    if dry_run:
        print("🔍 Dry run complete - no changes made.")
        return 0

    if not assume_yes:
        response = input("⚠️  Proceed with update? (y/N): ").strip().lower()
        if response != "y":
            print("❌ Update cancelled.")
            return 1

    summary = store.upsert_watchers(updated_watchers, replace=False)
    print(f"\n✅ Successfully updated {summary['input']} watcher(s)!")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update watchers' date ranges in seats-aero-monitor storage.")
    parser.add_argument("--state-backend", choices=["sqlite", "json"], default="sqlite", help="Storage backend: sqlite or json")
    parser.add_argument(
        "--state-db",
        "--db",
        dest="state_db",
        default=_default_state_db(),
        help="Path to SQLite state DB (used when --state-backend=sqlite)",
    )
    parser.add_argument(
        "--state-json",
        default=None,
        help="Path to JSON state file (used when --state-backend=json)",
    )
    parser.add_argument("--watcher", help="Update specific watcher by ID")
    parser.add_argument("--origin", help="Filter by origin airport (e.g., PVG)")
    parser.add_argument("--destination", help="Filter by destination airport (e.g., SFO)")
    parser.add_argument("--all", action="store_true", help="Update ALL watchers (use with caution!)")
    parser.add_argument("--start", dest="start_date", help="New fixed_start_date (YYYY-MM-DD)")
    parser.add_argument("--end", dest="end_date", help="New fixed_end_date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.state_backend == "json":
        if not args.state_json:
            print("❌ Error: --state-json is required when --state-backend=json")
            return 1
        store: Store = JsonStore(Path(args.state_json).resolve())
    else:
        store = SqliteStore(Path(args.state_db).resolve())

    try:
        return update_watchers(
            store=store,
            watcher_id=args.watcher,
            origin=args.origin,
            destination=args.destination,
            all_watchers=args.all,
            start_date=args.start_date,
            end_date=args.end_date,
            dry_run=args.dry_run,
            assume_yes=args.yes,
        )
    finally:
        store.close()


if __name__ == "__main__":
    raise SystemExit(main())
