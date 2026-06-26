# Crypto Trading

Assumes SDK is initialized. See SKILL.md.

⚠️ Crypto trading requires a brokerage connection that supports crypto. Some
brokerages also require re-authorization with trading permissions enabled.

---

## Step 1: Get Tradable Crypto Pairs

Returns all cryptocurrency pairs available to trade in the account.
Omit `base` and `quote` to get the full list.

```python
response = snaptrade.trading.search_cryptocurrency_pair_instruments(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    base="BTC",   # optional — base currency e.g. "BTC", "ETH"
    quote="USD",  # optional — quote currency e.g. "USD", "USDC"
)
pairs = response.body["items"]
# Each pair: symbol (e.g. "BTC-USD"), base, quote, increment
```

Use the `symbol` field (e.g. `"BTC-USD"`) when placing crypto orders.

---

## Step 2: Get Crypto Pair Quote

Returns the current bid/ask for a crypto pair.

```python
response = snaptrade.trading.get_cryptocurrency_pair_quote(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    instrument=crypto_symbol,  # e.g. "BTC-USD"
)
quote = response.body
# Fields: bid_price, ask_price, last_trade_price
```

---

## Step 3: Preview Crypto Order (Optional)

Simulates the order before placing. Returns estimated fees and impact.

```python
response = snaptrade.trading.preview_crypto_order(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    instrument={
        "symbol": "BTC-USD",
        "type": "CRYPTOCURRENCY_PAIR",
    },
    side="BUY",           # "BUY" or "SELL"
    type="MARKET",        # see order types below
    time_in_force="GTC",
    amount="0.01",        # amount of base currency (e.g. 0.01 BTC)
)
preview = response.body
```

---

## Step 4: Place Crypto Order

Places the order directly — no separate "place after preview" step.

```python
response = snaptrade.trading.place_crypto_order(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    instrument={
        "symbol": "BTC-USD",
        "type": "CRYPTOCURRENCY_PAIR",
    },
    side="BUY",                     # "BUY" or "SELL"
    type="LIMIT",                   # see order types below
    time_in_force="GTC",            # "GTC", "FOK", "IOC", "GTD"
    amount="0.01",                  # base currency amount
    limit_price="95000.00",         # required for LIMIT, STOP_LOSS_LIMIT, TAKE_PROFIT_LIMIT
    stop_price="90000.00",          # required for STOP_LOSS_*, TAKE_PROFIT_*
    post_only=False,                # LIMIT only — if True, rejects orders that would fill immediately (avoids taker fees)
    # expiration_date="2026-06-01T00:00:00Z"  # required if time_in_force is GTD
)
order = response.body
brokerage_order_id = order["brokerage_order_id"]
```

### Crypto Order Types

| Type | Description |
|---|---|
| `MARKET` | Execute immediately at market price |
| `LIMIT` | Execute at specified price or better |
| `STOP_LOSS_MARKET` | Market order triggered at stop price |
| `STOP_LOSS_LIMIT` | Limit order triggered at stop price |
| `TAKE_PROFIT_MARKET` | Market order triggered when profit target hit |
| `TAKE_PROFIT_LIMIT` | Limit order triggered when profit target hit |

### Time in Force (Crypto)

| Value | Meaning |
|---|---|
| `GTC` | Good Till Canceled |
| `FOK` | Fill or Kill |
| `IOC` | Immediate or Cancel |
| `GTD` | Good Till Date (requires `expiration_date`) |

---

## Cancel a Crypto Order

Same cancel endpoint as equities:

```python
snaptrade.trading.cancel_order(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    brokerage_order_id=brokerage_order_id,
)
```

---

## Notes

- `amount` is in units of the **base** currency (e.g. BTC in BTC-USD)
- Tickers vary by exchange — e.g. BTC may be `BTC`, `XBT`, or `XXBT` depending
  on the brokerage. Always use `get_crypto_pairs` to find the correct symbol
- Crypto markets trade 24/7 — no market hours restriction
