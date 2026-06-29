"""
胜率最高策略（保守策略）
低风险、高胜率，单关或2串1组合，目标胜率≥65%
"""

from ..data.models import PredictionResult, BettingStrategy
from .lottery import LotteryStrategyEngine


class ConservativeStrategy(LotteryStrategyEngine):
    """胜率最高策略生成器"""

    STRATEGY_NAME = "胜率最高策略"
    RISK_LEVEL = "低"
    SUGGESTED_RATIO = "70%"
    TARGET_WIN_RATE = 0.65
    TARGET_ODDS_MIN = 1.20
    TARGET_ODDS_MAX = 2.50

    def generate(self, prediction: PredictionResult) -> BettingStrategy:
        """生成胜率最高策略"""
        play_types = []

        # 1. 胜平负主推
        win_draw_loss = self.create_win_draw_loss_strategy(prediction)
        play_types.append(win_draw_loss)

        # 2. 让球胜平负（更稳定）
        handicap = self.create_handicap_strategy(prediction, handicap=0)
        play_types.append(handicap)

        # 3. 总进球数最高概率选项
        goals_strategies = self.create_total_goals_strategy(prediction)
        if goals_strategies and float(goals_strategies[0]["概率"].rstrip("%")) / 100 >= 0.30:
            play_types.append(goals_strategies[0])

        # 计算综合胜率和赔率
        win_rate = self._calculate_comprehensive_win_rate(play_types)
        avg_odds = self._calculate_average_odds(play_types)
        expected_value = (win_rate * avg_odds) - 1.0  # 凯利公式简化

        return BettingStrategy(
            strategy_name=self.STRATEGY_NAME,
            risk_level=self.RISK_LEVEL,
            suggested_bet_ratio=self.SUGGESTED_RATIO,
            play_types=play_types,
            expected_win_rate=win_rate,
            expected_odds=avg_odds,
            expected_value=expected_value,
        )

    def _calculate_comprehensive_win_rate(self, play_types: list) -> float:
        """计算综合胜率（使用最低胜率作为保守估计）"""
        probs = []
        for play in play_types:
            prob_str = play.get("概率", "0%").rstrip("%")
            probs.append(float(prob_str) / 100.0)
        return min(probs) if probs else 0.0

    def _calculate_average_odds(self, play_types: list) -> float:
        """计算平均赔率"""
        odds = [play.get("参考赔率", 1.0) for play in play_types]
        return sum(odds) / len(odds) if odds else 1.0
