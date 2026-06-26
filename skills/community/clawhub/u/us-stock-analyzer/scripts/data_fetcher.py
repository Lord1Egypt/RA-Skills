"""
US Stock Data Fetcher
Fetches market data from Yahoo Finance, FMP, and other sources.
"""

import os
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple


class DataFetcher:
    """Unified data fetcher for US stock analysis."""
    
    def __init__(self, fmp_api_key: Optional[str] = None):
        self.fmp_key = fmp_api_key or os.getenv("FMP_API_KEY")
        self.fmp_base = "https://financialmodelingprep.com/api/v3"
        
    def get_stock_data(self, ticker: str, period: str = "1y") -> Dict:
        """
        Fetch comprehensive stock data.
        
        Returns dict with:
        - price_history: DataFrame with OHLCV
        - info: Company fundamentals
        - financials: Income statement, balance sheet, cash flow
        """
        yf_ticker = yf.Ticker(ticker)
        
        # Price data
        hist = yf_ticker.history(period=period)
        
        # Company info
        info = yf_ticker.info
        
        # Financial statements from FMP (if available)
        financials = {}
        if self.fmp_key:
            financials = self._fetch_fmp_financials(ticker)
        
        return {
            "ticker": ticker,
            "price_history": hist,
            "info": info,
            "financials": financials,
            "last_updated": datetime.now()
        }
    
    def get_vix_data(self, period: str = "6mo") -> pd.DataFrame:
        """Fetch VIX index data."""
        vix = yf.Ticker("^VIX")
        return vix.history(period=period)
    
    def get_sector_etf(self, sector: str, period: str = "1y") -> pd.DataFrame:
        """
        Fetch sector ETF data.
        Common sectors: technology, finance, healthcare, energy, consumer
        """
        sector_map = {
            "technology": "XLK",
            "finance": "XLF",
            "healthcare": "XLV",
            "energy": "XLE",
            "consumer": "XLY",
            "industrial": "XLI",
            "materials": "XLB",
            "utilities": "XLU",
            "realestate": "XLRE"
        }
        etf = sector_map.get(sector.lower(), "SPY")
        return yf.Ticker(etf).history(period=period)
    
    def get_options_data(self, ticker: str) -> Dict:
        """
        Fetch options chain data for IV calculation.
        Returns put/call ratio and implied volatility metrics.
        """
        try:
            stock = yf.Ticker(ticker)
            expirations = stock.options
            
            if not expirations:
                return {"error": "No options data available"}
            
            # Get nearest expiration
            opt = stock.option_chain(expirations[0])
            calls = opt.calls
            puts = opt.puts
            
            # Calculate metrics
            call_vol = calls['volume'].sum() if 'volume' in calls else 0
            put_vol = puts['volume'].sum() if 'volume' in puts else 0
            
            pc_ratio = put_vol / call_vol if call_vol > 0 else 0
            
            # Average implied volatility
            avg_iv = pd.concat([calls['impliedVolatility'], puts['impliedVolatility']]).mean()
            
            return {
                "put_call_ratio": pc_ratio,
                "avg_implied_vol": avg_iv,
                "expiration": expirations[0]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _fetch_fmp_financials(self, ticker: str) -> Dict:
        """Fetch financial statements from FMP API."""
        if not self.fmp_key:
            return {}
        
        endpoints = {
            "income": f"{self.fmp_base}/income-statement/{ticker}",
            "balance": f"{self.fmp_base}/balance-sheet-statement/{ticker}",
            "cashflow": f"{self.fmp_base}/cash-flow-statement/{ticker}",
            "ratios": f"{self.fmp_base}/ratios-ttm/{ticker}"
        }
        
        results = {}
        for name, url in endpoints.items():
            try:
                resp = requests.get(f"{url}?apikey={self.fmp_key}", timeout=30)
                resp.raise_for_status()
                results[name] = resp.json()
            except Exception as e:
                results[name] = {"error": str(e)}
        
        return results
    
    def get_market_breadth(self) -> Dict:
        """
        Get market breadth indicators.
        NYSE advance/decline data if available.
        """
        # Using SPY as proxy for market breadth
        spy = yf.Ticker("SPY").history(period="1mo")
        
        return {
            "spy_20d_trend": "up" if spy['Close'][-1] > spy['Close'].mean() else "down",
            "spy_current_price": spy['Close'][-1],
            "spy_volume_vs_avg": spy['Volume'][-5:].mean() / spy['Volume'].mean()
        }


# CLI interface
if __name__ == "__main__":
    import json
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch stock data")
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--fmp-key", help="FMP API key", default=os.getenv("FMP_API_KEY"))
    parser.add_argument("--output", "-o", help="Output JSON file")
    
    args = parser.parse_args()
    
    fetcher = DataFetcher(fmp_api_key=args.fmp_key)
    data = fetcher.get_stock_data(args.ticker)
    
    # Convert DataFrame to dict for JSON serialization
    output = {
        "ticker": data["ticker"],
        "price_history": data["price_history"].tail(30).to_dict(),
        "info": {k: v for k, v in data["info"].items() if isinstance(v, (str, int, float, bool))},
        "last_updated": data["last_updated"].isoformat()
    }
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(output, f, indent=2, default=str)
        print(f"Data saved to {args.output}")
    else:
        print(json.dumps(output, indent=2, default=str))
