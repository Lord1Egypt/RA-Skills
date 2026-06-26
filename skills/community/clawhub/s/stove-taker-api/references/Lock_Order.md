# Lock Order [â](#lock-order)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `POST /api/v1/orders/lock`

**Description**: Lock order for filling

**Authentication**: API Key credential authentication

## Request Parameters [â](#request-parameters)

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| order_hash | string | Yes | Order hash |
| taker_address | string | Yes | Taker address |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| success | boolean | Whether lock succeeded |
| order_hash | string | Order hash |
| locked_by | string | Locked by |
| locked_at | string | Lock time |
| expires_at | string | Lock expiration time |

## Request Example [â](#request-example)

```bash
curl -X POST "/api/v1/orders/lock" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "order_hash": "0x1234567890abcdef...",
       "taker_address": "0xabcdef1234567890..."
     }'
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "success": true,
        "order_hash": "0x1234567890abcdef...",
        "locked_by": "0xabcdef1234567890...",
        "locked_at": "2025-01-17T03:00:24Z",
        "expires_at": "2025-01-17T04:00:24Z"
    }
}
```

## Notes [â](#notes)

- After locking, other Takers cannot operate on this order
- Lock has time limit, automatically unlocks after expiration
- Order filling operations can be performed during lock period
