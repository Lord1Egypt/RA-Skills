"""
Utility functions.
"""

import os
from typing import List, Tuple


def parse_stock_codes(stock_string: str) -> List[str]:
    """
    Parse comma-separated stock codes.
    
    Args:
        stock_string: Comma-separated stock codes
        
    Returns:
        List of stock codes
    """
    return [code.strip() for code in stock_string.split(',') if code.strip()]


def detect_market(code: str) -> str:
    """
    Detect stock market from code.
    
    Args:
        code: Stock code
        
    Returns:
        Market type: 'A', 'HK', or 'US'
    """
    if code.startswith('hk'):
        return 'HK'
    elif code.startswith('us') or (len(code) <= 5 and code.isalpha()):
        return 'US'
    else:
        return 'A'


def format_symbol(code: str, market: str = None) -> str:
    """
    Format stock symbol for data source.
    
    Args:
        code: Stock code
        market: Market type (auto-detect if None)
        
    Returns:
        Formatted symbol
    """
    if market is None:
        market = detect_market(code)
    
    if market == 'HK':
        return code.replace('hk', '') + '.HK'
    elif market == 'US':
        return code.replace('us', '')
    else:  # A-share
        return code


def format_price(price: float, currency: str = 'CNY') -> str:
    """
    Format price with currency symbol.
    
    Args:
        price: Price value
        currency: Currency code
        
    Returns:
        Formatted price string
    """
    symbols = {
        'CNY': '¥',
        'USD': '$',
        'HKD': 'HK$',
    }
    symbol = symbols.get(currency, '')
    return f"{symbol}{price:.2f}"


def format_change(change: float, change_percent: float) -> str:
    """
    Format price change with color indicators.
    
    Args:
        change: Price change
        change_percent: Change percentage
        
    Returns:
        Formatted change string
    """
    if change > 0:
        sign = '+'
        color = '🟢'
    elif change < 0:
        sign = ''
        color = '🔴'
    else:
        sign = ''
        color = '⚪'
    
    return f"{color} {sign}{change:.2f} ({sign}{change_percent:.2f}%)"
