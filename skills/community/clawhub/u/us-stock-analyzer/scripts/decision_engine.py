"""
Three-Factor Decision Engine
Combines DCF, Trend, and Sentiment analysis to generate buy signals.
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime

from data_fetcher import DataFetcher
from dcf_analyzer import DCFAnalyzer, DCFResult
from trend_analyzer import LivermoreAnalyzer, TrendResult
from sentiment_analyzer import VIXSentimentAnalyzer, SentimentResult


@dataclass
class AnalysisResult:
    """Complete analysis result."""
    ticker: str
    analysis_date: str
    
    # Factor scores
    value_score: int
    trend_score: int
    sentiment_score: int
    composite_score: float
    
    # Individual results
    dcf_result: DCFResult
    trend_result: TrendResult
    sentiment_result: SentimentResult
    
    # Decision
    buy_signal: bool
    confidence: str  # "high", "medium", "low"
    
    # Recommendations
    position_size_pct: float
    target_price: Optional[float]
    stop_loss: Optional[float]
    time_horizon: str
    
    # Report
    report: str


class StockAnalyzer:
    """
    Unified stock analyzer combining three factors:
    - Value (DCF): 40% weight
    - Trend (Livermore): 35% weight  
    - Sentiment (VIX): 25% weight
    
    Buy signal requires:
    - All three scores >= 60
    - Composite score >= 70
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Args:
            config_path: Path to config.yaml with API keys and thresholds
        """
        self.config = self._load_config(config_path)
        self.fetcher = DataFetcher(fmp_api_key=self.config.get("fmp_api_key"))
        
        # Initialize analyzers with config
        self.dcf_analyzer = DCFAnalyzer(
            discount_rate=self.config.get("dcf_discount_rate", 0.10),
            margin_of_safety_threshold=self.config.get("margin_of_safety", 0.20)
        )
        
        self.trend_analyzer = LivermoreAnalyzer(
            pivot_lookback=self.config.get("pivot_lookback", 20)
        )
        
        self.sentiment_analyzer = VIXSentimentAnalyzer(
            vix_high_threshold=self.config.get("vix_high", 25)
        )
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from YAML or use defaults."""
        defaults = {
            "dcf_discount_rate": 0.10,
            "terminal_growth": 0.025,
            "margin_of_safety": 0.20,
            "pivot_lookback": 20,
            "vix_low": 15,
            "vix_normal": 20,
            "vix_high": 25,
            "vix_panic": 30,
            "value_weight": 0.40,
            "trend_weight": 0.35,
            "sentiment_weight": 0.25,
            "min_score_threshold": 60,
            "composite_threshold": 70
        }
        
        if config_path and os.path.exists(config_path):
            import yaml
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                defaults.update(user_config)
        
        # Also check environment variables
        defaults["fmp_api_key"] = os.getenv("FMP_API_KEY", defaults.get("fmp_api_key"))
        
        return defaults
    
    def analyze(self, ticker: str, use_sector: bool = True) -> Dict:
        """
        Run complete three-factor analysis.
        
        Args:
            ticker: Stock symbol
            use_sector: Whether to fetch and analyze sector ETF
        
        Returns:
            Dict with complete analysis and report
        """
        print(f"\n🔍 Analyzing {ticker}...")
        
        # Fetch data
        stock_data = self.fetcher.get_stock_data(ticker)
        
        # Determine sector
        sector = stock_data["info"].get("sector", "").lower()
        
        # Fetch sector data if requested
        sector_data = None
        if use_sector and sector:
            try:
                sector_data = self.fetcher.get_sector_etf(sector)
            except:
                pass
        
        # Run three-factor analysis
        print("  📊 Running DCF valuation...")
        dcf_result = self.dcf_analyzer.analyze(stock_data)
        
        print("  📈 Analyzing trend...")
        trend_result = self.trend_analyzer.analyze(stock_data, sector_data)
        
        print("  🎭 Assessing market sentiment...")
        vix_data = self.fetcher.get_vix_data()
        options_data = self.fetcher.get_options_data(ticker)
        breadth = self.fetcher.get_market_breadth()
        sentiment_result = self.sentiment_analyzer.analyze(vix_data, options_data, breadth)
        
        # Calculate composite score
        weights = (
            self.config["value_weight"],
            self.config["trend_weight"],
            self.config["sentiment_weight"]
        )
        
        composite_score = (
            dcf_result.value_score * weights[0] +
            trend_result.trend_score * weights[1] +
            sentiment_result.sentiment_score * weights[2]
        )
        
        # Determine buy signal
        min_threshold = self.config["min_score_threshold"]
        composite_threshold = self.config["composite_threshold"]
        
        all_factors_pass = (
            dcf_result.value_score >= min_threshold and
            trend_result.trend_score >= min_threshold and
            sentiment_result.sentiment_score >= min_threshold
        )
        
        buy_signal = all_factors_pass and composite_score >= composite_threshold
        
        # Determine confidence
        if composite_score >= 80 and all_factors_pass:
            confidence = "high"
        elif composite_score >= 70:
            confidence = "medium"
        else:
            confidence = "low"
        
        # Calculate position sizing
        position_size = self._calculate_position_size(
            composite_score, confidence, sentiment_result.market_regime
        )
        
        # Calculate target and stop
        target_price = self._calculate_target(dcf_result, trend_result)
        stop_loss = self._calculate_stop_loss(trend_result)
        
        # Generate report
        report = self._generate_report(
            ticker=ticker,
            stock_data=stock_data,
            dcf=dcf_result,
            trend=trend_result,
            sentiment=sentiment_result,
            composite=composite_score,
            buy_signal=buy_signal,
            confidence=confidence,
            position_size=position_size
        )
        
        result = AnalysisResult(
            ticker=ticker,
            analysis_date=datetime.now().isoformat(),
            value_score=dcf_result.value_score,
            trend_score=trend_result.trend_score,
            sentiment_score=sentiment_result.sentiment_score,
            composite_score=round(composite_score, 1),
            dcf_result=dcf_result,
            trend_result=trend_result,
            sentiment_result=sentiment_result,
            buy_signal=buy_signal,
            confidence=confidence,
            position_size_pct=position_size,
            target_price=target_price,
            stop_loss=stop_loss,
            time_horizon="medium" if buy_signal else "N/A",
            report=report
        )
        
        return {
            "result": result,
            "report": report,
            "data": {
                "stock": stock_data,
                "sector": sector_data
            }
        }
    
    def _calculate_position_size(self, composite_score: float, confidence: str, 
                                  regime: str) -> float:
        """Calculate recommended position size as % of portfolio."""
        base_sizes = {
            "high": 0.10,
            "medium": 0.07,
            "low": 0.03
        }
        
        size = base_sizes.get(confidence, 0.03)
        
        # Adjust for market regime
        if regime == "panic":
            size *= 0
        elif regime == "risk_off":
            size *= 0.5
        elif regime == "risk_on":
            size *= 1.2
        
        # Cap at 15%
        return min(size, 0.15)
    
    def _calculate_target(self, dcf: DCFResult, trend: TrendResult) -> Optional[float]:
        """Calculate price target from DCF and trend levels."""
        targets = []
        
        if dcf.intrinsic_value > 0:
            targets.append(dcf.intrinsic_value)
        
        if trend.key_levels.get("nearest_resistance"):
            targets.append(trend.key_levels["nearest_resistance"])
        
        if targets:
            return round(sum(targets) / len(targets), 2)
        return None
    
    def _calculate_stop_loss(self, trend: TrendResult) -> Optional[float]:
        """Calculate stop loss from support levels."""
        if trend.key_levels.get("nearest_support"):
            # 2% below support
            return round(trend.key_levels["nearest_support"] * 0.98, 2)
        return None
    
    def _generate_report(self, ticker: str, stock_data: Dict, 
                         dcf: DCFResult, trend: TrendResult, 
                         sentiment: SentimentResult, composite: float,
                         buy_signal: bool, confidence: str,
                         position_size: float) -> str:
        """Generate formatted analysis report."""
        
        info = stock_data["info"]
        company_name = info.get("longName", ticker)
        current_price = dcf.current_price
        
        # Signal emoji
        signal_emoji = "🔥 BUY" if buy_signal else "❌ NO SIGNAL"
        
        # Score bars
        def score_bar(score: int) -> str:
            filled = int(score / 10)
            return "█" * filled + "░" * (10 - filled)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║  THREE-FACTOR STOCK ANALYSIS                                     ║
╠══════════════════════════════════════════════════════════════════╣
║  {company_name[:50]:<50} ║
║  Ticker: {ticker:<8}  Date: {datetime.now().strftime('%Y-%m-%d'):<29} ║
╚══════════════════════════════════════════════════════════════════╝

💰 CURRENT PRICE: ${current_price:.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 FACTOR ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Value (DCF)        [{score_bar(dcf.value_score)}] {dcf.value_score:>3}/100
  • Intrinsic Value: ${dcf.intrinsic_value:.2f}
  • Margin of Safety: {dcf.margin_of_safety*100:+.1f}%
  • Signal: {'✅ BUY' if dcf.buy_signal else '❌ HOLD'}

Trend (Livermore)  [{score_bar(trend.trend_score)}] {trend.trend_score:>3}/100
  • Direction: {trend.trend_direction.upper()}
  • Key Resistance: ${trend.key_levels.get('nearest_resistance', 'N/A')}
  • Key Support: ${trend.key_levels.get('nearest_support', 'N/A')}
  • Signal: {'✅ BUY' if trend.buy_signal else '❌ HOLD'}

Sentiment (VIX)    [{score_bar(sentiment.sentiment_score)}] {sentiment.sentiment_score:>3}/100
  • Regime: {sentiment.market_regime.upper()}
  • VIX Level: {sentiment.vix_level.upper()} ({sentiment.indicators.get('vix_current', 'N/A')})
  • Signal: {'✅ BUY' if sentiment.buy_signal else '❌ HOLD'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 COMPOSITE DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Composite Score: {composite:.1f}/100  [Confidence: {confidence.upper()}]

{signal_emoji}

Position Size: {position_size*100:.1f}% of portfolio
"""
        
        if buy_signal:
            target = self._calculate_target(dcf, trend)
            stop = self._calculate_stop_loss(trend)
            
            if target and stop:
                upside = (target - current_price) / current_price * 100
                downside = (stop - current_price) / current_price * 100
                rr_ratio = abs(upside / downside) if downside != 0 else 0
                
                report += f"""
Target Price:  ${target:.2f} (+{upside:.1f}%)
Stop Loss:     ${stop:.2f} ({downside:+.1f}%)
R/R Ratio:     {rr_ratio:.1f}:1

{trend.position_advice}
"""
        else:
            report += f"""
❌ Entry Conditions Not Met:
"""
            if dcf.value_score < 60:
                report += f"   • Value score too low ({dcf.value_score}/100)\n"
            if trend.trend_score < 60:
                report += f"   • Trend score too low ({trend.trend_score}/100)\n"
            if sentiment.sentiment_score < 60:
                report += f"   • Sentiment score too low ({sentiment.sentiment_score}/100)\n"
            if composite < 70:
                report += f"   • Composite score below threshold ({composite:.1f}/70)\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  RISK ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{sentiment.risk_assessment}

Disclaimer: This analysis is for informational purposes only and 
does not constitute investment advice. Always do your own research.
"""
        
        return report
    
    def plot_analysis(self, result: AnalysisResult, save_path: Optional[str] = None):
        """Generate visualization of analysis."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f"{result.ticker} - Three-Factor Analysis", fontsize=14, fontweight='bold')
        
        # Factor scores radar/bar
        ax1 = axes[0, 0]
        factors = ['Value\n(DCF)', 'Trend\n(Livermore)', 'Sentiment\n(VIX)', 'Composite']
        scores = [result.value_score, result.trend_score, 
                  result.sentiment_score, result.composite_score]
        colors = ['green' if s >= 60 else 'orange' if s >= 40 else 'red' for s in scores]
        bars = ax1.bar(factors, scores, color=colors, alpha=0.7)
        ax1.axhline(y=60, color='r', linestyle='--', label='Threshold')
        ax1.set_ylim(0, 100)
        ax1.set_ylabel('Score')
        ax1.set_title('Factor Scores')
        ax1.legend()
        
        # Add score labels on bars
        for bar, score in zip(bars, scores):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                    f'{score:.0f}', ha='center', va='bottom', fontweight='bold')
        
        # Price chart with key levels
        ax2 = axes[0, 1]
        # Placeholder - would need price data passed in
        ax2.text(0.5, 0.5, 'Price Chart\n(Integration with data_fetcher required)',
                ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title('Price Action with Key Levels')
        
        # DCF breakdown
        ax3 = axes[1, 0]
        dcf = result.dcf_result
        labels = ['Current Price', 'Intrinsic Value']
        values = [dcf.current_price, dcf.intrinsic_value]
        colors = ['red', 'green']
        bars = ax3.bar(labels, values, color=colors, alpha=0.7)
        ax3.set_title(f'DCF Valuation (MoS: {dcf.margin_of_safety*100:+.1f}%)')
        ax3.set_ylabel('Price ($)')
        
        # Sentiment indicators
        ax4 = axes[1, 1]
        sentiment = result.sentiment_result
        indicators = sentiment.indicators
        ax4.text(0.1, 0.8, f"VIX: {indicators.get('vix_current', 'N/A')}", 
                transform=ax4.transAxes, fontsize=12)
        ax4.text(0.1, 0.6, f"VIX Percentile: {indicators.get('vix_percentile', 'N/A')}%",
                transform=ax4.transAxes, fontsize=12)
        ax4.text(0.1, 0.4, f"P/C Ratio: {indicators.get('put_call_ratio', 'N/A')}",
                transform=ax4.transAxes, fontsize=12)
        ax4.text(0.1, 0.2, f"Regime: {sentiment.market_regime.upper()}",
                transform=ax4.transAxes, fontsize=12, fontweight='bold')
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1)
        ax4.axis('off')
        ax4.set_title('Sentiment Indicators')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
        
        plt.close()


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Three-Factor Stock Analysis")
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--config", "-c", help="Path to config.yaml")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--chart", help="Save chart to file")
    
    args = parser.parse_args()
    
    analyzer = StockAnalyzer(config_path=args.config)
    result = analyzer.analyze(args.ticker)
    
    # Print report
    print(result["report"])
    
    # Save JSON if requested
    if args.output:
        result_dict = asdict(result["result"])
        with open(args.output, 'w') as f:
            json.dump(result_dict, f, indent=2, default=str)
        print(f"\nResults saved to {args.output}")
    
    # Generate chart if requested
    if args.chart:
        analyzer.plot_analysis(result["result"], save_path=args.chart)
