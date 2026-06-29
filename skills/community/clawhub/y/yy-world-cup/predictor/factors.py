"""
预测因子计算模块
实现10类预测因子的计算逻辑
"""

import math
from typing import List, Dict
from .data.models import (
    InjuryInfo, WeatherInfo, RecentMatch, TeamStyle, Position, WeatherCondition
)


class FactorCalculator:
    """预测因子计算器"""

    # 各因子权重
    WEIGHTS = {
        'elo': 0.35,
        'injury': 0.15,
        'form': 0.12,
        'weather': 0.08,
        'group_stage': 0.07,
        'attack_defense': 0.07,
        'home_advantage': 0.05,
        'draw_rate': 0.05,
        'draw_bias': 0.04,
        'tactical_matchup': 0.02,
    }

    @staticmethod
    def calculate_injury_factor(injuries: List[InjuryInfo]) -> float:
        """
        伤病影响系数，范围0.80-1.20（1.0为无影响）
        - 不同位置权重：GK 0.08, DF 0.06, MF 0.07, FW 0.09
        - 主力球员权重×1.5
        - 仅上场概率<50%才计算影响
        """
        if not injuries:
            return 1.0

        total_factor = 1.0
        pos_weight = {
            Position.GK: 0.08, Position.DF: 0.06,
            Position.MF: 0.07, Position.FW: 0.09,
        }

        for injury in injuries:
            weight = pos_weight.get(injury.position, 0.05)
            if injury.is_starter:
                weight *= 1.5
            # 仅上场概率<50%才计算伤病影响
            if injury.playing_probability < 0.5:
                impact = weight * (1 - injury.playing_probability)
                total_factor -= impact
        return max(0.80, min(1.20, total_factor))

    @staticmethod
    def calculate_weather_factor(weather: WeatherInfo, team_style: TeamStyle) -> float:
        """
        天气影响系数，范围0.90-1.10（1.0为无影响）
        - 降水>60%：技术型-0.06、防守型-0.01、身体型-0.02
        - 温度>35°C或<5°C：-0.04/-0.03
        - 风力≥4级：长传/反击型-0.03、技术型-0.02
        """
        if not weather:
            return 1.0

        factor = 1.0

        # 降水影响
        if weather.precipitation_probability > 60:
            if team_style == TeamStyle.TECHNICAL:
                factor -= 0.06
            elif team_style == TeamStyle.PHYSICAL:
                factor -= 0.02
            elif team_style == TeamStyle.DEFENSIVE:
                factor -= 0.01

        # 温度影响
        temp = weather.temperature
        if temp > 35:
            factor -= 0.04
        elif temp < 5:
            factor -= 0.03

        # 风力影响
        if weather.wind_level >= 4:
            if team_style in (TeamStyle.LONG_BALL, TeamStyle.COUNTER):
                factor -= 0.03
            elif team_style == TeamStyle.TECHNICAL:
                factor -= 0.02

        return max(0.90, min(1.10, factor))

    @staticmethod
    def calculate_form_factor(recent_matches: List[RecentMatch]) -> float:
        """
        近期状态因子，范围0.90-1.10（1.0为平均状态）
        权重：最近一场0.30，依次0.25/0.20/0.15/0.10
        加分：胜1.2×weight、平1.0×weight、负0.8×weight
        进球加分（最高0.10）、失球减分（最高0.10）
        """
        if not recent_matches:
            return 1.0

        weights = [0.30, 0.25, 0.20, 0.15, 0.10]
        form_score = 0.0

        for i, match in enumerate(recent_matches[:5]):
            weight = weights[i] if i < len(weights) else 0.05
            # 基础结果得分
            if match.result == "win":
                form_score += weight * 1.2
            elif match.result == "draw":
                form_score += weight * 1.0
            else:
                form_score += weight * 0.8

            # 进球加分（封顶0.10）
            form_score += weight * min(0.10, match.goals * 0.03)
            # 失球减分（封顶0.10）
            form_score -= weight * min(0.10, match.conceded * 0.03)

        return max(0.90, min(1.10, form_score))

    @staticmethod
    def calculate_group_stage_factor(
        home_standings: Dict = None,
        away_standings: Dict = None
    ) -> float:
        """
        小组排名与奖金激励因子，范围0.95-1.05（1.0为无影响）
        - 出线形势严峻的球队战意更强
        - 提前出线的球队可能轮换
        - 最后一轮生死战激励作用最大
        """
        if not home_standings:
            return 1.0

        factor = 1.0

        # 基于积分位置调整
        home_points = home_standings.get('points', 0)
        home_position = home_standings.get('position', 1)
        home_matches_played = home_standings.get('played', 0)
        home_qualified = home_standings.get('qualified', None)

        # 提前出线但还有比赛 → 战意下降
        if home_qualified is True and home_matches_played < 3:
            factor -= 0.03
        # 出线形势危急 → 战意提升
        elif home_qualified is False and home_matches_played == 2:
            factor += 0.04

        if away_standings:
            away_points = away_standings.get('points', 0)
            away_position = away_standings.get('position', 1)
            away_matches_played = away_standings.get('played', 0)
            away_qualified = away_standings.get('qualified', None)

            if away_qualified is True and away_matches_played < 3:
                factor += 0.03  # 对手可能放松，对主队有利
            elif away_qualified is False and away_matches_played == 2:
                factor -= 0.04  # 对手死拼，对主队不利

        return max(0.95, min(1.05, factor))

    @staticmethod
    def calculate_attack_defense_factor(
        home_goals: float, home_conceded: float,
        away_goals: float, away_conceded: float
    ) -> float:
        """
        攻防数据因子，范围0.92-1.08（1.0为平均）
        综合场均进球和失球数
        """
        # 进攻强度：主队进攻/客队平均失球
        home_attack = home_goals / max(0.5, away_conceded)
        away_attack = away_goals / max(0.5, home_conceded)

        # 防守强度：主队失球越少越好
        home_defense = away_conceded / max(0.5, home_goals)
        away_defense = home_conceded / max(0.5, away_goals)

        # 综合差值
        attack_diff = home_attack - away_attack
        defense_diff = home_defense - away_defense

        # 归一化到0.92-1.08区间
        factor = 1.0 + (attack_diff + defense_diff) * 0.04
        return max(0.92, min(1.08, factor))

    @staticmethod
    def calculate_draw_rate_factor(
        stage: str = "group",
        recent_draw_rate: float = 0.25
    ) -> float:
        """
        实时赛事平局率因子，范围0.95-1.05
        - 小组赛平局率通常较高
        - 淘汰赛平局率较低
        """
        stage_base_rate = {
            "group": 0.28,
            "round_of_16": 0.18,
            "quarter": 0.15,
            "semi": 0.12,
            "final": 0.10,
        }.get(stage, 0.25)

        # 同阶段赛事平局率偏离基准
        rate_diff = recent_draw_rate - stage_base_rate
        factor = 1.0 + rate_diff * 0.4
        return max(0.95, min(1.05, factor))

    @staticmethod
    def calculate_draw_bias_factor(
        historical_meetings: int = 0,
        historical_draws: int = 0
    ) -> float:
        """
        历史对战平局偏差因子，范围0.96-1.04
        """
        if historical_meetings == 0:
            return 1.0

        draw_ratio = historical_draws / historical_meetings
        # 历史平局率高于30%则略微提高平局概率
        factor = 1.0 + (draw_ratio - 0.25) * 0.15
        return max(0.96, min(1.04, factor))

    @staticmethod
    def calculate_tactical_matchup_factor(
        home_style: TeamStyle, away_style: TeamStyle
    ) -> float:
        """
        战术克制关系因子，范围0.97-1.03
        战术相克映射表（基于足球战术常识）
        """
        # 战术相克关系
        matchup = {
            (TeamStyle.ATTACKING, TeamStyle.DEFENSIVE): 1.02,
            (TeamStyle.DEFENSIVE, TeamStyle.ATTACKING): 0.98,
            (TeamStyle.TECHNICAL, TeamStyle.PHYSICAL): 1.02,
            (TeamStyle.PHYSICAL, TeamStyle.TECHNICAL): 0.98,
            (TeamStyle.COUNTER, TeamStyle.ATTACKING): 1.03,
            (TeamStyle.ATTACKING, TeamStyle.COUNTER): 0.97,
            (TeamStyle.LONG_BALL, TeamStyle.TECHNICAL): 1.02,
            (TeamStyle.TECHNICAL, TeamStyle.LONG_BALL): 0.98,
        }

        factor = matchup.get((home_style, away_style), 1.0)
        return max(0.97, min(1.03, factor))

    @classmethod
    def calculate_all_factors(
        cls,
        home_elo: int, away_elo: int,
        home_injuries: List[InjuryInfo], away_injuries: List[InjuryInfo],
        home_style: TeamStyle, away_style: TeamStyle,
        home_weather: WeatherInfo, away_weather: WeatherInfo,
        home_recent: List[RecentMatch], away_recent: List[RecentMatch],
        home_standings: Dict = None, away_standings: Dict = None,
        home_goals: float = 1.5, away_goals: float = 1.0,
        home_conceded: float = 1.0, away_conceded: float = 1.5,
        stage: str = "group",
        historical_meetings: int = 0,
        historical_draws: int = 0,
        recent_draw_rate: float = 0.25,
    ) -> Dict[str, float]:
        """
        计算所有因子的综合影响
        Returns: 包含各因子值和加权综合的字典
        """
        factors = {
            'injury': cls.calculate_injury_factor(home_injuries),
            'weather': cls.calculate_weather_factor(home_weather, home_style),
            'form': cls.calculate_form_factor(home_recent),
            'group_stage': cls.calculate_group_stage_factor(home_standings, away_standings),
            'attack_defense': cls.calculate_attack_defense_factor(
                home_goals, home_conceded, away_goals, away_conceded
            ),
            'tactical_matchup': cls.calculate_tactical_matchup_factor(home_style, away_style),
        }

        # 公共因子（不区分主客场）
        public_factors = {
            'draw_rate': cls.calculate_draw_rate_factor(stage, recent_draw_rate),
            'draw_bias': cls.calculate_draw_bias_factor(historical_meetings, historical_draws),
        }

        # 计算主队综合因子（伤病/天气/状态/小组/攻防/战术克制）
        home_factor = (
            factors['injury'] * 0.25 +
            factors['weather'] * 0.15 +
            factors['form'] * 0.20 +
            factors['group_stage'] * 0.10 +
            factors['attack_defense'] * 0.15 +
            factors['tactical_matchup'] * 0.15
        )

        # 计算客队因子
        away_factors = {
            'injury': cls.calculate_injury_factor(away_injuries),
            'weather': cls.calculate_weather_factor(away_weather, away_style),
            'form': cls.calculate_form_factor(away_recent),
            'tactical_matchup': cls.calculate_tactical_matchup_factor(away_style, home_style),
        }

        away_factor = (
            away_factors['injury'] * 0.30 +
            away_factors['weather'] * 0.15 +
            away_factors['form'] * 0.25 +
            away_factors['tactical_matchup'] * 0.10 +
            factors['attack_defense'] * 0.20
        )

        return {
            'home_factor': home_factor,
            'away_factor': away_factor,
            'home_detailed': factors,
            'away_detailed': away_factors,
            'public': public_factors,
        }
