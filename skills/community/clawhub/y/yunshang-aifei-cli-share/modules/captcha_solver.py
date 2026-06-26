#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证码识别模块
自动从以下来源获取 API Key（按优先级）：
1. 环境变量 DASHSCOPE_API_KEY
2. OpenClaw 配置文件中的 DashScope Key
3. .env 文件中的 DASHSCOPE_API_KEY

使用 qwen3.5-plus 模型识别算术验证码，零额外依赖。
"""

import json
import os
import re
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CAPTCHA_MODEL = 'qwen3.5-plus'  # 支持图片输入


def _find_api_config() -> tuple:
    """自动查找 API Key 和 Base URL"""
    # 1. 环境变量
    key = os.getenv('DASHSCOPE_API_KEY')
    base = os.getenv('DASHSCOPE_BASE_URL', '')
    if key:
        if not base:
            base = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
        return key, base

    # 2. 从 OpenClaw 配置文件读取
    openclaw_paths = [
        Path.home() / '.openclaw' / 'openclaw.json',
        Path(__file__).parent.parent.parent.parent / 'openclaw.json',
    ]
    for config_path in openclaw_paths:
        if config_path.exists():
            try:
                config = json.loads(config_path.read_text(encoding='utf-8'))
                providers = config.get('models', {}).get('providers', {})
                for name, provider in providers.items():
                    base_url = provider.get('baseUrl', '')
                    if 'dashscope' in base_url or 'alibaba' in name:
                        api_key = provider.get('apiKey', '')
                        if api_key and api_key != '__OPENCLAW_REDACTED__':
                            return api_key, base_url
            except Exception:
                pass

    raise RuntimeError(
        '未找到 API Key！请通过以下任一方式配置：\n'
        '  1. 在 .env 中设置 DASHSCOPE_API_KEY\n'
        '  2. 在 OpenClaw 配置中添加 alibaba provider\n'
        '申请地址：https://dashscope.console.aliyun.com/'
    )


def _extract_answer(text: str) -> str:
    """从模型返回文本中提取算式答案"""
    # 匹配 数字 运算符 数字 = 答案
    match = re.search(r'(\d+)\s*([+\-×xX*÷/])\s*(\d+)\s*=\s*(\d+)', text)
    if match:
        num1 = int(match.group(1))
        op = match.group(2)
        num2 = int(match.group(3))
        model_answer = match.group(4)

        # 验算
        op_map = {'+': '+', '-': '-', '×': '*', 'x': '*', 'X': '*', '*': '*', '÷': '/', '/': '/'}
        try:
            calc = str(int(eval(f'{num1}{op_map.get(op, op)}{num2}')))
            if calc != model_answer:
                print(f'[验证码] ⚠️ 模型={model_answer} 计算={calc}，使用计算结果')
                return calc
        except:
            pass
        return model_answer

    # 没匹配到算式，取最后一个数字
    numbers = re.findall(r'\d+', text)
    if numbers:
        return numbers[-1]

    return text.strip()


def solve_captcha(image_base64: str) -> str:
    """
    识别算术验证码

    Args:
        image_base64: Base64 编码的验证码图片

    Returns:
        验证码答案（数字字符串）
    """
    api_key, base_url = _find_api_config()

    response = requests.post(
        f'{base_url}/chat/completions',
        json={
            'model': CAPTCHA_MODEL,
            'messages': [{
                'role': 'user',
                'content': [
                    {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{image_base64}'}},
                    {'type': 'text', 'text': '这是一个算术验证码图片。请识别图中的算式并计算答案。只返回算式和答案，如：3+5=8'}
                ]
            }]
        },
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        timeout=15
    )

    if response.status_code != 200:
        raise RuntimeError(f'API 调用失败: {response.status_code} {response.text[:200]}')

    raw = response.json()['choices'][0]['message']['content'].strip()
    answer = _extract_answer(raw)
    print(f'[验证码识别] {raw} → {answer}')
    return answer


if __name__ == '__main__':
    try:
        key, base = _find_api_config()
        print(f'✅ API Key: {key[:10]}...')
        print(f'✅ 端点: {base}')
    except Exception as e:
        print(f'❌ {e}')
