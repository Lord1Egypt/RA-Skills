#!/usr/bin/env python3
"""
Vehicle limit skill for OpenClaw.
基于极速数据车辆尾号限行 API：
https://www.jisuapi.com/api/vehiclelimit/
"""

import sys
import json
import os
import requests


VEHICLE_CITY_URL = "https://api.jisuapi.com/vehiclelimit/city"
VEHICLE_QUERY_URL = "https://api.jisuapi.com/vehiclelimit/query"


def get_vehicle_cities(appkey: str):
    """
    调用 /vehiclelimit/city 接口，获取支持限行查询的城市列表。
    返回 result 数组，每项包含:
    { "city": "hangzhou", "cityname": "杭州" }
    """
    params = {"appkey": appkey}

    try:
        resp = requests.get(VEHICLE_CITY_URL, params=params, timeout=10)
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


def query_vehicle_limit(appkey: str, req: dict):
    """
    调用 /vehiclelimit/query 接口，查询指定城市在某一天的尾号限行信息。

    请求 JSON 示例：
    {
        "city": "hangzhou",
        "date": "2015-12-02"
    }
    """
    city = req.get("city")
    date = req.get("date")
    if not city:
        return {"error": "missing_param", "message": "city is required"}
    if not date:
        return {"error": "missing_param", "message": "date is required"}

    params = {
        "appkey": appkey,
        "city": city,
        "date": date,
    }

    try:
        resp = requests.get(VEHICLE_QUERY_URL, params=params, timeout=10)
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


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  vehiclelimit.py cities                              # 获取支持限行查询的城市列表\n"
            "  vehiclelimit.py '{\"city\":\"hangzhou\",\"date\":\"2015-12-02\"}'  # 查询指定城市限行信息",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")

    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    # 子命令：城市列表
    if sys.argv[1].lower() in ("city", "cities", "citylist"):
        result = get_vehicle_cities(appkey)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 默认：限行查询，参数为 JSON
    raw = sys.argv[1]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if "city" not in req or "date" not in req:
        print("Error: 'city' and 'date' are required in request JSON.", file=sys.stderr)
        sys.exit(1)

    result = query_vehicle_limit(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

