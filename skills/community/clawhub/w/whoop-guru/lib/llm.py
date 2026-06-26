"""
LLM API 集成模块
支持多种模型提供商和用户自定义配置

支持的提供商：
- MiniMax (默认)
- OpenAI (GPT-4, GPT-3.5)
- Claude (Anthropic)
- 智谱AI (GLM)
- 通义千问
- DeepSeek
- Kimi (Moonshot)
- 硅基流动
- 任何 OpenAI 兼容 API

用户配置流程：
1. 选择提供商
2. 输入API Key
3. （可选）选择模型
4. 测试连接
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

# 路径配置
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SKILL_DIR, "data", "config", "llm_config.json")


# 支持的提供商配置
PROVIDERS: Dict[str, Dict] = {
    "minimax": {
        "name": "MiniMax",
        "name_cn": "MiniMax",
        "default_model": "abab6.5s-chat",
        "api_url": "https://api.minimax.chat/v1/text/chatcompletion_pro",
        "api_key_hint": "在 MiniMax 控制台获取 API Key",
        "models": [
            {"id": "abab6.5s-chat", "name": "ABAB 6.5S (默认)", "desc": "最新最强模型"},
            {"id": "abab6.5-chat", "name": "ABAB 6.5", "desc": "标准版"},
            {"id": "abab5.5s-chat", "name": "ABAB 5.5S", "desc": "轻量版"},
        ],
        "official_url": "https://platform.minimaxi.com"
    },
    "openai": {
        "name": "OpenAI",
        "name_cn": "OpenAI",
        "default_model": "gpt-4",
        "api_url": "https://api.openai.com/v1/chat/completions",
        "api_key_hint": "在 OpenAI 控制台获取 API Key",
        "models": [
            {"id": "gpt-4-turbo-preview", "name": "GPT-4 Turbo (推荐)", "desc": "速度快，性能强"},
            {"id": "gpt-4", "name": "GPT-4", "desc": "标准版"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "desc": "快速便宜"},
        ],
        "official_url": "https://platform.openai.com"
    },
    "claude": {
        "name": "Claude",
        "name_cn": "Claude",
        "default_model": "claude-3-opus-20240229",
        "api_url": "https://api.anthropic.com/v1/messages",
        "api_key_hint": "在 Anthropic 控制台获取 API Key",
        "models": [
            {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus (最强)", "desc": "最强大模型"},
            {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "desc": "性价比高"},
            {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku", "desc": "最快最便宜"},
        ],
        "official_url": "https://console.anthropic.com"
    },
    "glm": {
        "name": "GLM",
        "name_cn": "智谱AI (GLM)",
        "default_model": "glm-4",
        "api_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "api_key_hint": "在 智谱AI 控制台获取 API Key",
        "models": [
            {"id": "glm-4", "name": "GLM-4 (推荐)", "desc": "最新最强模型"},
            {"id": "glm-4-flash", "name": "GLM-4 Flash", "desc": "快速便宜"},
            {"id": "glm-3-turbo", "name": "GLM-3 Turbo", "desc": "标准版"},
        ],
        "official_url": "https://open.bigmodel.cn"
    },
    "kimi": {
        "name": "Kimi",
        "name_cn": "Kimi (Moonshot)",
        "default_model": "moonshot-v1-8k",
        "api_url": "https://api.moonshot.cn/v1/chat/completions",
        "api_key_hint": "在 Kimi 控制台获取 API Key",
        "models": [
            {"id": "moonshot-v1-8k", "name": "Moonshot V1 8K", "desc": "默认上下文8K"},
            {"id": "moonshot-v1-32k", "name": "Moonshot V1 32K", "desc": "长上下文32K"},
            {"id": "moonshot-v1-128k", "name": "Moonshot V1 128K", "desc": "超长上下文128K"},
        ],
        "official_url": "https://platform.moonshot.cn"
    },
    "qwen": {
        "name": "Qwen",
        "name_cn": "通义千问",
        "default_model": "qwen-turbo",
        "api_url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        "api_key_hint": "在 阿里云百炼 获取 API Key",
        "models": [
            {"id": "qwen-turbo", "name": "Qwen Turbo (快速)", "desc": "快速响应"},
            {"id": "qwen-plus", "name": "Qwen Plus (推荐)", "desc": "性价比高"},
            {"id": "qwen-max", "name": "Qwen Max", "desc": "最强模型"},
        ],
        "official_url": "https://dashscope.console.aliyun.com"
    },
    "deepseek": {
        "name": "DeepSeek",
        "name_cn": "DeepSeek",
        "default_model": "deepseek-chat",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "api_key_hint": "在 DeepSeek 控制台获取 API Key",
        "models": [
            {"id": "deepseek-chat", "name": "DeepSeek Chat", "desc": "通用对话"},
            {"id": "deepseek-coder", "name": "DeepSeek Coder", "desc": "代码专用"},
        ],
        "official_url": "https://platform.deepseek.com"
    },
    "siliconflow": {
        "name": "SiliconFlow",
        "name_cn": "硅基流动",
        "default_model": "Qwen/Qwen2.5-7B-Instruct",
        "api_url": "https://api.siliconflow.cn/v1/chat/completions",
        "api_key_hint": "在 硅基流动 获取 API Key (有免费额度)",
        "models": [
            {"id": "Qwen/Qwen2.5-7B-Instruct", "name": "Qwen2.5 7B (推荐)", "desc": "免费可用"},
            {"id": "deepseek-ai/DeepSeek-V2.5", "name": "DeepSeek V2.5", "desc": "强大开源"},
            {"id": "THUDM/glm-4-9b-chat", "name": "GLM-4 9B", "desc": "国产开源"},
        ],
        "official_url": "https://cloud.siliconflow.cn"
    },
    "custom": {
        "name": "Custom",
        "name_cn": "自定义 API",
        "default_model": "",
        "api_url": "",
        "api_key_hint": "输入你的 API Key",
        "models": [],
        "official_url": ""
    }
}


@dataclass
class LLMConfig:
    """LLM配置"""
    provider: str = "minimax"
    api_key: str = ""
    api_url: str = ""
    model: str = ""
    temperature: float = 0.7
    max_tokens: int = 4096


class LLMClient:
    """
    LLM API 客户端
    
    支持多种提供商，每个用户独立配置
    """
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.config = self._load_config()
    
    def _load_config(self) -> LLMConfig:
        """加载用户配置"""
        config = LLMConfig()
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    all_configs = json.load(f)
                    if self.user_id in all_configs:
                        cfg = all_configs[self.user_id]
                        config.provider = cfg.get("provider", "minimax")
                        config.api_key = cfg.get("api_key", "")
                        config.api_url = cfg.get("api_url", "")
                        config.model = cfg.get("model", "")
                        config.temperature = cfg.get("temperature", 0.7)
                        config.max_tokens = cfg.get("max_tokens", 4096)
            except Exception:
                pass
        
        # 设置默认值
        if not config.model or config.provider not in PROVIDERS:
            config.provider = "minimax"
            config.model = PROVIDERS["minimax"]["default_model"]
            config.api_url = PROVIDERS["minimax"]["api_url"]
        
        return config
    
    def _save_config(self) -> bool:
        """保存用户配置"""
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        
        all_configs = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    all_configs = json.load(f)
            except Exception:
                pass
        
        all_configs[self.user_id] = {
            "provider": self.config.provider,
            "api_key": self.config.api_key,
            "api_url": self.config.api_url,
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }
        
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(all_configs, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def configure(
        self,
        provider: str,
        api_key: str,
        model: Optional[str] = None,
        api_url: Optional[str] = None
    ) -> bool:
        """
        配置用户LLM设置
        
        Args:
            provider: 提供商ID
            api_key: API密钥
            model: 模型名称 (可选)
            api_url: API地址 (可选)
        
        Returns:
            是否配置成功
        """
        if provider not in PROVIDERS:
            return False
        
        self.config.provider = provider
        self.config.api_key = api_key
        self.config.api_url = api_url or PROVIDERS[provider]["api_url"]
        self.config.model = model or PROVIDERS[provider]["default_model"]
        
        return self._save_config()
    
    def configure_by_model_name(self, model_name: str, api_key: str) -> bool:
        """
        通过模型名称自动识别提供商并配置
        
        Args:
            model_name: 模型名称 (如 "gpt-4", "glm-4", "kimi")
            api_key: API密钥
        
        Returns:
            是否配置成功
        """
        # 自动识别提供商
        model_lower = model_name.lower()
        
        if "claude" in model_lower:
            provider = "claude"
        elif "gpt" in model_lower or "openai" in model_lower:
            provider = "openai"
        elif "glm" in model_lower:
            provider = "glm"
        elif "kimi" in model_lower or "moonshot" in model_lower:
            provider = "kimi"
        elif "qwen" in model_lower or "通义" in model_lower:
            provider = "qwen"
        elif "deepseek" in model_lower:
            provider = "deepseek"
        elif "minimax" in model_lower or "abab" in model_lower:
            provider = "minimax"
        else:
            # 尝试在所有提供商的模型中查找
            provider = None
            for p_id, p_info in PROVIDERS.items():
                for m in p_info.get("models", []):
                    if model_name.lower() in m["id"].lower():
                        provider = p_id
                        break
                if provider:
                    break
            
            if not provider:
                return False
        
        return self.configure(provider, api_key, model_name)
    
    def test_connection(self) -> Dict:
        """
        测试API连接
        
        Returns:
            {"success": True, "message": "..."} 或 {"success": False, "error": "..."}
        """
        if not self.config.api_key:
            return {
                "success": False,
                "error": "请先配置 API Key"
            }
        
        # 简单的连接测试
        result = self.chat([
            {"role": "user", "content": "Hi"}
        ], max_tokens=10)
        
        if "error" in result:
            return {
                "success": False,
                "error": result["error"]
            }
        
        return {
            "success": True,
            "message": f"连接 {self.get_provider_info()['name']} 成功！"
        }
    
    def get_info(self) -> Dict:
        """获取当前配置信息"""
        provider_info = PROVIDERS.get(self.config.provider, {})
        return {
            "provider": self.config.provider,
            "name": provider_info.get("name_cn", provider_info.get("name", "未知")),
            "model": self.config.model,
            "model_name": self._get_model_display_name(),
            "api_url": self.config.api_url,
            "has_api_key": bool(self.config.api_key),
            "is_configured": bool(self.config.api_key)
        }
    
    def _get_model_display_name(self) -> str:
        """获取模型显示名称"""
        provider_info = PROVIDERS.get(self.config.provider, {})
        for m in provider_info.get("models", []):
            if m["id"] == self.config.model:
                return m["name"]
        return self.config.model
    
    def get_provider_info(self) -> Dict:
        """获取提供商信息"""
        return PROVIDERS.get(self.config.provider, {})
    
    def chat(self, messages: List[Dict], **kwargs) -> Dict:
        """发送对话请求"""
        if not self.config.api_key:
            return {"error": "请先配置 API Key，使用【设置模型】命令"}
        
        temperature = kwargs.get("temperature", self.config.temperature)
        max_tokens = kwargs.get("max_tokens", self.config.max_tokens)
        
        if self.config.provider == "minimax":
            return self._chat_minimax(messages, temperature, max_tokens)
        elif self.config.provider == "openai":
            return self._chat_openai(messages, temperature, max_tokens)
        elif self.config.provider == "claude":
            return self._chat_claude(messages, temperature, max_tokens)
        elif self.config.provider == "glm":
            return self._chat_glm(messages, temperature, max_tokens)
        elif self.config.provider == "kimi":
            return self._chat_kimi(messages, temperature, max_tokens)
        elif self.config.provider == "qwen":
            return self._chat_qwen(messages, temperature, max_tokens)
        elif self.config.provider == "deepseek":
            return self._chat_deepseek(messages, temperature, max_tokens)
        elif self.config.provider == "siliconflow":
            return self._chat_siliconflow(messages, temperature, max_tokens)
        elif self.config.provider == "custom":
            return self._chat_custom(messages, temperature, max_tokens)
        else:
            return self._chat_openai(messages, temperature, max_tokens)
    
    def _chat_minimax(self, messages, temperature, max_tokens):
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        return self._post_request(self.config.api_url, headers, data)
    
    def _chat_openai(self, messages, temperature, max_tokens):
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        return self._post_request(self.config.api_url, headers, data)
    
    def _chat_claude(self, messages, temperature, max_tokens):
        headers = {
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        # Claude使用不同的消息格式
        claude_messages = []
        for msg in messages:
            role = "user" if msg.get("role") == "user" else "assistant"
            claude_messages.append({"role": role, "content": msg.get("content", "")})
        
        data = {
            "model": self.config.model,
            "messages": claude_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.config.api_url,
                headers=headers,
                json=data,
                timeout=60
            )
            result = response.json()
            
            if "error" in result:
                return result
            
            if "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    return {"content": content[0].get("text", ""), "usage": result.get("usage", {})}
                return {"content": str(content)}
            return {"error": "无法解析响应"}
        except Exception as e:
            return {"error": str(e)}
    
    def _chat_glm(self, messages, temperature, max_tokens):
        """智谱AI GLM"""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        return self._post_request(self.config.api_url, headers, data)
    
    def _chat_kimi(self, messages, temperature, max_tokens):
        """Kimi / Moonshot"""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        return self._post_request(self.config.api_url, headers, data)
    
    def _chat_qwen(self, messages, temperature, max_tokens):
        """通义千问"""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.model,
            "input": {"messages": messages},
            "parameters": {
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        }
        try:
            response = requests.post(
                self.config.api_url,
                headers=headers,
                json=data,
                timeout=60
            )
            result = response.json()
            if "error" in result:
                return result
            output = result.get("output", {})
            if "text" in output:
                return {"content": output["text"], "usage": result.get("usage", {})}
            return {"error": "无法解析响应"}
        except Exception as e:
            return {"error": str(e)}
    
    def _chat_deepseek(self, messages, temperature, max_tokens):
        """DeepSeek"""
        return self._chat_openai(messages, temperature, max_tokens)
    
    def _chat_siliconflow(self, messages, temperature, max_tokens):
        """硅基流动"""
        return self._chat_openai(messages, temperature, max_tokens)
    
    def _chat_custom(self, messages, temperature, max_tokens):
        """自定义API"""
        return self._chat_openai(messages, temperature, max_tokens)
    
    def _post_request(self, url, headers, data):
        """通用的POST请求"""
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            result = response.json()
            
            if "error" in result:
                return result
            
            choices = result.get("choices", [])
            if choices:
                return {
                    "content": choices[0].get("message", {}).get("content", ""),
                    "usage": result.get("usage", {})
                }
            return {"error": "无法解析响应"}
        except requests.exceptions.Timeout:
            return {"error": "请求超时，请检查网络"}
        except Exception as e:
            return {"error": str(e)}
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成内容的便捷方法"""
        result = self.chat([{"role": "user", "content": prompt}], **kwargs)
        if "error" in result:
            return f"[错误] {result['error']}"
        return result.get("content", "")


class LLMSetupWizard:
    """
    LLM设置向导 - 帮助小白用户配置API
    """
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.client = LLMClient(user_id)
    
    def get_welcome_message(self) -> str:
        """获取欢迎消息"""
        return """
🔧 **LLM 模型设置向导**

欢迎使用！我是你的健身教练 AI。

为了让教练能够为你制定个性化的训练计划，我需要连接一个大语言模型。

请告诉我你想使用哪个模型：

**常用推荐：**

1️⃣ **MiniMax** - 默认推荐，中文理解好
2️⃣ **OpenAI GPT-4** - 最强模型，需要魔法
3️⃣ **智谱 GLM** - 国产优秀，免费额度多
4️⃣ **Kimi** - 中文友好，支持长文本
5️⃣ **硅基流动** - 免费额度，性价比高

**其他选择：**
6️⃣ 通义千问 (Qwen)
7️⃣ DeepSeek
8️⃣ Claude

**回复示例：**
- "1" 或 "minimax"
- "gpt-4"
- "glm-4"
- "kimi"
- 或者直接告诉我你想要的模型名称

如果你已经有 API Key，可以直接发送给我，格式：
`API Key: sk-xxxxx`
`模型: gpt-4`

⚠️ 你的 API Key 仅存储在本地，不会上传到任何服务器。
"""
    
    def handle_setup(self, user_input: str) -> Dict:
        """
        处理用户输入
        
        Args:
            user_input: 用户输入
        
        Returns:
            {"next_step": "model_select"/"api_key"/"done", "message": "...", "data": {...}}
        """
        user_input = user_input.strip()
        
        # 检查是否是直接发送API Key
        if "sk-" in user_input or ":" in user_input:
            return self._parse_direct_api_key(user_input)
        
        # 数字映射
        number_map = {
            "1": "minimax",
            "2": "openai",
            "3": "glm",
            "4": "kimi",
            "5": "siliconflow",
            "6": "qwen",
            "7": "deepseek",
            "8": "claude"
        }
        if user_input in number_map:
            return self._show_provider_setup(number_map[user_input])
        
        # 关键词匹配
        keyword_to_provider = {
            "minimax": "minimax", "abab": "minimax",
            "openai": "openai", "gpt": "openai",
            "claude": "claude", "anthropic": "claude",
            "glm": "glm", "智谱": "glm", "zhipu": "glm",
            "kimi": "kimi", "moonshot": "kimi",
            "qwen": "qwen", "通义": "qwen", "阿里": "qwen",
            "deepseek": "deepseek",
            "siliconflow": "siliconflow", "硅基": "siliconflow"
        }
        
        user_lower = user_input.lower()
        for keyword, provider_id in keyword_to_provider.items():
            if keyword in user_lower:
                return self._show_provider_setup(provider_id)
        
        # 检查是否是模型名称（如 gpt-4, glm-4 等）
        model_keywords = ["gpt", "glm", "kimi", "claude", "qwen", "deepseek", "minimax", "abab", "moonshot"]
        if any(m in user_lower for m in model_keywords):
            self.client.configure_by_model_name(user_input, "")
            return {
                "next_step": "api_key",
                "message": f"好的，你选择了 {self.client.get_info()['model']}。\n\n请输入你的 API Key：\n{self.client.get_provider_info().get('api_key_hint', '')}",
                "data": {"provider": self.client.config.provider, "model": self.client.config.model}
            }
        
        # 默认显示选择
        return {
            "next_step": "provider_select",
            "message": self.get_welcome_message(),
            "data": {}
        }
    
    def _parse_direct_api_key(self, user_input: str) -> Dict:
        """解析直接的API Key输入"""
        api_key = ""
        model = ""
        
        # 解析格式
        if ":" in user_input:
            parts = user_input.split(":", 1)
            for part in parts:
                part = part.strip()
                if part.startswith("sk-"):
                    api_key = part
                elif part and not model:
                    model = part
        else:
            api_key = user_input.strip()
        
        if api_key:
            # 尝试自动识别模型
            if model:
                success = self.client.configure_by_model_name(model, api_key)
            else:
                # 使用当前配置
                success = bool(self.client.config.api_key)
                if success:
                    self.client.config.api_key = api_key
                    self.client._save_config()
            
            if success:
                # 测试连接
                test_result = self.client.test_connection()
                if test_result["success"]:
                    return {
                        "next_step": "done",
                        "message": f"✅ {test_result['message']}\n\n当前配置：\n- 提供商：{self.client.get_info()['name']}\n- 模型：{self.client.get_info()['model_name']}\n\n现在我可以为你制定训练计划了！",
                        "data": self.client.get_info()
                    }
                else:
                    return {
                        "next_step": "api_key",
                        "message": f"⚠️ API Key 已保存，但连接测试失败：{test_result['error']}\n\n请检查：\n1. API Key 是否正确\n2. 是否有足够的额度\n\n或者尝试其他模型？",
                        "data": self.client.get_info()
                    }
        
        return {
            "next_step": "api_key",
            "message": "请输入有效的 API Key",
            "data": {}
        }
    
    def _show_provider_setup(self, provider_id: str) -> Dict:
        """显示提供商设置"""
        provider = PROVIDERS.get(provider_id, {})
        
        models_text = ""
        if provider.get("models"):
            models_text = "\n可选模型：\n"
            for i, m in enumerate(provider["models"], 1):
                models_text += f"  {i}. {m['name']} - {m['desc']}\n"
        
        return {
            "next_step": "api_key",
            "message": f"""✅ 你选择了 **{provider.get('name_cn', provider.get('name'))}**

{models_text}

📝 请输入你的 API Key：
{provider.get('api_key_hint', '')}

💡 获取地址：{provider.get('official_url', '')}

直接发送 API Key 即可，例如：
`sk-xxxxxx`""",
            "data": {"provider": provider_id, "default_model": provider.get("default_model")}
        }
    
    def set_api_key(self, api_key: str) -> Dict:
        """设置API Key"""
        self.client.config.api_key = api_key
        self.client._save_config()
        
        # 测试连接
        test_result = self.client.test_connection()
        if test_result["success"]:
            return {
                "success": True,
                "message": f"✅ 配置成功！\n\n当前设置：\n- 提供商：{self.client.get_info()['name']}\n- 模型：{self.client.get_info()['model_name']}\n\n可以开始使用了！",
                "data": self.client.get_info()
            }
        else:
            return {
                "success": False,
                "error": test_result.get("error", "连接失败"),
                "message": f"⚠️ API Key 已保存，但连接失败：{test_result.get('error')}\n\n请检查：\n1. API Key 是否正确\n2. 是否有足够的额度"
            }
    
    def get_current_status(self) -> Dict:
        """获取当前状态"""
        info = self.client.get_info()
        if info["is_configured"]:
            return {
                "is_configured": True,
                "message": f"""✅ LLM 已配置完成

- 提供商：{info['name']}
- 模型：{info['model_name']}

可以直接使用教练功能！""",
                "data": info
            }
        else:
            return {
                "is_configured": False,
                "message": self.get_welcome_message(),
                "data": info
            }


def get_llm_client(user_id: str = "default") -> LLMClient:
    """获取LLM客户端"""
    return LLMClient(user_id)


def get_setup_wizard(user_id: str = "default") -> LLMSetupWizard:
    """获取设置向导"""
    return LLMSetupWizard(user_id)


if __name__ == "__main__":
    # 测试
    wizard = get_setup_wizard("test")
    print(wizard.get_welcome_message())
