"""
增强版世界杯预测器
主入口包
"""

from .data import (
    Team, Stadium, MatchInfo, InjuryInfo, WeatherInfo, RecentMatch,
    PredictionResult, BettingStrategy,
    TeamStyle, Position, WeatherCondition,
    BalldontlieFIFAClient, get_team_style,
    PolymarketClient, WeatherClient, WORLD_CUP_2026_VENUES
)
from .factors import FactorCalculator
from .core import WorldCupPredictor
from .strategy.lottery import LotteryStrategyEngine
from .strategy.conservative import ConservativeStrategy
from .strategy.aggressive import AggressiveStrategy
from .ml_enhancer import MLEnhancer
from .calibration import MarketCalibrator

__all__ = [
    'Team', 'Stadium', 'MatchInfo', 'InjuryInfo', 'WeatherInfo', 'RecentMatch',
    'PredictionResult', 'BettingStrategy',
    'TeamStyle', 'Position', 'WeatherCondition',
    'BalldontlieFIFAClient', 'get_team_style',
    'PolymarketClient', 'WeatherClient', 'WORLD_CUP_2026_VENUES',
    'FactorCalculator', 'WorldCupPredictor',
    'LotteryStrategyEngine', 'ConservativeStrategy', 'AggressiveStrategy',
    'MLEnhancer', 'MarketCalibrator',
]

__version__ = '3.6.0'
