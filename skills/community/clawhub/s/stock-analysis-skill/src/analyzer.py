#!/usr/bin/env python3
"""
Stock Analysis Skill for OpenClaw

Intelligent stock analysis system with:
- Multi-market support (A/H/US stocks)
- Real-time quotes from multiple sources
- Technical and sentiment analysis
- AI-powered decision dashboard
"""

import os
import sys
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from data_sources import YahooFinanceDataSource, AkShareDataSource, TushareDataSource
from analysis import TechnicalAnalyzer, NewsSentimentAnalyzer, DecisionDashboard
from utils import parse_stock_codes, detect_market, format_symbol


class StockAnalyzer:
    """Main stock analysis engine."""
    
    def __init__(self):
        """Initialize stock analyzer with all data sources and analyzers."""
        # Data sources
        self.yahoo = YahooFinanceDataSource()
        self.akshare = AkShareDataSource()
        
        # Tushare (optional backup)
        tushare_token = os.getenv('TUSHARE_TOKEN')
        if tushare_token:
            self.tushare = TushareDataSource(tushare_token)
        else:
            self.tushare = None
        
        # Analyzers
        self.technical = TechnicalAnalyzer()
        
        # News sentiment (optional)
        tavily_key = os.getenv('TAVILY_API_KEY')
        self.sentiment = NewsSentimentAnalyzer(tavily_key) if tavily_key else None
        
        # Decision dashboard
        self.dashboard = DecisionDashboard()
    
    def get_quote(self, code: str) -> Dict:
        """
        Get real-time quote with automatic source selection.
        
        Args:
            code: Stock code
            
        Returns:
            Quote data
        """
        market = detect_market(code)
        
        if market == 'US' or market == 'HK':
            symbol = format_symbol(code, market)
            return self.yahoo.get_quote(symbol)
        else:  # A-share
            # Try AkShare first
            quote = self.akshare.get_quote(code)
            
            # Fallback to Tushare if AkShare fails
            if quote.get('price', 0) == 0 and self.tushare:
                quote = self.tushare.get_quote(code)
            
            return quote
    
    def get_technical_analysis(self, code: str, market: str = None) -> Dict:
        """
        Get technical analysis.
        
        Args:
            code: Stock code
            market: Market type
            
        Returns:
            Technical indicators
        """
        if market is None:
            market = detect_market(code)
        
        if market == 'US' or market == 'HK':
            symbol = format_symbol(code, market)
            history = self.yahoo.get_history(symbol)
            return self.technical.analyze(code, history)
        else:
            # A-share technical analysis (simplified)
            return self.technical.analyze(code)
    
    def get_news_sentiment(self, code: str) -> Dict:
        """
        Get news sentiment analysis.
        
        Args:
            code: Stock code
            
        Returns:
            Sentiment data
        """
        if not self.sentiment:
            return {
                'news_count': 0,
                'sentiment': 'neutral',
                'sentiment_score': 0.5,
                'note': 'TAVILY_API_KEY not configured',
            }
        
        return self.sentiment.analyze(code)
    
    def analyze_stock(self, code: str) -> Dict:
        """
        Complete stock analysis.
        
        Args:
            code: Stock code
            
        Returns:
            Complete analysis results
        """
        # Get quote
        quote = self.get_quote(code)
        
        # Get technical analysis
        market = detect_market(code)
        technical = self.get_technical_analysis(code, market)
        
        # Get news sentiment
        news = self.get_news_sentiment(code)
        
        # Generate decision dashboard
        dashboard = self.dashboard.generate(code, quote, technical, news)
        
        return {
            'code': code,
            'quote': quote,
            'technical': technical,
            'news': news,
            'dashboard': dashboard,
        }
    
    def analyze_stocks(self, codes: List[str]) -> str:
        """
        Analyze multiple stocks and generate report.
        
        Args:
            codes: List of stock codes
            
        Returns:
            Formatted report
        """
        results = []
        
        for code in codes:
            try:
                result = self.analyze_stock(code)
                results.append(result)
            except Exception as e:
                results.append({
                    'code': code,
                    'error': str(e),
                })
        
        # Format report
        return self._format_report(results)
    
    def _format_report(self, results: List[Dict]) -> str:
        """Format analysis results as report."""
        lines = []
        lines.append("📊 股票智能分析报告")
        lines.append(f"\n分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"分析股票数：{len(results)}")
        lines.append("=" * 60)
        lines.append("")
        
        for result in results:
            if 'error' in result:
                lines.append(f"❌ {result['code']}: {result['error']}")
                lines.append("-" * 60)
                continue
            
            dashboard = result['dashboard']
            quote = result['quote']
            
            lines.append(f"{dashboard['action']} {result['code']}")
            lines.append(f"当前价格：{quote.get('price', 'N/A')}")
            lines.append(f"涨跌幅：{quote.get('change_percent', 0):.2f}%")
            lines.append(f"建议：{dashboard['recommendation']}")
            lines.append(f"目标价：{dashboard['target_price']}")
            lines.append(f"止损价：{dashboard['stop_loss']}")
            lines.append(f"置信度：{dashboard['confidence']}")
            lines.append(f"理由：{dashboard['reasoning']}")
            
            if dashboard.get('news_count', 0) > 0:
                lines.append(f"新闻：{dashboard['news_count']}条，{dashboard['news_sentiment']}情绪")
            
            lines.append("-" * 60)
            lines.append("")
        
        lines.append("\n⚠️ 免责声明：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。")
        
        return '\n'.join(lines)


def analyze_stocks(stock_codes: List[str], use_llm: bool = True) -> str:
    """
    Analyze multiple stocks (convenience function).
    
    Args:
        stock_codes: List of stock codes
        use_llm: Whether to use LLM (reserved for future)
        
    Returns:
        Formatted report
    """
    analyzer = StockAnalyzer()
    return analyzer.analyze_stocks(stock_codes)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <stock_codes>")
        print("  stock_codes: Comma-separated stock codes (e.g., 600519,hk00700,AAPL)")
        sys.exit(1)
    
    codes = parse_stock_codes(sys.argv[1])
    report = analyze_stocks(codes)
    print(report)
