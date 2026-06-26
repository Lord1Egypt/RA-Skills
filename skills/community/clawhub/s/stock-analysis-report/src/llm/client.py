from __future__ import annotations

import json
import logging
import re

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class LLMClient:
    """LLM 客户端，支持 DeepSeek 和 OpenAI 兼容模型"""

    def __init__(self, base_url: str, api_key: str, model: str):
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    async def analyze(self, system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
        """调用 LLM 进行分析，返回原始文本"""
        try:
            logger.debug("LLM 请求: model=%s, system_prompt=%d字符, user_prompt=%d字符",
                         self.model, len(system_prompt), len(user_prompt))
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=8192,
            )
            content = response.choices[0].message.content
            if content is None:
                raise ValueError("LLM 返回内容为空")
            usage = response.usage
            if usage:
                logger.debug("LLM 响应: %d字符, tokens(prompt=%d, completion=%d, total=%d)",
                             len(content), usage.prompt_tokens, usage.completion_tokens, usage.total_tokens)
            else:
                logger.debug("LLM 响应: %d字符", len(content))
            return content.strip()
        except Exception as e:
            logger.error("LLM 调用失败: %s", e)
            raise

    async def analyze_json(self, system_prompt: str, user_prompt: str, temperature: float = 0.3) -> dict:
        """调用 LLM 并解析 JSON 响应"""
        raw = await self.analyze(system_prompt, user_prompt, temperature)
        return self._extract_json(raw)

    @staticmethod
    def _extract_json(text: str) -> dict:
        """从 LLM 输出中提取 JSON，支持 markdown 代码块包裹"""
        json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
        if json_match:
            text = json_match.group(1).strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            brace_match = re.search(r"\{.*\}", text, re.DOTALL)
            if brace_match:
                try:
                    return json.loads(brace_match.group())
                except json.JSONDecodeError:
                    pass
            logger.warning("无法解析 LLM 输出为 JSON，返回原始文本包装")
            return {"raw_text": text}
