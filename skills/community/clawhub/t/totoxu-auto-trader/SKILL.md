---
name: totoxu-auto-trader
description: Automated cryptocurrency trading system powered by AI. Instruct the agent to analyze the market and execute Binance spot trades based on technical indicators.
version: 1.0.0
author: totoxu
requires:
  binaries:
    - python3
  env: ["SKILL_BILLING_API_KEY", "SKILL_ID"]
metadata:
  clawdbot:
    requires:
      env: ["SKILL_BILLING_API_KEY", "SKILL_ID", "BINANCE_API_KEY", "BINANCE_SECRET"]
    files:
      - "scripts/*"
---

# Auto Crypto Trader

This skill empowers you, the AI Agent, to act as an autonomous cryptocurrency trader. 
You can run technical analysis on symbols like BTCUSDT, and based on your findings, execute real market orders on Binance.

## Prerequisites
1. Ensure the user has the Python libraries `requests` and `ccxt` installed. If not, tell them to run `pip install requests ccxt`.
2. To execute REAL trades, the user MUST provide the `BINANCE_API_KEY` and `BINANCE_SECRET` environment variables. You must ask them to set these securely before you execute the trade tool.

## Billing (0.001 USDT per call via SkillPay)
This is a paid skill. **Every** analysis and trade execution call requires the `--user USER_ID` parameter, which you must fill in for billing tracking. If a call fails with a `payment_url`, you must show this link to the user and stop trading until they top up.

---

## Tool 1: Analyze Market
**When to use:** Use this tool to analyze whether the market currently has a strong BUY or SELL signal.
You should run this *before* making any trades.

**Command:**
```bash
python scripts/analyze_market.py --user USER_ID --symbol BTCUSDT --interval 1h
```

**Parameters:**
- `--symbol`: The trading pair on Binance (no slashes), e.g., `BTCUSDT`, `ETHUSDT`
- `--interval`: The timeframe (e.g., `15m`, `1h`, `4h`, `1d`)
- `--user`: The user's ID for billing. Pass the username you're talking to.

**Output:**
Returns current prices, moving averages, RSI, Bollinger Bands, and a boolean `action` recommendation (`BUY`, `SELL`, or `HOLD`).
If the action is `BUY` and the user told you to trade autonomously, you should proceed to Tool 2.

---

## Tool 2: Execute Trade
**When to use:** Use this tool when you have verified an opportunity and want to execute a market order on Binance.
**CRITICAL**: You must pass the API keys as environment variables when making this call.

**Command:**
```bash
# Example syntax using cross-platform env vars (on Windows PowerShell, remind user to set $env:BINANCE_API_KEY)
BINANCE_API_KEY="user_key_here" BINANCE_SECRET="user_secret_here" python scripts/execute_trade.py --user USER_ID --symbol BTC/USDT --side buy --amount 0.001
```

**Parameters:**
- `--symbol`: The trading pair **WITH SLASH** (e.g., `BTC/USDT`, NOT `BTCUSDT`)
- `--side`: `buy` or `sell`
- `--amount`: The quantity of the BASE currency to trade (e.g., `0.001` means 0.001 BTC). You must calculate this properly before trading.
- `--user`: The user's ID for billing.
- `--testnet`: (Optional flag). Include this if the user wants to test with virtual balances on Binance Testnet first. Highly recommended for first-time use.

**Result Validation:**
The script will return JSON containing `"status": "success"` and an `"order_id"` if the trade goes through.
If it fails due to authentication or insufficient funds, tell the user exactly what went wrong.
