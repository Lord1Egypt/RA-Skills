#!/usr/bin/env python3
"""
Solana 代币分析工具
用于分析 Solana 生态代币的基本面数据
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SolanaTokenAnalyzer:
    """Solana 代币分析器"""
    
    def __init__(self):
        self.risk_weights = {
            'team_allocation': 3,
            'low_liquidity': 2,
            'unverified_contract': 2,
            'new_token': 2,
            'no_social': 1
        }
    
    def analyze_token(self, token_data: Dict) -> Dict:
        """
        全面分析代币
        
        Args:
            token_data: 代币基本信息字典
            
        Returns:
            分析结果字典
        """
        result = {
            'token_name': token_data.get('name', 'Unknown'),
            'symbol': token_data.get('symbol', 'N/A'),
            'analysis_time': datetime.now().isoformat(),
            'health_score': self._calculate_health_score(token_data),
            'risk_level': self._assess_risk(token_data),
            'risk_factors': self._identify_risk_factors(token_data),
            'opportunity_signals': self._detect_signals(token_data),
            'recommendation': self._generate_recommendation(token_data)
        }
        return result
    
    def _calculate_health_score(self, data: Dict) -> int:
        """计算代币健康度分数 (0-100)"""
        score = 0
        
        # 流动性评分 (最高30分)
        liquidity = data.get('liquidity_usd', 0)
        if liquidity >= 1000000:
            score += 30
        elif liquidity >= 100000:
            score += 20
        elif liquidity >= 50000:
            score += 10
        else:
            score += 5
        
        # 持有者分布评分 (最高25分)
        top10 = data.get('top10_holder_percent', 100)
        if top10 <= 20:
            score += 25
        elif top10 <= 40:
            score += 15
        elif top10 <= 60:
            score += 10
        else:
            score += 5
        
        # 交易量评分 (最高25分)
        volume = data.get('volume_24h_usd', 0)
        if volume >= 10000000:
            score += 25
        elif volume >= 1000000:
            score += 20
        elif volume >= 100000:
            score += 15
        else:
            score += 5
        
        # 合约安全评分 (最高20分)
        if data.get('contract_verified', False):
            score += 20
        elif data.get('contract_audited', False):
            score += 15
        else:
            score += 5
        
        return min(score, 100)
    
    def _assess_risk(self, data: Dict) -> str:
        """评估风险等级"""
        risk_score = 0
        
        if data.get('team_allocation', 0) > 50:
            risk_score += 3
        if data.get('liquidity_usd', 0) < 50000:
            risk_score += 2
        if not data.get('contract_verified', False):
            risk_score += 2
        if data.get('age_days', 999) < 7:
            risk_score += 2
        if not data.get('has_social', False):
            risk_score += 1
        if data.get('dev_sold', False):
            risk_score += 3
            
        if risk_score >= 8:
            return 'EXTREME'
        elif risk_score >= 5:
            return 'HIGH'
        elif risk_score >= 3:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _identify_risk_factors(self, data: Dict) -> List[str]:
        """识别具体风险因素"""
        risks = []
        
        if data.get('team_allocation', 0) > 50:
            risks.append(f"团队/内部人持仓过高 ({data['team_allocation']}%)")
        
        if data.get('liquidity_usd', 0) < 50000:
            risks.append("流动性过低，易受价格操纵")
        
        if not data.get('contract_verified', False):
            risks.append("合约未验证，可能存在后门")
        
        if data.get('age_days', 999) < 7:
            risks.append("新币风险，无历史数据支撑")
        
        if data.get('dev_sold', False):
            risks.append("开发者已抛售代币")
        
        if data.get('mint_authority', True):
            risks.append("仍有增发权限，存在通胀风险")
            
        if data.get('freeze_authority', True):
            risks.append("仍有冻结权限，可能限制交易")
        
        return risks
    
    def _detect_signals(self, data: Dict) -> List[Dict]:
        """检测机会信号"""
        signals = []
        
        # 突破信号
        if data.get('price_change_24h', 0) > 50:
            signals.append({
                'type': '价格异动',
                'level': 'high' if data['price_change_24h'] > 100 else 'medium',
                'description': f"24h涨幅 {data['price_change_24h']:.1f}%"
            })
        
        # 放量信号
        volume_ratio = data.get('volume_ratio', 1)
        if volume_ratio > 5:
            signals.append({
                'type': '交易量激增',
                'level': 'high' if volume_ratio > 10 else 'medium',
                'description': f"交易量是平均值的 {volume_ratio:.1f} 倍"
            })
        
        # 持有者增长
        holder_growth = data.get('holder_growth_7d', 0)
        if holder_growth > 50:
            signals.append({
                'type': '持有者快速增长',
                'level': 'medium',
                'description': f"7日持有者增长 {holder_growth:.1f}%"
            })
        
        return signals
    
    def _generate_recommendation(self, data: Dict) -> str:
        """生成投资建议"""
        risk = self._assess_risk(data)
        health = self._calculate_health_score(data)
        
        if risk == 'EXTREME':
            return "⚠️ 极高风险，建议避免投资"
        elif risk == 'HIGH':
            return "🔴 高风险，如参与请极小仓位"
        elif health >= 70:
            return "🟢 健康度良好，可考虑适度参与"
        elif health >= 50:
            return "🟡 中等质量，谨慎参与"
        else:
            return "🟠 风险较高，建议观望"
    
    def format_report(self, result: Dict) -> str:
        """格式化分析报告"""
        report = f"""
{'='*60}
📊 {result['token_name']} ({result['symbol']}) 分析报告
{'='*60}

🎯 综合评分: {result['health_score']}/100
⚠️ 风险等级: {result['risk_level']}

📋 风险因素:
"""
        if result['risk_factors']:
            for risk in result['risk_factors']:
                report += f"  • {risk}\n"
        else:
            report += "  • 未发现明显风险因素\n"
        
        report += f"\n📈 机会信号:\n"
        if result['opportunity_signals']:
            for signal in result['opportunity_signals']:
                emoji = '🔥' if signal['level'] == 'high' else '📊'
                report += f"  {emoji} [{signal['type']}] {signal['description']}\n"
        else:
            report += "  • 暂无显著机会信号\n"
        
        report += f"\n💡 投资建议: {result['recommendation']}\n"
        report += f"\n⏰ 分析时间: {result['analysis_time']}\n"
        report += '='*60
        
        return report


def main():
    """主函数 - 示例用法"""
    analyzer = SolanaTokenAnalyzer()
    
    # 示例代币数据
    sample_token = {
        'name': 'Sample Meme Token',
        'symbol': 'SMT',
        'liquidity_usd': 150000,
        'top10_holder_percent': 45,
        'volume_24h_usd': 500000,
        'contract_verified': True,
        'age_days': 3,
        'has_social': True,
        'price_change_24h': 120,
        'volume_ratio': 8,
        'holder_growth_7d': 200,
        'dev_sold': False,
        'mint_authority': False,
        'freeze_authority': False
    }
    
    result = analyzer.analyze_token(sample_token)
    print(analyzer.format_report(result))


if __name__ == '__main__':
    main()
