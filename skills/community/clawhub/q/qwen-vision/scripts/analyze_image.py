#!/usr/bin/env python3
"""
Analyze images using Qwen Vision API (Alibaba Cloud DashScope).
"""

import argparse
import base64
import json
import urllib.request
import urllib.error
import sys
from pathlib import Path


def analyze_image(image_path: str, prompt: str, api_key: str, model: str = "qwen-vl-max-latest"):
    """Analyze an image using Qwen Vision API."""
    
    # Read and encode image
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Determine mime type
    ext = Path(image_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.png': 'image/png', '.gif': 'image/gif',
        '.webp': 'image/webp', '.bmp': 'image/bmp'
    }
    mime_type = mime_types.get(ext, 'image/jpeg')
    
    # Build request
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    
    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_data}"
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }]
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error: Unexpected response format: {json.dumps(result, ensure_ascii=False)}"
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ""
        return f"HTTP Error {e.code}: {e.reason}\n{error_body}"
    except Exception as e:
        return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(description="Analyze images using Qwen Vision API")
    parser.add_argument("--image", "-i", required=True, help="Path to image file")
    parser.add_argument("--prompt", "-p", default="请详细描述这张图片的内容。", help="Analysis prompt")
    parser.add_argument("--model", "-m", default="qwen-vl-max-latest", 
                        help="Model: qwen-vl-max-latest, qwen-vl-plus-latest")
    parser.add_argument("--api-key", "-k", required=True, help="DashScope API key")
    
    args = parser.parse_args()
    
    result = analyze_image(args.image, args.prompt, args.api_key, args.model)
    print(result)


if __name__ == "__main__":
    main()
