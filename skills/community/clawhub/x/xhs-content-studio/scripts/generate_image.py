#!/usr/bin/env python3
"""
MiniMax 图片生成脚本（Python 备选版）
使用方法:
    python generate_image.py --prompt "描述" --aspect_ratio "3:4" --n 3

推荐使用 generate_image_smart.js（纯 Node.js，无需 Python）
"""

import argparse
import json
import os
import sys
import time
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

DEFAULT_CONFIG_PATH = os.path.join(SCRIPT_DIR, 'config.json')
DEFAULT_CONFIG_EXAMPLE = os.path.join(SCRIPT_DIR, 'config.json.example')
DEFAULT_OUTPUT_DIR = os.path.join(SKILL_DIR, 'generated_images')


def load_config():
    if os.path.exists(DEFAULT_CONFIG_PATH):
        with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    if os.path.exists(DEFAULT_CONFIG_EXAMPLE):
        with open(DEFAULT_CONFIG_EXAMPLE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def get_output_dir(config):
    configured = config.get('paths', {}).get('image_output_dir')
    if configured:
        configured = os.path.expanduser(configured)
        return configured
    return DEFAULT_OUTPUT_DIR


def generate_image(prompt, api_key, api_base, aspect_ratio='3:4', n=1, output_dir=None):
    url = api_base.rstrip('/') + "/v1/image_generation"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "n": n,
        "response_format": "base64"
    }

    print(f"[MiniMax] 正在生成图片...")
    print(f"  Prompt: {prompt}")
    print(f"  比例: {aspect_ratio}")
    print(f"  数量: {n}")

    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        result = response.json()

        raw_imgs = result.get('data', {}).get('image_base64', [])
        if not raw_imgs:
            print(f"[ERROR] API 返回格式异常: {result}")
            return []

        os.makedirs(output_dir, exist_ok=True)
        saved = []
        ts = int(time.time())

        for i, b64 in enumerate(raw_imgs):
            filename = f"img_{ts}_{i+1}.jpeg"
            filepath = os.path.join(output_dir, filename)
            img_data = bytes(b64, 'utf-8') if isinstance(b64, str) else b64
            # 直接 decode base64
            import base64
            img_bytes = base64.b64decode(img_data)
            with open(filepath, 'wb') as f:
                f.write(img_bytes)
            saved.append(filepath)
            print(f"  [OK] {filename} ({len(img_bytes)//1024}KB)")

        print(f"\n[MiniMax] 成功保存 {len(saved)} 张图片到 {output_dir}")
        return saved

    except Exception as e:
        print(f"[ERROR] {e}")
        return []


def main():
    parser = argparse.ArgumentParser(description='MiniMax 图片生成工具')
    parser.add_argument('--prompt', '-p', required=True, help='图片描述')
    parser.add_argument('--aspect_ratio', '-r', default='3:4', help='图片比例')
    parser.add_argument('--n', '-n', type=int, default=3, help='生成数量')
    parser.add_argument('--output_dir', '-o', default=None, help='输出目录')
    parser.add_argument('--api_key', '-k', default=None, help='API Key')

    args = parser.parse_args()
    config = load_config()

    api_key = args.api_key or config.get('minimax', {}).get('api_key')
    api_base = config.get('minimax', {}).get('api_base', 'https://api.minimaxi.com')

    if not api_key or api_key == '你的MiniMax API Key':
        print("[ERROR] 请先配置 MiniMax API Key!")
        print(f"  复制 {DEFAULT_CONFIG_EXAMPLE} 为 {DEFAULT_CONFIG_PATH}")
        print("  访问 https://platform.minimaxi.com/ 注册获取 API Key")
        sys.exit(1)

    output_dir = args.output_dir or get_output_dir(config)
    os.makedirs(output_dir, exist_ok=True)

    saved = generate_image(
        prompt=args.prompt,
        api_key=api_key,
        api_base=api_base,
        aspect_ratio=args.aspect_ratio,
        n=args.n,
        output_dir=output_dir
    )

    if saved:
        print(f"\n[DONE] {len(saved)} 张图片已保存")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
