#!/usr/bin/env python3

# pyright: reportMissingImports=false

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "yfinance",
# ]
# ///
#
"""
Stock Fundamentals - Get core fundamental metrics from Yahoo Finance using yfinance.
"""

import sys

from mutex import acquire_lock
from service import format_output, get_stock_fundamentals


def main():
    """Entry point - expects a stock ticker symbol as the first CLI argument."""
    if len(sys.argv) < 2:
        print("Usage: stock-fundamentals <SYMBOL>")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    with acquire_lock():
        result = get_stock_fundamentals(symbol)
    print(format_output(result))


if __name__ == "__main__":
    main()
