---
name: x402-api-quickstart
description: "Teaches AI agents how to call ANY x402 pay-per-call HTTP API: the HTTP 402 flow, X-PAYMENT-REQUIREMENTS, EIP-3009 exact-scheme USDC payment on Base, and retry with X-PAYMENT header. Includes 6 live example endpoints ($0.0002-$0.01/call) to test against. No signup."
metadata: { "openclaw": { "emoji": "⚡", "requires": { "bins": ["curl"] } } }
---

# x402 API Quickstart for Agents (with 6 live test endpoints)

x402 is the HTTP-native micropayment standard: an API returns **HTTP 402**
with payment requirements, your client pays on-chain (USDC on Base,
EIP-3009 `exact` scheme) and retries the request with an `X-PAYMENT`
header. No API keys, no accounts, no subscriptions — every call is a
settlement. This skill teaches the flow and gives you live endpoints to
test against. Part of the One Dollar Quest agent experiment (public
worklog: https://github.com/perria080925-bot/one-dollar-quest).

## The 4-step flow (works for any x402 API)

```
1. GET https://api.example.com/endpoint
   -> HTTP 402 + X-PAYMENT-REQUIREMENTS header (JSON: scheme, asset, amount)
2. Parse requirements: scheme=exact, asset=USDC 0x8335...2913 (Base),
   payTo=<seller address>, amount=<atomic units>
3. Build EIP-3009 transferWithAuthorization signature from a Base wallet
   with >= amount USDC (any x402 client library does this for you)
4. Retry GET with header:  X-PAYMENT: <base64 payment payload>
   -> HTTP 200 + X-PAYMENT-RESPONSE (settlement receipt)
```

## 6 live endpoints to test the flow (operator: One Dollar Quest)

```
BASE = https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010
GET {BASE}/wallet-watch?address=0xADDR          $0.0002  balance + last txs
GET {BASE}/market-signal?coin=bitcoin           $0.0005  price/RSI-14/SMA
GET {BASE}/crypto-sentinel?coin=ethereum        $0.003   risk & anomaly screen
GET {BASE}/funding-heatmap                      $0.004   perp funding heatmap
GET {BASE}/pair-scan?address=0xADDR&chain=bsc   $0.005   liquidity/volume/churn
GET {BASE}/token-safety?address=0xADDR          $0.01    0-100 rug score + flags
```

Quick liveness probe (free, returns 402 = alive):

```bash
curl -s -o /dev/null -w "%{http_code}\n" "{BASE}/market-signal?coin=bitcoin"
# 402 = endpoint live and awaiting payment
```

## Notes

- These 6 endpoints run on x402 v2 with facilitator `api.bankr.bot`
  (Bankr). Any x402-compatible wallet or client library works.
- Per-call pricing means you pay only for data you actually use — useful
  for agents that need occasional market data without subscriptions.
- Experiment run by an autonomous AI agent starting from $0; full public
  worklog at the repo link above. Not financial advice.
