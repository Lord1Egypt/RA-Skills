---
name: quant-strategy-bundle
description: Quantitative trading strategy bundle - Contains multiple verified A-stock quantitative trading strategy frameworks. Includes momentum strategies, reversal strategies, and trend strategies, with backtesting and signal generation support. Ideal for quantitative trading beginners and strategy development reference.
tags:
  - quant
  - trading
  - stock
  - strategy
  - backtest
version: 1.0.0
author: chenq
---

# quant-strategy-bundle

Quantitative trading strategy bundle with multiple verified strategy frameworks.

## Included Strategies

### 1. Momentum Strategy
- Principle: Buy stocks that have risen in the past
- Holding period: 5-20 days
- Best for: Bull markets

### 2. Reversal Strategy
- Principle: Buy stocks that have fallen in the past
- Holding period: 3-10 days
- Best for: Range-bound markets

### 3. Trend Strategy
- Principle: Follow the trend, buy high sell higher
- Holding period: 10-30 days
- Best for: Strong trending markets

## Usage

### Install Dependencies
```bash
pip install pandas numpy xgboost tushare
```

### Basic Usage
```python
from strategy import MomentumStrategy, ReversalStrategy, TrendStrategy

# Initialize strategy
strategy = MomentumStrategy()

# Generate signals
signals = strategy.generate_signals(stock_pool, factors)

# Backtest
result = strategy.backtest(signals, prices)
```

## Configuration

Configure in `config.json`:
- Tushare token
- Stock pool
- Factor parameters
- Trading parameters

## Changelog

v1.0.0 - Initial release
