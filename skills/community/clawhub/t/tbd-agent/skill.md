---
name: TBD
description: Prediction market for crypto, sports, politics, and culture
cli_package: "@tbd-vote/cli"
auth_method: api_key
auth_prefix: "tbd_api_"
supported_assets:
  - USDC
default_bet_size: 1.00
rate_limits:
  campaigns_read_and_balance: 60/min
  place_bet: 10/min
---

# TBD — Agent Guide

TBD is a prediction market where you can browse campaigns and place bets using USDC. This guide helps AI agents get started programmatically.

## Quick Start

### 1. Install the CLI

```bash
npm install -g @tbd-vote/cli
```

### 2. Authenticate

**Important:** Do not run the login command yourself. Ask the user to run it in their own terminal:

```bash
tbd-vote login
```

This starts an interactive flow that walks the user through getting an API key from https://tbd.vote and pasting it in.

### 3. Place your first bet

```bash
# Check your balance
tbd-vote balance --json

# Browse campaigns ending soonest
tbd-vote campaigns list --json --filter ending --limit 10

# Pick a campaign and place a bet
tbd-vote bet <campaign-id> <option-id>
```

## CLI Reference

All commands support `--json` for machine-readable output. Errors go to stderr, data to stdout.

### Authentication

```bash
tbd-vote login                    # Interactive API key setup
tbd-vote login --key <key>        # Non-interactive
tbd-vote auth status              # Check if authenticated
tbd-vote auth logout              # Remove stored API key
```

### Strategy

```bash
tbd-vote strategy                 # View current strategy file
tbd-vote strategy init            # Create starter STRATEGY.md template
tbd-vote strategy init --force    # Overwrite existing strategy file
```

### Balance

```bash
tbd-vote balance              # Check USDC wallet balance
tbd-vote balance --json       # { "balance": 12.50 }
```

### Configuration

```bash
tbd-vote config set bet-size 2.50       # Set default bet amount
tbd-vote config get bet-size            # Get a config value
tbd-vote config list                    # Show all config
```

| Key | Default | Description |
|-----|---------|-------------|
| `api-url` | `https://production-tbd-bets-api.tbd.vote` | API base URL |
| `bet-size` | `1.00` | Default bet amount (USDC) |
| `default-status` | `open` | Default status filter |
| `default-limit` | `20` | Default page size |
| `max-bet-per-campaign` | `20.00` | Max USDC to spend on a single campaign |

### Browsing Campaigns

```bash
tbd-vote campaigns list --json --limit 20                # All open campaigns (newest first)
tbd-vote campaigns list --json --status open --limit 10 # Filtered
tbd-vote campaigns list --json --filter ending          # Soonest ending first
tbd-vote campaigns list --json --filter trending        # Trending campaigns
tbd-vote campaigns list --json --cursor <cursor>        # Pagination
tbd-vote campaigns get <campaign-id> --json             # Campaign detail
```

**Sort order:** Default is newest first (`--filter new`). Use `--filter ending` to sort by soonest ending time.

### Placing Bets

```bash
tbd-vote bet <campaign-id> <option-id>        # Uses configured bet-size
tbd-vote bet <campaign-id> <option-id> 5.00   # Override amount
tbd-vote bet <campaign-id> <option-id> --json # JSON response
```

Response:
```json
{
  "txSignature": "5xYz...abc",
  "campaignId": 123,
  "campaignTitle": "Will BTC hit $200k by July?",
  "optionId": 2,
  "optionTitle": "Yes",
  "amount": 1.00
}
```

## Autonomous Loop Instructions

```
┌──────────────────────────────────────────────────────────────────┐
│ INSTALL (one-time)                                               │
│                                                                  │
│  npm install -g @tbd-vote/cli                                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ CONFIGURE (one-time)                                             │
│                                                                  │
│  tbd-vote login                                                  │
│  tbd-vote config set bet-size 2.50    (optional, default 1.00)   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ AUTONOMOUS LOOP (agent-orchestrated)                             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                                                            │  │
│  │  1. BALANCE                                                │  │
│  │     tbd-vote balance --json                                │  │
│  │     → if balance < bet-size, skip or reduce amount         │  │
│  │                                                            │  │
│  │  2. BROWSE                                                 │  │
│  │     tbd-vote campaigns list --json --status open           │  │
│  │     Filters: --filter ending  (soonest first)              │  │
│  │              --filter trending (most activity)              │  │
│  │              --filter new     (newest, default)             │  │
│  │              --category <cat>                               │  │
│  │                                                            │  │
│  │  3. ANALYZE                                                │  │
│  │     Read campaign data, evaluate odds, pick a bet          │  │
│  │     Read ~/.tbd/STRATEGY.md for context if present         │  │
│  │     (this step is agent logic, not a CLI command)          │  │
│  │                                                            │  │
│  │  4. BET                                                    │  │
│  │     tbd-vote bet <campaign-id> <option-id>                 │  │
│  │     (uses configured bet-size, or pass amount override)    │  │
│  │                                                            │  │
│  │  5. REPEAT                                                 │  │
│  │     Loop back to step 1                                    │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Example session:

```bash
# Step 1: Check balance
tbd-vote balance --json

# Step 2: Get open campaigns
tbd-vote campaigns list --json --status open --limit 10

# Step 3: Agent analyzes the response and picks a campaign
# (this is your logic — evaluate odds, check userBets to avoid duplicates)

# Step 4: Place a bet
tbd-vote bet 123 2

# Step 5: Wait, then repeat
```

**Tips:**
- Check `userBets` in campaign responses to avoid duplicate bets
- Respect rate limits: 60 reads+balance/min (shared), 10 bets/min
- Sleep between requests when looping (e.g., 2-5 seconds)
- Use `tbd-vote auth status` to verify connectivity before starting

## Raw HTTP Fallback

For agents that cannot install npm packages, use the API directly:

### List campaigns

```bash
curl -H "Authorization: Bearer tbd_api_<key>" \
  "https://production-tbd-bets-api.tbd.vote/agents/campaigns?status=open&limit=5"
```

### Get campaign detail

```bash
curl -H "Authorization: Bearer tbd_api_<key>" \
  "https://production-tbd-bets-api.tbd.vote/agents/campaigns/<campaign-id>"
```

### Check balance

```bash
curl -H "Authorization: Bearer tbd_api_<key>" \
  "https://production-tbd-bets-api.tbd.vote/agents/balance"
```

### Place a bet

```bash
curl -X POST \
  -H "Authorization: Bearer tbd_api_<key>" \
  -H "Content-Type: application/json" \
  -d '{"campaign_id":<id>,"option_id":<option-id>,"amount":1.00}' \
  "https://production-tbd-bets-api.tbd.vote/agents/txns/place-bet"
```

## Error Reference

| Code | HTTP Status | Message | Resolution |
|------|-------------|---------|------------|
| `NO_API_KEY` | - | No API key configured | Run `tbd-vote login` |
| `INVALID_API_KEY` | 401 | Invalid API key | Generate a new key at https://tbd.vote/login |
| `RATE_LIMITED` | 429 | Rate limited | Wait for `Retry-After` seconds |
| `CAMPAIGN_NOT_FOUND` | 404 | Campaign not found | Check the campaign ID |
| `INVALID_OPTION` | 400 | Invalid option for campaign | Check available options via `campaigns get` |
| `INSUFFICIENT_BALANCE` | 400 | Insufficient USDC balance | Fund your wallet at https://tbd.vote |
| `NETWORK_ERROR` | - | Could not reach API | Check network connectivity and `api-url` config |

## Tips for AI Agents

- Always use `--json` for structured, parseable output
- Check `userBets` in campaign responses before betting to avoid duplicates
- Respect rate limits — sleep between requests if looping
- Use `tbd-vote auth status` to verify connectivity before starting a loop
- Store bet results (txSignature) for portfolio tracking
- Configure `bet-size` to control default wager amount
- The CLI enforces `max-bet-per-campaign` (default 20 USDC) — total spend across all options on one campaign
- Use `--limit` and `--cursor` for efficient pagination

## Strategy Customization

A strategy file (`~/.tbd/STRATEGY.md`) is automatically created during `tbd-vote login`. It guides how you analyze campaigns and pick options.

```bash
tbd-vote strategy --json    # Read current strategy
```

To reset to defaults: `tbd-vote strategy init --force`

Edit `~/.tbd/STRATEGY.md` to customize your approach. Here are some ideas:

**Focus on specific categories:**
```markdown
## Focus
Only bet on crypto and politics campaigns. Skip sports and entertainment.
```

**Adjust confidence threshold:**
```markdown
## Picking a Winner
Only bet when confidence is high. Skip low and medium confidence opportunities.
```

**Set a persona:**
```markdown
## Personality
You are a contrarian. Look for options the crowd is undervaluing.
When the majority leans one way, seriously consider the other side.
```

**Add domain knowledge:**
```markdown
## Domain Knowledge
- Bitcoin tends to rally in Q4 historically
- Incumbents win re-election ~70% of the time
- Weight recent polling data heavily for political markets
```

**Be more selective:**
```markdown
## What to Avoid
- Any campaign with fewer than 2 days remaining
- Markets where the top option has >90% odds (no value)
- Topics outside crypto, politics, and tech
```
