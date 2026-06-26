#!/usr/bin/env python3
"""
舆情监控守护进程 - 持续监控社交媒体情绪
"""

import os
import time
import yaml
import logging
from datetime import datetime
from typing import Dict, List

from token_sentiment import TokenSentimentAnalyzer
from trending_topics import TrendingTopicsTracker
from kol_monitor import KOLMonitor
from fud_detector import FUDDetector
from sentiment_report import SentimentReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sentiment_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SentimentMonitorDaemon:
    """舆情监控守护进程"""
    
    def __init__(self, config_path: str = 'config.yaml'):
        self.config = self.load_config(config_path)
        self.running = False
        
        # 初始化组件
        self.sentiment_analyzer = TokenSentimentAnalyzer()
        self.trending_tracker = TrendingTopicsTracker()
        self.kol_monitor = KOLMonitor()
        self.fud_detector = FUDDetector()
        self.report_generator = SentimentReportGenerator()
        
        # 加载监控的KOL
        self.load_monitored_kols()
    
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
            'interval': 15,  # 分钟
            'tokens': ['ETH', 'BTC', 'SOL'],
            'platforms': ['twitter', 'reddit'],
            'kols': ['VitalikButerin', 'cz_binance'],
            'thresholds': {
                'sentiment_alert': 80,  # 极端贪婪
                'fud_alert': 30,        # 恐慌
                'viral_threshold': 1000
            },
            'notifications': {
                'telegram': {'enabled': False},
                'discord': {'enabled': False}
            }
        }
    
    def load_monitored_kols(self):
        """加载监控的KOL"""
        kols = self.config.get('kols', [])
        for handle in kols:
            self.kol_monitor.add_kol(handle)
        
        logger.info(f"✅ 已加载 {len(kols)} 个KOL")
    
    def check_sentiment_alerts(self, token: str):
        """检查情绪预警"""
        sentiment = self.sentiment_analyzer.analyze_sentiment(token)
        
        threshold = self.config.get('thresholds', {}).get('sentiment_alert', 80)
        
        if sentiment.overall_score >= threshold:
            logger.warning(f"🚨 {token} 情绪极端贪婪: {sentiment.overall_sentiment:.1f}/100")
            # 这里可以添加通知逻辑
        
        elif sentiment.overall_sentiment <= 20:
            logger.warning(f"🚨 {token} 情绪极度恐慌: {sentiment.overall_sentiment:.1f}/100")
    
    def check_fud_alerts(self, token: str):
        """检查FUD预警"""
        sensitivity = self.config.get('fud_sensitivity', 'medium')
        alerts = self.fud_detector.monitor_token(token, hours=1, sensitivity=sensitivity)
        
        if alerts:
            critical_count = sum(1 for a in alerts if a.alert_level in ['critical', 'high'])
            if critical_count > 0:
                logger.warning(f"🚨 {token} 检测到 {critical_count} 个严重FUD预警")
    
    def check_kol_activity(self):
        """检查KOL活动"""
        for handle in self.kol_monitor.monitored_kols.keys():
            posts = self.kol_monitor.fetch_recent_posts(handle, hours=1)
            
            if posts:
                logger.info(f"📢 {handle} 过去1小时发布了 {len(posts)} 条内容")
                
                # 检测情绪变化
                change = self.kol_monitor.detect_sentiment_change(handle)
                if change:
                    logger.warning(f"⚠️  {handle} 情绪转变: {change['change']}")
    
    def run_single_check(self):
        """执行单次检查"""
        logger.info("🔍 执行舆情监控检查...")
        
        try:
            tokens = self.config.get('tokens', ['ETH', 'BTC'])
            
            # 1. 检查代币情绪
            for token in tokens:
                self.check_sentiment_alerts(token)
                self.check_fud_alerts(token)
            
            # 2. 检查KOL活动
            self.check_kol_activity()
            
            # 3. 每小时生成一次热点报告
            current_minute = datetime.now().minute
            if current_minute == 0:
                trending = self.trending_tracker.discover_trending(hours=1)
                logger.info(f"📊 发现 {len(trending)} 个热门话题")
            
            logger.info("✅ 检查完成")
            
        except Exception as e:
            logger.error(f"检查过程中出错: {e}")
    
    def run(self):
        """运行守护进程"""
        self.running = True
        interval = self.config.get('interval', 15)
        
        logger.info("="*80)
        logger.info("🚀 舆情监控守护进程已启动")
        logger.info(f"   检查间隔: {interval}分钟")
        logger.info(f"   监控代币: {self.config.get('tokens', [])}")
        logger.info(f"   监控KOL: {self.config.get('kols', [])}")
        logger.info("="*80)
        
        try:
            while self.running:
                self.run_single_check()
                
                # 等待下一次检查
                for _ in range(interval * 60):
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


def create_sample_config():
    """创建示例配置文件"""
    config = {
        'interval': 15,
        'tokens': ['ETH', 'BTC', 'SOL', 'DOGE'],
        'platforms': ['twitter', 'reddit'],
        'kols': [
            'VitalikButerin',
            'cz_binance',
            'elonmusk',
            'saylor'
        ],
        'thresholds': {
            'sentiment_alert': 80,
            'fud_alert': 30,
            'viral_threshold': 1000
        },
        'fud_sensitivity': 'medium',
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
    print("📱 舆情监控守护进程 - 演示")
    print("="*80)
    
    # 创建示例配置
    print("\n📝 创建示例配置...")
    create_sample_config()
    
    # 初始化守护进程
    print("\n🚀 初始化守护进程...")
    daemon = SentimentMonitorDaemon('config.yaml')
    
    print("\n📊 配置信息:")
    print(f"   检查间隔: {daemon.config.get('interval', 15)}分钟")
    print(f"   监控代币: {daemon.config.get('tokens', [])}")
    print(f"   监控KOL: {daemon.config.get('kols', [])}")
    
    # 执行一次检查
    print("\n🔍 执行单次检查...")
    daemon.run_single_check()
    
    print("\n✅ 演示完成!")
    print("\n实际使用时运行: python sentiment_daemon.py --config config.yaml")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--create-config':
        create_sample_config()
    elif len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo()
    else:
        # 正常运行
        daemon = SentimentMonitorDaemon()
        daemon.run()
