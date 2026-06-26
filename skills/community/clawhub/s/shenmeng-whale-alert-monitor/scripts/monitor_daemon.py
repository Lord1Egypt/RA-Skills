#!/usr/bin/env python3
"""
监控守护进程 - 持续监控鲸鱼活动
"""

import os
import time
import yaml
import logging
from datetime import datetime
from typing import Dict, List

# 导入其他模块
from whale_tracker import WhaleTracker
from transfer_monitor import TransferMonitor
from exchange_flow import ExchangeFlowMonitor
from alert_manager import AlertManager, NotificationChannel

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whale_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WhaleMonitorDaemon:
    """鲸鱼监控守护进程"""
    
    def __init__(self, config_path: str = 'config.yaml'):
        self.config = self.load_config(config_path)
        self.running = False
        
        # 初始化组件
        self.whale_tracker = WhaleTracker()
        self.transfer_monitor = TransferMonitor(self.config.get('thresholds', {}))
        self.exchange_monitor = ExchangeFlowMonitor()
        self.alert_manager = AlertManager()
        
        # 设置预警处理器
        self.transfer_monitor.add_alert_handler(self.handle_transfer_alert)
        
        # 加载监控的钱包
        self.load_watched_wallets()
    
    def load_config(self, path: str) -> Dict:
        """加载配置"""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"配置文件 {path} 不存在，使用默认配置")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            'interval': 60,
            'thresholds': {
                'ETH': {'warning': 1000, 'critical': 10000},
                'USDC': {'warning': 1000000, 'critical': 10000000}
            },
            'notifications': {
                'telegram': {'enabled': False},
                'discord': {'enabled': False}
            }
        }
    
    def load_watched_wallets(self):
        """加载监控的钱包"""
        wallets = self.config.get('wallets', [])
        for wallet in wallets:
            self.whale_tracker.add_wallet(
                wallet['address'],
                wallet.get('label')
            )
        
        logger.info(f"✅ 已加载 {len(wallets)} 个监控钱包")
    
    def handle_transfer_alert(self, alert):
        """处理转账预警"""
        # 发送到配置的通知渠道
        channels = [NotificationChannel.CONSOLE]
        
        if self.config.get('notifications', {}).get('telegram', {}).get('enabled'):
            channels.append(NotificationChannel.TELEGRAM)
        
        if self.config.get('notifications', {}).get('discord', {}).get('enabled'):
            channels.append(NotificationChannel.DISCORD)
        
        message = f"🚨 {alert.message}\n\n"
        message += f"从: {alert.from_addr[:20]}...\n"
        message += f"到: {alert.to_addr[:20]}...\n"
        message += f"交易: {alert.tx_hash}"
        
        data = {
            'token': alert.token,
            'value': alert.value,
            'usd_value': alert.usd_value,
            'level': alert.level.value
        }
        
        for channel in channels:
            self.alert_manager.send_notification(channel, message, data)
    
    def run_single_check(self):
        """执行单次检查"""
        logger.info("🔍 执行监控检查...")
        
        try:
            # 1. 检查大额转账
            tokens = self.config.get('monitor_tokens', ['ETH', 'USDC', 'USDT'])
            self.transfer_monitor.monitor_once(tokens)
            
            # 2. 检查监控钱包的活动
            for address in self.whale_tracker.wallets.keys():
                # 这里可以添加更频繁的钱包检查
                pass
            
            # 3. 检查交易所流向（每小时）
            current_minute = datetime.now().minute
            if current_minute == 0:
                exchanges = self.config.get('exchanges', ['binance'])
                for exchange in exchanges:
                    records = self.exchange_monitor.fetch_flow_data(exchange, hours=1)
                    significant = self.exchange_monitor.detect_significant_flows(records)
                    
                    if significant:
                        logger.warning(f"检测到 {len(significant)} 笔大额交易所流向")
            
            logger.info("✅ 检查完成")
            
        except Exception as e:
            logger.error(f"检查过程中出错: {e}")
    
    def run(self):
        """运行守护进程"""
        self.running = True
        interval = self.config.get('interval', 60)
        
        logger.info("="*80)
        logger.info("🚀 鲸鱼监控守护进程已启动")
        logger.info(f"   检查间隔: {interval}秒")
        logger.info(f"   监控代币: {self.config.get('monitor_tokens', ['ETH', 'USDC', 'USDT'])}")
        logger.info("="*80)
        
        try:
            while self.running:
                self.run_single_check()
                
                # 等待下一次检查
                for _ in range(interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            logger.info("\n⏹️ 收到停止信号")
            self.stop()
    
    def stop(self):
        """停止守护进程"""
        self.running = False
        logger.info("⏹️ 守护进程已停止")
        
        # 保存数据
        self.transfer_monitor.save_history()
        self.alert_manager.save_configs()


def create_sample_config():
    """创建示例配置文件"""
    config = {
        'interval': 60,
        'thresholds': {
            'ETH': {'warning': 1000, 'critical': 10000},
            'WBTC': {'warning': 50, 'critical': 500},
            'USDC': {'warning': 1000000, 'critical': 10000000},
            'USDT': {'warning': 1000000, 'critical': 10000000}
        },
        'wallets': [
            {
                'address': '0x742d35Cc6634C0532925a3b8D4E6D3b6e8d3e8D3',
                'label': 'Smart Whale A'
            }
        ],
        'exchanges': ['binance', 'coinbase'],
        'monitor_tokens': ['ETH', 'USDC', 'USDT', 'WBTC'],
        'notifications': {
            'telegram': {
                'enabled': True,
                'bot_token': '${TELEGRAM_BOT_TOKEN}',
                'chat_id': '${TELEGRAM_CHAT_ID}'
            },
            'discord': {
                'enabled': True,
                'webhook_url': '${DISCORD_WEBHOOK_URL}'
            }
        }
    }
    
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print("✅ 示例配置文件已创建: config.yaml")


def demo():
    """演示"""
    print("👹 鲸鱼监控守护进程 - 演示")
    print("="*80)
    
    # 创建示例配置
    print("\n📝 创建示例配置...")
    create_sample_config()
    
    # 初始化守护进程
    print("\n🚀 初始化守护进程...")
    daemon = WhaleMonitorDaemon('config.yaml')
    
    print("\n📊 配置信息:")
    print(f"   检查间隔: {daemon.config.get('interval', 60)}秒")
    print(f"   监控钱包: {len(daemon.whale_tracker.wallets)}个")
    print(f"   监控代币: {daemon.config.get('monitor_tokens', [])}")
    
    # 执行一次检查
    print("\n🔍 执行单次检查...")
    daemon.run_single_check()
    
    print("\n✅ 演示完成!")
    print("\n实际使用时运行: python monitor_daemon.py --config config.yaml")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--create-config':
        create_sample_config()
    elif len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo()
    else:
        # 正常运行
        daemon = WhaleMonitorDaemon()
        daemon.run()
