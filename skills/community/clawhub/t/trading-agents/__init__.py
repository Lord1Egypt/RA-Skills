"""
Trading Agents 股票投资分析系统
基于 AgentScope 的多智能体股票诊断技能
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"

# 导出主要类
from .scripts.stock_advisor import StockAdvisorSystem
from .scripts.config import config

__all__ = ["StockAdvisorSystem", "config"]
