#!/usr/bin/env python3
"""
Silver price skill for OpenClaw.
基于极速数据白银价格 API：
https://www.jisuapi.com/api/silver/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/silver"


def _call_silver_api(path: str, appkey: str, params: dict = None):
    if params is None:
        params = {}
    all_params = {"appkey": appkey}
    all_params.update({k: v for k, v in params.items() if v not in (None, "")})
    url = f"{BASE_URL}/{path}"

    try:
        resp = requests.get(url, params=params, timeout=10)
    except Exception as e:
        return {"error": "request_failed", "message": str(e)}

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "status_code": resp.status_code,
            "body": resp.text,
        }

    try:
        data = resp.json()
    except Exception:
        return {"error": "invalid_json", "body": resp.text}

    if data.get("status") != 0:
        return {
            "error": "api_error",
            "code": data.get("status"),
            "message": data.get("msg"),
        }

    return data.get("result", {})


def shgold(appkey: str):
    """上海黄金交易所白银价格 /silver/shgold"""
    return _call_silver_api("shgold", appkey)


def shfutures(appkey: str):
    """上海期货交易所白银价格 /silver/shfutures"""
    return _call_silver_api("shfutures", appkey)


def london_silver(appkey: str):
    """伦敦银价格 /silver/london"""
    return _call_silver_api("london", appkey)


def silver_history(appkey: str, req: dict):
    """
    白银历史行情 /silver/history

    请求 JSON 示例：
    {
        "market": "london",
        "startdate": "2026-06-01",
        "enddate": "2026-06-10",
        "type": "xag"
    }
    """
    for field in ("market", "startdate", "enddate", "type"):
        if not req.get(field):
            return {"error": "missing_param", "message": f"{field} is required"}
    params = {
        "market": req["market"],
        "startdate": req["startdate"],
        "enddate": req["enddate"],
        "type": req["type"],
    }
    return _call_silver_api("history", appkey, params)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  silver.py shgold        # 上海黄金交易所白银价格\n"
            "  silver.py shfutures     # 上海期货交易所白银价格\n"
            "  silver.py london        # 伦敦银价格\n"
            "  silver.py history '{\"market\":\"london\",\"startdate\":\"2026-06-01\",\"enddate\":\"2026-06-10\",\"type\":\"xag\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")

    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "shgold":
        result = shgold(appkey)
    elif cmd == "shfutures":
        result = shfutures(appkey)
    elif cmd == "london":
        result = london_silver(appkey)
    elif cmd == "history":
        if len(sys.argv) < 3:
            print("Error: JSON request body is required for 'history'.", file=sys.stderr)
            sys.exit(1)
        try:
            req = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        result = silver_history(appkey, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

