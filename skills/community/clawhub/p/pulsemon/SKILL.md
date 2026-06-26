---
name: pulsemon
description: Monitor cron jobs and background tasks with PulseMon. Check monitor status, create/update/delete monitors, view incidents, and manage alerts.
metadata:
  openclaw:
    requires:
      env:
        - PULSEMON_API_KEY
---

# PulseMon Skill

Monitor your cron jobs and background tasks through PulseMon.

## Setup

The user needs a PulseMon API key. They can generate one at https://pulsemon.dev/dashboard/settings under "API Keys".

Store it as the environment variable `PULSEMON_API_KEY`.

## Base URL

All API requests go to: `https://pulsemon.dev/api/v1`

## Authentication

Every request must include the header:

```
Authorization: Bearer {PULSEMON_API_KEY}
```

## Available Actions

### List all monitors

`GET /api/v1/monitors`

Returns an array of monitors with their name, slug, status (up/down/waiting/paused), last ping time, and expected interval.

### Get a specific monitor

`GET /api/v1/monitors/{id}`

Returns full monitor details including recent pings and incidents.

### Create a monitor

`POST /api/v1/monitors`

```
Content-Type: application/json
```

Body:

```json
{
  "name": "Nightly Backup",
  "slug": "nightly-backup",
  "expectedInterval": 86400,
  "gracePeriod": 300,
  "tags": ["production"]
}
```

- **name**: Human-readable name (required, 1-100 characters)
- **slug**: URL-safe identifier, lowercase letters, numbers, and hyphens only (required, 3-60 characters)
- **expectedInterval**: Seconds between expected pings (required, minimum 10, maximum 2592000)
- **gracePeriod**: Extra seconds before alerting (optional, 0-86400, defaults to a sensible value based on the interval)
- **tags**: Array of string tags for organisation (optional)
- **maxDuration**: Max allowed run time in milliseconds (optional, null to disable). Alerts if a ping reports a duration exceeding this threshold.

### Update a monitor

`PATCH /api/v1/monitors/{id}`

```
Content-Type: application/json
```

Body: any of these fields (at least one required):

- **name**: string (1-100 characters)
- **expectedInterval**: number (10-2592000)
- **gracePeriod**: number (0-86400)
- **isPaused**: boolean
- **tags**: array of strings
- **maxDuration**: number or null (milliseconds)

### Delete a monitor

`DELETE /api/v1/monitors/{id}`

### Pause a monitor

`POST /api/v1/monitors/{id}/pause`

### Resume a monitor

`POST /api/v1/monitors/{id}/resume`

### List pings for a monitor

`GET /api/v1/monitors/{id}/pings?limit=20&offset=0`

### List incidents for a monitor

`GET /api/v1/monitors/{id}/incidents?limit=20&offset=0`

### Ping a monitor

Pings are sent directly to the ping endpoint (no API key needed):

`GET https://pulsemon.dev/api/ping/{slug}`

Optional query params:
- **status**: "success" (default), "fail", or "start"
- **duration**: Job duration in milliseconds

`POST https://pulsemon.dev/api/ping/{slug}` with JSON body:

```json
{
  "status": "success",
  "duration": 1234,
  "body": "Processed 500 records"
}
```

- **status=start**: Signals a job has begun. Enables overlap detection. Does not reset the deadline.
- **status=success**: Signals the job completed. Resets the deadline.
- **status=fail**: Records a failure. Does not reset the deadline.
- **body**: Job output (up to 10 KB). Included in alert notifications.
- **duration**: Job run time in ms. Checked against maxDuration threshold if set.

## Response Format

All responses are JSON with this shape:

```json
{
  "data": { ... },
  "error": null
}
```

On error:

```json
{
  "data": null,
  "error": { "code": "NOT_FOUND", "message": "Monitor not found" }
}
```

## Common Intervals

When the user says a time like "every hour" or "daily", convert to seconds:

- Every minute: 60
- Every 5 minutes: 300
- Every 15 minutes: 900
- Every 30 minutes: 1800
- Every hour: 3600
- Every 6 hours: 21600
- Every 12 hours: 43200
- Daily: 86400
- Weekly: 604800

## Guidelines

- When listing monitors, show name, status, and last ping time in a readable format.
- When a monitor is "down", mention how long it's been down.
- When creating a monitor, suggest a sensible grace period if the user doesn't specify one (e.g. 10% of the interval, minimum 30 seconds).
- After creating a monitor, show the user the ping URL: `https://pulsemon.dev/api/ping/{slug}`
- Always confirm before deleting a monitor.
- When the user says "check my monitors" or similar, use the list endpoint and summarise the results.
- Format durations in human-readable form (e.g. "2 hours ago" instead of a raw timestamp).
