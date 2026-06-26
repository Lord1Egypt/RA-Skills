#!/usr/bin/env python3
"""
VIN skill for OpenClaw.
基于极速数据 VIN 车辆识别代码查询 API：
https://www.jisuapi.com/api/vin/
"""

import sys
import json
import os
import requests


VIN_QUERY_URL = "https://api.jisuapi.com/vin/query"
VIN_OIL_URL = "https://api.jisuapi.com/vin/oil"
VIN_GEARBOX_URL = "https://api.jisuapi.com/vin/gearbox"


def query_vin(appkey: str, req: dict):
    """
    调用 /vin/query 接口，按 17 位 VIN 车架号查询车辆信息。

    请求 JSON 示例：
    {
        "vin": "LSVAL41Z882104202",
        "strict": 0     # 可选，是否严格校验 VIN，0 否，1 是，默认 0
    }
    """
    params = {"appkey": appkey}

    vin = req.get("vin")
    if vin:
        params["vin"] = vin
    strict = req.get("strict")
    if strict is not None:
        params["strict"] = strict

    try:
        resp = requests.get(VIN_QUERY_URL, params=params, timeout=10)
    except Exception as e:
        return {
            "error": "request_failed",
            "message": str(e),
        }

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "status_code": resp.status_code,
            "body": resp.text,
        }

    try:
        data = resp.json()
    except Exception:
        return {
            "error": "invalid_json",
            "body": resp.text,
        }

    if data.get("status") != 0:
        return {
            "error": "api_error",
            "code": data.get("status"),
            "message": data.get("msg"),
        }

    return data.get("result", {})


def query_vin_oil(appkey: str, carid: int):
    """
    调用 /vin/oil 接口，按车型 ID 查询机油信息。
    carid 来自 VIN 查询结果中的 carlist.carid 或车型大全。
    """
    params = {
        "appkey": appkey,
        "carid": carid,
    }

    try:
        resp = requests.get(VIN_OIL_URL, params=params, timeout=10)
    except Exception as e:
        return {
            "error": "request_failed",
            "message": str(e),
        }

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "status_code": resp.status_code,
            "body": resp.text,
        }

    try:
        data = resp.json()
    except Exception:
        return {
            "error": "invalid_json",
            "body": resp.text,
        }

    if data.get("status") != 0:
        return {
            "error": "api_error",
            "code": data.get("status"),
            "message": data.get("msg"),
        }

    return data.get("result", {})


def query_vin_gearbox(appkey: str, carid: int):
    """
    调用 /vin/gearbox 接口，按车型 ID 查询变速箱信息。
    """
    params = {
        "appkey": appkey,
        "carid": carid,
    }

    try:
        resp = requests.get(VIN_GEARBOX_URL, params=params, timeout=10)
    except Exception as e:
        return {
            "error": "request_failed",
            "message": str(e),
        }

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "status_code": resp.status_code,
            "body": resp.text,
        }

    try:
        data = resp.json()
    except Exception:
        return {
            "error": "invalid_json",
            "body": resp.text,
        }

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
            "  vin.py '{\"vin\":\"LSVAL41Z882104202\"}'      # 按 VIN 查询车辆信息\n"
            "  vin.py oil 2641                               # 按 carid 查询机油信息\n"
            "  vin.py gearbox 21617                          # 按 carid 查询变速箱信息",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")

    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    # 子命令: 机油信息
    cmd = sys.argv[1].lower()
    if cmd in ("oil", "gearbox"):
        if len(sys.argv) < 3:
            print("Error: carid is required for oil/gearbox subcommand.", file=sys.stderr)
            sys.exit(1)
        try:
            carid = int(sys.argv[2])
        except ValueError:
            print("Error: carid must be an integer.", file=sys.stderr)
            sys.exit(1)

        if cmd == "oil":
            result = query_vin_oil(appkey, carid)
        else:
            result = query_vin_gearbox(appkey, carid)

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 默认：VIN 查询，参数为 JSON
    raw = sys.argv[1]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if "vin" not in req or not req["vin"]:
        print("Error: 'vin' is required in request JSON.", file=sys.stderr)
        sys.exit(1)

    result = query_vin(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

