# Module: Trade History & Reports

**When to load this file:** User asks about filled trades, closed positions, realized PnL, or funding fee history.

Trigger phrases: "history", "trade", "pnl", "realized", "funding", "filled", "closed", "history", "报表", "成交", "盈利", "亏损", "平仓", "资金费用"

---

## GET /trades/history — Executed trade history

Returns a list of all completed trade fills (actual executions).

**Request**
```
GET /trades/history
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | No | Filter by symbol, e.g. `BTC/USDT` |
| side | string | No | `buy` or `sell` |
| from | string | No | Start date, ISO 8601: `2025-01-01T00:00:00Z` |
| to | string | No | End date, ISO 8601 |
| limit | integer | No | Max records. Default: `50`, max: `500` |

**Response**
```json
{
  "trades": [
    {
      "trade_id": "TRD-20250324-001",
      "order_id": "ORD-20250324-005",
      "symbol": "BTC/USDT",
      "side": "buy",
      "size": 0.5,
      "price": 67100.00,
      "fee": 16.78,
      "fee_currency": "USDT",
      "realized_pnl": null,
      "executed_at": "2025-03-24T09:36:00Z"
    }
  ],
  "total": 1
}
```

---

## GET /orders/history — Historical orders

Returns all past orders regardless of status (filled, cancelled, rejected).

**Request**
```
GET /orders/history
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| status | string | No | `filled`, `cancelled`, `rejected`, or `all`. Default: `all` |
| symbol | string | No | Filter by symbol |
| from | string | No | Start date, ISO 8601 |
| to | string | No | End date, ISO 8601 |
| limit | integer | No | Default: `50`, max: `500` |

**Response**
```json
{
  "orders": [
    {
      "order_id": "ORD-20250324-005",
      "symbol": "BTC/USDT",
      "side": "buy",
      "type": "limit",
      "size": 0.5,
      "price": 67000.00,
      "leverage": 10,
      "filled_size": 0.5,
      "avg_fill_price": 67100.00,
      "status": "filled",
      "fee": 16.78,
      "created_at": "2025-03-24T09:35:00Z",
      "updated_at": "2025-03-24T09:36:00Z"
    }
  ],
  "total": 1
}
```

---

## GET /positions/history — Closed positions

Returns all closed (liquidated or manually closed) positions with realized PnL.

**Request**
```
GET /positions/history
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | No | Filter by symbol |
| from | string | No | Start date, ISO 8601 |
| to | string | No | End date, ISO 8601 |
| limit | integer | No | Default: `50`, max: `500` |

**Response**
```json
{
  "positions": [
    {
      "symbol": "ETH/USDT",
      "side": "long",
      "size": 5.0,
      "entry_price": 3500.00,
      "exit_price": 3720.00,
      "realized_pnl": 1040.00,
      "realized_pnl_pct": 5.94,
      "leverage": 10,
      "margin": 175.00,
      "fees": 26.25,
      "funding_fees": 3.75,
      "close_reason": "manual",
      "opened_at": "2025-03-20T08:00:00Z",
      "closed_at": "2025-03-24T14:30:00Z"
    }
  ],
  "total": 1
}
```

**Display guidance:**
- Present as a table sorted by `closed_at` descending.
- Show close reason: `manual` (user closed), `liquidation` (liquidated), `auto_deleverage` (ADL)
- Positive PnL = profit, negative = loss

| Symbol | Side | Size | Entry | Exit | PnL | PnL % | Close Reason | Closed |
|--------|------|------|-------|------|------|-------|--------------|--------|
| ETH/USDT | long | 5.0 | 3,500 | 3,720 | +1,040.00 | +5.94% | manual | Mar 24 |

---

## GET /account/transactions — Funding fee history

Returns all funding fee payments and deposits/withdrawals.

**Request**
```
GET /account/transactions
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | No | `deposit`, `withdrawal`, `funding`, `trade`, or `all`. Default: `all` |
| from | string | No | Start date, ISO 8601 |
| to | string | No | End date, ISO 8601 |
| limit | integer | No | Default: `50`, max: `500` |

**Response**
```json
{
  "transactions": [
    {
      "tx_id": "TX-20250324-001",
      "type": "deposit",
      "amount": 10000.00,
      "currency": "USDT",
      "balance_after": 15000.00,
      "description": "USDT deposit",
      "created_at": "2025-03-24T08:00:00Z"
    },
    {
      "tx_id": "TX-20250324-002",
      "type": "funding",
      "amount": -12.50,
      "currency": "USDT",
      "balance_after": 14987.50,
      "symbol": "BTC/USDT",
      "description": "BTC/USDT funding fee settlement",
      "created_at": "2025-03-24T16:00:00Z"
    },
    {
      "tx_id": "TX-20250325-001",
      "type": "trade",
      "amount": -335.50,
      "currency": "USDT",
      "balance_after": 14652.00,
      "symbol": "BTC/USDT",
      "description": "BTC/USDT long opened: 0.5 @ 67100",
      "created_at": "2025-03-25T10:30:00Z"
    }
  ],
  "total": 3
}
```

**Display guidance:**
- Default to last 30 days if user doesn't specify a date range.
- Positive `amount` = money in (deposit, sell proceeds, funding received).
- Negative `amount` = money out (withdrawal, position opened, funding paid).
- Present as a table sorted by `created_at` descending.
