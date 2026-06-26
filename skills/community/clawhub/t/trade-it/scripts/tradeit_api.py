#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASE_URL = "https://api.tradeit.app"
TOOL_EXECUTE_PATH = "/api/tool/execute"
REDACTED_VALUE = "***REDACTED***"
SENSITIVE_KEYS = {
    "accessToken",
    "access_token",
    "refreshToken",
    "refresh_token",
    "token",
    "password",
    "secret",
    "authorization",
    "apiKey",
    "api_key",
}
SENSITIVE_KEY_LUT = {s.lower() for s in SENSITIVE_KEYS}
TRADE_QUERY_KEY_MAP = {"order_by": "orderBy"}


def fail(msg, code=1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def env_or(name, explicit=None):
    value = explicit if explicit not in (None, "") else os.environ.get(name)
    if not value:
        fail(f"Missing required value: {name}")
    return value


def request_json(method, base_url, access_token, path, body=None, query=None):
    url = base_url.rstrip("/") + path
    if query:
        qs = urllib.parse.urlencode(query, doseq=True)
        if qs:
            url += "?" + qs
    data = None
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"raw": raw}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"error": raw}
        fail(json.dumps({"status": e.code, "response": payload}, indent=2), e.code)
    except urllib.error.URLError as e:
        fail(json.dumps({"error": f"Network error: {e.reason}"}, indent=2))


def load_json_arg(raw, file_path):
    try:
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        if raw:
            return json.loads(raw)
    except json.JSONDecodeError as e:
        fail(f"Invalid JSON input: {e}")
    return {}


def redact_obj(value):
    def _redact(v):
        if isinstance(v, dict):
            out = {}
            for k, item in v.items():
                if str(k).lower() in SENSITIVE_KEY_LUT:
                    out[k] = REDACTED_VALUE
                else:
                    out[k] = _redact(item)
            return out
        if isinstance(v, list):
            return [_redact(item) for item in v]
        return v

    return _redact(value)


def build_trade_query(args):
    query = {}
    for key in ("order_by", "filter", "cursor", "refresh", "expand"):
        val = getattr(args, key)
        if val is not None:
            query[TRADE_QUERY_KEY_MAP.get(key, key)] = val
    return query


def execute_tool(base_url, access_token, tool_name, params):
    return request_json("POST", base_url, access_token, TOOL_EXECUTE_PATH, {
        "toolName": tool_name,
        "params": params,
    })


def main():
    p = argparse.ArgumentParser(description="Trade It REST API helper for OpenClaw skills")
    p.add_argument("--access-token", default=os.environ.get("TRADEIT_ACCESS_TOKEN"))
    p.add_argument("--no-redact", action="store_true", help="Print raw JSON without redacting sensitive-looking fields")

    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("get-user")

    c = sub.add_parser("get-connection")
    c.add_argument("--id", type=int, required=True)

    h = sub.add_parser("get-holdings")
    h.add_argument("--account-id", type=int, required=True)

    ga = sub.add_parser("get-accounts")

    gt = sub.add_parser("get-trades")
    gt.add_argument("--order-by")
    gt.add_argument("--filter")
    gt.add_argument("--cursor")
    gt.add_argument("--refresh")
    gt.add_argument("--expand")

    te = sub.add_parser("tool-execute")
    te.add_argument("--tool-name", required=True)
    te.add_argument("--params-json")
    te.add_argument("--params-file")

    ct = sub.add_parser("create-trade")
    ct.add_argument("--params-json")
    ct.add_argument("--params-file")

    cot = sub.add_parser("create-options-trade")
    cot.add_argument("--params-json")
    cot.add_argument("--params-file")

    et = sub.add_parser("execute-trade")
    et.add_argument("--trade-id", type=int, required=True)

    su = sub.add_parser("get-session-url")
    su.add_argument("--target", choices=["connect", "trade"], required=True)
    su.add_argument("--brokerage-id", type=int)

    args = p.parse_args()
    access_token = env_or("TRADEIT_ACCESS_TOKEN", args.access_token)

    if args.command == "get-user":
        out = request_json(
            "GET",
            API_BASE_URL,
            access_token,
            "/api/user/me",
            query={"expand": "brokerage_connections[accounts]"},
        )
    elif args.command == "get-connection":
        out = request_json("GET", API_BASE_URL, access_token, f"/api/brokerageConnection/{args.id}")
    elif args.command == "get-holdings":
        out = request_json("GET", API_BASE_URL, access_token, f"/api/account/{args.account_id}/holdings")
    elif args.command == "get-accounts":
        out = execute_tool(API_BASE_URL, access_token, "get_accounts", {})
    elif args.command == "get-trades":
        out = request_json("GET", API_BASE_URL, access_token, "/api/trade", query=build_trade_query(args))
    elif args.command == "tool-execute":
        out = execute_tool(API_BASE_URL, access_token, args.tool_name, load_json_arg(args.params_json, args.params_file))
    elif args.command == "create-trade":
        out = execute_tool(API_BASE_URL, access_token, "create_trade", load_json_arg(args.params_json, args.params_file))
    elif args.command == "create-options-trade":
        out = execute_tool(API_BASE_URL, access_token, "create_options_trade", load_json_arg(args.params_json, args.params_file))
    elif args.command == "execute-trade":
        out = execute_tool(API_BASE_URL, access_token, "execute_trade", {"trade_id": args.trade_id})
    elif args.command == "get-session-url":
        body = {"target": args.target}
        if args.brokerage_id is not None:
            body["brokerageId"] = args.brokerage_id
        out = request_json("POST", API_BASE_URL, access_token, "/api/session/url", body)
    else:
        fail(f"Unknown command: {args.command}")

    payload = out if args.no_redact else redact_obj(out)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
