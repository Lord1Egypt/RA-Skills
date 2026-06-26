# Unlock Order [â](#unlock-order)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `POST /api/v1/orders/unlock`

**Description**: Unlock order

**Authentication**: API Key credential authentication

## Request Parameters [â](#request-parameters)

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| order_hash | string | Yes | Order hash |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| success | boolean | Whether unlock succeeded |
| order_hash | string | Order hash |
| message | string | Result description |

## Request Example [â](#request-example)

```bash
curl -X POST "/api/v1/orders/unlock" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "order_hash": "0x1234567890abcdef..."
     }'
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "success": true,
        "order_hash": "0x1234567890abcdef...",
        "message": "Order unlocked successfully"
    }
}
```

## Notes [â](#notes)

- Can only unlock orders locked by yourself
- After unlocking, order returns to pending status
- Other Takers can re-lock the order
