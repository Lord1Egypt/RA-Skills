#!/usr/bin/env python3
"""
持仓分析器 - 分析鲸鱼持仓变化和盈亏
"""

import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Holding:
    """持仓记录"""
    token: str
    amount: float
    avg_cost: float
    current_price: float
    current_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float

@dataclass
class Trade:
    """交易记录"""
    timestamp: datetime
    token: str
    action: str  # 'buy' or 'sell'
    amount: float
    price: float
    value: float

@dataclass
class HoldingReport:
    """持仓报告"""
    address: str
    total_value: float
    total_cost: float
    total_unrealized_pnl: float
    holdings: List[Holding]
    recent_trades: List[Trade]
    pnl_history: List[Dict]

class HoldingAnalyzer:
    """持仓分析器"""
    
    def __init__(self):
        self.price_cache: Dict[str, float] = {}
    
    def get_token_price(self, token: str) -> float:
        """获取代币价格（简化版）"""
        if token not in self.price_cache:
            # 模拟价格
            prices = {
                'ETH': 3500,
                'BTC': 65000,
                'WBTC': 65000,
                'USDC': 1,
                'USDT': 1,
                'LINK': 18,
                'UNI': 12,
                'AAVE': 145
            }
            self.price_cache[token] = prices.get(token, 1)
        
        return self.price_cache[token]
    
    def fetch_trade_history(self, address: str, days: int = 30) -> List[Trade]:
        """获取交易历史（模拟）"""
        import random
        
        trades = []
        base_time = datetime.now() - timedelta(days=days)
        
        tokens = ['ETH', 'LINK', 'UNI', 'AAVE']
        
        for i in range(random.randint(20, 50)):
            trade_time = base_time + timedelta(hours=random.uniform(0, days * 24))
            
            token = random.choice(tokens)
            action = random.choice(['buy', 'sell'])
            
            base_price = self.get_token_price(token)
            # 模拟历史价格（有波动）
            price = base_price * random.uniform(0.7, 1.3)
            amount = random.uniform(10, 1000)
            
            trade = Trade(
                timestamp=trade_time,
                token=token,
                action=action,
                amount=amount,
                price=price,
                value=amount * price
            )
            
            trades.append(trade)
        
        # 按时间排序
        trades.sort(key=lambda x: x.timestamp)
        return trades
    
    def calculate_holdings(self, trades: List[Trade]) -> List[Holding]:
        """计算当前持仓"""
        # 按代币分组计算
        token_trades = defaultdict(list)
        for trade in trades:
            token_trades[trade.token].append(trade)
        
        holdings = []
        
        for token, token_trade_list in token_trades.items():
            current_amount = 0
            total_cost = 0
            
            for trade in token_trade_list:
                if trade.action == 'buy':
                    current_amount += trade.amount
                    total_cost += trade.value
                else:  # sell
                    # 简化：按比例减少成本
                    if current_amount > 0:
                        cost_reduction = (trade.amount / current_amount) * total_cost
                        total_cost -= cost_reduction
                    current_amount -= trade.amount
            
            if current_amount > 0:
                avg_cost = total_cost / current_amount if current_amount > 0 else 0
                current_price = self.get_token_price(token)
                current_value = current_amount * current_price
                
                unrealized_pnl = current_value - total_cost
                unrealized_pnl_pct = (unrealized_pnl / total_cost * 100) if total_cost > 0 else 0
                
                holding = Holding(
                    token=token,
                    amount=current_amount,
                    avg_cost=avg_cost,
                    current_price=current_price,
                    current_value=current_value,
                    unrealized_pnl=unrealized_pnl,
                    unrealized_pnl_pct=unrealized_pnl_pct
                )
                
                holdings.append(holding)
        
        # 按价值排序
        holdings.sort(key=lambda x: x.current_value, reverse=True)
        return holdings
    
    def calculate_pnl_history(self, trades: List[Trade]) -> List[Dict]:
        """计算PnL历史"""
        history = []
        running_pnl = 0
        
        # 按天聚合
        daily_pnl = defaultdict(float)
        
        for trade in trades:
            if trade.action == 'sell':
                # 简化为卖出一律盈利（实际应该计算成本）
                daily_pnl[trade.timestamp.date()] += trade.value * 0.1
        
        for date, pnl in sorted(daily_pnl.items()):
            running_pnl += pnl
            history.append({
                'date': date.isoformat(),
                'daily_pnl': pnl,
                'cumulative_pnl': running_pnl
            })
        
        return history
    
    def analyze_wallet(self, address: str, days: int = 30) -> HoldingReport:
        """分析钱包持仓"""
        trades = self.fetch_trade_history(address, days)
        holdings = self.calculate_holdings(trades)
        pnl_history = self.calculate_pnl_history(trades)
        
        total_value = sum(h.current_value for h in holdings)
        total_cost = sum(h.amount * h.avg_cost for h in holdings)
        total_unrealized_pnl = sum(h.unrealized_pnl for h in holdings)
        
        return HoldingReport(
            address=address,
            total_value=total_value,
            total_cost=total_cost,
            total_unrealized_pnl=total_unrealized_pnl,
            holdings=holdings,
            recent_trades=trades[-10:],  # 最近10笔
            pnl_history=pnl_history
        )
    
    def print_report(self, report: HoldingReport):
        """打印报告"""
        print(f"\n{'='*80}")
        print(f"💼 持仓分析报告: {report.address[:20]}...")
        print(f"{'='*80}")
        
        print(f"\n📊 总体情况:")
        print(f"   持仓总价值: ${report.total_value:,.2f}")
        print(f"   总成本: ${report.total_cost:,.2f}")
        
        pnl_emoji = "🟢" if report.total_unrealized_pnl > 0 else "🔴"
        pnl_sign = "+" if report.total_unrealized_pnl > 0 else ""
        print(f"   未实现盈亏: {pnl_emoji} {pnl_sign}${report.total_unrealized_pnl:,.2f}")
        
        if report.total_cost > 0:
            pnl_pct = report.total_unrealized_pnl / report.total_cost * 100
            print(f"   盈亏比例: {pnl_sign}{pnl_pct:.2f}%")
        
        print(f"\n💰 持仓明细:")
        print(f"   {'代币':<10} {'数量':<15} {'均价':<12} {'现价':<12} {'市值':<15} {'盈亏':<15}")
        print(f"   {'-'*80}")
        
        for h in report.holdings:
            pnl_emoji = "🟢" if h.unrealized_pnl > 0 else "🔴"
            pnl_str = f"{pnl_emoji} {h.unrealized_pnl:+,.0f} ({h.unrealized_pnl_pct:+.1f}%)"
            
            print(f"   {h.token:<10} {h.amount:<15,.2f} ${h.avg_cost:<11,.2f} "
                  f"${h.current_price:<11,.2f} ${h.current_value:<14,.0f} {pnl_str:<20}")
        
        print(f"\n📜 最近交易:")
        print(f"   {'时间':<20} {'动作':<8} {'代币':<8} {'数量':<12} {'价格':<12} {'金额':<15}")
        print(f"   {'-'*80}")
        
        for trade in report.recent_trades:
            emoji = "🟢" if trade.action == 'buy' else "🔴"
            print(f"   {trade.timestamp.strftime('%Y-%m-%d %H:%M'):<20} "
                  f"{emoji} {trade.action.upper():<5} {trade.token:<8} "
                  f"{trade.amount:<12,.2f} ${trade.price:<11,.2f} ${trade.value:<14,.0f}")
        
        print(f"{'='*80}\n")
    
    def detect_accumulation(self, trades: List[Trade]) -> Optional[Dict]:
        """检测积累模式"""
        recent_buys = [t for t in trades if t.action == 'buy' and 
                      t.timestamp > datetime.now() - timedelta(days=7)]
        
        if len(recent_buys) >= 5:
            total_bought = sum(t.value for t in recent_buys)
            return {
                'pattern': 'accumulation',
                'confidence': min(len(recent_buys) / 10, 1.0),
                'total_bought': total_bought,
                'buy_count': len(recent_buys),
                'message': f'过去7天内买入{len(recent_buys)}次，总计${total_bought:,.0f}'
            }
        
        return None


def demo():
    """演示"""
    print("💼 持仓分析器 - 演示")
    print("="*80)
    
    analyzer = HoldingAnalyzer()
    
    # 分析示例钱包
    address = "0x742d35Cc6634C0532925a3b8D4E6D3b6e8d3e8D3"
    
    print(f"\n🔍 分析钱包: {address}")
    report = analyzer.analyze_wallet(address, days=30)
    
    # 打印报告
    analyzer.print_report(report)
    
    # 检测积累模式
    accumulation = analyzer.detect_accumulation(report.recent_trades)
    if accumulation:
        print(f"\n🔍 检测到积累模式:")
        print(f"   {accumulation['message']}")
        print(f"   置信度: {accumulation['confidence']*100:.0f}%")
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
