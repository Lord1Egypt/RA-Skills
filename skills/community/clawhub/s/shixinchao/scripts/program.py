#!/usr/bin/env python3
"""
测试-史新超 脚本

功能：测试-史新超
授权方式：ApiKey (Bearer Token)
凭证Key：通过环境变量 API_KEY 配置
"""

import os
import sys
import json
import argparse
import uuid
import warnings
warnings.filterwarnings("ignore", message="urllib3.*doesn't match a supported version")
import requests


def call_api(question: str, variables: dict) -> str:
    """
    调用异步对话 API

    Args:
        question: 用户输入文本
        variables: API 请求变量

    Returns:
        str: API 返回结果

    Raises:
        ValueError: 缺少必要配置
        Exception: API 调用失败
    """
    # 1. 获取凭证
    api_key = ""

    # 2. 获取 API 地址
    url = "https://developer.jointpilot.com/v1/api/async_chat/completions/"

    # 3. 构建请求
    chat_id = str(uuid.uuid4())
    data_id = str(uuid.uuid4())

    payload = {
        "chatId": chat_id,
        "stream": True,
        "detail": False,
        "variables": variables,
        "messages": [
            {
                "dataId": data_id,
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": {
                            "content": question
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 4. 发起请求
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            stream=False,
            timeout=60
        )

        # 检查 HTTP 状态码
        if response.status_code >= 400:
            raise Exception(f"HTTP 请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")

        # 5. 处理流式响应
        answer_parts = []

        for line in response.iter_lines():
            if not line:
                continue

            line_str = line.decode('utf-8')

            # 跳过空行和注释
            if not line_str.strip() or line_str.startswith(':'):
                continue

            # 解析 SSE 格式
            if line_str.startswith('data:'):
                data_str = line_str[5:].strip()

                if data_str == '[DONE]':
                    break

                try:
                    data = json.loads(data_str)

                    # 提取内容
                    if 'choices' in data and len(data['choices']) > 0:
                        delta = data['choices'][0].get('delta', {})
                        content = delta.get('content', '')

                        if content:
                            answer_parts.append(content)

                except json.JSONDecodeError:
                    continue

        # 6. 返回结果
        if answer_parts:
            return ''.join(answer_parts)
        else:
            raise Exception("未获取到有效答案")

    except requests.exceptions.RequestException as e:
        raise Exception(f"API 调用失败: {str(e)}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='测试-史新超')
    parser.add_argument(
        '--question',
        type=str,
        required=True,
        help='用户输入文本'
    )
    
    args = parser.parse_args()

    # 构建 variables 字典
    variables = {}

    try:
        result = call_api(args.question, variables)
        print(result)
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
