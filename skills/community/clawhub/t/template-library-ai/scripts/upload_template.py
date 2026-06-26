#!/usr/bin/env python3
"""
自有模板上传脚本
调用 user_upload_template API 上传模板文件并分析结构。

用法：
    python scripts/upload_template.py <文件路径> [--apikey KEY]

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
    parser = argparse.ArgumentParser(description="上传自有模板")
    parser.add_argument("filepath", help="模板文件路径（.docx / .doc）")
    parser.add_argument("--apikey", help="API 密钥")
    args = parser.parse_args()
    api_key = args.apikey or os.environ.get("TEMPLATE_API_KEY", "")
    return args.filepath, api_key


def upload_template(filepath: str, api_key: str) -> dict:
    """使用 multipart/form-data 上传文件。"""
    if not os.path.isfile(filepath):
        return {"ok": False, "error": f"文件不存在: {filepath}"}

    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        file_data = f.read()

    boundary = b"----FormBoundary7MA4YWxkTrZu0gW"
    body = b""
    body += b"--" + boundary + b"\r\n"
    body += f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode()
    body += b"Content-Type: application/octet-stream\r\n\r\n"
    body += file_data + b"\r\n"
    body += b"--" + boundary + b"--\r\n"

    url = f"{API_BASE}/user/upload"
    req = Request(url, data=body)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary.decode()}")
    if api_key:
        req.add_header("Authorization", f"Bearer {api_key}")

    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except URLError as e:
        return {"ok": False, "error": str(e)}


def show_structure(analysis: dict, indent: int = 0):
    """递归展示模板结构树。"""
    prefix = "  " * indent
    node_type = analysis.get("type", "unknown")
    label = analysis.get("label", "")
    hint = analysis.get("hint", "")

    if node_type == "chapter":
        print(f"{prefix}[o] {label or '章节'}")
    elif node_type == "text":
        print(f"{prefix}[*] {label}" + (f"  ({hint})" if hint else ""))
    elif node_type == "reference":
        print(f"{prefix}[o] {label}" + (f"  ({hint})" if hint else ""))
    else:
        print(f"{prefix}[?] {label or node_type}")

    for child in analysis.get("children", []):
        show_structure(child, indent + 1)


def main():
    filepath, api_key = get_api_key()
    print(f"正在上传: {filepath}...")
    result = upload_template(filepath, api_key)

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get("ok"):
        print(f"\n[!]  上传失败。")
        sys.exit(1)

    data = result.get("data", {})
    print(f"\n--- 上传成功 ---")
    print(f"会话 ID: {data.get('session_id')}（10 分钟过期）")
    print(f"文件名: {data.get('original_name')}")
    print(f"大小: {data.get('file_size')} bytes")
    print(f"格式: {data.get('format')}")
    print(f"\n--- 文档结构分析 ---")
    analysis = data.get("analysis", {})
    if analysis.get("structure"):
        show_structure(analysis["structure"])
    else:
        print("（无结构分析结果）")


if __name__ == "__main__":
    main()
