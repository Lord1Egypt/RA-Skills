"""
数据接入层
封装API客户端、缓存机制、数据模型
"""

from .models import (
    Team, Stadium, MatchInfo, InjuryInfo, WeatherInfo, RecentMatch,
    PredictionResult, BettingStrategy,
    TeamStyle, Position, WeatherCondition
)
from .api_client import BalldontlieFIFAClient, get_team_style
from .polymarket_client import PolymarketClient, PolymarketAPIError
from .weather_client import WeatherClient, WORLD_CUP_2026_VENUES
from .cache import FileCache, get_cache

__all__ = [
    'Team', 'Stadium', 'MatchInfo', 'InjuryInfo', 'WeatherInfo', 'RecentMatch',
    'PredictionResult', 'BettingStrategy',
    'TeamStyle', 'Position', 'WeatherCondition',
    'BalldontlieFIFAClient', 'get_team_style',
    'PolymarketClient', 'PolymarketAPIError',
    'WeatherClient', 'WORLD_CUP_2026_VENUES',
    'FileCache', 'get_cache',
]
