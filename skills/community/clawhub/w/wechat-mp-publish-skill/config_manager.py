#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一配置管理器
集中管理所有配置，支持环境变量替换、配置验证、权限设置
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict:
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        # 尝试主配置文件
        if self.config_path.exists():
            config_file = self.config_path
        else:
            # 回退到示例配置
            example_path = self.config_path.parent / "config.example.yaml"
            if example_path.exists():
                config_file = example_path
                logger.warning(f"主配置文件不存在，使用示例配置：{example_path}")
            else:
                raise FileNotFoundError(f"配置文件不存在：{self.config_path}")
        
        # 加载 YAML
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 环境变量替换
        self._substitute_env(config)
        
        # 设置配置文件权限（如果文件是新创建的）
        try:
            os.chmod(config_file, 0o600)
        except Exception as e:
            logger.warning(f"设置配置文件权限失败：{e}")
        
        return config
    
    def _substitute_env(self, config):
        """
        递归替换配置中的环境变量
        
        支持格式：
        - ${VAR_NAME} - 替换为环境变量
        - ${VAR_NAME:default} - 如果环境变量不存在，使用默认值
        
        Args:
            config: 配置字典（原地修改）
        """
        if isinstance(config, dict):
            for key, value in list(config.items()):
                if isinstance(value, str):
                    config[key] = self._replace_env_var(value)
                elif isinstance(value, (dict, list)):
                    self._substitute_env(value)
        elif isinstance(config, list):
            for i, item in enumerate(config):
                if isinstance(item, str):
                    config[i] = self._replace_env_var(item)
                elif isinstance(item, (dict, list)):
                    self._substitute_env(item)
    
    def _replace_env_var(self, value: str) -> str:
        """
        替换单个字符串中的环境变量
        
        Args:
            value: 原始字符串
            
        Returns:
            替换后的字符串
        """
        import re
        
        # 匹配 ${VAR_NAME} 或 ${VAR_NAME:default}
        pattern = r'\$\{([^}:]+)(?::([^}]*))?\}'
        
        def replacer(match):
            var_name = match.group(1)
            default_value = match.group(2)
            
            env_value = os.environ.get(var_name)
            
            if env_value is not None:
                return env_value
            elif default_value is not None:
                return default_value
            else:
                # 环境变量不存在且没有默认值，保留原样
                return match.group(0)
        
        return re.sub(pattern, replacer, value)
    
    def _validate_config(self):
        """
        验证配置的有效性
        
        Raises:
            ValueError: 配置无效时抛出
        """
        # 验证必需的配置项
        required_keys = ['wechat', 'image']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"缺少必需的配置项：{key}")
        
        # 验证微信公众号配置
        wechat_config = self.config.get('wechat', {})
        required_wechat_keys = ['appid', 'appsecret']
        for key in required_wechat_keys:
            if key not in wechat_config:
                raise ValueError(f"缺少微信公众号配置：{key}")
            if not wechat_config[key] or wechat_config[key].startswith('your-') or wechat_config[key].startswith('sk-your-'):
                logger.warning(f"微信公众号配置 {key} 可能未正确设置")
        
        # 验证图片源配置
        image_config = self.config.get('image', {})
        providers = image_config.get('providers', {})
        
        # 检查至少有一个图片源启用
        enabled_providers = [
            name for name, cfg in providers.items() 
            if isinstance(cfg, dict) and cfg.get('enabled', False)
        ]
        
        if not enabled_providers:
            logger.warning("没有启用的图片源，将只能使用占位图")
        
        logger.info(f"配置验证通过 - 启用的图片源：{enabled_providers}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项（支持点分隔的路径）
        
        Args:
            key: 配置键（如 'wechat.appid'）
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_wechat_config(self) -> Dict:
        """获取微信公众号配置"""
        return self.config.get('wechat', {})
    
    def get_image_config(self) -> Dict:
        """获取图片生成配置"""
        return self.config.get('image', {})
    
    def get_provider_config(self, provider_name: str) -> Dict:
        """
        获取指定图片源的配置
        
        Args:
            provider_name: 图片源名称（如 'unsplash', 'tongyi-wanxiang'）
            
        Returns:
            图片源配置
        """
        providers = self.config.get('image', {}).get('providers', {})
        return providers.get(provider_name, {})
    
    def is_provider_enabled(self, provider_name: str) -> bool:
        """
        检查图片源是否启用
        
        Args:
            provider_name: 图片源名称
            
        Returns:
            True 如果启用
        """
        provider_config = self.get_provider_config(provider_name)
        return provider_config.get('enabled', False)
    
    def to_dict(self) -> Dict:
        """
        获取完整配置字典
        
        Returns:
            配置字典
        """
        return self.config
    
    def __getitem__(self, key: str) -> Any:
        """支持字典式访问"""
        return self.get(key)
    
    def __contains__(self, key: str) -> bool:
        """支持 in 操作符"""
        try:
            return self.get(key) is not None
        except:
            return False


# 全局配置管理器实例
_global_config: Optional[ConfigManager] = None


def get_config(config_path: str = "config.yaml") -> ConfigManager:
    """
    获取全局配置管理器实例
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置管理器实例
    """
    global _global_config
    if _global_config is None:
        _global_config = ConfigManager(config_path)
    return _global_config


def test_config():
    """测试配置管理器"""
    print("测试配置管理器")
    print("=" * 50)
    
    config = get_config()
    
    print(f"公众号名称：{config.get('wechat.name')}")
    print(f"AppID: {config.get('wechat.appid')}")
    print(f"图片源优先级：{config.get('image.provider_priority')}")
    
    # 测试图片源配置
    for provider in ['unsplash', 'tongyi-wanxiang', 'baidu-yige', 'dall-e-3']:
        enabled = config.is_provider_enabled(provider)
        limit = config.get(f'image.providers.{provider}.monthly_limit', '无限制')
        print(f"{provider}: 启用={enabled}, 限额={limit}")
    
    print("=" * 50)
    print("配置验证通过！")


if __name__ == "__main__":
    test_config()
