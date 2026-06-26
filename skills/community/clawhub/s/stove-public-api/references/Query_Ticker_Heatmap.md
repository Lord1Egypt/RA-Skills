# Query Ticker Heatmap [â](#query-ticker-heatmap)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/tickers/heatmaps?exchange={exchange}`

**Description**: Query heatmap data for popular market stocks

**Authentication**: Accessible anonymously

## Query Parameters [â](#query-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| exchange | int | Yes | URL parameter, exchange code. See [`Exchange`](./overview.html#exchange-exchange-code) enum type description |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| symbol | string | Stock symbol |
| company_name | string | Company name |
| market_cap | int64 | Market capitalization |
| total_shares | float | Total supply (shares outstanding) |

## Request Example [â](#request-example)

```bash
curl -X GET "/api/v1/tickers/heatmaps?exchange=0" \
     -H "Content-Type: application/json"
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": [
        {
            "symbol": "NVDA",
            "market_cap": 4374494800000,
            "total_shares": 24300000000,
            "company_name": "NVIDIA Corporation"
        },
        {
            "symbol": "AAPL",
            "market_cap": 3872150675000,
            "total_shares": 14681140000,
            "company_name": "Apple Inc."
        }
    ]
}
```
