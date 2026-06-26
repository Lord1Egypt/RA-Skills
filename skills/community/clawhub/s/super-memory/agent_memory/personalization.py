"""
personalization.py - 个性化设置系统

功能：
1. 允许用户自定义界面设置
2. 允许用户自定义系统偏好
3. 支持设置的保存和加载
4. 提供默认设置
5. 支持多用户设置

使用方式：
    from personalization import PersonalizationManager
    personalization = PersonalizationManager()
    
    # 获取用户设置
    settings = personalization.get_settings(user_id="user123")
    
    # 更新用户设置
    personalization.update_settings(user_id="user123", settings={"theme": "dark"})
"""

from __future__ import annotations

import os
import sys
import logging
import json
import threading
from typing import Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class PersonalizationManager:
    """个性化设置管理器"""
    
    def __init__(self, settings_dir: str = None):
        """
        初始化个性化设置管理器
        
        Args:
            settings_dir: 设置文件存储目录
        """
        self.settings_dir = settings_dir or os.path.join(os.path.dirname(__file__), "data", "personalization")
        self.settings_file = os.path.join(self.settings_dir, "settings.json")
        self._lock = threading.Lock()
        self._settings_cache: Dict[str, Dict] = {}
        
        # 确保设置目录存在
        os.makedirs(self.settings_dir, exist_ok=True)
        
        # 加载设置
        self._load_settings()
    
    def _load_settings(self):
        """加载设置"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self._settings_cache = json.load(f)
                logger.info("个性化设置加载成功")
            else:
                # 初始化默认设置
                self._settings_cache = {}
                logger.info("个性化设置文件不存在，使用默认设置")
        except Exception as e:
            logger.error(f"加载个性化设置失败: {e}")
            self._settings_cache = {}
    
    def _save_settings(self):
        """保存设置"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self._settings_cache, f, ensure_ascii=False, indent=2)
            logger.info("个性化设置保存成功")
        except Exception as e:
            logger.error(f"保存个性化设置失败: {e}")
    
    def get_default_settings(self) -> Dict[str, Any]:
        """
        获取默认设置
        
        Returns:
            Dict: 默认设置
        """
        return {
            "interface": {
                "theme": "light",  # light, dark, system
                "language": "zh",  # zh, en
                "font_size": 14,  # 字体大小
                "font_family": "system",  # 字体家族
                "sidebar": {
                    "visible": True,  # 侧边栏是否可见
                    "width": 250,  # 侧边栏宽度
                    "collapsed": False  # 侧边栏是否折叠
                },
                "notifications": {
                    "enabled": True,  # 通知是否启用
                    "sound": False,  # 通知声音
                    "popup": True  # 弹出通知
                }
            },
            "system": {
                "auto_save": True,  # 自动保存
                "backup_frequency": "daily",  # 备份频率: daily, weekly, monthly
                "max_backups": 10,  # 最大备份数量
                "default_importance": "medium",  # 默认重要度
                "auto_cleanup": True,  # 自动清理
                "cleanup_frequency": "weekly",  # 清理频率
                "retention_days": 30  # 数据保留天数
            },
            "search": {
                "default_limit": 50,  # 默认搜索结果数量
                "enable_semantic": True,  # 启用语义搜索
                "enable_fts": True,  # 启用全文搜索
                "sort_by": "time",  # 排序方式: time, relevance, importance
                "show_preview": True  # 显示预览
            },
            "memory": {
                "enable_deduplication": True,  # 启用去重
                "enable_compression": True,  # 启用压缩
                "enable_decay": True,  # 启用记忆衰减
                "decay_rate": 0.01,  # 衰减率
                "min_importance": "low"  # 最小重要度
            },
            "notifications": {
                "enable_email": False,  # 启用邮件通知
                "email": "",  # 邮箱地址
                "enable_push": False,  # 启用推送通知
                "push_token": ""  # 推送令牌
            },
            "llm": {
                "model": "default",  # 模型名称
                "temperature": 0.7,  # 温度
                "max_tokens": 1000,  # 最大令牌数
                "top_p": 0.9  # 采样概率
            }
        }
    
    def get_settings(self, user_id: str = "default") -> Dict[str, Any]:
        """
        获取用户设置

        ⚠️ 安全: 返回设置时会将 llm.api_key 替换为 api_key_configured 布尔标志，
        避免通过 API 泄漏实际密钥。

        Args:
            user_id: 用户ID

        Returns:
            Dict: 用户设置（api_key 已脱敏）
        """
        with self._lock:
            if user_id not in self._settings_cache:
                self._settings_cache[user_id] = self.get_default_settings()
                self._save_settings()
            result = self._settings_cache[user_id].copy()
            # security: never return the actual API key through the API
            if "llm" in result and isinstance(result["llm"], dict):
                raw_key = result["llm"].get("api_key", "")
                result["llm"] = dict(result["llm"])
                result["llm"]["api_key_configured"] = bool(raw_key)
                result["llm"].pop("api_key", None)
            return result
    
    def update_settings(self, settings: Dict[str, Any], user_id: str = "default") -> bool:
        """
        更新用户设置
        
        Args:
            settings: 要更新的设置
            user_id: 用户ID
        
        Returns:
            bool: 是否更新成功
        """
        try:
            with self._lock:
                current_settings = self._settings_cache.get(user_id, self.get_default_settings())
                # security: if api_key is empty/absent in update, preserve the existing key
                if "llm" in settings and isinstance(settings["llm"], dict):
                    existing_key = current_settings.get("llm", {}).get("api_key", "")
                    new_key = settings["llm"].get("api_key", "")
                    if not new_key and existing_key:
                        settings["llm"]["api_key"] = existing_key
                self._update_recursive(current_settings, settings)
                self._save_settings()
                
            logger.info(f"用户 {user_id} 的个性化设置更新成功")
            return True
        except Exception as e:
            logger.error(f"更新用户 {user_id} 的个性化设置失败: {e}")
            return False
    
    def _update_recursive(self, current: Dict[str, Any], update: Dict[str, Any]):
        """
        递归更新设置
        
        Args:
            current: 当前设置
            update: 要更新的设置
        """
        for key, value in update.items():
            if key in current and isinstance(current[key], dict) and isinstance(value, dict):
                # 递归更新嵌套字典
                self._update_recursive(current[key], value)
            else:
                # 直接更新值
                current[key] = value
    
    def reset_settings(self, user_id: str = "default") -> bool:
        """
        重置用户设置为默认值
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 是否重置成功
        """
        try:
            with self._lock:
                self._settings_cache[user_id] = self.get_default_settings()
                self._save_settings()
            logger.info(f"用户 {user_id} 的个性化设置已重置为默认值")
            return True
        except Exception as e:
            logger.error(f"重置用户 {user_id} 的个性化设置失败: {e}")
            return False
    
    def delete_settings(self, user_id: str) -> bool:
        """
        删除用户设置
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 是否删除成功
        """
        try:
            with self._lock:
                if user_id in self._settings_cache:
                    del self._settings_cache[user_id]
                    self._save_settings()
            logger.info(f"用户 {user_id} 的个性化设置已删除")
            return True
        except Exception as e:
            logger.error(f"删除用户 {user_id} 的个性化设置失败: {e}")
            return False
    
    def list_users(self) -> list[str]:
        """
        列出所有有设置的用户
        
        Returns:
            list[str]: 用户ID列表
        """
        with self._lock:
            return list(self._settings_cache.keys())
    
    def export_settings(self, user_id: str = "default") -> Optional[Dict[str, Any]]:
        """
        导出用户设置
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[Dict]: 导出的设置
        """
        try:
            with self._lock:
                if user_id in self._settings_cache:
                    return self._settings_cache[user_id].copy()
                else:
                    return None
        except Exception as e:
            logger.error(f"导出用户 {user_id} 的个性化设置失败: {e}")
            return None
    
    def import_settings(self, settings: Dict[str, Any], user_id: str = "default") -> bool:
        """
        导入用户设置
        
        Args:
            settings: 要导入的设置
            user_id: 用户ID
        
        Returns:
            bool: 是否导入成功
        """
        try:
            with self._lock:
                self._settings_cache[user_id] = settings
                self._save_settings()
            logger.info(f"用户 {user_id} 的个性化设置导入成功")
            return True
        except Exception as e:
            logger.error(f"导入用户 {user_id} 的个性化设置失败: {e}")
            return False
    
    def get_interface_settings(self, user_id: str = "default") -> Dict[str, Any]:
        """
        获取界面设置
        
        Args:
            user_id: 用户ID
        
        Returns:
            Dict: 界面设置
        """
        settings = self.get_settings(user_id)
        return settings.get("interface", {})
    
    def update_interface_settings(self, interface_settings: Dict[str, Any], user_id: str = "default") -> bool:
        """
        更新界面设置
        
        Args:
            interface_settings: 界面设置
            user_id: 用户ID
        
        Returns:
            bool: 是否更新成功
        """
        return self.update_settings({"interface": interface_settings}, user_id)
    
    def get_system_settings(self, user_id: str = "default") -> Dict[str, Any]:
        """
        获取系统设置
        
        Args:
            user_id: 用户ID
        
        Returns:
            Dict: 系统设置
        """
        settings = self.get_settings(user_id)
        return settings.get("system", {})
    
    def update_system_settings(self, system_settings: Dict[str, Any], user_id: str = "default") -> bool:
        """
        更新系统设置
        
        Args:
            system_settings: 系统设置
            user_id: 用户ID
        
        Returns:
            bool: 是否更新成功
        """
        return self.update_settings({"system": system_settings}, user_id)
    
    def get_search_settings(self, user_id: str = "default") -> Dict[str, Any]:
        """
        获取搜索设置
        
        Args:
            user_id: 用户ID
        
        Returns:
            Dict: 搜索设置
        """
        settings = self.get_settings(user_id)
        return settings.get("search", {})
    
    def update_search_settings(self, search_settings: Dict[str, Any], user_id: str = "default") -> bool:
        """
        更新搜索设置
        
        Args:
            search_settings: 搜索设置
            user_id: 用户ID
        
        Returns:
            bool: 是否更新成功
        """
        return self.update_settings({"search": search_settings}, user_id)
    
    def get_memory_settings(self, user_id: str = "default") -> Dict[str, Any]:
        """
        获取记忆设置
        
        Args:
            user_id: 用户ID
        
        Returns:
            Dict: 记忆设置
        """
        settings = self.get_settings(user_id)
        return settings.get("memory", {})
    
    def update_memory_settings(self, memory_settings: Dict[str, Any], user_id: str = "default") -> bool:
        """
        更新记忆设置
        
        Args:
            memory_settings: 记忆设置
            user_id: 用户ID
        
        Returns:
            bool: 是否更新成功
        """
        return self.update_settings({"memory": memory_settings}, user_id)
    
    def get_notification_settings(self, user_id: str = "default") -> Dict[str, Any]:
        """
        获取通知设置
        
        Args:
            user_id: 用户ID
        
        Returns:
            Dict: 通知设置
        """
        settings = self.get_settings(user_id)
        return settings.get("notifications", {})
    
    def update_notification_settings(self, notification_settings: Dict[str, Any], user_id: str = "default") -> bool:
        """
        更新通知设置
        
        Args:
            notification_settings: 通知设置
            user_id: 用户ID
        
        Returns:
            bool: 是否更新成功
        """
        return self.update_settings({"notifications": notification_settings}, user_id)
    
    def get_llm_settings(self, user_id: str = "default") -> Dict[str, Any]:
        """
        获取LLM设置
        
        Args:
            user_id: 用户ID
        
        Returns:
            Dict: LLM设置
        """
        settings = self.get_settings(user_id)
        return settings.get("llm", {})
    
    def update_llm_settings(self, llm_settings: Dict[str, Any], user_id: str = "default") -> bool:
        """
        更新LLM设置
        
        Args:
            llm_settings: LLM设置
            user_id: 用户ID
        
        Returns:
            bool: 是否更新成功
        """
        return self.update_settings({"llm": llm_settings}, user_id)


# 全局个性化设置管理器实例
_personalization_manager = None

def get_personalization_manager() -> PersonalizationManager:
    """
    获取全局个性化设置管理器实例
    
    Returns:
        PersonalizationManager: 个性化设置管理器实例
    """
    global _personalization_manager
    if _personalization_manager is None:
        _personalization_manager = PersonalizationManager()
    return _personalization_manager
