---
name: quant-orchestrator
description: Multi-Agent AI Quant System with factor mining, strategy generation, and automated backtesting
metadata:
  clawdbot:
    emoji: "📊"
    homepage: "https://clawhub.com/quant-orchestrator"
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["python", "pip"]
      env: []
    install:
      - type: "script"
        run: "pip install lightgbm pandas numpy requests"
        description: "Install dependencies"
---

# Quant Orchestrator Skill

## 📊 Description
Multi-Agent AI Quant System for automated strategy research and backtesting.

## 💰 Pricing
- **1 USDC per call**
- 1 USDT = 1000 tokens
- Min deposit: 8 USDT
- Platform fee: 5%

## 🚀 Features
- **AI Factor Mining** - Generate trading factors automatically
- **AI Strategy Generation** - Create strategies from factors
- **Automated Backtesting** - One-click backtest with metrics
- **Strategy Evaluation** - Sharpe, MaxDrawdown, WinRate, IC, IR

## Architecture

```
Agentic Quant Platform
├── DataAgent (market data)
├── FactorAgent (AI factor mining)
├── StrategyAgent (AI strategy generation)
├── BacktestAgent (automated backtesting)
└── EvaluationAgent (strategy evaluation)
```

## Usage

```python
from skill_with_billing import QuantOrchestrator

# Run with user billing
orchestrator = QuantOrchestrator()
result = orchestrator.run_pipeline(
    task="研究BTC动量策略", 
    user_id="USER_ID"
)
```

## Output
- Sharpe Ratio
- Max Drawdown
- Win Rate
- IC (Information Coefficient)
- IR (Information Ratio)
- Strategy code
- Backtest results

## Quick Start

```bash
# Install dependencies
pip install lightgbm pandas numpy requests

# Run basic pipeline
python skill.py "研究BTC动量策略"

# Run with billing
python skill_with_billing.py "研究BTC策略" user123
```

## Files
- `skill.py` - Basic skill
- `skill_with_billing.py` - Skill with payment
- `billing.py` - Payment SDK
- `btc_predictor_optimized.py` - BTC prediction
