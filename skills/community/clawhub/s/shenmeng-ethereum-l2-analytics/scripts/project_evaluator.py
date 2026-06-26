#!/usr/bin/env python3
"""
Ethereum L2 项目评估器
使用 ROLLUP 框架评估 Ethereum L2 项目
"""

import json
import sys
from datetime import datetime
from typing import Dict, List


class L2ProjectEvaluator:
    """L2 项目评估器 - ROLLUP 框架"""
    
    def __init__(self):
        self.weights = {
            'revenue': 0.15,      # R - 收入
            'overhead': 0.15,     # O - 开销/效率
            'liquidity': 0.25,    # L - 流动性
            'latency': 0.15,      # L - 延迟/用户体验
            'users': 0.15,        # U - 用户
            'protocols': 0.15,    # P - 协议
        }
    
    def evaluate(self, project_data: Dict) -> Dict:
        """
        评估项目
        
        Args:
            project_data: 项目数据字典
            
        Returns:
            评估结果
        """
        # 计算各项得分
        revenue_score = self._evaluate_revenue(project_data)
        overhead_score = self._evaluate_overhead(project_data)
        liquidity_score = self._evaluate_liquidity(project_data)
        latency_score = self._evaluate_latency(project_data)
        users_score = self._evaluate_users(project_data)
        protocols_score = self._evaluate_protocols(project_data)
        
        # 计算加权总分
        total_score = (
            revenue_score * self.weights['revenue'] +
            overhead_score * self.weights['overhead'] +
            liquidity_score * self.weights['liquidity'] +
            latency_score * self.weights['latency'] +
            users_score * self.weights['users'] +
            protocols_score * self.weights['protocols']
        )
        
        return {
            'project_name': project_data.get('name', 'Unknown'),
            'timestamp': datetime.now().isoformat(),
            'total_score': round(total_score, 1),
            'grade': self._score_to_grade(total_score),
            'breakdown': {
                'revenue': round(revenue_score, 1),
                'overhead': round(overhead_score, 1),
                'liquidity': round(liquidity_score, 1),
                'latency': round(latency_score, 1),
                'users': round(users_score, 1),
                'protocols': round(protocols_score, 1),
            },
            'strengths': self._identify_strengths(project_data),
            'weaknesses': self._identify_weaknesses(project_data),
            'recommendation': self._generate_recommendation(total_score)
        }
    
    def _evaluate_revenue(self, data: Dict) -> float:
        """评估收入/经济模型 (0-100)"""
        score = 50  # 基础分
        
        # 费用收入
        daily_fees = data.get('daily_fees_usd', 0)
        if daily_fees > 1_000_000:
            score += 30
        elif daily_fees > 100_000:
            score += 20
        elif daily_fees > 10_000:
            score += 10
        
        # 代币经济
        if data.get('has_token', False):
            score += 10
            if data.get('token_utility') in ['gas', 'governance', 'staking']:
                score += 10
        
        return min(score, 100)
    
    def _evaluate_overhead(self, data: Dict) -> float:
        """评估效率/开销 (0-100)"""
        score = 50
        
        # TPS
        tps = data.get('tps', 0)
        if tps >= 10000:
            score += 30
        elif tps >= 1000:
            score += 20
        elif tps >= 100:
            score += 10
        
        # 费用效率
        avg_fee = data.get('avg_fee_usd', 1)
        if avg_fee < 0.1:
            score += 20
        elif avg_fee < 0.5:
            score += 10
        
        return min(score, 100)
    
    def _evaluate_liquidity(self, data: Dict) -> float:
        """评估流动性 (0-100)"""
        score = 0
        tvl = data.get('tvl_usd', 0)
        
        if tvl >= 10_000_000_000:
            score = 100
        elif tvl >= 5_000_000_000:
            score = 85
        elif tvl >= 1_000_000_000:
            score = 70
        elif tvl >= 500_000_000:
            score = 55
        elif tvl >= 100_000_000:
            score = 40
        else:
            score = 25
        
        return score
    
    def _evaluate_latency(self, data: Dict) -> float:
        """评估延迟/用户体验 (0-100)"""
        score = 50
        
        # 最终确定性时间
        finality = data.get('finality_time', '7 days')
        if finality == 'instant':
            score += 40
        elif finality == '1 hour':
            score += 25
        elif finality == '7 days':
            score += 0  # 需要第三方桥才能实现即时
        
        # 存款时间
        deposit_time = data.get('deposit_time_minutes', 30)
        if deposit_time <= 5:
            score += 10
        elif deposit_time <= 15:
            score += 5
        
        return min(score, 100)
    
    def _evaluate_users(self, data: Dict) -> float:
        """评估用户采用度 (0-100)"""
        score = 0
        
        # 日活地址
        dau = data.get('daily_active_users', 0)
        if dau >= 500_000:
            score = 100
        elif dau >= 200_000:
            score = 80
        elif dau >= 100_000:
            score = 65
        elif dau >= 50_000:
            score = 50
        elif dau >= 10_000:
            score = 35
        else:
            score = 20
        
        # 用户增长
        growth = data.get('user_growth_30d', 0)
        if growth > 50:
            score += 10
        elif growth > 0:
            score += 5
        
        return min(score, 100)
    
    def _evaluate_protocols(self, data: Dict) -> float:
        """评估协议生态 (0-100)"""
        score = 0
        
        # 协议数量
        protocols = data.get('protocol_count', 0)
        if protocols >= 100:
            score = 100
        elif protocols >= 50:
            score = 80
        elif protocols >= 20:
            score = 60
        elif protocols >= 10:
            score = 45
        else:
            score = 30
        
        # 蓝筹协议
        blue_chips = data.get('bluechip_protocols', [])
        if len(blue_chips) >= 5:
            score += 10
        elif len(blue_chips) >= 3:
            score += 5
        
        return min(score, 100)
    
    def _score_to_grade(self, score: float) -> str:
        """分数转等级"""
        if score >= 80:
            return 'A+'
        elif score >= 65:
            return 'A'
        elif score >= 50:
            return 'B'
        elif score >= 35:
            return 'C'
        else:
            return 'D'
    
    def _identify_strengths(self, data: Dict) -> List[str]:
        """识别优势"""
        strengths = []
        
        if data.get('tvl_usd', 0) > 5_000_000_000:
            strengths.append("💰 深厚的流动性基础")
        
        if data.get('daily_active_users', 0) > 100_000:
            strengths.append("👥 庞大的活跃用户群")
        
        if data.get('protocol_count', 0) > 50:
            strengths.append("🛠️ 丰富的协议生态")
        
        if data.get('tps', 0) > 5000:
            strengths.append("⚡ 高性能吞吐量")
        
        if data.get('finality_time') == 'instant':
            strengths.append("⏱️ 即时最终确定性")
        
        return strengths
    
    def _identify_weaknesses(self, data: Dict) -> List[str]:
        """识别劣势"""
        weaknesses = []
        
        if data.get('finality_time') == '7 days':
            weaknesses.append("🐌 7天挑战期 (提现慢)")
        
        if data.get('daily_active_users', 0) < 50_000:
            weaknesses.append("👤 用户采用度较低")
        
        if data.get('protocol_count', 0) < 20:
            weaknesses.append("🔧 协议生态尚不成熟")
        
        if not data.get('has_token', False):
            weaknesses.append("🪙 无原生代币 (治理激励受限)")
        
        if data.get('centralized_sequencer', True):
            weaknesses.append("⚠️ 中心化排序器")
        
        return weaknesses
    
    def _generate_recommendation(self, total_score: float) -> str:
        """生成投资建议"""
        if total_score >= 75:
            return "🟢 强烈推荐 - L2 领导者，生态成熟，可考虑配置"
        elif total_score >= 60:
            return "🟡 推荐 - 优质 L2，具备良好的发展前景"
        elif total_score >= 45:
            return "🟠 观望 - 新兴 L2，有潜力但风险较高"
        else:
            return "🔴 谨慎 - 早期项目，建议观察等待"
    
    def format_report(self, result: Dict) -> str:
        """格式化报告"""
        report = f"""
{'='*70}
⛓️ {result['project_name']} L2 评估报告 (ROLLUP 框架)
{'='*70}

🎯 综合评分: {result['total_score']}/100 | 等级: {result['grade']}

📈 分项得分:
  • 收入 (Revenue): {result['breakdown']['revenue']}/100
  • 效率 (Overhead): {result['breakdown']['overhead']}/100
  • 流动性 (Liquidity): {result['breakdown']['liquidity']}/100
  • 延迟 (Latency): {result['breakdown']['latency']}/100
  • 用户 (Users): {result['breakdown']['users']}/100
  • 协议 (Protocols): {result['breakdown']['protocols']}/100

"""
        # 优势
        if result['strengths']:
            report += "✅ 优势:\n"
            for s in result['strengths']:
                report += f"  {s}\n"
            report += "\n"
        
        # 劣势
        if result['weaknesses']:
            report += "⚠️ 劣势:\n"
            for w in result['weaknesses']:
                report += f"  {w}\n"
            report += "\n"
        
        report += f"💡 投资建议: {result['recommendation']}\n"
        report += f"\n⏰ 评估时间: {result['timestamp']}\n"
        report += '='*70
        
        return report


def main():
    """主函数 - 示例"""
    evaluator = L2ProjectEvaluator()
    
    # 示例项目数据 - Arbitrum
    sample_project = {
        'name': 'Arbitrum One',
        'tvl_usd': 15_000_000_000,
        'daily_fees_usd': 500_000,
        'has_token': True,
        'token_utility': 'governance',
        'tps': 40000,
        'avg_fee_usd': 0.20,
        'finality_time': '7 days',
        'deposit_time_minutes': 10,
        'daily_active_users': 200_000,
        'user_growth_30d': 15,
        'protocol_count': 500,
        'bluechip_protocols': ['Uniswap', 'Aave', 'Curve', 'Balancer', 'GMX'],
        'centralized_sequencer': True,
    }
    
    result = evaluator.evaluate(sample_project)
    print(evaluator.format_report(result))


if __name__ == '__main__':
    main()
