from __future__ import annotations
"""
smart_config.py - 智能记忆配置

智能记忆系统的配置管理
- 个性化设置
- 触发规则配置
- 系统参数调整
"""

import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class SmartConfig:
    """
    智能记忆配置
    
    管理智能记忆系统的配置
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config", "smart_config.json")
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置
        
        Returns:
            dict: 配置字典
        """
        default_config = {
            "smart_memory": {
                "enabled": True,
                "silence_threshold": 600,  # 10分钟
                "short_conversation_threshold": 300,  # 5分钟
                "long_conversation_threshold": 1800,  # 30分钟
                "auto_record": False
            },
            "feeding_mode": {
                "enabled": True,
                "inactivity_threshold": 300,  # 5分钟
                "max_feed_duration": 3600,  # 1小时
                "auto_end": True
            },
            "welcome_guide": {
                "enabled": True,
                "show_on_first_use": True,
                "show_tips": True
            },
            "openclaw_integration": {
                "enabled": True,
                "sync_enabled": True,
                "sync_interval": 300,  # 5分钟
                "auto_connect": False
            },
            "memory": {
                "auto_cleanup": True,
                "cleanup_interval": 86400,  # 1天
                "max_memory_size": 10000
            },
            "ui": {
                "show_notifications": True,
                "show_stats": True,
                "theme": "light"
            }
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置
                self._merge_config(default_config, config)
                return default_config
            else:
                # 确保目录存在
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                # 保存默认配置
                self._save_config(default_config)
                return default_config
        except Exception as e:
            logger.warning("smart_config: %s", e)
            return default_config
    
    def _merge_config(self, default: Dict, custom: Dict):
        """
        合并配置
        
        Args:
            default: 默认配置
            custom: 自定义配置
        """
        for key, value in custom.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_config(default[key], value)
            else:
                default[key] = value
    
    def _save_config(self, config: Dict):
        """
        保存配置
        
        Args:
            config: 配置字典
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning("smart_config: %s", e)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置
        
        Args:
            key: 配置键（支持点号分隔）
            default: 默认值
        
        Returns:
            Any: 配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        设置配置
        
        Args:
            key: 配置键（支持点号分隔）
            value: 配置值
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config(self.config)
    
    def enable(self, feature: str):
        """
        启用功能
        
        Args:
            feature: 功能名称
        """
        self.set(f"{feature}.enabled", True)
    
    def disable(self, feature: str):
        """
        禁用功能
        
        Args:
            feature: 功能名称
        """
        self.set(f"{feature}.enabled", False)
    
    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置
        
        Returns:
            dict: 所有配置
        """
        return self.config
    
    def reset(self):
        """
        重置配置
        """
        default_config = {
            "smart_memory": {
                "enabled": True,
                "silence_threshold": 600,
                "short_conversation_threshold": 300,
                "long_conversation_threshold": 1800,
                "auto_record": False
            },
            "feeding_mode": {
                "enabled": True,
                "inactivity_threshold": 300,
                "max_feed_duration": 3600,
                "auto_end": True
            },
            "welcome_guide": {
                "enabled": True,
                "show_on_first_use": True,
                "show_tips": True
            },
            "openclaw_integration": {
                "enabled": True,
                "sync_enabled": True,
                "sync_interval": 300,
                "auto_connect": False
            },
            "memory": {
                "auto_cleanup": True,
                "cleanup_interval": 86400,
                "max_memory_size": 10000
            },
            "ui": {
                "show_notifications": True,
                "show_stats": True,
                "theme": "light"
            }
        }
        
        self.config = default_config
        self._save_config(default_config)
    
    def validate(self) -> bool:
        """
        验证配置
        
        Returns:
            bool: 配置是否有效
        """
        try:
            # 基本验证
            required_sections = ["smart_memory", "feeding_mode", "welcome_guide", "openclaw_integration", "memory", "ui"]
            for section in required_sections:
                if section not in self.config:
                    logger.warning(f"配置缺少 section: {section}")
                    return False
            
            # 数值验证
            thresholds = [
                ("smart_memory.silence_threshold", 60, 3600),
                ("smart_memory.short_conversation_threshold", 60, 1800),
                ("smart_memory.long_conversation_threshold", 300, 7200),
                ("feeding_mode.inactivity_threshold", 60, 1800),
                ("feeding_mode.max_feed_duration", 600, 14400),
                ("openclaw_integration.sync_interval", 60, 3600),
                ("memory.cleanup_interval", 3600, 604800),
                ("memory.max_memory_size", 100, 100000)
            ]
            
            for key, min_val, max_val in thresholds:
                value = self.get(key)
                if value < min_val or value > max_val:
                    logger.warning(f"配置 {key} 超出范围: {value} (范围: {min_val}-{max_val})")
                    return False
            
            return True
        except Exception as e:
            logger.warning("smart_config: %s", e)
            return False


def create_smart_config(config_path: str = None) -> SmartConfig:
    """
    创建智能配置实例
    
    Args:
        config_path: 配置文件路径
    
    Returns:
        SmartConfig: 智能配置实例
    """
    return SmartConfig(config_path)
