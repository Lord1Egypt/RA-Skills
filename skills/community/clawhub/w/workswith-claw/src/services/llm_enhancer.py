"""
LLM 意图增强器
"""
import os
import json
import aiohttp
from typing import Optional
from src.models.intent import IntentResult


class LLMIntentEnhancer:
    """LLM 意图增强 - 处理模糊意图"""
    
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai")  # openai, anthropic, minimax
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.enabled = bool(self.api_key)
    
    async def enhance(self, utterance: str, context: dict = None) -> Optional[IntentResult]:
        """使用 LLM 增强意图理解"""
        
        if not self.enabled:
            return None
        
        # 构建 prompt
        prompt = self._build_prompt(utterance, context)
        
        try:
            # 调用 LLM
            result = await self._call_llm(prompt)
            
            # 解析结果
            return self._parse_result(result)
        except Exception as e:
            print(f"[LLMIntentEnhancer] Error: {e}")
            return None
    
    def _build_prompt(self, utterance: str, context: dict) -> str:
        return f"""用户的输入模糊或不明确，请推断用户可能的意图。

用户输入: {utterance}
上下文: {json.dumps(context or {}, ensure_ascii=False)}

请返回可能的意图（可选）:
{{
    "intent_type": "scene|action|query",
    "scene_id": "场景ID（如 movie, bath_prep, home, away）",
    "confidence": 0.0-1.0,
    "reasoning": "推理理由"
}}

如果无法推断，返回: {{"intent_type": "unknown"}}
"""

    async def _call_llm(self, prompt: str) -> str:
        """调用 LLM API"""
        
        if self.provider == "openai":
            return await self._call_openai(prompt)
        elif self.provider == "anthropic":
            return await self._call_anthropic(prompt)
        elif self.provider == "minimax":
            return await self._call_minimax(prompt)
        else:
            raise Exception(f"Unknown provider: {self.provider}")
    
    async def _call_openai(self, prompt: str) -> str:
        async with aiohttp.ClientSession() as session:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            body = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
            async with session.post(url, json=body, headers=headers) as resp:
                result = await resp.json()
                return result["choices"][0]["message"]["content"]
    
    async def _call_anthropic(self, prompt: str) -> str:
        async with aiohttp.ClientSession() as session:
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            body = {
                "model": self.model,
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}]
            }
            async with session.post(url, json=body, headers=headers) as resp:
                result = await resp.json()
                return result["content"][0]["text"]
    
    async def _call_minimax(self, prompt: str) -> str:
        async with aiohttp.ClientSession() as session:
            url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            body = {
                "model": "abab6.5s-chat",
                "messages": [{"role": "user", "content": prompt}]
            }
            async with session.post(url, json=body, headers=headers) as resp:
                result = await resp.json()
                return result["choices"][0]["message"]["content"]
    
    def _parse_result(self, result: str) -> Optional[IntentResult]:
        """解析 LLM 返回结果"""
        try:
            data = json.loads(result)
            
            if data.get("intent_type") == "unknown":
                return None
            
            return IntentResult(
                intent_type=data.get("intent_type", "scene"),
                scene_id=data.get("scene_id"),
                params={},
                confidence=data.get("confidence", 0.5),
                message=data.get("reasoning", "")
            )
        except:
            return None
