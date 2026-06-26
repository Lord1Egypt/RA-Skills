---
name: aionmarket-trading
description: Trades a market when your estimated probability diverges from the live market price, with dry-run by default, context checks, reasoning tags, and optional live execution through AION.
metadata:
    author: "Saul Su"
    version: "1.0.0"
    displayName: "AION Market Divergence Trader"
    difficulty: "intermediate"
---

# AION Market Divergence Trader

This skill is a publishable trading template for AION Market. It compares your probability estimate with the live market price, checks market context, and only places a trade when the edge clears a configurable threshold.

> **This is a template.** The default signal is probability divergence: if your model thinks the event is more likely than the market implies, the skill buys YES; if less likely, it buys NO. Remix the signal source with your own model, API, or research process. The skill handles trade discipline, operator output, and AION trade tagging.

## When To Use

Use this skill when an agent already has a probability estimate for a specific market and needs a safe execution wrapper around that signal.

## Skill Folder

This skill ships with three files:

- SKILL.md
- clawhub.json
- divergence_trader.py

## Defaults

- Venue: polymarket
- Trade size: 5.0
- Minimum edge: 0.05
- Execution mode: dry-run unless `--live` is passed
- Trade source: `sdk:aionmarket-trading`
- Skill slug: `aionmarket-trading`

## Required Inputs

The skill expects:

- `AION_API_KEY` or `AIONMARKET_API_KEY`
- `MARKET_ID` for the target market
- `MY_PROBABILITY` as a decimal between `0` and `1`

Optional inputs:

- `VENUE` such as `polymarket` or `kalshi`
- `TRADE_SIZE`
- `MIN_EDGE`
- `REASONING_PREFIX`

## Safety Rules

1. Always fetch market context before deciding.
2. Always default to dry-run. Live trading requires explicit `--live`.
3. Always attach `source`, `skill_slug`, and human-readable `reasoning`.
4. Skip trading when context reports warnings or flip-flop risk.
5. Return `HOLD` when the edge is smaller than the configured threshold.

## Decision Logic

1. Read the live market probability from market context.
2. Compute `edge = my_probability - market_probability`.
3. If `edge >= min_edge`, buy YES.
4. If `edge <= -min_edge`, buy NO.
5. Otherwise hold.

## Example Commands

Dry-run:

```bash
python divergence_trader.py --market-id 12345 --my-probability 0.62
```

Live trade:

```bash
python divergence_trader.py --market-id 12345 --my-probability 0.62 --amount 5 --live
```

## Expected Operator Output

The script prints an operator-style summary:

```text
Skill: aionmarket-trading
Venue: polymarket
Risk alerts:
- none

Decision:
- MARKET_ID: TRADE YES size=5.0 reason=edge +7.0%
```

## Remix Ideas

- Replace `MY_PROBABILITY` with a forecast model output.
- Drive `MARKET_ID` from a market scanner.
- Add portfolio-aware sizing before the trade call.
- Extend the loop to poll with jitter and auto-redeem resolved positions.
    key=private_key,
    chain_id=137,
)
creds = polymarket.create_or_derive_api_creds()
wallet = polymarket.get_address()

print(f"Wallet: {wallet}")
print(f"CLOB API Key: {creds.api_key}")

# 2. Register with AION Market
check = client.check_wallet_credentials(wallet)
if not check["hasCredentials"]:
    client.register_wallet_credentials(
        wallet_address=wallet,
        api_key=creds.api_key,
        api_secret=creds.api_secret,
        api_passphrase=creds.api_passphrase,
    )
    print(f"Wallet credentials registered for {wallet}")
else:
    print(f"Wallet {wallet} already configured.")
```

### Step 4 — Configure Risk Limits

```python
client.update_settings(
    max_trades_per_day=50,
    max_trade_amount=100.0,
    trading_paused=False,
    auto_redeem_enabled=True,
)
settings = client.get_settings()
print(settings)
```

### Step 5 — Kalshi Prerequisites (Optional, for Kalshi venue)

- Ensure Solana wallet is available (`SOLANA_PRIVATE_KEY` / `userPublicKey`)
- Use `kalshi_quote()` to request unsigned tx, locally sign, then call `kalshi_submit()`
- For BUY flows, provide `userPublicKey` so KYC/geo checks can be evaluated upstream

---

## Workflow: Market Search & Context

### Understanding Market Data Structure

> **Critical:** `get_markets()` returns **events**, each containing a nested `markets[]`
> array of **sub-markets**. Trading fields like `conditionId`, `clobTokenIds`,
> `outcomePrices`, `negRisk`, and `orderPriceMinTickSize` live on the **sub-market**, NOT the event.

```python
import ast

# Search returns events
events = client.get_markets(q="bitcoin", limit=10)

for event in events:
    print(f"Event: {event['title']}")
    for sub in event.get("markets", []):
        # Parse JSON strings
        prices = ast.literal_eval(sub.get("outcomePrices", '["0.5","0.5"]'))
        token_ids = ast.literal_eval(sub.get("clobTokenIds", '[]'))
        print(f"  Sub-market: {sub['question']}")
        print(f"    conditionId: {sub['conditionId']}")
        print(f"    YES price: {prices[0]}, NO price: {prices[1]}")
        print(f"    YES token: {token_ids[0] if token_ids else 'N/A'}")
        print(f"    negRisk: {sub.get('negRisk', False)}")
        print(f"    tickSize: {sub.get('orderPriceMinTickSize', 0.01)}")
        print(f"    minSize: {sub.get('orderMinSize', 5)}")
```

### Get Market Context (REQUIRED before trading)

```python
context = client.get_market_context("CONDITION_ID", user=wallet)

print(f"Name:       {context.get('name')}")
print(f"Position:   {context.get('myPosition')}")
print(f"Risk limit: {context.get('riskLimit')}")
print(f"Warnings:   {context.get('warnings')}")

if context.get("warnings"):
    print("⚠️  Review warnings before proceeding!")
```

### Automatic Pre-Trade Readiness Checks

Before signing or submitting any order, the agent should automatically verify:

- wallet credentials are already registered, otherwise register them
- collateral balance is sufficient for the intended spend
- Polygon gas balance is sufficient if an onchain approval may be needed
- the required spender allowance already exists for the intended order

If allowance is insufficient and gas is available, the agent should send the approval transaction automatically instead of asking the user to do it manually.

---

## Workflow: Trade Execution

### Building a Signed Order (REQUIRED)

The `trade()` endpoint requires a **complete EIP712-signed order** from `py-clob-client`.
Passing `"order": {}` will cause a credential lookup failure — the server reads
`order.signatureType` to find your wallet credentials.

```python
import ast
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, CreateOrderOptions, OrderArgs

# 1. Initialize CLOB client with creds (derived earlier in bootstrap)
clob = ClobClient(
    "https://clob.polymarket.com",
    key=private_key,     # WALLET_PRIVATE_KEY
    chain_id=137,
    creds=ApiCreds(
        api_key=creds.api_key,
        api_secret=creds.api_secret,
        api_passphrase=creds.api_passphrase,
    ),
)

# 2. Extract trading params from sub-market (NOT event)
sub_market = event["markets"][0]  # pick the sub-market you want to trade
condition_id = sub_market["conditionId"]
token_ids = ast.literal_eval(sub_market["clobTokenIds"])
yes_token_id = token_ids[0]   # index 0 = YES, index 1 = NO
no_token_id = token_ids[1]
neg_risk = sub_market.get("negRisk", False)
tick_size = str(sub_market.get("orderPriceMinTickSize", "0.01"))
min_size = sub_market.get("orderMinSize", 5)

# 3. Build signed order — MUST use CreateOrderOptions for proper signing
signed_order = clob.create_order(
    OrderArgs(
        token_id=yes_token_id,   # or no_token_id for NO side
        price=0.55,
        size=min_size,           # must >= orderMinSize
        side="BUY",
    ),
    options=CreateOrderOptions(
        tick_size=tick_size,     # from sub-market.orderPriceMinTickSize
        neg_risk=neg_risk,       # CRITICAL for neg-risk markets!
    ),
)

# 4. Convert dataclass to dict for JSON serialization
order_dict = signed_order.dict()
```

### Place a Trade

```python
result = client.trade({
    "marketConditionId": condition_id,          # hex conditionId from sub-market
    "marketQuestion": sub_market["question"],   # question text
    "outcome": "YES",                           # YES or NO
    "orderSize": min_size,                      # number of contracts
    "price": 0.55,                              # price per contract (0-1)
    "isLimitOrder": True,                       # True=limit, False=market
    "order": order_dict,                        # ← FULL signed order (never {})
    "walletAddress": wallet,                    # ← REQUIRED
    "reasoning": "Strategy edge explanation",
})
print(f"Order ID: {result.get('orderId')}")
print(f"Status:   {result.get('status')}")
```

### Default Execution Policy

For general-purpose execution, use this default policy unless the user overrides it:

1. prefer `market` mode
2. use `2` USDC as default buy size
3. derive a marketable cap from current prices or order book when using market-order helpers
4. ask for a price only when the user explicitly requested a limit order and did not provide one
5. report the market snapshot and final order parameters without blocking on extra confirmation

> **Common pitfalls:**
>
> - `"order": {}` → server cannot find `signatureType`, returns credential error
> - Using event numeric ID as `marketConditionId` → use sub-market hex `conditionId`
> - Missing `walletAddress` → "walletAddress 不能为空" error
> - Not setting `neg_risk=True` for neg-risk markets → invalid signature, Polymarket rejects
> - `orderSize` below `orderMinSize` → order rejected
> - Insufficient USDC balance → server returns generic `INTERNAL_ERROR`
> - Insufficient allowance → downstream exchange cannot spend collateral
> - SDK result is empty or generic → verify recent trades and orders before reporting failure

**Order types:** `GTC` (default), `FOK`, `GTD`, `FAK`
**Sides:** `BUY`, `SELL`
**Outcomes:** `YES`, `NO`

---

## Workflow: Kalshi Quote -> Sign -> Submit

Use this flow for Kalshi venue execution.

```python
quote = client.kalshi_quote(
    market_ticker="KX...",
    side="YES",
    action="BUY",
    amount=10,
    user_public_key="<solana-wallet>",
)

# Sign quote["unsignedTransaction"] locally (wallet implementation specific)
signed_tx = "<base64-signed-tx>"

submit = client.kalshi_submit(
    market_ticker="KX...",
    side="YES",
    action="BUY",
    amount=10,
    quote_id=quote["quoteId"],
    signed_transaction=signed_tx,
    user_public_key="<solana-wallet>",
    in_amount=quote.get("inAmount"),
    out_amount=quote.get("outAmount"),
    min_out_amount=quote.get("minOutAmount"),
)
print(submit)

# Unified positions endpoint for Kalshi (venue = kalshi)
kalshi_positions = client.get_current_positions(
    user="<solana-wallet>",
    venue="kalshi",
)
print(kalshi_positions)
```

Kalshi currently does not expose a dedicated cancel API in this SDK. Use a SELL flow (`kalshi_quote` -> sign -> `kalshi_submit`) to reduce/exit exposure.

## Workflow: Order Management

```python
# List open orders
open_orders = client.get_open_orders()

# Order history (with optional filters)
history = client.get_order_history(limit=20, order_status=2)

# Single order detail
detail = client.get_order_detail("ORDER_ID")

# Cancel one order
client.cancel_order("ORDER_ID")

# Cancel ALL orders (use with care)
client.cancel_all_orders()
```

---

## Workflow: Heartbeat / Briefing

Call periodically (every 30s–15min depending on strategy frequency).

```python
# wallet can be Polygon or Solana based on venue flow
briefing = client.get_briefing(user=wallet)

# 1. Handle risk alerts first
for alert in briefing.get("riskAlerts", []):
    print(f"⚠️  {alert}")

# 2. Review open orders
open_orders = client.get_open_orders()
print(f"Open orders: {len(open_orders)}")

# 3. Scan opportunity markets
for opp in briefing.get("opportunityMarkets", [])[:5]:
    print(f"Opportunity: {opp.get('id')} — {opp.get('question')}")
```

---

## Workflow: Redemption

When a market settles, redeem winning positions:

```python
client.redeem(market_id="MARKET_ID", side="YES")
```

---

## Error Handling

```python
from aionmarket_sdk import AionMarketClient, ApiError

client = AionMarketClient()

try:
    result = client.get_me()
except ApiError as e:
    if e.status_code == 401:
        print("❌ Invalid or missing API key")
    elif e.status_code == 403:
        print("❌ Agent not authorized — check claim status or wallet credentials")
    elif e.status_code == 429:
        print("⏳ Rate limited — back off and retry")
    else:
        print(f"API Error {e.code}: {e.message}")
```

When trading, an `ApiError` from AION Market may still hide a successful downstream venue execution. If the response is ambiguous, query venue-specific follow-up endpoints before concluding failure (Polymarket orders/trades, or Kalshi submit/positions state).

---

## SDK Method Reference

### Agent Management

| Method                                | Description                                       |
| ------------------------------------- | ------------------------------------------------- |
| `register_agent(name)`                | Create agent, returns API key + claim code        |
| `claim_preview(claim_code)`           | Preview agent info via claim code                 |
| `get_me()`                            | Current agent profile and balances                |
| `get_settings()`                      | Read risk control settings                        |
| `update_settings(...)`                | Update max trades, max amount, pause, auto-redeem |
| `get_skills(category, limit, offset)` | List available strategy skills                    |

### Market Operations

| Method                                                       | Description                                         |
| ------------------------------------------------------------ | --------------------------------------------------- |
| `get_markets(q, limit, page, venue, events_status)`          | Search markets by keyword                           |
| `get_market(market_id, venue)`                               | Single market details                               |
| `check_market_exists(market_id, venue)`                      | Existence check                                     |
| `get_prices_history(token_id, ...)`                          | Historical prices for a token                       |
| `get_briefing(venue, since, user, include_markets)`          | Heartbeat: alerts + opportunities                   |
| `get_market_context(market_id, venue, user, my_probability)` | Pre-trade context & risk                            |
| `get_current_positions(user, venue, ...)`                    | Unified current positions (`polymarket` / `kalshi`) |

### Wallet Management

| Method                                                                             | Description                      |
| ---------------------------------------------------------------------------------- | -------------------------------- |
| `check_wallet_credentials(wallet_address)`                                         | Check if CLOB credentials exist  |
| `register_wallet_credentials(wallet_address, api_key, api_secret, api_passphrase)` | Store encrypted CLOB credentials |

### Trading Operations

| Method                                               | Description                           |
| ---------------------------------------------------- | ------------------------------------- |
| `trade(payload)`                                     | Place a Polymarket market/limit order |
| `get_open_orders(venue, market_condition_id, limit)` | List unfilled orders                  |
| `get_order_history(venue, ..., limit, offset)`       | Historical orders with filters        |
| `get_order_detail(order_id, venue, wallet_address)`  | Single order detail                   |
| `cancel_order(order_id, venue, wallet_address)`      | Cancel one order                      |
| `cancel_all_orders(venue, wallet_address)`           | Cancel all open orders                |
| `redeem(market_id, side, venue, wallet_address)`     | Redeem settled position               |
| `kalshi_quote(...)`                                  | Build unsigned Kalshi quote tx        |
| `kalshi_submit(...)`                                 | Submit locally signed Kalshi tx       |

---

## Checklist: Ready to Trade

- [ ] `pip install aionmarket-sdk py-clob-client python-dotenv` installed
- [ ] `.env` file created with `AIONMARKET_API_KEY` and `WALLET_PRIVATE_KEY` (plus `SOLANA_PRIVATE_KEY` if using Kalshi)
- [ ] `.env` added to `.gitignore`
- [ ] `get_me()` returns valid agent info
- [ ] Polymarket CLOB credentials derived from private key and registered via `register_wallet_credentials()`
- [ ] automatic balance, gas/fees, and allowance checks are part of the trading flow
- [ ] missing allowance is auto-approved when technically possible
- [ ] Risk limits configured via `update_settings()`
- [ ] Heartbeat loop (`get_briefing()`) running or planned
- [ ] Error handling wraps every SDK call with `ApiError`
- [ ] For Kalshi: quote -> sign -> submit flow validated with `kalshi_quote()` / `kalshi_submit()`
- [ ] ambiguous trade responses are verified against venue-specific state endpoints

> Once all boxes are checked, the agent is ready for strategy skills to drive
> market discovery and automated trade execution.
