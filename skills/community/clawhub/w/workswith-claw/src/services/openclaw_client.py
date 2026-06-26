"""
OpenClaw 集成
"""
import os
import json
import aiohttp
from typing import Optional


class OpenClawClient:
    """OpenClaw 集成客户端"""
    
    def __init__(self):
        self.url = os.getenv("OPENCLAW_URL", "http://localhost:8080")
        self.api_key = os.getenv("OPENCLAW_API_KEY", "")
        self.enabled = bool(self.url and self.url != "http://localhost:8080")
    
    async def chat(self, message: str, context: dict = None) -> Optional[str]:
        """发送消息到 OpenClaw"""
        
        if not self.enabled:
            return None
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.url}/api/chat"
                headers = {"Content-Type": "application/json"}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                body = {
                    "message": message,
                    "context": context or {}
                }
                
                async with session.post(url, json=body, headers=headers) as resp:
                    if resp.status >= 400:
                        return None
                    result = await resp.json()
                    return result.get("response")
        except Exception as e:
            print(f"[OpenClawClient] Error: {e}")
            return None
    
    async def execute_intent(self, intent_result: dict) -> str:
        """执行意图并生成自然语言响应"""
        
        if not self.enabled:
            return self._default_response(intent_result)
        
        # 构建上下文
        context = {
            "intent": intent_result.get("intent_type"),
            "scene": intent_result.get("scene"),
            "details": intent_result.get("details", [])
        }
        
        # 尝试获取自然语言响应
        response = await self.chat(
            f"用户说：{intent_result.get('utterance', '')}\n"
            f"意图：{intent_result.get('intent_type')}\n"
            f"场景：{intent_result.get('scene')}",
            context
        )
        
        return response or self._default_response(intent_result)
    
    def _default_response(self, intent_result: dict) -> str:
        """默认响应"""
        intent_type = intent_result.get("intent_type")
        
        responses = {
            "scene": "搞定！",
            "action": "好嘞！",
            "query": "这个嘛..."
        }
        
        return responses.get(intent_type, "好的")
