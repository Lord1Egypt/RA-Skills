---
name: zapyeti
description: Use the ZapYeti API to list debts, track balances, view payoff schedules, log payments, and monitor debt-free progress via api.zapyeti.com. Use when the user asks about ZapYeti data, debt tracking, payoff progress, payment history, or debt plan management.
metadata: {"openclaw":{"emoji":"🏔️","primaryEnv":"ZAPYETI_API_KEY","requires":{"bins":["curl","python3"],"env":["ZAPYETI_API_KEY"]},"homepage":"https://zapyeti.com","source":"https://github.com/djedi/zapyeti"}}
---

# ZapYeti

Track and manage debt payoff plans on [ZapYeti.com](https://zapyeti.com) via REST API.

## Setup

- Requires env: `ZAPYETI_API_KEY`
- Generate an API key at ZapYeti.com → Settings → API Keys

## Usage

Use the helper script for all API calls:

```bash
scripts/zy_api.sh <METHOD> <path> [json_body]
```

### Common workflows

**List all debts:**
```bash
scripts/zy_api.sh GET /api/debts/
```

**Get a specific debt:**
```bash
scripts/zy_api.sh GET /api/debts/DEBT_ID
```

**Log a payment:**
```bash
scripts/zy_api.sh POST /api/payments/ \
  '{"debt_id":"DEBT_ID","amount":5000,"date":"2026-03-06"}'
```

**Payment summary:**
```bash
scripts/zy_api.sh GET /api/payments/summary
```

**Payment history:**
```bash
scripts/zy_api.sh GET /api/payments/history
```

**User profile:**
```bash
scripts/zy_api.sh GET /api/users/me
```

**Export data:**
```bash
scripts/zy_api.sh GET /api/settings/export
scripts/zy_api.sh GET /api/settings/export/csv
```

## API Reference

See `references/api.md` for the full endpoint list including debts, payments, SimpleFin sync, social features, and admin endpoints.

## Notes

- Amounts are in cents: $50.00 = 5000
- Debt payoff strategies: snowball (smallest first) and avalanche (highest interest first)
