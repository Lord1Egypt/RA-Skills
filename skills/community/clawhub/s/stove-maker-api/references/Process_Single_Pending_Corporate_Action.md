# Process Single Pending Corporate Action [â](#process-single-pending-corporate-action)

**Endpoint**: `POST /api/v1/maker/corporate-actions/action/{action_id}/process`

**Description**: Authorize processing of a single corporate action

**Authentication**: JWT token in `Authorization` header

**Request Parameters**:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| action_id | string | Yes | Route parameter, corporate action ID |
| asset_token | string | Yes | URL parameter, asset token address |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| code | int | Result code. 0 for success |
| data | object | Result object |
| data.id | uuid | Action record id |
| data.success | bool | Whether execution was successful |
| data.tx_hash | string | Execution transaction hash |
| data.error | string | Error description |

## Request Example [â](#request-example)

```bash
curl -X POST "api/v1/corporate-actions/maker/0x5fc23eB93208F58e29A1AC493dc15FD0b0Cb5C92/action/123/process?asset_token=0x09671802Cc9Bbf6402f2e7a07b220Aa7b43D8c91"
```

## Response Example [â](#response-example)

```json
{
  "code": 0,
  "data": {
    "id": "string",
    "success": true,
    "tx_hash": "0x...",
    "error": null
  }
}
```
