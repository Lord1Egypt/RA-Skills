"""
Livermore Trend Analyzer
Implements Jesse Livermore's trading rules for trend identification.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TrendResult:
    """Trend analysis result container."""
    trend_score: int  # 0-100
    trend_direction: str  # "up", "down", "sideways"
    key_levels: Dict
    buy_signal: bool
    position_advice: str
    analysis_details: Dict


class LivermoreAnalyzer:
    """
    Implements Jesse Livermore's key trading principles:
    1. Trade in direction of the trend (line of least resistance)
    2. Let profits run, cut losses quickly
    3. Wait for confirmation (price + volume)
    4. Key pivotal points for entries
    5. Trade leading stocks in leading sectors
    """
    
    def __init__(self,
                 pivot_lookback: int = 20,
                 volume_confirm_ratio: float = 1.5,
                 ma_short: int = 20,
                 ma_long: int = 60):
        self.pivot_lookback = pivot_lookback
        self.volume_confirm = volume_confirm_ratio
        self.ma_short = ma_short
        self.ma_long = ma_long
    
    def analyze(self, stock_data: Dict, sector_data: Optional[pd.DataFrame] = None) -> TrendResult:
        """
        Run Livermore trend analysis.
        
        Args:
            stock_data: Output from DataFetcher
            sector_data: Sector ETF price history (optional)
        
        Returns:
            TrendResult with scores and signals
        """
        df = stock_data["price_history"].copy()
        info = stock_data["info"]
        
        if len(df) < self.ma_long:
            return TrendResult(
                trend_score=0,
                trend_direction="unknown",
                key_levels={},
                buy_signal=False,
                position_advice="Insufficient data",
                analysis_details={"error": "Need at least 60 days of data"}
            )
        
        # Calculate indicators
        df = self._calculate_indicators(df)
        
        # Identify key levels
        key_levels = self._identify_key_levels(df)
        
        # Check trend direction
        trend_direction = self._determine_trend(df)
        
        # Check for pivot point break
        pivot_break = self._check_pivot_break(df, key_levels)
        
        # Volume confirmation
        volume_confirm = self._check_volume_confirmation(df)
        
        # Sector alignment
        sector_aligned = self._check_sector_alignment(sector_data) if sector_data is not None else True
        
        # Calculate trend score
        trend_score = self._calculate_trend_score(
            df, trend_direction, pivot_break, volume_confirm, sector_aligned
        )
        
        # Buy signal: Uptrend + pivot break + volume + sector aligned
        buy_signal = (
            trend_direction == "up" and
            pivot_break and
            volume_confirm and
            sector_aligned and
            trend_score >= 60
        )
        
        # Position advice
        position_advice = self._get_position_advice(df, key_levels, buy_signal)
        
        return TrendResult(
            trend_score=trend_score,
            trend_direction=trend_direction,
            key_levels=key_levels,
            buy_signal=buy_signal,
            position_advice=position_advice,
            analysis_details={
                "ma_short": df[f"MA{self.ma_short}"].iloc[-1],
                "ma_long": df[f"MA{self.ma_long}"].iloc[-1],
                "pivot_high_break": pivot_break,
                "volume_confirmed": volume_confirm,
                "sector_aligned": sector_aligned,
                "atr": df["ATR"].iloc[-1] if "ATR" in df.columns else None
            }
        )
    
    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators."""
        # Moving averages
        df[f"MA{self.ma_short}"] = df["Close"].rolling(window=self.ma_short).mean()
        df[f"MA{self.ma_long}"] = df["Close"].rolling(window=self.ma_long).mean()
        
        # Volume moving average
        df["Vol_MA20"] = df["Volume"].rolling(window=20).mean()
        
        # ATR for position sizing
        high_low = df["High"] - df["Low"]
        high_close = np.abs(df["High"] - df["Close"].shift())
        low_close = np.abs(df["Low"] - df["Close"].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df["ATR"] = true_range.rolling(window=14).mean()
        
        return df
    
    def _identify_key_levels(self, df: pd.DataFrame) -> Dict:
        """Identify pivotal support/resistance levels."""
        recent = df.tail(self.pivot_lookback * 3)
        
        # Pivot highs (resistance)
        pivot_highs = []
        for i in range(self.pivot_lookback, len(recent) - self.pivot_lookback):
            window = recent.iloc[i-self.pivot_lookback:i+self.pivot_lookback+1]
            if recent["High"].iloc[i] == window["High"].max():
                pivot_highs.append(recent["High"].iloc[i])
        
        # Pivot lows (support)
        pivot_lows = []
        for i in range(self.pivot_lookback, len(recent) - self.pivot_lookback):
            window = recent.iloc[i-self.pivot_lookback:i+self.pivot_lookback+1]
            if recent["Low"].iloc[i] == window["Low"].min():
                pivot_lows.append(recent["Low"].iloc[i])
        
        current_price = df["Close"].iloc[-1]
        
        # Find nearest levels
        resistance_above = [p for p in pivot_highs if p > current_price * 1.02]
        support_below = [p for p in pivot_lows if p < current_price * 0.98]
        
        return {
            "current_price": round(current_price, 2),
            "nearest_resistance": round(min(resistance_above), 2) if resistance_above else None,
            "nearest_support": round(max(support_below), 2) if support_below else None,
            "pivot_high_20d": round(df["High"].tail(20).max(), 2),
            "pivot_low_20d": round(df["Low"].tail(20).min(), 2),
            "all_resistances": sorted(set([round(p, 2) for p in pivot_highs[-5:]])),
            "all_supports": sorted(set([round(p, 2) for p in pivot_lows[-5:]]))
        }
    
    def _determine_trend(self, df: pd.DataFrame) -> str:
        """Determine trend direction using multiple timeframes."""
        ma20 = df[f"MA{self.ma_short}"].iloc[-1]
        ma60 = df[f"MA{self.ma_long}"].iloc[-1]
        price = df["Close"].iloc[-1]
        
        # Price vs MAs
        above_ma20 = price > ma20
        above_ma60 = price > ma60
        ma20_above_ma60 = ma20 > ma60
        
        # Trend strength
        if above_ma20 and above_ma60 and ma20_above_ma60:
            return "up"
        elif not above_ma20 and not above_ma60 and not ma20_above_ma60:
            return "down"
        else:
            return "sideways"
    
    def _check_pivot_break(self, df: pd.DataFrame, key_levels: Dict) -> bool:
        """Check if price has broken above recent pivot high."""
        recent_high = key_levels["pivot_high_20d"]
        current_price = df["Close"].iloc[-1]
        prev_price = df["Close"].iloc[-2]
        
        # Breakout: price crossed above recent high
        return current_price > recent_high * 0.99 and prev_price <= recent_high
    
    def _check_volume_confirmation(self, df: pd.DataFrame) -> bool:
        """Check if volume confirms the move."""
        recent_volume = df["Volume"].tail(5).mean()
        avg_volume = df["Vol_MA20"].iloc[-1]
        
        return recent_volume > avg_volume * self.volume_confirm
    
    def _check_sector_alignment(self, sector_data: Optional[pd.DataFrame]) -> bool:
        """Check if sector ETF is in uptrend."""
        if sector_data is None or len(sector_data) < 60:
            return True  # Assume aligned if no data
        
        sector_ma20 = sector_data["Close"].tail(20).mean()
        sector_ma60 = sector_data["Close"].tail(60).mean()
        sector_price = sector_data["Close"].iloc[-1]
        
        return sector_price > sector_ma20 and sector_ma20 > sector_ma60
    
    def _calculate_trend_score(self, df: pd.DataFrame, trend: str, 
                               pivot_break: bool, volume_confirm: bool,
                               sector_aligned: bool) -> int:
        """Calculate composite trend score 0-100."""
        score = 0
        
        # Trend direction (40 points)
        if trend == "up":
            score += 40
        elif trend == "sideways":
            score += 20
        
        # Moving average alignment (20 points)
        ma20 = df[f"MA{self.ma_short}"].iloc[-1]
        ma60 = df[f"MA{self.ma_long}"].iloc[-1]
        price = df["Close"].iloc[-1]
        
        if price > ma20 > ma60:
            score += 20
        elif price > ma60:
            score += 10
        
        # Pivot break (15 points)
        if pivot_break:
            score += 15
        
        # Volume confirmation (15 points)
        if volume_confirm:
            score += 15
        
        # Sector alignment (10 points)
        if sector_aligned:
            score += 10
        
        return score
    
    def _get_position_advice(self, df: pd.DataFrame, key_levels: Dict, buy_signal: bool) -> str:
        """Generate position sizing advice based on setup quality."""
        if not buy_signal:
            return "No position - wait for trend confirmation"
        
        atr = df["ATR"].iloc[-1] if "ATR" in df.columns else df["Close"].iloc[-1] * 0.02
        current_price = df["Close"].iloc[-1]
        
        # Calculate pyramid entry levels (Livermore method)
        if key_levels["nearest_support"]:
            stop_loss = key_levels["nearest_support"] - atr
        else:
            stop_loss = current_price - 2 * atr
        
        risk_per_share = current_price - stop_loss
        risk_pct = 0.02  # 2% risk per trade
        
        return (
            f"Initial position: Enter 1/3 size at ${current_price:.2f}\n"
            f"Add on pullback to ${current_price - atr:.2f} (1/3 more)\n"
            f"Final add at ${current_price + atr:.2f} breakout (1/3 more)\n"
            f"Stop loss: ${stop_loss:.2f} ({risk_per_share/current_price*100:.1f}% risk)"
        )


# CLI interface
if __name__ == "__main__":
    import argparse
    from data_fetcher import DataFetcher
    
    parser = argparse.ArgumentParser(description="Livermore Trend Analysis")
    parser.add_argument("ticker", help="Stock ticker")
    parser.add_argument("--sector", help="Sector ETF ticker (e.g., XLK)")
    
    args = parser.parse_args()
    
    fetcher = DataFetcher()
    stock_data = fetcher.get_stock_data(args.ticker)
    
    sector_data = None
    if args.sector:
        sector_data = fetcher.get_sector_etf(args.sector)
    
    analyzer = LivermoreAnalyzer()
    result = analyzer.analyze(stock_data, sector_data)
    
    print(f"\n{'='*50}")
    print(f"Livermore Trend Analysis: {args.ticker}")
    print(f"{'='*50}")
    print(f"Trend: {result.trend_direction.upper()}")
    print(f"Trend Score: {result.trend_score}/100")
    print(f"Buy Signal: {'YES' if result.buy_signal else 'NO'}")
    print(f"\nKey Levels:")
    for k, v in result.key_levels.items():
        print(f"  {k}: {v}")
    print(f"\nPosition Advice:\n{result.position_advice}")
