"""
足彩分析助手 - Football Betting Analyzer

提供足球比赛数据分析、赔率分析、投注建议
"""

__version__ = "1.0.0"
__author__ = "shenmeng"

from .analyzer import FootballBettingAnalyzer
from .odds_analyzer import (
    AsianHandicap,
    EuropeanOdds,
    KellyCalculator,
    ComprehensiveOddsAnalyzer
)
from .utils import (
    calculate_stake,
    generate_parlay_combinations,
    BankrollManager,
    format_analysis_report
)

__all__ = [
    "FootballBettingAnalyzer",
    "AsianHandicap",
    "EuropeanOdds",
    "KellyCalculator",
    "ComprehensiveOddsAnalyzer",
    "calculate_stake",
    "generate_parlay_combinations",
    "BankrollManager",
    "format_analysis_report",
]
