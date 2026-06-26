"""
Trading Agents 股票投资分析系统
基于 AgentScope 的多智能体股票诊断技能
"""

from .config import config, Config
from .stock_advisor import StockAdvisorSystem

__version__ = "1.0.0"
__all__ = ["config", "Config", "StockAdvisorSystem"]
