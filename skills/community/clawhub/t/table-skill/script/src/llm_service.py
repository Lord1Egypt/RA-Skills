"""LLM 服务模块。

提供统一的 LLM 服务接口，支持多种 LLM 提供商。
"""

import os
from typing import Optional


class OpenAILLMService:
    """基于 OpenAI 兼容协议的 LLM 服务。
    
    支持配置:
    - api_key: API 密钥（必需）
    - base_url: API 基础 URL（可选，默认使用 OpenAI 官方）
    - model: 模型名称（可选）
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        from openai import AsyncOpenAI
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY 环境变量未设置。\n"
                "请设置环境变量或在 openclaw.json 中配置：\n"
                '  "skills": {\n'
                '    "entries": {\n'
                '      "table-preprocess": {\n'
                '        "env": {\n'
                '          "OPENAI_API_KEY": "your-api-key",\n'
                '          "OPENAI_BASE_URL": "https://api.openai.com/v1",\n'
                '          "OPENAI_MODEL": "gpt-4"\n'
                '        }\n'
                '      }\n'
                '    }\n'
                '  }'
            )
        
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")
        
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    async def chat_async(self, system_prompt: str, user_prompt: str) -> str:
        """调用 OpenAI Chat Completion API。
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
        
        Returns:
            AI 响应文本
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
        )
        
        return response.choices[0].message.content


def get_llm_service(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None
) -> OpenAILLMService:
    """获取 LLM 服务。
    
    Args:
        api_key: API 密钥（可选，默认从环境变量读取）
        base_url: API 基础 URL（可选，默认从环境变量读取）
        model: 模型名称（可选，默认从环境变量读取）
    
    Returns:
        OpenAILLMService 实例
    
    Raises:
        ValueError: 当 API 密钥未设置时
    """
    # 直接使用 OpenAI 兼容服务
    return OpenAILLMService(
        api_key=api_key,
        base_url=base_url,
        model=model
    )


__all__ = [
    "OpenAILLMService",
    "get_llm_service",
]
