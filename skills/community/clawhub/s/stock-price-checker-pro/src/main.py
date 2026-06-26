#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "yfinance",
# ]
# ///
#
"""
Stock Price Checker - Get current stock prices from Yahoo Finance using yfinance.
"""

import sys

from mutex import acquire_lock
from service import format_output, get_stock_price


def main():
    """Entry point - expects a stock ticker symbol as the first CLI argument."""
    if len(sys.argv) < 2:
        print("Usage: stock-price <SYMBOL>")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    with acquire_lock():
        result = get_stock_price(symbol)
    print(format_output(result))


if __name__ == "__main__":
    main()
