---
name: zoom-meeting
description: |
  How to create, retrieve, list, and delete Zoom meetings using the Zoom REST API.
  Use this skill whenever the user mentions Zoom meetings, wants to schedule a meeting,
  needs meeting details, or asks to manage Zoom calls—even if they don't explicitly
  say "use the zoom-meeting skill." Supports both natural language requests and
  structured JSON commands. Always respond with human-readable output (no JSON).
---

# Zoom Meeting Skill

This skill allows programmatic management of Zoom meetings. Supports creating, retrieving, listing, and deleting meetings via the Zoom REST API.

## When to Use

Use this skill when the user:
- Wants to create or schedule a Zoom meeting
- Requests meeting details (join URL, password, etc.)
- Wants to see all upcoming meetings
- Needs to cancel/delete a meeting
- Mentions "Zoom" along with meeting-related actions

## Authentication

The skill automatically handles authentication via Zoom Server-to-Server OAuth.

**Credentials location:** `~/.openclaw/credentials/zoom.json`

**Required credentials:**
```json
{
  "account_id": "YOUR_ACCOUNT_ID",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

The skill automatically obtains and refreshes access tokens.

## Supported Actions

### 1. create_meeting

Create a new Zoom meeting.

**Parameters:**
- `topic` (required): Meeting topic/title
- `start_time` (optional): Date/time in ISO 8601 format. Default: current time.
- `duration` (optional): Duration in minutes. Default: 40.
- `timezone` (optional): Timezone. Default: `Asia/Almaty`.

**JSON Example:**
```json
{
  "action": "create_meeting",
  "topic": "Daily Standup",
  "start_time": "2026-03-10T10:00:00",
  "duration": 30,
  "timezone": "Asia/Almaty"
}
```

### 2. get_meeting

Retrieve details of an existing meeting.

**Parameters:**
- `meeting_id` (required): Zoom meeting ID

**JSON Example:**
```json
{
  "action": "get_meeting",
  "meeting_id": "123456789"
}
```

### 3. list_meetings

Get a list of all user's meetings.

**Parameters:**
- `user_id` (optional): User ID. Default: `me`.

**JSON Example:**
```json
{
  "action": "list_meetings"
}
```

### 4. delete_meeting

Delete a Zoom meeting.

**Parameters:**
- `meeting_id` (required): Zoom meeting ID

**JSON Example:**
```json
{
  "action": "delete_meeting",
  "meeting_id": "123456789"
}
```

## Usage Examples

### Natural Language

**User:** "Create a Zoom meeting tomorrow at 10 AM called 'Architecture Review'"

**Actions:**
1. Parse natural language to extract parameters
2. Convert "tomorrow at 10 AM" to ISO 8601 format
3. Call `create_meeting` with extracted parameters
4. Return human-readable response

**User:** "What's the join URL for meeting 123456789?"

**Actions:**
1. Call `get_meeting` with the meeting ID
2. Return join_url from the response

**User:** "Show all my upcoming Zoom meetings"

**Actions:**
1. Call `list_meetings`
2. Format results into a readable list

**User:** "Delete meeting 987654321"

**Actions:**
1. Call `delete_meeting` with the meeting ID
2. Confirm deletion

### Structured JSON

Users can pass direct JSON commands:

```json
{
  "action": "create_meeting",
  "topic": "Sprint Planning",
  "start_time": "2026-03-11T14:00:00",
  "duration": 60
}
```

## Parameter Collection

If the user provided incomplete information for creating a meeting, ask clarifying questions:

**User:** "Create a Zoom meeting"

**You:** "Sure! What's the meeting topic?"

**User:** "Team Sync"

**You:** "When should the meeting start?"

**User:** "Tomorrow at 2 PM"

**You:** "What duration? (default: 40 minutes)"

Then create the meeting with collected parameters and defaults.

## Output Format

Always return **human-readable text only** (no JSON):

**Example for create_meeting:**

```
✅ Meeting created!

📋 Topic: Daily Standup
🆔 Meeting ID: 123456789
🔗 Join: https://zoom.us/j/123456789
🔑 Password: 983421
⏰ Start: 2026-03-10T10:00:00
⏱ Duration: 30 min
🌍 Timezone: Asia/Almaty
```

## Error Handling

Handle errors gracefully and return them in readable format:

**Authentication failure:**
```
Error: Failed to obtain access token. Check credentials in ~/.openclaw/credentials/zoom.json
```

**Invalid meeting ID:**
```
Error: Meeting 123456789 does not exist or you don't have permission to access it
```

**API error:**
```
Error: Zoom API returned error 429: Rate Limited
```

## Implementation

The skill uses `scripts/zoom_api.py` for all API interactions. The script handles:

- Loading credentials from file
- OAuth token generation and refresh
- HTTP requests to Zoom API endpoints
- Response parsing and error handling

**Key endpoints:**
- Create: `POST /users/me/meetings`
- Get: `GET /meetings/{meetingId}`
- List: `GET /users/me/meetings`
- Delete: `DELETE /meetings/{meetingId}`

## Defaults

| Parameter | Default |
|-----------|---------|
| start_time | Current time |
| duration | 40 minutes |
| timezone | Asia/Almaty |

## Meeting Creation Rules

- Meetings are always created for `/users/me` (authenticated user)
- No duplicate detection—each request creates a new meeting
- All meetings are scheduled meetings (type 2)

## Reference Files

- `references/zoom_api_reference.md` - Detailed API documentation, endpoints, and error codes

## Design Principles

This skill follows these principles:

- **Minimal verbosity** - Responses are brief and focused
- **Deterministic output** - Same input always produces same output structure
- **Agent-friendly** - Structured responses that AI agents can parse
- **Safe credential handling** - Never expose credentials in logs or output
- **Human-readable output** - Always return human-readable text, not JSON
- **Local time display** - Meeting times are shown in the specified timezone, not UTC

## Dependencies

- `requests` - For HTTP requests to Zoom API
- `pytz` - For timezone conversions (installed automatically)
