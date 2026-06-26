# Trade It API Reference

Prefer the JSON request/response shapes in this file over prose summaries when implementing calls.
For enum values like brokerage ids, order types, time-in-force shorthands, directions, statuses, and units, read `enums.md` first.

## Auth and base URL

```http
Authorization: Bearer {{access_token}}
```

```txt
https://api.tradeit.app
```

Use bearer auth in all cases. `TRADEIT_ACCESS_TOKEN` may be an API key token or an OAuth access token.

## Error handling contract

When the helper script receives a non-2xx response, it returns:

```json
{
  "status": 401,
  "response": {
    "error": "Token expired"
  }
}
```

Recommended handling:
- `401`: token invalid or expired; re-authenticate and retry once with a fresh token.
- `403`: permission issue; verify account access/scope and do not blindly retry.
- `404`: resource not found; re-check IDs (`account_id`, `trade_id`, `connection_id`).
- `422`: validation issue; show field-level corrections and retry after user confirmation.
- `5xx`: transient server issue; retry with backoff and clear user messaging.

## Parameter and casing notes

Trade It uses endpoint-specific field casing. Do not normalize globally.

- Query uses `orderBy` for `GET /api/trade` sorting.
- Session URL requests use `brokerageId`.
- Tool params are typically snake_case (`buy_or_sell`, `time_in_force`, `account_id`).
- Create request/response naming differs: request uses `buy_or_sell`, response uses `action`.

## Endpoint summary

```json
{
  "read": [
    "GET /api/user/me",
    "GET /api/brokerageConnection/:id",
    "GET /api/account/:id/holdings",
    "GET /api/trade",
    "POST /api/tool/execute { toolName: \"get_accounts\" }"
  ],
  "trading": [
    "POST /api/tool/execute { toolName: \"create_trade\" }",
    "POST /api/tool/execute { toolName: \"create_options_trade\" }",
    "POST /api/tool/execute { toolName: \"execute_trade\" }"
  ],
  "hosted": [
    "POST /api/session/url"
  ]
}
```

---

## 1. Get User

```http
GET /api/user/me?expand="brokerage_connections[accounts]
```

Representative response:

```json
{
  "id": 1,
  "created_at": "2024-07-22T18:53:43.289Z",
  "username": "test123",
  "name": "Test User",
  "email": "test@test.com",
  "avatar_url": "https://images.test.com",
  "displayname": "Test User",
  "country": "US",
  "city": "New York",
  "updated_at": "2025-12-29T19:48:58.378Z",
  "default_account": 1,
  "default_crypto_account": 2,
  "default_investment": 100,
  "yolo_mode": false,
  "brokerage_connections": [
    {
      "id": 10,
      "created_at": "2026-01-09T17:37:26.294Z",
      "updated_at": "2026-01-09T17:37:26.294Z",
      "user_id": 1,
      "brokerage_id": 1,
      "status": 1,
      "accounts": [
        {
          "id": 11,
          "connection_id": 10,
          "name": "Robinhood x123",
          "balance": { "amount": 150, "currency": "USD" },
          "cash": { "amount": 100, "currency": "USD" },
          "created_at": "2026-01-13T11:01:18.002Z",
          "updated_at": "2026-01-13T11:01:18.002Z",
          "synced_at": "2026-01-13T11:01:18.002Z"
        }
      ]
    }
  ]
}
```

Use this when you need defaults and brokerage linkage.

---

## 2. Get Connection

```http
GET /api/brokerageConnection/:id
```

Representative response:

```json
{
  "id": 123,
  "created_at": "2026-02-06T18:09:19.640Z",
  "updated_at": "2026-02-18T19:32:08.331Z",
  "user_id": 1,
  "brokerage_id": 12,
  "status": 1,
  "expiry": 6661764499,
  "notified_at": null
}
```

Use this when the agent needs to inspect a known connection or detect stale/expired connection state.

---

## 3. Get Accounts

```http
POST /api/tool/execute
Content-Type: application/json
```

Request:

```json
{
  "toolName": "get_accounts",
  "params": {}
}
```

Representative response:

```json
[
  {
    "account": {
      "id": 304,
      "connection_id": 395,
      "external_id": "rh-304",
      "name": "Robinhood x1234",
      "balance": { "amount": 15420.5, "currency": "USD" },
      "cash": { "amount": 3420.5, "currency": "USD" },
      "created_at": "2026-01-03T15:20:10.000Z",
      "updated_at": "2026-03-17T13:55:02.000Z",
      "synced_at": "2026-03-17T13:55:02.000Z"
    },
    "brokerage_metadata": {
      "name": "Robinhood",
      "id": 1,
      "fractional_support": true,
      "minimum_order": 1
    },
    "connection": {
      "id": 395,
      "status": 1
    }
  }
]
```

Use this before trade creation when account choice matters.

---

## 4. Get Trades

```http
GET /api/trade
```

Example query:

```txt
/api/trade?orderBy=id%20DESC&expand=asset
```

Supported query params:

```json
{
  "orderBy": "id DESC",
  "filter": "created_at >= 2026-01-01T00:00:00.000Z",
  "cursor": "819",
  "refresh": "false",
  "expand": "asset"
}
```

`refresh` is sent as query text (`"true"` or `"false"`).

Representative response:

```json
[
  {
    "id": 737,
    "asset_id": 55,
    "account_id": 304,
    "action": "sell",
    "status": "placed",
    "total_units": 1,
    "filled_units": 0,
    "canceled_units": 0,
    "execution_price": null,
    "fee": null,
    "placed_at": "2025-12-03T18:57:56.650Z",
    "executed_at": null,
    "created_at": "2025-12-03T18:57:14.456Z",
    "updated_at": "2025-12-03T18:57:57.269Z",
    "external_id": "114",
    "user_id": 1,
    "order_type": "limit",
    "limit_price": { "amount": "0.01", "currency": "USD" },
    "stop_price": null,
    "time_in_force": "day",
    "error_message": null,
    "type": 1,
    "legs": [
      {
        "occ": "20251205C00275000",
        "type": "option",
        "action": "sell",
        "quantity": 1,
        "execution_price": null,
        "position_effect": "close"
      }
    ],
    "direction": "debit",
    "asset": {
      "id": 55,
      "name": "Amazon.com, Inc",
      "ticker": "AMZN",
      "type": 2,
      "logo_url": "https://images.tradeit.app/assets/amzn.webp",
      "exchange": "NASDAQ",
      "country": "US"
    }
  }
]
```

Use this for portfolio activity, execution history, order status checks, and post-trade follow-up.

---

## 5. Get Holdings

```http
GET /api/account/:id/holdings
```

Representative response:

```json
{
  "results": [
    {
      "symbol": "NET",
      "average_price": {
        "amount": 1.9999999524999998,
        "currency": "USD"
      },
      "quantity": 0.024277,
      "type": 2
    },
    {
      "symbol": "AMZN 260116C00295000",
      "average_price": {
        "amount": 1,
        "currency": "USD"
      },
      "quantity": 1,
      "type": 2
    }
  ],
  "next": null
}
```

Use this when the agent needs positions, cost basis, or to reason about covered calls and available inventory.

---

## 6. Create Trade

```http
POST /api/tool/execute
Content-Type: application/json
```

Request:

```json
{
  "toolName": "create_trade",
  "params": {
    "symbol": "TSLA",
    "amount": 1000,
    "unit": "dollars",
    "buy_or_sell": "buy",
    "order_type": "limit",
    "limit_price": 250,
    "time_in_force": "day",
    "account_id": 304
  }
}
```

Required params:

| field | required | type | notes |
|---|---|---|---|
| `symbol` | yes | string | asset symbol |
| `amount` | yes | number | dollars or shares based on `unit` |
| `unit` | yes | string | `dollars` or `shares` |
| `buy_or_sell` | yes | string | `buy` or `sell` |
| `order_type` | yes | string | `market`, `limit`, `stop`, `stop_limit` |
| `time_in_force` | yes | string | `day`, `gtc`, `ioc`, `fok` |
| `account_id` | yes | number | destination account |
| `limit_price` | conditional | number | required for `limit` and `stop_limit` |
| `stop_price` | conditional | number | required when order type/payload needs stop price |

Representative response:

```json
{
  "id": 842,
  "created_at": "2026-03-17T14:14:31.112Z",
  "updated_at": "2026-03-17T14:14:31.112Z",
  "user_id": 1,
  "asset_id": 88,
  "account_id": 304,
  "external_id": "draft-842",
  "type": 0,
  "action": "buy",
  "direction": null,
  "total_units": 4,
  "filled_units": 0,
  "canceled_units": 0,
  "execution_price": { "amount": 250, "currency": "USD" },
  "status": "draft",
  "order_type": "limit",
  "limit_price": { "amount": 250, "currency": "USD" },
  "stop_price": null,
  "time_in_force": "day",
  "placed_at": null,
  "executed_at": null,
  "error_message": null,
  "fee": null,
  "legs": null,
  "asset": {
    "id": 88,
    "name": "Tesla, Inc.",
    "ticker": "TSLA"
  }
}
```

Behavior:
- normally creates a draft
- for some users, create may place immediately based on account settings
- always inspect the returned `status`
- request uses `buy_or_sell`; response uses `action`

---

## 7. Create Options Trade

```http
POST /api/tool/execute
Content-Type: application/json
```

Request:

```json
{
  "toolName": "create_options_trade",
  "params": {
    "symbol": "SPY",
    "legs": [
      {
        "type": "option",
        "action": "buy",
        "position_effect": "open",
        "occ": "260620P00580000",
        "quantity": 1
      },
      {
        "type": "option",
        "action": "sell",
        "position_effect": "open",
        "occ": "260620P00570000",
        "quantity": 1
      }
    ],
    "direction": "debit",
    "order_type": "limit",
    "limit_price": 2.35,
    "time_in_force": "day",
    "account_id": 304
  }
}
```

Required params:

| field | required | type | notes |
|---|---|---|---|
| `symbol` | yes | string | underlying symbol |
| `legs` | yes | array | one or more option legs |
| `direction` | yes | string | `debit` or `credit` |
| `order_type` | yes | string | usually `limit` for multi-leg |
| `time_in_force` | yes | string | `day`, `gtc`, `ioc`, `fok` |
| `account_id` | yes | number | destination account |
| `limit_price` | conditional | number | required for `limit` and `stop_limit` |
| `stop_price` | conditional | number | required when order type/payload needs stop price |

Representative response:

```json
{
  "id": 843,
  "created_at": "2026-03-17T14:19:07.444Z",
  "updated_at": "2026-03-17T14:19:07.444Z",
  "user_id": 1,
  "asset_id": 23,
  "account_id": 304,
  "external_id": "draft-843",
  "type": 1,
  "action": "buy",
  "direction": "debit",
  "total_units": 1,
  "filled_units": 0,
  "canceled_units": 0,
  "execution_price": null,
  "status": "draft",
  "order_type": "limit",
  "limit_price": { "amount": 2.35, "currency": "USD" },
  "stop_price": null,
  "time_in_force": "day",
  "placed_at": null,
  "executed_at": null,
  "error_message": null,
  "fee": null,
  "legs": [
    {
      "occ": "260620P00580000",
      "type": "option",
      "action": "buy",
      "quantity": 1,
      "execution_price": null,
      "position_effect": "open"
    },
    {
      "occ": "260620P00570000",
      "type": "option",
      "action": "sell",
      "quantity": 1,
      "execution_price": null,
      "position_effect": "open"
    }
  ],
  "asset": {
    "id": 23,
    "name": "SPDR S&P 500 ETF Trust",
    "ticker": "SPY"
  }
}
```

Behavior:
- normally creates a draft
- for some users, create may place immediately based on account settings
- always inspect the returned `status`

---

## 8. Execute Trade

```http
POST /api/tool/execute
Content-Type: application/json
```

Request:

```json
{
  "toolName": "execute_trade",
  "params": {
    "trade_id": 842
  }
}
```

Required params:

| field | required | type | notes |
|---|---|---|---|
| `trade_id` | yes | number | must refer to a trade that is still executable |

Representative response:

```json
{
  "id": 842,
  "external_id": "114",
  "status": "placed",
  "placed_at": "2026-03-17T14:21:54.937Z",
  "executed_at": null,
  "order_type": "limit",
  "time_in_force": "day",
  "asset": {
    "id": 88,
    "name": "Tesla, Inc.",
    "ticker": "TSLA"
  }
}
```

Use this as the explicit commit step when the create call returned a still-executable draft.

---

## 9. Session URLs

```http
POST /api/session/url
Content-Type: application/json
```

### Connect request

```json
{
  "target": "connect"
}
```

### Brokerage-specific connect request

```json
{
  "target": "connect",
  "brokerageId": 1
}
```

### Connect response

```json
{
  "feature": "connect",
  "url": "https://alpha.tradeit.app/connect?token=...&embedded=1",
  "expiresAt": "2026-02-28T05:03:21.650Z"
}
```

### Trade request

```json
{
  "target": "trade"
}
```

### Trade response

```json
{
  "feature": "trade",
  "url": "https://alpha.tradeit.app/t/[ticker]?token=...&embedded=1",
  "expiresAt": "2026-02-28T05:04:39.056Z",
  "placeholder": "[ticker]"
}
```

Use these when the user should finish the step in Trade It's UI rather than a pure API flow.

---

## Design guidance for agents

### Preferred API-native sequence
1. `get_accounts`
2. `create_trade` or `create_options_trade`
3. inspect returned status
4. explicit user confirmation only if still draft
5. `execute_trade` only if still draft

### Preferred browser handoff sequence
1. `POST /api/session/url` with `target: "connect"` when unlinked
2. `POST /api/session/url` with `target: "trade"` when ready for hosted review