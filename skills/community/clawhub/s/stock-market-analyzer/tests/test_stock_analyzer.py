"""
Unit tests for Stock Market Analyzer
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.stock_analyzer import (
    query_realtime_price,
    query_technical_indicators,
    query_open_summary,
    query_close_summary,
    analyze_portfolio
)


class TestStockAnalyzer(unittest.TestCase):
    """Test cases for stock analyzer functions"""
    
    def test_query_realtime_price_structure(self):
        """Test that query_realtime_price returns a dict"""
        result = query_realtime_price("600519.SH")
        self.assertIsInstance(result, dict)
    
    def test_query_technical_indicators_structure(self):
        """Test that query_technical_indicators returns a dict"""
        result = query_technical_indicators("000001.SZ")
        self.assertIsInstance(result, dict)
    
    def test_query_open_summary_structure(self):
        """Test that query_open_summary returns a dict"""
        result = query_open_summary("600519.SH")
        self.assertIsInstance(result, dict)
    
    def test_query_close_summary_structure(self):
        """Test that query_close_summary returns a dict"""
        result = query_close_summary("600519.SH")
        self.assertIsInstance(result, dict)
    
    def test_analyze_portfolio_structure(self):
        """Test that analyze_portfolio returns correct structure"""
        portfolio = ["600519.SH", "000001.SZ"]
        result = analyze_portfolio(portfolio)
        self.assertIsInstance(result, dict)
        self.assertIn("portfolio", result)
        self.assertIn("count", result)
        self.assertIn("timestamp", result)
    
    def test_portfolio_count(self):
        """Test that portfolio count matches input"""
        portfolio = ["600519.SH", "000001.SZ"]
        result = analyze_portfolio(portfolio)
        self.assertEqual(result["count"], len(portfolio))


if __name__ == "__main__":
    unittest.main(verbosity=2)
