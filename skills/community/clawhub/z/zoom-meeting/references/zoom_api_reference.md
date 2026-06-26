# Zoom API Reference

## Authentication

This skill uses **Zoom Server-to-Server OAuth** for authentication.

### Credential File

Credentials are stored in:
```
~/.openclaw/credentials/zoom.json
```

Format:
```json
{
  "account_id": "YOUR_ACCOUNT_ID",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

### Token Flow

1. Read credentials from file
2. Request access token from `https://zoom.us/oauth/token`
3. Use token in `Authorization: Bearer <token>` header
4. Token expires after 3600 seconds (1 hour)
5. Automatically refresh when expired

## API Endpoints

### Create Meeting

**Endpoint:** `POST /users/me/meetings`

**Request Body:**
```json
{
  "topic": "Meeting Title",
  "type": 2,
  "start_time": "2026-03-10T10:00:00",
  "duration": 40,
  "timezone": "Asia/Aqtobe",
  "settings": {
    "join_before_host": true,
    "mute_upon_entry": false,
    "waiting_room": false
  }
}
```

**Response:**
```json
{
  "id": "123456789",
  "join_url": "https://zoom.us/j/123456789",
  "password": "983421",
  "topic": "Meeting Title",
  "start_time": "2026-03-10T10:00:00",
  "duration": 40,
  "timezone": "Asia/Aqtobe"
}
```

### Get Meeting

**Endpoint:** `GET /meetings/{meetingId}`

**Response:**
```json
{
  "id": "123456789",
  "join_url": "https://zoom.us/j/123456789",
  "password": "983421",
  "topic": "Meeting Title",
  "start_time": "2026-03-10T10:00:00",
  "duration": 40,
  "timezone": "Asia/Aqtobe",
  "status": "waiting"
}
```

### List Meetings

**Endpoint:** `GET /users/me/meetings`

**Response:**
```json
{
  "meetings": [
    {
      "id": "123456789",
      "topic": "Meeting Title",
      "start_time": "2026-03-10T10:00:00",
      "duration": 40,
      "join_url": "https://zoom.us/j/123456789"
    }
  ]
}
```

### Delete Meeting

**Endpoint:** `DELETE /meetings/{meetingId}`

**Response:** `204 No Content`

## Meeting Types

| Type | Value | Description |
|------|-------|-------------|
| Instant | 1 | Instant meeting |
| Scheduled | 2 | Scheduled meeting |
| Recurring (fixed) | 3 | Recurring with fixed time |
| Recurring (no fixed time) | 8 | Recurring without fixed time |

This skill uses **type 2** (Scheduled) for all created meetings.

## Default Values

| Parameter | Default |
|-----------|---------|
| start_time | Current time |
| duration | 40 minutes |
| timezone | Asia/Aqtobe |

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid/expired token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Meeting doesn't exist |
| 429 | Rate Limited - Too many requests |
| 500 | Internal Server Error |

## Error Response Format

```json
{
  "code": 1212,
  "errorMessage": "Invalid meeting ID"
}
```

## Timezone Format

Use IANA timezone database names:
- `Asia/Aqtobe`
- `America/New_York`
- `Europe/London`
- `Asia/Almaty`

## Start Time Format

ISO 8601 format:
- `2026-03-10T10:00:00`
- `2026-03-10T10:00:00Z` (UTC)
- `2026-03-10T10:00:00+06:00` (with offset)
