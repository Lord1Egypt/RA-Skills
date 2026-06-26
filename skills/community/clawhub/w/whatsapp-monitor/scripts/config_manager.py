#!/usr/bin/env python3
"""
配置管理器 - 处理配置文件和数据存储
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.data_dir = Path("data")
        
        # 配置文件路径
        self.whatsapp_config_path = self.config_dir / "whatsapp-targets.json"
        self.feishu_config_path = self.config_dir / "feishu-settings.json"
        self.matched_messages_path = self.data_dir / "matched_messages.json"
        
        # 配置数据
        self.whatsapp_config = None
        self.feishu_config = None
        
        # 创建目录
        self.config_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
    
    def load_configs(self) -> bool:
        """加载所有配置文件"""
        try:
            # 加载 WhatsApp 配置
            if self.whatsapp_config_path.exists():
                with open(self.whatsapp_config_path, 'r', encoding='utf-8') as f:
                    self.whatsapp_config = json.load(f)
                self.logger.info(f"已加载 WhatsApp 配置: {self.whatsapp_config_path}")
            else:
                self.logger.warning(f"WhatsApp 配置文件不存在: {self.whatsapp_config_path}")
                # 创建默认配置
                self.create_default_whatsapp_config()
            
            # 加载飞书配置
            if self.feishu_config_path.exists():
                with open(self.feishu_config_path, 'r', encoding='utf-8') as f:
                    self.feishu_config = json.load(f)
                self.logger.info(f"已加载飞书配置: {self.feishu_config_path}")
            else:
                self.logger.warning(f"飞书配置文件不存在: {self.feishu_config_path}")
                # 创建默认配置
                self.create_default_feishu_config()
            
            return True
            
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {str(e)}", exc_info=True)
            return False
    
    def create_default_whatsapp_config(self):
        """创建默认的 WhatsApp 配置"""
        default_config = {
            "version": "1.0",
            "targets": [
                {
                    "name": "示例群聊",
                    "type": "group",
                    "identifier": "群聊ID或名称",
                    "enabled": False,
                    "keywords": ["示例关键词"],
                    "priority": "medium",
                    "keyword_patterns": [".*示例.*"]
                }
            ],
            "monitoring": {
                "scan_interval_minutes": 5,
                "batch_size": 10,
                "max_age_hours": 24,
                "alert_on_high_priority": True,
                "include_context_messages": 2
            }
        }
        
        self.whatsapp_config = default_config
        self.save_whatsapp_config()
        self.logger.info("已创建默认 WhatsApp 配置")
    
    def create_default_feishu_config(self):
        """创建默认的飞书配置"""
        default_config = {
            "feishu": {
                "app_id": "YOUR_APP_ID",
                "app_secret": "YOUR_APP_SECRET",
                "tenant_access_token": "YOUR_TENANT_ACCESS_TOKEN",
                "table_app_token": "YOUR_TABLE_APP_TOKEN",
                "table_token": "YOUR_TABLE_TOKEN"
            },
            "table": {
                "name": "WhatsApp 消息监控日志",
                "fields": [
                    {"field_name": "timestamp", "type": 5, "property": {"date_format": "yyyy-MM-dd HH:mm:ss"}},
                    {"field_name": "source", "type": 1},
                    {"field_name": "sender", "type": 1},
                    {"field_name": "message_content", "type": 1},
                    {"field_name": "keyword_matched", "type": 1},
                    {"field_name": "priority", "type": 3},
                    {"field_name": "message_type", "type": 1},
                    {"field_name": "attachment", "type": 1},
                    {"field_name": "chat_link", "type": 1}
                ]
            },
            "export": {
                "batch_threshold": 10,
                "schedule": "every 30 minutes",
                "retry_on_failure": True,
                "max_retries": 3,
                "timeout_seconds": 30
            }
        }
        
        self.feishu_config = default_config
        self.save_feishu_config()
        self.logger.info("已创建默认飞书配置")
    
    def save_whatsapp_config(self):
        """保存 WhatsApp 配置"""
        try:
            with open(self.whatsapp_config_path, 'w', encoding='utf-8') as f:
                json.dump(self.whatsapp_config, f, ensure_ascii=False, indent=2)
            self.logger.info(f"已保存 WhatsApp 配置: {self.whatsapp_config_path}")
        except Exception as e:
            self.logger.error(f"保存 WhatsApp 配置失败: {str(e)}")
    
    def save_feishu_config(self):
        """保存飞书配置"""
        try:
            with open(self.feishu_config_path, 'w', encoding='utf-8') as f:
                json.dump(self.feishu_config, f, ensure_ascii=False, indent=2)
            self.logger.info(f"已保存飞书配置: {self.feishu_config_path}")
        except Exception as e:
            self.logger.error(f"保存飞书配置失败: {str(e)}")
    
    def get_whatsapp_config(self) -> Optional[Dict[str, Any]]:
        """获取 WhatsApp 配置"""
        return self.whatsapp_config
    
    def get_feishu_config(self) -> Optional[Dict[str, Any]]:
        """获取飞书配置"""
        return self.feishu_config
    
    def get_targets(self) -> List[Dict[str, Any]]:
        """获取监控目标列表"""
        if self.whatsapp_config and "targets" in self.whatsapp_config:
            return self.whatsapp_config["targets"]
        return []
    
    def get_targets_count(self) -> int:
        """获取监控目标数量"""
        return len(self.get_targets())
    
    def get_keywords(self) -> List[str]:
        """获取所有关键词"""
        keywords = []
        for target in self.get_targets():
            if "keywords" in target:
                keywords.extend(target["keywords"])
        return list(set(keywords))  # 去重
    
    def get_keywords_count(self) -> int:
        """获取关键词总数"""
        return len(self.get_keywords())
    
    def get_scan_interval(self) -> int:
        """获取扫描间隔（秒）"""
        if self.whatsapp_config and "monitoring" in self.whatsapp_config:
            minutes = self.whatsapp_config["monitoring"].get("scan_interval_minutes", 5)
            return minutes * 60
        return 300  # 默认 5 分钟
    
    def get_batch_threshold(self) -> int:
        """获取批量阈值"""
        if self.whatsapp_config and "monitoring" in self.whatsapp_config:
            return self.whatsapp_config["monitoring"].get("batch_size", 10)
        return 10
    
    def get_priority_targets(self, priority: str = "high") -> List[Dict[str, Any]]:
        """获取指定优先级的监控目标"""
        return [t for t in self.get_targets() if t.get("priority") == priority and t.get("enabled", False)]
    
    def save_matched_messages(self, messages: List[Dict[str, Any]]):
        """保存匹配的消息"""
        try:
            # 加载现有消息
            existing_messages = self.get_stored_messages()
            
            # 添加新消息
            existing_messages.extend(messages)
            
            # 根据时间戳排序
            existing_messages.sort(key=lambda x: x.get("timestamp", ""))
            
            # 限制消息数量（防止文件过大）
            max_messages = 1000
            if len(existing_messages) > max_messages:
                existing_messages = existing_messages[-max_messages:]
            
            # 保存到文件
            with open(self.matched_messages_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "last_updated": datetime.now().isoformat(),
                    "messages": existing_messages
                }, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"已保存 {len(messages)} 条匹配消息，总计 {len(existing_messages)} 条")
            
        except Exception as e:
            self.logger.error(f"保存匹配消息失败: {str(e)}")
    
    def get_stored_messages(self) -> List[Dict[str, Any]]:
        """获取存储的匹配消息"""
        try:
            if self.matched_messages_path.exists():
                with open(self.matched_messages_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("messages", [])
            return []
        except Exception as e:
            self.logger.error(f"读取存储消息失败: {str(e)}")
            return []
    
    def clear_stored_messages(self):
        """清空存储的消息"""
        try:
            if self.matched_messages_path.exists():
                with open(self.matched_messages_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "last_updated": datetime.now().isoformat(),
                        "messages": []
                    }, f, ensure_ascii=False, indent=2)
                self.logger.info("已清空存储的消息")
        except Exception as e:
            self.logger.error(f"清空存储消息失败: {str(e)}")
    
    def get_last_export_time(self) -> Optional[str]:
        """获取最后导出时间"""
        try:
            if self.matched_messages_path.exists():
                with open(self.matched_messages_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("last_updated")
            return None
        except Exception as e:
            self.logger.error(f"读取最后导出时间失败: {str(e)}")
            return None
    
    def configs_loaded(self) -> bool:
        """检查配置是否已加载"""
        return self.whatsapp_config is not None and self.feishu_config is not None
    
    def add_target(self, target: Dict[str, Any]):
        """添加监控目标"""
        if self.whatsapp_config:
            if "targets" not in self.whatsapp_config:
                self.whatsapp_config["targets"] = []
            self.whatsapp_config["targets"].append(target)
            self.save_whatsapp_config()
    
    def remove_target(self, target_name: str):
        """移除监控目标"""
        if self.whatsapp_config and "targets" in self.whatsapp_config:
            self.whatsapp_config["targets"] = [
                t for t in self.whatsapp_config["targets"] 
                if t.get("name") != target_name
            ]
            self.save_whatsapp_config()
    
    def update_target(self, target_name: str, updates: Dict[str, Any]):
        """更新监控目标"""
        if self.whatsapp_config and "targets" in self.whatsapp_config:
            for i, target in enumerate(self.whatsapp_config["targets"]):
                if target.get("name") == target_name:
                    self.whatsapp_config["targets"][i].update(updates)
                    self.save_whatsapp_config()
                    break