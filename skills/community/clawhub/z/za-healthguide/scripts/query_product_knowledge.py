#!/usr/bin/env python3
"""
众民保产品知识查询脚本
用法：python3 query_product_knowledge.py --msg "投保年龄" --product "众民保·中高端"
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

API_URL = "https://ihealth.zhongan.com/api/support/api/outer/v1/product/knowledge/recall"
API_KEY = "bfa9daba4a904448b23320596ce23c15"


def query(msg: str, product_name: str) -> dict:
    payload = json.dumps({
        "msg": msg,
        "apiKey": API_KEY,
        "productName": product_name
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"网络错误: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="众民保产品知识查询")
    parser.add_argument("--msg", required=True, help="查询问题，例如：投保年龄")
    parser.add_argument("--product", required=True, help="产品名称，例如：众民保·中高端")
    args = parser.parse_args()

    result = query(args.msg, args.product)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
