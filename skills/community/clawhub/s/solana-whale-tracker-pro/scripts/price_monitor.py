#!/usr/bin/env python3
"""
Solana Monitor - 价格监控模块
实时监控 Solana 代币价格，支持价格警报

版本：v0.1.0
作者：VIC ai-company
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

# CoinGecko API（免费，无需 API Key）
COINGECKO_API = "https://api.coingecko.com/api/v3"

class PriceMonitor:
    """Solana 代币价格监控器"""
    
    def __init__(self):
        self.supported_tokens = {
            'solana': 'sol',
            'bitcoin': 'btc',
            'ethereum': 'eth',
            'usd-coin': 'usdc',
            'tether': 'usdt',
        }
        self.price_cache = {}
        self.last_update = None
    
    def get_price(self, token_id: str, currency: str = 'usd') -> Optional[float]:
        """
        获取代币当前价格
        
        Args:
            token_id: CoinGecko 代币 ID（如 'solana'）
            currency: 货币单位（usd/eur/hkd）
        
        Returns:
            价格（float）或 None
        """
        try:
            url = f"{COINGECKO_API}/simple/price"
            params = {
                'ids': token_id,
                'vs_currencies': currency,
                'include_24hr_change': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            price = data.get(token_id, {}).get(currency)
            
            if price:
                self.price_cache[token_id] = {
                    'price': price,
                    'change_24h': data.get(token_id, {}).get(f'{currency}_24h_change', 0),
                    'timestamp': datetime.now().isoformat()
                }
                self.last_update = datetime.now()
            
            return price
            
        except Exception as e:
            print(f"❌ 获取价格失败：{e}")
            return None
    
    def get_sol_price(self) -> Optional[float]:
        """获取 SOL 当前价格"""
        return self.get_price('solana')
    
    def get_multiple_prices(self, token_ids: List[str]) -> Dict:
        """
        批量获取多个代币价格
        
        Args:
            token_ids: 代币 ID 列表
        
        Returns:
            价格字典
        """
        try:
            url = f"{COINGECKO_API}/simple/price"
            params = {
                'ids': ','.join(token_ids),
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"❌ 批量获取价格失败：{e}")
            return {}
    
    def check_price_alert(self, token_id: str, target_price: float, condition: str = 'above') -> bool:
        """
        检查价格是否达到警报条件
        
        Args:
            token_id: 代币 ID
            target_price: 目标价格
            condition: 'above'（高于）或 'below'（低于）
        
        Returns:
            是否触发警报
        """
        current_price = self.get_price(token_id)
        
        if current_price is None:
            return False
        
        if condition == 'above':
            triggered = current_price >= target_price
        elif condition == 'below':
            triggered = current_price <= target_price
        else:
            return False
        
        if triggered:
            print(f"🚨 价格警报！{token_id}")
            print(f"   当前价格：${current_price:.2f}")
            print(f"   目标价格：${target_price:.2f}")
            print(f"   条件：{condition}")
        
        return triggered


class PriceAlert:
    """价格警报管理器"""
    
    def __init__(self):
        self.alerts = []
    
    def add_alert(self, token_id: str, target_price: float, condition: str, 
                  notification_channel: str = 'telegram') -> Dict:
        """
        添加价格警报
        
        Args:
            token_id: 代币 ID
            target_price: 目标价格
            condition: 'above' 或 'below'
            notification_channel: 通知渠道（telegram/email）
        
        Returns:
            警报配置
        """
        alert = {
            'id': len(self.alerts) + 1,
            'token_id': token_id,
            'target_price': target_price,
            'condition': condition,
            'notification_channel': notification_channel,
            'active': True,
            'created_at': datetime.now().isoformat(),
            'triggered': False
        }
        
        self.alerts.append(alert)
        print(f"✅ 警报已添加：{alert['id']}")
        print(f"   代币：{token_id}")
        print(f"   条件：{condition} ${target_price:.2f}")
        
        return alert
    
    def remove_alert(self, alert_id: int) -> bool:
        """移除警报"""
        for i, alert in enumerate(self.alerts):
            if alert['id'] == alert_id:
                self.alerts.pop(i)
                print(f"✅ 警报 {alert_id} 已移除")
                return True
        print(f"❌ 未找到警报 {alert_id}")
        return False
    
    def list_alerts(self) -> List[Dict]:
        """列出所有警报"""
        return self.alerts
    
    def check_all_alerts(self, monitor: PriceMonitor) -> List[Dict]:
        """
        检查所有警报是否触发
        
        Returns:
            触发的警报列表
        """
        triggered = []
        
        for alert in self.alerts:
            if not alert['active']:
                continue
            
            is_triggered = monitor.check_price_alert(
                alert['token_id'],
                alert['target_price'],
                alert['condition']
            )
            
            if is_triggered:
                alert['triggered'] = True
                triggered.append(alert)
        
        return triggered


def main():
    """测试示例"""
    print("🔍 Solana Monitor - 价格监控测试")
    print("=" * 50)
    
    # 创建监控器
    monitor = PriceMonitor()
    
    # 获取 SOL 价格
    print("\n📊 获取 SOL 当前价格...")
    sol_price = monitor.get_sol_price()
    
    if sol_price:
        print(f"✅ SOL 价格：${sol_price:.2f} USD")
    else:
        print("❌ 无法获取价格")
    
    # 获取多个代币价格
    print("\n📊 获取多个代币价格...")
    tokens = ['solana', 'bitcoin', 'ethereum']
    prices = monitor.get_multiple_prices(tokens)
    
    for token in tokens:
        if token in prices:
            price = prices[token].get('usd', 0)
            change = prices[token].get('usd_24h_change', 0)
            print(f"  {token.upper()}: ${price:,.2f} ({change:+.2f}%)")
    
    # 测试警报系统
    print("\n🔔 测试价格警报...")
    alert_manager = PriceAlert()
    
    # 添加警报（假设 SOL 当前 $87，设置 $90 警报）
    if sol_price:
        alert_manager.add_alert('solana', sol_price * 1.05, 'above')  # 上涨 5%
        alert_manager.add_alert('solana', sol_price * 0.95, 'below')  # 下跌 5%
    
    # 列出警报
    print("\n📋 当前警报列表:")
    for alert in alert_manager.list_alerts():
        print(f"  [{alert['id']}] {alert['token_id']} {alert['condition']} ${alert['target_price']:.2f}")
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！")


if __name__ == "__main__":
    main()
