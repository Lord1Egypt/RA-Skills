# Cancel Order [â](#cancel-order)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `POST /api/v1/orders/{order_id}/cancel`

**Description**: Cancel an unfilled order

**Authentication**: `Authorization` header with JWT token

## Request Parameters [â](#request-parameters)

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| order_id | uuid | Yes | Order ID (route parameter) |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| success | bool | Whether cancellation succeeded |
| order_id | uuid | Order ID |
| message | string | Result description |

## Request Example [â](#request-example)

```bash
curl -X POST "/api/v1/orders/550e8400-e29b-41d4-a716-446655440000/cancel" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json"
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "success": true,
        "order_id": "550e8400-e29b-41d4-a716-446655440000",
        "message": "Order cancelled successfully"
    }
}
```
