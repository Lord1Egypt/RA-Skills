# Monte Carlo Crypto Core

Professional Monte Carlo simulation engine for crypto trading strategies on OpenClaw.

## Features

- **Geometric Brownian Motion (GBM)**: Accurate mathematical modeling of asset price paths.
- **Risk Assessment**: Calculates exact probabilities of hitting Stop-Loss or Take-Profit levels.
- **Value at Risk (VaR)**: Provides 5th and 95th percentile price expectations.
- **Long & Short Profiles**: Fully supports evaluating both long and short trading positions.
- **Billing Integration**: Pay-per-use at incredibly low rates (0.001 USDT per call via SkillPay).

## Prerequisites

- Python 3.9+
- `requests` library (for billing): `pip install requests`
- `SKILLPAY_API_KEY` environment variable (set by the skill owner)

The Monte Carlo engine itself uses only standard libraries (`math`, `random`) with the Box-Muller transform — no heavy dependencies like `numpy` or `scipy` needed.

## How to use

Once installed, simply chat with your OpenClaw agent:

> "I want to buy Ethereum at $3000. Assuming historic daily volatility is 3%, if I set a stop loss at $2800, what's my chance of getting stopped out in the next 14 days?"

The agent will use this skill to run 10,000 simulated timelines and return the exact probability and risk assessment.
