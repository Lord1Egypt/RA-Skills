# Read AI API Reference

## Base URL
```
https://api.read.ai/v1
```

## Authentication

All requests use Bearer token auth:
```
Authorization: Bearer <API_KEY>
```

Get your API key: Read AI Dashboard > Settings > Integrations > API Keys

## Endpoints

### List Meetings
```
GET /meetings
```

| Param | Type | Description |
|-------|------|-------------|
| since | ISO 8601 | Start date filter |
| until | ISO 8601 | End date filter |
| limit | int | Max results (default 50, max 100) |
| offset | int | Pagination offset |
| order | string | `asc` or `desc` |

### Get Meeting
```
GET /meetings/{meeting_id}
```

| Param | Type | Description |
|-------|------|-------------|
| include | string | Comma-separated: `transcript`, `action_items`, `topics` |

### Get Transcript
```
GET /meetings/{meeting_id}/transcript
```

Returns speaker-attributed transcript entries:
```json
{
  "transcript": [
    {
      "speaker": "Brandon Stewart",
      "speakerName": "Brandon Stewart",
      "text": "Let's review the Q1 numbers.",
      "timestamp": "00:01:23",
      "startTime": "2026-02-01T14:01:23Z",
      "endTime": "2026-02-01T14:01:28Z"
    }
  ]
}
```

### Get Action Items
```
GET /meetings/{meeting_id}/action-items
```

Returns:
```json
{
  "action_items": [
    {
      "text": "Send updated budget proposal",
      "assignee": "Brandon Stewart",
      "dueDate": "2026-02-15",
      "status": "open"
    }
  ]
}
```

### Get Summary
```
GET /meetings/{meeting_id}/summary
```

Returns AI-generated meeting recap, key topics, and decisions.

## Webhook Payloads

Read AI sends POST requests to your webhook URL when meetings end.

### Meeting Completed Event
```json
{
  "event": "meeting.completed",
  "id": "mtg_abc123",
  "title": "Weekly Team Standup",
  "startTime": "2026-02-01T14:00:00Z",
  "endTime": "2026-02-01T14:30:00Z",
  "duration": "30m",
  "participants": [
    {"name": "Brandon Stewart", "email": "brandon@example.com"}
  ],
  "summary": "Team discussed Q1 priorities...",
  "topics": [
    {"title": "Q1 Planning", "duration": "15m"},
    {"title": "Budget Review", "duration": "10m"}
  ],
  "action_items": [
    {"text": "Draft proposal", "assignee": "Brandon", "dueDate": "2026-02-10"}
  ],
  "decisions": [
    "Approved new vendor contract"
  ],
  "transcript": [
    {"speaker": "Brandon", "text": "Let's get started.", "timestamp": "00:00:05"}
  ]
}
```

## Webhook Setup

1. Go to Read AI Dashboard > Settings > Integrations > Webhooks
2. Add your endpoint URL
3. Select events to receive (meeting.completed, etc.)
4. Save and test with a meeting

## Rate Limits

- 100 requests per minute per API key
- Webhook retries: 3 attempts with exponential backoff

## Error Codes

| Code | Meaning |
|------|---------|
| 401 | Invalid/expired API key |
| 403 | Insufficient permissions |
| 404 | Meeting not found |
| 429 | Rate limited |
| 500 | Server error |
