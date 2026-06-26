"""
yfinance skill - A wrapper for Yahoo Finance data retrieval.

This skill provides a convenient client for querying US and Hong Kong stock data
using the yfinance library. It supports retrieving:
- Stock prices and historical data
- Company information and fundamentals
- Analyst recommendations and price targets
- Market sector and industry data
- Stock screener queries
- Real-time news
"""

__version__ = "0.1.0"

from yfinance_skill.client import YFinanceClient

__all__ = ["YFinanceClient"]
