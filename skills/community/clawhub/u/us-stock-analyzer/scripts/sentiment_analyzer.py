"""
VIX Market Sentiment Analyzer
Analyzes market sentiment using VIX and related indicators.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SentimentResult:
    """Sentiment analysis result container."""
    sentiment_score: int  # 0-100
    market_regime: str  # "risk_on", "neutral", "risk_off", "panic"
    vix_level: str  # "low", "normal", "elevated", "high"
    buy_signal: bool
    risk_assessment: str
    indicators: Dict


class VIXSentimentAnalyzer:
    """
    Analyzes market sentiment using:
    - VIX absolute level
    - VIX term structure (futures curve)
    - Put/Call ratios
    - Implied volatility rank
    - Market breadth
    """
    
    def __init__(self,
                 vix_low_threshold: float = 15,
                 vix_normal_threshold: float = 20,
                 vix_high_threshold: float = 25,
                 vix_panic_threshold: float = 30,
                 max_iv_rank: float = 70):
        self.vix_low = vix_low_threshold
        self.vix_normal = vix_normal_threshold
        self.vix_high = vix_high_threshold
        self.vix_panic = vix_panic_threshold
        self.max_iv_rank = max_iv_rank
    
    def analyze(self, 
                vix_data: pd.DataFrame,
                options_data: Optional[Dict] = None,
                market_breadth: Optional[Dict] = None) -> SentimentResult:
        """
        Run VIX sentiment analysis.
        
        Args:
            vix_data: VIX price history
            options_data: Options chain data from DataFetcher
            market_breadth: Market breadth indicators
        
        Returns:
            SentimentResult with score and regime
        """
        if len(vix_data) < 20:
            return SentimentResult(
                sentiment_score=50,
                market_regime="unknown",
                vix_level="unknown",
                buy_signal=False,
                risk_assessment="Insufficient VIX data",
                indicators={}
            )
        
        current_vix = vix_data["Close"].iloc[-1]
        vix_ma20 = vix_data["Close"].tail(20).mean()
        
        # Determine VIX level
        vix_level = self._classify_vix_level(current_vix)
        
        # Calculate VIX percentile (IV rank proxy)
        vix_percentile = self._calculate_vix_percentile(vix_data)
        
        # Check term structure (if we had futures data)
        term_structure = "unknown"  # Would need VIX futures
        
        # Put/call ratio from options data
        pc_ratio = options_data.get("put_call_ratio", 0.5) if options_data else 0.5
        
        # Market breadth trend
        breadth_trend = market_breadth.get("spy_20d_trend", "neutral") if market_breadth else "neutral"
        
        # Determine market regime
        regime = self._determine_regime(current_vix, vix_ma20, breadth_trend)
        
        # Calculate sentiment score
        sentiment_score = self._calculate_sentiment_score(
            current_vix, vix_percentile, pc_ratio, breadth_trend
        )
        
        # Buy signal: Not in panic, VIX reasonable, breadth positive
        buy_signal = (
            current_vix < self.vix_high and
            vix_percentile < self.max_iv_rank and
            sentiment_score >= 60 and
            breadth_trend == "up"
        )
        
        # Risk assessment
        risk_assessment = self._assess_risk(current_vix, regime, sentiment_score)
        
        return SentimentResult(
            sentiment_score=sentiment_score,
            market_regime=regime,
            vix_level=vix_level,
            buy_signal=buy_signal,
            risk_assessment=risk_assessment,
            indicators={
                "vix_current": round(current_vix, 2),
                "vix_ma20": round(vix_ma20, 2),
                "vix_percentile": round(vix_percentile, 1),
                "put_call_ratio": round(pc_ratio, 2),
                "breadth_trend": breadth_trend,
                "term_structure": term_structure
            }
        )
    
    def _classify_vix_level(self, vix: float) -> str:
        """Classify VIX absolute level."""
        if vix < self.vix_low:
            return "low"
        elif vix < self.vix_normal:
            return "normal"
        elif vix < self.vix_high:
            return "elevated"
        elif vix < self.vix_panic:
            return "high"
        else:
            return "panic"
    
    def _calculate_vix_percentile(self, vix_data: pd.DataFrame, lookback: int = 252) -> float:
        """Calculate VIX percentile over lookback period."""
        recent_vix = vix_data["Close"].tail(lookback)
        current = vix_data["Close"].iloc[-1]
        
        return (recent_vix < current).mean() * 100
    
    def _determine_regime(self, current_vix: float, vix_ma20: float, 
                          breadth: str) -> str:
        """Determine overall market regime."""
        # VIX trending up + high level = risk off
        if current_vix > vix_ma20 * 1.1 and current_vix > self.vix_normal:
            if current_vix > self.vix_panic:
                return "panic"
            return "risk_off"
        
        # Low VIX + positive breadth = risk on
        if current_vix < self.vix_normal and breadth == "up":
            return "risk_on"
        
        return "neutral"
    
    def _calculate_sentiment_score(self, vix: float, vix_percentile: float,
                                    pc_ratio: float, breadth: str) -> int:
        """Calculate composite sentiment score 0-100."""
        score = 50  # Neutral base
        
        # VIX level scoring (30 points)
        if vix < self.vix_low:
            score += 20  # Complacent, but not terrible
        elif vix < self.vix_normal:
            score += 30  # Ideal
        elif vix < self.vix_high:
            score += 10  # Caution
        elif vix < self.vix_panic:
            score -= 20  # Elevated fear
        else:
            score -= 40  # Panic
        
        # VIX percentile (20 points)
        # Lower percentile = calmer market = better for buying
        if vix_percentile < 30:
            score += 20
        elif vix_percentile < 50:
            score += 15
        elif vix_percentile < 70:
            score += 5
        elif vix_percentile < 85:
            score -= 10
        else:
            score -= 20
        
        # Put/call ratio (20 points)
        # Very high = fear (contrarian bullish), very low = greed (bearish)
        if 0.7 <= pc_ratio <= 1.2:
            score += 20  # Normal
        elif pc_ratio > 1.5:
            score += 10  # High fear, contrarian signal
        elif pc_ratio < 0.5:
            score -= 20  # Extreme greed
        elif pc_ratio < 0.7:
            score -= 10  # Elevated greed
        
        # Market breadth (30 points)
        if breadth == "up":
            score += 30
        elif breadth == "neutral":
            score += 15
        else:
            score -= 10
        
        return max(0, min(100, score))
    
    def _assess_risk(self, vix: float, regime: str, score: int) -> str:
        """Generate risk assessment."""
        assessments = {
            "panic": "EXTREME RISK - Market panic, avoid new positions",
            "risk_off": "HIGH RISK - Defensive posture recommended",
            "neutral": "MODERATE RISK - Normal caution applies",
            "risk_on": "LOW RISK - Favorable environment for buying"
        }
        
        base = assessments.get(regime, "Unknown risk level")
        
        if score >= 75:
            return f"{base} | Sentiment very favorable"
        elif score >= 60:
            return f"{base} | Sentiment favorable"
        elif score >= 40:
            return f"{base} | Sentiment neutral"
        else:
            return f"{base} | Sentiment unfavorable - wait"
    
    def get_position_sizing_guidance(self, sentiment_score: int) -> Dict:
        """
        Provide position sizing guidance based on sentiment.
        
        Returns dict with:
        - max_position_pct: Max portfolio allocation
        - leverage: Whether leverage is appropriate
        - hedging: Whether to hedge
        """
        if sentiment_score >= 80:
            return {
                "max_position_pct": 0.15,  # 15% max
                "leverage": False,
                "hedging": False,
                "note": "Favorable conditions - full position size"
            }
        elif sentiment_score >= 60:
            return {
                "max_position_pct": 0.10,  # 10% max
                "leverage": False,
                "hedging": False,
                "note": "Good conditions - standard position size"
            }
        elif sentiment_score >= 40:
            return {
                "max_position_pct": 0.05,  # 5% max
                "leverage": False,
                "hedging": True,
                "note": "Caution warranted - reduced size, consider hedges"
            }
        else:
            return {
                "max_position_pct": 0,
                "leverage": False,
                "hedging": True,
                "note": "Unfavorable - avoid new positions"
            }


# CLI interface
if __name__ == "__main__":
    import argparse
    from data_fetcher import DataFetcher
    
    parser = argparse.ArgumentParser(description="VIX Sentiment Analysis")
    parser.add_argument("ticker", help="Stock ticker (for options data)", nargs="?", default="SPY")
    
    args = parser.parse_args()
    
    fetcher = DataFetcher()
    
    # Get VIX data
    vix_data = fetcher.get_vix_data()
    
    # Get options data for the stock
    options_data = fetcher.get_options_data(args.ticker)
    
    # Get market breadth
    breadth = fetcher.get_market_breadth()
    
    analyzer = VIXSentimentAnalyzer()
    result = analyzer.analyze(vix_data, options_data, breadth)
    
    print(f"\n{'='*50}")
    print(f"VIX Sentiment Analysis")
    print(f"{'='*50}")
    print(f"Market Regime: {result.market_regime.upper()}")
    print(f"VIX Level: {result.vix_level.upper()}")
    print(f"Sentiment Score: {result.sentiment_score}/100")
    print(f"Buy Signal: {'YES' if result.buy_signal else 'NO'}")
    print(f"\nRisk Assessment: {result.risk_assessment}")
    print(f"\nIndicators:")
    for k, v in result.indicators.items():
        print(f"  {k}: {v}")
