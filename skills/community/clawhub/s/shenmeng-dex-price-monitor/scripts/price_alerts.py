#!/usr/bin/env python3
"""
DEX价格预警器
设置价格阈值，当价格达到条件时发送通知
"""

import time
import json
import logging
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Callable
from enum import Enum
import requests
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertCondition(Enum):
    ABOVE = "above"
    BELOW = "below"
    RANGE = "range"
    CHANGE = "change"

@dataclass
class PriceAlert:
    """价格预警配置"""
    id: str
    token_pair: str
    condition: AlertCondition
    price: float
    secondary_price: Optional[float] = None  # 用于range条件
    message: Optional[str] = None
    cooldown_minutes: int = 30
    notify_channels: List[str] = None
    is_active: bool = True
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0

class PriceAlertManager:
    """价格预警管理器"""
    
    def __init__(self):
        self.alerts: Dict[str, PriceAlert] = {}
        self.notification_handlers: Dict[str, Callable] = {}
        self.setup_default_handlers()
    
    def setup_default_handlers(self):
        """设置默认通知处理器"""
        self.notification_handlers['console'] = self._console_notification
        self.notification_handlers['telegram'] = self._telegram_notification
        self.notification_handlers['discord'] = self._discord_notification
    
    def add_alert(self, alert: PriceAlert) -> str:
        """添加预警"""
        alert_id = f"{alert.token_pair}_{alert.condition.value}_{int(time.time())}"
        alert.id = alert_id
        self.alerts[alert_id] = alert
        logger.info(f"✅ 预警已添加: {alert_id}")
        return alert_id
    
    def remove_alert(self, alert_id: str):
        """移除预警"""
        if alert_id in self.alerts:
            del self.alerts[alert_id]
            logger.info(f"🗑️  预警已移除: {alert_id}")
    
    def check_alert(self, alert: PriceAlert, current_price: float) -> bool:
        """检查预警是否应该触发"""
        if not alert.is_active:
            return False
        
        # 检查冷却时间
        if alert.last_triggered:
            elapsed = (datetime.now() - alert.last_triggered).total_seconds() / 60
            if elapsed < alert.cooldown_minutes:
                return False
        
        # 检查条件
        triggered = False
        
        if alert.condition == AlertCondition.ABOVE:
            triggered = current_price > alert.price
        elif alert.condition == AlertCondition.BELOW:
            triggered = current_price < alert.price
        elif alert.condition == AlertCondition.RANGE:
            if alert.secondary_price:
                triggered = current_price < alert.price or current_price > alert.secondary_price
        
        return triggered
    
    def trigger_alert(self, alert: PriceAlert, current_price: float):
        """触发预警"""
        alert.last_triggered = datetime.now()
        alert.trigger_count += 1
        
        message = self._format_alert_message(alert, current_price)
        
        # 发送到各通知渠道
        for channel in alert.notify_channels or ['console']:
            handler = self.notification_handlers.get(channel)
            if handler:
                try:
                    handler(message, alert)
                except Exception as e:
                    logger.error(f"通知发送失败 ({channel}): {e}")
    
    def _format_alert_message(self, alert: PriceAlert, current_price: float) -> str:
        """格式化预警消息"""
        condition_str = {
            AlertCondition.ABOVE: "突破",
            AlertCondition.BELOW: "跌破",
            AlertCondition.RANGE: "超出范围",
            AlertCondition.CHANGE: "变化"
        }.get(alert.condition, "触发")
        
        if alert.message:
            return alert.message
        
        emoji = "🚨" if alert.condition in [AlertCondition.ABOVE, AlertCondition.BELOW] else "⚠️"
        
        return f"""
{emoji} 价格预警

代币: {alert.token_pair}
条件: {condition_str} ${alert.price:,.2f}
当前价格: ${current_price:,.2f}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
触发次数: {alert.trigger_count}
"""
    
    def _console_notification(self, message: str, alert: PriceAlert):
        """控制台通知"""
        print("\n" + "="*60)
        print(message)
        print("="*60 + "\n")
    
    def _telegram_notification(self, message: str, alert: PriceAlert):
        """Telegram通知"""
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            logger.warning("Telegram配置缺失")
            return
        
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
    
    def _discord_notification(self, message: str, alert: PriceAlert):
        """Discord通知"""
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        if not webhook_url:
            logger.warning("Discord配置缺失")
            return
        
        payload = {
            'content': message,
            'username': 'DEX Price Alert'
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            logger.info("✅ Discord通知已发送")
        else:
            logger.error(f"Discord发送失败: {response.status_code}")
    
    def check_all_alerts(self, prices: Dict[str, float]):
        """检查所有预警"""
        for alert in self.alerts.values():
            if alert.token_pair in prices:
                current_price = prices[alert.token_pair]
                
                if self.check_alert(alert, current_price):
                    self.trigger_alert(alert, current_price)
    
    def list_alerts(self):
        """列出所有预警"""
        print(f"\n{'='*80}")
        print(f"📋 预警列表 (共{len(self.alerts)}个)")
        print(f"{'='*80}")
        print(f"{'ID':<25} {'代币':<15} {'条件':<15} {'价格':<15} {'状态':<10}")
        print(f"{'-'*80}")
        
        for alert in self.alerts.values():
            status = "🟢 活跃" if alert.is_active else "🔴 停用"
            condition_str = f"{alert.condition.value} ${alert.price:.0f}"
            print(f"{alert.id:<25} {alert.token_pair:<15} {condition_str:<15} ${alert.price:<14.2f} {status:<10}")
        
        print(f"{'='*80}\n")
    
    def save_alerts(self, filename: str):
        """保存预警配置"""
        data = {
            'alerts': [
                {
                    **asdict(alert),
                    'condition': alert.condition.value,
                    'last_triggered': alert.last_triggered.isoformat() if alert.last_triggered else None
                }
                for alert in self.alerts.values()
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"预警配置已保存到: {filename}")
    
    def load_alerts(self, filename: str):
        """加载预警配置"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            for item in data.get('alerts', []):
                alert = PriceAlert(
                    id=item['id'],
                    token_pair=item['token_pair'],
                    condition=AlertCondition(item['condition']),
                    price=item['price'],
                    secondary_price=item.get('secondary_price'),
                    message=item.get('message'),
                    cooldown_minutes=item.get('cooldown_minutes', 30),
                    notify_channels=item.get('notify_channels', ['console']),
                    is_active=item.get('is_active', True),
                    last_triggered=datetime.fromisoformat(item['last_triggered']) if item.get('last_triggered') else None,
                    trigger_count=item.get('trigger_count', 0)
                )
                self.alerts[alert.id] = alert
            
            logger.info(f"✅ 已加载 {len(self.alerts)} 个预警")
        except FileNotFoundError:
            logger.warning(f"文件 {filename} 不存在")


def interactive_demo():
    """交互式演示"""
    print("🔔 DEX价格预警器 - 交互式演示")
    print("="*60)
    
    manager = PriceAlertManager()
    
    # 添加示例预警
    print("\n📝 添加示例预警...")
    
    alert1 = PriceAlert(
        id="",
        token_pair="ETH/USDC",
        condition=AlertCondition.ABOVE,
        price=3600,
        message="ETH突破3600！🚀",
        cooldown_minutes=60,
        notify_channels=['console']
    )
    manager.add_alert(alert1)
    
    alert2 = PriceAlert(
        id="",
        token_pair="ETH/USDC",
        condition=AlertCondition.BELOW,
        price=3400,
        message="ETH跌破3400！📉",
        cooldown_minutes=60,
        notify_channels=['console']
    )
    manager.add_alert(alert2)
    
    alert3 = PriceAlert(
        id="",
        token_pair="BTC/USDC",
        condition=AlertCondition.RANGE,
        price=60000,
        secondary_price=70000,
        message="BTC价格异常波动！",
        cooldown_minutes=30,
        notify_channels=['console']
    )
    manager.add_alert(alert3)
    
    # 显示列表
    manager.list_alerts()
    
    # 模拟价格检查
    print("\n🧪 模拟价格检查...\n")
    
    test_prices = [
        {"ETH/USDC": 3500, "BTC/USDC": 65000},  # 不触发
        {"ETH/USDC": 3650, "BTC/USDC": 65000},  # 触发ETH above
        {"ETH/USDC": 3650, "BTC/USDC": 65000},  # 冷却中，不触发
        {"ETH/USDC": 3350, "BTC/USDC": 65000},  # 触发ETH below
        {"ETH/USDC": 3500, "BTC/USDC": 58000},  # 触发BTC range
    ]
    
    for i, prices in enumerate(test_prices, 1):
        print(f"\n--- 第{i}轮价格更新 ---")
        for pair, price in prices.items():
            print(f"  {pair}: ${price:,.2f}")
        
        manager.check_all_alerts(prices)
        time.sleep(1)
    
    # 保存配置
    manager.save_alerts('price_alerts.json')
    
    print("\n✅ 演示完成！")


def demo():
    """快速演示"""
    print("🔔 DEX价格预警器 - 演示")
    print("="*60)
    
    manager = PriceAlertManager()
    
    # 添加预警
    alert = PriceAlert(
        id="",
        token_pair="ETH/USDC",
        condition=AlertCondition.ABOVE,
        price=3500,
        cooldown_minutes=0,  # 演示用，不设置冷却
        notify_channels=['console']
    )
    manager.add_alert(alert)
    
    # 显示列表
    manager.list_alerts()
    
    # 测试触发
    print("\n🧪 测试预警触发:\n")
    
    # 不触发
    print("价格 $3,400 (不触发)")
    manager.check_all_alerts({"ETH/USDC": 3400})
    
    # 触发
    print("\n价格 $3,600 (触发)")
    manager.check_all_alerts({"ETH/USDC": 3600})
    
    # 显示更新后的列表
    manager.list_alerts()


if __name__ == "__main__":
    interactive_demo()
