"""
核心预测引擎
实现双模式评分模型（爆冷/平衡）和比分预测
"""

import math
from typing import Tuple, List, Dict
from .data.models import MatchInfo, PredictionResult
from .factors import FactorCalculator


class WorldCupPredictor:
    """世界杯比赛预测器核心引擎"""

    ELO_DIFF_THRESHOLD = 15  # Elo差阈值，超过则启用爆冷模式
    HOME_ADVANTAGE_ELO = 70  # 主场优势Elo加成（真实主场）
    NEUTRAL_ADVANTAGE_ELO = 25  # 中立球场下的微弱主场优势（世界杯、欧洲杯）
    MIN_PROB = 0.05  # 最小概率
    MAX_PROB = 0.85  # 最大概率

    def __init__(self):
        self.factor_calculator = FactorCalculator()

    def _normalized_probabilities(
        self, win_prob: float, draw_prob: float, loss_prob: float
    ) -> Tuple[float, float, float]:
        """归一化概率到合法范围，确保和为1"""
        # 限制到合理区间
        win_prob = max(self.MIN_PROB, min(self.MAX_PROB, win_prob))
        loss_prob = max(self.MIN_PROB, min(self.MAX_PROB, loss_prob))
        draw_prob = max(0.08, min(0.45, draw_prob))

        # 归一化
        total = win_prob + draw_prob + loss_prob
        return win_prob / total, draw_prob / total, loss_prob / total

    def _balanced_mode(
        self, home_elo: int, away_elo: int,
        home_factor: float, away_factor: float,
        is_neutral: bool = False,
        stage: str = "group",
        matchday: int = 1
    ) -> Tuple[float, float, float]:
        """
        平衡模式：实力接近时使用压缩泊松模型
        基于Elo评分体系计算胜平负概率
        足球比赛平局概率实际较高（~26-30%），不能太低
        实力越接近，平局概率应越高
        小组赛首轮往往非常保守，平局概率进一步提升
        """
        # 主场优势（中立球场大幅降低）
        home_adv = self.NEUTRAL_ADVANTAGE_ELO if is_neutral else self.HOME_ADVANTAGE_ELO

        # 调整后的Elo差（应用各因子）
        elo_diff = (home_elo * home_factor) - (away_elo * away_factor)
        elo_diff += home_adv

        # 基于Elo差计算胜率（标准Elo公式）
        win_prob = 1.0 / (1.0 + 10 ** ((-(elo_diff)) / 400.0))

        # 平局概率：足球比赛基础平局率较高
        # 小组赛首轮比赛非常保守，引入"谨慎因子"（+5-8%）
        actual_elo_diff = abs(elo_diff - home_adv)
        if actual_elo_diff < 50:
            base_draw_prob = 0.40  # 实力接近时基础平局率高
        elif actual_elo_diff < 100:
            base_draw_prob = 0.36
        elif actual_elo_diff < 200:
            base_draw_prob = 0.30
        else:
            base_draw_prob = 0.25

        # 小组赛首轮（matchday=1）谨慎因子：+6%
        # 世界杯/欧洲杯这种大赛更明显
        if matchday == 1 and stage == "group":
            cautious_boost = 0.10
        elif matchday == 2 and stage == "group":
            cautious_boost = 0.10
        else:
            cautious_boost = 0.10
        base_draw_prob += cautious_boost

        draw_prob = max(0.20, min(0.50, base_draw_prob))

        # 失败概率
        loss_prob = 1.0 - win_prob - draw_prob

        return self._normalized_probabilities(win_prob, draw_prob, loss_prob)

    def _upset_mode(
        self, home_elo: int, away_elo: int,
        home_factor: float, away_factor: float,
        is_neutral: bool = False,
        stage: str = "group",
        matchday: int = 1
    ) -> Tuple[float, float, float]:
        """
        爆冷模式：实力差距大时使用进攻×防守弱点模型
        强队爆冷概率会显著提升（参考2022世界杯大量爆冷）
        2026世界杯首轮4场全平局证明：实力差距大≠容易出胜负
        """
        home_adv = self.NEUTRAL_ADVANTAGE_ELO if is_neutral else self.HOME_ADVANTAGE_ELO

        # 调整后的Elo
        adjusted_home = home_elo * home_factor
        adjusted_away = away_elo * away_factor
        elo_diff = adjusted_home - adjusted_away + home_adv

        # 绝对Elo差（用于计算强队胜率和爆冷因子）
        actual_diff = abs(elo_diff - home_adv)

        # 强队的基础胜率（绝对Elo差越大，胜率越高）
        stronger_win = 1.0 / (1.0 + 10 ** (-(actual_diff) / 400.0))

        # 爆冷因子：使用对数衰减，封顶0.30
        upset_factor = min(0.30, 0.10 * math.log(1.0 + actual_diff / 100.0))

        # 强队胜率因爆冷降低
        stronger_adjusted = stronger_win * (1.0 - upset_factor)

        # 平局概率：基础值大幅提升
        # 小组赛首轮谨慎：实力差距大时平局率也比平时高
        if actual_diff < 100:
            base_draw_prob = 0.36
        elif actual_diff < 200:
            base_draw_prob = 0.32
        elif actual_diff < 300:
            base_draw_prob = 0.30  # 实力悬殊但首轮保守
        else:
            base_draw_prob = 0.26

        # 大赛首轮谨慎因子
        if matchday == 1 and stage == "group":
            cautious_boost = 0.10
        elif matchday == 2 and stage == "group":
            cautious_boost = 0.10
        else:
            cautious_boost = 0.10
        base_draw_prob += cautious_boost

        draw_prob = max(0.20, min(0.50, base_draw_prob))

        # 弱队胜率 = 剩余概率
        weaker_prob = 1.0 - stronger_adjusted - draw_prob

        # 分配到主胜/客胜
        if elo_diff > 0:
            # 主队是强队
            win_prob = stronger_adjusted
            loss_prob = max(0.05, weaker_prob)
        else:
            # 客队是强队
            loss_prob = stronger_adjusted
            win_prob = max(0.05, weaker_prob)

        return self._normalized_probabilities(win_prob, draw_prob, loss_prob)

    def _poisson_prob(self, k: int, lam: float) -> float:
        """泊松分布概率"""
        if lam <= 0:
            return 1.0 if k == 0 else 0.0
        return (lam ** k) * math.exp(-lam) / math.factorial(k)

    def _predict_scores(
        self,
        win_prob: float, draw_prob: float, loss_prob: float,
        home_goals: float, away_goals: float,
        n: int = 3
    ) -> List[Tuple[str, float]]:
        """预测最可能的n组比分"""
        # 常见比分组合
        possible_scores = [
            (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1),
            (0, 0), (1, 1), (2, 2), (3, 3),
            (0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3), (0, 4), (1, 4),
        ]

        scores = []
        for hg, ag in possible_scores:
            hg_prob = self._poisson_prob(hg, home_goals)
            ag_prob = self._poisson_prob(ag, away_goals)

            # 根据胜平负概率加权
            if hg > ag:
                weight = win_prob * 2
            elif hg == ag:
                weight = draw_prob * 2
            else:
                weight = loss_prob * 2

            prob = hg_prob * ag_prob * weight
            scores.append((f"{hg}-{ag}", prob))

        # 按概率排序，取前n个并归一化
        scores.sort(key=lambda x: x[1], reverse=True)
        top_scores = scores[:n]
        total = sum(p for _, p in top_scores)
        if total > 0:
            return [(s, p / total) for s, p in top_scores]
        return [(s, 1.0 / n) for s, _ in top_scores]

    def _calculate_goals_prob(
        self, scores: List[Tuple[str, float]]
    ) -> List[Tuple[int, float]]:
        """计算总进球数概率分布（0-7球）"""
        goal_probs = {i: 0.0 for i in range(8)}  # 0-7球
        for score, prob in scores:
            hg, ag = map(int, score.split('-'))
            total = hg + ag
            if total <= 7:
                goal_probs[total] += prob

        # 按概率排序
        result = sorted(goal_probs.items(), key=lambda x: x[1], reverse=True)
        # 归一化
        total_sum = sum(p for _, p in result)
        if total_sum > 0:
            result = [(g, p / total_sum) for g, p in result]
        return result

    def _calculate_ht_ft_probs(
        self, win_prob: float, draw_prob: float, loss_prob: float
    ) -> Dict[str, float]:
        """计算半全场概率（简化模型）"""
        # 半全场组合（9种）
        return {
            "胜胜": round(win_prob * 0.55, 4),
            "胜平": round(win_prob * 0.20, 4),
            "胜负": round(win_prob * 0.25, 4),
            "平胜": round(draw_prob * 0.30, 4),
            "平平": round(draw_prob * 0.40, 4),
            "平负": round(draw_prob * 0.30, 4),
            "负胜": round(loss_prob * 0.25, 4),
            "负平": round(loss_prob * 0.20, 4),
            "负负": round(loss_prob * 0.55, 4),
        }

    def predict(self, match: MatchInfo) -> PredictionResult:
        """预测比赛结果"""
        # 计算所有因子
        factors = self.factor_calculator.calculate_all_factors(
            home_elo=match.home_team.elo,
            away_elo=match.away_team.elo,
            home_injuries=match.home_injuries,
            away_injuries=match.away_injuries,
            home_style=match.home_team.style,
            away_style=match.away_team.style,
            home_weather=match.weather,
            away_weather=match.weather,  # 同一场比赛天气相同
            home_recent=match.home_recent,
            away_recent=match.away_recent,
            home_standings=match.group_standings_home,
            away_standings=match.group_standings_away,
            home_goals=match.home_goals_per_match,
            away_goals=match.away_goals_per_match,
            home_conceded=match.home_conceded_per_match,
            away_conceded=match.away_conceded_per_match,
            stage=match.stage,
        )

        # 选择预测模式
        elo_diff = abs(match.home_team.elo - match.away_team.elo)
        is_neutral = match.is_neutral
        stage = match.stage
        # 推断matchday：基于比赛时间字段（这里简单假设都为第1轮）
        matchday = 1
        if elo_diff >= self.ELO_DIFF_THRESHOLD:
            win_prob, draw_prob, loss_prob = self._upset_mode(
                match.home_team.elo, match.away_team.elo,
                factors['home_factor'], factors['away_factor'],
                is_neutral=is_neutral, stage=stage, matchday=matchday
            )
            mode = "爆冷模式"
        else:
            win_prob, draw_prob, loss_prob = self._balanced_mode(
                match.home_team.elo, match.away_team.elo,
                factors['home_factor'], factors['away_factor'],
                is_neutral=is_neutral, stage=stage, matchday=matchday
            )
            mode = "平衡模式"

        # 预测比分
        scores = self._predict_scores(
            win_prob, draw_prob, loss_prob,
            match.home_goals_per_match, match.away_goals_per_match
        )

        # 总进球数概率
        goals_prob = self._calculate_goals_prob(scores)

        # 半全场概率
        ht_ft_probs = self._calculate_ht_ft_probs(win_prob, draw_prob, loss_prob)

        return PredictionResult(
            home_win_prob=win_prob,
            draw_prob=draw_prob,
            away_win_prob=loss_prob,
            predicted_scores=scores,
            total_goals_prob=goals_prob,
            ht_ft_probs=ht_ft_probs,
            predict_mode=mode,
        )
