import os
import aiohttp
import json
import re
from .safe_json import safe_parse_json

# ✅ 使用MiniMax API
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")

async def call_llm(prompt: str, model: str = "MiniMax-M2.5", temperature: float = 0.7) -> str:
    """调用MiniMax API（不依赖response_format）"""
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 2000
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{MINIMAX_BASE_URL}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            ) as resp:
                result = await resp.json()
                if resp.status == 200 and "choices" in result:
                    return result["choices"][0]["message"]["content"]
                else:
                    error_msg = result.get("error", {}).get("message", str(result))
                    print(f"[LLM Error] {error_msg}")
                    return "{}"
    except Exception as e:
        print(f"[LLM Exception] {e}")
        return "{}"

async def call_llm_json(prompt: str, model: str = "MiniMax-M2.5") -> dict:
    """强制返回JSON（用safe_parse解析）"""
    raw = await call_llm(prompt + "\n只输出纯JSON，不要思考过程。", model, temperature=0.1)
    return safe_parse_json(raw, default={})