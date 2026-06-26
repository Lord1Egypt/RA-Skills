#!/usr/bin/env python3
"""
Stable runner for daily A-share market evidence generation.

This wrapper avoids Windows shell redirection issues by calling the panel
builder directly, clearing broken local proxy variables, and writing
both the full evidence pack and a compact report_context JSON.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import market_panel


SCRIPT_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_ROOT.parent
DEFAULT_REPORTS_DIR = SKILL_ROOT / "reports"


def clear_proxy_env(env: dict) -> dict:
    cleaned = env.copy()
    for key in (
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
    ):
        cleaned.pop(key, None)
    cleaned["PYTHONIOENCODING"] = "utf-8"
    return cleaned


def sibling_stderr_path(evidence_path: Path) -> Path:
    return evidence_path.with_name(f"{evidence_path.stem}.stderr.log")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run market_panel.py safely and write UTF-8 evidence/context files."
    )
    parser.add_argument("--asof", default=None, help="Analysis date, YYYYMMDD or YYYY-MM-DD. Defaults to today.")
    parser.add_argument("--offset", type=int, default=0, help="Trading-day offset from asof.")
    parser.add_argument("--allow-future", action="store_true", help="Allow positive offset for post-hoc checks.")
    parser.add_argument("--lookback", type=int, default=120, help="Number of trading days to load.")
    parser.add_argument("--index", default="000300.SH", help="Benchmark index ts_code.")
    parser.add_argument("--sample-limit", type=int, default=40, help="Generic candidate sample limit.")
    parser.add_argument("--market-trend-days", type=int, default=90, help="Market-trend window.")
    parser.add_argument("--index-kline-days", type=int, default=market_panel.DEFAULT_INDEX_KLINE_DAYS, help="Index candlestick window for HTML output.")
    parser.add_argument("--sleep", type=float, default=0.12, help="Sleep seconds between uncached API calls.")
    parser.add_argument("--fetch-workers", type=int, default=6, help="Max worker threads for cache/API fetching.")
    parser.add_argument("--no-cache", action="store_true", help="Disable cache in market_panel.py.")
    parser.add_argument("--refresh-cache", action="store_true", help="Force refetch and overwrite cache.")
    parser.add_argument("--with-limit", action="store_true", help="Fetch official limit_list_d stats.")
    parser.add_argument("--reports-dir", default=str(DEFAULT_REPORTS_DIR), help="Directory for generated files.")
    parser.add_argument("--evidence-out", default=None, help="Full evidence JSON output path.")
    parser.add_argument("--context-out", default=None, help="Compact report_context JSON output path.")
    parser.add_argument("--module-context-dir", default=None, help="Directory for module-level subagent JSON files.")
    parser.add_argument("--no-module-context", action="store_true", help="Skip module-level subagent JSON files.")
    parser.add_argument("--stderr-out", default=None, help="Stderr log output path.")
    parser.add_argument("--money-context-limit", type=int, default=80, help="Money-effect rows in context.")
    parser.add_argument("--decline-context-limit", type=int, default=20, help="Volume-decline rows in context.")
    parser.add_argument("--feature-context-limit", type=int, default=20, help="Module 5 feature-group rows per subgroup in context.")
    parser.add_argument("--amount-context-limit", type=int, default=20, help="Top-amount rows in context.")
    return parser


def build_panel_argv(args: argparse.Namespace, extra_args: List[str]) -> List[str]:
    argv = [
        "panel",
        "--lookback",
        str(args.lookback),
        "--index",
        args.index,
        "--sample-limit",
        str(args.sample_limit),
        "--market-trend-days",
        str(args.market_trend_days),
        "--index-kline-days",
        str(args.index_kline_days),
        "--sleep",
        str(args.sleep),
        "--fetch-workers",
        str(args.fetch_workers),
        "--offset",
        str(args.offset),
    ]
    if args.asof:
        argv.extend(["--asof", args.asof])
    if args.allow_future:
        argv.append("--allow-future")
    if args.no_cache:
        argv.append("--no-cache")
    if args.refresh_cache:
        argv.append("--refresh-cache")
    if args.with_limit:
        argv.append("--with-limit")
    argv.extend(extra_args)
    return argv


def default_stem(asof: Optional[str]) -> str:
    date = market_panel.normalize_date(asof) if asof else datetime.now().strftime("%Y%m%d")
    return f"evidence_{date}_utf8"


@contextlib.contextmanager
def patched_environment(env: Dict[str, str]):
    original = os.environ.copy()
    try:
        os.environ.clear()
        os.environ.update(env)
        yield
    finally:
        os.environ.clear()
        os.environ.update(original)


def write_module_contexts(evidence: dict, module_dir: Path) -> None:
    module_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in market_panel.build_module_contexts(evidence).items():
        (module_dir / f"{name}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args, extra_args = parser.parse_known_args(argv)

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    preliminary_evidence = Path(args.evidence_out) if args.evidence_out else reports_dir / f"{default_stem(args.asof)}.json"
    stderr_path = Path(args.stderr_out) if args.stderr_out else sibling_stderr_path(preliminary_evidence)

    env = clear_proxy_env(os.environ)
    panel_argv = build_panel_argv(args, extra_args)
    stderr_buffer = io.StringIO()
    try:
        panel_args = market_panel.build_arg_parser().parse_args(panel_argv)
        with patched_environment(env), contextlib.redirect_stderr(stderr_buffer):
            evidence = market_panel.build_panel(panel_args)
    finally:
        stderr_path.write_text(stderr_buffer.getvalue(), encoding="utf-8")

    resolved_date = evidence.get("metadata", {}).get("resolved_trade_date") or market_panel.normalize_date(args.asof)
    evidence_path = Path(args.evidence_out) if args.evidence_out else reports_dir / f"evidence_{resolved_date}_utf8.json"
    context_path = Path(args.context_out) if args.context_out else reports_dir / f"report_context_{resolved_date}.json"
    if args.stderr_out is None:
        stderr_path = sibling_stderr_path(evidence_path)
        stderr_path.write_text(stderr_buffer.getvalue(), encoding="utf-8")

    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    report_context = market_panel.build_report_context(
        evidence,
        money_limit=args.money_context_limit,
        decline_limit=args.decline_context_limit,
        feature_limit=args.feature_context_limit,
        amount_limit=args.amount_context_limit,
    )
    context_path.write_text(json.dumps(report_context, ensure_ascii=False, indent=2), encoding="utf-8")

    module_context_dir = None
    if not args.no_module_context:
        module_context_dir = Path(args.module_context_dir) if args.module_context_dir else reports_dir / f"module_context_{resolved_date}"
        write_module_contexts(evidence, module_context_dir)

    print(json.dumps({
        "resolved_trade_date": resolved_date,
        "evidence": str(evidence_path),
        "report_context": str(context_path),
        "module_context_dir": str(module_context_dir) if module_context_dir else None,
        "stderr": str(stderr_path),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
