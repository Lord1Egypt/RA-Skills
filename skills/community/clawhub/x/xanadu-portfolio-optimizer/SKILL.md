---
name: portfolio-optimizer
description: Optimize investment portfolios through rebalancing, risk analysis, and tax-loss harvesting. Use when: (1) Rebalancing portfolio allocation, (2) Analyzing portfolio risk and diversification, (3) Finding tax-loss harvesting opportunities, (4) Calculating optimal asset allocation.
---

# Portfolio Optimizer

Optimize investment portfolios with rebalancing, risk analysis, and tax optimization.

## Quick Start

```bash
# Analyze portfolio
python scripts/optimizer.py analyze --holdings AAPL:10,MSFT:15,GOOGL:5

# Rebalance
python scripts/optimizer.py rebalance --holdings AAPL:10,MSFT:15,GOOGL:5 --target "AAPL:30,MSFT:30,GOOGL:40"

# Tax-loss harvest
python scripts/optimizer.py harvest --holdings AAPL:-500,MSFT:200
```

## Core Features

### 1. Portfolio Analysis

- Current allocation breakdown
- Sector exposure
- Risk metrics (volatility, beta, Sharpe ratio)
- Diversification score
- Performance vs benchmarks

### 2. Rebalancing

Calculate trades needed to reach target allocation:
- Threshold-based rebalancing (e.g., rebalance when >5% drift)
- Calendar-based (quarterly, annually)
- Tax-aware rebalancing (minimize capital gains)

### 3. Tax-Loss Harvesting

Identify positions with losses to offset gains:
- Short-term vs long-term losses
- Wash sale rule awareness
- Suggested replacement securities

### 4. Risk Analysis

- Portfolio volatility
- Maximum drawdown
- Value at Risk (VaR)
- Beta vs market
- Correlation matrix

## Usage

### Analyze Current Portfolio
```bash
python scripts/optimizer.py analyze --holdings AAPL:10,MSFT:15,GOOGL:5
```

### Get Rebalancing Trades
```bash
python scripts/optimizer.py rebalance \
  --holdings AAPL:10000,MSFT:15000,GOOGL:5000 \
  --target "AAPL:33,MSFT:33,GOOGL:33"
```

### Tax-Loss Harvesting Opportunities
```bash
python scripts/optimizer.py harvest --file portfolio.json
```

### Risk Report
```bash
python scripts/optimizer.py risk --holdings AAPL:10,MSFT:20,GOOGL:5
```

## Input Format

Holdings can be specified as:
- `SYMBOL:VALUE` (dollar value)
- `SYMBOL:SHARES:AVG_COST` (shares with cost basis)

Example:
```bash
--holdings AAPL:15000,MSFT:20000,GOOGL:5000
```

Or with cost basis:
```bash
--holdings "AAPL:100:150.00,MSFT:50:280.00"
```

## Output

Analysis includes:
- Current vs target allocation
- Trades needed to rebalance
- Estimated tax impact
- Risk metrics
- Recommendations

## Requirements

- Python 3.10+
- `yfinance` for price data
- `numpy`, `pandas` for calculations

---

## Monetization (SkillPay)

This skill supports SkillPay integration for premium features.

### Pricing Tiers
| Tier | Price | Features |
|------|-------|----------|
| Basic | Free | Basic analysis, manual rebalancing |
| Pro | $29/mo | Auto rebalancing, tax-loss harvesting, risk metrics |
| Premium | $49/mo | API access, unlimited portfolios, priority support |

Owner: Xanadu Studios
