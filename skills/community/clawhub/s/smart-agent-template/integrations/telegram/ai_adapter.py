"""
AI 引擎适配器（优化版 v2.0）
新增：上下文感知、工作规范融入
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict


class AIAdapter(ABC):
    """AI 引擎适配器基类"""
    
    def __init__(self):
        self.model = None  # 子类需要设置
    
    @abstractmethod
    async def get_response(self, message: str, context: dict) -> str:
        """
        获取 AI 回复
        
        Args:
            message: 用户消息
            context: 上下文信息
                - history: 对话历史 (list)
                - memory: 长期记忆 (str)
                - system_prompt: 系统提示词 (str)
            
        Returns:
            AI 回复内容
        """
        pass
    
    def _build_messages(self, message: str, context: dict) -> List[Dict]:
        """构建消息列表（融入上下文）"""
        messages = []
        
        # 1. 添加对话历史（短期记忆）
        history = context.get("history", [])
        if history:
            # 只保留最近 5 轮（10 条消息）
            recent_history = history[-10:]
            messages.extend(recent_history)
        
        # 2. 添加当前消息
        messages.append({"role": "user", "content": message})
        
        return messages
    
    def _build_system_prompt(self, context: dict) -> str:
        """构建 System Prompt（融入记忆 + 工作规范）"""
        # 基础 System Prompt
        base_prompt = context.get("system_prompt", "你是一个智能助手")
        
        # 添加长期记忆
        memory = context.get("memory", "")
        if memory:
            memory_section = f"\n\n【长期记忆】\n{memory[:500]}"  # 限制长度
            base_prompt += memory_section
        
        return base_prompt


class OpenAIAdapter(AIAdapter):
    """OpenAI 适配器"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        super().__init__()
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError("请安装 openai: pip install openai")
    
    async def get_response(self, message: str, context: dict) -> str:
        system_prompt = self._build_system_prompt(context)
        messages = self._build_messages(message, context)
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                *messages
            ]
        )
        return response.choices[0].message.content


class ClaudeAdapter(AIAdapter):
    """Claude 适配器（支持自定义 base_url）"""
    
    def __init__(self, api_key: str, model: str = "claude-sonnet-4", base_url: Optional[str] = None):
        super().__init__()
        try:
            import anthropic
            # 支持自定义 base_url（本地 Claude 代理）
            if base_url:
                self.client = anthropic.AsyncAnthropic(api_key=api_key, base_url=base_url)
            else:
                self.client = anthropic.AsyncAnthropic(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError("请安装 anthropic: pip install anthropic")
    
    async def get_response(self, message: str, context: dict) -> str:
        system_prompt = self._build_system_prompt(context)
        messages = self._build_messages(message, context)
        
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=messages
        )
        return response.content[0].text


class DeepSeekAdapter(AIAdapter):
    """DeepSeek 适配器"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        super().__init__()
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
            self.model = model
        except ImportError:
            raise ImportError("请安装 openai: pip install openai")
    
    async def get_response(self, message: str, context: dict) -> str:
        system_prompt = self._build_system_prompt(context)
        messages = self._build_messages(message, context)
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                *messages
            ]
        )
        return response.choices[0].message.content


class OllamaAdapter(AIAdapter):
    """Ollama 适配器（本地模型）"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        super().__init__()
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(
                base_url=f"{base_url}/v1",
                api_key="ollama"  # Ollama 不需要真实 API key
            )
            self.model = model
        except ImportError:
            raise ImportError("请安装 openai: pip install openai")
    
    async def get_response(self, message: str, context: dict) -> str:
        system_prompt = self._build_system_prompt(context)
        messages = self._build_messages(message, context)
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                *messages
            ]
        )
        return response.choices[0].message.content


def create_ai_adapter(engine: str, api_key: Optional[str] = None, 
                     model: Optional[str] = None, 
                     base_url: Optional[str] = None) -> AIAdapter:
    """
    创建 AI 适配器工厂函数
    
    Args:
        engine: AI 引擎类型
        api_key: API Key
        model: 模型名称
        base_url: API 基础 URL
        
    Returns:
        AI 适配器实例
    """
    if engine == "openai":
        return OpenAIAdapter(api_key, model or "gpt-4")
    elif engine == "claude":
        # 支持自定义 base_url（本地 Claude 代理）
        return ClaudeAdapter(api_key, model or "claude-sonnet-4", base_url=base_url)
    elif engine == "deepseek":
        return DeepSeekAdapter(api_key, model or "deepseek-chat")
    elif engine == "ollama":
        return OllamaAdapter(base_url or "http://localhost:11434", model or "llama2")
    else:
        raise ValueError(f"Unsupported AI engine: {engine}")
