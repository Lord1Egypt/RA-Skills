#!/usr/bin/env python3
"""
大额转账监控器 - 监控链上的大额转账并发送预警
"""

import os
import time
import json
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from enum import Enum

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class TransferAlert:
    """转账预警"""
    timestamp: datetime
    level: AlertLevel
    from_addr: str
    to_addr: str
    value: float
    token: str
    tx_hash: str
    usd_value: float
    message: str

class TransferMonitor:
    """大额转账监控器"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.thresholds = self.config.get('thresholds', {
            'ETH': {'warning': 1000, 'critical': 10000},
            'WBTC': {'warning': 50, 'critical': 500},
            'USDC': {'warning': 1000000, 'critical': 10000000},
            'USDT': {'warning': 1000000, 'critical': 10000000}
        })
        self.alert_handlers: List[Callable] = []
        self.alert_history: List[TransferAlert] = []
        self.cooldown_minutes = self.config.get('cooldown', 30)
        self.last_alert_time: Dict[str, datetime] = {}
    
    def add_alert_handler(self, handler: Callable):
        """添加预警处理器"""
        self.alert_handlers.append(handler)
    
    def get_token_price(self, token: str) -> float:
        """获取代币价格（简化版）"""
        prices = {
            'ETH': 3500,
            'WBTC': 65000,
            'USDC': 1,
            'USDT': 1,
            'LINK': 18,
            'UNI': 12
        }
        return prices.get(token, 1)
    
    def determine_alert_level(self, token: str, value: float) -> AlertLevel:
        """确定预警级别"""
        token_thresholds = self.thresholds.get(token, {'warning': 1000000, 'critical': 10000000})
        
        if value >= token_thresholds.get('critical', float('inf')):
            return AlertLevel.CRITICAL
        elif value >= token_thresholds.get('warning', float('inf')):
            return AlertLevel.WARNING
        else:
            return AlertLevel.INFO
    
    def check_cooldown(self, alert_key: str) -> bool:
        """检查冷却时间"""
        if alert_key not in self.last_alert_time:
            return True
        
        elapsed = (datetime.now() - self.last_alert_time[alert_key]).total_seconds() / 60
        return elapsed >= self.cooldown_minutes
    
    def fetch_recent_transfers(self, token: str = 'ETH', hours: int = 1) -> List[Dict]:
        """获取最近转账（模拟数据）"""
        import random
        
        transfers = []
        base_time = datetime.now() - timedelta(hours=hours)
        
        # 生成5-20笔转账
        for i in range(random.randint(5, 20)):
            tx_time = base_time + timedelta(minutes=random.uniform(0, hours * 60))
            
            # 生成随机价值（大部分小额，少数大额）
            if token == 'ETH':
                value = random.expovariate(1/500)  # 指数分布
            elif token in ['USDC', 'USDT']:
                value = random.expovariate(1/500000)
            else:
                value = random.expovariate(1/1000)
            
            transfers.append({
                'timestamp': tx_time,
                'from': f"0x{''.join([random.choice('0123456789abcdef') for _ in range(40)])}",
                'to': f"0x{''.join([random.choice('0123456789abcdef') for _ in range(40)])}",
                'value': value,
                'token': token,
                'hash': f"0x{''.join([random.choice('0123456789abcdef') for _ in range(64)])}"
            })
        
        return transfers
    
    def process_transfer(self, transfer: Dict) -> Optional[TransferAlert]:
        """处理单笔转账"""
        token = transfer['token']
        value = transfer['value']
        
        # 确定预警级别
        level = self.determine_alert_level(token, value)
        
        # 只处理warning及以上级别
        if level == AlertLevel.INFO:
            return None
        
        # 检查冷却
        alert_key = f"{transfer['from']}_{transfer['to']}"
        if not self.check_cooldown(alert_key):
            return None
        
        # 计算美元价值
        price = self.get_token_price(token)
        usd_value = value * price
        
        # 生成消息
        emoji = "🔴" if level == AlertLevel.CRITICAL else "🟠"
        message = f"{emoji} 大额{token}转账: {value:,.2f} ({usd_value:,.0f} USD)"
        
        alert = TransferAlert(
            timestamp=transfer['timestamp'],
            level=level,
            from_addr=transfer['from'],
            to_addr=transfer['to'],
            value=value,
            token=token,
            tx_hash=transfer['hash'],
            usd_value=usd_value,
            message=message
        )
        
        # 更新冷却时间
        self.last_alert_time[alert_key] = datetime.now()
        
        return alert
    
    def trigger_alert(self, alert: TransferAlert):
        """触发预警"""
        self.alert_history.append(alert)
        
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"预警处理器错误: {e}")
    
    def console_alert_handler(self, alert: TransferAlert):
        """控制台预警处理器"""
        print(f"\n{'='*80}")
        print(f"🚨 大额转账预警 [{alert.level.value.upper()}]")
        print(f"{'='*80}")
        print(f"   {alert.message}")
        print(f"   时间: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   从: {alert.from_addr}")
        print(f"   到: {alert.to_addr}")
        print(f"   交易: {alert.tx_hash}")
        print(f"{'='*80}\n")
    
    def monitor_once(self, tokens: Optional[List[str]] = None):
        """单次监控"""
        if tokens is None:
            tokens = ['ETH', 'USDC', 'USDT']
        
        logger.info(f"🔍 开始监控... 代币: {tokens}")
        
        all_alerts = []
        
        for token in tokens:
            transfers = self.fetch_recent_transfers(token, hours=1)
            
            for transfer in transfers:
                alert = self.process_transfer(transfer)
                if alert:
                    all_alerts.append(alert)
                    self.trigger_alert(alert)
        
        # 按时间排序
        all_alerts.sort(key=lambda x: x.timestamp, reverse=True)
        
        logger.info(f"✅ 监控完成，发现 {len(all_alerts)} 个预警")
        return all_alerts
    
    def run_continuous(self, tokens: Optional[List[str]] = None, interval: int = 60):
        """持续监控"""
        logger.info(f"🚀 启动持续监控 (每{interval}秒检查一次)")
        logger.info("按Ctrl+C停止\n")
        
        try:
            while True:
                self.monitor_once(tokens)
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("\n⏹️ 监控已停止")
            self.save_history()
    
    def save_history(self, filename: str = 'alert_history.json'):
        """保存预警历史"""
        data = [
            {
                'timestamp': a.timestamp.isoformat(),
                'level': a.level.value,
                'token': a.token,
                'value': a.value,
                'usd_value': a.usd_value,
                'from': a.from_addr,
                'to': a.to_addr,
                'hash': a.tx_hash,
                'message': a.message
            }
            for a in self.alert_history
        ]
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"预警历史已保存到: {filename}")
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        if not self.alert_history:
            return {}
        
        by_token = {}
        by_level = {'critical': 0, 'warning': 0, 'info': 0}
        
        total_usd = 0
        
        for alert in self.alert_history:
            by_token[alert.token] = by_token.get(alert.token, 0) + 1
            by_level[alert.level.value] = by_level.get(alert.level.value, 0) + 1
            total_usd += alert.usd_value
        
        return {
            'total_alerts': len(self.alert_history),
            'by_token': by_token,
            'by_level': by_level,
            'total_usd_value': total_usd
        }


def demo():
    """演示"""
    print("💰 大额转账监控器 - 演示")
    print("="*80)
    
    config = {
        'thresholds': {
            'ETH': {'warning': 500, 'critical': 5000},
            'USDC': {'warning': 500000, 'critical': 5000000},
            'USDT': {'warning': 500000, 'critical': 5000000}
        },
        'cooldown': 5  # 演示用较短的冷却时间
    }
    
    monitor = TransferMonitor(config)
    monitor.add_alert_handler(monitor.console_alert_handler)
    
    # 单次监控
    print("\n🔍 执行单次监控...\n")
    alerts = monitor.monitor_once(tokens=['ETH', 'USDC', 'USDT'])
    
    # 统计
    stats = monitor.get_statistics()
    if stats:
        print(f"\n📊 本次监控统计:")
        print(f"   总预警: {stats['total_alerts']}")
        print(f"   按代币: {stats['by_token']}")
        print(f"   按级别: {stats['by_level']}")
        print(f"   涉及总额: ${stats['total_usd_value']:,.0f}")
    
    # 保存历史
    monitor.save_history()
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
