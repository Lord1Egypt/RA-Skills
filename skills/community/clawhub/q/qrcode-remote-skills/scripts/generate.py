"""
QR Code Generator - 生成二维码并保存到本地。

用法:
  python scripts/generate.py --data <文本内容> --output <保存路径> [选项]

选项:
  --size              图片尺寸，默认 400x400
  --format            输出格式 png|svg，默认 png
  --error-correction  纠错级别 L|M|Q|H，默认 M
  --border            边框宽度，默认 2

输出 JSON:
  {"url": "...", "file": "..."}
  错误时: {"error": "..."}
"""

import sys
import json
import os
import argparse
from urllib.parse import quote, urlencode
import urllib.request

API_BASE = "https://api.2dcode.biz/v1/create-qr-code"


def build_url(data: str, size: str, fmt: str, ecc: str, border: int) -> str:
    params = {"data": data, "size": size}
    if fmt != "png":
        params["format"] = fmt
    if ecc != "M":
        params["error_correction"] = ecc
    if border != 2:
        params["border"] = str(border)
    return f"{API_BASE}?{urlencode(params, quote_via=quote)}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="二维码文本内容")
    parser.add_argument("--output", required=True, help="本地保存路径")
    parser.add_argument("--size", default="400x400")
    parser.add_argument("--format", default="png", dest="fmt", choices=["png", "svg"])
    parser.add_argument("--error-correction", default="M", dest="ecc", choices=["L", "M", "Q", "H"])
    parser.add_argument("--border", type=int, default=2)
    args = parser.parse_args()

    url = build_url(args.data, args.size, args.fmt, args.ecc, args.border)
    output_path = os.path.abspath(args.output)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    try:
        urllib.request.urlretrieve(url, output_path)
    except Exception as e:
        print(json.dumps({"error": f"下载失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps({"url": url, "file": output_path}, ensure_ascii=False))


if __name__ == "__main__":
    main()
