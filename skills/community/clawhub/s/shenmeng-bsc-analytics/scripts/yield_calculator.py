#!/usr/bin/env python3
"""
BSC 收益计算器
计算 BSC DeFi 挖矿/质押收益
"""

import json
from datetime import datetime
from typing import Dict, List


class BSCYieldCalculator:
    """BSC 收益计算器"""
    
    def __init__(self):
        self.farms = {
            'pancakeswap-cake': {
                'name': 'PancakeSwap CAKE Pool',
                'apy': 15.5,
                'type': 'staking',
                'risk': 'low',
                'token': 'CAKE'
            },
            'pancakeswap-bnb-busd': {
                'name': 'PancakeSwap BNB-BUSD LP',
                'apy': 12.8,
                'type': 'lp',
                'risk': 'medium',
                'tokens': ['BNB', 'BUSD'],
                'impermanent_loss_risk': 'low'
            },
            'venus-bnb': {
                'name': 'Venus BNB Supply',
                'apy': 4.2,
                'type': 'lending',
                'risk': 'low',
                'token': 'BNB'
            },
            'alpaca-leveraged': {
                'name': 'Alpaca 3x Leveraged BNB',
                'apy': 28.5,
                'type': 'leveraged_farming',
                'risk': 'high',
                'token': 'BNB',
                'leverage': 3
            },
            'biswap-bnb-busd': {
                'name': 'Biswap BNB-BUSD LP',
                'apy': 35.0,
                'type': 'lp',
                'risk': 'medium',
                'tokens': ['BNB', 'BUSD'],
                'impermanent_loss_risk': 'low'
            },
            'beefy-auto': {
                'name': 'Beefy BNB-USDT Vault',
                'apy': 22.0,
                'type': 'auto_compound',
                'risk': 'medium',
                'tokens': ['BNB', 'USDT'],
                'compounds_per_day': 3
            },
            'ankr-staking': {
                'name': 'Ankr BNB Liquid Staking',
                'apy': 4.5,
                'type': 'liquid_staking',
                'risk': 'low',
                'token': 'BNB',
                'receives': 'ankrBNB'
            }
        }
    
    def calculate_yield(self, farm_id: str, amount: float, days: int = 365) -> Dict:
        """
        计算收益
        
        Args:
            farm_id: 农场 ID
            amount: 投资金额 (USD)
            days: 投资天数
            
        Returns:
            收益计算结果
        """
        if farm_id not in self.farms:
            return {'error': f'Farm {farm_id} not found'}
        
        farm = self.farms[farm_id]
        apy = farm['apy'] / 100
        
        # 计算收益
        daily_rate = apy / 365
        total_return = amount * (1 + daily_rate) ** days
        profit = total_return - amount
        
        # 考虑费用
        fees = self._estimate_fees(farm, amount)
        net_profit = profit - fees
        net_apy = (net_profit / amount) / (days / 365) * 100
        
        return {
            'farm': farm['name'],
            'amount': amount,
            'period_days': days,
            'gross_apy': farm['apy'],
            'gross_profit': profit,
            'fees': fees,
            'net_profit': net_profit,
            'net_apy': round(net_apy, 2),
            'total_value': amount + net_profit,
            'daily_yield': net_profit / days,
            'risk_level': farm['risk'],
            'warnings': self._generate_warnings(farm)
        }
    
    def _estimate_fees(self, farm: Dict, amount: float) -> float:
        """估算费用"""
        fees = 0
        
        if farm['type'] == 'lp':
            # LP 费用: 0.3% 交易费的一部分
            fees += amount * 0.001
        
        if farm['type'] == 'leveraged_farming':
            # 借贷利息
            leverage = farm.get('leverage', 1)
            borrow_amount = amount * (leverage - 1)
            fees += borrow_amount * 0.05  # 5% 年借贷成本
        
        if farm['type'] == 'auto_compound':
            # 自动复利费用
            fees += amount * 0.005
        
        # Gas 费用估算
        fees += 5  # 假设 $5 gas 成本
        
        return fees
    
    def _generate_warnings(self, farm: Dict) -> List[str]:
        """生成风险提示"""
        warnings = []
        
        if farm['risk'] == 'high':
            warnings.append("⚠️ 高风险策略，可能导致本金损失")
        
        if farm['type'] == 'lp':
            warnings.append("⚠️ 存在无常损失风险")
        
        if farm['type'] == 'leveraged_farming':
            warnings.append("⚠️ 杠杆操作，存在清算风险")
        
        if farm.get('apy', 0) > 50:
            warnings.append("⚠️ 超高收益通常不可持续")
        
        return warnings
    
    def compare_farms(self, amount: float, days: int = 365) -> List[Dict]:
        """对比所有农场"""
        results = []
        
        for farm_id, farm in self.farms.items():
            calc = self.calculate_yield(farm_id, amount, days)
            if 'error' not in calc:
                results.append({
                    'farm_id': farm_id,
                    'name': farm['name'],
                    'type': farm['type'],
                    'risk': farm['risk'],
                    'gross_apy': farm['apy'],
                    'net_apy': calc['net_apy'],
                    'net_profit': calc['net_profit'],
                    'daily_yield': calc['daily_yield']
                })
        
        return sorted(results, key=lambda x: x['net_apy'], reverse=True)
    
    def format_calculation(self, result: Dict) -> str:
        """格式化计算结果"""
        if 'error' in result:
            return f"❌ {result['error']}"
        
        report = f"""
{'='*70}
💰 {result['farm']} 收益计算
{'='*70}

📊 投资参数:
  • 投资金额: ${result['amount']:,.2f}
  • 投资周期: {result['period_days']} 天
  • 风险等级: {result['risk_level'].upper()}

📈 收益预估:
  • 名义 APY: {result['gross_apy']:.1f}%
  • 实际 APY: {result['net_apy']:.1f}%
  • 总收益: ${result['net_profit']:,.2f}
  • 日均收益: ${result['daily_yield']:.2f}
  • 期末总资产: ${result['total_value']:,.2f}

💸 费用:
  • 预估费用: ${result['fees']:.2f}
  • 毛利润: ${result['gross_profit']:,.2f}

"""
        if result['warnings']:
            report += "⚠️ 风险提示:\n"
            for w in result['warnings']:
                report += f"  {w}\n"
        
        report += f"\n{'='*70}\n"
        return report
    
    def format_comparison(self, results: List[Dict], amount: float, days: int) -> str:
        """格式化对比结果"""
        report = f"""
{'='*70}
📊 BSC 收益农场对比 (${amount:,.0f} × {days} 天)
{'='*70}

排名 | 农场名称 | 类型 | 风险 | 名义APY | 实际APY | 净收益
-----|----------|------|------|---------|---------|--------
"""
        for i, r in enumerate(results[:10], 1):
            report += f"{i:4} | {r['name'][:20]:20} | {r['type'][:10]:10} | {r['risk'][:6]:6} | {r['gross_apy']:6.1f}% | {r['net_apy']:6.1f}% | ${r['net_profit']:,.0f}\n"
        
        report += f"\n{'='*70}\n"
        return report


def main():
    """主函数"""
    calculator = BSCYieldCalculator()
    
    # 单个农场计算
    print("="*70)
    print("示例 1: PancakeSwap CAKE 质押 (投资 $1000, 365 天)")
    print("="*70)
    result = calculator.calculate_yield('pancakeswap-cake', 1000, 365)
    print(calculator.format_calculation(result))
    
    # 杠杆挖矿
    print("="*70)
    print("示例 2: Alpaca 3x 杠杆挖矿 (投资 $1000, 365 天)")
    print("="*70)
    result = calculator.calculate_yield('alpaca-leveraged', 1000, 365)
    print(calculator.format_calculation(result))
    
    # 农场对比
    print("="*70)
    print("农场收益对比 (投资 $1000, 365 天)")
    print("="*70)
    comparison = calculator.compare_farms(1000, 365)
    print(calculator.format_comparison(comparison, 1000, 365))


if __name__ == '__main__':
    main()
