# Query Pending Corporate Actions [â](#query-pending-corporate-actions)

**Endpoint**: `GET /api/v1/maker/corporate-actions/pending`

**Description**: Get all pending corporate actions

**Authentication**: JWT token in `Authorization` header

**Request Parameters**:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| token | string | No | URL parameter, stock token address |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| code | int | Result code. 0 for success |
| data | object | Result object |
| data.actions | object array | Corporate action object array |
| data.actions[].id | uuid | Action record id |
| data.actions[].maker | string | Maker |
| data.actions[].holding_qty | string | Holding quantity |
| data.actions[].token_address | string | Stock token address |
| data.actions[].action_qty | string | Execution quantity |
| data.actions[].action_type | enum | Action type (dividend, stock_split, reverse_stock_split, delisting) |
| data.actions[].compensation_qty | string | Compensation quantity |
| data.actions[].create_at | string | Creation time |
| data.actions[].params | object | Other parameters |

## Dividend params [â](#dividend-params)

| Field | Type | Description |
| --- | --- | --- |
| data.actions[].params.dividend_per_share | string | Dividend amount per token |
| data.actions[].params.tax_rate | string | Dividend tax rate % |
| data.actions[].params.fee_amount | string | Fee (USD) |

## Stock Split params [â](#stock-split-params)

| Field | Type | Description |
| --- | --- | --- |
| data.actions[].params.split_ratio | string | Split ratio |
| data.actions[].params.compensation_per_share | string | Compensation amount per share |
| data.actions[].params.fee_amount | string | Fee (USD) |

## Reverse Stock Split params [â](#reverse-stock-split-params)

| Field | Type | Description |
| --- | --- | --- |
| data.actions[].params.merge_ratio | string | Merge ratio |
| data.actions[].params.compensation_per_share | string | Compensation amount per share |
| data.actions[].params.fee_amount | string | Fee (USD) |

## Delisting params [â](#delisting-params)

| Field | Type | Description |
| --- | --- | --- |
| data.actions[].params.compensation_per_share | string | Compensation amount per share |
| data.actions[].params.fee_amount | string | Fee (USD) |

## Request Example [â](#request-example)

```bash
# Query all pending corporate actions
curl "api/v1/corporate-actions/maker/0x5fc23eB93208F58e29A1AC493dc15FD0b0Cb5C92/pending"

# Query pending corporate actions for a specific token
curl "api/v1/corporate-actions/maker/0x5fc23eB93208F58e29A1AC493dc15FD0b0Cb5C92/pending?token=0x1c6611cde556f439252c2845c33702c3035fe351"
```

## Response Example [â](#response-example)

```json
{
  "code": 0,
  "data": {
    "actions": [
      {
        "id": "string",
        "maker": "string",
        "holding_qty": "string",
        "action_qty": "string", 
        "compensation_qty": "string",
        "created_at": "2024-01-01T00:00:00Z",
        "token_address": "string",
        "action_type": "string",
        "params": {}
      }
    ],
    "total_count": 0
  }
}
```
