---
name: questrade
description: Query a Questrade brokerage account and Canadian/US market data via the Questrade REST API. Use for account info (balances, positions, orders, executions, activities), Level 1 market quotes, historical OHLCV candles, and symbol search. Use when the user asks about their Questrade portfolio, Canadian/US stock prices, wants to check orders or executions, or search for a ticker. Note: personal API tokens are read-only — order placement requires Questrade partner access.
---

# Questrade Skill

Interact with a Questrade brokerage account and Canadian/US market data via
the [Questrade REST API](https://www.questrade.com/api/documentation/getting-started).

## Setup

### 1. Activate API Access

Log in to Questrade → **App Hub** → **API Centre** → **Activate API**.
Generate a **manual authorization token** (this is your initial refresh token,
valid for 7 days).

### 2. Store Credentials

**Option A — environment variables (recommended):**

```bash
export QUESTRADE_REFRESH_TOKEN="paste-your-token-here"
export QUESTRADE_PRACTICE="false"    # "true" for a practice account
export QUESTRADE_READ_ONLY="true"    # "true" to block order placement/cancellation
```

**Option B — credentials file (`~/.openclaw/credentials/questrade.json`):**

```json
{
  "refreshToken": "paste-your-token-here",
  "practice": false,
  "readOnly": true
}
```

> **Important:** Questrade refresh tokens *rotate* — every time the token is
> used to obtain a new access token, Questrade issues a new refresh token.
> This script automatically saves the new refresh token back to the credentials
> file, so you only need to paste the initial token once.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install requests
```

---

## Quick Reference

### Server Time

```bash
python3 scripts/questrade_cli.py time
```

### Accounts

```bash
python3 scripts/questrade_cli.py accounts
```

### Balances

```bash
python3 scripts/questrade_cli.py balances 12345678
```

### Positions

```bash
python3 scripts/questrade_cli.py positions 12345678
```

### Orders

```bash
# Open orders (default)
python3 scripts/questrade_cli.py orders 12345678

# All orders in a date range
python3 scripts/questrade_cli.py orders 12345678 --state All --start 2026-01-01 --end 2026-03-01

# Closed orders
python3 scripts/questrade_cli.py orders 12345678 --state Closed
```

### Order Detail

```bash
python3 scripts/questrade_cli.py order-detail 12345678 987654321
```

### Executions

```bash
python3 scripts/questrade_cli.py executions 12345678
python3 scripts/questrade_cli.py executions 12345678 --start 2026-01-01 --end 2026-02-28
```

### Account Activities

```bash
# Max 30-day window; --end defaults to today if omitted
python3 scripts/questrade_cli.py activities 12345678 --start 2026-02-01
python3 scripts/questrade_cli.py activities 12345678 --start 2026-02-01 --end 2026-02-28
```

### Symbol Search

```bash
# Search by ticker prefix
python3 scripts/questrade_cli.py symbol-search SHOP

# Search by company name
python3 scripts/questrade_cli.py symbol-search "Royal Bank"
```

> **Note:** Questrade market data endpoints use integer **symbol IDs**, not
> ticker strings.  Always run `symbol-search` first to get the correct ID
> before calling `quote` or `candles`.

### Symbol Info

```bash
# Full metadata for a symbol (by Questrade ID)
python3 scripts/questrade_cli.py symbol-info 8049
```

### Level 1 Quotes

```bash
# Single symbol
python3 scripts/questrade_cli.py quote 8049

# Multiple symbols (comma-separated IDs)
python3 scripts/questrade_cli.py quote 8049,38738,45340
```

### Historical Candles (OHLCV)

```bash
# Daily candles for the past month
python3 scripts/questrade_cli.py candles 8049 --start 2026-02-01

# Hourly candles for a specific range
python3 scripts/questrade_cli.py candles 8049 --start 2026-01-01 --end 2026-02-01 --interval OneHour

# Available intervals:
# OneMinute, TwoMinutes, ThreeMinutes, FourMinutes, FiveMinutes,
# TenMinutes, FifteenMinutes, TwentyMinutes, HalfHour,
# OneHour, TwoHours, FourHours, OneDay, OneWeek, OneMonth, OneYear
```

### Markets

```bash
python3 scripts/questrade_cli.py markets
```

### Place Order *(partner API access required)*

```bash
# Market order
python3 scripts/questrade_cli.py order buy 12345678 8049 10 Market

# Limit order
python3 scripts/questrade_cli.py order buy 12345678 8049 10 Limit --limit-price 145.50

# Stop-limit order
python3 scripts/questrade_cli.py order sell 12345678 8049 5 StopLimit --stop-price 140.00 --limit-price 139.50

# Skip confirmation prompts
python3 scripts/questrade_cli.py order buy 12345678 8049 10 Market --force
```

**Order Guardrails:**

1. **Live quote fetch** — retrieves current bid/ask before submitting
2. **Price sanity check** — warns if buy limit > ask or sell limit < bid
3. **Order summary** — shows notional cost and requires `y/n` confirmation
4. Use `--force` to skip all prompts (automated use only)

> **Note:** Order placement and cancellation require Questrade *partner*
> API access.  Personal API tokens are read-only (GET requests only).

### Cancel Order

```bash
python3 scripts/questrade_cli.py cancel-order 12345678 987654321
```

---

## Workflow: Finding a Symbol and Getting a Quote

Because Questrade quotes use integer IDs rather than tickers, the typical
two-step flow is:

```bash
# Step 1: Find the symbol ID
python3 scripts/questrade_cli.py symbol-search AAPL

# Step 2: Use the ID from the output
python3 scripts/questrade_cli.py quote 8049
```

---

## Script Location

All commands use: `scripts/questrade_cli.py` (relative to this skill directory)

## API Reference

See `references/api.md` for full endpoint documentation and response schemas.

## Known Limitations

- **Level 1 quotes and candles** (`quote`, `candles`) may return `403 out of allowed OAuth scopes` if your Questrade account does not have a market data subscription or the token was not generated with market data scope enabled. Account data commands (`accounts`, `balances`, `positions`, `orders`, `executions`, `activities`) work with all personal tokens.
- **Activities** endpoint has a maximum window of **30 days** — always provide both `--start` and `--end`. If `--end` is omitted it defaults to today.

## Safety Notes

- **Personal API tokens cannot place trades.** Questrade restricts order placement
  and cancellation (`POST`/`DELETE /accounts/{id}/orders`) to partner-level API
  access only. Attempting either with a personal token returns `403 Forbidden`.
- The `order` and `cancel-order` commands are included for completeness but will
  not work unless you have Questrade partner API access.
- The refresh token rotates on every use; do **not** share the credentials file.
- Access tokens expire in ~30 minutes; the script caches and refreshes them automatically.

