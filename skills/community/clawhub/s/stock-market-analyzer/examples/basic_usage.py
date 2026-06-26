"""
Basic usage example for Stock Market Analyzer
"""

from scripts.stock_analyzer import (
    query_realtime_price,
    query_technical_indicators,
    query_open_summary,
    query_close_summary,
    analyze_portfolio
)

# Example 1: Query real-time price for Kweichow Moutai
print("=" * 50)
print("Example 1: Real-time Price Query")
print("=" * 50)
result = query_realtime_price("600519.SH")
print(f"Stock: 600519.SH (Kweichow Moutai)")
print(f"Result: {result}")
print()

# Example 2: Query technical indicators for Ping An Bank
print("=" * 50)
print("Example 2: Technical Indicators")
print("=" * 50)
result = query_technical_indicators("000001.SZ")
print(f"Stock: 000001.SZ (Ping An Bank)")
print(f"Result: {result}")
print()

# Example 3: Query opening summary
print("=" * 50)
print("Example 3: Opening Summary")
print("=" * 50)
result = query_open_summary("600519.SH")
print(f"Stock: 600519.SH")
print(f"Result: {result}")
print()

# Example 4: Query closing summary for multiple stocks
print("=" * 50)
print("Example 4: Closing Summary (Multiple Stocks)")
print("=" * 50)
result = query_close_summary("000001.SZ,600519.SH")
print(f"Stocks: 000001.SZ, 600519.SH")
print(f"Result: {result}")
print()

# Example 5: Portfolio analysis
print("=" * 50)
print("Example 5: Portfolio Analysis")
print("=" * 50)
portfolio = ["600519.SH", "000001.SZ", "000858.SZ"]
result = analyze_portfolio(portfolio)
print(f"Portfolio: {portfolio}")
print(f"Analysis: {result}")
