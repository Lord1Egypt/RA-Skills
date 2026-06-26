#!/usr/bin/env python3
"""
Shared utilities for stock analysis scripts.
"""

import requests
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import time


# Cache directory
CACHE_DIR = Path("/tmp/stock_analysis_cache")
CACHE_DIR.mkdir(exist_ok=True)


def cache_path(ticker: str, data_type: str, suffix: str = "json") -> Path:
    """Generate cache file path."""
    return CACHE_DIR / f"{ticker}_{data_type}.{suffix}"


def is_cache_valid(cache_file: Path, max_age_hours: int = 24) -> bool:
    """Check if cached file is still fresh."""
    if not cache_file.exists():
        return False
    age = time.time() - cache_file.stat().st_mtime
    return age < max_age_hours * 3600


def fetch_tencent_kline(ticker: str, days: int = 250) -> Optional[Dict]:
    """
    Fetch daily k-line data from Tencent Finance API with caching.

    Args:
        ticker: Stock code with market prefix (e.g., 'sh000001', 'sz399006')
        days: Number of trading days to fetch (max ~320)

    Returns:
        Dictionary with 'dates', 'open', 'high', 'low', 'close', 'volume', 'pe', 'pb' etc.
    """
    cache_file = cache_path(ticker, f"kline_{days}")

    if is_cache_valid(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except:
            pass  # Cache read failed, fetch fresh

    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param={ticker},day,,,{days},qfq"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        text = resp.text

        # Extract JSON from JavaScript variable
        match = re.search(r'kline_dayqfq=(\{.*\})', text)
        if not match:
            print(f"Warning: Could not parse response for {ticker}")
            return None

        data = json.loads(match.group(1))

        # Parse the data structure
        if data.get('code') != 0:
            return None

        ticker_key = list(data['data'].keys())[0]
        raw_data = data['data'][ticker_key]

        # Extract k-line data: try 'qfqday' first (forward-adjusted), fallback to 'day'
        kline_array = raw_data.get('qfqday') or raw_data.get('day', [])
        if not kline_array:
            print(f"Warning: No kline data for {ticker}")
            return None

        dates = []
        opens, highs, lows, closes, vols = [], [], [], [], []
        for entry in kline_array:
            # Entry can be either list or dict depending on API version
            if isinstance(entry, list):
                if len(entry) >= 6:
                    dates.append(entry[0])
                    opens.append(float(entry[1]))
                    highs.append(float(entry[2]))
                    lows.append(float(entry[3]))
                    closes.append(float(entry[4]))
                    vols.append(float(entry[5]))
            elif isinstance(entry, dict):
                dates.append(entry.get('date') or entry.get('dt'))
                opens.append(float(entry.get('open', 0)))
                highs.append(float(entry.get('high', 0)))
                lows.append(float(entry.get('low', 0)))
                closes.append(float(entry.get('close', 0)))
                vols.append(float(entry.get('volume', 0)))

        # Extract qt (latest snapshot) for PE/PB if available
        qt = raw_data.get('qt', [])
        pe = pb = None
        if qt and len(qt) > 50:
            # PE and PB positions may vary; need to detect by field names
            # For now, we can't reliably extract PE/PB from this endpoint
            pass

        result = {
            'ticker': ticker,
            'dates': dates,
            'open': opens,
            'high': highs,
            'low': lows,
            'close': closes,
            'volume': vols,
            'pe': pe,
            'pb': pb,
            'fetched_at': datetime.now().isoformat()
        }

        # Cache it
        with open(cache_file, 'w') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return result

    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None


def fetch_index_components(index_code: str) -> List[Dict]:
    """
    Fetch constituent stocks of an index.
    Placeholder - would need to scrape CSI website or use alternative API.
    """
    # TODO: Implement using http://www.csindex.com.cn or other sources
    return []


def get_risk_free_rate() -> float:
    """Get current risk-free rate (10-year Chinese government bond yield)."""
    # Placeholder - could fetch from market data
    return 0.03  # 3% default


def calculate_cagr(start: float, end: float, years: float) -> float:
    """Calculate compound annual growth rate."""
    if start <= 0 or end <= 0:
        return None
    return (end / start) ** (1 / years) - 1


def annualize_volatility(daily_returns: List[float]) -> float:
    """Annualize daily volatility."""
    import numpy as np
    return float(np.std(daily_returns, ddof=1) * np.sqrt(252) * 100)


def fetch_fundamental_financials(ticker: str) -> Optional[Dict]:
    """
    Fetch financial statements for a stock.
    Placeholder - would need to integrate with Eastmoney or other source.
    """
    # TODO: Implement using Eastmoney API or file-based data
    return None


if __name__ == "__main__":
    # Test
    data = fetch_tencent_kline("sh000001", 60)
    if data:
        print(f"Fetched {len(data['close'])} days of data")
        print(f"Latest close: {data['close'][-1]}")
    else:
        print("Failed to fetch data")
