---
name: x402-cfo
description: Financial brain for x402 payments — budget enforcement, cost policies, spend analytics, anomaly detection, and audit trail for autonomous agents.
version: 0.2.0
author: x402-cfo
tags: [x402, payments, budget, finance, usdc, analytics, cfo, audit]
tools: [exec, read, write]
---

# x402-cfo Skill

You are an AI agent with financial awareness. You have access to x402-cfo, which gives you budget enforcement, cost policies, spend analytics, and anomaly detection for any x402 payment you make.

## Setup

Before using this skill, ensure x402-cfo is installed in the current project:

```bash
npm list x402-cfo 2>/dev/null || npm install x402-cfo
```

## How to use x402-cfo

When you need to make HTTP requests to x402-compatible paid APIs (any endpoint that returns HTTP 402), you MUST route the request through the AgentCFO instead of making raw fetch calls.

### Initialization

At the start of any session involving paid API calls, initialize the CFO:

```typescript
import { AgentCFO, JsonFileStorage } from 'x402-cfo';

const cfo = new AgentCFO({
  wallet: walletInstance, // Your x402-compatible wallet
  budget: {
    hourly: parseFloat(process.env.X402_BUDGET_HOURLY || '5'),
    daily: parseFloat(process.env.X402_BUDGET_DAILY || '50'),
    session: parseFloat(process.env.X402_BUDGET_SESSION || '200'),
  },
  policy: {
    maxPerRequest: parseFloat(process.env.X402_MAX_PER_REQUEST || '2.00'),
    allowedCurrencies: ['USDC'],
    allowedNetworks: (process.env.X402_NETWORKS || 'base').split(','),
    blocklist: (process.env.X402_BLOCKLIST || '').split(',').filter(Boolean),
  },
  storage: new JsonFileStorage('./x402-cfo-ledger.json'),
});
```

### Making paid requests

ALWAYS use `cfo.fetch()` instead of raw `fetch()` for any x402 endpoint:

```typescript
const response = await cfo.fetch('https://api.paid-service.com/v1/data');
```

The CFO will automatically:
1. Check if the URL passes your cost policies
2. Check if you have remaining budget
3. Pay the x402 challenge if approved
4. Log the payment to the audit ledger
5. Fire events if spending is getting hot

### Before committing to expensive operations

Check if you can afford it:

```typescript
const estimate = cfo.estimateCost('https://api.paid-service.com/v1/data');
// → { average: 0.25, min: 0.20, max: 0.35, samples: 47 }

const budget = cfo.spent();
// → { sessionSpent: "4.25", hourlyRemaining: "0.75", dailyRemaining: "45.75" }
```

### When the user asks about spending

Provide a financial summary:

```typescript
const summary = cfo.summary();
// → { totalSpent, burnRatePerMinute, projectedDaily, topEndpoints, currencyBreakdown }

const audit = cfo.audit();
// → Full ledger: every payment decision with timestamp, amount, URL, status, reason
```

### Reacting to financial events

Wire alerts so you can adapt your behavior:

```typescript
cfo.events.on('budget:warning', ({ window, percentUsed }) => {
  // Budget is running low — reduce spending or ask the user
});

cfo.events.on('budget:exhausted', ({ window }) => {
  // No budget left in this window — stop making paid requests
});

cfo.events.on('velocity:spike', ({ multiplier }) => {
  // Spending is abnormally fast — slow down or alert the user
});
```

## Key rules

1. **Never bypass the CFO.** All x402 payments go through `cfo.fetch()`.
2. **Check budget before expensive operations.** Use `cfo.spent()` and `cfo.estimateCost()`.
3. **Report spending when asked.** Use `cfo.summary()` for high-level stats, `cfo.audit()` for the full ledger.
4. **Respect budget exhaustion.** When a `budget:exhausted` event fires, stop making paid requests and inform the user.
5. **React to velocity spikes.** When spending is 2x+ above average, slow down and assess.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `X402_BUDGET_HOURLY` | `5` | Maximum spend per hour (USDC) |
| `X402_BUDGET_DAILY` | `50` | Maximum spend per day (USDC) |
| `X402_BUDGET_SESSION` | `200` | Maximum spend per session (USDC) |
| `X402_MAX_PER_REQUEST` | `2.00` | Maximum spend per single request (USDC) |
| `X402_NETWORKS` | `base` | Comma-separated allowed networks |
| `X402_BLOCKLIST` | `` | Comma-separated blocked domains |
