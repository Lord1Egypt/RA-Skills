import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class LLMEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get("provider", "openai")
        self.model = config.get("model", "gpt-4")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 2000)
        
        self._client = None
        self._init_client()
        
    def _init_client(self):
        if self.provider == "openai":
            try:
                from openai import OpenAI
                api_key = os.environ.get("OPENAI_API_KEY")
                if api_key:
                    self._client = OpenAI(api_key=api_key)
                else:
                    logger.warning("OPENAI_API_KEY not set")
            except ImportError:
                logger.warning("openai package not installed")
                
    def generate(self, system_prompt: str, user_message: str) -> str:
        if self._client is None:
            return self._fallback_generate(system_prompt, user_message)
            
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return self._fallback_generate(system_prompt, user_message)
            
    def _fallback_generate(self, system_prompt: str, user_message: str) -> str:
        return f"（模拟回复）{user_message} - 这是一个示例回复，请配置LLM API Key以启用真实生成"
        
    def extract_profile(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not messages:
            return {"name": "Unknown", "nickname": "", "personality": "", "speaking_style": "", "catchphrases": "", "habitual_phrases": ""}
            
        conversation_text = "\n".join([
            f"{msg.get('sender', 'Unknown')}: {msg.get('content', '')}"
            for msg in messages[:100]
        ])
        
        profile_prompt = f"""请分析以下聊天记录，提取人物的性格特征、说话风格和口头禅。

聊天记录：
{conversation_text}

请用JSON格式返回以下信息：
{{
    "name": "人物称呼/名字",
    "nickname": "昵称",
    "personality": "性格特征（简洁描述）",
    "speaking_style": "说话风格（简洁描述）",
    "catchphrases": "口头禅（用逗号分隔）",
    "habitual_phrases": "习惯用语（用逗号分隔）"
}}
"""
        
        if self._client:
            try:
                response = self._client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "你是一个聊天记录分析助手，擅长提取人物性格特征。"},
                        {"role": "user", "content": profile_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                
                result_text = response.choices[0].message.content
                
                import re
                json_match = re.search(r'\{[\s\S]*\}', result_text)
                if json_match:
                    return json.loads(json_match.group())
            except Exception as e:
                logger.error(f"Profile extraction failed: {e}")
                
        return {
            "name": "Unknown",
            "nickname": "",
            "personality": "无法分析",
            "speaking_style": "无法分析",
            "catchphrases": "",
            "habitual_phrases": ""
        }
