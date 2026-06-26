#!/usr/bin/env python3
"""
多平台 LLM 客户端（OpenAI 兼容接口）。
通过 LLM_API_KEY + LLM_BASE_URL + LLM_MODEL 三个环境变量统一配置，
适配 DeepSeek / DashScope / OpenAI / Groq 等任意 OpenAI 兼容平台。

用法：
    from llm_client import LLMClient
    client = LLMClient.from_env()
    result = client.chat(messages=[{'role': 'user', 'content': '你好'}])

版本：v1.0.13
"""

import os
import time
import sys
from pathlib import Path

import requests

# 可重试的 HTTP 状态码
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class LLMClient:
    """OpenAI-compatible 多平台 LLM 客户端。

    环境变量要求（三者缺一不可）：
      LLM_API_KEY   API 密钥
      LLM_BASE_URL  API 基础地址（例：https://api.deepseek.com）
      LLM_MODEL     模型名称（例：deepseek-v4-pro）
    """

    def __init__(self, api_key: str, base_url: str, model: str,
                 max_retries: int = 3, timeout_base: int = 300):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.max_retries = max_retries
        self.timeout_base = timeout_base

    # ---- 工厂方法 ----

    @classmethod
    def from_env(cls):
        """从环境变量构建客户端。读取 ~/.openclaw/.env。"""
        from dotenv import load_dotenv
        load_dotenv(Path.home() / '.openclaw' / '.env')

        api_key = os.getenv('LLM_API_KEY', '').strip()
        base_url = os.getenv('LLM_BASE_URL', '').strip()
        model = os.getenv('LLM_MODEL', '').strip()

        missing = []
        if not api_key:
            missing.append('LLM_API_KEY')
        if not base_url:
            missing.append('LLM_BASE_URL')
        if not model:
            missing.append('LLM_MODEL')

        if missing:
            raise ValueError(
                f"\n❌ 缺少 LLM 配置环境变量：{', '.join(missing)}\n"
                f"\n请在 ~/.openclaw/.env 中配置：\n"
                f"  LLM_API_KEY=your_api_key\n"
                f"  LLM_BASE_URL=https://api.deepseek.com\n"
                f"  LLM_MODEL=deepseek-v4-pro\n"
            )

        return cls(api_key, base_url, model)

    # ---- 核心 API ----

    def chat(self, messages: list[dict], system_prompt: str | None = None,
             temperature: float = 0.7, max_tokens: int | None = None) -> str | None:
        """
        OpenAI-compatible /chat/completions。

        请求：POST {base_url}/chat/completions
        返回：AI 响应文本，失败返回 None。
        """
        if system_prompt:
            full_msgs = [{'role': 'system', 'content': system_prompt}] + list(messages)
        else:
            full_msgs = list(messages)

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

        body = {
            'model': self.model,
            'messages': full_msgs,
            'stream': False,
        }
        if temperature is not None:
            body['temperature'] = temperature
        if max_tokens is not None:
            body['max_tokens'] = max_tokens

        endpoint = f'{self.base_url}/chat/completions'
        last_error: Exception | None = None

        for attempt in range(self.max_retries):
            try:
                timeout = self.timeout_base * (attempt + 1)
                print(f"   尝试 {attempt + 1}/{self.max_retries} (超时：{timeout}s)...")

                response = requests.post(
                    endpoint, headers=headers, json=body, timeout=timeout,
                )

                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']

                if response.status_code in RETRYABLE_STATUS:
                    wait_s = 2 ** attempt
                    print(f"   ⚠️  HTTP {response.status_code}，{wait_s}s 后重试...")
                    time.sleep(wait_s)
                    continue

                print(f"   ❌ HTTP {response.status_code}: {response.text[:300]}")
                return None

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                print(f"   ⚠️  {type(e).__name__}，准备重试...")
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)

        if last_error:
            print(f"   ❌ 重试耗尽：{last_error}")
        return None

    # ---- 便捷方法 ----

    def analyze_simple(self, system_prompt: str, user_prompt: str) -> str | None:
        """简化调用：system + user 单轮对话。"""
        return self.chat(
            messages=[{'role': 'user', 'content': user_prompt}],
            system_prompt=system_prompt,
        )

    def __repr__(self) -> str:
        return f"LLMClient(model={self.model}, base_url={self.base_url})"


# ============ 独立测试入口 ============
if __name__ == '__main__':
    try:
        client = LLMClient.from_env()
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    print(f"🚀 {client}")
    print()

    result = client.chat(
        messages=[{'role': 'user', 'content': '请用一句话介绍你自己'}],
    )

    if result:
        print(f"✅ 响应: {result}")
    else:
        print("❌ 调用失败")
        sys.exit(1)
