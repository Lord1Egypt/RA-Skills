# Query Next Available Nonce [â](#query-next-available-nonce)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/orders/maker/next-nonce`

**Description**: Query the next available order nonce for the Maker

**Authentication**: `Authorization` header with JWT token

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| maker | string | Maker address |
| next_nonce | long | Next available nonce |

## Request Example [â](#request-example)

```bash
curl -X GET "/api/v1/orders/maker/next-nonce" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json"
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "maker": "0x1234567890123456789012345678901234567890",
        "next_nonce": 5
    }
}
```
