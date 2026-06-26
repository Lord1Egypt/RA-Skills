# Account Data

Assumes SDK is initialized and `user_id` / `user_secret` are set. See SKILL.md.

---

## List All Accounts

Returns all connected brokerage accounts. `account_id` is required for all
subsequent calls — always fetch this first.

```python
response = snaptrade.account_information.list_user_accounts(
    user_id=user_id,
    user_secret=user_secret,
)
accounts = response.body
# Each account: id, name, number, institution_name, meta.type
account_id = accounts[0]["id"]
```

---

## Get Account Detail

Returns account name, number, total market value, and sync status.

```python
response = snaptrade.account_information.get_user_account_details(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
)
detail = response.body
# Fields: id, name, number, institution_name, meta.type, sync_status, balance
```

---

## Get Balances

Returns cash holdings and buying power, broken out by currency.

```python
response = snaptrade.account_information.get_user_account_balance(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
)
balances = response.body
# Each balance: {currency: {code, name}, cash: float}
```

---

## Get Positions

Returns stock/ETF/crypto/mutual fund positions. Does not include options.

```python
response = snaptrade.account_information.get_user_account_positions(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
)
positions = response.body
# Each position: symbol, units, price, average_purchase_price, open_pnl, currency
# units > 0 = long, units < 0 = short
```

## Get Option Positions

```python
response = snaptrade.options.list_option_holdings(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
)
option_positions = response.body
```

---

## Get All Holdings at Once

Returns positions + balances + orders + total value in one call.
Slower than individual endpoints — use only when you need everything.

```python
response = snaptrade.account_information.get_user_holdings(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
)
holdings = response.body
# Keys: account, balances, positions, orders, total_value
```

---

## Get Orders

Returns all orders including pending, filled, and cancelled.

```python
response = snaptrade.account_information.get_user_account_orders(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
)
orders = response.body
# Each order: brokerage_order_id, status, action, units, price, symbol, time_in_force
```

---

## Get Recent Orders (Last 24 Hours)

Returns only orders placed in the last 24 hours. Faster than the full order list.

```python
response = snaptrade.account_information.get_user_account_recent_orders(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
)
recent_orders = response.body
```

---

## Get Single Order Detail

Returns full detail for a specific order by its brokerage order ID.

```python
response = snaptrade.account_information.get_user_account_order_detail(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    brokerage_order_id=brokerage_order_id,
)
order = response.body
```

---

## Get Historical Account Total Value (BETA)

Returns the total account value over time — useful for performance tracking.

```python
response = snaptrade.account_information.get_account_balance_history(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    start_date="2024-01-01",   # optional
    end_date="2024-12-31",     # optional
)
history = response.body
# Each entry: date, total_value, currency
```

---

## Data Freshness

Data is cached and refreshed once daily by default. For real-time data, either
use a paid API key or trigger a manual refresh — see `references/cancel-refresh.md`.
