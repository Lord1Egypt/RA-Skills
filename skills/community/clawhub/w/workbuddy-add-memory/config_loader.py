#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强配置加载器 v3.0
作者: zcg007
日期: 2026-03-15

支持多层级配置、验证和智能合并
"""

import os
import json
import yaml
import toml
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    """增强配置加载器"""
    
    def __init__(self, config_dir: str = None):
        """
        初始化配置加载器
        
        Args:
            config_dir: 配置目录路径，默认为技能目录下的config子目录
        """
        if config_dir is None:
            # 默认配置目录：技能目录下的config子目录
            self.config_dir = Path(__file__).parent / "config"
        else:
            self.config_dir = Path(config_dir)
        
        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置缓存
        self._config_cache = {}
        
        # 默认配置
        self.default_config = {
            "memory_sources": [
                "~/.workbuddy/global_summaries/",
                "~/.workbuddy/unified_memory/",
                "~/.workbuddy/skills/",
                "~/.workbuddy/learnings/",
            ],
            "retrieval_config": {
                "max_results": 15,
                "min_relevance": 0.3,
                "weight_keyword": 0.6,
                "weight_semantic": 0.4,
                "boost_recent": 0.2,
                "boost_importance": 0.3,
                "cache_size": 1000,
                "cache_ttl": 3600,  # 1小时
            },
            "detection_config": {
                "task_keywords": {
                    "excel": ["excel", "表格", "报表", "预算", "财务", "数据"],
                    "analysis": ["分析", "统计", "报告", "总结", "评估"],
                    "skill": ["技能", "skill", "安装", "开发", "创建"],
                    "memory": ["记忆", "记忆", "经验", "学习", "总结"],
                    "workflow": ["工作流", "流程", "自动化", "任务"],
                },
                "min_confidence": 0.5,
                "context_window": 5,  # 上下文窗口大小
                "enable_intent_detection": True,
            },
            "ui_config": {
                "output_format": "markdown",
                "max_display_items": 10,
                "show_relevance_scores": True,
                "group_by_category": True,
                "color_scheme": "default",
            },
            "system_config": {
                "auto_update_interval": 300,  # 5分钟
                "max_file_size": 10485760,  # 10MB
                "enable_logging": True,
                "log_level": "INFO",
                "backup_enabled": True,
                "backup_count": 5,
            },
        }
    
    def load_config(self, config_name: str = "main") -> Dict[str, Any]:
        """
        加载配置，支持多层级合并
        
        Args:
            config_name: 配置名称，对应config目录下的{config_name}.yaml文件
            
        Returns:
            合并后的配置字典
        """
        if config_name in self._config_cache:
            return self._config_cache[config_name]
        
        # 1. 从默认配置开始
        config = self.default_config.copy()
        
        # 2. 加载用户配置文件（如果存在）
        config_files = [
            self.config_dir / f"{config_name}.yaml",
            self.config_dir / f"{config_name}.json",
            self.config_dir / f"{config_name}.toml",
            self.config_dir / f"{config_name}.yml",
        ]
        
        user_config = {}
        for config_file in config_files:
            if config_file.exists():
                try:
                    user_config = self._load_file(config_file)
                    logger.info(f"加载配置文件: {config_file}")
                    break
                except Exception as e:
                    logger.warning(f"加载配置文件失败 {config_file}: {e}")
        
        # 3. 深度合并配置
        config = self._deep_merge(config, user_config)
        
        # 4. 加载环境变量覆盖
        env_config = self._load_env_vars()
        config = self._deep_merge(config, env_config)
        
        # 5. 验证配置
        self._validate_config(config)
        
        # 6. 缓存配置
        self._config_cache[config_name] = config
        
        return config
    
    def _load_file(self, file_path: Path) -> Dict[str, Any]:
        """加载配置文件"""
        suffix = file_path.suffix.lower()
        
        if suffix in ['.yaml', '.yml']:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        elif suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif suffix == '.toml':
            with open(file_path, 'r', encoding='utf-8') as f:
                return toml.load(f)
        else:
            raise ValueError(f"不支持的配置文件格式: {suffix}")
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """深度合并两个字典"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _load_env_vars(self) -> Dict[str, Any]:
        """从环境变量加载配置"""
        env_config = {}
        prefix = "WORKBUDDY_MEMORY_"
        
        for key, value in os.environ.items():
            if key.startswith(prefix):
                # 转换环境变量名：WORKBUDDY_MEMORY_MAX_RESULTS -> max_results
                config_key = key[len(prefix):].lower()
                
                # 尝试转换值类型
                try:
                    # 尝试转换为整数
                    converted_value = int(value)
                except ValueError:
                    try:
                        # 尝试转换为浮点数
                        converted_value = float(value)
                    except ValueError:
                        # 尝试转换为布尔值
                        if value.lower() in ['true', 'yes', '1']:
                            converted_value = True
                        elif value.lower() in ['false', 'no', '0']:
                            converted_value = False
                        else:
                            # 保持字符串
                            converted_value = value
                
                # 支持嵌套配置：MAX_RESULTS -> retrieval_config.max_results
                if '_' in config_key:
                    parts = config_key.split('_')
                    current = env_config
                    for part in parts[:-1]:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    current[parts[-1]] = converted_value
                else:
                    env_config[config_key] = converted_value
        
        return env_config
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """验证配置的有效性"""
        # 验证内存源配置
        if "memory_sources" in config:
            if not isinstance(config["memory_sources"], list):
                raise ValueError("memory_sources必须是列表")
            
            # 展开路径中的~符号
            for i, source in enumerate(config["memory_sources"]):
                if isinstance(source, str):
                    config["memory_sources"][i] = os.path.expanduser(source)
        
        # 验证检索配置
        if "retrieval_config" in config:
            rc = config["retrieval_config"]
            if "max_results" in rc and rc["max_results"] <= 0:
                raise ValueError("max_results必须大于0")
            if "min_relevance" in rc and not (0 <= rc["min_relevance"] <= 1):
                raise ValueError("min_relevance必须在0到1之间")
        
        # 记录验证成功
        logger.debug("配置验证通过")
    
    def save_config(self, config: Dict[str, Any], config_name: str = "main") -> None:
        """
        保存配置到文件
        
        Args:
            config: 配置字典
            config_name: 配置名称
        """
        config_file = self.config_dir / f"{config_name}.yaml"
        
        # 确保目录存在
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存配置
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        # 清除缓存
        if config_name in self._config_cache:
            del self._config_cache[config_name]
        
        logger.info(f"配置已保存到: {config_file}")
    
    def get_memory_sources(self) -> List[str]:
        """获取内存源路径列表"""
        config = self.load_config()
        return config.get("memory_sources", [])
    
    def get_retrieval_config(self) -> Dict[str, Any]:
        """获取检索配置"""
        config = self.load_config()
        return config.get("retrieval_config", {})
    
    def get_detection_config(self) -> Dict[str, Any]:
        """获取检测配置"""
        config = self.load_config()
        return config.get("detection_config", {})
    
    def get_ui_config(self) -> Dict[str, Any]:
        """获取UI配置"""
        config = self.load_config()
        return config.get("ui_config", {})
    
    def reload_config(self, config_name: str = "main") -> None:
        """重新加载配置"""
        if config_name in self._config_cache:
            del self._config_cache[config_name]
        self.load_config(config_name)


# 全局配置实例
config_loader = ConfigLoader()


if __name__ == "__main__":
    # 测试配置加载器
    loader = ConfigLoader()
    config = loader.load_config()
    
    print("=== 配置加载测试 ===")
    print(f"内存源数量: {len(config['memory_sources'])}")
    print(f"最大检索结果数: {config['retrieval_config']['max_results']}")
    print(f"最小相关性阈值: {config['retrieval_config']['min_relevance']}")
    
    # 测试保存配置
    test_config = config.copy()
    test_config["retrieval_config"]["max_results"] = 20
    loader.save_config(test_config, "test")
    
    print("\n=== 配置保存测试完成 ===")