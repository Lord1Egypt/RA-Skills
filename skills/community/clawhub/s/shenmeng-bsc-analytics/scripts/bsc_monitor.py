#!/usr/bin/env python3
"""
BSC 生态监控器
监控 BNB Chain 的关键指标
"""

import json
from datetime import datetime
from typing import Dict, List


class BSCMonitor:
    """BSC 监控器"""
    
    def __init__(self):
        self.protocols = {
            'pancakeswap': {
                'name': 'PancakeSwap',
                'category': 'DEX',
                'tvl': 2_500_000_000,
                'token': 'CAKE',
                'apy': 15.5
            },
            'venus': {
                'name': 'Venus',
                'category': 'Lending',
                'tvl': 1_200_000_000,
                'token': 'XVS',
                'apy': 8.2
            },
            'alpaca': {
                'name': 'Alpaca Finance',
                'category': 'Leveraged Farming',
                'tvl': 400_000_000,
                'token': 'ALPACA',
                'apy': 22.5
            },
            'biswap': {
                'name': 'Biswap',
                'category': 'DEX',
                'tvl': 200_000_000,
                'token': 'BSW',
                'apy': 35.0
            },
            'beefy': {
                'name': 'Beefy Finance',
                'category': 'Yield Aggregator',
                'tvl': 400_000_000,
                'token': 'BIFI',
                'apy': 18.0
            }
        }
    
    def get_ecosystem_overview(self) -> Dict:
        """获取生态概览"""
        total_tvl = sum(p['tvl'] for p in self.protocols.values())
        
        return {
            'timestamp': datetime.now().isoformat(),
            'chain': 'BNB Chain',
            'total_tvl': total_tvl,
            'total_tvl_formatted': f"${total_tvl/1e9:.2f}B",
            'protocol_count': len(self.protocols),
            'categories': self._get_category_breakdown(),
            'top_protocols': self._get_top_protocols(5),
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
    
    def analyze_protocol(self, protocol_id: str) -> Dict:
        """分析特定协议"""
        if protocol_id not in self.protocols:
            return {'error': f'Protocol {protocol_id} not found'}
        
        p = self.protocols[protocol_id]
        total_tvl = sum(proto['tvl'] for proto in self.protocols.values())
        market_share = p['tvl'] / total_tvl * 100
        
        return {
            'name': p['name'],
            'category': p['category'],
            'tvl': p['tvl'],
            'market_share': market_share,
            'token': p['token'],
            'apy': p.get('apy', 0),
            'risk_level': self._assess_risk(p),
            'recommendation': self._generate_recommendation(p, market_share)
        }
    
    def _assess_risk(self, protocol: Dict) -> str:
        """评估风险等级"""
        tvl = protocol.get('tvl', 0)
        apy = protocol.get('apy', 0)
        
        if tvl > 1_000_000_000 and apy < 20:
            return 'Low'
        elif tvl > 200_000_000 and apy < 40:
            return 'Medium'
        else:
            return 'High'
    
    def _generate_recommendation(self, protocol: Dict, market_share: float) -> str:
        """生成投资建议"""
        if market_share > 30:
            return "🟢 龙头协议，生态地位稳固，适合稳健配置"
        elif market_share > 10:
            return "🟡 主流协议，有竞争力，可考虑配置"
        elif protocol.get('apy', 0) > 30:
            return "🟠 收益较高但风险较大，建议小额参与"
        else:
            return "🔵 新兴协议，可观察等待"
    
    def find_yield_opportunities(self, min_apy: float = 10) -> List[Dict]:
        """发现收益机会"""
        opportunities = []
        
        for protocol_id, p in self.protocols.items():
            apy = p.get('apy', 0)
            if apy >= min_apy:
                opportunities.append({
                    'protocol': p['name'],
                    'token': p['token'],
                    'apy': apy,
                    'tvl': p['tvl'],
                    'risk': self._assess_risk(p),
                    'category': p['category']
                })
        
        return sorted(opportunities, key=lambda x: x['apy'], reverse=True)
    
    def format_overview_report(self, data: Dict) -> str:
        """格式化概览报告"""
        report = f"""
{'='*70}
🟨 BSC 生态监控报告
⏰ 更新时间: {data['timestamp']}
{'='*70}

📊 核心指标:
  • 总 TVL: {data['total_tvl_formatted']}
  • 协议数量: {data['protocol_count']}
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
        
        report += f"\n{'='*70}\n"
        return report
    
    def format_protocol_report(self, data: Dict) -> str:
        """格式化协议报告"""
        if 'error' in data:
            return f"❌ {data['error']}"
        
        report = f"""
{'='*70}
📝 {data['name']} 协议分析报告
{'='*70}

📋 基本信息:
  • 类别: {data['category']}
  • 代币: {data['token']}
  • TVL: ${data['tvl']/1e9:.2f}B
  • 市场份额: {data['market_share']:.1f}%

💰 收益:
  • APY: {data['apy']:.1f}%
  • 风险等级: {data['risk_level']}

💡 投资建议:
  {data['recommendation']}

{'='*70}
"""
        return report


def main():
    """主函数"""
    monitor = BSCMonitor()
    
    # 生态概览
    overview = monitor.get_ecosystem_overview()
    print(monitor.format_overview_report(overview))
    
    # PancakeSwap 分析
    pancake = monitor.analyze_protocol('pancakeswap')
    print(monitor.format_protocol_report(pancake))
    
    # 高收益机会
    print("\n🎯 高收益机会 (APY > 20%):\n")
    opportunities = monitor.find_yield_opportunities(min_apy=20)
    for opp in opportunities:
        print(f"  • {opp['protocol']} ({opp['token']}): {opp['apy']:.1f}% APY - {opp['risk']} Risk")
    
    # 保存数据
    output_file = f"/tmp/bsc_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(overview, f, indent=2)
    print(f"\n💾 数据已保存: {output_file}")


if __name__ == '__main__':
    main()
