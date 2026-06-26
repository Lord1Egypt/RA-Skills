"""
Decision Dashboard Module

Generates AI-powered trading decisions:
- Buy/Sell/Hold recommendations
- Target and stop-loss prices
- Confidence scoring
- Clear reasoning
"""


class DecisionDashboard:
    """AI-powered decision dashboard generator."""
    
    def __init__(self):
        import logging
        self.logger = logging.getLogger(__name__)
    
    def generate(self, stock_code: str, quote: dict, technical: dict, news: dict) -> dict:
        """
        Generate decision dashboard.
        
        Args:
            stock_code: Stock code
            quote: Real-time quote data
            technical: Technical analysis data
            news: News sentiment data
            
        Returns:
            Decision dashboard with recommendation
        """
        try:
            price = quote.get('price', 0)
            change_percent = quote.get('change_percent', 0)
            trend = technical.get('trend', 'neutral')
            
            # News sentiment
            sentiment = news.get('sentiment', 'neutral')
            sentiment_score = news.get('sentiment_score', 0.5)
            news_count = news.get('news_count', 0)
            
            # Scoring system
            score = 50  # Base score
            
            # Technical score (±20)
            if trend == 'bullish':
                score += 20
            elif trend == 'bearish':
                score -= 20
            
            # Price change score (±10)
            if change_percent > 3:
                score += 10
            elif change_percent < -3:
                score -= 10
            
            # News sentiment score (±20)
            if sentiment == 'positive':
                score += int(sentiment_score * 20)
            elif sentiment == 'negative':
                score -= int((1 - sentiment_score) * 20)
            
            # Determine recommendation
            if score >= 70:
                recommendation = 'BUY'
                action = '🟢 买入'
            elif score <= 30:
                recommendation = 'SELL'
                action = '🔴 卖出'
            else:
                recommendation = 'HOLD'
                action = '🟡 观望'
            
            # Calculate target and stop-loss
            target_price, stop_loss = self._calculate_price_levels(
                price, recommendation
            )
            
            # Build reasoning
            reasoning = self._build_reasoning(trend, change_percent, sentiment, sentiment_score, news_count)
            
            return {
                'stock_code': stock_code,
                'recommendation': recommendation,
                'action': action,
                'score': score,
                'current_price': price,
                'target_price': target_price,
                'stop_loss': stop_loss,
                'confidence': 'high' if score >= 70 or score <= 30 else 'medium',
                'reasoning': reasoning,
                'news_sentiment': sentiment,
                'news_count': news_count,
            }
        except Exception as e:
            self.logger.error(f"Decision dashboard error for {stock_code}: {e}")
            return self._get_default_dashboard(stock_code)
    
    def _calculate_price_levels(self, price: float, recommendation: str) -> tuple:
        """Calculate target and stop-loss prices."""
        if recommendation == 'BUY':
            target = round(price * 1.1, 2)
            stop_loss = round(price * 0.95, 2)
        elif recommendation == 'SELL':
            target = round(price * 0.9, 2)
            stop_loss = round(price * 1.05, 2)
        else:  # HOLD
            target = round(price * 1.05, 2)
            stop_loss = round(price * 0.95, 2)
        
        return target, stop_loss
    
    def _build_reasoning(self, trend: str, change_percent: float, 
                        sentiment: str, sentiment_score: float, news_count: int) -> str:
        """Build clear reasoning string."""
        parts = [f"技术趋势：{trend}", f"涨跌幅：{change_percent:.2f}%"]
        
        if news_count > 0:
            parts.append(f"舆情：{sentiment} ({sentiment_score:.2f})")
        
        return ', '.join(parts)
    
    def _get_default_dashboard(self, stock_code: str) -> dict:
        """Return default dashboard."""
        return {
            'stock_code': stock_code,
            'recommendation': 'HOLD',
            'action': '🟡 观望',
            'score': 50,
            'current_price': 0,
            'target_price': 0,
            'stop_loss': 0,
            'confidence': 'low',
            'reasoning': '数据不足',
            'news_sentiment': 'neutral',
            'news_count': 0,
        }
