#!/usr/bin/env python3
"""
TV program schedule skill for OpenClaw.
基于极速数据电视节目预告 API：
https://www.jisuapi.com/api/tv/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/tv"


def _call_tv_api(path: str, appkey: str, params: dict = None):
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

    return data.get("result", {})


def query(appkey: str, req: dict):
    """
    电视节目查询 /tv/query

    请求 JSON 示例：
    {
        "tvid": 435,
        "date": "2015-10-19"
    }
    """
    tvid = req.get("tvid")
    date = req.get("date")

    missing = []
    if tvid in (None, ""):
        missing.append("tvid")
    if not date:
        missing.append("date")
    if missing:
        return {
            "error": "missing_param",
            "message": f"Missing required fields: {', '.join(missing)}",
        }

    params = {
        "tvid": tvid,
        "date": date,
    }
    return _call_tv_api("query", appkey, params)


def channel(appkey: str):
    """
    电视节目频道列表 /tv/channel
    """
    return _call_tv_api("channel", appkey, {})


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  tv.py channel                                   # 获取频道列表\n"
            "  tv.py query '{\"tvid\":435,\"date\":\"2015-10-19\"}'  # 查询某频道某日节目单",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "channel":
        result = channel(appkey)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if cmd != "query":
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Error: JSON body is required for 'query'.", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[2]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    result = query(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

