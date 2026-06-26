# Placing Orders

**Confirmation mode — two supported patterns:**

- **Manual mode (default):** Before every order or cancellation, show the full
  order details (symbol, action, quantity, order type, price) and wait for the
  user to confirm. Use this unless the user has explicitly opted into automated mode.

- **Automated mode:** Only use if you have explicitly configured OpenClaw for
  autonomous/algorithmic trading AND have all of the following enforced in your
  decision engine before any order endpoint is called:
  - **Symbol allowlist** — only trade pre-approved symbols
  - **Notional cap** — maximum dollar value per order (e.g. $500/trade)
  - **Position limit** — maximum units or total exposure per symbol
  - **Daily loss limit** — halt trading if daily P&L exceeds a threshold
  - **Paper trading first** — validate the full automated flow on a paper/sandbox
    account before connecting a live brokerage

  Automated mode without these guardrails is not recommended and may result in
  unintended financial loss.

The checked order flow (impact check → place) is the recommended default in
both modes. The direct/force order flow is available in either mode.

Assumes `universal_symbol_id` is already resolved. If not, see `references/symbol-resolution.md`.

---

## Order Parameters Reference

| Parameter | Options |
|---|---|
| `action` | `"BUY"`, `"SELL"` |
| `order_type` | `"Market"`, `"Limit"`, `"Stop"`, `"StopLimit"` |
| `time_in_force` | `"Day"`, `"GTC"`, `"FOK"`, `"IOC"` |
| `price` | Required for `Limit` and `StopLimit` |
| `stop` | Required for `Stop` and `StopLimit` |
| `units` | Number of shares (decimal ok for fractional) |
| `notional_value` | Dollar amount — use instead of `units` for dollar-based orders |

---

## Flow 1: Checked Order (Recommended)

Simulates the order first, then places it. Safer — confirms cash impact before execution.
**`trade_id` expires after 5 minutes. Place immediately after impact check.**

### Step 1 — Check Impact

```python
response = snaptrade.trading.get_order_impact(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    universal_symbol_id=universal_symbol_id,
    action="BUY",
    order_type="Limit",
    time_in_force="Day",
    price=150.00,
    units=10,
)
trade_id = response.body["trade"]["id"]
remaining_cash = response.body["trade_impacts"][0]["remaining_cash"]
estimated_commissions = response.body["trade_impacts"][0]["estimated_commissions"]
```

### Step 2 — Place Checked Order

```python
response = snaptrade.trading.place_order(
    trade_id=trade_id,
    user_id=user_id,
    user_secret=user_secret,
)
order = response.body
brokerage_order_id = order["brokerage_order_id"]
status = order["status"]
```

---

## Flow 2: Direct Order (Force Order)

Skips the impact check. Available in both manual and automated mode.
In manual mode, confirm order details with the user before calling.
In automated mode, ensure your decision engine has validated the order
(symbol, side, quantity, price, notional limits) before calling.

```python
response = snaptrade.trading.place_force_order(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    universal_symbol_id=universal_symbol_id,
    action="BUY",
    order_type="Market",
    time_in_force="Day",
    units=10,
    # price=150.00       # include for Limit/StopLimit
    # stop=145.00        # include for Stop/StopLimit
    # notional_value=1500.00  # use instead of units for dollar-based
)
order = response.body
brokerage_order_id = order["brokerage_order_id"]
```

---

## Flow 3: Bracket Order

Places an entry order with an automatic stop loss and take profit in one call.

```python
response = snaptrade.trading.place_bracket_order(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    universal_symbol_id=universal_symbol_id,
    action="BUY",
    units=10,
    entry_price=150.00,
    stop_loss_price=145.00,
    take_profit_price=160.00,
    time_in_force="GTC",
)
order = response.body
```

---

## Error Handling

Common 400 errors:
- `Markets are not open`
- `Not enough cash to place trade`
- `Exchange does not support market orders`
- `Invalid symbol for this brokerage`

```python
try:
    response = snaptrade.trading.place_force_order(...)
except Exception as e:
    # Log and surface to decision engine for retry or skip logic
    raise
```

---

## After Placing

Always trigger a manual holdings refresh after placing an order so account
state reflects the new position. See `references/cancel-refresh.md`.
