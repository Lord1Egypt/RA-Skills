# Query Maker Positions [â](#query-maker-positions)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/positions`

**Description**: Query held stock token information

**Authentication**: `Authorization` header with JWT token

## Query Parameters [â](#query-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| ticker | string | No | Stock symbol (exact or fuzzy match) |
| ticker_like | boolean | No | Enable fuzzy search, default false |
| page | int | No | Page number, default 1 |
| page_size | int | No | Page size, default 20, max 100 |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| total | int | Total records |
| page | int | Current page |
| page_size | int | Page size |
| total_pages | int | Total pages |
| positions | array | Position list |

### Position Object Field [â](#position-object-field)

| Field | Type | Description |
| --- | --- | --- |
| positions[].ticker | string | Stock symbol |
| positions[].exchange | int | Market code enum index. See [`Exchange`](./../overview.html#exchange-exchange-code) |
| positions[].token_address | string | Token address |
| positions[].balance | string | Position balance |
| positions[].locked_balance | string | Locked position balance |
| positions[].available_balance | string | Available position balance |
| positions[].avg_price | string | average transaction price |

## Request Example [â](#request-example)

```bash
curl -X GET "/api/v1/positions?page=1&page_size=20&ticker_like=true&ticker=AAPL" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json"
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "positions": [
            {
                "ticker": "AAPL",
                "exchange": 0,
                "token_address": "0xc48eec40...",
                "balance": "6",
                "locked_balance": "0",
                "available_balance": "6",
                "avg_price": "256598079145728583333"
            },
            {
                "ticker": "AMZN",
                "exchange": 0,
                "token_address": "0xfd5d300742...",
                "balance": "12",
                "locked_balance": "0",
                "available_balance": "12",
                "avg_price": "233225286432160750000"
            }
        ],
        "total": 2,
        "page": 1,
        "page_size": 20,
        "total_pages": 1
    }
}
```
