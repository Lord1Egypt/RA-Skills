# Cancellation Response [â](#cancellation-response)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `POST /api/v1/orders/cancel-result`

**Description**: When Maker requests to cancel a locked order, Taker returns the cancellation result through this endpoint

**Authentication**: API Key credential authentication

## Use Case [â](#use-case)

When Taker receives a `cancellation_request` message via WebSocket, it needs to:

1. Check if the order can be cancelled (whether trading process has started)
2. If cancellable, execute cancellation operation (unlock order)
3. Call this endpoint to notify the system of cancellation result

## Request Parameters [â](#request-parameters)

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| order_hash | string | Yes | Order hash |
| taker_address | string | Yes | Taker address |
| cancellation_success | boolean | Yes | Whether cancellation succeeded |
| message | string | Yes | Result message |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| success | boolean | Whether API call succeeded |
| message | string | Response message |
| order_hash | string | Order hash |

## Request Examples [â](#request-examples)

### Cancellation Success [â](#cancellation-success)

```bash
curl -X POST "/api/v1/orders/cancel-result" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "order_hash": "0x1234567890abcdef...",
       "taker_address": "0xabcdef1234567890...",
       "cancellation_success": true,
       "message": "Order cancelled successfully"
     }'
```

### Cancellation Failure [â](#cancellation-failure)

```bash
curl -X POST "/api/v1/orders/cancel-result" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "order_hash": "0x1234567890abcdef...",
       "taker_address": "0xabcdef1234567890...",
       "cancellation_success": false,
       "message": "Order already in trading process, cannot cancel"
     }'
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "success": true,
        "message": "Cancellation result recorded",
        "order_hash": "0x1234567890abcdef..."
    }
}
```

## Notes [â](#notes)

- This endpoint must be called after receiving a `cancellation_request` WebSocket message
- If cancellation succeeds (cancellation_success=true), the order will be unlocked and updated to cancelled or expired status
- If cancellation fails (cancellation_success=false), the order remains locked, and Taker should continue to complete the trade
- Recommend responding promptly after receiving cancellation request to avoid timeout
