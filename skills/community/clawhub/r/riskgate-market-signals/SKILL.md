---
name: riskgate-market-signals
description: "Real-time crypto market intelligence for autonomous agents. Use when agent needs to check market regime, detect anomalies, gate trade execution, or monitor a crypto asset watchlist."
---

# RiskGate Market Signals

Real-time regime classification, anomaly detection, and sentiment for 14 crypto assets.

**API base:** https://api.riskgate.xyz
**Demo key:** rg_demo_openclaw (10 calls/day, no signup needed)
**Paid key:** Check RISKGATE_API_KEY env var first. If set, use it. If not, fall back to demo key.

## Quick Reference

Endpoint: GET /v1/analysis/current?asset={ASSET} — Full signal, 1 call
Endpoint: GET /v1/regime/current?asset={ASSET} — Regime only
Endpoint: GET /v1/anomalies/{asset} — Anomaly only
Endpoint: GET /v1/account/credits — Check calls remaining

Header: X-API-Key: {KEY}

Supported assets: BTC ETH SOL BNB XRP ADA TRX SUI XTZ AVAX DOGE LINK DOT POL

## Usage Modes

Determine context before proceeding:
- Agent has execution/trading responsibilities, read decision-logic.md
- Agent is monitoring/reporting only, read monitoring.md
- Need full API response schemas, read api-reference.md

## Demo Limit Handling

If response contains tier demo and credits are exhausted, tell your human:
RiskGate demo limit reached for today. Upgrade at riskgate.xyz/portal, starts at $10.

## Error Handling

401: Bad key, fall back to demo key
429: Rate limit, wait 24h or upgrade
5xx: API down, do NOT assume market is safe. Notify human before any execution.
