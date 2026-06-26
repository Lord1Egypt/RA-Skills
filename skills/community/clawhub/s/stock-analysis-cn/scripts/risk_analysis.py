#!/usr/bin/env python3
"""
Risk Analysis Module for Stocks and ETFs

Calculates risk metrics including:
- Volatility (annualized standard deviation)
- Maximum Drawdown (peak-to-trough decline)
- Sharpe Ratio (risk-adjusted return)
- Sortino Ratio (downside risk-adjusted return)
- Value at Risk (VaR)
- Beta (relative to benchmark)
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class RiskMetrics:
    """Container for risk analysis results"""
    ticker: str
    analysis_period: str  # e.g., "1y", "3y", "5y"

    # Return metrics
    annualized_return: Optional[float] = None  # %
    annualized_volatility: Optional[float] = None  # %
    max_drawdown: Optional[float] = None  # Max peak-to-trough decline (%)

    # Risk-adjusted
    sharpe_ratio: Optional[float] = None  # Assuming risk-free rate ~2%
    sortino_ratio: Optional[float] = None
    calmar_ratio: Optional[float] = None  # Return / Max Drawdown

    # Tail risk
    var_95: Optional[float] = None  # 1-day 95% VaR (%)
    cvar_95: Optional[float] = None  # Conditional VaR (Expected Shortfall)

    # Market-relative
    beta: Optional[float] = None  # Beta vs benchmark (e.g., 沪深300)
    correlation: Optional[float] = None
    treynor_ratio: Optional[float] = None

    # Streaks
    longest_up_streak: Optional[int] = None
    longest_down_streak: Optional[int] = None


def fetch_returns(ticker: str, period_days: int = 252) -> np.ndarray:
    """
    Fetch daily returns series using Tencent Finance API.

    Args:
        ticker: Stock/ETF code
        period_days: Number of trading days (252 ≈ 1 year)

    Returns:
        Array of daily returns in decimal (0.02 = 2%)
    """
    from utils import fetch_tencent_kline
    import numpy as np

    data = fetch_tencent_kline(ticker, period_days + 1)  # need one extra for return calculation
    if not data or len(data['close']) < 2:
        return np.array([])

    closes = np.array(data['close'], dtype=float)
    # Calculate daily returns: (today - yesterday) / yesterday
    returns = (closes[1:] - closes[:-1]) / closes[:-1]

    return returns


def calculate_volatility(returns: np.ndarray, annualize: bool = True) -> float:
    """Calculate annualized standard deviation of returns."""
    if len(returns) == 0:
        return None
    daily_vol = np.std(returns, ddof=1)
    if annualize:
        return float(daily_vol * np.sqrt(252) * 100)
    return float(daily_vol * 100)


def calculate_max_drawdown(prices: np.ndarray) -> float:
    """Compute maximum peak-to-trough drawdown percentage."""
    if len(prices) == 0:
        return None
    # Running maximum
    running_max = np.maximum.accumulate(prices)
    # Drawdown series
    drawdown = (prices - running_max) / running_max * 100
    max_dd = np.min(drawdown)
    return float(abs(max_dd))


def calculate_sharpe(returns: np.ndarray, rf_rate: float = 0.02) -> Optional[float]:
    """Annualized Sharpe ratio (excess return / volatility)."""
    if len(returns) == 0:
        return None
    mean_daily = np.mean(returns)
    vol_daily = np.std(returns, ddof=1)
    if vol_daily == 0:
        return None
    sharpe_daily = (mean_daily - rf_rate/252) / vol_daily
    return float(sharpe_daily * np.sqrt(252))


def calculate_sortino(returns: np.ndarray, rf_rate: float = 0.02, target: float = 0) -> Optional[float]:
    """Sortino ratio (excess return / downside deviation)."""
    if len(returns) == 0:
        return None
    excess_returns = returns - rf_rate/252
    mean_excess = np.mean(excess_returns)

    downside_returns = excess_returns[excess_returns < target]
    if len(downside_returns) == 0:
        return None
    downside_dev = np.std(downside_returns, ddof=1)
    if downside_dev == 0:
        return None
    sortino_daily = mean_excess / downside_dev
    return float(sortino_daily * np.sqrt(252))


def calculate_var(returns: np.ndarray, confidence: float = 0.95) -> Optional[float]:
    """Historical Value at Risk (1-day, % loss)."""
    if len(returns) == 0:
        return None
    loss = -returns  # convert to loss positive
    var = np.percentile(loss, (1 - confidence) * 100)
    return float(var * 100)


def calculate_cvar(returns: np.ndarray, confidence: float = 0.95) -> Optional[float]:
    """Conditional Value at Risk (expected shortfall)."""
    if len(returns) == 0:
        return None
    loss = -returns
    var = np.percentile(loss, (1 - confidence) * 100)
    cvar = np.mean(loss[loss >= var])
    return float(cvar * 100)


def calculate_beta(returns: np.ndarray, benchmark_returns: np.ndarray) -> Optional[float]:
    """Beta = Cov(Ri, Rm) / Var(Rm)"""
    if len(returns) != len(benchmark_returns) or len(returns) < 2:
        return None
    cov = np.cov(returns, benchmark_returns)[0, 1]
    var_m = np.var(benchmark_returns, ddof=1)
    if var_m == 0:
        return None
    return float(cov / var_m)


def calculate_streaks(returns: np.ndarray) -> Tuple[int, int]:
    """Calculate longest consecutive up and down days."""
    if len(returns) == 0:
        return (0, 0)
    signs = np.sign(returns)
    up_streak = down_streak = 0
    max_up = max_down = 0
    for s in signs:
        if s > 0:
            up_streak += 1
            down_streak = 0
            max_up = max(max_up, up_streak)
        elif s < 0:
            down_streak += 1
            up_streak = 0
            max_down = max(max_down, down_streak)
        else:
            up_streak = down_streak = 0
    return (max_up, max_down)


def analyze(ticker: str, period_days: int = 252, benchmark: str = "sh000001") -> Dict:
    """
    Main entry point: perform comprehensive risk analysis.

    Args:
        ticker: Stock/ETF code
        period_days: Lookback period in trading days (default 1 year)
        benchmark: Benchmark index code (default: 上证指数)

    Returns:
        Dictionary with RiskMetrics and summary
    """
    # 1. Fetch returns
    returns = fetch_returns(ticker, period_days)
    if len(returns) < 20:
        return {"error": "Insufficient return data"}

    # 2. Reconstruct price series from returns
    price_series = 100 * np.cumprod(1 + returns)  # start at 100

    # 3. Compute metrics
    metrics = RiskMetrics(
        ticker=ticker,
        analysis_period=f"{period_days}d"
    )

    metrics.annualized_return = float((price_series[-1] / price_series[0]) ** (252 / len(returns)) - 1) * 100
    metrics.annualized_volatility = calculate_volatility(returns)
    metrics.max_drawdown = calculate_max_drawdown(price_series)
    metrics.sharpe_ratio = calculate_sharpe(returns)
    metrics.sortino_ratio = calculate_sortino(returns)
    metrics.var_95 = calculate_var(returns)
    metrics.cvar_95 = calculate_cvar(returns)

    # Beta (need benchmark returns)
    # bench_returns = fetch_returns(benchmark, period_days)
    # if len(bench_returns) == len(returns):
    #     metrics.beta = calculate_beta(returns, bench_returns)
    #     metrics.correlation = np.corrcoef(returns, bench_returns)[0,1]

    metrics.longest_up_streak, metrics.longest_down_streak = calculate_streaks(returns)
    metrics.calmar_ratio = (metrics.annualized_return / 100) / (metrics.max_drawdown / 100) if metrics.max_drawdown else None

    # 4. Summary
    summary = generate_summary(metrics)

    return {
        'ticker': ticker,
        'metrics': metrics,
        'summary': summary
    }


def generate_summary(m: RiskMetrics) -> str:
    """Generate plain-language risk summary."""
    parts = []

    if m.annualized_volatility:
        vol_desc = f"年化波动率: {m.annualized_volatility:.1f}%"
        if m.annualized_volatility > 30:
            vol_desc += "（高波动）"
        elif m.annualized_volatility < 15:
            vol_desc += "（低波动）"
        parts.append(vol_desc)

    if m.max_drawdown:
        dd_desc = f"最大回撤: {m.max_drawdown:.1f}%"
        parts.append(dd_desc)

    if m.sharpe_ratio:
        sharpe_desc = f"夏普比率: {m.sharpe_ratio:.2f}"
        parts.append(sharpe_desc)

    if m.beta:
        beta_desc = f"Beta: {m.beta:.2f}"
        if m.beta > 1.2:
            beta_desc += "（进攻型，波动大于大盘）"
        elif m.beta < 0.8:
            beta_desc += "（防御型，波动小于大盘）"
        parts.append(beta_desc)

    return "；".join(parts)


if __name__ == "__main__":
    # Example with mock data
    np.random.seed(42)
    mock_returns = np.random.normal(0.0005, 0.02, 252)
    ticker = "MOCK"

    result = analyze(ticker)
    print(f"Risk Analysis for {ticker}:")
    print(result['summary'])
