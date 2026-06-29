"""
单元测试 - 预测因子计算
"""

import unittest
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from predictor.factors import FactorCalculator
from predictor.data.models import InjuryInfo, WeatherInfo, RecentMatch, TeamStyle, Position, WeatherCondition


class TestInjuryFactor(unittest.TestCase):
    """测试伤病因子计算"""

    def test_no_injuries(self):
        factor = FactorCalculator.calculate_injury_factor([])
        self.assertEqual(factor, 1.0)

    def test_minor_injury_high_prob(self):
        """轻微伤病且上场概率>50%应该无影响"""
        injury = InjuryInfo(player_name="Test", is_starter=False,
                           playing_probability=0.8, position=Position.MF)
        factor = FactorCalculator.calculate_injury_factor([injury])
        self.assertEqual(factor, 1.0)

    def test_starter_injury(self):
        """主力球员伤病应该降低因子"""
        injury = InjuryInfo(player_name="Star", is_starter=True,
                           playing_probability=0.2, position=Position.FW)
        factor = FactorCalculator.calculate_injury_factor([injury])
        self.assertLess(factor, 1.0)
        self.assertGreaterEqual(factor, 0.80)

    def test_factor_bounds(self):
        """因子范围必须在0.80-1.20之间"""
        injuries = [
            InjuryInfo(f"P{i}", is_starter=True, playing_probability=0.0,
                      position=Position.FW)
            for i in range(10)
        ]
        factor = FactorCalculator.calculate_injury_factor(injuries)
        self.assertGreaterEqual(factor, 0.80)
        self.assertLessEqual(factor, 1.20)


class TestWeatherFactor(unittest.TestCase):
    """测试天气因子计算"""

    def test_normal_weather(self):
        weather = WeatherInfo(temperature=20, precipitation_probability=10,
                             wind_level=2, weather_condition=WeatherCondition.SUNNY)
        factor = FactorCalculator.calculate_weather_factor(weather, TeamStyle.BALANCED)
        self.assertEqual(factor, 1.0)

    def test_rain_affects_technical_team(self):
        weather = WeatherInfo(temperature=20, precipitation_probability=80,
                             wind_level=2, weather_condition=WeatherCondition.RAINY)
        factor = FactorCalculator.calculate_weather_factor(weather, TeamStyle.TECHNICAL)
        self.assertLess(factor, 1.0)

    def test_high_temp_negative(self):
        weather = WeatherInfo(temperature=38, precipitation_probability=10,
                             wind_level=2, weather_condition=WeatherCondition.SUNNY)
        factor = FactorCalculator.calculate_weather_factor(weather, TeamStyle.BALANCED)
        self.assertLess(factor, 1.0)


class TestFormFactor(unittest.TestCase):
    """测试近期状态因子"""

    def test_no_recent_matches(self):
        factor = FactorCalculator.calculate_form_factor([])
        self.assertEqual(factor, 1.0)

    def test_winning_streak(self):
        matches = [RecentMatch(result="win", goals=2, conceded=0) for _ in range(5)]
        factor = FactorCalculator.calculate_form_factor(matches)
        self.assertGreater(factor, 1.0)

    def test_losing_streak(self):
        matches = [RecentMatch(result="loss", goals=0, conceded=3) for _ in range(5)]
        factor = FactorCalculator.calculate_form_factor(matches)
        self.assertLess(factor, 1.0)


class TestTacticalMatchup(unittest.TestCase):
    """测试战术克制因子"""

    def test_attacking_vs_defensive(self):
        """进攻型对防守型：进攻型占优"""
        factor = FactorCalculator.calculate_tactical_matchup_factor(
            TeamStyle.ATTACKING, TeamStyle.DEFENSIVE
        )
        self.assertGreater(factor, 1.0)

    def test_counter_vs_attacking(self):
        """反击型对进攻型：反击型占优"""
        factor = FactorCalculator.calculate_tactical_matchup_factor(
            TeamStyle.COUNTER, TeamStyle.ATTACKING
        )
        self.assertGreater(factor, 1.0)

    def test_balanced_matchup(self):
        """平衡型对平衡型：中性"""
        factor = FactorCalculator.calculate_tactical_matchup_factor(
            TeamStyle.BALANCED, TeamStyle.BALANCED
        )
        self.assertEqual(factor, 1.0)


class TestStrategyOdds(unittest.TestCase):
    """测试赔率计算"""

    def test_high_prob_low_odds(self):
        from predictor.strategy.lottery import LotteryStrategyEngine
        odds = LotteryStrategyEngine.prob_to_odds(0.85)
        self.assertLess(odds, 1.20)

    def test_low_prob_high_odds(self):
        from predictor.strategy.lottery import LotteryStrategyEngine
        odds = LotteryStrategyEngine.prob_to_odds(0.05)
        self.assertGreater(odds, 15.0)

    def test_prob_to_odds_regression(self):
        """验证之前赔率bug已修复（不再全部返回20.0）"""
        from predictor.strategy.lottery import LotteryStrategyEngine
        # 之前所有概率都返回20.0
        probs = [0.85, 0.65, 0.45, 0.25, 0.10, 0.55]
        odds_list = [LotteryStrategyEngine.prob_to_odds(p) for p in probs]
        # 验证赔率是有差异的
        self.assertGreater(len(set(odds_list)), 3)
        # 验证赔率在合理范围内
        for odds in odds_list:
            self.assertGreater(odds, 1.0)
            self.assertLess(odds, 50.0)


if __name__ == '__main__':
    unittest.main()
