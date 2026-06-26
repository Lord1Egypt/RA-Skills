import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib import parse, request


@dataclass
class EnvConfig:
    base_url: str
    api_key: str


def build_env_config(env: str, base_url: Optional[str], api_key: str) -> EnvConfig:
    """Resolve final base URL from env / override."""
    if not api_key:
        raise SystemExit("api_key is required for Taker API calls.")

    if base_url:
        return EnvConfig(base_url=base_url.rstrip("/"), api_key=api_key)

    if env == "test":
        return EnvConfig(base_url="https://api-qa.proto.stove.finance", api_key=api_key)

    # default: production
    return EnvConfig(base_url="https://proto.stove.finance", api_key=api_key)


def _build_request(
    url: str,
    method: str,
    cfg: EnvConfig,
    body: Optional[Dict[str, Any]] = None,
) -> request.Request:
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    else:
        data = None

    req = request.Request(url, method=method, data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("X-API-Key", cfg.api_key)
    return req


def http_call(req: request.Request) -> Dict[str, Any]:
    """Perform HTTP request and return parsed JSON."""
    try:
        with request.urlopen(req, timeout=20) as resp:
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


def cmd_orders_list(cfg: EnvConfig, args: argparse.Namespace) -> None:
    path = "/api/v1/takers/orders"
    params: Dict[str, Any] = {}
    if args.status:
        params["status"] = args.status
    if args.ticker:
        params["ticker"] = args.ticker
    if args.exchange is not None:
        params["exchange"] = args.exchange
    if args.page:
        params["page"] = args.page
    if args.page_size:
        params["page_size"] = args.page_size

    query = parse.urlencode(params)
    url = f"{cfg.base_url}{path}"
    if query:
        url = f"{url}?{query}"

    req = _build_request(url, "GET", cfg)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_order_get(cfg: EnvConfig, args: argparse.Namespace) -> None:
    path = f"/api/v1/takers/orders/{args.order_hash}"
    url = f"{cfg.base_url}{path}"
    req = _build_request(url, "GET", cfg)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_fills_list(cfg: EnvConfig, args: argparse.Namespace) -> None:
    path = "/api/v1/takers/fills"
    params: Dict[str, Any] = {}
    if args.ticker:
        params["ticker"] = args.ticker
    if args.exchange is not None:
        params["exchange"] = args.exchange
    if args.page:
        params["page"] = args.page
    if args.page_size:
        params["page_size"] = args.page_size

    query = parse.urlencode(params)
    url = f"{cfg.base_url}{path}"
    if query:
        url = f"{url}?{query}"

    req = _build_request(url, "GET", cfg)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_validate(cfg: EnvConfig, args: argparse.Namespace) -> None:
    url = f"{cfg.base_url}/api/v1/takers/orders/validate"
    body = json.loads(args.body)
    req = _build_request(url, "POST", cfg, body=body)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_lock(cfg: EnvConfig, args: argparse.Namespace) -> None:
    url = f"{cfg.base_url}/api/v1/takers/orders/lock"
    body = json.loads(args.body)
    req = _build_request(url, "POST", cfg, body=body)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_unlock(cfg: EnvConfig, args: argparse.Namespace) -> None:
    url = f"{cfg.base_url}/api/v1/takers/orders/unlock"
    body = json.loads(args.body)
    req = _build_request(url, "POST", cfg, body=body)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_fill(cfg: EnvConfig, args: argparse.Namespace) -> None:
    url = f"{cfg.base_url}/api/v1/takers/orders/fill"
    body = json.loads(args.body)
    req = _build_request(url, "POST", cfg, body=body)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_reject(cfg: EnvConfig, args: argparse.Namespace) -> None:
    url = f"{cfg.base_url}/api/v1/takers/orders/reject"
    body = json.loads(args.body)
    req = _build_request(url, "POST", cfg, body=body)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Stove Protocol Taker API helper (validate / lock / fill / query).",
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
    parser.add_argument(
        "--api-key",
        required=True,
        help="Taker API Key，将作为 X-API-Key 头使用。",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # orders list
    p_orders = subparsers.add_parser(
        "orders",
        help="查询 Taker 订单列表 /api/v1/takers/orders",
    )
    p_orders.add_argument(
        "--status",
        help="订单状态，多个状态以逗号分隔，例如 locked,filled。",
    )
    p_orders.add_argument("--ticker", help="股票代码，可选。")
    p_orders.add_argument("--exchange", type=int, help="交易所编码，可选。")
    p_orders.add_argument("--page", type=int, help="页码（默认 1）。")
    p_orders.add_argument("--page-size", type=int, help="每页条数，最大 100。")
    p_orders.set_defaults(func=cmd_orders_list)

    # single order
    p_order = subparsers.add_parser(
        "order",
        help="查询单个 Taker 订单详情 /api/v1/takers/orders/{order_hash}",
    )
    p_order.add_argument(
        "--order-hash",
        required=True,
        help="订单哈希。",
    )
    p_order.set_defaults(func=cmd_order_get)

    # fills list
    p_fills = subparsers.add_parser(
        "fills",
        help="查询成交记录列表 /api/v1/takers/fills",
    )
    p_fills.add_argument("--ticker", help="股票代码，可选。")
    p_fills.add_argument("--exchange", type=int, help="交易所编码，可选。")
    p_fills.add_argument("--page", type=int, help="页码（默认 1）。")
    p_fills.add_argument("--page-size", type=int, help="每页条数，最大 100。")
    p_fills.set_defaults(func=cmd_fills_list)

    # validate
    p_validate = subparsers.add_parser(
        "validate",
        help="校验订单 /api/v1/takers/orders/validate（POST，请通过 --body 传入 JSON 字符串）。",
    )
    p_validate.add_argument(
        "--body",
        required=True,
        help="JSON 字符串，请符合文档中的请求体结构。",
    )
    p_validate.set_defaults(func=cmd_validate)

    # lock
    p_lock = subparsers.add_parser(
        "lock",
        help="锁定订单 /api/v1/takers/orders/lock（POST，请通过 --body 传入 JSON 字符串）。",
    )
    p_lock.add_argument(
        "--body",
        required=True,
        help="JSON 字符串，请符合文档中的请求体结构。",
    )
    p_lock.set_defaults(func=cmd_lock)

    # unlock
    p_unlock = subparsers.add_parser(
        "unlock",
        help="解锁订单 /api/v1/takers/orders/unlock（POST，请通过 --body 传入 JSON 字符串）。",
    )
    p_unlock.add_argument(
        "--body",
        required=True,
        help="JSON 字符串，请符合文档中的请求体结构。",
    )
    p_unlock.set_defaults(func=cmd_unlock)

    # fill
    p_fill = subparsers.add_parser(
        "fill",
        help="成交订单 /api/v1/takers/orders/fill（POST，请通过 --body 传入 JSON 字符串）。",
    )
    p_fill.add_argument(
        "--body",
        required=True,
        help="JSON 字符串，请符合文档中的请求体结构。",
    )
    p_fill.set_defaults(func=cmd_fill)

    # reject
    p_reject = subparsers.add_parser(
        "reject",
        help="拒绝订单 /api/v1/takers/orders/reject（POST，请通过 --body 传入 JSON 字符串）。",
    )
    p_reject.add_argument(
        "--body",
        required=True,
        help="JSON 字符串，请符合文档中的请求体结构。",
    )
    p_reject.set_defaults(func=cmd_reject)

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    cfg = build_env_config(env=args.env, base_url=args.base_url, api_key=args.api_key)
    args.func(cfg, args)


if __name__ == "__main__":
    main()

