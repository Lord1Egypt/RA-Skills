import os
import json
import aiohttp

class MiniMaxClient:
    """MiniMax TokenPlan客户端 - 只用支持的模型"""
    
    def __init__(self):
        self.api_key = os.getenv("MINIMAX_API_KEY")
        self.base_url = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
        
        # ✅ 只用TokenPlan支持的模型
        self.models = {
            "queen": "MiniMax-M2.5",
            "worker_time": "MiniMax-M2.5",      # ✅ 改用M2.5
            "worker_budget": "MiniMax-M2.5",    # ✅ 改用M2.5
            "worker_experience": "MiniMax-M2.5", # ✅ 改用M2.5
            "default": "MiniMax-M2.5",
            "fast": "MiniMax-M2.5",             # ✅ 改用M2.5
        }
    
    async def call(self, prompt: str, model_type: str = "default") -> str:
        """调用MiniMax API"""
        model = self.models.get(model_type, self.models["default"])
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            ) as resp:
                result = await resp.json()
                if resp.status == 200 and "choices" in result:
                    return result["choices"][0]["message"]["content"]
                else:
                    error_msg = result.get("error", {}).get("message", str(result))
                    raise Exception(f"MiniMax API失败: {error_msg}")

# 全局实例
minimax_client = MiniMaxClient()

async def call_llm(prompt: str) -> str:
    """默认调用 - MiniMax-M2.5"""
    return await minimax_client.call(prompt, "default")

async def call_llm_fast(prompt: str) -> str:
    """极速调用 - MiniMax-M2.7-highspeed"""
    return await minimax_client.call(prompt, "fast")

async def call_llm_queen(prompt: str) -> str:
    """蜂女王调用 - MiniMax-M2.5（仲裁决策）"""
    return await minimax_client.call(prompt, "queen")

async def call_llm_json(prompt: str) -> dict:
    """强制返回JSON"""
    content = await minimax_client.call(
        prompt + "\n\n只输出合法JSON，不要其他文字。",
        "default"
    )
    content = content.strip()
    
    try:
        return json.loads(content)
    except:
        pass
    
    # 提取JSON部分
    start = content.find("{")
    end = content.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(content[start:end])
        except:
            pass
    
    return {"error": "JSON解析失败", "raw": content[:200]}