---
name: totoxu-montecarlo
description: Monte Carlo Crypto Trading Core. Simulates thousands of future price paths (Geometric Brownian Motion) to evaluate win probabilities, risk of ruin, and stop-loss impact for trading strategies.
version: 1.0.0
author: totoxu
requires:
  binaries:
    - python3
  env: ["SKILL_BILLING_API_KEY", "SKILL_ID"]
metadata:
  clawdbot:
    requires:
      env: ["SKILL_BILLING_API_KEY", "SKILL_ID"]
    files:
      - "scripts/*"
---

# Monte Carlo Crypto Core

This skill enables you to run sophisticated Monte Carlo simulations for trading strategies. 
It helps answer questions like: "If I buy BTC at $70,000 with 5% daily volatility and put a stop loss at $65,000, what is the probability I get stopped out within 30 days?"

## Setup
1. Install `requests`: `pip install requests`
2. Set the `SKILLPAY_API_KEY` environment variable with the skill owner's SkillPay API key.

## Billing (0.001 USDT per call via SkillPay)
This is a paid skill. **Every** simulation call requires the `--user USER_ID` parameter. If a call fails with a `payment_url`, you must show this link to the user.

---

## Tool: Run Monte Carlo Simulation

**Command:**
```bash
python scripts/montecarlo.py --user USER_ID --price 70000 --vol 0.04 --drift 0.001 --days 30 --paths 5000 --stop-loss 65000 --position long
```

**Required Parameters:**
- `--user`: The user's ID for billing.
- `--price`: The current price of the asset.
- `--vol`: The estimated **daily** volatility as a decimal (e.g., `0.04` for 4%). You can derive this from historical data standard deviation.

**Optional Parameters:**
- `--drift`: The expected daily return. Default is `0.0`. Positive drift favours longs, negative favours shorts.
- `--days`: Number of days to simulate into the future. Default: `30`.
- `--paths`: Number of simulation paths to run. Higher is more accurate but slower. Max is `20000`, Default `10000`.
- `--position`: `long` or `short`. Default is `long`. 
- `--stop-loss`: The exact price level where the position gets liquidated or closed for a loss.
- `--take-profit`: The exact price level where the position closes in profit.

**Output:**
Returns a JSON object containing expected prices, 5th/95th percentile worst/best case scenarios, and `risk_metrics` including the exact probability of hitting the stop loss (`hit_stop_loss_pct`) and overall win probability.

Use these probabilities to justify your trading advice to the user. Do not recommend trades with a `win_probability_pct` lower than 50% unless the user explicitly accepts high risk.
