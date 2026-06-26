#!/usr/bin/env python3
"""
CogView-3-Flash 生图脚本
"""
import argparse
import os
import sys
import json
from pathlib import Path
from datetime import datetime
import time

import requests


def get_api_key() -> str:
    """从环境变量或 TOOLS.md 获取 API Key"""
    # 1. 环境变量
    key = os.environ.get("ZHIPU_API_KEY")
    if key:
        return key

    # 2. 从 TOOLS.md 读取
    possible_paths = [
        Path(__file__).parent.parent.parent.parent / "TOOLS.md",
        Path.cwd() / "TOOLS.md",
        Path("~/.openclaw/workspace/TOOLS.md"),
    ]

    for path in possible_paths:
        try:
            if path.exists():
                content = path.read_text(encoding="utf-8")
                match = re.search(r'ZHIPU_API_KEY:\s*(\S+)', content)
                if match:
                    key = match.group(1)
                    if key and not key.startswith('请在这里'):
                        return key
        except Exception:
            continue
    
    return None


# 模型配置
MODELS = {
    "cogview": {
        "name": "cogview-3-flash",
        "recommended_sizes": [
            "1024x1024",
            "768x1344",
            "864x1152",
            "1344x768",
            "1152x864",
            "1440x720",
            "720x1440",
        ],
        "default_size": "1024x1024",
        "min_dim": 512,
        "max_dim": 2048,
        "multiple": 16,
        "max_pixels": 2**21,
    },
    "glm": {
        "name": "glm-image",
        "recommended_sizes": [
            "1280x1280",
            "1568x1056",
            "1056x1568",
            "1472x1088",
            "1088x1472",
            "1728x960",
            "960x1728",
        ],
        "default_size": "1280x1280",
        "min_dim": 1024,
        "max_dim": 2048,
        "multiple": 32,
        "max_pixels": 2**22,
    },
}


def parse_size(size_str: str) -> tuple[int, int]:
    """解析尺寸字符串，返回 (width, height)"""
    parts = size_str.lower().split("x")
    if len(parts) != 2:
        raise ValueError("size 格式应为 WIDTHxHEIGHT，例如 1024x1024")
    return int(parts[0]), int(parts[1])


def validate_size(size_str: str, model_key: str) -> tuple[int, int]:
    config = MODELS[model_key]
    width, height = parse_size(size_str)
    min_dim = config["min_dim"]
    max_dim = config["max_dim"]
    multiple = config["multiple"]
    max_pixels = config["max_pixels"]
    if not (min_dim <= width <= max_dim and min_dim <= height <= max_dim):
        print(
            f"❌ 尺寸超出范围: {width}x{height}, 需在 {min_dim}-{max_dim}px 之间"
        )
        sys.exit(1)
    if width % multiple != 0 or height % multiple != 0:
        print(
            f"❌ 尺寸不合法: {width}x{height}, 边长需为 {multiple} 的整数倍"
        )
        sys.exit(1)
    if width * height > max_pixels:
        print(
            f"❌ 像素数过大: {width*height}, 需不超过 {max_pixels}"
        )
        sys.exit(1)
    return width, height


def download_image(url: str, output: str) -> str:
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"image_{timestamp}.png"

    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()

    with open(output, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return os.path.abspath(output)


def generate_image(
    prompt: str,
    model_key: str = "cogview",
    size: str | None = None,
    watermark_enabled: bool = True,
    output: str | None = None,
) -> str:
    """
    生成图片
    
    Args:
        prompt: 提示词
        model_key: 模型键值，默认 cogview
        size: 尺寸
        watermark_enabled: 是否添加水印
        output: 输出路径
    """
    if model_key not in MODELS:
        model_key = "cogview"
    config = MODELS[model_key]
    if size:
        chosen_size = size
    else:
        chosen_size = config["default_size"]
    width, height = validate_size(chosen_size, model_key)
    api_key = get_api_key()
    if not api_key:
        print("❌ 错误: 未设置 ZHIPU_API_KEY 环境变量，也未在 TOOLS.md 中找到")
        print("请设置: export ZHIPU_API_KEY='your-api-key'")
        sys.exit(1)

    url = "https://open.bigmodel.cn/api/paas/v4/images/generations"

    payload = {
        "model": config["name"],
        "prompt": prompt,
        "watermark_enabled": bool(watermark_enabled),
        "size": chosen_size,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"🎨 正在调用 {config['name']} 生成图片...")
    print(f"   尺寸: {chosen_size} ({width}x{height})")
    print(f"   水印: {'开启' if watermark_enabled else '关闭'}")
    print(f"   提示词: {prompt[:60]}{'...' if len(prompt) > 60 else ''}")

    try:
        while True:
            response = requests.post(url, json=payload, headers=headers, timeout=120)
            if response.status_code == 429:
                try:
                    err = response.json()
                    code = err.get("error", {}).get("code")
                except Exception:
                    code = None
                if code == "1305":
                    print("⚠️ 模型当前访问量过大，1 秒后重试...")
                    time.sleep(1)
                    continue
            if response.status_code != 200:
                print(f"❌ HTTP 错误 {response.status_code}: {response.text}")
                sys.exit(1)
            break

        data = response.json()
        if "data" not in data or not data["data"]:
            print(f"❌ 返回结果中未找到 data 字段或为空: {json.dumps(data, ensure_ascii=False)}")
            sys.exit(1)

        first = data["data"][0]
        image_url = first.get("url")
        if not image_url:
            print(f"❌ 返回结果中未找到图片 url: {json.dumps(data, ensure_ascii=False)}")
            sys.exit(1)

        print("⬇️  正在下载图片...")
        saved_path = download_image(image_url, output)
        print(f"✅ 图片已保存: {saved_path}")
        return saved_path

    except Exception as e:
        print(f"❌ 调用接口或下载图片时出错: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="使用 cogview-3-flash 模型生成图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate.py "两只可爱的小猫咪，坐在阳光明媚的窗台上，背景是蓝天白云。" --size 1024x1024
  python generate.py "赛博朋克城市夜景，霓虹灯与雨夜" --no-watermark -o cyberpunk.png
        """,
    )

    parser.add_argument("prompt", help="图片生成提示词（支持中文）")
    parser.add_argument(
        "--model",
        default="cogview",
        choices=["cogview", "glm"],
        help="模型选择: cogview 对应 cogview-3-flash, glm 对应 glm-image",
    )
    parser.add_argument(
        "--size",
        help="图片尺寸，如 1024x1024。留空则使用所选模型的默认尺寸",
    )
    parser.add_argument(
        "--watermark",
        action="store_true",
        help="开启水印（默认开启，如果同时传 --no-watermark 则以 no 为准）",
    )
    parser.add_argument(
        "--no-watermark",
        action="store_true",
        help="关闭水印",
    )
    parser.add_argument("--output", "-o", help="输出文件路径")

    args = parser.parse_args()

    if args.no_watermark:
        watermark_enabled = False
    elif args.watermark:
        watermark_enabled = True
    else:
        watermark_enabled = True

    generate_image(
        prompt=args.prompt,
        model_key=args.model,
        size=args.size,
        watermark_enabled=watermark_enabled,
        output=args.output,
    )


if __name__ == "__main__":
    main()
