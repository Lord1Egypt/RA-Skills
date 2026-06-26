# Query Order List [â](#query-order-list)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/orders`

**Description**: Flexible order list query with filtering, pagination, and sorting

**Authentication**: `Authorization` header with JWT token

## Query Parameters [â](#query-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| order_hash | string | No | Order hash (exact match) |
| principal | string | No | Recipient address (exact match) |
| ticker | string | No | Stock symbol (exact or fuzzy match) |
| ticker_like | boolean | No | Enable fuzzy search, default false |
| exchange | int | No | Exchange ID (exact match) |
| asset | string | No | Asset token address (exact match) |
| is_buy | boolean | No | Is buy order (exact match) |
| nonce | int | No | Nonce (exact match) |
| price_min | string | No | Minimum price |
| price_max | string | No | Maximum price |
| quantity_min | string | No | Minimum quantity |
| quantity_max | string | No | Maximum quantity |
| incentive_min | string | No | Minimum incentive |
| incentive_max | string | No | Maximum incentive |
| filled_quantity_min | string | No | Minimum filled quantity |
| filled_quantity_max | string | No | Maximum filled quantity |
| status | string | No | Order status, supports multiple (comma-separated, e.g. "pending,filled") |
| deadline_after | int | No | Earliest deadline (Unix timestamp) |
| deadline_before | int | No | Latest deadline (Unix timestamp) |
| created_after | int | No | Earliest creation time (Unix timestamp) |
| created_before | int | No | Latest creation time (Unix timestamp) |
| sort_by | string | No | Sort field (price, quantity, incentive, deadline, created_at), default created_at |
| sort_order | string | No | Sort direction (asc, desc), default desc |
| page | int | No | Page number, default 1 |
| page_size | int | No | Page size, default 20, max 100 |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| total | int | Total records |
| page | int | Current page |
| page_size | int | Page size |
| total_pages | int | Total pages |
| orders | array | Order list |

### Order Object Fields [â](#order-object-fields)

| Field | Type | Description |
| --- | --- | --- |
| id | string | Order ID (UUID) |
| maker | string | Order creator address |
| principal | string | Recipient address |
| is_buy | boolean | Is buy order |
| ticker | string | Stock symbol |
| exchange | int | Exchange ID |
| asset | string | Asset token address |
| price | string | Price (wei unit) |
| quantity | string | Quantity (wei unit) |
| incentive | string | Incentive amount (wei unit) |
| deadline | int | Deadline (Unix timestamp) |
| nonce | int | Nonce |
| signature | string | Order signature |
| order_hash | string | Order hash |
| status | string | Order status |
| filled_quantity | string | Filled quantity (wei unit) |
| notes | string | Notes (optional) |
| created_at | string | Creation time (ISO 8601 format) |
| updated_at | string | Update time (ISO 8601 format) |
| fills | array | Fill details list (only returned for partially_filled and filled status orders) |

### Fill Detail Object Fields [â](#fill-detail-object-fields)

| Field | Type | Description |
| --- | --- | --- |
| id | string | Fill record ID (UUID) |
| order_id | string | Order ID |
| order_hash | string | Order hash |
| taker | string | Taker address |
| fill_quantity | string | Fill quantity (wei unit) |
| fill_amount | string | Fill amount (wei unit) |
| fee_amount | string | Fee amount (wei unit) |
| incentive_amount | string | Incentive amount (wei unit) |
| taker_incentive | string | Taker incentive (wei unit) |
| tx_hash | string | Transaction hash |
| block_number | int | Block number |
| status | string | Fill status |
| reference_id | string | Reference ID (optional) |
| created_at | string | Creation time (ISO 8601 format) |

## Request Example [â](#request-example)

```bash
# Basic query
curl -X GET "/api/v1/orders?ticker=AAPL&page=1&page_size=20" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json"

# Multiple status query
curl -X GET "/api/v1/orders?status=pending,partially_filled" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json"

# Price range query
curl -X GET "/api/v1/orders?price_min=100000000000000000000&price_max=200000000000000000000" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json"
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "total": 3,
        "page": 1,
        "page_size": 20,
        "total_pages": 1,
        "orders": [
            {
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
                "status": "pending",
                "filled_quantity": "0",
                "notes": null,
                "created_at": "2025-01-17T03:00:24Z",
                "updated_at": "2025-01-17T03:00:24Z"
            },
            {
                "id": "660e8400-e29b-41d4-a716-446655440001",
                "maker": "0x1234567890123456789012345678901234567890",
                "principal": "0x1234567890123456789012345678901234567890",
                "is_buy": false,
                "ticker": "TSLA",
                "exchange": 0,
                "asset": "0x09671802Cc9Bbf6402f2e7a07b220Aa7b43D8c91",
                "price": "245000000000000000000",
                "quantity": "5000000000000000000",
                "incentive": "50000000000000000",
                "deadline": 1735747200,
                "nonce": 2,
                "signature": "0x789012fedcba...",
                "order_hash": "0x789012fedcba...",
                "status": "locked",
                "filled_quantity": "0",
                "notes": null,
                "created_at": "2025-01-17T05:30:00Z",
                "updated_at": "2025-01-17T06:15:00Z"
            },
            {
                "id": "770e8400-e29b-41d4-a716-446655440002",
                "maker": "0x1234567890123456789012345678901234567890",
                "principal": "0x1234567890123456789012345678901234567890",
                "is_buy": true,
                "ticker": "GOOGL",
                "exchange": 0,
                "asset": "0x09671802Cc9Bbf6402f2e7a07b220Aa7b43D8c91",
                "price": "138500000000000000000",
                "quantity": "20000000000000000000",
                "incentive": "200000000000000000",
                "deadline": 1735833600,
                "nonce": 3,
                "signature": "0xfedcba987654...",
                "order_hash": "0xfedcba987654...",
                "status": "filled",
                "filled_quantity": "20000000000000000000",
                "notes": null,
                "created_at": "2025-01-16T10:00:00Z",
                "updated_at": "2025-01-17T08:45:00Z",
                "fills": [
                    {
                        "id": "880e8400-e29b-41d4-a716-446655440003",
                        "order_id": "770e8400-e29b-41d4-a716-446655440002",
                        "order_hash": "0xfedcba987654...",
                        "taker": "0x9876543210987654321098765432109876543210",
                        "fill_quantity": "20000000000000000000",
                        "fill_amount": "2770000000000000000000",
                        "fee_amount": "13850000000000000000",
                        "incentive_amount": "200000000000000000",
                        "taker_incentive": "200000000000000000",
                        "tx_hash": "0xabcdef123456789...",
                        "block_number": 12345678,
                        "status": "confirmed",
                        "reference_id": "Taker-1737105945abc",
                        "created_at": "2025-01-17T08:45:00Z"
                    }
                ]
            }
        ]
    }
}
```
