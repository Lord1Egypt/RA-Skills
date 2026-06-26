#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///
"""SmartOCR Session Image Extractor

从当前 openclaw 会话的 session jsonl 文件中提取最近的图片，
直接调用 SmartOCR API 进行识别。

用法:
  uv run python {baseDir}/scripts/smartocr_from_session.py [options]

环境变量:
  SMARTOCR_API_KEY  — API Key（sk- 前缀）
  SMARTOCR_API_URL  — API 地址（默认 https://smartocr.yunlizhi.cn）
  OPENCLAW_HOME     — openclaw 安装目录（默认 ~/.openclaw）
"""

import argparse
import glob
import json
import os
import sys

import requests

DEFAULT_API_URL = "https://smartocr.yunlizhi.cn"


def find_openclaw_home():
    """查找 openclaw 安装目录。"""
    home = os.environ.get("OPENCLAW_HOME")
    if home and os.path.isdir(home):
        return home
    default = os.path.expanduser("~/.openclaw")
    if os.path.isdir(default):
        return default
    return None


def find_latest_session(openclaw_home, agent_id="main"):
    """找到指定 agent 最新的 session jsonl 文件。"""
    sessions_dir = os.path.join(openclaw_home, "agents", agent_id, "sessions")
    if not os.path.isdir(sessions_dir):
        return None
    files = glob.glob(os.path.join(sessions_dir, "*.jsonl"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def extract_images_from_session(session_file, count=1):
    """从 session jsonl 中提取最近 N 张图片的 base64 数据。

    从文件末尾向前扫描，找到包含 type=image 的 user 消息。

    Returns:
        list of base64 字符串（按时间从旧到新排列）
    """
    images = []
    with open(session_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in reversed(lines):
        if len(images) >= count:
            break
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        msg = entry.get("message", {})
        if msg.get("role") != "user":
            continue
        content = msg.get("content", [])
        if isinstance(content, str):
            continue
        for item in reversed(content):
            if len(images) >= count:
                break
            if isinstance(item, dict) and item.get("type") == "image":
                data = item.get("data", "")
                if data:
                    images.append(data)

    images.reverse()
    return images


def ocr(image_data, api_url, api_key, timeout=60):
    """调用 SmartOCR API。"""
    resp = requests.post(
        f"{api_url.rstrip('/')}/api/ocr",
        headers={"X-API-Key": api_key},
        json={"image": image_data},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(
        description="从当前 openclaw 会话中提取最近的图片并调用 SmartOCR 识别",
    )
    parser.add_argument(
        "-n", "--count", type=int, default=1,
        help="提取最近 N 张图片（默认: 1）",
    )
    parser.add_argument(
        "--agent", default="main",
        help="agent ID（默认: main）",
    )
    parser.add_argument(
        "--session", default=None,
        help="指定 session jsonl 文件路径（默认: 自动查找最新）",
    )
    parser.add_argument(
        "-t", "--timeout", type=int, default=60,
        help="请求超时秒数（默认: 60）",
    )
    parser.add_argument(
        "--raw", action="store_true",
        help="输出原始 JSON（不格式化）",
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

    session_file = args.session
    if not session_file:
        home = find_openclaw_home()
        if not home:
            print("错误: 找不到 openclaw 安装目录", file=sys.stderr)
            sys.exit(1)
        session_file = find_latest_session(home, args.agent)
        if not session_file:
            print(f"错误: 找不到 agent '{args.agent}' 的 session 文件", file=sys.stderr)
            sys.exit(1)

    images = extract_images_from_session(session_file, count=args.count)
    if not images:
        print("错误: 当前会话中没有找到图片", file=sys.stderr)
        sys.exit(1)

    results = []
    for i, img_data in enumerate(images):
        try:
            result = ocr(img_data, api_url, api_key, timeout=args.timeout)
            result["_image_index"] = i + 1
            results.append(result)
        except requests.exceptions.HTTPError as e:
            code = e.response.status_code
            try:
                msg = e.response.json().get("error", str(e))
            except (ValueError, AttributeError):
                msg = getattr(e.response, "text", str(e))
            results.append({"_image_index": i + 1, "error": f"HTTP {code}: {msg}"})
        except requests.exceptions.Timeout:
            results.append({"_image_index": i + 1, "error": "请求超时"})
        except requests.exceptions.ConnectionError:
            results.append({"_image_index": i + 1, "error": f"无法连接到 {api_url}"})

    output = results[0] if len(results) == 1 else results
    if args.raw:
        print(json.dumps(output, ensure_ascii=False))
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
