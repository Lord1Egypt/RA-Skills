---
name: snaptrade-trading
description: >
  Execute trades and retrieve account data via the SnapTrade API using the
  snaptrade-python-sdk. Use this skill whenever OpenClaw needs to place a buy
  or sell order, check account balances, get current positions, retrieve order
  history, fetch symbol quotes, cancel an open order, or refresh account
  holdings through SnapTrade. Triggers on any trading action or account data
  request routed through SnapTrade — even if the user just says "buy X shares",
  "what's my balance", "check my positions", "cancel that order", or "did my
  trade go through". Always use this skill when brokerage account interaction
  of any kind is needed.
credentials:
  - name: SNAPTRADE_CLIENT_ID
    description: SnapTrade partner client ID. Used to authenticate all API requests. Treat as sensitive.
    required: true
  - name: SNAPTRADE_CONSUMER_KEY
    description: SnapTrade partner consumer key. Used to sign all API requests. Treat as sensitive — do not share or log.
    required: true
  - name: SNAPTRADE_USER_ID
    description: SnapTrade user ID for the connected brokerage user. Grants access to that user's account data and trading permissions.
    required: true
  - name: SNAPTRADE_USER_SECRET
    description: SnapTrade user secret for the connected brokerage user. Acts as a per-user API key. Treat as sensitive — rotate via SnapTrade dashboard if compromised.
    required: true
warnings:
  - This skill can place real trades and cancel orders on connected brokerage accounts.
  - Default to requiring user confirmation per trade. Automated mode is supported if explicitly configured — enforce symbol allowlists, notional caps, position limits, and daily loss limits before enabling.
  - Use paper trading or a low-limit account during testing.
  - Store credentials in a .env file or secret manager — never hardcode, log, or pass them through untrusted channels.
  - Rotate SNAPTRADE_USER_SECRET immediately via the SnapTrade dashboard if there is any chance it was exposed.
  - Prefer a dedicated SnapTrade user with limited brokerage permissions for automated trading rather than using your primary account credentials.
compatibility:
  - python >= 3.8
  - snaptrade-python-sdk == 11.0.187
  - python-dotenv == 1.2.2
  - Run scripts/setup.sh before first use
---

# SnapTrade Trading Skill

SnapTrade connects OpenClaw to the user's brokerage (IBKR, Questrade, Alpaca,
and more) through a unified API. This skill handles all account data retrieval
and order execution. For market price data and OHLCV bars, use the
`massive-data-feed` skill — SnapTrade does not provide chart data.

---

## Setup

Run once before first use:
```bash
bash scripts/setup.sh
source .venv-snaptrade/bin/activate
```

See `README.md` for full onboarding — how to get credentials, register a user,
and connect a brokerage account.

---

## SDK Initialization

Always run this first before any other call:

```python
import os
from snaptrade_client import SnapTrade

snaptrade = SnapTrade(
    consumer_key=os.environ["SNAPTRADE_CONSUMER_KEY"],
    client_id=os.environ["SNAPTRADE_CLIENT_ID"],
)
user_id = os.environ["SNAPTRADE_USER_ID"]
user_secret = os.environ["SNAPTRADE_USER_SECRET"]
```

---

## What to do next — read the right reference file

Each reference file covers one domain. Read only what you need.

| Task | Reference file |
|---|---|
| Get accounts, balances, positions, orders, historical value | `references/account-data.md` |
| Resolve a ticker to a symbol ID + get quotes | `references/symbol-resolution.md` |
| Place an equity trade (limit, market, bracket) | `references/place-orders.md` |
| Place an options order (single or multi-leg) | `references/options-trading.md` |
| Place a crypto order | `references/crypto-trading.md` |
| Cancel an order or refresh holdings | `references/cancel-refresh.md` |
| Get historical transactions / activity log | `references/historical-data.md` |

---

## Key constraints to keep in mind

- `trade_id` from an impact check expires in **5 minutes** — place the order immediately after getting it, don't do other work in between
- SnapTrade does **not** provide OHLCV or price history — use `massive-data-feed` for that
- Not all brokerages support trading — some are data-only connections
- Always resolve symbol IDs fresh — don't cache them long term, they can change
- After any order placement or cancellation, trigger a manual refresh so the account state stays current (see `references/cancel-refresh.md`)
