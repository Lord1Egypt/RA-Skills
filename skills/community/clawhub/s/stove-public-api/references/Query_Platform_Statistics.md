# Query Platform Statistics [â](#query-platform-statistics)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/stats`

**Description**: Get platform statistics, including user count, order count, and stock token count

**Authentication**: Accessible anonymously

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| total_user_addresses | int | User count |
| total_orders | int | Order count |
| total_instruments | int | Stock token count |
| total_balance | string | The sum of all users' holdings on the platform (unit: wei) |
| total_minted_tokens | string | Query the total number of tokens minted (i.e., the cumulative sum of executed buy orders) |
| total_market_value | decimal | Total market value of all positions on the platform |

## Request Example [â](#request-example)

```bash
curl -X GET "/api/v1/stats" \
     -H "Content-Type: application/json"
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "total_user_addresses": 1250,
        "total_orders": 5430,
        "total_instruments": 150,
        "total_balance": "497438",
        "total_minted_tokens": "672273",
        "total_market_value": 1544.32
    }
}
```
