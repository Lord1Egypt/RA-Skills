import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib import parse, request


@dataclass
class EnvConfig:
    base_url: str
    jwt_token: str


def build_env_config(env: str, base_url: Optional[str], jwt_token: str) -> EnvConfig:
    """Resolve final base URL from env / override."""
    if not jwt_token:
        raise SystemExit("jwt_token is required for Maker API calls.")

    if base_url:
        return EnvConfig(base_url=base_url.rstrip("/"), jwt_token=jwt_token)

    if env == "test":
        return EnvConfig(base_url="https://api-qa.proto.stove.finance", jwt_token=jwt_token)

    # default: production
    return EnvConfig(base_url="https://proto.stove.finance", jwt_token=jwt_token)


def _build_request(url: str, method: str, cfg: EnvConfig, body: Optional[Dict[str, Any]] = None) -> request.Request:
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    else:
        data = None

    req = request.Request(url, method=method, data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {cfg.jwt_token}")
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
    path = "/api/v1/orders"
    params: Dict[str, Any] = {}
    if args.ticker:
        params["ticker"] = args.ticker
    if args.status:
        params["status"] = args.status
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
    path = f"/api/v1/orders/{args.order_hash}"
    url = f"{cfg.base_url}{path}"
    req = _build_request(url, "GET", cfg)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_positions(cfg: EnvConfig, args: argparse.Namespace) -> None:  # noqa: ARG001
    url = f"{cfg.base_url}/api/v1/positions"
    req = _build_request(url, "GET", cfg)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_nonce(cfg: EnvConfig, args: argparse.Namespace) -> None:  # noqa: ARG001
    url = f"{cfg.base_url}/api/v1/orders/nonce"
    req = _build_request(url, "GET", cfg)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_estimate_fee(cfg: EnvConfig, args: argparse.Namespace) -> None:
    url = f"{cfg.base_url}/api/v1/orders/estimate-fee"
    body = json.loads(args.body)
    req = _build_request(url, "POST", cfg, body=body)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_create_order(cfg: EnvConfig, args: argparse.Namespace) -> None:
    url = f"{cfg.base_url}/api/v1/orders"
    body = json.loads(args.body)
    req = _build_request(url, "POST", cfg, body=body)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_cancel_order(cfg: EnvConfig, args: argparse.Namespace) -> None:
    # 具体取消路径以官方文档为准，这里假设为 DELETE /api/v1/orders/{order_hash}
    path = f"/api/v1/orders/{args.order_hash}"
    url = f"{cfg.base_url}{path}"
    req = _build_request(url, "DELETE", cfg)
    data = http_call(req)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Stove Protocol Maker API helper (orders / positions / nonce / fee).",
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
        "--jwt-token",
        required=True,
        help="Maker API JWT Token，将作为 Authorization: Bearer {jwt} 使用。",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # orders list
    p_orders = subparsers.add_parser("orders", help="查询订单列表 /api/v1/orders")
    p_orders.add_argument("--ticker", help="股票代码，可选。")
    p_orders.add_argument(
        "--status",
        help="订单状态，支持多个状态以逗号分隔，例如 pending,filled。",
    )
    p_orders.add_argument("--page", type=int, help="页码（默认 1）。")
    p_orders.add_argument("--page-size", type=int, help="每页条数，最大 100。")
    p_orders.set_defaults(func=cmd_orders_list)

    # order get
    p_order_get = subparsers.add_parser(
        "order",
        help="查询单个订单详情 /api/v1/orders/{order_hash}",
    )
    p_order_get.add_argument(
        "--order-hash",
        required=True,
        help="订单哈希。",
    )
    p_order_get.set_defaults(func=cmd_order_get)

    # positions
    p_pos = subparsers.add_parser(
        "positions",
        help="查询 Maker 持仓 /api/v1/positions",
    )
    p_pos.set_defaults(func=cmd_positions)

    # nonce
    p_nonce = subparsers.add_parser(
        "nonce",
        help="查询下一个可用订单 nonce /api/v1/orders/nonce",
    )
    p_nonce.set_defaults(func=cmd_nonce)

    # estimate-fee
    p_fee = subparsers.add_parser(
        "estimate-fee",
        help="估算订单手续费 /api/v1/orders/estimate-fee（POST，请通过 --body 传入 JSON 字符串）。",
    )
    p_fee.add_argument(
        "--body",
        required=True,
        help="JSON 字符串，请符合文档中的请求体结构。",
    )
    p_fee.set_defaults(func=cmd_estimate_fee)

    # create order
    p_create = subparsers.add_parser(
        "create-order",
        help="创建订单 /api/v1/orders（POST，请通过 --body 传入 JSON 字符串）。",
    )
    p_create.add_argument(
        "--body",
        required=True,
        help="JSON 字符串，请符合文档中的请求体结构。",
    )
    p_create.set_defaults(func=cmd_create_order)

    # cancel order
    p_cancel = subparsers.add_parser(
        "cancel-order",
        help="取消订单（DELETE /api/v1/orders/{order_hash}，具体以文档为准）。",
    )
    p_cancel.add_argument(
        "--order-hash",
        required=True,
        help="要取消的订单哈希。",
    )
    p_cancel.set_defaults(func=cmd_cancel_order)

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    cfg = build_env_config(env=args.env, base_url=args.base_url, jwt_token=args.jwt_token)
    args.func(cfg, args)


if __name__ == "__main__":
    main()

