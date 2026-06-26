# -*- coding: utf-8 -*-
"""
通知发送器
统一管理通知发送，支持多渠道
优先使用 OpenClaw 长连接，回退到 Webhook
"""

import yaml
from pathlib import Path
from typing import List, Optional

from services.feishu_bot import FeishuBot
from services.wecom_bot import WecomBot

SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"


class Notifier:
    def __init__(self, default_target: str = "Liam"):
        self.settings = self._load_settings()
        self.feishu = FeishuBot(default_target)
        self.wecom = WecomBot(default_target)
        self.default_target = default_target
    
    def _load_settings(self) -> dict:
        settings_file = CONFIG_DIR / "settings.yaml"
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def _save_settings(self):
        settings_file = CONFIG_DIR / "settings.yaml"
        with open(settings_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.settings, f, allow_unicode=True, default_flow_style=False)
    
    def set_channel(self, channel: str):
        if "notification" not in self.settings:
            self.settings["notification"] = {}
        self.settings["notification"]["channel"] = channel
        self._save_settings()
    
    def set_feishu_webhook(self, webhook: str):
        if "notification" not in self.settings:
            self.settings["notification"] = {}
        self.settings["notification"]["feishu_webhook"] = webhook
        self._save_settings()
    
    def set_wecom_webhook(self, webhook: str):
        if "notification" not in self.settings:
            self.settings["notification"] = {}
        self.settings["notification"]["wecom_webhook"] = webhook
        self._save_settings()
    
    def set_target(self, target: str):
        self.default_target = target
        self.feishu.default_target = target
        self.wecom.default_target = target
    
    def get_channel(self) -> str:
        return self.settings.get("notification", {}).get("channel", "wecom")
    
    def get_feishu_webhook(self) -> str:
        return self.settings.get("notification", {}).get("feishu_webhook", "")
    
    def get_wecom_webhook(self) -> str:
        return self.settings.get("notification", {}).get("wecom_webhook", "")
    
    def format_alert_message(self, alerts: List[dict]) -> str:
        if not alerts:
            return ""
        
        message = "🚢 **特价预警通知**\n\n"
        message += "━━━━━━━━━━━━━━━━━━━━\n"
        
        for i, alert in enumerate(alerts[:10], 1):
            message += f"**{i}. {alert['box_type']} ${alert['price']}** (阈值: ${alert['threshold']})\n"
            message += f"   {alert['pol']} → {alert['pod']}\n"
            message += f"   船公司: {alert['carrier']} | 开船: {alert['etd']}\n\n"
        
        if len(alerts) > 10:
            message += f"... 共发现 **{len(alerts)}** 条特价\n"
        else:
            message += f"共发现 **{len(alerts)}** 条特价\n"
        
        message += "━━━━━━━━━━━━━━━━━━━━"
        return message
    
    def send(self, alerts: List[dict], target: str = None) -> tuple:
        if not alerts:
            return False, "没有预警需要发送"
        
        message = self.format_alert_message(alerts)
        if not message:
            return False, "消息格式化失败"
        
        channel = self.get_channel()
        target = target or self.default_target
        
        if channel == "feishu":
            webhook = self.get_feishu_webhook()
            return self.feishu.send(webhook, message, target)
        else:
            webhook = self.get_wecom_webhook()
            return self.wecom.send(webhook, message, target)
    
    def test(self, channel: str = None, target: str = None) -> tuple:
        if channel is None:
            channel = self.get_channel()
        
        target = target or self.default_target
        test_message = "🧪 **测试通知**\n\n这是一条测试消息，用于验证通知配置是否正确。"
        
        if channel == "feishu":
            webhook = self.get_feishu_webhook()
            return self.feishu.send(webhook, test_message, target)
        else:
            webhook = self.get_wecom_webhook()
            return self.wecom.send(webhook, test_message, target)
    
    def get_status(self) -> dict:
        return {
            "channel": self.get_channel(),
            "default_target": self.default_target,
            "openclaw_available": {
                "wecom": self.wecom.is_openclaw_available(),
                "feishu": self.feishu.is_openclaw_available()
            },
            "webhook_configured": {
                "wecom": bool(self.get_wecom_webhook()),
                "feishu": bool(self.get_feishu_webhook())
            }
        }
