#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///
"""SmartOCR — 车辆证件与票据识别 CLI

从图片中提取结构化信息，支持行驶证正页/副页、收据/发票。
自动判断图片类型并返回对应字段的 JSON 数据。

环境变量:
  SMARTOCR_API_KEY  — API Key（sk- 前缀）
  SMARTOCR_API_URL  — API 地址（默认 http://localhost:5001）
"""

import argparse
import base64
import json
import os
import sys

import requests

DEFAULT_API_URL = "https://smartocr.yunlizhi.cn"


def ocr(image: str, api_url: str, api_key: str, timeout: int = 60) -> dict:
    """调用 SmartOCR API 识别图片。

    Args:
        image: 图片 URL 或 Base64 编码字符串
        api_url: API 基础地址
        api_key: API Key
        timeout: 请求超时秒数

    Returns:
        包含 ocr_type 和 content 的字典
    """
    resp = requests.post(
        f"{api_url.rstrip('/')}/api/ocr",
        headers={"X-API-Key": api_key},
        json={"image": image},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(
        description="SmartOCR — 车辆证件与票据识别",
        epilog="支持行驶证正页/副页、收据/发票，自动判断类型。",
    )
    parser.add_argument("image", help="图片 URL 或本地文件路径")
    parser.add_argument(
        "-t", "--timeout", type=int, default=60, help="请求超时秒数 (默认: 60)"
    )
    parser.add_argument(
        "--raw", action="store_true", help="输出原始 JSON（不格式化）"
    )
    args = parser.parse_args()

    api_key = os.environ.get("SMARTOCR_API_KEY", "")
    api_url = os.environ.get("SMARTOCR_API_URL", DEFAULT_API_URL)

    if not api_key:
        print(
            "错误: 未设置 SMARTOCR_API_KEY 环境变量\n"
            '请运行: openclaw config set env.vars.SMARTOCR_API_KEY "sk-your-api-key"',
            file=sys.stderr,
        )
        sys.exit(1)

    # 判断是 URL 还是本地文件
    image_input = args.image
    if not image_input.startswith(("http://", "https://", "data:")):
        path = os.path.expanduser(image_input)
        if not os.path.isfile(path):
            print(f"错误: 文件不存在: {path}", file=sys.stderr)
            sys.exit(1)
        with open(path, "rb") as f:
            image_input = base64.b64encode(f.read()).decode()

    try:
        result = ocr(image_input, api_url, api_key, timeout=args.timeout)
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code
        try:
            msg = e.response.json().get("error", str(e))
        except (ValueError, AttributeError):
            msg = getattr(e.response, "text", str(e))
        print(f"HTTP {code}: {msg}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("错误: 请求超时，请稍后重试", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"错误: 无法连接到 {api_url}", file=sys.stderr)
        sys.exit(1)

    if args.raw:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
