#!/usr/bin/env python3
"""
Screening Module for Stocks and ETFs

Factor-based screening and ranking system.

Supported factors:
- Value: PE, PB, PS, PEG
- Quality: ROE, ROA, Debt/Equity, CF quality
- Growth: Revenue CAGR, Profit CAGR
- Momentum: Price momentum (1m, 3m, 6m)
- Low Volatility: Historical beta, volatility
- Dividend: Dividend yield, payout ratio
"""

import pandas as pd
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field


@dataclass
class ScreenCriteria:
    """Criteria for filtering investment candidates"""
    # Universe filters
    market: List[str] = field(default_factory=lambda: ['sh', 'sz'])  # A-shares
    instrument_type: str = "etf"  # 'stock' or 'etf'
    min_liquidity: Optional[float] = None  # Min daily avg volume (万元)
    min_aum: Optional[float] = None  # Min assets under management (亿元) for ETFs

    # Factor thresholds (all in decimal or percentile)
    pe_max: Optional[float] = None  # e.g., 20 means PE <= 20
    pb_max: Optional[float] = None
    roe_min: Optional[float] = None  # e.g., 15 means ROE >= 15%
    revenue_growth_min: Optional[float] = None
    momentum_rank: Optional[int] = None  # Top N by recent performance
    dividend_yield_min: Optional[float] = None

    # Composite scoring weights (for ranking)
    weights: Dict[str, float] = field(default_factory=dict)


class ScreeningResult:
    """Container for screening results"""
    def __init__(self, candidates: pd.DataFrame, summary: str):
        self.candidates = candidates  # DataFrame with ticker, name, metrics, score
        self.summary = summary
        self.count = len(candidates)

    def top_n(self, n: int) -> pd.DataFrame:
        """Return top N ranked candidates."""
        return self.candidates.head(n)

    def to_markdown(self) -> str:
        """Render results as markdown table."""
        if self.candidates.empty:
            return "无符合条件的结果"
        # Select columns for display
        cols = ['ticker', 'name', 'pe', 'pb', 'roe', 'revenue_growth_cagr', 'dividend_yield', 'score']
        display_df = self.candidates[cols].copy()
        # Format numbers
        for col in ['pe', 'pb']:
            display_df[col] = display_df[col].round(2)
        for col in ['roe', 'revenue_growth_cagr', 'dividend_yield']:
            display_df[col] = display_df[col].round(1)
        display_df['score'] = display_df['score'].round(3)
        return display_df.to_markdown(index=False)


def fetch_universe(criteria: ScreenCriteria) -> pd.DataFrame:
    """
    Fetch all tickers in the target universe.
    For ETFs, attempts to load from a local CSV file that contains ETF metadata.
    Falls back to an empty DataFrame if no data source available.

    Expected CSV format (semicolon or comma separated):
        ticker,name,index,volume,aum,management_fee,etc.

    Returns:
        DataFrame with columns: ticker, name, instrument_type, ...
    """
    import csv
    from pathlib import Path

    # Try to load from common locations
    possible_files = [
        Path("/root/.openclaw/etf-workspace/etf_list.csv"),
        Path("/tmp/etf_list.csv"),
        Path("etf_list.csv"),
    ]

    for filepath in possible_files:
        if filepath.exists():
            try:
                df = pd.read_csv(filepath, dtype={'ticker': str})
                # Standardize column names
                if '代码' in df.columns:
                    df = df.rename(columns={'代码': 'ticker', '名称': 'name'})
                if '基金代码' in df.columns:
                    df = df.rename(columns={'基金代码': 'ticker', '基金名称': 'name'})
                # Ensure required columns
                if 'ticker' not in df.columns or 'name' not in df.columns:
                    continue
                df['instrument_type'] = 'etf'
                return df[['ticker', 'name', 'instrument_type']]
            except Exception as e:
                print(f"Warning: Could not load ETF list from {filepath}: {e}")
                continue

    # No data source found
    print("Warning: No ETF list file found. Screening will return empty result.")
    return pd.DataFrame()


def enrich_with_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add fundamental and market metrics to each ticker.

    For each ticker, fetch/calculate:
    - Volume: average daily volume (from recent data)
    - Returns: 1m, 3m, 6m price returns
    - PE, PB: from static benchmarks mapping (index-based)
    - Other fundamentals: placeholder for future integration

    Returns:
        Augmented DataFrame with metric columns
    """
    from utils import fetch_tencent_kline
    from valuation_analysis import analyze as val_analyze
    import numpy as np

    if df.empty:
        return df

    # Add metric columns
    df['avg_volume'] = np.nan
    df['return_1m'] = np.nan
    df['return_3m'] = np.nan
    df['return_6m'] = np.nan
    df['pe'] = np.nan
    df['pb'] = np.nan
    df['roe'] = np.nan
    df['dividend_yield'] = np.nan

    # Simple ETF->Index PE mapping (static approximations)
    ETF_PE_MAP = {
        'sh510300': 12.5,  # 沪深300
        'sh510500': 22.0,  # 中证500
        'sz159915': 45.0,  # 创业板
        'sh588000': 55.0,  # 科创50
        'sh512880': 18.0,  # 证券
    }
    ETF_PB_MAP = {
        'sh510300': 1.7,
        'sh510500': 2.0,
        'sz159915': 4.5,
        'sh588000': 5.5,
        'sh512880': 1.8,
    }

    for idx, row in df.iterrows():
        ticker = row['ticker']

        # 1. Fetch price data to compute returns and volume
        hist = fetch_tencent_kline(ticker, 320)  # enough for 6m
        if hist and len(hist['close']) > 0:
            closes = hist['close']
            vols = hist['volume']

            # Volume: average over last 20 days (in 万元) - adjust if needed
            if len(vols) >= 20:
                df.at[idx, 'avg_volume'] = float(np.mean(vols[-20:]))

            # Returns (approx trading days: 22/month)
            if len(closes) >= 22:
                df.at[idx, 'return_1m'] = (closes[-1] / closes[-22] - 1) * 100
            if len(closes) >= 66:
                df.at[idx, 'return_3m'] = (closes[-1] / closes[-66] - 1) * 100
            if len(closes) >= 132:
                df.at[idx, 'return_6m'] = (closes[-1] / closes[-132] - 1) * 100

        # 2. Valuation metrics: use static mapping for known ETFs, else try valuation_analysis
        if ticker in ETF_PE_MAP:
            df.at[idx, 'pe'] = ETF_PE_MAP[ticker]
            df.at[idx, 'pb'] = ETF_PB_MAP.get(ticker, np.nan)
        else:
            try:
                # Fallback to valuation_analysis (works for index codes)
                val_result = val_analyze(ticker)
                metrics = val_result['metrics']
                # Only use if realistic values returned (not placeholder)
                if metrics.pe and metrics.pe > 0:
                    df.at[idx, 'pe'] = metrics.pe
                if metrics.pb and metrics.pb > 0:
                    df.at[idx, 'pb'] = metrics.pb
            except:
                pass  # leave as NaN

        # 3. Fundamental metrics - placeholder
        # Would need separate API call (future)
        # For demo, can mock for known tickers
        if ticker in ['sh600519', 'sz000001']:
            df.at[idx, 'roe'] = 15.0  # mock

    return df


def apply_filters(df: pd.DataFrame, criteria: ScreenCriteria) -> pd.DataFrame:
    """Apply hard filters to the universe, gracefully handling missing data."""
    filtered = df.copy()

    if criteria.pe_max:
        mask = filtered['pe'].notna() & (filtered['pe'] <= criteria.pe_max)
        filtered = filtered[mask]
    if criteria.pb_max:
        mask = filtered['pb'].notna() & (filtered['pb'] <= criteria.pb_max)
        filtered = filtered[mask]
    if criteria.roe_min:
        mask = filtered['roe'].notna() & (filtered['roe'] >= criteria.roe_min)
        filtered = filtered[mask]
    if criteria.revenue_growth_min:
        mask = filtered['revenue_growth_cagr'].notna() & (filtered['revenue_growth_cagr'] >= criteria.revenue_growth_min)
        filtered = filtered[mask]
    if criteria.dividend_yield_min:
        mask = filtered['dividend_yield'].notna() & (filtered['dividend_yield'] >= criteria.dividend_yield_min)
        filtered = filtered[mask]
    if criteria.min_liquidity:
        mask = filtered['avg_volume'].notna() & (filtered['avg_volume'] >= criteria.min_liquidity)
        filtered = filtered[mask]
    if criteria.min_aum:
        mask = filtered['aum'].notna() & (filtered['aum'] >= criteria.min_aum)
        filtered = filtered[mask]

    return filtered


def calculate_composite_score(df: pd.DataFrame, weights: Dict[str, float]) -> pd.Series:
    """
    Calculate a composite score for each candidate.

    Scoring:
    - For each factor, normalize to 0-1 scale (min-max or percentile)
    - Weighted sum: score = Σ (factor_score * weight)
    - Higher score = better

    Args:
        df: DataFrame with factor columns
        weights: Dictionary mapping factor names to weights (should sum to 1)

    Returns:
        Series of composite scores indexed same as df
    """
    score_df = pd.DataFrame(index=df.index)

    for factor, weight in weights.items():
        if factor not in df.columns:
            continue
        series = df[factor].copy()
        # Direction: higher is better for most factors except PE, PB
        if factor in ['pe', 'pb']:
            # Invert: lower PE/PB = higher score
            series = -series
        # Min-max normalization to 0-1
        if series.max() != series.min():
            normalized = (series - series.min()) / (series.max() - series.min())
        else:
            normalized = 1.0
        score_df[factor] = normalized * weight

    composite = score_df.sum(axis=1)
    return composite


def screen(criteria: ScreenCriteria, universe_df: Optional[pd.DataFrame] = None) -> ScreeningResult:
    """
    Main entry point: run the screening workflow.

    Steps:
    1. Fetch universe (or use provided DataFrame)
    2. Enrich with metrics (fundamental, market, factor data)
    3. Apply hard filters (cutoffs on individual factors)
    4. Rank by composite score (if weights provided)
    5. Return sorted candidates

    Args:
        criteria: Screening criteria object
        universe_df: Optional pre-loaded universe DataFrame (skips fetch_universe)

    Returns:
        ScreeningResult with candidates and summary
    """
    # 1. Fetch universe
    if universe_df is None:
        universe = fetch_universe(criteria)
    else:
        universe = universe_df.copy()

    if universe.empty:
        return ScreeningResult(pd.DataFrame(), "空 Universe 或数据源不可用")

    initial_count = len(universe)

    # 2. Enrich
    enriched = enrich_with_metrics(universe)

    # 3. Filter
    filtered = apply_filters(enriched, criteria)

    # 4. Composite score if weights exist
    if criteria.weights and not filtered.empty:
        filtered['score'] = calculate_composite_score(filtered, criteria.weights)
        filtered = filtered.sort_values('score', ascending=False)
    elif not filtered.empty:
        filtered['score'] = 0

    # 5. Summary
    summary = f"初选池: {initial_count} 只 → 过滤后: {len(filtered)} 只"
    if 'score' in filtered.columns:
        summary += f"（已按综合得分排序）"

    return ScreeningResult(filtered, summary)


# --- Preset Screen Templates ---

def value_screening() -> ScreenCriteria:
    """筛选低估值股票/ETF"""
    return ScreenCriteria(
        pe_max=15,
        pb_max=1.5,
        roe_min=10,
        dividend_yield_min=2.0,
        weights={'pe': -0.3, 'pb': -0.3, 'roe': 0.2, 'dividend_yield': 0.2}  # - means lower is better
    )


def growth_screening() -> ScreenCriteria:
    """筛选高成长股票"""
    return ScreenCriteria(
        revenue_growth_min=15,
        weights={'revenue_growth_cagr': 0.5, 'roe': 0.3, 'pe': -0.2}  # Accept higher PE for growth
    )


def quality_screening() -> ScreenCriteria:
    """筛选高质量（盈利稳定、低负债）"""
    return ScreenCriteria(
        roe_min=15,
        weights={'roe': 0.4, 'debt_to_equity': -0.3, 'revenue_growth_cagr': 0.2, 'ocf_to_net_income': 0.1}
    )


def low_vol_screening() -> ScreenCriteria:
    """筛选低波动品种"""
    return ScreenCriteria(
        weights={'annualized_volatility': -0.5, 'beta': -0.3, 'max_drawdown': -0.2}  # lower is better
    )


def etf_liquidity_screening(min_volume: float = 1000, min_aum: float = 5) -> ScreenCriteria:
    """筛选流动性好的ETF"""
    return ScreenCriteria(
        instrument_type='etf',
        min_liquidity=min_volume,
        min_aum=min_aum
    )


if __name__ == "__main__":
    # Example: Run value screening on a small test ETF list
    print("=== Stock Analysis Skill - Screening Demo ===")

    criteria = value_screening()
    print(f"Criteria: PE<={criteria.pe_max}, PB<={criteria.pb_max}, ROE>={criteria.roe_min}%, DivYield>={criteria.dividend_yield_min}%")

    # Load test universe from CSV (must have columns: ticker, name)
    try:
        import pandas as pd
        universe = pd.read_csv('/tmp/etf_list_test.csv', dtype={'ticker': str})
        universe['instrument_type'] = 'etf'
        print(f"\nUniverse loaded: {len(universe)} ETFs")
        print(universe[['ticker','name']].to_string(index=False))
    except Exception as e:
        print(f"Could not load test universe: {e}")
        print("Please create /tmp/etf_list_test.csv with columns: ticker,name")
        exit(1)

    # Run screen
    result = screen(criteria, universe_df=universe)

    print(f"\n{result.summary}")
    if not result.candidates.empty:
        print("\nCandidates that passed filters:")
        cols = ['ticker','name','pe','pb','roe','dividend_yield']
        print(result.candidates[cols].to_string(index=False))
    else:
        print("\nNo candidates met all criteria. Consider relaxing thresholds.")
        print("\nSample enriched data (before filtering):")
        enriched = enrich_with_metrics(universe.copy())
        print(enriched[['ticker','pe','pb','avg_volume','return_1m']].to_string(index=False))
