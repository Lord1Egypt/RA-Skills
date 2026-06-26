#!/usr/bin/env python3
"""Search research reports from fxbaogao for the report-search skill."""

from __future__ import annotations

import argparse
import json
import sys

from fxbaogao_client import (
    FxbaogaoError,
    RELATIVE_TIME_VALUES,
    format_search_output,
    parse_date_to_timestamp,
    search_reports,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="搜索研究报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
时间范围:
    --time last3day   最近 3 天
    --time last7day   最近 1 周
    --time last1mon   最近 1 个月
    --time last3mon   最近 3 个月
    --time last1year  最近 1 年

示例:
    python3 search_reports.py "人工智能" --time last1mon --json
    python3 search_reports.py "新能源" --org "中信证券" --author "张三"
    python3 search_reports.py "锂电池" --start-date 2025-01-01 --end-date 2025-03-31
        """,
    )

    parser.add_argument("keywords", nargs="?", help="搜索关键词")
    parser.add_argument(
        "--author",
        "-a",
        action="append",
        dest="authors",
        help="作者姓名，可重复指定",
    )
    parser.add_argument(
        "--org",
        "-o",
        action="append",
        dest="org_names",
        help="机构名称，可重复指定",
    )
    parser.add_argument(
        "--time",
        "-t",
        choices=sorted(RELATIVE_TIME_VALUES),
        help="相对时间范围",
    )
    parser.add_argument("--start-date", help="开始日期，格式 YYYY-MM-DD")
    parser.add_argument("--end-date", help="结束日期，格式 YYYY-MM-DD")
    parser.add_argument("--start-ts", type=int, help="开始时间戳（毫秒）")
    parser.add_argument("--end-ts", type=int, help="结束时间戳（毫秒）")
    parser.add_argument(
        "--size",
        "-s",
        type=int,
        default=10,
        help="返回数量（默认 10，最大 100）",
    )
    parser.add_argument("--json", "-j", action="store_true", help="输出规范化 JSON")
    return parser


def resolve_time_args(args: argparse.Namespace) -> tuple[int | None, int | str | None]:
    has_explicit_range = any(
        [
            args.start_date,
            args.end_date,
            args.start_ts is not None,
            args.end_ts is not None,
        ]
    )
    if args.time and has_explicit_range:
        raise ValueError("--time 不能与显式时间范围参数同时使用")

    if args.time:
        return None, args.time

    start_time = args.start_ts
    end_time = args.end_ts

    if args.start_date:
        start_time = parse_date_to_timestamp(args.start_date)
    if args.end_date:
        end_time = parse_date_to_timestamp(args.end_date, end_of_day=True)

    if (
        start_time is not None
        and isinstance(end_time, int)
        and start_time > end_time
    ):
        raise ValueError("开始时间不能晚于结束时间")

    return start_time, end_time


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.keywords and not args.authors and not args.org_names:
        parser.error("请至少指定一个搜索条件（关键词、作者或机构）")

    try:
        start_time, end_time = resolve_time_args(args)
        result = search_reports(
            keywords=args.keywords,
            authors=args.authors,
            org_names=args.org_names,
            start_time=start_time,
            end_time=end_time,
            page_size=args.size,
        )
    except (ValueError, FxbaogaoError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(format_search_output(result))


if __name__ == "__main__":
    main()
