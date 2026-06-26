#!/usr/bin/env python3
"""
预警管理器 - 管理预警配置和通知
"""

import os
import json
import logging
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NotificationChannel(Enum):
    CONSOLE = "console"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    WEBHOOK = "webhook"

@dataclass
class AlertConfig:
    """预警配置"""
    id: str
    name: str
    enabled: bool
    conditions: Dict
    channels: List[NotificationChannel]
    cooldown_minutes: int
    created_at: datetime

class AlertManager:
    """预警管理器"""
    
    def __init__(self):
        self.configs: Dict[str, AlertConfig] = {}
        self.alert_history: List[Dict] = []
        self.load_configs()
    
    def load_configs(self):
        """加载配置"""
        try:
            with open('alert_configs.json', 'r') as f:
                data = json.load(f)
                for item in data.get('configs', []):
                    config = AlertConfig(
                        id=item['id'],
                        name=item['name'],
                        enabled=item['enabled'],
                        conditions=item['conditions'],
                        channels=[NotificationChannel(c) for c in item['channels']],
                        cooldown_minutes=item['cooldown_minutes'],
                        created_at=datetime.fromisoformat(item['created_at'])
                    )
                    self.configs[config.id] = config
            logger.info(f"✅ 已加载 {len(self.configs)} 个预警配置")
        except FileNotFoundError:
            logger.info("未找到现有配置，创建新配置")
    
    def save_configs(self):
        """保存配置"""
        data = {
            'configs': [
                {
                    **asdict(config),
                    'channels': [c.value for c in config.channels],
                    'created_at': config.created_at.isoformat()
                }
                for config in self.configs.values()
            ]
        }
        
        with open('alert_configs.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info("✅ 配置已保存")
    
    def add_config(self, name: str, conditions: Dict, 
                   channels: List[NotificationChannel],
                   cooldown_minutes: int = 30) -> str:
        """添加预警配置"""
        config_id = f"alert_{len(self.configs)}_{int(datetime.now().timestamp())}"
        
        config = AlertConfig(
            id=config_id,
            name=name,
            enabled=True,
            conditions=conditions,
            channels=channels,
            cooldown_minutes=cooldown_minutes,
            created_at=datetime.now()
        )
        
        self.configs[config_id] = config
        self.save_configs()
        
        logger.info(f"✅ 预警配置已添加: {name}")
        return config_id
    
    def remove_config(self, config_id: str):
        """移除预警配置"""
        if config_id in self.configs:
            del self.configs[config_id]
            self.save_configs()
            logger.info(f"🗑️  预警配置已移除: {config_id}")
    
    def toggle_config(self, config_id: str):
        """切换配置状态"""
        if config_id in self.configs:
            self.configs[config_id].enabled = not self.configs[config_id].enabled
            status = "启用" if self.configs[config_id].enabled else "停用"
            logger.info(f"🔄 预警配置已{status}: {self.configs[config_id].name}")
            self.save_configs()
    
    def send_notification(self, channel: NotificationChannel, message: str, data: Optional[Dict] = None):
        """发送通知"""
        if channel == NotificationChannel.CONSOLE:
            self._send_console(message, data)
        elif channel == NotificationChannel.TELEGRAM:
            self._send_telegram(message, data)
        elif channel == NotificationChannel.DISCORD:
            self._send_discord(message, data)
        elif channel == NotificationChannel.WEBHOOK:
            self._send_webhook(message, data)
    
    def _send_console(self, message: str, data: Optional[Dict]):
        """控制台通知"""
        print(f"\n{'='*80}")
        print(f"🚨 预警通知")
        print(f"{'='*80}")
        print(message)
        if data:
            print(f"\n数据: {json.dumps(data, indent=2)}")
        print(f"{'='*80}\n")
    
    def _send_telegram(self, message: str, data: Optional[Dict]):
        """Telegram通知"""
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            logger.warning("Telegram配置缺失")
            return
        
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Telegram通知已发送")
            else:
                logger.error(f"Telegram发送失败: {response.text}")
        except Exception as e:
            logger.error(f"Telegram通知错误: {e}")
    
    def _send_discord(self, message: str, data: Optional[Dict]):
        """Discord通知"""
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        if not webhook_url:
            logger.warning("Discord配置缺失")
            return
        
        try:
            embed = {
                'title': '鲸鱼预警',
                'description': message,
                'color': 0xff0000,
                'timestamp': datetime.now().isoformat()
            }
            
            if data:
                embed['fields'] = [
                    {'name': k, 'value': str(v), 'inline': True}
                    for k, v in data.items()
                ]
            
            payload = {
                'embeds': [embed]
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 204:
                logger.info("✅ Discord通知已发送")
            else:
                logger.error(f"Discord发送失败: {response.status_code}")
        except Exception as e:
            logger.error(f"Discord通知错误: {e}")
    
    def _send_webhook(self, message: str, data: Optional[Dict]):
        """Webhook通知"""
        webhook_url = os.getenv('CUSTOM_WEBHOOK_URL')
        
        if not webhook_url:
            logger.warning("Webhook配置缺失")
            return
        
        try:
            payload = {
                'message': message,
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Webhook通知已发送")
        except Exception as e:
            logger.error(f"Webhook通知错误: {e}")
    
    def list_configs(self):
        """列出所有配置"""
        print(f"\n{'='*80}")
        print(f"📋 预警配置列表 ({len(self.configs)}个)")
        print(f"{'='*80}")
        print(f"{'ID':<20} {'名称':<20} {'状态':<10} {'渠道':<20}")
        print(f"{'-'*80}")
        
        for config in self.configs.values():
            status = "🟢 启用" if config.enabled else "🔴 停用"
            channels = ", ".join(c.value for c in config.channels)
            print(f"{config.id:<20} {config.name:<20} {status:<10} {channels:<20}")
        
        print(f"{'='*80}\n")
    
    def test_notification(self, channel: NotificationChannel):
        """测试通知"""
        message = "🧪 这是一条测试预警消息\n\n如果您收到这条消息，说明通知配置正确！"
        data = {
            'test': True,
            'timestamp': datetime.now().isoformat()
        }
        
        self.send_notification(channel, message, data)
        logger.info(f"✅ 测试通知已发送到 {channel.value}")
    
    def export_history(self, filename: str = 'alert_history.json'):
        """导出预警历史"""
        with open(filename, 'w') as f:
            json.dump(self.alert_history, f, indent=2)
        
        logger.info(f"✅ 预警历史已导出到: {filename}")


def demo():
    """演示"""
    print("🔔 预警管理器 - 演示")
    print("="*80)
    
    manager = AlertManager()
    
    # 添加示例配置
    print("\n📝 添加示例配置...")
    
    config1_id = manager.add_config(
        name="ETH大额转账预警",
        conditions={'token': 'ETH', 'min_value': 1000},
        channels=[NotificationChannel.CONSOLE],
        cooldown_minutes=30
    )
    
    config2_id = manager.add_config(
        name="交易所流入监控",
        conditions={'type': 'exchange_inflow', 'threshold': 5000000},
        channels=[NotificationChannel.CONSOLE, NotificationChannel.TELEGRAM],
        cooldown_minutes=60
    )
    
    # 列出配置
    manager.list_configs()
    
    # 测试通知
    print("\n🧪 测试控制台通知...")
    manager.test_notification(NotificationChannel.CONSOLE)
    
    # 模拟发送预警
    print("\n🚨 模拟发送预警...")
    manager.send_notification(
        channel=NotificationChannel.CONSOLE,
        message="🐋 检测到鲸鱼转账: 5,000 ETH\n从: 0x742d...\n到: Binance",
        data={'amount': 5000, 'token': 'ETH', 'value_usd': 17500000}
    )
    
    # 切换配置状态
    print("\n🔄 切换配置状态...")
    manager.toggle_config(config1_id)
    
    # 再次列出
    manager.list_configs()
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
