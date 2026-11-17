#!/usr/bin/env python3
"""
SiliconFlow OCR 脚本
使用 Qwen VL 模型进行图片文字识别
"""

import os
import base64
import urllib.request
import json
import argparse


def ocr_image(image_path: str = None, image_url: str = None, 
              api_key: str = None, model: str = "Qwen/Qwen3-VL-8B-Instruct",
              prompt: str = "请识别图片中所有文字内容，原文输出。",
              timeout: int = 120) -> dict:
    """
    使用 SiliconFlow Qwen VL 模型识别图片文字
    
    Args:
        image_path: 本地图片路径（与 image_url 二选一）
        image_url: 图片URL（与 image_path 二选一）
        api_key: SiliconFlow API Key（默认从环境变量读取）
        model: 使用的模型，默认 Qwen/Qwen3-VL-8B-Instruct
        prompt: 识别提示词
        timeout: 超时时间（秒）
    
    Returns:
        dict: 包含 ok、text、usage 等字段的结果
    """
    if api_key is None:
        api_key = os.getenv("SILICONFLOW_API_KEY")
        if not api_key:
            return {"ok": False, "error": "未配置 SILICONFLOW_API_KEY 环境变量"}
    
    if not image_path and not image_url:
        return {"ok": False, "error": "必须提供 image_path 或 image_url"}
    
    # 处理图片数据
    if image_path:
        with open(image_path, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
        img_data = f"data:image/jpeg;base64,{img_b64}"
    else:
        img_data = image_url
    
    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": img_data}}
            ]
        }],
        "temperature": 0.1,
        "max_tokens": 4000
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        'https://api.siliconflow.cn/v1/chat/completions',
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            if 'error' in result:
                return {"ok": False, "error": result['error']}
            
            content = result['choices'][0]['message']['content']
            return {
                "ok": True,
                "text": content,
                "usage": result.get('usage', {}),
                "model": model
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            err_json = json.loads(error_body)
            return {"ok": False, "error": f"HTTP {e.code}: {err_json.get('message', error_body)}"}
        except:
            return {"ok": False, "error": f"HTTP {e.code}: {error_body[:200]}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description='SiliconFlow OCR 工具')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', '-f', help='本地图片路径')
    group.add_argument('--url', '-u', help='图片URL')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--api-key', '-k', help='SiliconFlow API Key（默认从环境变量读取）')
    parser.add_argument('--model', '-m', default='Qwen/Qwen3-VL-8B-Instruct', help='使用的模型')
    parser.add_argument('--prompt', '-p', default='请识别图片中所有文字内容，原文输出。', help='识别提示词')
    parser.add_argument('--pretty', action='store_true', help='格式化输出JSON')
    
    args = parser.parse_args()
    
    result = ocr_image(
        image_path=args.file,
        image_url=args.url,
        api_key=args.api_key,
        model=args.model,
        prompt=args.prompt
    )
    
    if result['ok']:
        print(result['text'])
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                if args.pretty:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                else:
                    f.write(result['text'])
            print(f"\n已保存到: {args.output}")
    else:
        print(f"错误: {result['error']}", file=__import__('sys').stderr)
        exit(1)


if __name__ == '__main__':
    main()
