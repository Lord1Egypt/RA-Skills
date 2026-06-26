#!/usr/bin/env python3
"""
Seedream Image Generator
使用火山引擎方舟平台 Seedream 模型生成图片

用法:
    python3 generate_image.py --prompt "一只可爱的猫咪" [options]

依赖:
    pip install volcengine-python-sdk[ark]
    # 或者使用 openai 兼容方式:
    pip install openai
"""

import argparse
import base64
import os
import sys
import time
from pathlib import Path


def generate_with_volcengine_sdk(prompt, model, size, output_path, response_format="url", n=1):
    """使用官方 volcengine SDK 调用"""
    try:
        from volcenginesdkarkruntime import Ark
    except ImportError:
        print("缺少依赖，请运行: pip install 'volcengine-python-sdk[ark]'", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("ARK_API_KEY") or os.environ.get("VOLCENGINE_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 ARK_API_KEY（方舟平台 API Key）", file=sys.stderr)
        sys.exit(1)

    client = Ark(api_key=api_key)

    kwargs = dict(
        model=model,
        prompt=prompt,
        response_format=response_format,
    )
    if size:
        kwargs["size"] = size

    print(f"正在调用 Seedream 模型: {model}")
    print(f"提示词: {prompt}")

    resp = client.images.generate(**kwargs)
    return resp


def generate_with_openai_sdk(prompt, model, size, output_path, response_format="url", n=1):
    """使用 openai 兼容方式调用"""
    try:
        from openai import OpenAI
    except ImportError:
        print("缺少依赖，请运行: pip install openai", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("ARK_API_KEY") or os.environ.get("VOLCENGINE_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 ARK_API_KEY（方舟平台 API Key）", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url="https://ark.cn-beijing.volces.com/api/v3",
    )

    kwargs = dict(
        model=model,
        prompt=prompt,
        response_format=response_format,
    )
    if size:
        kwargs["size"] = size

    print(f"正在调用 Seedream 模型 (OpenAI 兼容模式): {model}")
    print(f"提示词: {prompt}")

    resp = client.images.generate(**kwargs)
    return resp


def save_image(resp, output_path, response_format):
    """保存生成的图片"""
    saved_files = []
    for i, item in enumerate(resp.data):
        if response_format == "url":
            url = item.url
            print(f"\n图片 {i+1} URL: {url}")
            # 下载图片
            import urllib.request
            suffix = ".png"
            if output_path:
                save_to = output_path if len(resp.data) == 1 else f"{Path(output_path).stem}_{i+1}{Path(output_path).suffix}"
            else:
                timestamp = int(time.time())
                save_to = f"seedream_output_{timestamp}_{i+1}{suffix}"

            print(f"正在下载图片到: {save_to}")
            urllib.request.urlretrieve(url, save_to)
            saved_files.append(save_to)
            print(f"✅ 已保存: {save_to}")

        elif response_format == "b64_json":
            b64_data = item.b64_json
            if output_path:
                save_to = output_path if len(resp.data) == 1 else f"{Path(output_path).stem}_{i+1}{Path(output_path).suffix}"
            else:
                timestamp = int(time.time())
                save_to = f"seedream_output_{timestamp}_{i+1}.png"

            with open(save_to, "wb") as f:
                f.write(base64.b64decode(b64_data))
            saved_files.append(save_to)
            print(f"✅ 已保存: {save_to}")

    return saved_files


def main():
    parser = argparse.ArgumentParser(description="使用 Seedream 生成图片")
    parser.add_argument("--prompt", "-p", required=True, help="图片生成提示词（支持中英文）")
    parser.add_argument(
        "--model", "-m",
        default="doubao-seedream-4-0-250828",
        help="模型 ID，默认: doubao-seedream-4-0-250828"
    )
    parser.add_argument(
        "--size", "-s",
        default=None,
        help="图片尺寸，如 1024x1024、1792x1024 等（可选）"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="输出文件路径，默认自动命名"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["url", "b64_json"],
        default="url",
        help="响应格式，默认 url"
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="生成图片数量，默认 1"
    )
    parser.add_argument(
        "--sdk",
        choices=["ark", "openai"],
        default="ark",
        help="使用的 SDK，ark=官方 SDK，openai=OpenAI 兼容方式，默认 ark"
    )

    args = parser.parse_args()

    try:
        if args.sdk == "openai":
            resp = generate_with_openai_sdk(
                args.prompt, args.model, args.size,
                args.output, args.format, args.n
            )
        else:
            resp = generate_with_volcengine_sdk(
                args.prompt, args.model, args.size,
                args.output, args.format, args.n
            )

        saved = save_image(resp, args.output, args.format)
        print(f"\n生成完成，共保存 {len(saved)} 张图片")
        for f in saved:
            print(f"  📁 {os.path.abspath(f)}")

    except Exception as e:
        print(f"❌ 生成失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
