#!/usr/bin/env python3
"""选品分析 — 多平台蓝海打分 — ClawHub 云端薄客户端。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from bootstrap import ensure_cloud_client_path

ensure_cloud_client_path(__file__)

from cloud_cli import print_run_meta, print_skill_output, read_text_arg
from discover import DiscoverError, discover_candidates, resolve_search_query
from yufluent_api import YufluentApiError, run_skill

SKILL_API_ID = "product-pick"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TokenApi 选品分析（云端）")
    parser.add_argument("--niche", required=True, help="选品方向 / 细分品类")
    parser.add_argument(
        "--product-candidates",
        help="多平台候选品数据（BSR/价格/评论等）或 .txt/.json 文件路径；--discover 时可省略",
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="启用 Browser 自动发现候选品（需 BROWSER_SERVICE_URL）",
    )
    parser.add_argument(
        "--discover-source",
        choices=["amazon_serp", "amazon_bs", "tiktok_trending"],
        help="发现来源：amazon_serp / amazon_bs（畅销排序搜索）/ tiktok_trending",
    )
    parser.add_argument(
        "--search-query",
        help="品类关键词（--discover 时默认使用 --niche）",
    )
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=20,
        help="--discover 时最多抓取候选品数量（1–50，默认 20）",
    )
    parser.add_argument(
        "--browser-url",
        help="Browser Service 地址（默认 BROWSER_SERVICE_URL 或 http://127.0.0.1:9222）",
    )
    parser.add_argument(
        "--platforms",
        default="amazon,tiktok,aliexpress",
        help="目标平台，逗号分隔",
    )
    parser.add_argument(
        "--data-source",
        dest="data_source",
        choices=["browser_extract", "manual", "api_snapshot"],
        default="browser_extract",
        help="数据来源类型",
    )
    parser.add_argument("--unit-cost", help="单位成本 / 到岸成本说明")
    parser.add_argument("--target-margin", help="目标毛利率，如 25%")
    parser.add_argument("--max-capital", help="最大可投入库存资金")
    parser.add_argument("--risk-constraints", help="风险约束（侵权/红海等）")
    parser.add_argument("--message", help="本轮问题或决策背景")
    parser.add_argument("--context", help="补充背景")
    parser.add_argument("--lang", default="zh")
    parser.add_argument("-o", "--output", help="写入 JSON 文件")
    return parser


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.discover:
        if not args.discover_source:
            parser.error("--discover 需要 --discover-source")
        if not resolve_search_query(args):
            parser.error("--discover 需要 --search-query 或 --niche")
        if args.max_candidates < 1 or args.max_candidates > 50:
            parser.error("--max-candidates 须在 1–50 之间")
    elif not args.product_candidates:
        parser.error("未使用 --discover 时必须提供 --product-candidates")


def resolve_product_candidates(args: argparse.Namespace) -> str:
    if args.discover:
        query = resolve_search_query(args)
        print(
            f"Discover: source={args.discover_source} query={query!r} max={args.max_candidates}",
            file=sys.stderr,
        )
        return discover_candidates(
            args.discover_source,
            query,
            max_candidates=args.max_candidates,
            browser_url=args.browser_url,
        )
    return read_text_arg(args.product_candidates or "")


def build_payload(args: argparse.Namespace, *, product_candidates: str) -> dict[str, str]:
    data_source = args.data_source
    if getattr(args, "discover", False):
        data_source = "browser_extract"

    payload: dict[str, str] = {
        "platform": "multi",
        "lang": args.lang,
        "niche": args.niche.strip(),
        "product_candidates": product_candidates,
        "platforms": args.platforms.strip(),
        "data_source": data_source,
    }
    if getattr(args, "discover", False) and getattr(args, "discover_source", None):
        payload["discover_source"] = args.discover_source
    if args.unit_cost:
        payload["unit_cost"] = args.unit_cost.strip()
    if args.target_margin:
        payload["target_margin"] = args.target_margin.strip()
    if args.max_capital:
        payload["max_capital"] = args.max_capital.strip()
    if args.risk_constraints:
        payload["risk_constraints"] = args.risk_constraints.strip()
    if args.message:
        payload["message"] = args.message.strip()
    if args.context:
        payload["context"] = args.context.strip()
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_args(parser, args)

    try:
        candidates = resolve_product_candidates(args)
        payload = build_payload(args, product_candidates=candidates)
    except DiscoverError as exc:
        print(f"Discover error: {exc}", file=sys.stderr)
        return 3

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=180.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    if args.output:
        out = data.get("formatted_text") or ""
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print_skill_output(data, prefer_formatted=True)
    print_run_meta(data, platform="multi")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
