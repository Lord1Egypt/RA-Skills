#!/usr/bin/env python3
"""NeoData 金融数据查询客户端（通过代理 API）

Usage:
    python query.py --query "腾讯最新财报" --token "<JWT>"
    python query.py --query "贵州茅台股价" --data-type api --token "<JWT>"
    python query.py --query "黄金价格" --token "<JWT>"

鉴权优先级: --token 参数 > NEODATA_TOKEN 环境变量

环境变量 (可选):
    NEODATA_TOKEN    - JWT token (当未使用 --token 参数时的备选)
    NEODATA_ENDPOINT - 代理 URL (可选，默认 https://copilot.tencent.com/agenttool/v1/neodata)
"""

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("需要安装 requests: pip install requests", file=sys.stderr)
    sys.exit(1)

DEFAULT_ENDPOINT = "https://copilot.tencent.com/agenttool/v1/neodata"


def query_neodata(
    query: str,
    data_type: str = "all",
    token: str | None = None,
    endpoint: str | None = None,
) -> dict:
    url = endpoint or os.getenv("NEODATA_ENDPOINT", DEFAULT_ENDPOINT)
    jwt_token = token or os.getenv("NEODATA_TOKEN")
    if not jwt_token:
        print("错误: 未提供 token。请使用 --token 参数或设置 NEODATA_TOKEN 环境变量", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}",
    }

    payload: dict = {
        "query": query,
        "channel": "neodata",
        "sub_channel": "workbuddy",
    }
    if data_type != "all":
        payload["data_type"] = data_type

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="NeoData 金融数据查询")
    parser.add_argument("--query", "-q", required=True, help="自然语言查询")
    parser.add_argument("--token", "-t", default=None, help="JWT token (优先级高于 NEODATA_TOKEN 环境变量)")
    parser.add_argument("--data-type", "-d", default="all", choices=["all", "api", "doc"], help="数据类型 (默认: all)")
    args = parser.parse_args()

    try:
        result = query_neodata(
            query=args.query,
            data_type=args.data_type,
            token=args.token,
        )
    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
