# Module: Account & Margin

**When to load this file:** User asks about balance, margin, leverage, liquidation price, or overall position summary.

Trigger phrases: "balance", "margin", "leverage", "liquidation", "wallet", "余额", "保证金", "杠杆", "强平", "账户"

---

## GET /account/balance

Returns the user's wallet balance (available + used in margin).

**Request**
```
GET /account/balance
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Response**
```json
{
  "currency": "USDT",
  "wallet_balance": 10000.00,
  "available_balance": 7500.00,
  "used_margin": 2500.00,
  "unrealized_pnl": 320.50,
  "total_equity": 10320.50
}
```

Field notes:
- `wallet_balance` — total funds deposited
- `available_balance` — funds free to open new positions
- `used_margin` — margin locked in open positions
- `unrealized_pnl` — combined PnL of all open positions
- `total_equity` — wallet_balance + unrealized_pnl

---

## GET /account/leverage

Returns the current default leverage and margin mode.

**Request**
```
GET /account/leverage
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Response**
```json
{
  "margin_mode": "isolated",
  "default_leverage": 10,
  "max_leverage": 125
}
```

Field notes:
- `isolated` — each position has its own margin
- `cross` — all positions share the same margin pool
- Max leverage varies by symbol (BTC: 125x, altcoins: lower)

---

## GET /positions

Returns all open positions across all symbols.

**Request**
```
GET /positions
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | No | Filter by symbol, e.g. `BTC/USDT` |

**Response**
```json
{
  "positions": [
    {
      "symbol": "BTC/USDT",
      "side": "long",
      "size": 0.5,
      "entry_price": 67500.00,
      "mark_price": 68200.00,
      "liquidation_price": 62000.00,
      "leverage": 10,
      "margin": 337.50,
      "unrealized_pnl": 350.00,
      "unrealized_pnl_pct": 3.74,
      "funding_fee_accrued": -12.50
    }
  ],
  "total_unrealized_pnl": 350.00
}
```

**Display format:** Present as a table when multiple positions exist.

| Symbol | Side | Size | Entry | Mark | Liq. Price | Leverage | Margin | PnL | PnL % |
|--------|------|------|-------|------|------------|---------|--------|-----|-------|
| BTC/USDT | long | 0.5 | 67,500 | 68,200 | 62,000 | 10x | 337.50 | +350.00 | +3.74% |

---

## GET /positions/{symbol}

Returns detailed info for a specific symbol position.

**Request**
```
GET /positions/BTC-USDT
X-API-KEY: {XCARD_TRADE_API_KEY}
```

> Note: symbol uses hyphen `BTC-USDT` in the URL path.

**Response**
```json
{
  "symbol": "BTC/USDT",
  "side": "long",
  "size": 0.5,
  "entry_price": 67500.00,
  "mark_price": 68200.00,
  "index_price": 68185.00,
  "liquidation_price": 62000.00,
  "leverage": 10,
  "margin": 337.50,
  "margin_mode": "isolated",
  "unrealized_pnl": 350.00,
  "unrealized_pnl_pct": 3.74,
  "realized_pnl": 0.00,
  "funding_fee_accrued": -12.50,
  "created_at": "2025-03-24T08:00:00Z",
  "updated_at": "2025-03-25T10:30:00Z"
}
```

---

## POST /account/leverage — Set leverage for a symbol

**Request**
```
POST /account/leverage
X-API-KEY: {XCARD_TRADE_API_KEY}
Content-Type: application/json
```

**Request body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | Yes | Symbol, e.g. `BTC/USDT` |
| leverage | integer | Yes | Leverage multiplier, e.g. `10` |

**Example**
```json
{
  "symbol": "BTC/USDT",
  "leverage": 20
}
```

**Response**
```json
{
  "symbol": "BTC/USDT",
  "leverage": 20,
  "max_leverage": 125
}
```

> ⚠️ Increasing leverage raises liquidation risk. Warn users when setting leverage above 20x.
