# Module: Order Execution

**When to load this file:** User wants to place, cancel, or check the status of perpetual futures orders.

Trigger phrases: "buy", "sell", "long", "short", "order", "cancel", "stop", "limit", "market", "买入", "卖出", "做多", "做空", "下单", "挂单", "撤单", "止损", "止盈"

---

## ⚠️ Order Safety Rules

Before calling POST /orders, always:

1. **Confirm details** — repeat back symbol, side, type, size, leverage, and price (if limit).
2. **Wait for explicit confirmation** — only proceed after user says "yes", "confirm", or equivalent.
3. **Liquidation warning** — calculate and show the approximate liquidation price before confirming. If the order would open a position with margin below 10% of position value, show a strong warning.
4. **Never assume** — if any parameter is ambiguous (e.g., user says "buy some BTC"), ask for size, leverage, and entry price before proceeding.

---

## POST /orders — Place an order

**Request**
```
POST /orders
X-API-KEY: {XCARD_TRADE_API_KEY}
Content-Type: application/json
```

**Request body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | Yes | Symbol, e.g. `BTC/USDT` |
| side | string | Yes | `buy` (long) or `sell` (short) |
| type | string | Yes | `limit`, `market`, or `stop` |
| size | number | Yes | Position size in base currency (e.g. `0.5` BTC) |
| price | number | Limit only | Required for `limit` and `stop` orders |
| leverage | integer | Yes | Leverage multiplier, e.g. `10` |
| reduce_only | boolean | No | `true` to close only, not open. Default: `false` |
| stop_price | number | Stop only | Required when type is `stop` |
| take_profit_price | number | No | Trigger price for take-profit (close long if price rises to this) |
| stop_loss_price | number | No | Trigger price for stop-loss (close position if price falls to this) |

**Example — limit long (buy / go long)**
```json
{
  "symbol": "BTC/USDT",
  "side": "buy",
  "type": "limit",
  "size": 0.5,
  "price": 67000.00,
  "leverage": 10
}
```

**Example — market short (sell / go short)**
```json
{
  "symbol": "BTC/USDT",
  "side": "sell",
  "type": "market",
  "size": 0.5,
  "leverage": 10
}
```

**Example — stop-loss order**
```json
{
  "symbol": "BTC/USDT",
  "side": "sell",
  "type": "stop",
  "size": 0.5,
  "stop_price": 65000.00,
  "leverage": 10
}
```

**Response**
```json
{
  "order_id": "ORD-20250325-001",
  "symbol": "BTC/USDT",
  "side": "buy",
  "type": "limit",
  "size": 0.5,
  "price": 67000.00,
  "leverage": 10,
  "status": "open",
  "filled_size": 0,
  "avg_fill_price": null,
  "created_at": "2025-03-25T10:35:00Z"
}
```

---

## DELETE /orders/{order_id} — Cancel an order

**Request**
```
DELETE /orders/ORD-20250325-001
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Response**
```json
{
  "order_id": "ORD-20250325-001",
  "status": "cancelled",
  "cancelled_at": "2025-03-25T10:40:00Z"
}
```

> Only orders with status `open` can be cancelled. If already filled or cancelled, the API returns 400.

---

## PATCH /orders/{order_id} — Modify an order

**Request**
```
PATCH /orders/ORD-20250325-001
X-API-KEY: {XCARD_TRADE_API_KEY}
Content-Type: application/json
```

**Request body** (all fields optional, only provided fields are updated)

| Field | Type | Description |
|-------|------|-------------|
| price | number | New limit price |
| size | number | New size (not allowed for reduce_only orders) |

**Example**
```json
{
  "price": 67500.00
}
```

**Response**
```json
{
  "order_id": "ORD-20250325-001",
  "price": 67500.00,
  "size": 0.5,
  "status": "open",
  "updated_at": "2025-03-25T10:42:00Z"
}
```

---

## GET /orders/open — List open orders

Returns all pending (unfilled or partially filled) orders.

**Request**
```
GET /orders/open
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | No | Filter by symbol |

**Response**
```json
{
  "orders": [
    {
      "order_id": "ORD-20250325-001",
      "symbol": "BTC/USDT",
      "side": "buy",
      "type": "limit",
      "size": 0.5,
      "filled_size": 0.1,
      "price": 67000.00,
      "avg_fill_price": 66980.00,
      "leverage": 10,
      "status": "open",
      "created_at": "2025-03-25T10:35:00Z"
    }
  ]
}
```

---

## GET /orders/{order_id} — Get a single order

**Request**
```
GET /orders/ORD-20250325-001
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Response**
```json
{
  "order_id": "ORD-20250325-001",
  "symbol": "BTC/USDT",
  "side": "buy",
  "type": "limit",
  "size": 0.5,
  "filled_size": 0.5,
  "avg_fill_price": 67100.00,
  "leverage": 10,
  "status": "filled",
  "fills": [
    { "price": 67100.00, "size": 0.5, "time": "2025-03-25T10:37:00Z" }
  ],
  "created_at": "2025-03-25T10:35:00Z"
}
```

**Order status values**

| Status | Meaning |
|--------|---------|
| `open` | Pending, no fills yet |
| `partial` | Partially filled |
| `filled` | Fully executed |
| `cancelled` | Cancelled by user |
| `rejected` | Rejected (insufficient margin, too much size, etc.) |

---

## ⚠️ Liquidation Price Reference

For a long position with leverage L and entry price P:
```
Liquidation ≈ P × (1 - 1/L)
```

Example: Entry $67,000 @ 10x leverage → Liquidation ≈ $60,300
Example: Entry $67,000 @ 20x leverage → Liquidation ≈ $63,650

Always show the estimated liquidation price when placing a new order. Warn if it is within 10% of the current price.
