"""
Stock Market Analyzer - A-share stock analysis toolkit
Author: ClawHub Skill
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Union, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def query_realtime_price(ticker: str, time: str = None, file_path: str = None) -> Dict:
    """
    Query real-time price data for A-share stocks.
    
    Args:
        ticker: Stock code (e.g., "600519.SH" or "000001.SZ")
        time: Query time in format "YYYY-MM-DD HH:MM:SS" (optional)
        file_path: Path to save CSV data (optional)
    
    Returns:
        Dictionary containing price data
    """
    try:
        from kimi_finance import kimi_finance
        
        if time is None:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%00")
        
        if file_path is None:
            file_path = f"/tmp/{ticker.replace('.', '_')}_realtime.csv"
        
        result = kimi_finance(
            ticker=ticker,
            time=time,
            type="realtime_price",
            file_path=file_path
        )
        
        # Read the CSV file and return as dict
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if not df.empty:
                return df.to_dict('records')[0]
        
        return {"status": "success", "ticker": ticker, "time": time}
    except Exception as e:
        return {"error": str(e), "ticker": ticker}


def query_technical_indicators(ticker: str, time: str = None, file_path: str = None) -> Dict:
    """
    Query technical indicators for A-share stocks.
    
    Args:
        ticker: Stock code (e.g., "600519.SH" or "000001.SZ")
        time: Query time in format "YYYY-MM-DD HH:MM:SS" (optional)
        file_path: Path to save CSV data (optional)
    
    Returns:
        Dictionary containing technical indicators
    """
    try:
        from kimi_finance import kimi_finance
        
        if time is None:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%00")
        
        if file_path is None:
            file_path = f"/tmp/{ticker.replace('.', '_')}_tech.csv"
        
        result = kimi_finance(
            ticker=ticker,
            time=time,
            type="realtime_tech",
            file_path=file_path
        )
        
        # Read the CSV file and return as dict
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if not df.empty:
                return df.to_dict('records')[0]
        
        return {"status": "success", "ticker": ticker, "time": time}
    except Exception as e:
        return {"error": str(e), "ticker": ticker}


def query_open_summary(ticker: str, time: str = None, file_path: str = None) -> Dict:
    """
    Query opening summary data for A-share stocks.
    
    Args:
        ticker: Stock code (e.g., "600519.SH" or "000001.SZ")
        time: Query time in format "YYYY-MM-DD HH:MM:SS" (optional)
        file_path: Path to save CSV data (optional)
    
    Returns:
        Dictionary containing opening summary data
    """
    try:
        from kimi_finance import kimi_finance
        
        if time is None:
            time = datetime.now().strftime("%Y-%m-%d 09:30:00")
        
        if file_path is None:
            file_path = f"/tmp/{ticker.replace('.', '_')}_open.csv"
        
        result = kimi_finance(
            ticker=ticker,
            time=time,
            type="open_summary",
            file_path=file_path
        )
        
        # Read the CSV file and return as dict
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if not df.empty:
                return df.to_dict('records')[0]
        
        return {"status": "success", "ticker": ticker, "time": time}
    except Exception as e:
        return {"error": str(e), "ticker": ticker}


def query_close_summary(ticker: str, time: str = None, file_path: str = None) -> Dict:
    """
    Query closing summary data for A-share stocks.
    
    Args:
        ticker: Stock code(s), comma-separated, max 3 (e.g., "000001.SZ,600519.SH")
        time: Query time in format "YYYY-MM-DD HH:MM:SS" (optional)
        file_path: Path to save CSV data (optional)
    
    Returns:
        Dictionary containing closing summary data
    """
    try:
        from kimi_finance import kimi_finance
        
        if time is None:
            time = datetime.now().strftime("%Y-%m-%d 15:00:00")
        
        if file_path is None:
            safe_ticker = ticker.replace(',', '_').replace('.', '_')
            file_path = f"/tmp/{safe_ticker}_close.csv"
        
        result = kimi_finance(
            ticker=ticker,
            time=time,
            type="close_summary",
            file_path=file_path
        )
        
        # Read the CSV file and return as dict
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if not df.empty:
                return {
                    "stocks": df.to_dict('records'),
                    "count": len(df)
                }
        
        return {"status": "success", "ticker": ticker, "time": time}
    except Exception as e:
        return {"error": str(e), "ticker": ticker}


def analyze_portfolio(tickers: List[str]) -> Dict:
    """
    Analyze a portfolio of stocks.
    
    Args:
        tickers: List of stock codes
    
    Returns:
        Dictionary containing portfolio analysis
    """
    results = []
    
    for ticker in tickers[:3]:  # Max 3 per query
        try:
            data = query_realtime_price(ticker)
            results.append(data)
        except Exception as e:
            results.append({"ticker": ticker, "error": str(e)})
    
    return {
        "portfolio": results,
        "count": len(results),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    # Test the functions
    print("Testing Stock Market Analyzer...")
    
    # Test single stock
    result = query_realtime_price("600519.SH")
    print(f"Real-time price result: {result}")
