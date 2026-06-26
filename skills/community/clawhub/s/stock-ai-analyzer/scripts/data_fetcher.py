#!/usr/bin/env python3
"""
Atomic Tushare data fetcher for the a-stock-analyzer skill.

This module intentionally does not generate analysis, prompts, reports,
recommendations, or combined outputs. It only resolves stock identifiers and
fetches one requested dataset at a time.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
from typing import Any, Callable, Dict, List, Optional

import pandas as pd

from cninfo import (
    CNINFO_ALLOWED_TAB_TYPES,
    CNINFO_REPORT_TYPES,
    DEFAULT_CNINFO_PAGE_SIZE,
    DEFAULT_CNINFO_TIMEOUT,
)
from common import dataframe_to_records, normalize_ts_code
from evidence_pack import build_evidence_pack, write_pack_outputs
from fetcher_core import StockDataFetcher

DatasetHandler = Callable[[StockDataFetcher, argparse.Namespace], Any]

def _dataset_handlers() -> Dict[str, DatasetHandler]:
    return {
        "company": lambda fetcher, args: fetcher.get_company(args.query),
        "financial": lambda fetcher, args: fetcher.get_financial_indicators(args.query, args.limit),
        "income": lambda fetcher, args: fetcher.get_income(args.query, args.limit),
        "balance": lambda fetcher, args: fetcher.get_balance(args.query, args.limit),
        "cashflow": lambda fetcher, args: fetcher.get_cashflow(args.query, args.limit),
        "daily": lambda fetcher, args: fetcher.get_daily(args.query, args.limit),
        "daily-basic": lambda fetcher, args: fetcher.get_daily_basic(args.query, args.limit),
        "valuation-band": lambda fetcher, args: fetcher.get_valuation_band(args.query, years=args.years),
        "main-business-product": lambda fetcher, args: fetcher.get_main_business(args.query, "P", args.limit),
        "main-business-region": lambda fetcher, args: fetcher.get_main_business(args.query, "D", args.limit),
        "top10-holders": lambda fetcher, args: fetcher.get_top10_holders(args.query, args.limit),
        "managers": lambda fetcher, args: fetcher.get_managers(args.query),
        "rewards": lambda fetcher, args: fetcher.get_rewards(args.query),
        "share-float": lambda fetcher, args: fetcher.get_share_float(args.query, limit=args.limit),
        "block-trade": lambda fetcher, args: fetcher.get_block_trade(args.query, limit=args.limit),
        "holder-trade": lambda fetcher, args: fetcher.get_holder_trade(args.query, limit=args.limit),
        "holder-number": lambda fetcher, args: fetcher.get_holder_number(args.query, args.limit),
        "institutional-research": (
            lambda fetcher, args: fetcher.get_institutional_research(
                args.query,
                start_date=args.start_date,
                end_date=args.end_date,
                trade_date=args.trade_date,
                limit=args.limit,
            )
        ),
        "announcements": (
            lambda fetcher, args: fetcher.get_announcements(
                args.query,
                tab_type=args.tabtype,
                date_range=args.date,
                searchkey=args.searchkey,
                category=args.category,
                trade=args.trade,
                page_num=args.page_num,
                page_size=args.page_size,
                limit=args.limit,
                include_excluded=args.include_excluded,
                timeout=args.timeout,
            )
        ),
        "announcement-raw": (
            lambda fetcher, args: fetcher.get_raw_announcement(
                args.query,
                tab_type=args.tabtype,
                date_range=args.date,
                searchkey=args.searchkey,
                category=args.category,
                trade=args.trade,
                announcement_index=args.announcement_index,
                include_excluded=args.include_excluded,
                download_dir=args.download_dir,
                timeout=args.timeout,
            )
        ),
        "announcement-text": (
            lambda fetcher, args: fetcher.get_announcement_text(
                args.query,
                tab_type=args.tabtype,
                date_range=args.date,
                searchkey=args.searchkey,
                category=args.category,
                trade=args.trade,
                announcement_index=args.announcement_index,
                include_excluded=args.include_excluded,
                max_pages=args.max_pages,
                max_chars=args.max_chars,
                to_markdown=args.to_markdown,
                section=args.section,
                timeout=args.timeout,
            )
        ),
        "report-list": (
            lambda fetcher, args: fetcher.get_report_announcements(
                args.query,
                report_type=args.report_type,
                report_year=args.report_year,
                limit=args.limit,
                include_variants=args.include_report_variants,
                timeout=args.timeout,
            )
        ),
        "report-raw": (
            lambda fetcher, args: fetcher.get_raw_report(
                args.query,
                report_type=args.report_type,
                report_year=args.report_year,
                report_index=args.report_index,
                include_variants=args.include_report_variants,
                download_dir=args.download_dir,
                timeout=args.timeout,
            )
        ),
        "report-text": (
            lambda fetcher, args: fetcher.get_report_text(
                args.query,
                report_type=args.report_type,
                report_year=args.report_year,
                report_index=args.report_index,
                include_variants=args.include_report_variants,
                max_pages=args.max_pages,
                max_chars=args.max_chars,
                to_markdown=args.to_markdown,
                section=args.section,
                timeout=args.timeout,
            )
        ),
    }


def serialize_payload(payload: Any) -> Any:
    """Convert supported fetch results to JSON-serializable values."""
    if isinstance(payload, pd.DataFrame):
        return dataframe_to_records(payload)
    if isinstance(payload, dict) or payload is None:
        return payload
    return payload


def print_payload(payload: Any, output_format: str) -> None:
    """Print raw fetched data in JSON or CSV."""
    if output_format == "csv":
        if isinstance(payload, pd.DataFrame):
            print(payload.to_csv(index=False))
            return
        print(pd.DataFrame([payload] if isinstance(payload, dict) else payload).to_csv(index=False))
        return

    print(json.dumps(serialize_payload(payload), ensure_ascii=False, indent=2, default=str))


def _add_shared_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments shared by ``fetch`` and ``pack`` subcommands."""
    parser.add_argument("--date", help="CNInfo date range: YYYY-MM-DD~YYYY-MM-DD.")
    parser.add_argument("--tabtype", choices=sorted(CNINFO_ALLOWED_TAB_TYPES), default="fulltext")
    parser.add_argument("--searchkey", default="")
    parser.add_argument("--category", default="")
    parser.add_argument("--trade", default="")
    parser.add_argument("--page-num", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=DEFAULT_CNINFO_PAGE_SIZE)
    parser.add_argument("--include-excluded", action="store_true")
    parser.add_argument("--start-date", help="Tushare start date: YYYYMMDD or YYYY-MM-DD.")
    parser.add_argument("--end-date", help="Tushare end date: YYYYMMDD or YYYY-MM-DD.")
    parser.add_argument("--trade-date", help="Tushare trade/survey date: YYYYMMDD or YYYY-MM-DD.")
    parser.add_argument("--report-type", choices=sorted(CNINFO_REPORT_TYPES), default="all")
    parser.add_argument("--report-year", type=int)
    parser.add_argument("--include-report-variants", action="store_true")
    parser.add_argument("--timeout", type=int, default=DEFAULT_CNINFO_TIMEOUT)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch one Tushare dataset without analysis.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search listed A-share stocks.")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--format", choices=["json", "csv"], default="json")

    fetch = subparsers.add_parser("fetch", help="Fetch one dataset for one stock.")
    fetch.add_argument("dataset", choices=sorted(_dataset_handlers().keys()))
    fetch.add_argument("query", help="Stock name, six-digit code, or ts_code.")
    fetch.add_argument("--limit", type=int, default=12)
    fetch.add_argument("--format", choices=["json", "csv"], default="json")
    fetch.add_argument("--announcement-index", type=int, default=1)
    fetch.add_argument("--download-dir")
    fetch.add_argument("--max-pages", type=int, default=120)
    fetch.add_argument("--max-chars", type=int, default=60000)
    fetch.add_argument("--to-markdown", action="store_true", help="Keep Markdown structure when pymupdf4llm is installed (report-text/announcement-text).")
    fetch.add_argument("--section", default=None, help="Extract a periodic-report chapter (mda/财务报告/重要事项/治理/股东) or keyword window instead of the first-N-pages slice.")
    fetch.add_argument("--years", type=int, default=5, help="Years of history for valuation-band.")
    fetch.add_argument("--report-index", type=int, default=1)
    _add_shared_args(fetch)

    pack = subparsers.add_parser("pack", help="Build full evidence, compact context, and module contexts for one stock.")
    pack.add_argument("query", help="Stock name, six-digit code, or ts_code.")
    pack.add_argument("--format", choices=["json"], default="json")
    pack.add_argument("--financial-limit", type=int, default=8)
    pack.add_argument("--market-limit", type=int, default=60)
    pack.add_argument("--band-years", type=int, default=5, help="Years of history for valuation-band.")
    pack.add_argument("--business-limit", type=int, default=30)
    pack.add_argument("--holder-periods", type=int, default=4)
    pack.add_argument("--holder-limit", type=int, default=30)
    pack.add_argument("--report-limit", type=int, default=8)
    pack.add_argument("--announcement-limit", type=int, default=30)
    pack.add_argument("--research-limit", type=int, default=30)
    pack.add_argument("--evidence-out")
    pack.add_argument("--context-out")
    pack.add_argument("--module-context-dir")
    pack.add_argument("--max-workers", type=int, default=4, help="Max parallel fetch workers for pack.")
    pack.add_argument("--cache-dir", default=None, help="Directory for persistent TTL cache.")
    _add_shared_args(pack)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    fetcher = StockDataFetcher(cache_dir=getattr(args, "cache_dir", None))

    if args.command == "search":
        payload = fetcher.search_stock(args.query, limit=args.limit)
        print_payload(payload, args.format)
        return 0

    if args.command == "fetch":
        if args.dataset in {"report-raw", "report-text"} and args.report_index < 1:
            raise ValueError("report-index must be >= 1.")
        if args.dataset in {"announcement-raw", "announcement-text"} and args.announcement_index < 1:
            raise ValueError("announcement-index must be >= 1.")
        if args.dataset in {"announcements", "announcement-raw", "announcement-text"} and not str(args.query or "").strip():
            raise ValueError("CNInfo announcement queries require one stock.")
        ts_code = fetcher.resolve_ts_code(args.query)
        args.query = ts_code
        handler = _dataset_handlers()[args.dataset]
        payload = handler(fetcher, args)
        print_payload(payload, args.format)
        return 0

    if args.command == "pack":
        package = build_evidence_pack(fetcher, args)
        manifest = write_pack_outputs(package, args)
        print_payload(manifest or package, args.format)
        return 0

    return 1


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
