#!/usr/bin/env python3
"""
Extract weekly cafeteria menu from an image using OpenRouter VLM.

Usage:
    python extract_menu.py <image_path>

Environment:
    MENU_OPENROUTER_API_KEY  OpenRouter API key (required)
"""

import base64
import json
import os
import sys
import urllib.error
import urllib.request

MODEL = "qwen/qwen-vl-plus"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
PROMPT = (
    "这是一张食堂一周菜单图，请识别并按以下结构输出：\n"
    "1. 本周日期范围\n"
    "2. 每天（周一至周五，或包含周末）的：\n"
    "   - 早餐菜品列表\n"
    "   - 午餐菜品列表\n"
    "   - 小吃（午餐区域中单独成行、用"+"分隔的内容，"
    "例如"牛肉拉面+云南过桥米线"，属于小吃摊位，请单独列出）\n"
    "请输出结构化 Markdown，便于 agent 直接参考使用。"
)


def extract_menu(image_path: str) -> dict:
    api_key = os.environ.get("MENU_OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("MENU_OPENROUTER_API_KEY environment variable is not set")

    ext = os.path.splitext(image_path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"

    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{img_b64}"},
                    },
                    {"type": "text", "text": PROMPT},
                ],
            }
        ],
        "max_tokens": 3000,
    }

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())

    usage = result.get("usage", {})
    return {
        "menu": result["choices"][0]["message"]["content"],
        "model": result.get("model", MODEL),
        "tokens": usage.get("total_tokens", 0),
        "cost_usd": usage.get("cost", 0.0),
    }


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python extract_menu.py <image_path>", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"Error: file not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    try:
        result = extract_menu(image_path)
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"API error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

    print(result["menu"])
    print(
        f"\n---\nModel: {result['model']} | Tokens: {result['tokens']} | Cost: ${result['cost_usd']:.6f}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
