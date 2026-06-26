#!/usr/bin/env python3
"""
赔率分析模块 - 亚盘、欧赔、凯利指数分析
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json


@dataclass
class AsianHandicap:
    """亚盘数据"""
    handicap: float          # 盘口 (如 -0.5, -0.75, 0, +0.25)
    home_odds: float        # 主队水位
    away_odds: float        # 客队水位
    
    def get_favorite(self) -> str:
        """判断让球方"""
        if self.handicap < 0:
            return "home"  # 主队让球
        elif self.handicap > 0:
            return "away"  # 客队让球
        return "none"      # 平手盘
    
    def calculate_water_diff(self) -> float:
        """计算水位差"""
        return abs(self.home_odds - self.away_odds)
    
    def is_balanced(self, threshold: float = 0.1) -> bool:
        """判断盘口是否平衡"""
        return self.calculate_water_diff() < threshold


@dataclass
class EuropeanOdds:
    """欧赔数据"""
    home_win: float         # 主胜
    draw: float             # 平局
    away_win: float         # 客胜
    
    def calculate_return_rate(self) -> float:
        """计算返还率"""
        return 1 / (1/self.home_win + 1/self.draw + 1/self.away_win)
    
    def get_implied_probabilities(self) -> Dict[str, float]:
        """计算隐含概率"""
        total = 1/self.home_win + 1/self.draw + 1/self.away_win
        return {
            "home": (1/self.home_win) / total,
            "draw": (1/self.draw) / total,
            "away": (1/self.away_win) / total
        }
    
    def detect_suspicious_odds(self) -> List[str]:
        """检测异常赔率"""
        alerts = []
        probs = self.get_implied_probabilities()
        
        # 检测超低赔
        if self.home_win < 1.15:
            alerts.append(f"主胜赔率过低 ({self.home_win})，可能存在诱盘")
        if self.away_win < 1.15:
            alerts.append(f"客胜赔率过低 ({self.away_win})，可能存在诱盘")
        
        # 检测平局异常
        if self.draw < 2.8 and max(probs["home"], probs["away"]) > 0.5:
            alerts.append("平局赔率偏低，可能机构看好平局")
        
        return alerts


class KellyCalculator:
    """凯利指数计算器"""
    
    @staticmethod
    def calculate_true_probability(
        market_odds: float, 
        margin: float = 0.05
    ) -> float:
        """
        根据市场赔率和抽水率计算真实概率
        
        Args:
            market_odds: 市场赔率
            margin: 庄家抽水率 (默认5%)
        """
        implied_prob = 1 / market_odds
        return implied_prob / (1 + margin)
    
    @staticmethod
    def calculate_kelly_criterion(
        true_probability: float, 
        odds: float,
        fraction: float = 0.25
    ) -> float:
        """
        计算凯利公式投注比例
        
        Args:
            true_probability: 真实胜率估计
            odds: 赔率
            fraction: 凯利分数 (保守策略用0.25)
        
        Returns:
            建议投注资金比例
        """
        if odds <= 1:
            return 0
        
        kelly = (true_probability * odds - 1) / (odds - 1)
        return max(0, kelly * fraction)  # 应用分数凯利
    
    @staticmethod
    def analyze_value(
        model_probability: float,
        market_odds: float,
        min_edge: float = 0.05
    ) -> Dict:
        """
        分析价值投注
        
        Returns:
            {
                "is_value_bet": bool,      # 是否有价值
                "edge": float,              # 边际优势
                "kelly_fraction": float,    # 凯利比例
                "recommendation": str       # 建议
            }
        """
        implied_prob = 1 / market_odds
        edge = model_probability - implied_prob
        
        is_value = edge > min_edge
        kelly = KellyCalculator.calculate_kelly_criterion(
            model_probability, market_odds
        )
        
        if edge < -0.1:
            recommendation = "❌ 避免投注 - 赔率无价值"
        elif edge < 0:
            recommendation = "⚠️ 赔率略低 - 观望"
        elif edge < min_edge:
            recommendation = "➖ 价值不明显 - 可选"
        elif kelly < 0.02:
            recommendation = "✅ 有价值但比例小 - 小额娱乐"
        elif kelly < 0.05:
            recommendation = "✅ 有价值 - 适量投注"
        else:
            recommendation = "🔥 高价值 - 重点考虑"
        
        return {
            "is_value_bet": is_value,
            "edge": round(edge, 4),
            "kelly_fraction": round(kelly, 4),
            "recommendation": recommendation
        }


class OddsMovementAnalyzer:
    """赔率变化分析器"""
    
    def __init__(self):
        self.movement_history: List[Dict] = []
    
    def add_snapshot(self, timestamp: str, odds: EuropeanOdds):
        """添加赔率快照"""
        self.movement_history.append({
            "time": timestamp,
            "home": odds.home_win,
            "draw": odds.draw,
            "away": odds.away_win
        })
    
    def analyze_trend(self) -> Dict:
        """分析赔率趋势"""
        if len(self.movement_history) < 2:
            return {"error": "数据不足"}
        
        first = self.movement_history[0]
        last = self.movement_history[-1]
        
        home_change = ((last["home"] - first["home"]) / first["home"]) * 100
        draw_change = ((last["draw"] - first["draw"]) / first["draw"]) * 100
        away_change = ((last["away"] - first["away"]) / first["away"]) * 100
        
        analysis = {
            "home_trend": "🔼 升" if home_change > 5 else ("🔽 降" if home_change < -5 else "➡️ 稳"),
            "draw_trend": "🔼 升" if draw_change > 5 else ("🔽 降" if draw_change < -5 else "➡️ 稳"),
            "away_trend": "🔼 升" if away_change > 5 else ("🔽 降" if away_change < -5 else "➡️ 稳"),
            "home_change_pct": round(home_change, 2),
            "draw_change_pct": round(draw_change, 2),
            "away_change_pct": round(away_change, 2)
        }
        
        # 判断机构倾向
        if home_change < -10 and away_change > 5:
            analysis["bookmaker_bias"] = "🏠 机构看好主队"
        elif away_change < -10 and home_change > 5:
            analysis["bookmaker_bias"] = "✈️ 机构看好客队"
        elif abs(home_change) < 5 and abs(away_change) < 5:
            analysis["bookmaker_bias"] = "⚖️ 机构态度平稳"
        else:
            analysis["bookmaker_bias"] = "🔄 机构调整中"
        
        return analysis


class ComprehensiveOddsAnalyzer:
    """综合赔率分析器"""
    
    def __init__(self):
        self.kelly = KellyCalculator()
        self.movement = OddsMovementAnalyzer()
    
    def analyze_match(
        self,
        home_win_odds: float,
        draw_odds: float,
        away_win_odds: float,
        model_probs: Optional[Dict[str, float]] = None
    ) -> Dict:
        """
        综合分析一场比赛的所有赔率
        
        Args:
            home_win_odds: 主胜赔率
            draw_odds: 平局赔率
            away_win_odds: 客胜赔率
            model_probs: 模型预测概率 (可选)
        """
        # 欧赔基础分析
        euro_odds = EuropeanOdds(home_win_odds, draw_odds, away_win_odds)
        implied = euro_odds.get_implied_probabilities()
        return_rate = euro_odds.calculate_return_rate()
        suspicious = euro_odds.detect_suspicious_odds()
        
        result = {
            "european_odds": {
                "home": home_win_odds,
                "draw": draw_odds,
                "away": away_win_odds,
                "return_rate": round(return_rate * 100, 2)
            },
            "implied_probabilities": {
                k: round(v * 100, 1) for k, v in implied.items()
            },
            "suspicious_alerts": suspicious
        }
        
        # 如果有模型概率，进行价值分析
        if model_probs:
            for outcome, prob in model_probs.items():
                odds = getattr(euro_odds, f"{outcome}_win" if outcome != "draw" else "draw")
                value_analysis = self.kelly.analyze_value(prob, odds)
                result[f"{outcome}_value"] = value_analysis
        
        return result
    
    def generate_betting_advice(self, analysis: Dict) -> str:
        """生成投注建议文本"""
        lines = ["\n🎯 赔率分析报告", "=" * 50]
        
        # 基础赔率
        euro = analysis["european_odds"]
        lines.append(f"\n📊 欧赔: 主{euro['home']} | 平{euro['draw']} | 客{euro['away']}")
        lines.append(f"💰 返还率: {euro['return_rate']}%")
        
        # 隐含概率
        implied = analysis["implied_probabilities"]
        lines.append(f"\n📈 隐含概率: 主{implied['home']}% | 平{implied['draw']}% | 客{implied['away']}%")
        
        # 异常提示
        if analysis["suspicious_alerts"]:
            lines.append("\n⚠️ 异常提示:")
            for alert in analysis["suspicious_alerts"]:
                lines.append(f"   • {alert}")
        
        # 价值分析
        lines.append("\n💡 价值分析:")
        for outcome in ["home", "draw", "away"]:
            key = f"{outcome}_value"
            if key in analysis:
                val = analysis[key]
                lines.append(f"   {outcome.upper()}: {val['recommendation']} (边际: {val['edge']:+.2%})")
        
        lines.append("=" * 50)
        return "\n".join(lines)


# 演示
def demo():
    """赔率分析演示"""
    analyzer = ComprehensiveOddsAnalyzer()
    
    # 示例: 曼城 vs 阿森纳
    print("曼城 vs 阿森纳 赔率分析")
    print("=" * 60)
    
    analysis = analyzer.analyze_match(
        home_win_odds=1.75,    # 主胜
        draw_odds=3.60,        # 平局
        away_win_odds=4.50,    # 客胜
        model_probs={          # 模型预测
            "home": 0.58,
            "draw": 0.24,
            "away": 0.18
        }
    )
    
    print(analyzer.generate_betting_advice(analysis))
    
    # 亚盘示例
    print("\n\n亚盘示例:")
    ah = AsianHandicap(handicap=-0.75, home_odds=0.95, away_odds=0.95)
    print(f"盘口: 主队让{abs(ah.handicap)}球")
    print(f"主队水位: {ah.home_odds}")
    print(f"客队水位: {ah.away_odds}")
    print(f"是否平衡: {'是' if ah.is_balanced() else '否'}")


if __name__ == "__main__":
    demo()
