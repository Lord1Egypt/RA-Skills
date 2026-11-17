#!/usr/bin/env python3
"""Trip.com 携程国际版 — 出境游助手

支持3种模式：hotel（海外酒店）、flight（国际机票）、attraction（境外景点门票）。
通过 TripGenie API 返回实时数据，含 Trip.com 联盟预订链接。

用法: python trip_com.py <mode> <query>

模式:
  hotel      <查询>   — 搜索海外酒店，如"东京新宿附近酒店"
  flight     <查询>   — 查询国际机票，如"上海到东京机票"
  attraction <查询>   — 搜索境外景点门票，如"大阪环球影城门票"
"""

import sys
import json
import urllib.request
import urllib.error

PROXY_URL = "https://1439498936-eu423jdjnd.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"


def query_tripgenie(query: str, command_type: str = "query") -> dict:
    """Query TripGenie API through SCF proxy."""
    payload = {"query": query, "locale": "zh", "command_type": command_type}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-Proxy-Token": PROXY_TOKEN,
            "User-Agent": "TripCom-CN/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if isinstance(result, dict) and "data" in result:
                return {"success": True, "response": result["data"]}
            elif isinstance(result, str):
                return {"success": True, "response": result}
            else:
                return {"success": True, "response": str(result)}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}"}
    except Exception as e:
        return {"success": False, "error": f"请求失败: {str(e)}"}


def main():
    if len(sys.argv) < 3:
        print("用法: python trip_com.py <hotel|flight|attraction> <查询内容>")
        print("示例: python trip_com.py hotel 东京新宿附近性价比高的酒店")
        sys.exit(1)

    mode = sys.argv[1].lower()
    query = " ".join(sys.argv[2:])

    # 根据模式构造更精确的查询
    if mode == "hotel":
        full_query = f"搜索海外酒店：{query}。请返回酒店名称、特色、每晚价格、评分和Trip.com预订链接。"
    elif mode == "flight":
        full_query = f"查询国际机票：{query}。请返回航班号、起降时间、价格和预订链接。"
    elif mode == "attraction":
        full_query = f"搜索境外景点门票：{query}。请返回景点介绍、门票价格和购买链接。"
    else:
        print(f"不支持的模式: {mode}")
        print("支持: hotel, flight, attraction")
        sys.exit(1)

    result = query_tripgenie(full_query, command_type=mode)

    if result.get("success"):
        print(result["response"])
    else:
        print(f"查询失败: {result.get('error', '未知错误')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
