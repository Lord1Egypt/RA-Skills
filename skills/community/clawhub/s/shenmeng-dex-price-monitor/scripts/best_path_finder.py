#!/usr/bin/env python3
"""
DEX最优交易路径查找器
找出最优的交易路径，获取最佳价格
"""

import requests
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class Chain(Enum):
    ETHEREUM = 1
    BSC = 56
    POLYGON = 137
    ARBITRUM = 42161
    OPTIMISM = 10
    BASE = 8453

@dataclass
class RouteQuote:
    """路由报价"""
    aggregator: str
    from_token: str
    to_token: str
    from_amount: float
    to_amount: float
    price: float
    gas_cost: Optional[float] = None
    path: Optional[List[str]] = None

class BestPathFinder:
    """最优路径查找器"""
    
    def __init__(self):
        self.results: List[RouteQuote] = []
    
    def get_1inch_quote(
        self,
        chain: Chain,
        from_token: str,
        to_token: str,
        amount: str,
        api_key: str
    ) -> Optional[RouteQuote]:
        """获取1inch报价"""
        try:
            url = f"https://api.1inch.dev/swap/v5.2/{chain.value}/quote"
            headers = {'Authorization': f'Bearer {api_key}'}
            params = {
                'src': from_token,
                'dst': to_token,
                'amount': amount
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            
            if 'toAmount' in data:
                return RouteQuote(
                    aggregator='1inch',
                    from_token=from_token,
                    to_token=to_token,
                    from_amount=int(amount) / 1e18,  # 假设18位小数
                    to_amount=int(data['toAmount']) / 1e6,  # USDC 6位小数
                    price=int(data['toAmount']) / int(amount),
                    gas_cost=data.get('estimatedGas'),
                    path=data.get('protocols', [])
                )
        except Exception as e:
            print(f"1inch API error: {e}")
        
        return None
    
    def get_0x_quote(
        self,
        chain: Chain,
        sell_token: str,
        buy_token: str,
        sell_amount: str
    ) -> Optional[RouteQuote]:
        """获取0x报价"""
        try:
            url = "https://api.0x.org/swap/v1/quote"
            params = {
                'sellToken': sell_token,
                'buyToken': buy_token,
                'sellAmount': sell_amount,
                'chainId': chain.value
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'buyAmount' in data:
                sell_amt = int(sell_amount)
                buy_amt = int(data['buyAmount'])
                
                return RouteQuote(
                    aggregator='0x',
                    from_token=sell_token,
                    to_token=buy_token,
                    from_amount=sell_amt / 1e18,
                    to_amount=buy_amt / 1e6,
                    price=buy_amt / sell_amt,
                    gas_cost=data.get('gas'),
                    path=[s.get('name') for s in data.get('sources', []) if s.get('proportion') > 0]
                )
        except Exception as e:
            print(f"0x API error: {e}")
        
        return None
    
    def get_paraswap_quote(
        self,
        chain: Chain,
        src_token: str,
        dest_token: str,
        amount: str
    ) -> Optional[RouteQuote]:
        """获取ParaSwap报价"""
        try:
            url = "https://api.paraswap.io/prices"
            params = {
                'srcToken': src_token,
                'destToken': dest_token,
                'amount': amount,
                'srcDecimals': 18,
                'destDecimals': 6,
                'network': chain.value
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'priceRoute' in data:
                route = data['priceRoute']
                return RouteQuote(
                    aggregator='ParaSwap',
                    from_token=src_token,
                    to_token=dest_token,
                    from_amount=int(amount) / 1e18,
                    to_amount=int(route['destAmount']) / 1e6,
                    price=int(route['destAmount']) / int(amount),
                    gas_cost=route.get('gasCostUSD'),
                    path=route.get('multiRoute', [])
                )
        except Exception as e:
            print(f"ParaSwap API error: {e}")
        
        return None
    
    def find_best_path(
        self,
        chain: Chain,
        from_token: str,
        to_token: str,
        amount: str,
        inch_api_key: Optional[str] = None
    ) -> Dict:
        """找出最优路径"""
        self.results = []
        
        print(f"🔍 查找最优路径...")
        print(f"   链: {chain.name}")
        print(f"   从: {from_token}")
        print(f"   到: {to_token}")
        print(f"   数量: {amount}\n")
        
        # 获取各聚合器报价
        quote_1inch = None
        if inch_api_key:
            quote_1inch = self.get_1inch_quote(chain, from_token, to_token, amount, inch_api_key)
            if quote_1inch:
                self.results.append(quote_1inch)
        
        quote_0x = self.get_0x_quote(chain, from_token, to_token, amount)
        if quote_0x:
            self.results.append(quote_0x)
        
        quote_paraswap = self.get_paraswap_quote(chain, from_token, to_token, amount)
        if quote_paraswap:
            self.results.append(quote_paraswap)
        
        return self.analyze_results()
    
    def analyze_results(self) -> Dict:
        """分析结果"""
        if not self.results:
            return {'error': '无法获取任何报价'}
        
        # 按输出数量排序
        sorted_results = sorted(self.results, key=lambda x: x.to_amount, reverse=True)
        best = sorted_results[0]
        worst = sorted_results[-1]
        
        analysis = {
            'best_aggregator': best.aggregator,
            'best_output': best.to_amount,
            'best_price': best.price,
            'savings_vs_worst': worst.to_amount - best.to_amount,
            'savings_pct': (worst.to_amount - best.to_amount) / worst.to_amount * 100,
            'all_quotes': [
                {
                    'aggregator': r.aggregator,
                    'output': r.to_amount,
                    'price': r.price,
                    'gas': r.gas_cost
                }
                for r in sorted_results
            ]
        }
        
        return analysis
    
    def print_comparison(self):
        """打印比较结果"""
        if not self.results:
            print("❌ 无可用报价")
            return
        
        print(f"\n{'='*70}")
        print(f"📊 DEX聚合器报价对比")
        print(f"{'='*70}")
        print(f"{'聚合器':<15} {'输出数量':<15} {'价格':<15} {'Gas':<15}")
        print(f"{'-'*70}")
        
        sorted_results = sorted(self.results, key=lambda x: x.to_amount, reverse=True)
        
        for i, r in enumerate(sorted_results):
            marker = "🥇" if i == 0 else "  "
            gas_str = f"{r.gas_cost:.0f}" if r.gas_cost else "N/A"
            print(f"{marker} {r.aggregator:<12} {r.to_amount:>12.4f} {r.price:>12.6f} {gas_str:<15}")
        
        best = sorted_results[0]
        worst = sorted_results[-1]
        savings = worst.to_amount - best.to_amount
        savings_pct = savings / worst.to_amount * 100
        
        print(f"{'='*70}")
        print(f"💡 最优选择: {best.aggregator}")
        print(f"💰 额外获得: {savings:.4f} ({savings_pct:.2f}%)")
        print(f"{'='*70}\n")
    
    def simulate_comparison(self) -> Dict:
        """模拟比较（无需API key）"""
        import random
        
        self.results = []
        
        base_output = 3500
        
        aggregators = [
            ('1inch', 1.002),
            ('0x', 0.998),
            ('ParaSwap', 1.001),
            ('OpenOcean', 0.999),
            ('KyberSwap', 1.000)
        ]
        
        for name, multiplier in aggregators:
            output = base_output * multiplier * (1 + random.uniform(-0.001, 0.001))
            
            self.results.append(RouteQuote(
                aggregator=name,
                from_token='ETH',
                to_token='USDC',
                from_amount=1.0,
                to_amount=output,
                price=output,
                gas_cost=random.randint(80000, 150000)
            ))
        
        return self.analyze_results()


def demo():
    """演示"""
    print("🛣️  DEX最优交易路径查找器 - 演示")
    print("="*70)
    
    finder = BestPathFinder()
    
    # 模拟比较（不需要API key）
    print("\n📝 模拟报价对比:\n")
    result = finder.simulate_comparison()
    finder.print_comparison()
    
    # 显示详细分析
    print("📊 详细分析:")
    print(f"  最优聚合器: {result['best_aggregator']}")
    print(f"  最佳输出: {result['best_output']:.4f}")
    print(f"  相比最差节省: {result['savings_vs_worst']:.4f} ({result['savings_pct']:.2f}%)")
    
    print("\n" + "="*70)
    print("💡 提示: 实际使用需要API key")
    print("   - 1inch: https://portal.1inch.dev/")
    print("   - 0x: 免费使用")
    print("   - ParaSwap: 免费使用")


if __name__ == "__main__":
    demo()
