# Query Orders [â](#query-orders)

## Query Order List [â](#query-order-list)

### Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/takers/orders`

**Description**: Query orders locked or filled by taker, supports status filtering, pagination, and sorting

**Authentication**: API Key credential authentication

### Query Parameters [â](#query-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| status | string | No | Order status, multiple statuses separated by commas |
| ticker | string | No | Stock symbol |
| exchange | int | No | Exchange ID |
| is_buy | boolean | No | Whether buy order |
| created_after | long | No | Created after (Unix timestamp) |
| created_before | long | No | Created before (Unix timestamp) |
| sort_by | string | No | Sort field (created_at, locked_at, price), default created_at |
| sort_order | string | No | Sort direction (asc, desc), default desc |
| page | int | No | Page number, default 1 |
| page_size | int | No | Page size, default 20, max 100 |

### Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| total | int | Total records |
| page | int | Current page |
| page_size | int | Page size |
| total_pages | int | Total pages |
| orders | array | Order list |

#### Order Object Fields [â](#order-object-fields)

| Field | Type | Description |
| --- | --- | --- |
| order_hash | string | Order hash |
| maker | string | Order creator address |
| principal | string | Recipient address |
| is_buy | boolean | Whether buy order |
| ticker | string | Stock symbol |
| exchange | int | Exchange ID |
| asset | string | Asset token address |
| price | string | Price (wei unit) |
| quantity | string | Quantity (wei unit) |
| incentive | string | Incentive amount (wei unit) |
| deadline | long | Deadline timestamp (Unix timestamp) |
| nonce | long | Anti-replay nonce |
| signature | string | Order signature |
| status | string | Order status |
| created_at | string | Creation time (ISO 8601 format) |
| locked_by | string | Locked by address (optional) |
| locked_at | string | Lock time (optional) |
| reference_id | string | Reference ID (optional) |
| tx_hash | string | Transaction hash (optional) |

### Request Example [â](#request-example)

```bash
curl -X GET "/api/v1/takers/orders?status=locked,partially_filled&page=1&page_size=20" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json"
```

### Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "total": 50,
        "page": 1,
        "page_size": 20,
        "total_pages": 3,
        "orders": [
            {
                "order_hash": "0x1234567890abcdef...",
                "maker": "0x1234567890123456789012345678901234567890",
                "principal": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
                "is_buy": true,
                "ticker": "AAPL",
                "exchange": 0,
                "asset": "0x0000000000000000000000000000000000000001",
                "price": "150250000000000000000",
                "quantity": "10000000000000000000",
                "incentive": "1000000000000000000",
                "deadline": 1735689600,
                "nonce": 1,
                "signature": "0x...",
                "status": "locked",
                "created_at": "2025-01-17T03:00:24Z",
                "locked_by": "0xabcdef1234567890...",
                "locked_at": "2025-01-17T03:05:00Z",
                "reference_id": "REF123456"
            }
        ]
    }
}
```

---

## Get Single Order [â](#get-single-order)

### Endpoint Information [â](#endpoint-information-1)

**Endpoint**: `GET /api/v1/takers/orders/:order_hash`

**Description**: Get detailed information of a single order by order hash

**Authentication**: API Key credential authentication

### Path Parameters [â](#path-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| order_hash | string | Yes | Order hash |

### Response Parameters [â](#response-parameters-1)

| Field | Type | Description |
| --- | --- | --- |
| id | string | Order ID (UUID) |
| maker | string | Order creator address |
| principal | string | Recipient address |
| is_buy | boolean | Whether buy order |
| ticker | string | Stock symbol |
| exchange | int | Exchange ID |
| asset | string | Asset token address |
| price | string | Price (wei unit) |
| quantity | string | Quantity (wei unit) |
| incentive | string | Incentive amount (wei unit) |
| deadline | int | Deadline (Unix timestamp) |
| nonce | int | Anti-replay nonce |
| signature | string | Order signature |
| order_hash | string | Order hash |
| status | string | Order status |
| filled_quantity | string | Filled quantity (wei unit) |
| notes | string | Notes (optional) |
| created_at | string | Creation time (ISO 8601 format) |
| updated_at | string | Update time (ISO 8601 format) |

### Request Example [â](#request-example-1)

```bash
curl -X GET "/api/v1/takers/orders/0x123456abcdef..." \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json"
```

### Response Example [â](#response-example-1)

```json
{
    "code": 0,
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "maker": "0x1234567890123456789012345678901234567890",
        "principal": "0x1234567890123456789012345678901234567890",
        "is_buy": true,
        "ticker": "AAPL",
        "exchange": 0,
        "asset": "0x09671802Cc9Bbf6402f2e7a07b220Aa7b43D8c91",
        "price": "150250000000000000000",
        "quantity": "10000000000000000000",
        "incentive": "100000000000000000",
        "deadline": 1735660800,
        "nonce": 1,
        "signature": "0xabcdef123456...",
        "order_hash": "0x123456abcdef...",
        "status": "locked",
        "filled_quantity": "0",
        "notes": null,
        "created_at": "2025-01-17T03:00:24Z",
        "updated_at": "2025-01-17T03:05:00Z"
    }
}
```

### Notes [â](#notes)

- Can only query orders that Taker has locked or filled
- Will return error if order does not exist or access is unauthorized
- Recommend using this endpoint to get the latest order status
