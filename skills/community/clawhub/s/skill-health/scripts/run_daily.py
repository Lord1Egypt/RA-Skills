#!/usr/bin/env python3
"""
Run daily analysis and output JSON (stdout and/or file).

Usage:
  uv run python code/scripts/run_daily.py --data-dir data --output-dir outputs
  uv run python code/scripts/run_daily.py --data-path data/health_data_20260209_124646 --output-dir outputs --date 2026-01-15
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from _bootstrap import ensure_pkg_on_path

ensure_pkg_on_path()

from skill_health.analysis.daily import (
    build_daily_report,
    infer_target_date_from_bundle,
)
from skill_health.load import (
    load_health_data_from_directory,
    load_health_data_from_path,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Daily health analysis; outputs JSON to stdout and/or --output-dir."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--data-dir",
        type=Path,
        help="Directory with health_data_* folder(s) or ZIP(s).",
    )
    group.add_argument(
        "--data-path", type=Path, help="Path to health_data_* directory or ZIP."
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Target date YYYY-MM-DD; default: most recent date with data.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to save JSON (e.g. outputs/daily_2026-01-15.json).",
    )
    parser.add_argument(
        "--timezone",
        type=str,
        default="UTC",
        help="IANA timezone for naive timestamps (e.g. Europe/Madrid, America/New_York).",
    )
    args = parser.parse_args()

    os.environ["SKILL_HEALTH_TIMEZONE"] = args.timezone

    if args.data_dir is not None:
        bundle = load_health_data_from_directory(args.data_dir)
    else:
        bundle = load_health_data_from_path(args.data_path)

    if args.date is not None:
        target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        target_date = infer_target_date_from_bundle(bundle)

    payload = build_daily_report(bundle, target_date)
    json_str = json.dumps(payload, indent=2, ensure_ascii=False)

    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"daily_{target_date.isoformat()}.json"
        out_path = args.output_dir / filename
        out_path.write_text(json_str, encoding="utf-8")
        print(f"Wrote {out_path}", file=sys.stderr)

    print(json_str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
