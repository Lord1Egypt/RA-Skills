---
name: whentomeet
description: WhenToMeet group scheduling via public REST API.
metadata: {"openclaw":{"emoji":"📅","requires":["api-key"]}}
---

# WhenToMeet

**Base URL:** `https://whentomeet.io/api/v1/`
**OpenAPI Spec:** `https://whentomeet.io/api/openapi.json`
**Authentication:** `Authorization: Bearer sk_YOUR_API_KEY_HERE`

## Request/Response Format

**Request Format:**
- **GET requests:** Query parameters (e.g., `?limit=10&offset=0`)
- **POST requests:** Plain JSON body (e.g., `{"title": "My Event"}`)
- **No wrapper objects** - send plain JSON directly

**Response Format:**
- All responses return plain JSON with ISO 8601 date strings
- No envelope or wrapping

**Date Format:** ISO 8601 strings (e.g., `"2026-03-14T14:00:00Z"`)

## Data Model

### Event Object
- `id`: UUID
- `title`: string (1-255 chars)
- `description`: string (optional, max 4096 chars)
- `status`: "PLANNING" | "FINALIZED"
- `publicUrl`: Full URL to event page
- `organizerId`: UUID
- `createdAt`: ISO 8601 timestamp
- `modificationPolicy`: "EVERYONE" | "ORGANIZER"
- `outputCalendarId`: UUID (optional, for finalizing events to calendar)
- `slotCount`: number of time slots

### Time Slot Object
- `id`: UUID
- `eventId`: UUID
- `startTime`: ISO 8601 timestamp
- `endTime`: ISO 8601 timestamp
- `timezone`: IANA timezone identifier (optional, e.g., "Europe/Berlin")
- `availabilities`: array of participant responses

## Create Event

**POST** `/api/v1/events`

```bash
curl -X POST "https://whentomeet.io/api/v1/events" \
  -H "Authorization: Bearer sk_YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Event",
    "description": "Optional description",
    "slots": [
      {"startTime": "2026-03-14T14:00:00Z", "endTime": "2026-03-14T16:00:00Z"},
      {"startTime": "2026-03-15T14:00:00Z", "endTime": "2026-03-15T16:00:00Z"}
    ],
    "modificationPolicy": "EVERYONE"
  }'
```

**Request Fields:**

| Field              | Type   | Required | Notes                                  |
|--------------------|--------|----------|----------------------------------------|
| title              | string | yes      | 1-255 chars                            |
| description        | string | no       | max 4096 chars                         |
| slots              | array  | yes      | min 1 slot; each has startTime, endTime (ISO 8601), optional timezone |
| modificationPolicy  | string | no       | "EVERYONE" or "ORGANIZER" (default)    |
| outputCalendarId   | string | no       | UUID of calendar to create final event in |

**Response:**
```json
{
  "id": "uuid",
  "title": "My Event",
  "description": "Optional description",
  "status": "PLANNING",
  "publicUrl": "https://whentomeet.io/events/uuid",
  "slotCount": 2,
  "createdAt": "2026-03-14T14:00:00Z"
}
```

## List Events

**GET** `/api/v1/events`

```bash
curl -X GET "https://whentomeet.io/api/v1/events?limit=10&offset=0&status=PLANNING" \
  -H "Authorization: Bearer sk_YOUR_API_KEY_HERE"
```

**Query Parameters:**

| Field  | Type   | Required | Notes                          |
|--------|--------|----------|--------------------------------|
| limit  | number | no       | 1-100, default 10             |
| offset | number | no       | default 0                      |
| status | string | no       | "PLANNING" or "FINALIZED"      |

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "My Event",
    "description": "...",
    "status": "PLANNING",
    "slotCount": 2,
    "publicUrl": "https://whentomeet.io/events/uuid",
    "createdAt": "2026-03-14T14:00:00Z"
  }
]
```

## Get Event Details

**GET** `/api/v1/events/{eventId}`

```bash
curl -X GET "https://whentomeet.io/api/v1/events/{eventId}" \
  -H "Authorization: Bearer sk_YOUR_API_KEY_HERE"
```

**Response:**
```json
{
  "id": "uuid",
  "title": "My Event",
  "description": "...",
  "status": "PLANNING",
  "organizerId": "uuid",
  "createdAt": "2026-03-14T14:00:00Z",
  "modificationPolicy": "EVERYONE",
  "outputCalendarId": null,
  "slots": [
    {
      "id": "uuid",
      "eventId": "uuid",
      "startTime": "2026-03-14T14:00:00Z",
      "endTime": "2026-03-14T16:00:00Z",
      "availabilities": [
        {
          "id": "uuid",
          "slotId": "uuid",
          "userId": null,
          "displayName": "John Doe",
          "status": "available",
          "user": null
        }
      ]
    }
  ]
}
```

## Delete Event

**DELETE** `/api/v1/events/{eventId}`

```bash
curl -X DELETE "https://whentomeet.io/api/v1/events/{eventId}" \
  -H "Authorization: Bearer sk_YOUR_API_KEY_HERE"
```

**Response:**
```json
{
  "success": true
}
```

## Other Endpoints

### List Bookings

**GET** `/api/v1/bookings`

```bash
curl -X GET "https://whentomeet.io/api/v1/bookings?limit=10&status=confirmed" \
  -H "Authorization: Bearer sk_YOUR_API_KEY_HERE"
```

**Query Parameters:**
- `limit`: 1-100, default 10
- `offset`: default 0
- `status`: "confirmed" or "cancelled"

### List Calendar Connections

**GET** `/api/v1/calendar/connections`

```bash
curl -X GET "https://whentomeet.io/api/v1/calendar/connections" \
  -H "Authorization: Bearer sk_YOUR_API_KEY_HERE"
```

Lists all connected calendar accounts (Google, Microsoft, CalDAV, iCal).

### Get Event Statistics

**GET** `/api/v1/analytics/events`

```bash
curl -X GET "https://whentomeet.io/api/v1/analytics/events?dateFrom=2026-01-01T00:00:00Z&dateTo=2026-03-13T23:59:59Z" \
  -H "Authorization: Bearer sk_YOUR_API_KEY_HERE"
```

**Query Parameters:**
- `dateFrom`: ISO 8601 start date (optional, defaults to 30 days ago)
- `dateTo`: ISO 8601 end date (optional, defaults to now)

**Response:**
```json
{
  "totalEvents": 42,
  "finalizedEvents": 28,
  "dateRange": {
    "from": "2026-01-01T00:00:00Z",
    "to": "2026-03-13T23:59:59Z"
  }
}
```

## Error Codes

| HTTP Status | Code               | Meaning                                             |
|-------------|--------------------|-----------------------------------------------------|
| 400         | BAD_REQUEST        | Invalid input (check zodError in response for field details) |
| 401         | UNAUTHORIZED       | Missing or invalid API key                          |
| 403         | FORBIDDEN          | Insufficient permissions or subscription tier         |
| 404         | NOT_FOUND          | Resource not found or not owned by you              |
| 429         | TOO_MANY_REQUESTS  | Rate limit exceeded                                 |
| 500         | INTERNAL_SERVER_ERROR | Server error                                        |

**Error Response Format:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Event not found or access denied"
  }
}
```

## Rate Limits

| Tier           | Limit                     |
|----------------|---------------------------|
| Free           | 32 requests (lifetime total)|
| Plus           | 1,000 requests per hour    |
| Plus Lifetime  | 1,000 requests per hour    |

Check response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Getting an API Key

1. Sign up for a [Plus or Plus Lifetime subscription](https://whentomeet.io/pricing)
2. Navigate to [API Keys settings](https://whentomeet.io/settings/api-keys)
3. Click "Create API Key" and copy your key (shown only once)

## Example: Complete Event Workflow

```bash
# 1. Create event
EVENT_RESPONSE=$(curl -X POST "https://whentomeet.io/api/v1/events" \
  -H "Authorization: Bearer sk_YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "description": "Weekly sync",
    "slots": [
      {"startTime": "2026-03-14T10:00:00Z", "endTime": "2026-03-14T11:00:00Z"},
      {"startTime": "2026-03-14T14:00:00Z", "endTime": "2026-03-14T15:00:00Z"}
    ],
    "modificationPolicy": "EVERYONE"
  }')

# Extract event ID
EVENT_ID=$(echo $EVENT_RESPONSE | jq -r '.id')
PUBLIC_URL=$(echo $EVENT_RESPONSE | jq -r '.publicUrl')

echo "Event created: $PUBLIC_URL"

# 2. List events
curl -X GET "https://whentomeet.io/api/v1/events" \
  -H "Authorization: Bearer sk_YOUR_API_KEY_HERE"

# 3. Get event details with participant responses
curl -X GET "https://whentomeet.io/api/v1/events/$EVENT_ID" \
  -H "Authorization: Bearer sk_YOUR_API_KEY_HERE"

# 4. Delete event (cleanup)
curl -X DELETE "https://whentomeet.io/api/v1/events/$EVENT_ID" \
  -H "Authorization: Bearer sk_YOUR_API_KEY_HERE"
```
