# Query Ticker Information and Statistics [â](#query-ticker-information-and-statistics)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/tickers/{symbol}/stats?exchange={exchange}`

**Description**: Get statistics for a specific stock, including basic information and trading statistics

**Authentication**: Accessible anonymously

## Query Parameters [â](#query-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| symbol | string | Yes | Route parameter, stock symbol |
| exchange | int | Yes | URL parameter, exchange code. See [`Exchange`](./overview.html#exchange-exchange-code) enum type description |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| ticker | string | Stock symbol |
| name | string | Stock name |
| address | string | Token address |
| exchange | int | Exchange code. See [`Exchange`](./overview.html#exchange-exchange-code) enum type description |
| orders | int | Order count |
| volume | string | Volume |

## Request Example [â](#request-example)

```bash
curl -X GET "/api/v1/tickers/AAPL/stats?exchange=0" \
     -H "Content-Type: application/json"
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "address": "0x1234567890abcdef...",
        "exchange": 0,
        "orders": 150,
        "volume": "50000"
    }
}
```
