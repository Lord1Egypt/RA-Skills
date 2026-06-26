#!/usr/bin/env python3
"""
SiliconFlow Qwen2.5-VL - 图片理解
使用 SiliconFlow 的 Qwen2.5-VL 模型进行图片分析
"""

import os
import sys
import base64
import json
import requests
import argparse

def encode_image(image_path: str) -> str:
    """将图片编码为 base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_image(image_path: str, prompt: str, api_key: str = None) -> str:
    """使用 SiliconFlow Qwen2.5-VL 分析图片"""
    
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: 请设置 OPENAI_API_KEY 环境变量或传入 api_key 参数", file=sys.stderr)
        sys.exit(1)
    
    # 编码图片
    image_data = encode_image(image_path)
    
    # SiliconFlow API 请求
    url = "https://api.siliconflow.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 使用 Qwen2.5-VL 模型 (支持图片理解)
    payload = {
        "model": "Qwen/Qwen2.5-VL-72B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2048
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    
    if response.status_code != 200:
        print(f"Error: API 返回错误 {response.status_code}", file=sys.stderr)
        print(response.text, file=sys.stderr)
        sys.exit(1)
    
    result = response.json()
    
    if "choices" in result and len(result["choices"]) > 0:
        return result["choices"][0]["message"]["content"]
    else:
        print(f"Error: API 返回格式异常", file=sys.stderr)
        print(json.dumps(result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="SiliconFlow Qwen2.5-VL 图片理解")
    parser.add_argument("--image", "-i", required=True, help="图片路径")
    parser.add_argument("--prompt", "-p", default="请描述这张图片", help="提示词")
    parser.add_argument("--api-key", "-k", help="API Key (可选，默认从环境变量读取)")
    parser.add_argument("--output", "-o", help="输出文件路径 (可选)")
    
    args = parser.parse_args()
    
    result = analyze_image(args.image, args.prompt, args.api_key)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"结果已保存到: {args.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()
