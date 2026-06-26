#!/usr/bin/env python3
"""
Sih.AI图片生成API客户端
支持图片URL或Base64输入，返回生成后的图片URL
"""
import sys
import json
import base64
import requests
from pathlib import Path

API_URL = "https://api.vwu.ai/v1/images/generations/"
API_TOKEN = "sk-w4YfLvoXwIEM0I3uNcOOOclfHkBDiR19Md9ixabWv1XMNPhn"
DEFAULT_MODEL = "sihai-image-27"


def encode_image_to_base64(image_path: str) -> str:
    """将图片文件编码为base64格式（不带前缀，适配sihai-image-27模型）"""
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    # sihai-image-27模型只需要纯base64，不需要data:image前缀
    return image_data


def generate_image(image_input: str, prompt: str, model: str = DEFAULT_MODEL) -> dict:
    """
    调用图片生成API

    Args:
        image_input: 图片URL或本地文件路径
        prompt: 处理提示词（如"背景改为在海边"）
        model: 模型名称，默认sihai-image-27

    Returns:
        API响应的JSON数据
    """
    # 判断是URL还是本地文件
    if image_input.startswith(('http://', 'https://')):
        image = image_input
    else:
        # 本地文件，转换为base64
        image = encode_image_to_base64(image_input)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    payload = {
        "image": [image],
        "prompt": prompt,
        "model": model
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("Usage: python image_gen.py <image_url_or_path> <prompt> [model]")
        print("Example: python image_gen.py https://example.com/image.jpg '背景改为在海边'")
        print("Example: python image_gen.py ./photo.jpg '换成动漫风格'")
        sys.exit(1)

    image_input = sys.argv[1]
    prompt = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_MODEL

    try:
        result = generate_image(image_input, prompt, model)
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # 提取并打印图片URL
        if 'data' in result and len(result['data']) > 0:
            print("\n生成的图片URL:")
            for item in result['data']:
                print(f"- {item['url']}")

    except requests.exceptions.RequestException as e:
        print(f"Error: API请求失败 - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
