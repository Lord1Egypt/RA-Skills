"""
激进策略
高赔率、中等胜率，多串关或高赔玩法组合，目标命中率≥25%
"""

from ..data.models import PredictionResult, BettingStrategy
from .lottery import LotteryStrategyEngine


class AggressiveStrategy(LotteryStrategyEngine):
    """激进策略生成器"""

    STRATEGY_NAME = "激进策略"
    RISK_LEVEL = "中高"
    SUGGESTED_RATIO = "30%"
    TARGET_WIN_RATE = 0.25
    TARGET_ODDS_MIN = 3.00
    TARGET_ODDS_MAX = 15.00

    def generate(self, prediction: PredictionResult) -> BettingStrategy:
        """生成激进策略"""
        play_types = []

        # 1. 比分玩法（高赔率）
        score_play = self.create_score_strategy(prediction)
        play_types.append(score_play)

        # 2. 半全场玩法
        ht_ft_play = self.create_ht_ft_strategy(prediction)
        play_types.append(ht_ft_play)

        # 3. 总进球数中等奖项
        goals_strategies = self.create_total_goals_strategy(prediction)
        if len(goals_strategies) >= 2:
            play_types.append(goals_strategies[1])

        # 计算综合胜率和赔率（激进策略使用几何平均）
        win_rate = self._calculate_geometric_win_rate(play_types)
        # 串关赔率（2串1）
        combo_odds = self._calculate_combo_odds(play_types)
        expected_value = (win_rate * combo_odds) - 1.0

        return BettingStrategy(
            strategy_name=self.STRATEGY_NAME,
            risk_level=self.RISK_LEVEL,
            suggested_bet_ratio=self.SUGGESTED_RATIO,
            play_types=play_types,
            expected_win_rate=win_rate,
            expected_odds=combo_odds,
            expected_value=expected_value,
        )

    def _calculate_geometric_win_rate(self, play_types: list) -> float:
        """计算综合胜率（几何平均，更适合串关）"""
        probs = []
        for play in play_types:
            prob_str = play.get("概率", "0%").rstrip("%")
            probs.append(float(prob_str) / 100.0)

        if not probs:
            return 0.0

        # 几何平均
        product = 1.0
        for p in probs:
            product *= p
        return product ** (1.0 / len(probs))

    def _calculate_combo_odds(self, play_types: list) -> float:
        """计算串关赔率（2串1）"""
        # 取前两个最高赔率玩法进行2串1
        sorted_plays = sorted(play_types, key=lambda x: x.get("参考赔率", 1.0), reverse=True)
        top_two = sorted_plays[:2]
        combo_odds = 1.0
        for play in top_two:
            combo_odds *= play.get("参考赔率", 1.0)
        return round(combo_odds, 2)
