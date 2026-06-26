#!/usr/bin/env python3
"""
报告生成器模块

功能：
- 生成分析报告
- 格式化输出
- 风险提示
"""

import json
from typing import Dict
from datetime import datetime
import os


class ReportGenerator:
    """报告生成器"""

    def __init__(self, config: Dict):
        self.config = config
        self.template_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'templates'
        )

    def generate_report(self, sport: str, team1: str, team2: str,
                        match_data: Dict, features: Dict,
                        prediction: Dict, risk_assessment: Dict) -> Dict:
        """
        生成分析报告

        Args:
            sport: 体育项目
            team1: 主队
            team2: 客队
            match_data: 比赛数据
            features: 特征
            prediction: 预测结果
            risk_assessment: 风险评估

        Returns:
            报告字典
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "sport": sport,
            "match": f"{team1} vs {team2}",
            "match_date": match_data.get('match_date', '未知'),
            "venue": match_data.get('venue', '未知'),
            "summary": self._generate_summary(sport, team1, team2, prediction, risk_assessment),
            "data_overview": self._generate_data_overview(match_data),
            "prediction": self._format_prediction(prediction, team1, team2),
            "betting_recommendation": self._generate_betting_recommendation(prediction, risk_assessment),
            "risk_assessment": risk_assessment,
            "explanation": self._generate_explanation(features, prediction),
            "factors_analysis": self._analyze_factors(features, match_data),
            "data_sources": ["模拟数据（MVP版本）"],
            "disclaimer": self._get_disclaimer()
        }

        return report

    def _generate_summary(self, sport: str, team1: str, team2: str,
                          prediction: Dict, risk_assessment: Dict) -> str:
        """生成摘要"""
        pred_result = prediction.get('prediction', '未知')
        confidence = prediction.get('confidence', 0)

        # 转换预测结果
        if pred_result == 'team1':
            pred_text = team1
        elif pred_result == 'team2':
            pred_text = team2
        else:
            pred_text = "平局"

        summary = f"""🏆 {sport} 比赛分析：{team1} vs {team2}

🎯 预测结果：{pred_text} 胜
📊 置信度：{confidence:.1%}
⚠️ 风险等级：{risk_assessment.get('risk_level', '中')}

💡 建议投注：{risk_assessment.get('suggested_bet_percentage', 0)}%
"""
        return summary

    def _generate_data_overview(self, match_data: Dict) -> Dict:
        """生成数据概览"""
        team1 = match_data.get('team1', '')
        team2 = match_data.get('team2', '')
        team1_stats = match_data.get('team1_stats', {})
        team2_stats = match_data.get('team2_stats', {})
        h2h = match_data.get('h2h', {})

        return {
            "team1": {
                "name": team1,
                "season_win_rate": team1_stats.get('season_win_rate', 0),
                "recent_5_games": team1_stats.get('recent_5_games', []),
                "key_players_status": [p['status'] for p in team1_stats.get('key_players', [])]
            },
            "team2": {
                "name": team2,
                "season_win_rate": team2_stats.get('season_win_rate', 0),
                "recent_5_games": team2_stats.get('recent_5_games', []),
                "key_players_status": [p['status'] for p in team2_stats.get('key_players', [])]
            },
            "head_to_head": {
                "total_games": h2h.get('total_games', 0),
                "team1_wins": h2h.get('team1_wins', 0),
                "team2_wins": h2h.get('team2_wins', 0),
                "draws": h2h.get('draws', 0)
            },
            "average_odds": match_data.get('odds', {}).get('average', {})
        }

    def _format_prediction(self, prediction: Dict, team1: str, team2: str) -> Dict:
        """格式化预测结果"""
        probs = prediction.get('probabilities', {})

        formatted = {
            "result": prediction.get('prediction', '未知'),
            "confidence": prediction.get('confidence', 0),
            "probabilities": {}
        }

        # 转换概率显示
        if 'team1' in probs:
            formatted['probabilities'][team1] = f"{probs['team1']:.1%}"
        if 'team2' in probs:
            formatted['probabilities'][team2] = f"{probs['team2']:.1%}"
        if 'draw' in probs:
            formatted['probabilities']['平局'] = f"{probs['draw']:.1%}"

        return formatted

    def _generate_betting_recommendation(self, prediction: Dict, risk_assessment: Dict) -> Dict:
        """生成投注建议"""
        confidence = prediction.get('confidence', 0)
        risk_level = risk_assessment.get('risk_level', 'moderate')
        is_value = risk_assessment.get('value_bet', False)

        recommendation = {
            "action": "观望",
            "bet_percentage": 0,
            "reason": "",
            "betting_options": []
        }

        if confidence < self.config.get('min_confidence', 0.6):
            recommendation['action'] = "观望"
            recommendation['reason'] = f"置信度 {confidence:.1%} 低于阈值 {self.config['min_confidence']:.0%}"
        elif risk_level == 'high':
            recommendation['action'] = "谨慎投注"
            recommendation['bet_percentage'] = risk_assessment.get('suggested_bet_percentage', 1)
            recommendation['reason'] = "风险较高，建议降低投注比例"
        elif is_value:
            recommendation['action'] = "推荐投注"
            recommendation['bet_percentage'] = risk_assessment.get('suggested_bet_percentage', 2)
            recommendation['reason'] = "价值投注机会，建议把握"
        else:
            recommendation['action'] = "可以投注"
            recommendation['bet_percentage'] = risk_assessment.get('suggested_bet_percentage', 2)
            recommendation['reason'] = "正常投注机会"

        return recommendation

    def _generate_explanation(self, features: Dict, prediction: Dict) -> str:
        """生成解释性说明"""
        strength_diff = features.get('strength_diff', 0)
        home_advantage = features.get('home_advantage', 0)
        recent_form_diff = features.get('team1_recent_form', 0) - features.get('team2_recent_form', 0)

        explanation = f"""📊 预测依据：

1. 实力对比："""
        if strength_diff > 0.1:
            explanation += f" 主队实力明显优势（+{strength_diff:.2%}）"
        elif strength_diff < -0.1:
            explanation += f" 客队实力明显优势（{strength_diff:.2%}）"
        else:
            explanation += f" 实力相当"

        explanation += f"""

2. 主客场优势："""
        if home_advantage > 0.05:
            explanation += f" 主场优势明显（+{home_advantage:.2%}）"
        elif home_advantage < -0.05:
            explanation += f" 客场劣势明显（{home_advantage:.2%}）"
        else:
            explanation += f" 主客场影响不大"

        explanation += f"""

3. 近期状态："""
        if recent_form_diff > 0.2:
            explanation += f" 主队近期状态更好（+{recent_form_diff:.1%}）"
        elif recent_form_diff < -0.2:
            explanation += f" 客队近期状态更好（{recent_form_diff:.1%}）"
        else:
            explanation += f" 近期状态相近"

        explanation += f"""

4. 综合评估：模型综合考虑了实力、主客场、近期状态、历史对战、伤病等多个因素，得出当前预测结果。置信度 {prediction.get('confidence', 0):.1%} 代表模型对预测结果的信心程度。"""

        return explanation

    def _analyze_factors(self, features: Dict, match_data: Dict) -> Dict:
        """分析各因素"""
        factors = {
            "strength": {
                "name": "实力对比",
                "value": features.get('strength_diff', 0),
                "importance": "高",
                "description": "基于赛季胜率、积分排名等综合实力评估"
            },
            "home_advantage": {
                "name": "主客场优势",
                "value": features.get('home_advantage', 0),
                "importance": "高",
                "description": "主场球队通常有统计优势"
            },
            "recent_form": {
                "name": "近期状态",
                "value": features.get('team1_recent_form', 0) - features.get('team2_recent_form', 0),
                "importance": "中",
                "description": "基于最近5场比赛的表现"
            },
            "h2h": {
                "name": "历史对战",
                "value": features.get('h2h_advantage', 0),
                "importance": "中",
                "description": "历史交锋记录的心理优势"
            },
            "injuries": {
                "name": "伤病影响",
                "value": features.get('team2_injury_impact', 0) - features.get('team1_injury_impact', 0),
                "importance": "中",
                "description": "关键球员伤病对球队实力的影响"
            }
        }

        # 按重要性排序
        sorted_factors = sorted(factors.items(), key=lambda x: abs(x[1]['value']), reverse=True)

        return dict(sorted_factors)

    def _get_disclaimer(self) -> str:
        """获取免责声明"""
        return """⚠️ 重要提示：

1. 本分析仅供参考，不构成投注建议
2. 体育比赛存在不确定性，预测不保证准确
3. 请理性投注，控制风险，量力而行
4. 不要过度依赖单一分析工具
5. 请遵守当地法律法规

数据来源：当前版本使用模拟数据，实际应用应接入真实数据源。"""

    def format_as_text(self, report: Dict) -> str:
        """格式化为文本报告"""
        text = f"""
{'='*60}
📊 体育彩票分析报告
{'='*60}

{report['summary']}

{'='*60}
📋 数据概览
{'='*60}

【主队】{report['data_overview']['team1']['name']}
- 赛季胜率：{report['data_overview']['team1']['season_win_rate']:.1%}
- 近5场：{' '.join(report['data_overview']['team1']['recent_5_games'])}
- 核心球员状态：{', '.join(report['data_overview']['team1']['key_players_status'])}

【客队】{report['data_overview']['team2']['name']}
- 赛季胜率：{report['data_overview']['team2']['season_win_rate']:.1%}
- 近5场：{' '.join(report['data_overview']['team2']['recent_5_games'])}
- 核心球员状态：{', '.join(report['data_overview']['team2']['key_players_status'])}

【历史对战】
- 总场次：{report['data_overview']['head_to_head']['total_games']}
- 主队胜：{report['data_overview']['head_to_head']['team1_wins']}
- 客队胜：{report['data_overview']['head_to_head']['team2_wins']}
- 平局：{report['data_overview']['head_to_head']['draws']}

【平均赔率】
{self._format_odds(report['data_overview']['average_odds'])}

{'='*60}
🎯 预测结果
{'='*60}

结果：{report['prediction']['result']}
置信度：{report['prediction']['confidence']:.1%}

概率分布：
{self._format_probabilities(report['prediction']['probabilities'])}

{'='*60}
💡 投注建议
{'='*60}

建议：{report['betting_recommendation']['action']}
投注比例：{report['betting_recommendation']['bet_percentage']}%
理由：{report['betting_recommendation']['reason']}

风险等级：{report['risk_assessment']['risk_level']}
价值投注：{'是' if report['risk_assessment']['value_bet'] else '否'}

{'='*60}
📊 因素分析
{'='*60}

{self._format_factors(report['factors_analysis'])}

{'='*60}
📝 可解释性说明
{'='*60}

{report['explanation']}

{'='*60}
⚠️ 免责声明
{'='*60}

{report['disclaimer']}

{'='*60}
生成时间：{report['timestamp']}
{'='*60}
"""
        return text

    def _format_odds(self, odds: Dict) -> str:
        """格式化赔率"""
        lines = []
        for key, value in odds.items():
            lines.append(f"  {key}: {value}")
        return '\n'.join(lines)

    def _format_probabilities(self, probs: Dict) -> str:
        """格式化概率"""
        lines = []
        for key, value in probs.items():
            lines.append(f"  {key}: {value}")
        return '\n'.join(lines)

    def _format_factors(self, factors: Dict) -> str:
        """格式化因素分析"""
        lines = []
        for key, factor in factors.items():
            lines.append(f"\n【{factor['name']}】（重要性：{factor['importance']}）")
            lines.append(f"  数值：{factor['value']:+.2%}")
            lines.append(f"  说明：{factor['description']}")
        return '\n'.join(lines)

    def save_report(self, report: Dict, filename: str = None):
        """保存报告到文件"""
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        report_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'reports'
        )
        os.makedirs(report_dir, exist_ok=True)

        filepath = os.path.join(report_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.format_as_text(report))

        # 同时保存JSON格式
        json_filepath = filepath.replace('.md', '.json')
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return filepath