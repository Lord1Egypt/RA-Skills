"""
PyWenCai 股票数据技能
提供同花顺问财API的简易访问接口
"""

from .search import (
    search,
    hot_sectors,
    top_gainers,
    top_losers,
    dragon_tiger_list,
    search_stock_by_code
)

__all__ = [
    'search',
    'hot_sectors',
    'top_gainers',
    'top_losers',
    'dragon_tiger_list',
    'search_stock_by_code'
]

__version__ = '1.0.0'
