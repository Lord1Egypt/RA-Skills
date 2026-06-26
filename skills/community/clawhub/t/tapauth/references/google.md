# Google Workspace via TapAuth

## Available Scopes

Use the Google scope name without the URL prefix. Full URLs also work.

| Scope | Access | Full URL |
|-------|--------|----------|
| `calendar.readonly` | Read calendar events | `https://www.googleapis.com/auth/calendar.readonly` |
| `calendar.events` | Create/edit/delete events in calendars where the calendar ID is already known; does not list calendars by name | `https://www.googleapis.com/auth/calendar.events` |
| `calendar.events.readonly` | Read calendar events (events-only) | `https://www.googleapis.com/auth/calendar.events.readonly` |
| `calendar.calendarlist.readonly` | List the user's calendars and calendar IDs | `https://www.googleapis.com/auth/calendar.calendarlist.readonly` |
| `calendar` | Full Google Calendar access; use when the workflow needs both discovery and writes and narrower scopes are insufficient | `https://www.googleapis.com/auth/calendar` |
| `spreadsheets.readonly` | Read Google Sheets | `https://www.googleapis.com/auth/spreadsheets.readonly` |
| `spreadsheets` | Full Sheets access | `https://www.googleapis.com/auth/spreadsheets` |
| `documents.readonly` | Read Google Docs | `https://www.googleapis.com/auth/documents.readonly` |
| `documents` | Full Docs access | `https://www.googleapis.com/auth/documents` |
| `userinfo.email` | Read user email | `https://www.googleapis.com/auth/userinfo.email` |
| `userinfo.profile` | Read user profile | `https://www.googleapis.com/auth/userinfo.profile` |

## Example: Read a Google Sheet

```bash
# 1. Get a token
scripts/tapauth.sh google spreadsheets.readonly

# 2. Read a sheet
curl -H "Authorization: Bearer <token>" \
  "https://sheets.googleapis.com/v4/spreadsheets/SPREADSHEET_ID/values/Sheet1"
```

## Example: List Calendar Events

```bash
curl -H "Authorization: Bearer <token>" \
  "https://www.googleapis.com/calendar/v3/calendars/primary/events?maxResults=10&timeMin=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Example: Create Calendar Event

```bash
# 1. Get approval for event write scope when the calendar ID is already known
scripts/tapauth.sh google calendar.events

# 2. Create an event (replace YYYY-MM-DD with a future date)
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Team standup",
    "start": {"dateTime": "YYYY-MM-DDT09:00:00Z"},
    "end":   {"dateTime": "YYYY-MM-DDT09:30:00Z"}
  }' \
  "https://www.googleapis.com/calendar/v3/calendars/primary/events"
```

## Example: Create Calendar Event by Calendar Name

To add events to a calendar by name, request calendar discovery and event write scopes together. `calendar.events` alone can insert events, but it cannot call `calendarList.list` to find a calendar ID by name.

```bash
# 1. Get approval for both discovery and event writes
scripts/tapauth.sh google calendar.events,calendar.calendarlist.readonly

# 2. Start the real operation immediately; --token polls until the user approves
CALENDAR_ID="$(curl -s -H "Authorization: Bearer $(scripts/tapauth.sh --token google calendar.events,calendar.calendarlist.readonly)" \
  "https://www.googleapis.com/calendar/v3/users/me/calendarList" \
  | jq -r '.items[] | select(.summary == "Charlie & Sam") | .id' | head -n 1)"
test -n "$CALENDAR_ID" || { echo "Calendar not found: Charlie & Sam" >&2; exit 1; }

curl -X POST \
  -H "Authorization: Bearer $(scripts/tapauth.sh --token google calendar.events,calendar.calendarlist.readonly)" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Team standup",
    "start": {"dateTime": "YYYY-MM-DDT09:00:00Z"},
    "end":   {"dateTime": "YYYY-MM-DDT09:30:00Z"}
  }' \
  "https://www.googleapis.com/calendar/v3/calendars/${CALENDAR_ID}/events"
```

If the narrower pair is not available or does not cover the workflow, request full Calendar access with `scripts/tapauth.sh google calendar`.

## Example: Multiple Scopes

```bash
# Comma-separated (required format)
scripts/tapauth.sh google calendar.events,calendar.calendarlist.readonly
```

## Gotchas

- **Scope names:** Use Google's actual scope names without the URL prefix (e.g. `calendar.readonly`, not `calendar_read`). Full URLs also work.
- **Token refresh:** Google access tokens expire after ~1 hour. TapAuth handles refresh automatically — just call the token endpoint again to get a fresh token.
- **Unverified app warning:** Users may see a "This app isn't verified" screen. They can click "Advanced" → "Go to TapAuth" to proceed.
- **Readonly preference:** Always prefer read-only scope variants unless you need write access. Higher approval rate.
- **Workflow-based scopes:** Request every scope needed for the whole workflow up front. Discovery-plus-write tasks often need one read/list scope and one mutation scope.
- **Multiple scopes:** Pass as comma-separated: `calendar.events,calendar.calendarlist.readonly`

## Recommended Minimum Scopes

| Use Case | Scopes |
|----------|--------|
| Read calendar | `calendar.readonly` |
| Create/edit events when calendar ID is known | `calendar.events` |
| Add event to calendar by name | `calendar.events,calendar.calendarlist.readonly` |
| Full Calendar access | `calendar` |
| Read spreadsheet | `spreadsheets.readonly` |
| Read document | `documents.readonly` |
| Full workspace | `calendar`, `spreadsheets`, `documents` |
