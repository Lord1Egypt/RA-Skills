"""数据采集工具模块

包含:
1. TushareTools: Tushare 数据接口
2. AKShareTools: AKShare 数据接口
3. AgentScope Toolkit: 使用 AgentScope Toolkit 注册的工具函数
"""

from .tushare_tools import TushareTools
from .akshare_tools import AKShareTools
from .toolkit import (
    create_stock_toolkit,
    create_market_analyst_toolkit,
    create_fundamentals_analyst_toolkit,
    create_news_analyst_toolkit,
    # 工具函数
    get_stock_daily,
    get_technical_indicators,
    get_stock_basic,
    get_valuation,
    get_financial_indicator,
    get_stock_news,
    get_market_sentiment,
)

__all__ = [
    # 基础工具类
    "TushareTools", 
    "AKShareTools",
    
    # AgentScope Toolkit
    "create_stock_toolkit",
    "create_market_analyst_toolkit",
    "create_fundamentals_analyst_toolkit",
    "create_news_analyst_toolkit",
    
    # 工具函数
    "get_stock_daily",
    "get_technical_indicators",
    "get_stock_basic",
    "get_valuation",
    "get_financial_indicator",
    "get_stock_news",
    "get_market_sentiment",
]
