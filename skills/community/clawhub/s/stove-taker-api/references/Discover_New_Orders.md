# Discover New Orders [â](#discover-new-orders)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/orders/available`

**Description**: Get all available pending orders as a backup method for WebSocket order push

**Authentication**: API Key credential authentication

## Query Parameters [â](#query-parameters)

None

## Response Parameters [â](#response-parameters)

Returns an array of orders, each containing the following fields:

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
| status | string | Order status (fixed as "pending") |
| filled_quantity | string | Filled quantity (wei unit) |
| notes | string | Notes (optional) |
| created_at | string | Creation time (ISO 8601 format) |
| updated_at | string | Update time (ISO 8601 format) |

## Request Example [â](#request-example)

```bash
curl -X GET "/api/v1/orders/available" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json"
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": [
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
        }
    ]
}
```

## Notes [â](#notes)

- This endpoint returns all orders with pending status
- Recommend using WebSocket for order push as primary method, use this endpoint as backup polling method
- Polling interval should be no less than 5 seconds to avoid excessive server load
- The returned order list may be large, filter as needed
