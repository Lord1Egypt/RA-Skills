#!/usr/bin/env python3
"""
历史天气 skill for OpenClaw.
基于极速数据历史天气 API：
https://www.jisuapi.com/api/weather2/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/weather2"


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


def cmd_query(appkey: str, req: dict):
    """
    历史天气查询 /weather2/query

    请求 JSON 示例：
    {"city": "安顺", "date": "2018-01-01"}
    或 {"cityid": 111, "date": "2018-01-01"}
    """
    date_val = req.get("date")
    if not date_val:
        return {"error": "missing_param", "message": "date is required (format: 2018-01-01)"}

    params = {"appkey": appkey, "date": date_val}
    if req.get("city") is not None:
        params["city"] = req["city"]
    if req.get("cityid") is not None:
        params["cityid"] = req["cityid"]

    return _call_api("query", appkey, params)


def cmd_city(appkey: str, _req: dict):
    """获取历史天气支持的城市列表 /weather2/city，无参数。"""
    return _call_api("city", appkey, {})


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  weather2.py query '{\"city\":\"北京\",\"date\":\"2018-01-01\"}'  # 历史天气\n"
            "  weather2.py city '{}'   # 支持城市列表",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].strip().lower()
    req = {}
    if len(sys.argv) >= 3 and sys.argv[2].strip():
        try:
            req = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(req, dict):
            req = {}

    if cmd == "query":
        result = cmd_query(appkey, req)
    elif cmd == "city":
        result = cmd_city(appkey, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    if isinstance(result, dict) and result.get("error"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
