"""配置管理模块 - 统一管理配置文件"""

import json
import os
from typing import Any, Optional
from dataclasses import dataclass, field

SKILL_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@dataclass
class LLMConfig:
    enabled: bool = False
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o-mini"
    timeout: int = 30
    retries: int = 2

@dataclass
class NotifyConfig:
    type: str = "terminal"
    webhook_url: str = ""

@dataclass
class AppConfig:
    llm: LLMConfig = field(default_factory=LLMConfig)
    notify: NotifyConfig = field(default_factory=NotifyConfig)
    fetch_interval_days: int = 7

class ConfigManager:
    def __init__(self, config_path: Optional[str] = None) -> None:
        self.config_path: str = config_path or os.path.join(SKILL_DIR, "config.json")
        self._config: Optional[AppConfig] = None
    
    def load(self) -> AppConfig:
        """加载配置"""
        if self._config is not None:
            return self._config
        
        default_config = AppConfig()
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    data: dict[str, Any] = json.load(f)
                
                # 解析LLM配置
                llm_data: dict[str, Any] = data.get("llm", {})
                llm_config = LLMConfig(
                    enabled=llm_data.get("enabled", default_config.llm.enabled),
                    base_url=llm_data.get("base_url", default_config.llm.base_url),
                    model=llm_data.get("model", default_config.llm.model),
                    timeout=llm_data.get("timeout", default_config.llm.timeout),
                    retries=llm_data.get("retries", default_config.llm.retries),
                )
                
                # 解析通知配置
                notify_data: dict[str, Any] = data.get("notify", {})
                notify_config = NotifyConfig(
                    type=notify_data.get("type", default_config.notify.type),
                    webhook_url=notify_data.get("webhook_url", default_config.notify.webhook_url),
                )
                
                self._config = AppConfig(
                    llm=llm_config,
                    notify=notify_config,
                    fetch_interval_days=data.get("fetch_interval_days", default_config.fetch_interval_days),
                )
            except (json.JSONDecodeError, OSError) as e:
                print(f"配置文件加载失败: {e}，使用默认配置")
                self._config = default_config
        else:
            self._config = default_config
        
        return self._config
    
    def save(self, config: AppConfig) -> None:
        """保存配置"""
        data: dict[str, Any] = {
            "llm": {
                "enabled": config.llm.enabled,
                "base_url": config.llm.base_url,
                "model": config.llm.model,
                "timeout": config.llm.timeout,
                "retries": config.llm.retries,
            },
            "notify": {
                "type": config.notify.type,
                "webhook_url": config.notify.webhook_url,
            },
            "fetch_interval_days": config.fetch_interval_days,
        }
        
        with open(self.config_path, "w") as f:
            json.dump(data, f, indent=2)
        
        self._config = config
    
    def get_llm_api_key(self) -> Optional[str]:
        """获取LLM API Key"""
        env_path: str = os.path.join(SKILL_DIR, ".env")
        if not os.path.exists(env_path):
            return None
        
        try:
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    k, _, v = line.partition("=")
                    if k.strip() == "LLM_API_KEY":
                        val: str = v.strip().strip("\"'")
                        return val if val else None
        except (OSError, UnicodeDecodeError):
            return None
