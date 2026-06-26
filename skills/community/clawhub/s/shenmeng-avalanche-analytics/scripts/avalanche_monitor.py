#!/usr/bin/env python3
"""
Avalanche 生态监控器
监控 Avalanche C-Chain 和子网数据
"""

import json
from datetime import datetime
from typing import Dict, List


class AvalancheMonitor:
    """Avalanche 监控器"""
    
    def __init__(self):
        self.protocols = {
            'traderjoe': {
                'name': 'TraderJoe',
                'category': 'DEX',
                'tvl': 1_200_000_000,
                'token': 'JOE',
                'apy': 18.5
            },
            'aave': {
                'name': 'Aave V3',
                'category': 'Lending',
                'tvl': 800_000_000,
                'token': 'AAVE',
                'apy': 5.2
            },
            'benqi': {
                'name': 'Benqi',
                'category': 'Liquid Staking',
                'tvl': 400_000_000,
                'token': 'QI',
                'apy': 8.0
            },
            'gmx': {
                'name': 'GMX',
                'category': 'Derivatives',
                'tvl': 500_000_000,
                'token': 'GMX',
                'apy': 12.0
            },
            'curve': {
                'name': 'Curve',
                'category': 'DEX',
                'tvl': 300_000_000,
                'token': 'CRV',
                'apy': 6.5
            }
        }
        
        self.subnets = {
            'defi-kingdoms': {
                'name': 'DeFi Kingdoms',
                'type': 'GameFi',
                'token': 'JEWEL',
                'active': True
            },
            'dexalot': {
                'name': 'Dexalot',
                'type': 'DeFi',
                'token': 'ALOT',
                'active': True
            },
            'swimmer': {
                'name': 'Swimmer Network',
                'type': 'GameFi',
                'token': 'TUS',
                'active': True
            }
        }
    
    def get_ecosystem_overview(self) -> Dict:
        """获取生态概览"""
        total_tvl = sum(p['tvl'] for p in self.protocols.values())
        
        return {
            'timestamp': datetime.now().isoformat(),
            'chain': 'Avalanche',
            'total_tvl': total_tvl,
            'total_tvl_formatted': f"${total_tvl/1e9:.2f}B",
            'protocol_count': len(self.protocols),
            'subnet_count': len(self.subnets),
            'categories': self._get_category_breakdown(),
            'top_protocols': self._get_top_protocols(5),
            'subnets': list(self.subnets.values()),
            'avg_apy': sum(p.get('apy', 0) for p in self.protocols.values()) / len(self.protocols)
        }
    
    def _get_category_breakdown(self) -> Dict:
        """获取分类统计"""
        categories = {}
        for protocol in self.protocols.values():
            cat = protocol['category']
            if cat not in categories:
                categories[cat] = {'count': 0, 'tvl': 0}
            categories[cat]['count'] += 1
            categories[cat]['tvl'] += protocol['tvl']
        return categories
    
    def _get_top_protocols(self, n: int) -> List[Dict]:
        """获取头部协议"""
        sorted_protocols = sorted(
            self.protocols.items(),
            key=lambda x: x[1]['tvl'],
            reverse=True
        )[:n]
        
        return [
            {
                'name': p['name'],
                'category': p['category'],
                'tvl': p['tvl'],
                'tvl_formatted': f"${p['tvl']/1e9:.2f}B",
                'token': p['token'],
                'apy': p.get('apy', 0)
            }
            for _, p in sorted_protocols
        ]
    
    def calculate_validator_yield(self, stake_amount: float, 
                                   validator_fee: float = 0.05) -> Dict:
        """
        计算验证者收益
        
        Args:
            stake_amount: 质押 AVAX 数量 (最低 2000)
            validator_fee: 验证者收取的费用比例
        """
        min_stake = 2000
        
        if stake_amount < min_stake:
            return {'error': f'Minimum stake is {min_stake} AVAX'}
        
        # 估算参数
        base_apy = 0.08  # 8% 基础年化
        network_fee_yield = 0.02  # 2% 网络手续费收益
        
        # 计算收益
        gross_apy = base_apy + network_fee_yield
        net_apy = gross_apy * (1 - validator_fee)
        
        annual_yield = stake_amount * net_apy
        monthly_yield = annual_yield / 12
        
        # 运营成本估算
        server_cost_monthly = 150  # $150/月
        avax_price = 37  # $37/AVAX
        server_cost_avax = server_cost_monthly / avax_price
        
        net_monthly = monthly_yield - server_cost_avax
        
        return {
            'stake_amount': stake_amount,
            'gross_apy': gross_apy * 100,
            'validator_fee': validator_fee * 100,
            'net_apy': net_apy * 100,
            'annual_yield_avax': annual_yield,
            'annual_yield_usd': annual_yield * avax_price,
            'monthly_yield_avax': monthly_yield,
            'monthly_yield_usd': monthly_yield * avax_price,
            'server_cost_monthly': server_cost_avax,
            'server_cost_usd': server_cost_monthly,
            'net_monthly_avax': net_monthly,
            'net_monthly_usd': net_monthly * avax_price,
            'break_even_months': server_cost_monthly / (monthly_yield * avax_price) if monthly_yield > 0 else float('inf')
        }
    
    def format_overview_report(self, data: Dict) -> str:
        """格式化概览报告"""
        report = f"""
{'='*70}
🔺 Avalanche 生态监控报告
⏰ 更新时间: {data['timestamp']}
{'='*70}

📊 核心指标:
  • 总 TVL: {data['total_tvl_formatted']}
  • C-Chain 协议: {data['protocol_count']}
  • 活跃子网: {data['subnet_count']}
  • 平均 APY: {data['avg_apy']:.1f}%

"""
        # 分类统计
        report += "📈 分类统计:\n"
        for cat, stats in data['categories'].items():
            report += f"  • {cat}: {stats['count']} 个协议, ${stats['tvl']/1e9:.2f}B TVL\n"
        
        # 头部协议
        report += f"\n🏆 TVL 排名:\n"
        for i, p in enumerate(data['top_protocols'], 1):
            report += f"  {i}. {p['name']} ({p['token']}): {p['tvl_formatted']} - APY: {p['apy']:.1f}%\n"
        
        # 子网
        report += f"\n🔗 活跃子网:\n"
        for subnet in data['subnets']:
            status = "🟢" if subnet['active'] else "🔴"
            report += f"  {status} {subnet['name']} ({subnet['type']}) - Token: {subnet['token']}\n"
        
        report += f"\n{'='*70}\n"
        return report
    
    def format_validator_report(self, data: Dict) -> str:
        """格式化验证者报告"""
        if 'error' in data:
            return f"❌ {data['error']}"
        
        report = f"""
{'='*70}
🔺 Avalanche 验证者收益计算
{'='*70}

📊 质押参数:
  • 质押数量: {data['stake_amount']:,.0f} AVAX
  • 验证者费率: {data['validator_fee']:.1f}%

💰 收益预估:
  • 总年化收益率: {data['gross_apy']:.2f}%
  • 净年化收益率: {data['net_apy']:.2f}%
  • 年收益: {data['annual_yield_avax']:.2f} AVAX (${data['annual_yield_usd']:,.0f})
  • 月收益: {data['monthly_yield_avax']:.2f} AVAX (${data['monthly_yield_usd']:,.0f})

💸 成本:
  • 服务器成本: {data['server_cost_monthly']:.2f} AVAX/月 (${data['server_cost_usd']:.0f})

📈 净收益:
  • 月净收益: {data['net_monthly_avax']:.2f} AVAX (${data['net_monthly_usd']:,.0f})
  • 回本周期: {data['break_even_months']:.1f} 个月

{'='*70}
"""
        return report


def main():
    """主函数"""
    monitor = AvalancheMonitor()
    
    # 生态概览
    overview = monitor.get_ecosystem_overview()
    print(monitor.format_overview_report(overview))
    
    # 验证者收益计算 (2,000 AVAX)
    print("="*70)
    print("验证者收益计算 (2,000 AVAX 质押)")
    print("="*70)
    validator = monitor.calculate_validator_yield(2000)
    print(monitor.format_validator_report(validator))
    
    # 保存数据
    output_file = f"/tmp/avalanche_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(overview, f, indent=2)
    print(f"💾 数据已保存: {output_file}")


if __name__ == '__main__':
    main()
