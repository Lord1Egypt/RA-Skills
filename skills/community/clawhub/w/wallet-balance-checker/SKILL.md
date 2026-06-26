---
name: wallet-balance-checker
description: "Check balances across Coinbase, Polymarket (Polygon USDC), Kalshi, and sportsbook accounts. Provides a unified capital view with low-balance alerts. Read-only — never moves funds. Use when asked about balances, capital, wallet status, or fund allocation."
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: ["curl", "jq"]
    credentials:
      - id: "coinbase-api-key"
        name: "Coinbase API Key"
        description: "Read-only API key from https://www.coinbase.com/settings/api"
        env: "COINBASE_API_KEY"
      - id: "coinbase-api-secret"
        name: "Coinbase API Secret"
        description: "API secret paired with the Coinbase API key"
        env: "COINBASE_API_SECRET"
      - id: "kalshi-api-key"
        name: "Kalshi API Key"
        description: "Read-only API key from Kalshi account settings"
        env: "KALSHI_API_KEY"
      - id: "polygon-rpc-url"
        name: "Polygon RPC URL"
        description: "Polygon JSON-RPC endpoint (Alchemy, Infura, or public)"
        env: "POLYGON_RPC_URL"
      - id: "polymarket-wallet"
        name: "Polymarket Wallet Address"
        description: "Your 0x Polygon wallet address holding USDC"
        env: "POLYMARKET_WALLET_ADDRESS"
---

# Wallet Balance Checker

Check balances across Coinbase, Polymarket, Kalshi, and sportsbook accounts. Unified capital view. Read-only.

## When to Use

Use this skill when the user asks about:
- Current balances on any platform
- Total available capital across platforms
- Whether they have enough funds for a trade
- Capital allocation or distribution
- Low-balance warnings or alerts
- "How much do I have?"

## CRITICAL: Read-Only Skill

This skill ONLY reads balances. It NEVER:
- Initiates transfers or withdrawals
- Places trades or orders
- Modifies account settings
- Sends funds to any address

If the user asks to move funds, tell them to do it manually or use a dedicated transfer skill with proper security controls.

## Operations

### 1. Check Coinbase Balance

Query all Coinbase accounts and show non-zero balances:

```bash
CB_TIMESTAMP=$(date +%s)
CB_MESSAGE="${CB_TIMESTAMP}GET/v2/accounts"
CB_SIGNATURE=$(echo -n "$CB_MESSAGE" | openssl dgst -sha256 -hmac "$COINBASE_API_SECRET" | cut -d' ' -f2)

curl -s "https://api.coinbase.com/v2/accounts" \
  -H "CB-ACCESS-KEY: $COINBASE_API_KEY" \
  -H "CB-ACCESS-SIGN: $CB_SIGNATURE" \
  -H "CB-ACCESS-TIMESTAMP: $CB_TIMESTAMP" \
  -H "CB-VERSION: 2024-01-01" \
  | jq '[.data[] | select((.balance.amount | tonumber) > 0) | {
    currency: .balance.currency,
    amount: .balance.amount,
    usd_value: .native_balance.amount
  }]'

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-wallet-balance-checker-skill/](https://agentbets.ai/guides/openclaw-wallet-balance-checker-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
