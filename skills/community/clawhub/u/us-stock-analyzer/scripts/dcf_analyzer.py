"""
DCF (Discounted Cash Flow) Analyzer
Calculates intrinsic value and generates value score.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DCFResult:
    """DCF analysis result container."""
    intrinsic_value: float
    current_price: float
    margin_of_safety: float
    value_score: int  # 0-100
    assumptions: Dict
    buy_signal: bool


class DCFAnalyzer:
    """
    DCF valuation model for stock analysis.
    
    Calculates intrinsic value using discounted free cash flow method.
    Generates a value score (0-100) based on margin of safety and fundamentals.
    """
    
    def __init__(self, 
                 discount_rate: float = 0.10,
                 terminal_growth: float = 0.025,
                 projection_years: int = 10,
                 margin_of_safety_threshold: float = 0.20):
        """
        Args:
            discount_rate: WACC or required rate of return (default 10%)
            terminal_growth: Perpetual growth rate (default 2.5%)
            projection_years: Years to project FCF (default 10)
            margin_of_safety_threshold: Required discount to intrinsic value (default 20%)
        """
        self.discount_rate = discount_rate
        self.terminal_growth = terminal_growth
        self.projection_years = projection_years
        self.mos_threshold = margin_of_safety_threshold
        
    def analyze(self, stock_data: Dict) -> DCFResult:
        """
        Run DCF analysis on stock data.
        
        Args:
            stock_data: Output from DataFetcher.get_stock_data()
        
        Returns:
            DCFResult with valuation and score
        """
        ticker = stock_data["ticker"]
        info = stock_data["info"]
        financials = stock_data.get("financials", {})
        current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
        
        # Extract financial metrics
        fcf = self._extract_fcf(financials, info)
        growth_rate = self._estimate_growth_rate(info, financials)
        shares_outstanding = info.get("sharesOutstanding", 0)
        
        if fcf <= 0 or shares_outstanding <= 0:
            return DCFResult(
                intrinsic_value=0,
                current_price=current_price,
                margin_of_safety=-1,
                value_score=0,
                assumptions={"error": "Insufficient financial data"},
                buy_signal=False
            )
        
        # Calculate DCF
        intrinsic_value_per_share = self._calculate_dcf(
            fcf=fcf,
            growth_rate=growth_rate,
            shares_outstanding=shares_outstanding
        )
        
        # Calculate margin of safety
        if intrinsic_value_per_share > 0:
            margin_of_safety = (intrinsic_value_per_share - current_price) / intrinsic_value_per_share
        else:
            margin_of_safety = -1
        
        # Calculate value score
        value_score = self._calculate_value_score(
            margin_of_safety=margin_of_safety,
            info=info,
            financials=financials
        )
        
        # Buy signal: MOS sufficient AND fundamentals healthy
        buy_signal = (
            margin_of_safety >= self.mos_threshold and 
            value_score >= 60
        )
        
        return DCFResult(
            intrinsic_value=round(intrinsic_value_per_share, 2),
            current_price=round(current_price, 2),
            margin_of_safety=round(margin_of_safety, 3),
            value_score=value_score,
            assumptions={
                "fcf": fcf,
                "growth_rate": growth_rate,
                "discount_rate": self.discount_rate,
                "terminal_growth": self.terminal_growth,
                "projection_years": self.projection_years,
                "shares_outstanding": shares_outstanding
            },
            buy_signal=buy_signal
        )
    
    def _extract_fcf(self, financials: Dict, info: Dict) -> float:
        """Extract free cash flow from financial data."""
        # Try info first
        fcf = info.get("freeCashflow", 0)
        if fcf > 0:
            return fcf
        
        # Try FMP cashflow data
        cf = financials.get("cashflow", [])
        if cf and len(cf) > 0:
            latest = cf[0]
            operating_cf = latest.get("operatingCashFlow", 0)
            capex = latest.get("capitalExpenditure", 0)
            return operating_cf - abs(capex)
        
        # Estimate from net income
        net_income = info.get("netIncomeToCommon", 0)
        return net_income * 0.8  # Rough estimate
    
    def _estimate_growth_rate(self, info: Dict, financials: Dict) -> float:
        """Estimate FCF growth rate from historical data and analyst estimates."""
        # Use analyst estimate if available
        analyst_growth = info.get("earningsGrowth", 0)
        if analyst_growth and analyst_growth > 0:
            return min(analyst_growth, 0.25)  # Cap at 25%
        
        # Calculate from historical FCF
        cf = financials.get("cashflow", [])
        if len(cf) >= 3:
            fcfs = [c.get("freeCashFlow", 0) for c in cf[:3]]
            if all(f > 0 for f in fcfs):
                cagr = (fcfs[0] / fcfs[-1]) ** (1/2) - 1
                return min(max(cagr, 0.02), 0.20)  # Bound between 2-20%
        
        # Default based on sector
        sector = info.get("sector", "").lower()
        growth_defaults = {
            "technology": 0.12,
            "healthcare": 0.10,
            "finance": 0.06,
            "energy": 0.04,
            "utilities": 0.03
        }
        return growth_defaults.get(sector, 0.07)
    
    def _calculate_dcf(self, fcf: float, growth_rate: float, shares_outstanding: float) -> float:
        """Calculate intrinsic value per share using DCF."""
        # Project FCF
        projected_fcfs = []
        current_fcf = fcf
        
        for year in range(1, self.projection_years + 1):
            if year <= 5:
                # Higher growth in first 5 years
                current_fcf *= (1 + growth_rate)
            else:
                # Gradual decline to terminal growth
                decayed_growth = growth_rate * (1 - (year - 5) / (self.projection_years - 5))
                decayed_growth = max(decayed_growth, self.terminal_growth)
                current_fcf *= (1 + decayed_growth)
            
            projected_fcfs.append(current_fcf)
        
        # Discount to present value
        present_values = [
            fcf / ((1 + self.discount_rate) ** (i + 1))
            for i, fcf in enumerate(projected_fcfs)
        ]
        
        # Terminal value
        terminal_fcf = projected_fcfs[-1] * (1 + self.terminal_growth)
        terminal_value = terminal_fcf / (self.discount_rate - self.terminal_growth)
        terminal_pv = terminal_value / ((1 + self.discount_rate) ** self.projection_years)
        
        # Total enterprise value
        enterprise_value = sum(present_values) + terminal_pv
        
        # Equity value (simplified - assumes cash/debt roughly balance)
        equity_value = enterprise_value
        
        return equity_value / shares_outstanding if shares_outstanding > 0 else 0
    
    def _calculate_value_score(self, margin_of_safety: float, info: Dict, financials: Dict) -> int:
        """Calculate composite value score 0-100."""
        score = 0
        
        # Margin of safety component (40 points max)
        if margin_of_safety > 0.30:
            score += 40
        elif margin_of_safety > 0.20:
            score += 30
        elif margin_of_safety > 0.10:
            score += 20
        elif margin_of_safety > 0:
            score += 10
        
        # Financial health (30 points max)
        roe = info.get("returnOnEquity", 0)
        if roe > 0.15:
            score += 15
        elif roe > 0.10:
            score += 10
        elif roe > 0.05:
            score += 5
        
        debt_to_equity = info.get("debtToEquity", 0)
        if debt_to_equity < 50:
            score += 15
        elif debt_to_equity < 100:
            score += 10
        elif debt_to_equity < 200:
            score += 5
        
        # Profitability (20 points max)
        profit_margin = info.get("profitMargins", 0)
        if profit_margin > 0.20:
            score += 20
        elif profit_margin > 0.10:
            score += 15
        elif profit_margin > 0.05:
            score += 10
        elif profit_margin > 0:
            score += 5
        
        # Consistency (10 points max)
        pe = info.get("trailingPE", 100)
        if pe < 15:
            score += 10
        elif pe < 25:
            score += 5
        
        return min(score, 100)


# CLI interface
if __name__ == "__main__":
    import json
    import argparse
    from data_fetcher import DataFetcher
    
    parser = argparse.ArgumentParser(description="DCF Analysis")
    parser.add_argument("ticker", help="Stock ticker")
    parser.add_argument("--discount-rate", type=float, default=0.10)
    parser.add_argument("--mos", type=float, default=0.20)
    
    args = parser.parse_args()
    
    fetcher = DataFetcher()
    data = fetcher.get_stock_data(args.ticker)
    
    analyzer = DCFAnalyzer(
        discount_rate=args.discount_rate,
        margin_of_safety_threshold=args.mos
    )
    result = analyzer.analyze(data)
    
    print(f"\n{'='*50}")
    print(f"DCF Analysis: {args.ticker}")
    print(f"{'='*50}")
    print(f"Current Price: ${result.current_price:.2f}")
    print(f"Intrinsic Value: ${result.intrinsic_value:.2f}")
    print(f"Margin of Safety: {result.margin_of_safety*100:.1f}%")
    print(f"Value Score: {result.value_score}/100")
    print(f"Buy Signal: {'YES' if result.buy_signal else 'NO'}")
    print(f"\nAssumptions:")
    for k, v in result.assumptions.items():
        print(f"  {k}: {v}")
