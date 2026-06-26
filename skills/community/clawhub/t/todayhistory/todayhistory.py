#!/usr/bin/env python3
"""
Today in history skill for OpenClaw.
基于极速数据历史上的今天 API：
https://www.jisuapi.com/api/todayhistory/
"""

import sys
import json
import os
import requests


TODAY_HISTORY_URL = "https://api.jisuapi.com/todayhistory/query"


def query_todayhistory(appkey: str, req: dict):
    """
    历史上的今天查询 /todayhistory/query

    请求 JSON 示例：
    {
        "month": 1,
        "day": 2
    }
    """
    month = req.get("month")
    day = req.get("day")

    if month is None or day is None:
        return {"error": "missing_param", "message": "month and day are required"}

    params = {
        "appkey": appkey,
        "month": month,
        "day": day,
    }

    try:
        resp = requests.get(TODAY_HISTORY_URL, params=params, timeout=10)
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

    return data.get("result", [])


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\\n"
            "  todayhistory.py query '{\"month\":1,\"day\":2}'   # 查询 1 月 2 日的历史事件",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd != "query":
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Error: JSON body is required.", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[2]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(req, dict):
        print("Error: JSON body must be an object.", file=sys.stderr)
        sys.exit(1)

    result = query_todayhistory(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

