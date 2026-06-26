---
name: zoom
description: |
  Zoom API integration with managed OAuth. Manage meetings, webinars, recordings, and user profiles.
  Use this skill when users want to schedule meetings, manage webinars, get meeting details, list recordings, or retrieve user information.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: "📹"
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Zoom

Access the Zoom API with managed OAuth authentication. Manage meetings, webinars, cloud recordings, and user profiles.

## Quick Start

```bash
# Get current user profile
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoom/v2/users/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/zoom/v2/
```

All endpoints documented below are accessed under this base URL. The gateway proxies requests to `api.zoom.us` and automatically injects your OAuth token. Only the endpoints listed in the API Reference section below are supported.

## Security & Permissions

- The Maton API key acts as a credential — treat it as a secret and do not expose it in client-side code or public repositories
- The OAuth connection grants scoped access to meetings, webinars, recordings, and user profiles on the connected Zoom account
- **Read operations** (GET) retrieve data from the connected Zoom account
- **Write operations** (POST, PATCH, DELETE) create, modify, or delete meetings, webinars, and recordings — confirm with the user before destructive actions
- Access is limited to the Zoom account linked through the OAuth connection

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Zoom OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=zoom&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoom'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2026-04-10T00:35:13.470841Z",
    "last_updated_time": "2026-04-10T00:37:08.985792Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "zoom",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Zoom connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoom/v2/users/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Users

#### Get Current User

```bash
GET /zoom/v2/users/me
```

**Response:**
```json
{
  "id": "APv5EPHiSvitxgPAw0DbaQ",
  "first_name": "John",
  "last_name": "Doe",
  "display_name": "John Doe",
  "email": "john@example.com",
  "type": 1,
  "role_name": "Owner",
  "pmi": 5017823017,
  "timezone": "America/Los_Angeles",
  "status": "active",
  "created_at": "2023-06-01T19:33:22Z",
  "last_login_time": "2026-04-10T00:35:21Z"
}
```

**User Types:**
- `1` - Basic
- `2` - Licensed
- `3` - On-prem

### Meetings

#### List User's Meetings

```bash
GET /zoom/v2/users/me/meetings
GET /zoom/v2/users/{userId}/meetings
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | `scheduled`, `live`, `upcoming`, `upcoming_meetings`, `previous_meetings` |
| `page_size` | integer | Results per page (max 300, default 30) |
| `next_page_token` | string | Pagination token |
| `from` | string | Start date (YYYY-MM-DD) |
| `to` | string | End date (YYYY-MM-DD) |

**Response:**
```json
{
  "page_size": 30,
  "total_records": 1,
  "next_page_token": "",
  "meetings": [
    {
      "uuid": "RPrVctdSRxaVmIUTHVUlGQ==",
      "id": 82931897821,
      "host_id": "APv5EPHiSvitxgPAw0DbaQ",
      "topic": "Team Standup",
      "type": 2,
      "start_time": "2026-04-10T00:39:32Z",
      "duration": 30,
      "timezone": "America/Los_Angeles",
      "join_url": "https://us05web.zoom.us/j/82931897821?pwd=..."
    }
  ]
}
```

#### Get Upcoming Meetings

```bash
GET /zoom/v2/users/me/upcoming_meetings
```

Returns meetings scheduled for the future.

#### Create Meeting

```bash
POST /zoom/v2/users/me/meetings
POST /zoom/v2/users/{userId}/meetings
Content-Type: application/json

{
  "topic": "Weekly Team Sync",
  "type": 2,
  "start_time": "2026-04-15T14:00:00Z",
  "duration": 60,
  "timezone": "America/Los_Angeles",
  "agenda": "Discuss project updates",
  "settings": {
    "host_video": true,
    "participant_video": true,
    "join_before_host": false,
    "mute_upon_entry": true,
    "waiting_room": true
  }
}
```

**Meeting Types:**
- `1` - Instant meeting
- `2` - Scheduled meeting
- `3` - Recurring meeting with no fixed time
- `8` - Recurring meeting with fixed time

**Example - Create Meeting:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "topic": "Project Review",
    "type": 2,
    "start_time": "2026-04-15T14:00:00Z",
    "duration": 60,
    "timezone": "America/Los_Angeles",
    "settings": {
        "host_video": True,
        "participant_video": True,
        "waiting_room": True
    }
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoom/v2/users/me/meetings', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
resp = json.load(urllib.request.urlopen(req))
print(f"Meeting created! Join URL: {resp['join_url']}")
EOF
```

**Response:**
```json
{
  "uuid": "RPrVctdSRxaVmIUTHVUlGQ==",
  "id": 82931897821,
  "host_id": "APv5EPHiSvitxgPAw0DbaQ",
  "host_email": "john@example.com",
  "topic": "Project Review",
  "type": 2,
  "status": "waiting",
  "start_time": "2026-04-15T14:00:00Z",
  "duration": 60,
  "timezone": "America/Los_Angeles",
  "start_url": "https://us05web.zoom.us/s/82931897821?zak=...",
  "join_url": "https://us05web.zoom.us/j/82931897821?pwd=...",
  "password": "AX2hsd"
}
```

#### Get Meeting

```bash
GET /zoom/v2/meetings/{meetingId}
```

**Path Parameters:**
- `meetingId` - Meeting ID or UUID (double-encode UUID if it contains `/` or `//`)

#### Update Meeting

```bash
PATCH /zoom/v2/meetings/{meetingId}
Content-Type: application/json

{
  "topic": "Updated Meeting Title",
  "duration": 45,
  "settings": {
    "waiting_room": false
  }
}
```

**Example - Update Meeting:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "topic": "Updated Weekly Sync",
    "duration": 45
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoom/v2/meetings/82931897821', data=data, method='PATCH')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
urllib.request.urlopen(req)
print("Meeting updated!")
EOF
```

#### Delete Meeting

```bash
DELETE /zoom/v2/meetings/{meetingId}
```

**Query Parameters:**
- `schedule_for_reminder` - Send cancellation email to registrants (boolean)
- `cancel_meeting_reminder` - Send cancellation email notification (boolean)

### Recordings

#### List User's Cloud Recordings

```bash
GET /zoom/v2/users/me/recordings
GET /zoom/v2/users/{userId}/recordings
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `from` | string | Start date (YYYY-MM-DD) |
| `to` | string | End date (YYYY-MM-DD) |
| `page_size` | integer | Results per page (max 300, default 30) |
| `next_page_token` | string | Pagination token |
| `trash` | boolean | List trashed recordings |
| `trash_type` | string | `meeting_recordings` or `recording_file` |

**Response:**
```json
{
  "from": "2026-04-01",
  "to": "2026-04-10",
  "page_count": 1,
  "page_size": 30,
  "total_records": 2,
  "next_page_token": "",
  "meetings": [
    {
      "uuid": "...",
      "id": 123456789,
      "topic": "Team Meeting",
      "start_time": "2026-04-05T14:00:00Z",
      "duration": 45,
      "total_size": 52428800,
      "recording_count": 2,
      "recording_files": [
        {
          "id": "...",
          "meeting_id": "...",
          "recording_start": "2026-04-05T14:00:00Z",
          "recording_end": "2026-04-05T14:45:00Z",
          "file_type": "MP4",
          "file_size": 50000000,
          "play_url": "https://...",
          "download_url": "https://...",
          "status": "completed",
          "recording_type": "shared_screen_with_speaker_view"
        }
      ]
    }
  ]
}
```

#### Get Meeting Recordings

```bash
GET /zoom/v2/meetings/{meetingId}/recordings
```

#### Delete Meeting Recordings

```bash
DELETE /zoom/v2/meetings/{meetingId}/recordings
```

### Webinars

**Note:** Webinar endpoints require a Webinar add-on plan.

#### List User's Webinars

```bash
GET /zoom/v2/users/me/webinars
GET /zoom/v2/users/{userId}/webinars
```

#### Create Webinar

```bash
POST /zoom/v2/users/{userId}/webinars
Content-Type: application/json

{
  "topic": "Product Launch Webinar",
  "type": 5,
  "start_time": "2026-05-01T10:00:00Z",
  "duration": 90,
  "timezone": "America/Los_Angeles"
}
```

**Webinar Types:**
- `5` - Scheduled webinar
- `6` - Recurring webinar with no fixed time
- `9` - Recurring webinar with fixed time

#### Get Webinar

```bash
GET /zoom/v2/webinars/{webinarId}
```

#### Update Webinar

```bash
PATCH /zoom/v2/webinars/{webinarId}
Content-Type: application/json

{
  "topic": "Updated Webinar Title"
}
```

#### Delete Webinar

```bash
DELETE /zoom/v2/webinars/{webinarId}
```

### Meeting Registrants

#### List Meeting Registrants

```bash
GET /zoom/v2/meetings/{meetingId}/registrants
```

#### Add Meeting Registrant

```bash
POST /zoom/v2/meetings/{meetingId}/registrants
Content-Type: application/json

{
  "email": "attendee@example.com",
  "first_name": "Jane",
  "last_name": "Smith"
}
```

### Meeting Participants

#### List Past Meeting Participants

```bash
GET /zoom/v2/past_meetings/{meetingUUID}/participants
```

**Note:** Use double-encoded UUID if it contains `/` or `//`.

## Pagination

Zoom uses cursor-based pagination with `next_page_token`:

```bash
GET /zoom/v2/users/me/meetings?page_size=50
```

**Response includes pagination info:**
```json
{
  "page_size": 50,
  "total_records": 150,
  "next_page_token": "Tva2CuIdTgsv8wAnhyAdU3m06Y2HuLQtlh3",
  "meetings": [...]
}
```

**Get next page:**
```bash
GET /zoom/v2/users/me/meetings?page_size=50&next_page_token=Tva2CuIdTgsv8wAnhyAdU3m06Y2HuLQtlh3
```

When `next_page_token` is empty, there are no more pages.

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/zoom/v2/users/me/meetings',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.meetings);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/zoom/v2/users/me/meetings',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
meetings = response.json()['meetings']
```

### Create Meeting and Get Join URL

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# Create a meeting
meeting = requests.post(
    'https://gateway.maton.ai/zoom/v2/users/me/meetings',
    headers=headers,
    json={
        'topic': 'Quick Sync',
        'type': 2,
        'duration': 30,
        'settings': {
            'waiting_room': True,
            'join_before_host': False
        }
    }
).json()

print(f"Meeting ID: {meeting['id']}")
print(f"Join URL: {meeting['join_url']}")
print(f"Password: {meeting['password']}")
```

## Notes

- Meeting IDs are numeric; UUIDs are base64-encoded strings
- When using UUID in path, double-encode if it contains `/` or `//`
- User `me` can be used to reference the authenticated user
- Some endpoints require admin scopes and may not be available with standard OAuth
- Webinar endpoints require a Webinar add-on subscription
- Recordings are only available for cloud recording-enabled accounts
- Rate limits vary by plan and endpoint category
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq`, environment variables may not expand correctly in some shells

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request or missing required parameter |
| 401 | Invalid or missing Maton API key |
| 403 | Forbidden - insufficient permissions |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Zoom API |

### Common Error Codes

| Code | Message |
|------|---------|
| 3001 | Meeting does not exist |
| 4711 | Invalid access token, missing required scopes |
| 200 (in body) | Feature not available (e.g., Webinar plan missing) |

## Resources

- [Zoom API Documentation](https://developers.zoom.us/docs/api/)
- [Zoom REST API Reference](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/)
- [Zoom Meeting API](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Meetings)
- [Zoom OAuth Scopes](https://developers.zoom.us/docs/integrations/oauth-scopes/)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
