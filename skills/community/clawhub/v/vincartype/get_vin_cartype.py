#!/usr/bin/env python3
"""
VIN skill for OpenClaw.
积智数据 VIN 车型解析
"""

import sys
import json
import os
import requests
import re


VIN_CARTYPE_URL = "https://erp.qipeidao.com/jzOpenClaw/getVinCarType"

def query_vin_cartype(appkey: str, vin: str):
    """
    调用 /getVinCarType 接口，按 17 位 VIN 车架号查询车辆信息。

    请求 JSON 示例：
    {
        "vin": "LSVAL41Z882104202"
    }
    """
    if not is_valid_vin(vin):
        return {
            "error": "invalid_vin",
            "msg": "VIN must be 17 characters long and contain only letters and numbers.",
        }
    params = {"apiKey": appkey, "vinCode": vin}
    try:
        resp = requests.post(VIN_CARTYPE_URL, json=params, timeout=100)
    except Exception as e:
        return {
            "error": "request_failed",
            "msg": str(e),
        }

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "state": resp.status_code,
            "msg": resp.text,
        }

    data = json.loads(resp.text)
#     try:
#         data = resp.text.json()
#     except Exception:
#         return {
#             "error": "invalid_json",
#             "body": resp.text,
#         }
    return data;
def is_valid_vin(vin):
    return len(vin) == 17 and re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin)

def main():
    if len(sys.argv) < 1:
        print(
            "Usage:\n"
            "  vin.py 'LSVAL41Z882104202'      # 按 VIN 查询车辆信息\n",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JZ_API_KEY")

    if not appkey:
        print("Error: JZ_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)


    # 默认：VIN 查询，参数为 JSON
    vin = sys.argv[1]
    if not vin:
        print("Error: 'vin' is required.", file=sys.stderr)
        sys.exit(1)

    result = query_vin_cartype(appkey,vin)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

