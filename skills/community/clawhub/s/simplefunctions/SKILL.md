---
name: simplefunctions
description: SimpleFunctions — AI-native prediction market runtime for Kalshi & Polymarket. Thesis tracking, edge scanning, position monitoring, and trade execution via CLI. Also supports Telegram alerts for human users.
homepage: https://simplefunctions.dev
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["sf"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@spfunctions/cli",
              "bins": ["sf"],
              "label": "Install @spfunctions/cli (npm)",
            },
          ],
      },
  }
---

# SimpleFunctions

AI-native prediction market runtime. Track theses, scan for mispriced contracts on Kalshi and Polymarket, monitor positions, and trade — all through a single CLI built for agents.

**Setup**

```bash
npm install -g @spfunctions/cli
sf setup          # Interactive configuration wizard
```

Requires a SimpleFunctions account (free tier available at simplefunctions.dev).

---

## Core Commands

### Thesis Management

```bash
# List all theses
sf list

# Create a new thesis
sf create "Fed will cut rates by 50bps in Q2 2025"

# Get thesis context (primary command for agents)
sf context <thesis-id>

# Inject a signal into the thesis queue
sf signal <thesis-id> "CPI came in hotter than expected"

# Trigger deep evaluation
sf evaluate <thesis-id>
```

### Market Scanning

```bash
# Scan Kalshi for contracts matching a query (no auth required)
sf scan "oil prices"

# Top edges across all theses — what to trade right now
sf edges

# Explore public theses
sf explore
```

### Positions & Trading

```bash
# Show Kalshi positions with thesis edge overlay
sf positions

# Show resting orders
sf orders

# Account balance
sf balance

# Settled contracts with P&L
sf settlements
```

### Dashboard

```bash
# Terminal portfolio dashboard
sf dashboard
```

### Upcoming Events

```bash
# Kalshi calendar events
sf milestones

# Market distribution forecast (P50/P75/P90 history)
sf forecast <event-ticker>
```

---

## Telegram Alerts (Human Users)

Set up Telegram monitoring so SimpleFunctions can push confidence changes and alerts to your phone:

```bash
sf telegram --token YOUR_BOTFATHER_TOKEN
```

Then send `/start` in Telegram and the bot auto-detects your thesis.

---

## API Keys

- `SF_API_KEY` — SimpleFunctions API token (from simplefunctions.dev)
- `KALSHI_API_KEY_ID` + `KALSHI_PRIVATE_KEY_PATH` — for position/order data

Set via environment variables or `sf setup`.

---

## Notes

- All commands support `--json` for scripted/agentic use
- `sf agent <thesis-id>` launches interactive natural language mode
- No auth required for `sf scan` and `sf explore`
- Free plan includes 15M tokens; charge per token after that
