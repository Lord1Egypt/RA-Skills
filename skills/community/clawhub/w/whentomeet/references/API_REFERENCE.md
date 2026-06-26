# WhenToMeet API Reference

This document provides complete endpoint documentation for the WhenToMeet API.

## Reference Links

- Interactive API docs: https://docs.whentomeet.io/api-docs
- OpenAPI spec (machine-readable): https://whentomeet.io/api/openapi.json
- LLM-friendly product overview: https://whentomeet.io/llms.txt
- Main site: https://whentomeet.io

## v1 Authenticated Endpoints

All v1 endpoints require Bearer authentication:
```
Authorization: Bearer sk_your_api_key_here
```

### Create Event

**POST** `/api/trpc/v1.event.create`

Create a polling event with proposed time slots.

**Input:**
```json
{
  "json": {
    "title": "Team Standup",
    "description": "Weekly sync",
    "slots": [
      {
        "startTime": "2026-03-01T09:00:00Z",
        "endTime": "2026-03-01T10:00:00Z",
        "timezone": "America/New_York"
      },
      {
        "startTime": "2026-03-02T09:00:00Z",
        "endTime": "2026-03-02T10:00:00Z",
        "timezone": "America/New_York"
      }
    ],
    "modificationPolicy": "ORGANIZER"
  }
}
```

**Fields:**

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
  "result": {
    "data": {
      "json": {
        "id": "uuid",
        "title": "Team Standup",
        "description": "Weekly sync",
        "status": "PLANNING",
        "publicUrl": "https://whentomeet.io/event/uuid",
        "createdAt": "2026-02-25T12:00:00.000Z"
      }
    }
  }
}
```

---

### Get Event

**GET** `/api/trpc/v1.event.get`

Retrieve event details including all slots and participant responses. Only accessible by the event organizer.

**Input:**
```json
{
  "json": {
    "eventId": "uuid"
  }
}
```

**Response:** Includes `slots[]` with nested `availabilities[]`, each containing:
- `displayName` — participant name
- `status` — "available", "maybe", or "unavailable"
- `user` — linked user info (if authenticated participant)

---

### List Events

**GET** `/api/trpc/v1.event.list`

List your events with pagination and optional status filter.

**Input:**
```json
{
  "json": {
    "limit": 10,
    "offset": 0,
    "status": "PLANNING"
  }
}
```

**Fields:**

| Field  | Type   | Required | Notes                          |
|--------|--------|----------|--------------------------------|
| limit  | number | no       | 1-100, default 10             |
| offset | number | no       | default 0                      |
| status | string | no       | "PLANNING" or "FINALIZED"      |

---

### Delete Event

**POST** `/api/trpc/v1.event.delete`

Permanently deletes an event and all associated data. Organizer only.

**Input:**
```json
{
  "json": {
    "eventId": "uuid"
  }
}
```

**Response:**
```json
{
  "result": {
    "data": {
      "json": {
        "success": true
      }
    }
  }
}
```

---

### List Bookings

**GET** `/api/trpc/v1.booking.list`

List bookings made on your bookable scheduling pages.

**Input:**
```json
{
  "json": {
    "limit": 10,
    "offset": 0,
    "status": "confirmed"
  }
}
```

**Fields:**

| Field  | Type   | Required | Notes                          |
|--------|--------|----------|--------------------------------|
| limit  | number | no       | 1-100, default 10             |
| offset | number | no       | default 0                      |
| status | string | no       | "confirmed" or "cancelled"     |

**Response:** Includes `attendeeName`, `attendeeEmail`, `startTime`, `endTime`, `status`, and the associated `bookableEvent`.

---

### List Calendar Connections

**GET** `/api/trpc/v1.calendar.listConnections`

List all connected calendar accounts (Google, Microsoft, CalDAV, iCal).

**Input:** No input required.

**Response:** Returns array of connections with `provider`, `accountEmail`, `isActive`, and `status`.

---

### Event Statistics

**GET** `/api/trpc/v1.analytics.eventStats`

Get event creation statistics within a date range.

**Input:**
```json
{
  "json": {
    "dateFrom": "2026-01-01T00:00:00Z",
    "dateTo": "2026-02-25T23:59:59Z"
  }
}
```

Defaults to last 30 days if no range provided.

**Response:** Returns `totalEvents`, `finalizedEvents`, and `dateRange`.

---

## Public Booking Endpoints

These endpoints let you book time on someone's public scheduling page without authentication.

### Get Available Slots

**GET** `/api/trpc/public.getAvailabilitySlots`

Query open time slots for a user's bookable event. Calendar-aware — excludes times blocked by the user's connected calendars.

**Input:**
```json
{
  "json": {
    "username": "jane",
    "eventSlug": "30min-call"
  }
}
```

---

### Create Booking

**POST** `/api/trpc/public.createBooking`

Book a specific time slot.

**Input:**
```json
{
  "json": {
    "username": "jane",
    "eventSlug": "30min-call",
    "startTime": "2026-03-01T14:00:00Z",
    "attendeeName": "John Doe",
    "attendeeEmail": "john@example.com"
  }
}
```

---

### Get Booking Details

**GET** `/api/trpc/public.getBookingDetails`

Retrieve details of an existing booking (requires email verification).

---

### Cancel Booking

**POST** `/api/trpc/public.cancelBooking`

Cancel a booking (requires email verification).

---

## Error Codes

| HTTP Status | Code               | Meaning                                             |
|-------------|--------------------|-----------------------------------------------------|
| 400         | BAD_REQUEST        | Invalid input (check zodError in response for field details) |
| 401         | UNAUTHORIZED       | Missing or invalid API key                          |
| 403         | FORBIDDEN          | Subscription tier doesn't allow API access         |
| 404         | NOT_FOUND          | Resource not found or not owned by you              |
| 429         | TOO_MANY_REQUESTS  | Rate limit exceeded — check X-RateLimit-Reset header |
| 500         | INTERNAL_SERVER_ERROR | Server error                                        |

When rate limited, wait until the `X-RateLimit-Reset` timestamp before retrying.
