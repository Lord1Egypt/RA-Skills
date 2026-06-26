#!/usr/bin/env python3
"""
Stock index skill for OpenClaw.
基于极速数据上证股票指数 API：
https://www.jisuapi.com/api/stockindex/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/stockindex"


def _call_api(path: str, appkey: str, params: dict = None):
    if params is None:
        params = {}
    all_params = {"appkey": appkey}
    all_params.update({k: v for k, v in params.items() if v not in (None, "")})

    url = f"{BASE_URL}/{path}"

    try:
        resp = requests.get(url, params=all_params, timeout=10)
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

    return data.get("result")


def sh(appkey: str):
    """
    股票指数 /stockindex/sh
    上证指数、深证成指、创业板指、中小板指、沪深300、上证50、科创50、B股指数等，
    返回最新价、昨收盘价、数据量、更新时间及分钟级趋势（trend / trend_standard）。
    无需请求参数。
    """
    return _call_api("sh", appkey, {})


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  stockindex.py sh    # 获取上证/深证/创业板等指数行情（分钟粒度）",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "sh":
        result = sh(appkey)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
