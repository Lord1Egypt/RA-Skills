#!/usr/bin/env python3
"""
Run cross-temporal alerts analysis. Reads JSON from outputs dir, detects patterns, outputs JSON.

Usage:
  uv run python code/scripts/run_cross_alerts.py --outputs-dir outputs --output-dir outputs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _bootstrap import ensure_pkg_on_path

ensure_pkg_on_path()

from skill_health.analysis.cross_alerts import (
    build_cross_alerts,
    load_metrics_from_outputs_dir,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cross-temporal health alerts; reads JSON from --outputs-dir, outputs alerts to stdout and/or --output-dir."
    )
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory containing hourly_*.json, daily_*.json, weekly_*.json, monthly_*.json.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to save alerts JSON (e.g. outputs/cross_alerts.json).",
    )
    args = parser.parse_args()

    metrics_context = load_metrics_from_outputs_dir(args.outputs_dir)
    alerts = build_cross_alerts(metrics_context)
    payload = {"alerts": alerts, "count": len(alerts)}
    json_str = json.dumps(payload, indent=2, ensure_ascii=False)

    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        out_path = args.output_dir / "cross_alerts.json"
        out_path.write_text(json_str, encoding="utf-8")
        print(f"Wrote {out_path}", file=sys.stderr)

    print(json_str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
