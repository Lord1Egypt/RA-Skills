---
name: riskstate
version: 1.4.0
description: Pre-trade risk API for crypto trading agents. Returns exposure limits, allowed actions, and policy constraints for BTC/USD and ETH/USD from 30+ real-time signals. Spot, perpetual futures (perps), and DeFi borrowing aware.
category: risk-management
auth: bearer-token
env: RISKSTATE_API_KEY
endpoint: POST https://api.riskstate.ai/v1/risk-state
assets: [BTC, ETH]
refresh: 60s cache, recommend 5min polling
homepage: https://riskstate.ai
docs: https://riskstate.ai/docs/api
repository: https://github.com/likidodefi/riskstate-docs
tags: [crypto, ai, bitcoin, trading, ethereum, trading-bot, agents, policy-engine, ai-agents, defi, decentralized-finance, ai-trading, agent-skills, defi-risk-management, risk-governance, skills-sh, perpetual-futures, perps, spot-trading, btc-usd, eth-usd]
pricing: free-beta
author: RiskState
license: proprietary
---

# RiskState — Pre-Trade Risk Layer for Crypto

## What it does

Returns **dynamic risk permissions** for BTC/USD and ETH/USD before capital is deployed.
A deterministic policy engine computes how much exposure is allowed based on 30+ real-time signals across macro, on-chain, derivatives, and DeFi health. Applicable to **spot**, **perpetual futures (perps)**, and **DeFi borrowing**.

The response tells you:
- **max_size_fraction**: Maximum exposure as fraction of portfolio (0.0–1.0). For spot: amount to deploy. For perps: max notional exposure (divide by your leverage for margin).
- **allowed_actions / blocked_actions**: What MAY and MUST NOT be done (enum tokens)
- **risk_flags**: Structural blockers (hard stop) vs contextual risks (reduce conviction)
- **binding_constraint**: Which cap is limiting and why
- **policy_level**: 1–5 summary label (informational — use `exposure_policy` for enforcement)

## What it does NOT do

- No trade signals, no entry/exit prices, no predictions
- No portfolio allocation advice
- No order execution or routing
- No historical data or backtesting

This is a **risk governor**, not a trading oracle. The assessment is USD-denominated.

## When to call

- **Before opening or sizing positions** — check permissions first
- **Periodically during holds** — every 5 min for active trading, every 4h for holding
- **After significant market moves** — cache invalidates after 60s (`ttl_seconds` in response)

## Authentication

Request a free API key at [https://riskstate.ai](https://riskstate.ai) (email only). You will receive a key with the `rs_live_` prefix. Set it as the `RISKSTATE_API_KEY` environment variable and pass it as a Bearer token:

```
Authorization: Bearer $RISKSTATE_API_KEY
```

## Binding precedence

When consuming the response, agents MUST evaluate fields in this order:

1. `risk_flags.structural_blockers` — if non-empty, ABORT new entries
2. `exposure_policy.blocked_actions` — actions the agent MUST NOT take
3. `exposure_policy.reduce_recommended` — reduce exposure if true
4. `exposure_policy.max_size_fraction` — maximum position size
5. `exposure_policy.max_leverage` — maximum leverage allowed
6. `exposure_policy.direction_bias` — preferred trade direction
7. `policy_level` — informational summary only, do not use for enforcement

## Decision rules by policy level

| `policy_level` | Summary | Key constraints |
|----------------|---------|-----------------|
| 1 (BLOCK Survival) | No new positions | `blocked_actions: [NEW_TRADES, ...]`, `max_leverage: "0x"` |
| 2 (BLOCK Defensive) | Wait or hedge only | `blocked_actions: [AGGRESSIVE_LONG, ...]`, `max_leverage: "1x"` |
| 3 (CAUTIOUS) | DCA with R:R >2:1 | `blocked_actions: [LEVERAGE, ALL_IN, ...]`, `max_leverage: "1x"` |
| 4 (GREEN Selective) | Trade with confirmation | `max_leverage: "1.5x"` |
| 5 (GREEN Expansion) | Full operations | `max_leverage: "2x"` |

`policy_level` is a convenience label. Always check `exposure_policy` fields for actual constraints.

## Failure modes

| Condition | Agent behavior |
|-----------|----------------|
| `stale_fields` contains core indicators (price, funding, rsi) | Downgrade conviction. Data integrity compromised. |
| `data_quality_score` < 70 | Treat as degraded. Reduce position sizes by 50%. |
| `data_quality_score` < 50 | Treat as unreliable. Do not open new positions. |
| `confidence_score` < 0.5 | Signals conflict heavily. Prefer WAIT over action. |
| HTTP 500 or timeout | Assume worst case (BLOCK). Retry after 60s. |
| `cached: true` + `stale_fields` non-empty | Re-request after cache TTL (60s) for fresh data. |

## Security

**API host**: All API calls go to `https://api.riskstate.ai` (the `/v1/*` endpoints). The `https://riskstate.ai` domain is the landing page only — no API endpoints are served there.

**API keys**: All keys have the `rs_live_` prefix and are rate-limited to 60 req/min. Store your key in the `RISKSTATE_API_KEY` environment variable. Do not hardcode keys in source code.

## Example requests

### Minimal (BTC)

```bash
curl -X POST https://api.riskstate.ai/v1/risk-state \
  -H "Authorization: Bearer $RISKSTATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asset": "BTC"}'
```

### Detailed (with scoring breakdown)

```bash
curl -X POST https://api.riskstate.ai/v1/risk-state \
  -H "Authorization: Bearer $RISKSTATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asset": "BTC", "include_details": true}'
```

### DeFi monitoring (with wallet)

```bash
curl -X POST https://api.riskstate.ai/v1/risk-state \
  -H "Authorization: Bearer $RISKSTATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asset": "ETH", "wallet": "0xYOUR_WALLET_ADDRESS", "include_details": true}'
```

## Example response (minimal)

```json
{
  "exposure_policy": {
    "max_size_fraction": 0.42,
    "leverage_allowed": false,
    "max_leverage": "1x",
    "direction_bias": "LONG_PREFERRED",
    "reduce_recommended": false,
    "allowed_actions": ["DCA", "WAIT", "LIGHT_ACCUMULATION", "RR_GT_2"],
    "blocked_actions": ["LEVERAGE", "AGGRESSIVE_LONG", "ALL_IN"]
  },
  "tactical_state": "LEAN BULL",
  "structural_state": "MID",
  "macro_state": "NEUTRAL",
  "market_regime": "TREND",
  "volatility_regime": "NORMAL",
  "policy_level": 3,
  "confidence_score": 0.72,
  "data_quality_score": 85,
  "binding_constraint": {
    "source": "MACRO",
    "reason": "NEUTRAL × NORMAL",
    "reason_codes": ["MACRO_NEUTRAL", "COUPLING_NORMAL"],
    "cap_value": 0.70
  },
  "risk_flags": {
    "structural_blockers": [],
    "context_risks": ["HIGH_FUNDING"]
  },
  "defi": null,
  "policy_hash": "a1b2c3d4e5f6...",
  "scoring_version": "score_v2",
  "version": "1.2.2",
  "timestamp": "2026-03-13T14:30:00.000Z",
  "asset": "BTC",
  "cached": false,
  "ttl_seconds": 60,
  "stale_fields": []
}
```

## Detailed response

Pass `"include_details": true` in the request body to receive expanded scoring data (composite subscores, positioning intelligence, whale pressure, trend strength, caps breakdown). All minimal fields are included plus: `caps`, `positioning`, `volatility`, `whale_pressure`, `trend_strength`, `composite`, `extreme_scores`, `macro_detail`, `data_sources`, and `core_missing`.

See [docs/api-v1.md](docs/api-v1.md) for full API documentation including all field types, ranges, action enums, risk flags reference, and interpretation guide.
