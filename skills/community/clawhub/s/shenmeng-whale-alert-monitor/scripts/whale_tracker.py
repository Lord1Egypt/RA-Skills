#!/usr/bin/env python3
"""
鲸鱼追踪器 - 追踪特定鲸鱼钱包的所有活动
"""

import os
import json
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Transaction:
    """交易记录"""
    hash: str
    timestamp: datetime
    from_addr: str
    to_addr: str
    value: float
    token: str
    token_contract: Optional[str] = None
    gas_price: Optional[float] = None
    gas_used: Optional[int] = None

@dataclass
class WalletProfile:
    """钱包画像"""
    address: str
    label: Optional[str] = None
    first_seen: Optional[datetime] = None
    total_transactions: int = 0
    current_balance_eth: float = 0
    tokens: Dict[str, float] = field(default_factory=dict)
    transaction_history: List[Transaction] = field(default_factory=list)

class WhaleTracker:
    """鲸鱼追踪器"""
    
    def __init__(self):
        self.api_key = os.getenv('ETHERSCAN_API_KEY')
        self.wallets: Dict[str, WalletProfile] = {}
        self.load_wallet_labels()
    
    def load_wallet_labels(self):
        """加载钱包标签"""
        # 内置一些已知的交易所和机构地址
        self.labels = {
            '0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE': 'Binance Hot Wallet 1',
            '0xdB3c617cDd2fBf0c8611C04A49d34C7B332e2BB6': 'Binance Hot Wallet 2',
            '0x71660c4005BA85c37ccec55d0C4493E66Fe775d3': 'Coinbase',
            '0x2B6eD29a95753C3Ad948348e3e7b1A251039FBB9': 'KuCoin',
        }
    
    def get_label(self, address: str) -> Optional[str]:
        """获取地址标签"""
        return self.labels.get(address.lower())
    
    def add_wallet(self, address: str, label: Optional[str] = None):
        """添加要监控的钱包"""
        address = address.lower()
        
        if address not in self.wallets:
            self.wallets[address] = WalletProfile(
                address=address,
                label=label or self.get_label(address)
            )
            logger.info(f"✅ 已添加钱包: {label or address}")
        else:
            logger.warning(f"钱包已存在: {address}")
    
    def fetch_transactions(self, address: str, days: int = 7) -> List[Transaction]:
        """获取交易历史（模拟数据）"""
        import random
        
        transactions = []
        base_time = datetime.now() - timedelta(days=days)
        
        tokens = ['ETH', 'USDC', 'USDT', 'WBTC', 'LINK']
        
        # 生成10-30笔交易
        for i in range(random.randint(10, 30)):
            tx_time = base_time + timedelta(hours=random.uniform(0, days * 24))
            
            token = random.choice(tokens)
            
            # 生成价值
            if token == 'ETH':
                value = random.uniform(10, 5000)
            elif token in ['USDC', 'USDT']:
                value = random.uniform(10000, 5000000)
            elif token == 'WBTC':
                value = random.uniform(1, 100)
            else:
                value = random.uniform(100, 50000)
            
            tx = Transaction(
                hash=f"0x{''.join([random.choice('0123456789abcdef') for _ in range(64)])}",
                timestamp=tx_time,
                from_addr=address if random.random() > 0.5 else f"0x{''.join([random.choice('0123456789abcdef') for _ in range(40)])}",
                to_addr=f"0x{''.join([random.choice('0123456789abcdef') for _ in range(40)])}" if random.random() > 0.5 else address,
                value=value,
                token=token,
                gas_price=random.uniform(10, 100),
                gas_used=random.randint(21000, 200000)
            )
            
            transactions.append(tx)
        
        # 按时间排序
        transactions.sort(key=lambda x: x.timestamp, reverse=True)
        return transactions
    
    def analyze_wallet(self, address: str, days: int = 30) -> WalletProfile:
        """分析钱包"""
        address = address.lower()
        
        if address not in self.wallets:
            self.add_wallet(address)
        
        profile = self.wallets[address]
        
        # 获取交易
        transactions = self.fetch_transactions(address, days)
        profile.transaction_history = transactions
        profile.total_transactions = len(transactions)
        
        if transactions:
            profile.first_seen = min(t.timestamp for t in transactions)
        
        # 计算当前余额（简化）
        profile.current_balance_eth = random.uniform(100, 50000)
        
        # 计算代币持仓
        token_balances = defaultdict(float)
        for tx in transactions:
            if tx.to_addr.lower() == address:
                token_balances[tx.token] += tx.value
            elif tx.from_addr.lower() == address:
                token_balances[tx.token] -= tx.value
        
        profile.tokens = dict(token_balances)
        
        return profile
    
    def detect_patterns(self, profile: WalletProfile) -> Dict:
        """检测交易模式"""
        patterns = []
        
        # 检查是否有大量流入交易所
        exchange_outflows = [tx for tx in profile.transaction_history 
                            if self.get_label(tx.to_addr)]
        
        if len(exchange_outflows) > 3:
            total_to_exchange = sum(tx.value for tx in exchange_outflows 
                                   if tx.token == 'ETH')
            if total_to_exchange > 1000:
                patterns.append({
                    'type': 'distributing',
                    'description': f'频繁向交易所转账，总计 {total_to_exchange:.2f} ETH',
                    'severity': 'high'
                })
        
        # 检查积累模式
        recent_buys = [tx for tx in profile.transaction_history 
                      if tx.to_addr.lower() == profile.address.lower()]
        
        if len(recent_buys) > 5:
            patterns.append({
                'type': 'accumulating',
                'description': f'近期频繁买入，共 {len(recent_buys)} 笔交易',
                'severity': 'medium'
            })
        
        return {
            'patterns': patterns,
            'total_patterns': len(patterns)
        }
    
    def print_wallet_report(self, profile: WalletProfile):
        """打印钱包报告"""
        print(f"\n{'='*80}")
        print(f"🐋 鲸鱼钱包报告: {profile.label or profile.address}")
        print(f"{'='*80}")
        
        print(f"\n📋 基本信息:")
        print(f"   地址: {profile.address}")
        print(f"   标签: {profile.label or '未知'}")
        print(f"   首次活跃: {profile.first_seen.strftime('%Y-%m-%d') if profile.first_seen else '未知'}")
        print(f"   总交易数: {profile.total_transactions}")
        print(f"   ETH余额: {profile.current_balance_eth:,.2f}")
        
        print(f"\n💰 代币持仓:")
        for token, balance in profile.tokens.items():
            if balance != 0:
                emoji = "🟢" if balance > 0 else "🔴"
                print(f"   {emoji} {token}: {abs(balance):,.2f}")
        
        print(f"\n📜 最近交易 (Top 10):")
        print(f"   {'时间':<20} {'类型':<8} {'代币':<8} {'金额':<15} {'对手方':<20}")
        print(f"   {'-'*75}")
        
        for tx in profile.transaction_history[:10]:
            tx_type = "⬅️  接收" if tx.to_addr.lower() == profile.address.lower() else "➡️  发送"
            counterparty = tx.from_addr if tx_type == "⬅️  接收" else tx.to_addr
            counterparty_label = self.get_label(counterparty)
            counterparty_display = counterparty_label or f"{counterparty[:15]}..."
            
            print(f"   {tx.timestamp.strftime('%Y-%m-%d %H:%M'):<20} "
                  f"{tx_type:<8} {tx.token:<8} {tx.value:<15,.2f} {counterparty_display:<20}")
        
        # 检测模式
        patterns = self.detect_patterns(profile)
        if patterns['patterns']:
            print(f"\n🔍 检测到的模式:")
            for p in patterns['patterns']:
                emoji = "🔴" if p['severity'] == 'high' else "🟠"
                print(f"   {emoji} {p['type']}: {p['description']}")
        
        print(f"{'='*80}\n")
    
    def export_data(self, profile: WalletProfile, filename: str):
        """导出数据"""
        data = {
            'address': profile.address,
            'label': profile.label,
            'first_seen': profile.first_seen.isoformat() if profile.first_seen else None,
            'total_transactions': profile.total_transactions,
            'current_balance_eth': profile.current_balance_eth,
            'tokens': profile.tokens,
            'transactions': [
                {
                    'hash': tx.hash,
                    'timestamp': tx.timestamp.isoformat(),
                    'from': tx.from_addr,
                    'to': tx.to_addr,
                    'value': tx.value,
                    'token': tx.token
                }
                for tx in profile.transaction_history
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"数据已导出到: {filename}")


def demo():
    """演示"""
    print("🐋 鲸鱼追踪器 - 演示")
    print("="*80)
    
    tracker = WhaleTracker()
    
    # 添加示例钱包
    print("\n📝 添加示例钱包...")
    tracker.add_wallet("0x742d35Cc6634C0532925a3b8D4E6D3b6e8d3e8D3", "Smart Whale A")
    
    # 分析钱包
    print("\n📊 分析钱包...")
    profile = tracker.analyze_wallet("0x742d35Cc6634C0532925a3b8D4E6D3b6e8d3e8D3", days=30)
    
    # 打印报告
    tracker.print_wallet_report(profile)
    
    # 导出数据
    tracker.export_data(profile, 'whale_profile.json')
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
