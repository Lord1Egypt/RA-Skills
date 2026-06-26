import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib import parse, request


@dataclass
class EnvConfig:
    base_url: str


def build_env_config(env: str, base_url: Optional[str]) -> EnvConfig:
    """Resolve final base URL from env / override."""
    if base_url:
        return EnvConfig(base_url=base_url.rstrip("/"))

    if env == "test":
        return EnvConfig(base_url="https://api-qa.proto.stove.finance")

    # default: production
    return EnvConfig(base_url="https://proto.stove.finance")


def http_get_json(url: str) -> Dict[str, Any]:
    """Perform a GET request and return parsed JSON."""
    req = request.Request(url, method="GET")
    req.add_header("Content-Type", "application/json")

    try:
        with request.urlopen(req, timeout=15) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8")
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"HTTP request failed: {exc}") from exc

    if status < 200 or status >= 300:
        raise SystemExit(f"Unexpected HTTP status {status}: {body}")

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:  # noqa: BLE001
        raise SystemExit(f"Failed to parse JSON: {exc}\nBody: {body}") from exc


def cmd_stats(cfg: EnvConfig, _args: argparse.Namespace) -> None:
    url = f"{cfg.base_url}/api/v1/stats"
    data = http_get_json(url)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_ticker_stats(cfg: EnvConfig, args: argparse.Namespace) -> None:
    path = f"/api/v1/tickers/{args.symbol}/stats"
    query = parse.urlencode({"exchange": args.exchange})
    url = f"{cfg.base_url}{path}?{query}"
    data = http_get_json(url)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_ticker_heatmap(cfg: EnvConfig, args: argparse.Namespace) -> None:
    path = "/api/v1/tickers/heatmaps"
    query = parse.urlencode({"exchange": args.exchange})
    url = f"{cfg.base_url}{path}?{query}"
    data = http_get_json(url)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Stove Protocol Public API helper (stats / ticker stats / heatmap).",
    )
    parser.add_argument(
        "--env",
        choices=["prod", "test"],
        default="prod",
        help="选择环境：prod(生产，默认) 或 test(测试 api-qa)。",
    )
    parser.add_argument(
        "--base-url",
        help="可选：自定义 API 根地址，设置后优先生效。",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # stats
    p_stats = subparsers.add_parser("stats", help="查询平台统计 /api/v1/stats")
    p_stats.set_defaults(func=cmd_stats)

    # ticker-stats
    p_tstats = subparsers.add_parser(
        "ticker-stats",
        help="查询单个股票统计 /api/v1/tickers/{symbol}/stats",
    )
    p_tstats.add_argument(
        "--symbol",
        required=True,
        help="股票代码，例如 AAPL。",
    )
    p_tstats.add_argument(
        "--exchange",
        type=int,
        required=True,
        help="交易所编码（整数），详见文档中的 Exchange 枚举。",
    )
    p_tstats.set_defaults(func=cmd_ticker_stats)

    # ticker-heatmap
    p_heat = subparsers.add_parser(
        "ticker-heatmap",
        help="查询热门股票热力图 /api/v1/tickers/heatmaps",
    )
    p_heat.add_argument(
        "--exchange",
        type=int,
        required=True,
        help="交易所编码（整数），详见文档中的 Exchange 枚举。",
    )
    p_heat.set_defaults(func=cmd_ticker_heatmap)

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    cfg = build_env_config(env=args.env, base_url=args.base_url)
    args.func(cfg, args)


if __name__ == "__main__":
    main()

