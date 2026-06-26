#!/usr/bin/env python3
"""
大模型 JSON 生成工具
使用 LangChain 框架的结构化输出功能，确保返回正确的 JSON 格式

使用方式: python llm_json.py --content 内容 --prompt 提示词 --api_key API密钥 --output 输出.json

参数:
    --content/-c    : 要处理的内容（文本或 OCR 识别结果）
    --prompt/-p      : 给大模型的提示词
    --api_key/-k     : MiniMax API 密钥
    --output/-o      : 输出 JSON 文件路径
    --base_url       : API 地址（可选，默认 https://api.minimaxi.com/v1）
    --model          : 模型名称（可选，默认 MiniMax-M2.5）
    --temperature    : 温度参数（可选，默认 1.0）
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Union

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minimax_langchain import (
    get_chat_model,
    simple_chat_with_json,
    SalesData,
    SalesDataList,
    chat_with_json_output,
)


def chat_with_json(
    content: str,
    prompt: str,
    api_key: str,
    base_url: str = "https://api.minimaxi.com/v1",
    model: str = "MiniMax-M2.5",
    temperature: float = 1.0,
    use_structured_output: bool = True,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    发送文本给大模型并使用 LangChain 结构化输出获取 JSON 响应

    参数:
        content: 要处理的内容（文本）
        prompt: 给大模型的提示词
        api_key: API 密钥
        base_url: API 地址
        model: 模型名称
        temperature: 温度参数
        use_structured_output: 是否使用 LangChain 结构化输出（推荐启用）

    返回:
        解析后的 JSON 数据
    """
    full_prompt = f"{prompt}\n\n内容:\n{content}"

    if use_structured_output:
        return chat_with_json_output(
            prompt=full_prompt,
            json_schema=SalesDataList,
            temperature=temperature,
            api_key=api_key,
            model=model,
            base_url=base_url,
        )
    else:
        return simple_chat_with_json(
            full_prompt,
            temperature=temperature,
            api_key=api_key,
            model=model,
            base_url=base_url,
        )


def main():
    parser = argparse.ArgumentParser(description='大模型 JSON 生成工具 (LangChain 版)')
    parser.add_argument('--content', '-c', required=True, help='要处理的内容')
    parser.add_argument('--prompt', '-p', required=True, help='给大模型的提示词')
    parser.add_argument('--api_key', '-k', required=True, help='MiniMax API 密钥')
    parser.add_argument('--output', '-o', required=True, help='输出 JSON 文件路径')
    parser.add_argument('--base_url', default='https://api.minimaxi.com/v1', help='API 地址')
    parser.add_argument('--model', default='MiniMax-M2.5', help='模型名称')
    parser.add_argument('--temperature', type=float, default=1.0, help='温度参数')
    parser.add_argument('--no-structured', action='store_true', help='不使用 LangChain 结构化输出')

    args = parser.parse_args()

    print(f"正在调用大模型 (LangChain 结构化输出)...")

    try:
        result = chat_with_json(
            content=args.content,
            prompt=args.prompt,
            api_key=args.api_key,
            base_url=args.base_url,
            model=args.model,
            temperature=args.temperature,
            use_structured_output=not args.no_structured,
        )

        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"✓ 结果已保存到: {args.output}")
        print(f"\n结果预览:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
