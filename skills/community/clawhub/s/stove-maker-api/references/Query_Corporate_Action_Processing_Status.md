# Query Corporate Action Processing Status [â](#query-corporate-action-processing-status)

**Endpoint**: `GET /api/v1/maker/corporate-actions/token/{token}/processing-status`

**Description**: Query if there are corporate actions being processed

**Authentication**: JWT token in `Authorization` header

**Request Parameters**:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| token | string | Yes | Route parameter, stock token address |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| code | int | Result code. 0 for success |
| data | object | Result object |
| data.is_processing | bool | Whether there are corporate actions being processed |

## Request Example [â](#request-example)

```bash
curl "api/v1/corporate-actions/maker/0x5fc23eB93208F58e29A1AC493dc15FD0b0Cb5C92/token/0x1c6611cde556f439252c2845c33702c3035fe351/processing-status"
```

## Response Example [â](#response-example)

```json
{
  "code": 0,
  "data": {
    "is_processing": false
  }
}
```
