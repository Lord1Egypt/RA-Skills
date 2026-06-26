#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
starmemo v2.0 - AI 处理层
结构化提取 + 智能压缩 + 知识提取
"""
import os
import sys
import json
import re

# 自动安装依赖
def auto_install():
    try:
        import requests
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "requests"])
auto_install()

import requests


# 国内 LLM 预设配置
LLM_PRESET = {
    "huoshan": {
        "url": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "doubao-seed-code-preview-251028"
    },
    "tongyi": {
        "url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-turbo"
    },
    "wenxin": {
        "url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat",
        "model": "ernie-lite-8k"
    },
    "deepseek": {
        "url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat"
    },
    "zhipu": {
        "url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-4-flash"
    },
    "xinghuo": {
        "url": "https://spark-api-open.xf-yun.com/v1",
        "model": "generalv3.5"
    },
    "hunyuan": {
        "url": "https://hunyuan.tencentcloudapi.com/v1",
        "model": "hunyuan-lite"
    }
}


class AIProcessor:
    """AI 处理器 - 结构化提取、压缩、知识提取"""
    
    def __init__(self, api_key: str = "", base_url: str = "", model: str = "", 
                 enable_ai: bool = True, temperature: float = 0.3):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.enable_ai = enable_ai and bool(api_key)
        self.temperature = temperature
        self.api_endpoint = f"{base_url.rstrip('/')}/chat/completions" if base_url else ""
    
    def _call_llm(self, prompt: str, max_tokens: int = 500) -> str:
        """调用 LLM"""
        if not self.enable_ai:
            return ""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": max_tokens
        }
        
        try:
            res = requests.post(self.api_endpoint, headers=headers, json=data, timeout=15)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"⚠️ LLM 调用失败: {e}")
            return ""
    
    def extract_structured(self, text: str) -> dict:
        """
        从文本提取结构化记忆（因→改→待）
        
        Returns:
            dict: {cause, change, todo, topic}
        """
        if not self.enable_ai:
            # 无 AI 时简单处理
            return {
                "cause": text[:100],
                "change": text[:200],
                "todo": "",
                "topic": "日常记录"
            }
        
        prompt = f"""分析以下文本，提取结构化记忆信息。严格按照JSON格式返回。

文本：
{text[:1000]}

返回格式：
{{
    "topic": "主题（2-5字）",
    "cause": "原因/背景（一句话）",
    "change": "做了什么/改了什么（一句话）",
    "todo": "待办/后续（可为空）"
}}

只返回JSON，不要其他内容。"""

        result = self._call_llm(prompt, max_tokens=300)
        
        try:
            # 提取 JSON
            json_match = re.search(r'\{[^}]+\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # 降级处理
        return {
            "cause": text[:100],
            "change": text[:200],
            "todo": "",
            "topic": "日常记录"
        }
    
    def compress(self, text: str, max_len: int = 200) -> str:
        """压缩文本，保留核心信息"""
        if len(text) <= max_len:
            return text
        
        if not self.enable_ai:
            return text[:max_len]
        
        prompt = f"精简以下内容，保留核心信息，不超过{max_len}字：\n\n{text}"
        result = self._call_llm(prompt, max_tokens=max_len * 2)
        return result[:max_len] if result else text[:max_len]
    
    def extract_knowledge(self, text: str) -> list:
        """
        从文本提取知识点
        
        Returns:
            list: [{key, content}, ...]
        """
        if not self.enable_ai:
            return []
        
        prompt = f"""从以下文本中提取有价值的知识点。每个知识点包含标题和内容。

文本：
{text[:2000]}

返回JSON数组格式：
[
    {{"key": "知识点标题", "content": "知识点内容（详细）"}},
    ...
]

如果没有有价值的知识点，返回空数组 []。
只返回JSON，不要其他内容。"""

        result = self._call_llm(prompt, max_tokens=800)
        
        try:
            # 提取 JSON 数组
            json_match = re.search(r'\[[\s\S]*\]', result)
            if json_match:
                knowledge_list = json.loads(json_match.group())
                return knowledge_list if isinstance(knowledge_list, list) else []
        except:
            pass
        
        return []
    
    def clarify(self, user_input: str, memory: str) -> str:
        """生成澄清问题"""
        if not self.enable_ai:
            return "请补充更多信息。"
        
        prompt = f"""用户问题：{user_input[:500]}
相关记忆（可能不准确）：{memory[:300]}

记忆不足以回答问题，请生成1-2个澄清问题，帮助理解用户需求。
要求：简洁自然，不超过80字。"""
        
        return self._call_llm(prompt, max_tokens=100) or "请补充更多信息。"
    
    def answer_with_memory(self, user_input: str, memory: str) -> str:
        """基于记忆回答"""
        if not self.enable_ai:
            return memory[:200]
        
        prompt = f"""基于以下记忆回答用户问题。简洁准确，不超过200字。

记忆：{memory[:500]}

用户问题：{user_input[:300]}

回答："""
        
        return self._call_llm(prompt, max_tokens=250) or memory[:200]


class MessageCleaner:
    """消息清洗工具"""
    
    @staticmethod
    def clean(text: str) -> str:
        """清洗消息文本"""
        if not isinstance(text, str):
            return ""
        
        # 移除 @ 人
        text = re.sub(r"<at.*?>.*?</at>", " ", text)
        # 移除 CQ 码
        text = re.sub(r"\[CQ:.*?\]", " ", text)
        # 移除 @用户名
        text = re.sub(r"@\S+", " ", text)
        # 合并空白
        text = re.sub(r"\s+", " ", text)
        
        return text.strip()
    
    @staticmethod
    def is_config_command(text: str) -> bool:
        """判断是否为配置指令"""
        return text.strip().startswith("记忆配置")


class ConfigManager:
    """配置管理"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.api_key = ""
        self.base_url = ""
        self.model = ""
        self.enable_ai = False
        self.persist_key = False
        self.allow_web_fetch = False
        self.temperature = 0.3
        self.archive_days = 3
        
        self.load()
    
    def load(self):
        """加载配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                self.api_key = data.get("api_key", "")
                self.base_url = data.get("base_url", "")
                self.model = data.get("model_name", "")
                self.enable_ai = data.get("enable_ai", False)
                self.persist_key = data.get("persist_key", False)
                self.allow_web_fetch = data.get("allow_web_fetch", False)
                self.temperature = data.get("temperature", 0.3)
                self.archive_days = data.get("archive_days", 3)
            except:
                pass
    
    def save(self):
        """保存配置"""
        data = {
            "api_key": self.api_key if self.persist_key else "",
            "base_url": self.base_url,
            "model_name": self.model,
            "enable_ai": self.enable_ai,
            "persist_key": self.persist_key,
            "allow_web_fetch": self.allow_web_fetch,
            "temperature": self.temperature,
            "archive_days": self.archive_days
        }
        
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        os.chmod(self.config_path, 0o600)
    
    def set_llm(self, llm_key: str, api_key: str = None):
        """设置 LLM"""
        if llm_key in LLM_PRESET:
            self.base_url = LLM_PRESET[llm_key]["url"]
            self.model = LLM_PRESET[llm_key]["model"]
        
        if api_key:
            self.api_key = api_key
        
        self.enable_ai = bool(self.api_key)
        self.save()
