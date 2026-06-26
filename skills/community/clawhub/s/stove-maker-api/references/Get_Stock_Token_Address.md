# Get Stock Token Address [â](#get-stock-token-address)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/instruments/token-address`

**Description**: Get the token contract address for a stock based on ticker and exchange ID

**Authentication**: `Authorization` header with JWT token

## Request Parameters [â](#request-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| ticker | string | Yes | Stock ticker symbol (e.g., AAPL) |
| exchange | number | Yes | Exchange ID, see [Exchange enum](./overview.html#exchange-exchange-code) |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| ticker | string | Stock ticker symbol |
| name | string | Stock name |
| exchange_id | number | Exchange ID |
| token_address | string | Token contract address |

## Request Example [â](#request-example)

```bash
curl -X GET "/api/v1/instruments/token-address?ticker=AAPL&exchange=0" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json"
```

## Response Examples [â](#response-examples)

### Success Response [â](#success-response)

```json
{
  "code": 0,
  "data": {
    "ticker": "AAPL",
    "name": "Apple Inc.",
    "exchange_id": 0,
    "token_address": "0x1234567890abcdef..."
  }
}
```

### Error Responses [â](#error-responses)

**Missing ticker parameter**:

```json
{
  "error": "ticker parameter is required"
}
```

**Missing exchange parameter**:

```json
{
  "error": "exchange parameter is required"
}
```

**Stock not found**:

```json
{
  "error": "Instrument not found"
}
```

## Use Cases [â](#use-cases)

- Query token address before creating an order
- Verify if a stock is available on the platform
- Get basic information about a stock
