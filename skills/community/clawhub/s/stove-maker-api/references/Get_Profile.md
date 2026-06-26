# Get Profile [â](#get-profile)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/makers/profiles`

**Description**: Get account profile

**Authentication**: `Authorization` header with JWT token

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| wallet_address | string | Web3 wallet address |
| username | string | Username |
| email | string | Email address |
| avatar_url | string | Avatar URL |
| status | string | User status. See MakerStatus enum type description |

## Request Example [â](#request-example)

```bash
curl -X GET "/api/v1/makers/profiles" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json"
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "wallet_address": "0x1234567890123456789012345678901234567890",
        "username": "trader123",
        "email": "trader@example.com",
        "avatar_url": "https://example.com/avatar.png",
        "status": "active"
    }
}
```

## Enum Types [â](#enum-types)

### MakerStatus - User Status [â](#makerstatus-user-status)

| Enum | Index | Description |
| --- | --- | --- |
| active | 1 | Active |
| inactive | 2 | Inactive |
| suspended | 3 | Suspended |
