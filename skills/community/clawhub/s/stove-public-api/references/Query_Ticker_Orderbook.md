# Query Ticker Orderbook [â](#query-ticker-orderbook)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/tickers/{symbol}/orderbooks?exchange={exchange}`

**Description**: Query platform orderbook

**Authentication**: Accessible anonymously

## Query Parameters [â](#query-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| symbol | string | Yes | Route parameter, stock symbol |
| exchange | int | Yes | URL parameter, exchange code. See [`Exchange`](./overview.html#exchange-exchange-code) enum type description |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| symbol | string | Stock symbol |
| market | string | Market code enum. See [`Market`](./overview.html#market-market-code) enum type description |
| ask | object array | Ask orders |
| ask[].price | decimal | Price in corresponding market |
| ask[].volume | decimal | Volume |
| bid | object array | Bid orders |
| bid[].price | decimal | Price in corresponding market |
| bid[].volume | decimal | Volume |
| time | string | Time |

## Request Example [â](#request-example)

```bash
curl -X GET "/api/v1/tickers/AAPL/orderbooks?exchange=0" \
     -H "Content-Type: application/json"
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "symbol": "AAPL",
        "market": "usex",
        "ask": [
            {"price": "150.25", "volume": "100"},
            {"price": "150.30", "volume": "200"}
        ],
        "bid": [
            {"price": "150.20", "volume": "150"},
            {"price": "150.15", "volume": "250"}
        ],
        "time": "2025-01-17T03:00:24Z"
    }
}
```
