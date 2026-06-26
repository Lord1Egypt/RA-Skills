#!/usr/bin/env python3
"""
MiniMax 文生图工具
- 自动保存图片到本地
- 支持批量生成
- 返回本地文件路径
用法: python generate_image.py "你的图片描述" [--model image-01] [--style 漫画] [--ratio 1:1] [--n 1]
"""

import argparse
import os
import requests
import sys
import time


def generate_image(
    prompt: str,
    model: str = "image-01",
    style_type: str = None,
    style_weight: float = 0.8,
    aspect_ratio: str = "1:1",
    n: int = 1,
    response_format: str = "url",
    api_key: str = None,
):
    """调用 MiniMax 文生图 API"""

    api_key = api_key or os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

    url = "https://api.minimaxi.com/v1/image_generation"

    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": response_format,
        "n": min(n, 9),  # 最多9张
    }

    # 仅 image-01-live 支持 style
    if model == "image-01-live" and style_type:
        payload["style"] = {
            "style_type": style_type,
            "style_weight": style_weight,
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"正在生成 {n} 张图片...")
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    result = response.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        error_msg = result.get("base_resp", {}).get("status_msg", "未知错误")
        raise Exception(f"API 错误: {error_msg}")

    return result


def download_and_save(image_urls, save_dir, prefix="text2img"):
    """下载并保存图片，返回本地路径列表"""
    os.makedirs(save_dir, exist_ok=True)
    saved_paths = []
    timestamp = int(time.time())

    for i, url in enumerate(image_urls):
        filename = f"{prefix}_{timestamp}_{i+1}.jpeg"
        filepath = os.path.join(save_dir, filename)

        print(f"  下载第 {i+1}/{len(image_urls)} 张...")
        img_response = requests.get(url, timeout=30)
        with open(filepath, 'wb') as f:
            f.write(img_response.content)

        saved_paths.append(filepath)
        print(f"    ✅ 已保存: {filepath}")

    return saved_paths


def main():
    parser = argparse.ArgumentParser(description="MiniMax 文生图工具")
    parser.add_argument("prompt", help="图片描述文本")
    parser.add_argument("--model", default="image-01", choices=["image-01", "image-01-live"])
    parser.add_argument("--style", dest="style_type", help="画风类型 (仅 image-01-live)")
    parser.add_argument("--weight", type=float, default=0.8, dest="style_weight")
    parser.add_argument("--ratio", default="1:1", dest="aspect_ratio")
    parser.add_argument("--n", type=int, default=1, help="生成数量 [1-9]")
    parser.add_argument("--api-key", dest="api_key")
    parser.add_argument("--save-dir", dest="save_dir",
                        default="~/.openclaw/workspace/assets/images",
                        help="保存目录")

    args = parser.parse_args()

    try:
        result = generate_image(
            prompt=args.prompt,
            model=args.model,
            style_type=args.style_type,
            style_weight=args.style_weight,
            aspect_ratio=args.aspect_ratio,
            n=args.n,
            api_key=args.api_key,
        )

        print("\n✅ 生成成功!")
        print(f"成功: {result['metadata']['success_count']} 张")
        print(f"失败: {result['metadata']['failed_count']} 张")

        image_urls = result.get("data", {}).get("image_urls", [])
        save_dir = os.path.expanduser(args.save_dir)

        print(f"\n正在保存到: {save_dir}")
        saved_paths = download_and_save(image_urls, save_dir, prefix="text2img")

        print(f"\n📁 所有图片已保存到: {save_dir}")
        print("\n生成的文件:")
        for path in saved_paths:
            print(f"  - {path}")

        # 返回第一个路径方便复制
        print(f"\n📎 {saved_paths[0]}")

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
