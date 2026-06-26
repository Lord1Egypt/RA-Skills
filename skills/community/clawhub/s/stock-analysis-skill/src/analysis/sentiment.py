"""
News and Sentiment Analysis Module

Provides news search and sentiment analysis:
- Tavily Search API integration
- Keyword-based sentiment analysis
- Sentiment scoring
"""

import os
from .base import AnalysisBase


class NewsSentimentAnalyzer(AnalysisBase):
    """News sentiment analysis using Tavily Search API."""
    
    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key or os.getenv('TAVILY_API_KEY')
        
        if not self.api_key:
            self.logger.warning("TAVILY_API_KEY not configured - news sentiment disabled")
    
    def analyze(self, stock_code: str, days: int = 3) -> dict:
        """
        Analyze news sentiment for a stock.
        
        Args:
            stock_code: Stock code
            days: Number of days to search news
            
        Returns:
            Dictionary with sentiment data
        """
        if not self.api_key:
            return self._get_empty_sentiment('TAVILY_API_KEY not configured')
        
        try:
            return self._tavily_search(stock_code, days)
        except Exception as e:
            self.logger.error(f"News sentiment error for {stock_code}: {e}")
            return self._get_empty_sentiment(str(e))
    
    def _tavily_search(self, stock_code: str, days: int) -> dict:
        """Search news using Tavily API."""
        import requests
        
        search_query = f"{stock_code} stock news analysis {days} days"
        
        url = "https://api.tavily.com/search"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        data = {
            'query': search_query,
            'search_depth': 'advanced',
            'max_results': 10,
            'include_answer': True,
            'include_raw_content': False
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        results = response.json()
        return self._analyze_sentiment(results, stock_code)
    
    def _analyze_sentiment(self, results: dict, stock_code: str) -> dict:
        """Analyze sentiment from search results."""
        news_items = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        # Keywords for sentiment analysis
        positive_words = [
            'buy', 'upgrade', 'beat', 'surge', 'gain', 'rise', 'positive',
            'bullish', 'outperform', 'growth', 'strong', 'exceed', 'profit'
        ]
        negative_words = [
            'sell', 'downgrade', 'miss', 'drop', 'loss', 'fall', 'negative',
            'bearish', 'underperform', 'decline', 'weak', 'below', 'warning'
        ]
        
        for result in results.get('results', []):
            title = result.get('title', '')
            content = result.get('content', '')
            text = (title + ' ' + content).lower()
            
            # Analyze sentiment
            pos_score = sum(1 for word in positive_words if word in text)
            neg_score = sum(1 for word in negative_words if word in text)
            
            if pos_score > neg_score:
                positive_count += 1
                sentiment = 'positive'
            elif neg_score > pos_score:
                negative_count += 1
                sentiment = 'negative'
            else:
                neutral_count += 1
                sentiment = 'neutral'
            
            news_items.append({
                'title': title,
                'url': result.get('url', ''),
                'sentiment': sentiment,
            })
        
        # Calculate overall sentiment score
        total = positive_count + negative_count + neutral_count
        if total == 0:
            overall_sentiment = 'neutral'
            sentiment_score = 0.5
        else:
            sentiment_score = (positive_count * 1.0 + neutral_count * 0.5 + negative_count * 0.0) / total
            
            if sentiment_score > 0.6:
                overall_sentiment = 'positive'
            elif sentiment_score < 0.4:
                overall_sentiment = 'negative'
            else:
                overall_sentiment = 'neutral'
        
        return {
            'news_count': len(news_items),
            'sentiment': overall_sentiment,
            'sentiment_score': round(sentiment_score, 2),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'news_items': news_items[:5],  # Top 5 news
            'source': 'tavily',
        }
    
    def _get_empty_sentiment(self, reason: str) -> dict:
        """Return empty sentiment data."""
        return {
            'news_count': 0,
            'sentiment': 'neutral',
            'sentiment_score': 0.5,
            'positive_count': 0,
            'negative_count': 0,
            'neutral_count': 0,
            'news_items': [],
            'source': 'none',
            'note': reason,
        }
