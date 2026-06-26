#!/usr/bin/env python3
"""
付费状态检查脚本
调用 key_balance API 查询付费状态和剩余免费次数。

用法：
    python scripts/check_payment.py [--apikey KEY]

环境变量：
    TEMPLATE_API_KEY — API 密钥（未传 --apikey 时使用）
"""

import argparse
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError

API_BASE = "http://124.221.10.61/api/v1"


def get_api_key() -> str:
    parser = argparse.ArgumentParser(description="检查付费状态")
    parser.add_argument("--apikey", help="API 密钥")
    args = parser.parse_args()
    return args.apikey or os.environ.get("TEMPLATE_API_KEY", "")


def check_payment(api_key: str) -> dict:
    url = f"{API_BASE}/key/balance"
    req = Request(url)
    if api_key:
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("X-API-Key", api_key)

    try:
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except URLError as e:
        return {"ok": False, "error": str(e)}


def main():
    api_key = get_api_key()
    result = check_payment(api_key)

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get("ok"):
        print("\n[!]  查询失败，请检查网络连接和 API 密钥。")
        sys.exit(1)

    data = result.get("data", result)
    paid = data.get("paid", False)
    free_remaining = data.get("free_uses_remaining", 0)

    print("\n--- 摘要 ---")
    print(f"付费状态: {'[OK] 已付费' if paid else '[NO] 未付费'}")
    print(f"剩余免费次数: {free_remaining}")
    if paid:
        print("所有功能不限次数使用。")
    elif free_remaining > 0:
        print(f"还有 {free_remaining} 次免费使用机会。")
    else:
        print("免费额度已用完，请提醒用户付费。")


if __name__ == "__main__":
    main()
