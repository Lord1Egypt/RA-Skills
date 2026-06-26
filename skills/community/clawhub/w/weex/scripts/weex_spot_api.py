#!/usr/bin/env python3
"""WEEX Spot REST API helper.

- Endpoint definitions loaded from references/spot-api-definitions.json
- Private auth from environment variables only
- Supports generic endpoint calls and deterministic order placement
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import error, parse, request

DEFAULT_BASE_URL = "https://api-spot.weex.com"
DEFAULT_LOCALE = "en-US"
DEFAULT_TIMEOUT = 15.0


@dataclass(frozen=True)
class Endpoint:
    key: str
    category: str
    title: str
    method: str
    path: str
    requires_auth: bool
    doc_url: str


def load_endpoint_map() -> Dict[str, Endpoint]:
    refs = Path(__file__).resolve().parent.parent / "references" / "spot-api-definitions.json"
    obj = json.loads(refs.read_text(encoding="utf-8"))
    endpoint_map: Dict[str, Endpoint] = {}
    for d in obj.get("definitions", []):
        ep = Endpoint(
            key=d["key"],
            category=d.get("category", ""),
            title=d.get("title", ""),
            method=d.get("method", "GET").upper(),
            path=d.get("path", ""),
            requires_auth=bool(d.get("requires_auth", False)),
            doc_url=d.get("doc_url", ""),
        )
        endpoint_map[ep.key] = ep
    return endpoint_map


ENDPOINTS = load_endpoint_map()


def find_endpoint_key_by_doc_suffix(doc_suffix: str) -> str:
    target = f"/{doc_suffix}"
    for endpoint in ENDPOINTS.values():
        if endpoint.doc_url.endswith(target):
            return endpoint.key
    raise SystemExit(f"Unable to find endpoint with doc suffix {doc_suffix}")


def parse_json_arg(raw: str, arg_name: str) -> Dict[str, Any]:
    raw = raw.strip()
    if not raw:
        return {}
    if raw.startswith("@"):
        raise SystemExit(
            f"{arg_name} no longer accepts @file input. Pass a JSON object string directly."
        )
    payload = raw
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON for {arg_name}: {exc}") from exc
    if parsed is None:
        return {}
    if not isinstance(parsed, dict):
        raise SystemExit(f"{arg_name} must be a JSON object")
    return parsed


def compact_json(value: Optional[Dict[str, Any]]) -> str:
    if not value:
        return ""
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


class WeexSpotClient:
    def __init__(
        self,
        base_url: str,
        timeout: float,
        locale: str,
        api_key: Optional[str],
        api_secret: Optional[str],
        api_passphrase: Optional[str],
        user_agent: str = "weex-trader-skill-spot/1.0",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.locale = locale
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.user_agent = user_agent

    def _require_auth(self) -> None:
        missing = []
        if not self.api_key:
            missing.append("WEEX_API_KEY")
        if not self.api_secret:
            missing.append("WEEX_API_SECRET")
        if not self.api_passphrase:
            missing.append("WEEX_API_PASSPHRASE")
        if missing:
            raise SystemExit(
                "Missing private API credentials in environment. "
                "Set these vars and retry: " + ", ".join(missing)
            )

    def _sign(self, timestamp_ms: str, method: str, path: str, query_string: str, body_str: str) -> str:
        message = f"{timestamp_ms}{method}{path}"
        if query_string:
            message += f"?{query_string}"
        message += body_str
        digest = hmac.new(
            self.api_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        return base64.b64encode(digest).decode("utf-8")

    def prepare_request(
        self,
        endpoint: Endpoint,
        query: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        method = endpoint.method.upper()
        q = query or {}
        b = body or {}
        query_string = parse.urlencode(q, doseq=True)
        body_str = compact_json(b)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "locale": self.locale,
            "User-Agent": self.user_agent,
        }

        if endpoint.requires_auth:
            self._require_auth()
            ts = str(int(time.time() * 1000))
            sign = self._sign(ts, method, endpoint.path, query_string, body_str)
            headers.update(
                {
                    "ACCESS-KEY": self.api_key,
                    "ACCESS-PASSPHRASE": self.api_passphrase,
                    "ACCESS-TIMESTAMP": ts,
                    "ACCESS-SIGN": sign,
                }
            )

        url = f"{self.base_url}{endpoint.path}"
        if query_string:
            url = f"{url}?{query_string}"

        data = body_str.encode("utf-8") if body_str and method != "GET" else None
        return {
            "method": method,
            "url": url,
            "headers": headers,
            "data": data,
            "query": q,
            "body": b,
        }

    def send(self, prepared: Dict[str, Any]) -> Dict[str, Any]:
        req = request.Request(
            url=prepared["url"],
            method=prepared["method"],
            data=prepared["data"],
            headers=prepared["headers"],
        )
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError:
                    payload = {"raw": raw}
                return {"ok": True, "status": resp.status, "data": payload}
        except error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = {"raw": raw}
            return {"ok": False, "status": exc.code, "error": payload}
        except error.URLError as exc:
            return {"ok": False, "status": None, "error": {"message": str(exc)}}


def sanitize_headers(headers: Dict[str, str]) -> Dict[str, str]:
    result = dict(headers)
    for k in ["ACCESS-KEY", "ACCESS-PASSPHRASE", "ACCESS-SIGN"]:
        if k in result:
            result[k] = "***"
    return result


def output_json(payload: Dict[str, Any], pretty: bool) -> None:
    if pretty:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False))
    else:
        print(json.dumps(payload, ensure_ascii=False))


def is_mutating(endpoint: Endpoint) -> bool:
    return endpoint.method in {"POST", "PUT", "DELETE"} and endpoint.requires_auth


def execute_endpoint(
    client: WeexSpotClient,
    endpoint_key: str,
    query: Dict[str, Any],
    body: Dict[str, Any],
    dry_run: bool,
    confirm_live: bool,
    pretty: bool,
) -> int:
    endpoint = ENDPOINTS[endpoint_key]

    if is_mutating(endpoint) and not confirm_live and not dry_run:
        raise SystemExit(
            f"Refusing live mutating request for {endpoint_key}. "
            "Use --confirm-live to send, or --dry-run to preview."
        )

    prepared = client.prepare_request(endpoint, query=query, body=body)

    if dry_run:
        preview = {
            "dry_run": True,
            "endpoint": endpoint.key,
            "method": prepared["method"],
            "url": prepared["url"],
            "headers": sanitize_headers(prepared["headers"]),
            "query": query,
            "body": body,
        }
        output_json(preview, pretty)
        return 0

    resp = client.send(prepared)
    payload = {
        "endpoint": endpoint.key,
        "method": endpoint.method,
        "path": endpoint.path,
        "status": resp.get("status"),
        "ok": resp.get("ok"),
        "result": resp.get("data") if resp.get("ok") else resp.get("error"),
    }
    output_json(payload, pretty)
    return 0 if resp.get("ok") else 1


def normalize_spot_symbol(symbol: str) -> str:
    s = symbol.strip().upper().replace("-", "").replace("/", "").replace(" ", "")
    if s.endswith("USDT") and len(s) > 4:
        return s
    raise SystemExit(f"Unsupported symbol format: {symbol}. Expected like ETHUSDT.")


def generate_client_order_id() -> str:
    return f"codex-{int(time.time() * 1000)}-{secrets.token_hex(3)}"


def cmd_list_endpoints(args: argparse.Namespace) -> int:
    rows = []
    for ep in sorted(ENDPOINTS.values(), key=lambda e: (e.category, e.key)):
        if args.category and ep.category != args.category:
            continue
        rows.append(
            {
                "key": ep.key,
                "category": ep.category,
                "method": ep.method,
                "path": ep.path,
                "requires_auth": ep.requires_auth,
                "doc_url": ep.doc_url,
            }
        )
    output_json({"count": len(rows), "endpoints": rows}, args.pretty)
    return 0


def cmd_call(args: argparse.Namespace, client: WeexSpotClient) -> int:
    return execute_endpoint(
        client=client,
        endpoint_key=args.endpoint,
        query=parse_json_arg(args.query, "--query"),
        body=parse_json_arg(args.body, "--body"),
        dry_run=args.dry_run,
        confirm_live=args.confirm_live,
        pretty=args.pretty,
    )


def cmd_ticker(args: argparse.Namespace, client: WeexSpotClient) -> int:
    return execute_endpoint(
        client=client,
        endpoint_key=find_endpoint_key_by_doc_suffix("GetTickerInfo"),
        query={"symbol": normalize_spot_symbol(args.symbol)},
        body={},
        dry_run=False,
        confirm_live=False,
        pretty=args.pretty,
    )


def cmd_place_order(args: argparse.Namespace, client: WeexSpotClient) -> int:
    body: Dict[str, Any] = {
        "symbol": normalize_spot_symbol(args.symbol),
        "side": args.side.upper(),
        "type": args.order_type.upper(),
        "quantity": args.quantity,
        "newClientOrderId": args.new_client_order_id or generate_client_order_id(),
    }
    if args.price is not None:
        body["price"] = args.price
    if args.time_in_force is not None:
        body["timeInForce"] = args.time_in_force.upper()
    if body["type"] == "LIMIT":
        if "price" not in body:
            raise SystemExit("price is required when type=LIMIT")
        if "timeInForce" not in body:
            raise SystemExit("time-in-force is required when type=LIMIT")
    else:
        if "price" in body:
            raise SystemExit("price must be omitted when type=MARKET")
        if "timeInForce" in body:
            raise SystemExit("time-in-force must be omitted when type=MARKET")

    return execute_endpoint(
        client=client,
        endpoint_key=find_endpoint_key_by_doc_suffix("PlaceOrder"),
        query={},
        body=body,
        dry_run=args.dry_run,
        confirm_live=args.confirm_live,
        pretty=args.pretty,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WEEX Spot REST API helper")
    parser.add_argument("--base-url", default=os.getenv("WEEX_SPOT_API_BASE", DEFAULT_BASE_URL))
    parser.add_argument("--locale", default=os.getenv("WEEX_LOCALE", DEFAULT_LOCALE))
    parser.add_argument("--timeout", type=float, default=float(os.getenv("WEEX_API_TIMEOUT", DEFAULT_TIMEOUT)))
    categories = sorted({endpoint.category for endpoint in ENDPOINTS.values() if endpoint.category})

    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list-endpoints", help="List supported spot REST endpoints")
    p_list.add_argument("--category", choices=categories, default=None)
    p_list.add_argument("--pretty", action="store_true")

    p_call = sub.add_parser("call", help="Call a spot endpoint by key with JSON query/body")
    p_call.add_argument("--endpoint", required=True, choices=sorted(ENDPOINTS.keys()))
    p_call.add_argument("--query", default="{}", help="JSON object string")
    p_call.add_argument("--body", default="{}", help="JSON object string")
    p_call.add_argument("--dry-run", action="store_true")
    p_call.add_argument("--confirm-live", action="store_true")
    p_call.add_argument("--pretty", action="store_true")

    p_ticker = sub.add_parser("ticker", help="Get spot ticker for one symbol")
    p_ticker.add_argument("--symbol", required=True)
    p_ticker.add_argument("--pretty", action="store_true")

    p_place = sub.add_parser("place-order", help="Convenience wrapper for the live spot PlaceOrder doc")
    p_place.add_argument("--symbol", required=True)
    p_place.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"])
    p_place.add_argument("--order-type", required=True, choices=["LIMIT", "MARKET", "limit", "market"])
    p_place.add_argument("--quantity", required=True)
    p_place.add_argument("--price", default=None)
    p_place.add_argument("--time-in-force", default=None, choices=["GTC", "IOC", "FOK", "gtc", "ioc", "fok"])
    p_place.add_argument("--new-client-order-id", default=None)
    p_place.add_argument("--dry-run", action="store_true")
    p_place.add_argument("--confirm-live", action="store_true")
    p_place.add_argument("--pretty", action="store_true")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    client = WeexSpotClient(
        base_url=args.base_url,
        timeout=args.timeout,
        locale=args.locale,
        api_key=os.getenv("WEEX_API_KEY"),
        api_secret=os.getenv("WEEX_API_SECRET"),
        api_passphrase=os.getenv("WEEX_API_PASSPHRASE"),
    )

    if args.command == "list-endpoints":
        return cmd_list_endpoints(args)
    if args.command == "call":
        return cmd_call(args, client)
    if args.command == "ticker":
        return cmd_ticker(args, client)
    if args.command == "place-order":
        return cmd_place_order(args, client)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
