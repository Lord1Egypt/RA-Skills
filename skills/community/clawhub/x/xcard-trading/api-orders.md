# Module: Order Execution

**When to load this file:** User wants to place, cancel, or check the status of orders.

Trigger phrases: "buy", "sell", "order", "cancel", "买入", "卖出", "下单", "挂单", "撤单"

---

## ⚠️ Order Safety Rules

Before calling POST /orders, always:

1. **Confirm details** — repeat back symbol, side, type, quantity, and price (if limit).
2. **Wait for explicit confirmation** — only proceed after user says "yes", "confirm", or equivalent.
3. **Large order warning** — if the order value exceeds 10% of the user's available balance, show an extra warning before confirming.
4. **Never assume** — if any parameter is ambiguous (e.g., user says "buy some AAPL"), ask for quantity and price before proceeding.

---

## POST /orders — Place an order

**Request**
```
POST /orders
X-API-KEY: {XCard_API_KEY}
Content-Type: application/json
```

**Request body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | Yes | Token symbol, e.g. `TOKEN-AAPL` |
| side | string | Yes | `buy` or `sell` |
| type | string | Yes | `limit` or `market` |
| quantity | number | Yes | Number of tokens |
| price | number | Limit only | Required when type is `limit` |

**Example — limit buy**
```json
{
  "symbol": "TOKEN-AAPL",
  "side": "buy",
  "type": "limit",
  "quantity": 100,
  "price": 194.50
}
```

**Example — market sell**
```json
{
  "symbol": "TOKEN-AAPL",
  "side": "sell",
  "type": "market",
  "quantity": 50
}
```

**Response**
```json
{
  "order_id": "ORD-20250325-001",
  "symbol": "TOKEN-AAPL",
  "side": "buy",
  "type": "limit",
  "quantity": 100,
  "price": 194.50,
  "status": "open",
  "filled_quantity": 0,
  "avg_fill_price": null,
  "created_at": "2025-03-25T10:35:00Z"
}
```

---

## DELETE /orders/{order_id} — Cancel an order

**Request**
```
DELETE /orders/ORD-20250325-001
X-API-KEY: {XCard_API_KEY}
```

**Response**
```json
{
  "order_id": "ORD-20250325-001",
  "status": "cancelled",
  "cancelled_at": "2025-03-25T10:40:00Z"
}
```

> Only orders with status `open` or `partial` can be cancelled.  
> If the order is already filled or cancelled, the API returns 400.

---

## GET /orders/open — List open orders

Returns all pending or partially filled orders.

**Request**
```
GET /orders/open
X-API-KEY: {XCard_API_KEY}
```

**Response**
```json
{
  "orders": [
    {
      "order_id": "ORD-20250325-001",
      "symbol": "TOKEN-AAPL",
      "side": "buy",
      "type": "limit",
      "quantity": 100,
      "filled_quantity": 30,
      "price": 194.50,
      "status": "partial",
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
X-API-KEY: {XCard_API_KEY}
```

**Response** — same schema as above, with additional fill details:
```json
{
  "order_id": "ORD-20250325-001",
  "status": "filled",
  "filled_quantity": 100,
  "avg_fill_price": 194.48,
  "fills": [
    { "price": 194.45, "quantity": 60, "time": "2025-03-25T10:36:00Z" },
    { "price": 194.52, "quantity": 40, "time": "2025-03-25T10:37:00Z" }
  ]
}
```

**Order status values**

| Status | Meaning |
|--------|---------|
| `open` | Pending, no fills yet |
| `partial` | Partially filled |
| `filled` | Fully executed |
| `cancelled` | Cancelled by user |
| `rejected` | Rejected by system |
