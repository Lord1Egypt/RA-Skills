# Cancel Orders & Refresh Holdings

---

## Cancel an Order

Cancels an open order. Works for all asset types (equity, options, crypto).
Only open/pending orders can be cancelled — filled or already-cancelled orders will be rejected.

```python
response = snaptrade.trading.cancel_order(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    brokerage_order_id=brokerage_order_id,  # from place order response or order list
)
```

To get `brokerage_order_id` for an open order, fetch orders first:
```python
orders = snaptrade.account_information.get_user_account_orders(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
).body
open_orders = [o for o in orders if o["status"] == "PENDING"]
```

---

## Manual Holdings Refresh

Triggers a fresh sync of positions, balances, and orders from the brokerage.
Call this after placing or cancelling any order to ensure account state is current.

```python
# Step 1: get the authorization (connection) ID
connections = snaptrade.connections.list_brokerage_authorizations(
    user_id=user_id,
    user_secret=user_secret,
).body
authorization_id = connections[0]["id"]

# Step 2: trigger refresh
snaptrade.connections.refresh_brokerage_authorization(
    authorization_id=authorization_id,
    user_id=user_id,
    user_secret=user_secret,
)
```

**Note:** If the user has multiple connections (multiple brokerages), iterate
over all connections and refresh each one, or target only the relevant one by
matching `connection["brokerage"]["slug"]` to the brokerage you traded on.

---

## Connection Health Check

Before trading, verify the connection is not disabled:

```python
connections = snaptrade.connections.list_brokerage_authorizations(
    user_id=user_id,
    user_secret=user_secret,
).body

for conn in connections:
    if conn["disabled"]:
        # Connection is broken — cannot access live data or place trades
        # User must re-authenticate via the Connection Portal
        print(f"Connection {conn['id']} is disabled: {conn['brokerage']['name']}")
```
