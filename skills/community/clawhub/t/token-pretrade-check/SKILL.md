---
name: token-pretrade-check
description: "Full pre-trade checklist for any EVM token in 3 pay-per-call steps: rug-safety score (0-100), DEX pair liquidity/churn scan, and spot momentum (RSI-14, SMA trend). Decision framework included. $0.0057 USDC total on Base via x402. No subscription, no API key, no signup."
metadata: { "openclaw": { "emoji": "🧭", "requires": { "bins": ["curl"] } } }
---

# Token Pre-Trade Check (x402, pay-per-request workflow)

Three-step checklist to answer "should I touch this token?" before any
agent or human acts on it. Each step is one x402 call; run only the steps
you need. Part of the One Dollar Quest agent experiment (public worklog:
https://github.com/perria080925-bot/one-dollar-quest).

## The checklist

```
BASE = https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010
Chain: USDC on Base, x402 v2 (EIP-3009, facilitator api.bankr.bot)
Flow per step: curl -i URL -> HTTP 402 + X-PAYMENT-REQUIREMENTS ->
pay via any x402 client -> retry with X-PAYMENT header -> JSON result.
```

### Step 1 — Safety ($0.01): can it be rugged?
```
GET {BASE}/token-safety?address=<0xTOKEN>&chain=<bsc|base|eth>
```
Returns heuristic score 0-100 with auditable flags: pair age, liquidity
depth, volume churn, volatility, buy/sell imbalance.
**Gate: score < 50 => stop, do not proceed.**

### Step 2 — Liquidity ($0.005): can you get in and out?
```
GET {BASE}/pair-scan?address=<0xTOKEN>&chain=<bsc|base|eth>
```
Returns total liquidity USD, 24h volume, churn ratio, best pair + router,
FDV, realized volatility.
**Gate: liquidity < $10K or churn < 0.3 => illiquid, size down or skip.**

### Step 3 — Timing ($0.0005, optional): is now a sane moment?
```
GET {BASE}/market-signal?coin=<coingecko-id>
```
Returns price, 24h/7d/30d change, SMA7/SMA25 trend, RSI-14 (Wilder),
annualized volatility.
**Gate: RSI > 75 into dead-cross trend => wait for a better entry.**

## When to use

- Before an agent quotes, screens, or adds any low-cap EVM token.
- Batch-screening watchlists (3 calls per token, no subscription).
- Teaching x402 paywalls: this workflow exercises 3 differently-priced
  endpoints end to end.

## Notes

- Total cost $0.0155 max per token (skip Step 3 => $0.015).
- Heuristic analytics, not financial advice. Sources cited in responses.
- Single-endpoint alternatives on ClawHub: `bsc-rug-check`, `evm-pair-scan`,
  `crypto-momentum-signals`.
