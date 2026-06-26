# Options Trading

Assumes SDK is initialized. See SKILL.md.

⚠️ Option trading is only supported on certain brokerages. Check the SnapTrade
broker support matrix before attempting option orders.

---

## Get Option Positions

Returns all open option positions in the account.

```python
response = snaptrade.options.list_option_holdings(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
)
positions = response.body
# Each position: option_symbol (ticker, option_type, strike_price,
#   expiration_date, is_mini_option, underlying_symbol), units, price
```

---

## Get Option Quote (BETA)

Returns a quote for a specific option contract.

```python
response = snaptrade.trading.get_user_account_option_quotes(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    option_symbol_id=option_symbol_id,  # UUID from option position or search
)
quote = response.body
```

---

## Check Option Order Impact (BETA)

Simulates an option order before placing it. Returns estimated cash impact.

```python
response = snaptrade.trading.get_option_impact(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    option_symbol_id=option_symbol_id,
    action="BUY_TO_OPEN",   # See actions below
    units=1,
    order_type="Limit",
    time_in_force="Day",
    price=2.50,             # per share (x100 per contract)
)
```

---

## Place Option Order (Multi-Leg)

Places a single or multi-leg option order using OCC symbol format.

**OCC symbol format:** `AAPL  261218C00240000`
= underlying + expiry (YYMMDD) + type (C/P) + strike * 1000 (8 digits)

```python
response = snaptrade.trading.place_mleg_order(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    order_type="LIMIT",         # "MARKET", "LIMIT", "STOP_LOSS_MARKET",
                                # "STOP_LOSS_LIMIT"
    time_in_force="Day",        # "Day", "GTC", "FOK", "IOC"
    limit_price="2.50",         # required for LIMIT, STOP_LOSS_LIMIT
    stop_price="2.00",          # required for STOP_LOSS_MARKET, STOP_LOSS_LIMIT
    price_effect="DEBIT",       # "CREDIT", "DEBIT", "EVEN" — for limit orders
    legs=[
        {
            "instrument": {
                "symbol": "AAPL  261218C00240000",  # OCC symbol
                "instrument_type": "OPTION",
            },
            "action": "BUY_TO_OPEN",  # See actions below
            "units": 1,
        }
    ],
)
order = response.body
brokerage_order_id = order["brokerage_order_id"]
```

### Option Actions

| Action | Meaning |
|---|---|
| `BUY_TO_OPEN` | Buy to open a new long position |
| `BUY_TO_CLOSE` | Buy to close an existing short position |
| `SELL_TO_OPEN` | Sell to open a new short position |
| `SELL_TO_CLOSE` | Sell to close an existing long position |

### Multi-Leg Example (Vertical Spread)

```python
legs=[
    {
        "instrument": {"symbol": "AAPL  261218C00240000", "instrument_type": "OPTION"},
        "action": "BUY_TO_OPEN",
        "units": 1,
    },
    {
        "instrument": {"symbol": "AAPL  261218C00250000", "instrument_type": "OPTION"},
        "action": "SELL_TO_OPEN",
        "units": 1,
    },
]
```

---

## Notes

- Option prices are per share — multiply by 100 for cost per contract
  (10 for mini options where `is_mini_option=True`)
- `trade_id` from impact check (BETA) expires in 5 minutes
- Not all brokerages support multi-leg orders — single-leg is more widely supported
