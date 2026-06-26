"""
LLM API 客户端 - 支持 OpenAI 兼容 API
"""

import os
import time
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class LLMClient:
    """SiliconFlow LLM 客户端"""
    
    def __init__(self):
        self.api_key = os.getenv("SILICONFLOW_API_KEY")
        self.base_url = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
        self.model = os.getenv("SILICONFLOW_MODEL", "Qwen/Qwen3-8B")
        self.rate_limit = int(os.getenv("API_RATE_LIMIT", "2"))
        
        if not self.api_key:
            raise ValueError("SILICONFLOW_API_KEY 未配置，请检查.env 文件")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        self._last_request_time = 0
    
    def _wait_for_rate_limit(self):
        """等待以满足限流要求"""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed
            time.sleep(sleep_time)
        self._last_request_time = time.time()
    
    def chat(self, messages: list, max_tokens: int = 2000) -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            max_tokens: 最大返回 token 数
            
        Returns:
            LLM 响应文本
        """
        self._wait_for_rate_limit()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.3,  # 较低温度，保证分析准确性
            )
            return response.choices[0].message.content
        except Exception as e:
            if "429" in str(e) or "rate limit" in str(e).lower():
                # 遇到限流，等待更长时间后重试
                print("⚠️  触发限流，等待 10 秒后重试...")
                time.sleep(10)
                return self.chat(messages, max_tokens)
            raise e
    
    def analyze_log(self, log_content: str, mode: str = "brief") -> str:
        """
        分析安全日志
        
        Args:
            log_content: 日志内容
            mode: 分析模式 ("brief" 或 "detailed")
            
        Returns:
            分析报告
        """
        from prompts import SYSTEM_PROMPT, BRIEF_ANALYSIS_PROMPT, DETAILED_ANALYSIS_PROMPT
        
        # 选择提示词
        if mode == "detailed":
            user_prompt = DETAILED_ANALYSIS_PROMPT.format(log_content=log_content)
            max_tokens = 3000
        else:
            user_prompt = BRIEF_ANALYSIS_PROMPT.format(log_content=log_content)
            max_tokens = 1500
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        
        return self.chat(messages, max_tokens)


# 测试函数
def test_connection():
    """测试 API 连接"""
    client = LLMClient()
    try:
        response = client.chat([{"role": "user", "content": "你好，请用一句话介绍你自己"}])
        print("✅ API 连接成功")
        print(f"响应：{response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ API 连接失败：{e}")
        return False


if __name__ == "__main__":
    test_connection()
