#!/usr/bin/env python3
"""
DEX实时价格监控器
实时监控多个DEX的代币价格，发现价差机会
"""

import time
import json
import logging
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Callable
from threading import Thread, Event
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class PriceData:
    """价格数据"""
    dex: str
    chain: str
    token_pair: str
    price: float
    timestamp: datetime
    volume_24h: Optional[float] = None
    liquidity: Optional[float] = None

@dataclass
class SpreadAlert:
    """价差预警"""
    token_pair: str
    buy_dex: str
    sell_dex: str
    buy_price: float
    sell_price: float
    spread_pct: float
    timestamp: datetime

class DEXPriceMonitor:
    """DEX价格监控器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.running = False
        self.stop_event = Event()
        self.price_history: Dict[str, List[PriceData]] = {}
        self.alert_handlers: List[Callable] = []
        
    def add_alert_handler(self, handler: Callable):
        """添加预警处理器"""
        self.alert_handlers.append(handler)
    
    def fetch_price_from_coingecko(self, token_id: str) -> Optional[float]:
        """从CoinGecko获取价格"""
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': token_id,
                'vs_currencies': 'usd'
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return data.get(token_id, {}).get('usd')
        except Exception as e:
            logger.error(f"Error fetching from CoinGecko: {e}")
            return None
    
    def fetch_price_from_dexscreener(self, token_address: str) -> List[PriceData]:
        """从DexScreener获取价格"""
        try:
            url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            prices = []
            for pair in data.get('pairs', []):
                prices.append(PriceData(
                    dex=pair.get('dexId', 'unknown'),
                    chain=pair.get('chainId', 'unknown'),
                    token_pair=f"{pair.get('baseToken', {}).get('symbol')}/{pair.get('quoteToken', {}).get('symbol')}",
                    price=float(pair.get('priceUsd', 0)),
                    timestamp=datetime.now(),
                    volume_24h=pair.get('volume', {}).get('h24'),
                    liquidity=pair.get('liquidity', {}).get('usd')
                ))
            return prices
        except Exception as e:
            logger.error(f"Error fetching from DexScreener: {e}")
            return []
    
    def simulate_prices(self, token_pair: str) -> List[PriceData]:
        """模拟价格数据（演示用）"""
        import random
        
        base_prices = {
            'ETH/USDC': 3500,
            'WBTC/USDC': 65000,
            'LINK/USDC': 18.5,
            'UNI/USDC': 12.3,
            'AAVE/USDC': 145
        }
        
        base_price = base_prices.get(token_pair, 100)
        
        dex_configs = [
            ('Uniswap V3', 'ethereum', 0),
            ('SushiSwap', 'ethereum', 0.002),
            ('Curve', 'ethereum', -0.001),
            ('Uniswap V3', 'arbitrum', 0.001),
            ('SushiSwap', 'arbitrum', 0.003),
            ('Camelot', 'arbitrum', -0.002)
        ]
        
        prices = []
        for dex, chain, offset in dex_configs:
            noise = random.uniform(-0.005, 0.005)
            price = base_price * (1 + offset + noise)
            
            prices.append(PriceData(
                dex=dex,
                chain=chain,
                token_pair=token_pair,
                price=price,
                timestamp=datetime.now(),
                liquidity=random.uniform(1000000, 50000000)
            ))
        
        return prices
    
    def calculate_spreads(self, prices: List[PriceData]) -> List[SpreadAlert]:
        """计算价差"""
        alerts = []
        
        for i, buy_data in enumerate(prices):
            for j, sell_data in enumerate(prices):
                if i >= j:
                    continue
                
                if sell_data.price > buy_data.price:
                    spread_pct = (sell_data.price - buy_data.price) / buy_data.price * 100
                    
                    if spread_pct >= self.config.get('min_spread_pct', 0.5):
                        alert = SpreadAlert(
                            token_pair=buy_data.token_pair,
                            buy_dex=buy_data.dex,
                            sell_dex=sell_data.dex,
                            buy_price=buy_data.price,
                            sell_price=sell_data.price,
                            spread_pct=spread_pct,
                            timestamp=datetime.now()
                        )
                        alerts.append(alert)
        
        alerts.sort(key=lambda x: x.spread_pct, reverse=True)
        return alerts
    
    def check_price_thresholds(self, prices: List[PriceData]):
        """检查价格阈值"""
        thresholds = self.config.get('price_thresholds', [])
        
        for price_data in prices:
            for threshold in thresholds:
                if price_data.token_pair == threshold['token_pair']:
                    if threshold['condition'] == 'above' and price_data.price > threshold['price']:
                        self.trigger_alert('price_above', price_data, threshold)
                    elif threshold['condition'] == 'below' and price_data.price < threshold['price']:
                        self.trigger_alert('price_below', price_data, threshold)
    
    def trigger_alert(self, alert_type: str, data, config):
        """触发预警"""
        for handler in self.alert_handlers:
            try:
                handler(alert_type, data, config)
            except Exception as e:
                logger.error(f"Alert handler error: {e}")
    
    def print_price_table(self, prices: List[PriceData]):
        """打印价格表"""
        print(f"\n{'='*80}")
        print(f"📊 {prices[0].token_pair} 实时价格对比")
        print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        print(f"{'DEX':<20} {'链':<15} {'价格(USD)':<15} {'流动性':<15} {'差异':<10}")
        print(f"{'-'*80}")
        
        # 找基准价格
        base_price = prices[0].price
        
        for p in prices:
            diff = (p.price - base_price) / base_price * 100
            liquidity_str = f"${p.liquidity:,.0f}" if p.liquidity else "N/A"
            print(f"{p.dex:<20} {p.chain:<15} ${p.price:<14.2f} {liquidity_str:<15} {diff:+.2f}%")
        
        print(f"{'='*80}")
    
    def print_spread_alerts(self, alerts: List[SpreadAlert]):
        """打印价差预警"""
        if not alerts:
            return
        
        print(f"\n🔔 发现 {len(alerts)} 个套利机会")
        print(f"{'='*80}")
        
        for alert in alerts[:5]:  # 只显示前5个
            print(f"\n{alert.token_pair}")
            print(f"  买入: {alert.buy_dex} @ ${alert.buy_price:.2f}")
            print(f"  卖出: {alert.sell_dex} @ ${alert.sell_price:.2f}")
            print(f"  价差: {alert.spread_pct:.2f}%")
        
        print(f"{'='*80}\n")
    
    def monitor_once(self):
        """单次监控"""
        all_prices = []
        
        for token_pair in self.config.get('token_pairs', []):
            # 获取价格（使用模拟数据演示）
            prices = self.simulate_prices(token_pair)
            all_prices.extend(prices)
            
            # 存储历史
            if token_pair not in self.price_history:
                self.price_history[token_pair] = []
            self.price_history[token_pair].extend(prices)
            
            # 限制历史记录大小
            max_history = self.config.get('max_history', 1000)
            if len(self.price_history[token_pair]) > max_history:
                self.price_history[token_pair] = self.price_history[token_pair][-max_history:]
        
        # 显示价格表
        for token_pair in self.config.get('token_pairs', []):
            pair_prices = [p for p in all_prices if p.token_pair == token_pair]
            if pair_prices:
                self.print_price_table(pair_prices)
        
        # 检查价差
        alerts = self.calculate_spreads(all_prices)
        if alerts:
            self.print_spread_alerts(alerts)
            for alert in alerts:
                self.trigger_alert('spread', alert, {})
        
        # 检查价格阈值
        self.check_price_thresholds(all_prices)
    
    def start(self):
        """开始监控"""
        self.running = True
        interval = self.config.get('interval', 10)
        
        logger.info(f"🚀 启动DEX价格监控")
        logger.info(f"   监控交易对: {self.config.get('token_pairs', [])}")
        logger.info(f"   检查间隔: {interval}秒")
        logger.info(f"   最小关注价差: {self.config.get('min_spread_pct', 0.5)}%")
        logger.info(f"   按Ctrl+C停止\n")
        
        try:
            while self.running and not self.stop_event.is_set():
                self.monitor_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("\n⏹️  监控已停止")
            self.stop()
    
    def stop(self):
        """停止监控"""
        self.running = False
        self.stop_event.set()
        logger.info("监控已停止")
    
    def save_data(self, filename: str):
        """保存数据到文件"""
        data = {
            'price_history': {
                pair: [
                    {
                        'dex': p.dex,
                        'chain': p.chain,
                        'price': p.price,
                        'timestamp': p.timestamp.isoformat(),
                        'liquidity': p.liquidity
                    }
                    for p in prices
                ]
                for pair, prices in self.price_history.items()
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"数据已保存到: {filename}")


# 示例预警处理器
def console_alert_handler(alert_type: str, data, config):
    """控制台预警处理器"""
    if alert_type == 'spread':
        alert = data
        print(f"\n🔔 套利预警: {alert.token_pair}")
        print(f"   {alert.buy_dex} -> {alert.sell_dex}: {alert.spread_pct:.2f}%")
    elif alert_type in ['price_above', 'price_below']:
        price_data = data
        condition = '突破' if alert_type == 'price_above' else '跌破'
        print(f"\n🚨 价格预警: {price_data.token_pair} {condition} ${config['price']}")
        print(f"   当前价格: ${price_data.price:.2f}")


def demo():
    """演示"""
    print("🤖 DEX实时价格监控器")
    print("="*80)
    
    config = {
        'token_pairs': ['ETH/USDC', 'WBTC/USDC', 'LINK/USDC'],
        'interval': 10,
        'min_spread_pct': 0.3,
        'max_history': 100,
        'price_thresholds': [
            {
                'token_pair': 'ETH/USDC',
                'condition': 'above',
                'price': 3600
            }
        ]
    }
    
    monitor = DEXPriceMonitor(config)
    monitor.add_alert_handler(console_alert_handler)
    
    # 运行30秒演示
    print("\n⏱️  运行30秒演示...\n")
    
    def stop_after_timeout():
        time.sleep(30)
        monitor.stop()
    
    # 启动定时停止线程
    stop_thread = Thread(target=stop_after_timeout)
    stop_thread.daemon = True
    stop_thread.start()
    
    monitor.start()
    
    # 保存数据
    monitor.save_data('price_monitor_data.json')


if __name__ == "__main__":
    demo()
