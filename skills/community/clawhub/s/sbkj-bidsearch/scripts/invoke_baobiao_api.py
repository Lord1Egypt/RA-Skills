#!/usr/bin/env python3
"""安全调用保标招标外部 POST 接口。

脚本只使用 Python 标准库，API Key 从 BAOBIAO_ZTB_API_KEY 读取。
示例：
  python invoke_baobiao_api.py --endpoint searchProjectApi --data-file request.json
  echo '{"companyName":"湖北会计师事务所"}' | python invoke_baobiao_api.py --endpoint companyProfileSummary
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any


BASE_URL = "https://gate.gov-bid.com/outer-gateway/bid"


def parse_args() -> argparse.Namespace:
    """解析命令行参数，支持 JSON 字符串、文件或标准输入作为请求体。"""
    parser = argparse.ArgumentParser(description="调用保标招标外部 POST 接口")
    parser.add_argument("--endpoint", required=True, help="接口名称或以 / 开头的接口路径")
    parser.add_argument("--data", help="请求 JSON 字符串")
    parser.add_argument("--data-file", help="请求 JSON 文件路径；未指定数据时读取标准输入")
    parser.add_argument("--base-url", default=BASE_URL, help="接口基地址，默认使用保标招标网关")
    parser.add_argument("--key-env", default="BAOBIAO_ZTB_API_KEY", help="API Key 环境变量名")
    parser.add_argument("--timeout", type=float, default=30, help="请求超时时间，单位秒")
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    """读取并校验请求 JSON，拒绝数组、字符串等非对象请求体。"""
    if args.data and args.data_file:
        raise ValueError("--data 与 --data-file 不能同时使用")

    if args.data:
        raw = args.data
    elif args.data_file:
        with open(args.data_file, "r", encoding="utf-8") as file:
            raw = file.read()
    else:
        raw = sys.stdin.read()

    if not raw.strip():
        return {}

    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("请求 JSON 必须是对象")
    return payload


def build_url(base_url: str, endpoint: str, api_key: str) -> str:
    """拼接接口地址并追加 Key；不在异常信息中暴露完整 URL。"""
    path = endpoint.strip()
    if not path.startswith("/"):
        path = "/" + path
    return f"{base_url.rstrip('/')}{path}?key={api_key}"


def call_api(url: str, payload: dict[str, Any], timeout: float) -> Any:
    """发送 JSON POST 请求并解析 JSON 响应。"""
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"HTTP 请求失败：{exc.code}，响应摘要：{detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"网络请求失败：{exc.reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("接口未返回合法 JSON") from exc


def main() -> int:
    """执行接口调用，校验业务响应并输出 JSON。"""
    args = parse_args()
    api_key = os.environ.get(args.key_env, "").strip()
    if not api_key:
        print(f"未配置 API Key，请设置环境变量 {args.key_env}", file=sys.stderr)
        return 2

    try:
        payload = load_payload(args)
        result = call_api(build_url(args.base_url, args.endpoint, api_key), payload, args.timeout)
    except (OSError, ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if isinstance(result, dict):
        code = result.get("code")
        sub_code = result.get("subCode")
        if code not in (None, 200) or sub_code not in (None, "0000000000"):
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
