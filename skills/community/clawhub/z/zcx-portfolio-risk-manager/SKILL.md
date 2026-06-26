---
name: portfolio-risk-manager
description: Calculate portfolio risk metrics — Value at Risk (VaR), Sharpe ratio, max drawdown, correlation matrix, position sizing, and scenario analysis. Supports multi-asset portfolios with historical data analysis.
emoji: 📊
tags: [portfolio, risk-management, var, sharpe, drawdown, position-sizing, kelly]
metadata:
  openclaw:
    requires:
      bins: []
---

# Portfolio Risk Manager — 投资组合风险管理

Calculate key risk metrics for multi-asset portfolios using pure math (no third-party financial libraries). Supports equities, crypto, futures, and mixed portfolios.

## Risk Metrics

### 1. Value at Risk (VaR)

Historical simulation — the worst expected loss over a given confidence level and time horizon.

```python
import numpy as np

def calculate_var(returns, confidence=0.95):
    """Historical VaR."""
    sorted_returns = np.sort(returns)
    index = int((1 - confidence) * len(sorted_returns))
    return sorted_returns[index]

def calculate_cvar(returns, confidence=0.95):
    """Conditional VaR (Expected Shortfall) — average of losses beyond VaR."""
    sorted_returns = np.sort(returns)
    index = int((1 - confidence) * len(sorted_returns))
    tail = sorted_returns[:index]
    return np.mean(tail) if len(tail) > 0 else sorted_returns[0]
```

**Interpretation:**
- 95% VaR of -2% → 5% chance of losing >2% in a day
- CVaR is stricter than VaR (looks at the tail, not just the threshold)

### 2. Sharpe Ratio

Risk-adjusted return measure. Annualized.

```python
def sharpe_ratio(returns, risk_free_rate=0.05, periods_per_year=252):
    """Annualized Sharpe Ratio."""
    excess = np.mean(returns) - risk_free_rate / periods_per_year
    return excess / np.std(returns) * np.sqrt(periods_per_year) if np.std(returns) > 0 else 0

def sortino_ratio(returns, risk_free_rate=0.05, periods_per_year=252):
    """Sortino Ratio — only penalizes downside volatility."""
    excess = np.mean(returns) - risk_free_rate / periods_per_year
    downside = np.std(returns[returns < 0]) if np.any(returns < 0) else 0.001
    return excess / downside * np.sqrt(periods_per_year)
```

**Interpretation:**
| Sharpe | Rating |
|:-------|:-------|
| > 2.0 | Excellent |
| 1.0 - 2.0 | Good |
| 0.5 - 1.0 | Average |
| < 0.5 | Poor |
| < 0 | Underperforming risk-free |

### 3. Maximum Drawdown

Largest peak-to-trough decline.

```python
def max_drawdown(prices):
    """Calculate max drawdown from price series."""
    peak = np.maximum.accumulate(prices)
    drawdown = (prices - peak) / peak
    max_dd = np.min(drawdown)
    # Also return duration: how long to recover
    trough_idx = np.argmin(drawdown)
    recovery_idx = np.argmax(prices[trough_idx:] >= prices[:len(prices)-trough_idx][0])
    recovery_days = recovery_idx if recovery_idx > 0 else None
    return {"drawdown": max_dd, "trough_index": trough_idx, "recovery_days": recovery_days}
```

### 4. Correlation Matrix

```python
def correlation_matrix(returns_dict):
    """Correlation matrix from multiple return series."""
    assets = list(returns_dict.keys())
    n = len(assets)
    matrix = np.ones((n, n))
    for i in range(n):
        for j in range(i+1, n):
            r = np.corrcoef(returns_dict[assets[i]], returns_dict[assets[j]])[0, 1]
            matrix[i, j] = round(r, 3)
            matrix[j, i] = round(r, 3)
    return {"assets": assets, "matrix": matrix}
```

**Interpretation:** Correlation of 1 = move together, -1 = move opposite, 0 = no relationship. During crises, correlations converge toward 1 (everything sells off together).

### 5. Position Sizing (Kelly Criterion)

```python
def kelly_criterion(win_rate, avg_win, avg_loss):
    """Full Kelly — aggressive. Most traders use fractional Kelly."""
    b = avg_win / abs(avg_loss) if avg_loss != 0 else 1
    p = win_rate
    q = 1 - p
    full_kelly = (p * b - q) / b if b > 0 else 0
    return {
        "full_kelly": max(0, full_kelly),
        "quarter_kelly": max(0, full_kelly * 0.25),
        "half_kelly": max(0, full_kelly * 0.5),
    }
```

### 6. Scenario Analysis

```python
def scenario_analysis(positions, scenario_returns):
    """Analyze portfolio under different market scenarios.
    
    positions: {"BTC": 50000, "ETH": 30000, "CASH": 20000}
    scenario_returns: {"crash": {"BTC": -0.3, "ETH": -0.4, "CASH": 0},
                       "rally": {"BTC": 0.2, "ETH": 0.25, "CASH": 0}}
    """
    results = {}
    for scenario, returns in scenario_returns.items():
        pnl = 0
        for asset, exposure in positions.items():
            if asset in returns:
                pnl += exposure * returns[asset]
        total = sum(positions.values())
        results[scenario] = {"pnl": round(pnl, 2), "return_pct": round(pnl / total * 100, 2) if total > 0 else 0}
    return results
```

## Complete Usage Example

```python
import numpy as np

# Daily returns for 3 assets (1 year = 252 days)
portfolio = {
    "BTC": np.random.normal(0.001, 0.03, 252),
    "ETH": np.random.normal(0.001, 0.04, 252),
    "BOND": np.random.normal(0.0003, 0.005, 252),
}
weights = {"BTC": 0.5, "ETH": 0.3, "BOND": 0.2}
portfolio_returns = sum(weights[a] * portfolio[a] for a in weights)

print(f"95% VaR: {calculate_var(portfolio_returns):.2%}")
print(f"CVaR:    {calculate_cvar(portfolio_returns):.2%}")
print(f"Sharpe:  {sharpe_ratio(portfolio_returns):.2f}")
print(f"Sortino: {sortino_ratio(portfolio_returns):.2f}")

# Simulated price series
prices = 100 * np.exp(np.cumsum(portfolio_returns))
dd = max_drawdown(prices)
print(f"Max DD:  {dd['drawdown']:.2%}  (recovery: {dd['recovery_days'] or 'N/A'} days)")

print(f"Correlation:\n{correlation_matrix(portfolio)}")

# Scenario analysis
scenarios = {
    "crash": {"BTC": -0.3, "ETH": -0.4, "BOND": 0.02},
    "mild_dip": {"BTC": -0.05, "ETH": -0.08, "BOND": 0.01},
    "rally": {"BTC": 0.15, "ETH": 0.2, "BOND": -0.02},
}
positions = {"BTC": 50000, "ETH": 30000, "BOND": 20000}
print(f"Scenario: {scenario_analysis(positions, scenarios)}")
```

## Format Output

```
📊 投资组合风险报告

组合总值: $100,000
持仓: BTC 50% | ETH 30% | BOND 20%

🛡️ 风险指标
• VaR (95%):    -2.3%  → 日最大亏损 $2,300
• CVaR (95%):   -3.1%  → 尾部平均亏损 $3,100
• VaR (99%):    -3.8%  → 日最大亏损 $3,800
• Sharpe:        1.25  🟢
• Sortino:       1.52  🟢 (更好，只看下行)
• 最大回撤:     -15.4%  (恢复期: 45天)

🔗 相关性矩阵
        BTC    ETH   BOND
BTC     1.00   0.65  0.10
ETH     0.65   1.00  0.08
BOND    0.10   0.08  1.00

📈 情景分析
• 崩盘 (-30%):   PnL -$27,000 (-27.0%) 🔴
• 温和回调 (-5%): PnL -$4,900 (-4.9%)  🟡
• 大涨 (+15%):   PnL +$13,500 (+13.5%) 🟢

💰 仓位建议 (Kelly)
• BTC:  35% (全Kelly)  → 17.5% (半Kelly)  → 8.7% (¼Kelly)
• ETH:  20% → 10% → 5%
• 现金: 45% → 72.5% → 86.3%

⚠️ 回测不代表未来，Kelly建议保守使用半仓或¼仓
```

## Notes
- All calculations use NumPy only — no external financial libraries needed
- Historical VaR/CVaR assumes past patterns persist (they often don't in crises)
- Kelly Criterion is aggressive — most professional traders use fractional Kelly (25-50%)
- Correlation is NOT constant — it spikes during market stress (correlations converge to 1)
- Sortino > Sharpe when returns are asymmetric (typical in options trading)
- Always stress-test with scenario analysis — don't rely on VaR alone
