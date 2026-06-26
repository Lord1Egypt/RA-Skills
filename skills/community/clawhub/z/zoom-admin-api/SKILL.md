---
name: zoom-admin
description: |
  Zoom Admin API integration with managed OAuth. Manage users, meetings, webinars, recordings, and account settings with admin-level access.
  Use this skill when users want to list users, create or manage meetings, view recordings, check user/account settings, or administer a Zoom workspace.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Security: The MATON_API_KEY authenticates with Maton.ai but grants NO access to Zoom by itself. Zoom access requires explicit OAuth authorization by the user through Maton's connect flow. Access is strictly scoped to the Zoom account the user has authorized. All API requests are proxied through Maton's gateway, which handles OAuth token management. Only connect the intended Zoom account and revoke the connection when no longer needed.
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Zoom Admin

Access the Zoom API with managed OAuth authentication and admin-level scopes. Manage users, meetings, webinars, recordings, and account settings.

## Quick Start

```bash
# List users in your Zoom account
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/zoom-admin/v2/users?status=active&page_size=30')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/zoom-admin/{native-api-path}
```

Replace `{native-api-path}` with the actual Zoom API endpoint path (e.g., `v2/users`, `v2/meetings/123`). The gateway proxies requests to `api.zoom.us` and automatically injects your OAuth token.

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

Manage your Zoom Admin OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=zoom-admin&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoom-admin'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
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
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "zoom-admin",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Zoom Admin connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/zoom-admin/v2/users?status=active')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- **No implicit access:** The MATON_API_KEY alone cannot access Zoom. The user must explicitly authorize a Zoom account via OAuth through Maton's connect flow.
- **Scoped access:** Access is limited to the specific Zoom account the user authorized. Admin scopes grant read/write access to users, meetings, webinars, and recordings within that account only.
- **Write safeguards:** All write operations (POST, PATCH, PUT, DELETE) require explicit user approval. Before executing any create, update, or delete call, confirm the exact target resource, account, and intended effect with the user.
- **Least privilege:** Connect only the intended Zoom account. Revoke or delete the connection when it is no longer needed.
- **Data handling:** API requests and responses flow through Maton's gateway, which handles OAuth token injection. No credentials are stored in this skill or exposed to the agent.

## API Reference

### User Operations

#### List Users

```bash
GET /zoom-admin/v2/users?status=active&page_size=30
```

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `status` | string | `active` | `active`, `inactive`, or `pending` |
| `page_size` | integer | 30 | Max: 2000 |
| `next_page_token` | string | | Pagination token (15-min expiry) |
| `role_id` | string | | Filter by role ID |

**Response:**
```json
{
  "page_size": 30,
  "total_records": 1,
  "next_page_token": "",
  "users": [
    {
      "id": "a-IOECePRV265Gy_wotUdQ",
      "first_name": "Richard",
      "last_name": "Song",
      "display_name": "Richard Song",
      "email": "user@example.com",
      "type": 1,
      "pmi": 6862513852,
      "timezone": "America/Los_Angeles",
      "verified": 1,
      "status": "active",
      "created_at": "2025-03-21T21:52:50Z",
      "last_login_time": "2026-05-01T01:01:08Z",
      "role_id": "0"
    }
  ]
}
```

User type values: `1` = Basic, `2` = Licensed, `4` = Unassigned, `99` = None.

#### Get User

```bash
GET /zoom-admin/v2/users/{userId}
```

Use `me` for the authenticated user, or a user ID / email address.

**Response:**
```json
{
  "id": "a-IOECePRV265Gy_wotUdQ",
  "first_name": "Richard",
  "last_name": "Song",
  "display_name": "Richard Song",
  "email": "user@example.com",
  "type": 1,
  "role_name": "Owner",
  "pmi": 6862513852,
  "use_pmi": false,
  "personal_meeting_url": "https://us05web.zoom.us/j/6862513852?pwd=...",
  "timezone": "America/Los_Angeles",
  "status": "active",
  "account_id": "ciah2jjMRgedBSqxO8bOjA",
  "role_id": "0",
  "login_types": [100, 1],
  "created_at": "2025-03-21T21:52:50Z",
  "last_login_time": "2026-05-01T01:01:08Z"
}
```

#### Get User Settings

```bash
GET /zoom-admin/v2/users/{userId}/settings
```

**Query Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `option` | string | `meeting_authentication`, `recording_authentication`, or `meeting_security` |

Returns detailed settings grouped into sections: `schedule_meeting`, `in_meeting`, `email_notification`, `recording`, `telephony`, `feature`, `whiteboard`, `audio_conferencing`, etc.

### Meeting Operations

#### List Meetings

```bash
GET /zoom-admin/v2/users/{userId}/meetings?type=scheduled&page_size=30
```

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `type` | string | `live` | `scheduled`, `live`, `upcoming`, `upcoming_meetings`, `previous_meetings` |
| `page_size` | integer | 30 | Max: 300 |
| `next_page_token` | string | | Pagination token (15-min expiry) |

**Response:**
```json
{
  "page_size": 30,
  "total_records": 11,
  "next_page_token": "B4Tr0tLbJKQMnChspbYH7UUvt7g0UeDQNh2",
  "meetings": [
    {
      "uuid": "SukzvlkXQO2rNcNPKUGCpw==",
      "id": 89560318205,
      "host_id": "a-IOECePRV265Gy_wotUdQ",
      "topic": "Team Standup",
      "type": 2,
      "start_time": "2026-03-30T18:00:00Z",
      "duration": 30,
      "timezone": "America/Los_Angeles",
      "created_at": "2026-03-29T18:01:40Z",
      "join_url": "https://us05web.zoom.us/j/89560318205?pwd=..."
    }
  ]
}
```

Meeting type values: `1` = Instant, `2` = Scheduled, `3` = Recurring (no fixed time), `4` = PMI, `8` = Recurring (fixed time).

#### Get Meeting

```bash
GET /zoom-admin/v2/meetings/{meetingId}
```

**Query Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `occurrence_id` | string | For recurring meetings |
| `show_previous_occurrences` | boolean | Show previous occurrences |

Returns full meeting details including `settings`, `recurrence`, `occurrences`, `join_url`, `start_url`, `password`, etc.

#### Create Meeting

```bash
POST /zoom-admin/v2/users/{userId}/meetings
Content-Type: application/json

{
  "topic": "Weekly Team Sync",
  "type": 2,
  "start_time": "2026-05-02T10:00:00Z",
  "duration": 30,
  "timezone": "America/Los_Angeles",
  "agenda": "Discuss project updates",
  "settings": {
    "host_video": true,
    "participant_video": true,
    "join_before_host": false,
    "mute_upon_entry": true,
    "waiting_room": false,
    "auto_recording": "none",
    "audio": "voip"
  }
}
```

**Key Request Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `topic` | string | Meeting topic |
| `type` | integer | `1` = Instant, `2` = Scheduled, `3` = Recurring (no fixed), `8` = Recurring (fixed) |
| `start_time` | string | ISO 8601 datetime (required for type 2 and 8) |
| `duration` | integer | Duration in minutes |
| `timezone` | string | e.g., `America/New_York` |
| `password` | string | Up to 10 characters |
| `agenda` | string | Max 2000 characters |
| `recurrence` | object | Required for type 8 |
| `settings` | object | Meeting settings |

Returns the created meeting object (same as Get Meeting).

#### Update Meeting

```bash
PATCH /zoom-admin/v2/meetings/{meetingId}
Content-Type: application/json

{
  "topic": "Updated Meeting Topic",
  "duration": 45
}
```

All fields are optional. Returns `204 No Content` on success.

#### Delete Meeting

```bash
DELETE /zoom-admin/v2/meetings/{meetingId}
```

**Query Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `occurrence_id` | string | Delete specific occurrence of recurring meeting |
| `schedule_for_reminder` | boolean | Notify host about cancellation |
| `cancel_meeting_reminder` | string | Notify registrants (`true`/`false`) |

Returns `204 No Content` on success.

#### Get Past Meeting Details

```bash
GET /zoom-admin/v2/past_meetings/{meetingId}
```

Use the meeting ID or UUID. If the UUID starts with `/` or contains `//`, it must be double-URL-encoded.

**Response:**
```json
{
  "uuid": "/LAYgqiEQ8CW4NlhkyOvVA==",
  "id": 89560318205,
  "host_id": "a-IOECePRV265Gy_wotUdQ",
  "type": 2,
  "topic": "Team Standup",
  "user_name": "Richard Song",
  "user_email": "user@example.com",
  "start_time": "2026-03-30T18:02:25Z",
  "end_time": "2026-03-30T18:09:50Z",
  "duration": 8,
  "total_minutes": 22,
  "participants_count": 3,
  "source": "Calendly for Zoom"
}
```

#### List Past Meeting Instances

```bash
GET /zoom-admin/v2/past_meetings/{meetingId}/instances
```

**Response:**
```json
{
  "meetings": [
    {
      "uuid": "/LAYgqiEQ8CW4NlhkyOvVA==",
      "start_time": "2026-03-30T18:02:25Z"
    }
  ]
}
```

### Webinar Operations

Webinar endpoints require a Webinar plan on the Zoom account.

#### List Webinars

```bash
GET /zoom-admin/v2/users/{userId}/webinars?page_size=30
```

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `type` | string | `scheduled` | `scheduled` or `upcoming` |
| `page_size` | integer | 30 | Max: 300 |
| `next_page_token` | string | | Pagination token |

**Response:**
```json
{
  "page_size": 30,
  "total_records": 0,
  "next_page_token": "",
  "webinars": [
    {
      "uuid": "...",
      "id": 12345678901,
      "host_id": "...",
      "topic": "Product Launch Webinar",
      "type": 5,
      "start_time": "2026-05-15T14:00:00Z",
      "duration": 60,
      "timezone": "America/Los_Angeles",
      "join_url": "https://us05web.zoom.us/j/..."
    }
  ]
}
```

Webinar type values: `5` = Webinar, `6` = Recurring (no fixed time), `9` = Recurring (fixed time).

#### Get Webinar

```bash
GET /zoom-admin/v2/webinars/{webinarId}
```

Returns full webinar details including settings, recurrence, and registration info.

### Recording Operations

#### List User Recordings

```bash
GET /zoom-admin/v2/users/{userId}/recordings?from=2026-04-01&to=2026-04-30&page_size=30
```

**Query Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `from` | string | Start date (`yyyy-mm-dd`). Max range: 1 month. Max past: 6 months |
| `to` | string | End date (`yyyy-mm-dd`) |
| `page_size` | integer | Max: 300 |
| `next_page_token` | string | Pagination token |
| `trash` | boolean | List trashed recordings |

**Response:**
```json
{
  "from": "2026-04-01",
  "to": "2026-04-30",
  "total_records": 0,
  "next_page_token": "",
  "meetings": [
    {
      "uuid": "...",
      "id": 12345678901,
      "host_id": "...",
      "topic": "Meeting Topic",
      "start_time": "2026-04-15T10:00:00Z",
      "duration": 45,
      "total_size": 52428800,
      "recording_count": 2,
      "recording_files": [
        {
          "id": "...",
          "file_type": "MP4",
          "file_extension": "MP4",
          "file_size": 41943040,
          "play_url": "https://...",
          "download_url": "https://...",
          "recording_type": "shared_screen_with_speaker_view",
          "status": "completed"
        }
      ]
    }
  ]
}
```

#### Get Meeting Recordings

```bash
GET /zoom-admin/v2/meetings/{meetingId}/recordings
```

Use the meeting ID or UUID. If the UUID starts with `/` or contains `//`, it must be double-URL-encoded.

**Query Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `include_fields` | string | `download_access_token` for JWT download token |
| `ttl` | integer | Token TTL in seconds (0–604800, default: 172800) |

Returns the meeting's recording files with download URLs.

### Account Operations

#### Get Account Settings

```bash
GET /zoom-admin/v2/accounts/{accountId}/settings
```

Use `me` for the connected account. Requires a paid Zoom plan.

**Query Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `option` | string | `meeting_authentication`, `recording_authentication`, `security`, `meeting_security` |

Returns account-level settings grouped into sections: `security`, `schedule_meeting`, `in_meeting`, `recording`, `telephony`, `feature`, `chat`, etc.

## Pagination

Zoom uses token-based pagination via `next_page_token`. Tokens expire after 15 minutes.

```bash
# First page
GET /zoom-admin/v2/users?page_size=30

# Next page
GET /zoom-admin/v2/users?page_size=30&next_page_token={next_page_token}
```

Response includes pagination fields:

```json
{
  "page_size": 30,
  "total_records": 100,
  "next_page_token": "B4Tr0tLbJKQMnChspbYH7UUvt7g0UeDQNh2"
}
```

When `next_page_token` is empty, there are no more pages. Do not reuse expired tokens — start from the first page if a token expires.

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/zoom-admin/v2/users?status=active&page_size=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/zoom-admin/v2/users',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'status': 'active', 'page_size': 10}
)
data = response.json()
```

## Notes

- The `zoom-admin` app uses admin-level OAuth scopes that grant access to all users in the Zoom account
- Meeting IDs are integers; UUIDs are base64-encoded strings. Both can be used in most endpoints
- UUIDs starting with `/` or containing `//` must be double-URL-encoded when used in path parameters
- Webinar endpoints require a Webinar add-on plan on the Zoom account
- Account Settings endpoint (`/v2/accounts/me/settings`) requires a paid Zoom plan
- Zoom enforces a limit of 100 meeting create/update operations per day per user
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Zoom Admin connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 404 | Resource not found (meeting, user, recording) |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Zoom API |

### Zoom Rate Limits

| Category | Pro Plan | Business+ |
|----------|----------|-----------|
| LIGHT | 4/sec, 6,000/day | 30/sec |
| MEDIUM | 2/sec, 2,000/day | 20/sec |
| HEAVY | 1/sec, 1,000/day | 10/sec |

Rate-limited responses include a `Retry-After` header.

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `zoom-admin`. For example:

- Correct: `https://api.maton.ai/zoom-admin/v2/users`
- Incorrect: `https://api.maton.ai/v2/users`

## Resources

- [Zoom API Overview](https://developers.zoom.us/docs/api/)
- [Zoom Meeting API Reference](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/)
- [Zoom User API Reference](https://developers.zoom.us/docs/api/rest/reference/user/methods/)
- [Zoom Account API Reference](https://developers.zoom.us/docs/api/rest/reference/account/methods/)
- [Zoom Rate Limits](https://developers.zoom.us/docs/api/rest/rate-limits/)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
