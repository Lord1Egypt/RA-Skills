#!/usr/bin/env python3
"""
Solana Monitor - 大额转账监控模块
实时监控 Solana 链上大额转账，发送警报

版本：v0.1.0
作者：VIC ai-company
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

# Solana RPC 节点（公共免费）
SOLANA_RPC = "https://api.mainnet-beta.solana.com"

class WhaleMonitor:
    """Solana 大额转账监控器"""
    
    def __init__(self, threshold_sol: float = 100.0):
        """
        初始化监控器
        
        Args:
            threshold_sol: 大额转账阈值（SOL）
        """
        self.threshold_sol = threshold_sol
        self.monitored_addresses = []
        self.last_signature = None
    
    def get_recent_transactions(self, limit: int = 10) -> List[Dict]:
        """
        获取最近交易
        
        Args:
            limit: 获取交易数量
        
        Returns:
            交易列表
        """
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getSignaturesForAddress",
                "params": [
                    "Vote111111111111111111111111111111111111111",  # Solana 投票账户
                    {"limit": limit}
                ]
            }
            
            response = requests.post(SOLANA_RPC, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('result', [])
            
        except Exception as e:
            print(f"❌ 获取交易失败：{e}")
            return []
    
    def get_transaction_details(self, signature: str) -> Optional[Dict]:
        """
        获取交易详情
        
        Args:
            signature: 交易签名
        
        Returns:
            交易详情
        """
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTransaction",
                "params": [
                    signature,
                    {"encoding": "jsonParsed"}
                ]
            }
            
            response = requests.post(SOLANA_RPC, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('result')
            
        except Exception as e:
            print(f"❌ 获取交易详情失败：{e}")
            return None
    
    def analyze_transaction(self, tx_data: Dict) -> Optional[Dict]:
        """
        分析交易是否为大额转账
        
        Args:
            tx_data: 交易数据
        
        Returns:
            分析结果
        """
        if not tx_data:
            return None
        
        try:
            # 解析交易信息
            meta = tx_data.get('meta', {})
            transaction = tx_data.get('transaction', {})
            
            # 获取转账金额
            pre_balances = meta.get('preBalances', [])
            post_balances = meta.get('postBalances', [])
            
            # 计算余额变化
            changes = []
            for i in range(len(pre_balances)):
                change = post_balances[i] - pre_balances[i]
                if abs(change) > self.threshold_sol * 1e9:  # 转换为 lamports
                    changes.append({
                        'index': i,
                        'change_sol': change / 1e9,
                        'change_lamports': change
                    })
            
            if changes:
                # 获取账户地址
                account_keys = tx_data.get('transaction', {}).get('message', {}).get('accountKeys', [])
                
                return {
                    'signature': tx_data.get('signatures', ['Unknown'])[0],
                    'timestamp': tx_data.get('blockTime', 0),
                    'changes': changes,
                    'accounts': account_keys,
                    'is_whale': True
                }
            
            return None
            
        except Exception as e:
            print(f"❌ 分析交易失败：{e}")
            return None
    
    def monitor_continuous(self, interval: int = 60):
        """
        持续监控
        
        Args:
            interval: 检查间隔（秒）
        """
        print(f"🐋 开始监控大额转账（阈值：{self.threshold_sol} SOL）")
        print(f"检查间隔：{interval}秒\n")
        
        while True:
            try:
                # 获取最近交易
                transactions = self.get_recent_transactions(limit=5)
                
                for tx in transactions:
                    signature = tx.get('signature')
                    
                    # 跳过已处理的交易
                    if signature == self.last_signature:
                        break
                    
                    # 获取交易详情
                    tx_data = self.get_transaction_details(signature)
                    
                    # 分析交易
                    result = self.analyze_transaction(tx_data)
                    
                    if result and result['is_whale']:
                        print(f"\n🚨 大额转账检测到！")
                        print(f"签名：{result['signature']}")
                        print(f"时间：{datetime.fromtimestamp(result['timestamp'])}")
                        
                        for change in result['changes']:
                            print(f"金额：{change['change_sol']:.2f} SOL")
                            if change['change_sol'] > 0:
                                print(f"方向：接收 💰")
                            else:
                                print(f"方向：发送 💸")
                        
                        # 这里可以添加通知发送逻辑
                        # notifier.send_whale_alert(...)
                    
                    # 更新最后处理的签名
                    self.last_signature = signature
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n⏹️  监控已停止")
                break
            except Exception as e:
                print(f"❌ 监控错误：{e}")
                time.sleep(interval)


class AddressMonitor:
    """特定地址监控器"""
    
    def __init__(self):
        self.watchlist = []
    
    def add_address(self, address: str, label: str = ""):
        """
        添加监控地址
        
        Args:
            address: Solana 地址
            label: 地址标签（如：交易所、巨鲸等）
        """
        self.watchlist.append({
            'address': address,
            'label': label,
            'added_at': datetime.now().isoformat()
        })
        print(f"✅ 已添加监控地址：{address[:16]}... ({label})")
    
    def remove_address(self, address: str):
        """移除监控地址"""
        self.watchlist = [a for a in self.watchlist if a['address'] != address]
        print(f"✅ 已移除监控地址：{address[:16]}...")
    
    def list_addresses(self):
        """列出所有监控地址"""
        print(f"\n📋 监控地址列表 ({len(self.watchlist)}个):\n")
        for addr in self.watchlist:
            print(f"  • {addr['address'][:16]}...{addr['address'][-8:]}")
            print(f"    标签：{addr['label']}")
            print(f"    添加：{addr['added_at']}\n")


def main():
    """测试示例"""
    print("🐋 Solana Monitor - 大额转账监控测试")
    print("=" * 50)
    
    # 创建监控器
    whale_monitor = WhaleMonitor(threshold_sol=100.0)
    
    # 测试获取交易
    print("\n📊 获取最近交易...")
    transactions = whale_monitor.get_recent_transactions(limit=5)
    
    if transactions:
        print(f"✅ 获取到 {len(transactions)} 笔交易")
        for tx in transactions[:3]:
            print(f"  - {tx.get('signature', 'Unknown')[:16]}...")
    else:
        print("❌ 无法获取交易")
    
    # 测试地址监控
    print("\n📋 测试地址监控...")
    address_monitor = AddressMonitor()
    
    # 添加示例地址（Binance 热钱包）
    address_monitor.add_address(
        "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
        "Binance Hot Wallet"
    )
    
    address_monitor.list_addresses()
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！")
    print("\n💡 提示：运行 monitor_continuous() 开始持续监控")


if __name__ == "__main__":
    main()
