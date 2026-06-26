# -*- coding: utf-8 -*-
"""
Skill 配置管理模块
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class SkillConfig:
    """
    Skill 配置类，从环境变量或 Skill 配置系统中读取配置
    """
    
    def __init__(self):
        # 从 OpenClaw 配置系统获取配置
        # 本地开发时从环境变量读取
        self.llm_api_key = self._get_config("LLM_API_KEY", os.getenv("llm_api_key", ""))
        self.llm_base_url = self._get_config("LLM_BASE_URL", os.getenv("llm_base_url", "https://api.openai.com/v1"))
        self.llm_model = self._get_config("LLM_MODEL", os.getenv("llm_model", "gpt-3.5-turbo"))
        
        self.baidu_search_api_key = self._get_config("BAIDU_SEARCH_API_KEY", os.getenv("baidu_search_api_key", ""))
        self.baidu_search_secret_key = self._get_config("BAIDU_SEARCH_SECRET_KEY", os.getenv("baidu_search_secret_key", ""))
        
        self.cache_duration = int(self._get_config("CACHE_DURATION", os.getenv("cache_duration", "24")))
        self.default_language = self._get_config("DEFAULT_LANGUAGE", os.getenv("default_language", "zh-CN"))
        self.push_channel = self._get_config("PUSH_CHANNEL", os.getenv("push_channel", "current"))
        self.cost_alert_threshold = float(self._get_config("COST_ALERT_THRESHOLD", os.getenv("cost_alert_threshold", "10.0")))
        self.auto_clear_cache = self._get_config("AUTO_CLEAR_CACHE", os.getenv("auto_clear_cache", "True")).lower() == "true"
        
        # 验证必填配置
        self._validate_config()
    
    def _get_config(self, key: str, default: Any = None) -> Any:
        """
        获取配置值，优先从 OpenClaw 配置系统获取，否则使用默认值
        """
        # OpenClaw Skill 运行时会将配置注入到环境变量中，使用 skill_config_ 前缀
        env_key = f"SKILL_CONFIG_{key.upper()}"
        return os.getenv(env_key, default)
    
    def _validate_config(self) -> None:
        """
        验证必填配置是否存在
        """
        missing = []
        
        if not self.llm_api_key:
            missing.append("大模型 API Key")
        
        if not self.baidu_search_api_key:
            missing.append("百度搜索 API Key")
        
        if not self.baidu_search_secret_key:
            missing.append("百度搜索 Secret Key")
        
        if missing and not os.getenv("TEST_MODE", "").lower() == "true":
            raise ValueError(f"缺少必填配置项：{', '.join(missing)}\n请在 Skill 配置页面填写完整信息后再使用。")
    
    def is_config_complete(self) -> bool:
        """
        检查配置是否完整
        """
        try:
            self._validate_config()
            return True
        except ValueError:
            return False
    
    def get_llm_config(self) -> Dict[str, str]:
        """
        获取大模型配置
        """
        return {
            "api_key": self.llm_api_key,
            "base_url": self.llm_base_url,
            "model": self.llm_model
        }
    
    def get_baidu_search_config(self) -> Dict[str, str]:
        """
        获取百度搜索配置
        """
        return {
            "api_key": self.baidu_search_api_key,
            "secret_key": self.baidu_search_secret_key
        }
    
    def mask_sensitive_data(self, data: str) -> str:
        """
        敏感数据掩码处理，只显示前4位和后4位
        """
        if not data or len(data) < 8:
            return "***"
        return f"{data[:4]}****{data[-4:]}"
    
    def __str__(self) -> str:
        """
        字符串表示，掩码敏感数据
        """
        return f"SkillConfig(llm_api_key={self.mask_sensitive_data(self.llm_api_key)}, baidu_api_key={self.mask_sensitive_data(self.baidu_search_api_key)})"
    
    def __repr__(self) -> str:
        return self.__str__()
