#!/usr/bin/env python3
"""
BSC 项目评估器
使用 BISCUIT 框架评估 BSC 项目
"""

import json
from datetime import datetime
from typing import Dict, List


class BSCProjectEvaluator:
    """BSC 项目评估器 - BISCUIT 框架"""
    
    def __init__(self):
        self.weights = {
            'bridges': 0.15,      # B - 跨链桥安全
            'innovation': 0.15,   # I - 创新性
            'security': 0.20,     # S - 安全审计
            'community': 0.10,    # C - 社区活跃度
            'utility': 0.15,      # U - 实用性
            'incentives': 0.10,   # I - 激励机制
            'team': 0.15          # T - 团队背景
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
        scores = {
            'bridges': self._evaluate_bridges(project_data),
            'innovation': self._evaluate_innovation(project_data),
            'security': self._evaluate_security(project_data),
            'community': self._evaluate_community(project_data),
            'utility': self._evaluate_utility(project_data),
            'incentives': self._evaluate_incentives(project_data),
            'team': self._evaluate_team(project_data)
        }
        
        # 计算加权总分
        total_score = sum(scores[k] * self.weights[k] for k in scores)
        
        return {
            'project_name': project_data.get('name', 'Unknown'),
            'timestamp': datetime.now().isoformat(),
            'total_score': round(total_score, 1),
            'grade': self._score_to_grade(total_score),
            'breakdown': {k: round(v, 1) for k, v in scores.items()},
            'risk_factors': self._identify_risks(project_data),
            'strengths': self._identify_strengths(project_data),
            'recommendation': self._generate_recommendation(total_score)
        }
    
    def _evaluate_bridges(self, data: Dict) -> float:
        """评估跨链桥安全 (0-100)"""
        score = 50
        
        bridge_type = data.get('bridge_type', 'third_party')
        if bridge_type == 'native':
            score += 40
        elif bridge_type == 'official':
            score += 30
        elif bridge_type == 'established':
            score += 20
        
        if data.get('bridge_audited', False):
            score += 10
        
        return min(score, 100)
    
    def _evaluate_innovation(self, data: Dict) -> float:
        """评估创新性 (0-100)"""
        score = 30
        
        if data.get('novel_mechanism', False):
            score += 30
        
        if data.get('unique_features', []):
            score += min(len(data['unique_features']) * 10, 20)
        
        if data.get('first_mover', False):
            score += 20
        
        return min(score, 100)
    
    def _evaluate_security(self, data: Dict) -> float:
        """评估安全审计 (0-100)"""
        score = 0
        
        audits = data.get('audits', [])
        if not audits:
            return 20
        
        # 审计公司声誉
        top_tier = ['Trail of Bits', 'OpenZeppelin', 'CertiK', 'PeckShield']
        for audit in audits:
            if any(tier in audit.get('firm', '') for tier in top_tier):
                score += 25
            else:
                score += 15
        
        score = min(score, 80)
        
        # 漏洞赏金
        if data.get('bug_bounty', False):
            score += 10
        
        # 保险
        if data.get('insurance', False):
            score += 10
        
        return min(score, 100)
    
    def _evaluate_community(self, data: Dict) -> float:
        """评估社区活跃度 (0-100)"""
        score = 0
        
        twitter_followers = data.get('twitter_followers', 0)
        if twitter_followers >= 100000:
            score += 40
        elif twitter_followers >= 50000:
            score += 30
        elif twitter_followers >= 10000:
            score += 20
        else:
            score += 10
        
        telegram_members = data.get('telegram_members', 0)
        if telegram_members >= 50000:
            score += 30
        elif telegram_members >= 10000:
            score += 20
        elif telegram_members >= 1000:
            score += 10
        
        discord_members = data.get('discord_members', 0)
        if discord_members >= 20000:
            score += 30
        elif discord_members >= 5000:
            score += 20
        elif discord_members >= 1000:
            score += 10
        
        return min(score, 100)
    
    def _evaluate_utility(self, data: Dict) -> float:
        """评估实用性 (0-100)"""
        score = 30
        
        tvl = data.get('tvl', 0)
        if tvl >= 100_000_000:
            score += 40
        elif tvl >= 10_000_000:
            score += 30
        elif tvl >= 1_000_000:
            score += 20
        else:
            score += 10
        
        daily_users = data.get('daily_users', 0)
        if daily_users >= 10000:
            score += 20
        elif daily_users >= 1000:
            score += 10
        
        if data.get('token_utility'):
            score += 10
        
        return min(score, 100)
    
    def _evaluate_incentives(self, data: Dict) -> float:
        """评估激励机制 (0-100)"""
        score = 30
        
        apy = data.get('apy', 0)
        if apy >= 50:
            score += 40
        elif apy >= 20:
            score += 30
        elif apy >= 10:
            score += 20
        elif apy > 0:
            score += 10
        
        if data.get('sustainable_emissions', False):
            score += 20
        
        if data.get('vesting_schedule', False):
            score += 10
        
        return min(score, 100)
    
    def _evaluate_team(self, data: Dict) -> float:
        """评估团队背景 (0-100)"""
        score = 20
        
        if data.get('doxxed_team', False):
            score += 30
        
        if data.get('previous_projects', []):
            score += min(len(data['previous_projects']) * 10, 20)
        
        if data.get('experience_years', 0) >= 5:
            score += 20
        elif data.get('experience_years', 0) >= 2:
            score += 10
        
        if data.get('active_development', False):
            score += 10
        
        return min(score, 100)
    
    def _score_to_grade(self, score: float) -> str:
        """分数转等级"""
        if score >= 80:
            return 'A+'
        elif score >= 70:
            return 'A'
        elif score >= 60:
            return 'B'
        elif score >= 50:
            return 'C'
        elif score >= 40:
            return 'D'
        else:
            return 'F'
    
    def _identify_risks(self, data: Dict) -> List[str]:
        """识别风险因素"""
        risks = []
        
        if not data.get('audits', []):
            risks.append("⚠️ 未经审计")
        
        if not data.get('doxxed_team', False):
            risks.append("⚠️ 团队匿名")
        
        if data.get('tvl', 0) < 1_000_000:
            risks.append("⚠️ 低流动性")
        
        if data.get('apy', 0) > 100:
            risks.append("⚠️ 过高收益，可能不可持续")
        
        if data.get('bridge_type') == 'third_party':
            risks.append("⚠️ 使用第三方跨链桥")
        
        return risks
    
    def _identify_strengths(self, data: Dict) -> List[str]:
        """识别优势"""
        strengths = []
        
        if data.get('audits', []):
            strengths.append("✅ 已通过安全审计")
        
        if data.get('doxxed_team', False):
            strengths.append("✅ 团队实名")
        
        if data.get('tvl', 0) > 100_000_000:
            strengths.append("✅ 高流动性")
        
        if data.get('first_mover', False):
            strengths.append("✅ 赛道先发优势")
        
        if data.get('bug_bounty', False):
            strengths.append("✅ 有漏洞赏金计划")
        
        return strengths
    
    def _generate_recommendation(self, total_score: float) -> str:
        """生成投资建议"""
        if total_score >= 75:
            return "🟢 强烈推荐 - 优质项目，可考虑配置"
        elif total_score >= 60:
            return "🟡 可以考虑 - 中等质量，适度参与"
        elif total_score >= 45:
            return "🟠 观望 - 风险较高，建议观察"
        else:
            return "🔴 谨慎 - 高风险，不建议投资"
    
    def format_report(self, result: Dict) -> str:
        """格式化报告"""
        report = f"""
{'='*70}
🟨 {result['project_name']} BSC 项目评估报告 (BISCUIT 框架)
{'='*70}

🎯 综合评分: {result['total_score']}/100 | 等级: {result['grade']}

📈 分项得分:
  • 跨链桥 (Bridges): {result['breakdown']['bridges']}/100
  • 创新性 (Innovation): {result['breakdown']['innovation']}/100
  • 安全 (Security): {result['breakdown']['security']}/100
  • 社区 (Community): {result['breakdown']['community']}/100
  • 实用性 (Utility): {result['breakdown']['utility']}/100
  • 激励 (Incentives): {result['breakdown']['incentives']}/100
  • 团队 (Team): {result['breakdown']['team']}/100

"""
        # 优势
        if result['strengths']:
            report += "✅ 优势:\n"
            for s in result['strengths']:
                report += f"  {s}\n"
            report += "\n"
        
        # 风险
        if result['risk_factors']:
            report += "⚠️ 风险:\n"
            for r in result['risk_factors']:
                report += f"  {r}\n"
            report += "\n"
        
        report += f"💡 投资建议: {result['recommendation']}\n"
        report += f"\n⏰ 评估时间: {result['timestamp']}\n"
        report += '='*70
        
        return report


def main():
    """主函数 - 示例"""
    evaluator = BSCProjectEvaluator()
    
    # 示例项目 - PancakeSwap
    sample_project = {
        'name': 'PancakeSwap',
        'bridge_type': 'native',
        'bridge_audited': True,
        'novel_mechanism': True,
        'unique_features': ['IFO', '彩票', '预测市场'],
        'first_mover': True,
        'audits': [
            {'firm': 'CertiK'},
            {'firm': 'SlowMist'}
        ],
        'bug_bounty': True,
        'insurance': False,
        'twitter_followers': 1500000,
        'telegram_members': 200000,
        'discord_members': 80000,
        'tvl': 2_500_000_000,
        'daily_users': 50000,
        'token_utility': True,
        'apy': 15.5,
        'sustainable_emissions': True,
        'vesting_schedule': True,
        'doxxed_team': True,
        'previous_projects': [],
        'experience_years': 4,
        'active_development': True
    }
    
    result = evaluator.evaluate(sample_project)
    print(evaluator.format_report(result))


if __name__ == '__main__':
    main()
