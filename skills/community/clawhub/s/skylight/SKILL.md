---
name: skylight
description: Interact with Skylight Calendar frame - manage calendar events, chores, lists, task box items, and rewards. Use when the user wants to view/create calendar events, manage family chores, work with shopping or to-do lists, check reward points, or interact with their Skylight smart display.
metadata:
  clawdbot:
    emoji: 📅
    requires:
      bins:
        - curl
        - openssl
        - python3
      env:
        - SKYLIGHT_FRAME_ID
    primaryEnv: SKYLIGHT_EMAIL
---

# Skylight Calendar

Control Skylight Calendar frame via the unofficial API.

## Setup

Set environment variables:
- `SKYLIGHT_URL`: Base URL (default: `https://app.ourskylight.com`)
- `SKYLIGHT_FRAME_ID`: Your frame (household) ID — find this by logging into [ourskylight.com](https://ourskylight.com/), clicking your calendar, and copying the number from the URL (e.g., `4197102` from `https://ourskylight.com/calendar/4197102`)

**Authentication:**

Use either plain env vars or 1Password references:

- Plain env: `SKYLIGHT_EMAIL`, `SKYLIGHT_PASSWORD`
- 1Password refs: `SKYLIGHT_EMAIL_OP_REF`, `SKYLIGHT_PASSWORD_OP_REF` (`op://vault/item/field`)
- `SKYLIGHT_TOKEN`: Full Authorization header value, usually `Bearer <access_token>`

## Authentication

Use the bundled OAuth helper to get an access token. With 1Password, store only references in env/config. If using a 1Password service-account/access token, make `OP_SERVICE_ACCOUNT_TOKEN` available to the Gateway process:

```bash
export OP_SERVICE_ACCOUNT_TOKEN='ops_...'
export SKYLIGHT_EMAIL_OP_REF='op://AIVault/Skylight/username'
export SKYLIGHT_PASSWORD_OP_REF='op://AIVault/Skylight/password'
export SKYLIGHT_TOKEN="$(./scripts/get-access-token.sh)"
```

Plain env vars still work:

```bash
export SKYLIGHT_EMAIL='you@example.com'
export SKYLIGHT_PASSWORD='...'
export SKYLIGHT_TOKEN="$(./scripts/get-access-token.sh)"
```

The script follows Skylight's current web/mobile OAuth flow:

1. Resolves `SKYLIGHT_EMAIL` and `SKYLIGHT_PASSWORD`; if either value is an `op://...` reference, or the matching `*_OP_REF` env var is set, it reads the secret with `op read`
2. Starts `/oauth/authorize` with client `skylight-mobile` and scope `everything`
3. Fetches `/auth/session/new` and extracts the Rails `authenticity_token`
4. Posts the resolved email/password to `/auth/session`
5. Follows the first redirect, extracts the OAuth `code` from the second redirect
6. Exchanges the code at `/oauth/token`
7. Prints `Bearer <access_token>` for direct use as `SKYLIGHT_TOKEN`

Optional overrides:

- `SKYLIGHT_URL`: Base URL, default `https://app.ourskylight.com`
- `SKYLIGHT_COOKIE_JAR`: Path to keep cookies for debugging; by default the script uses and deletes a temp jar
- `SKYLIGHT_DEVICE_FINGERPRINT`: OAuth device fingerprint; default matches the observed web flow

Do not print or persist Skylight or 1Password tokens unless needed. When using `OP_SERVICE_ACCOUNT_TOKEN`, never inline it in shell commands such as `OP_SERVICE_ACCOUNT_TOKEN='...' op read ...`; rely on the process environment so tmux/pane logs do not echo the token. Tokens may expire or rotate; rerun the helper when API calls return `401`.

## API Format

Responses use JSON:API format with `data`, `included`, and `relationships` fields.

## Calendar Events

### List events
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/calendar_events?date_min=2025-01-27&date_max=2025-01-31" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Accept: application/json"
```

Query params:
- `date_min` (required): Start date YYYY-MM-DD
- `date_max` (required): End date YYYY-MM-DD
- `timezone`: Timezone string (optional)
- `include`: CSV of related resources (`categories,calendar_account,event_notification_setting`)

### List source calendars
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/source_calendars" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

## Chores

### List chores
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/chores?after=2025-01-27&before=2025-01-31" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

Query params:
- `after`: Start date YYYY-MM-DD
- `before`: End date YYYY-MM-DD
- `include_late`: Include overdue chores (bool)
- `filter`: Filter by `linked_to_profile`

### Create chore
```bash
curl -s -X POST "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/chores" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "chore",
      "attributes": {
        "summary": "Take out trash",
        "status": "pending",
        "start": "2025-01-28",
        "start_time": "08:00",
        "recurring": false
      },
      "relationships": {
        "category": {
          "data": {"type": "category", "id": "CATEGORY_ID"}
        }
      }
    }
  }'
```

Chore attributes:
- `summary`: Chore title
- `status`: `pending` or `completed`
- `start`: Date YYYY-MM-DD
- `start_time`: Time HH:MM (optional)
- `recurring`: Boolean
- `recurrence_set`: RRULE string for recurring chores
- `reward_points`: Integer (optional)
- `emoji_icon`: Emoji (optional)

## Lists (Shopping/To-Do)

### List all lists
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/lists" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

### Get list with items
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/lists/{listId}" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

Response includes `data.attributes.kind` (`shopping` or `to_do`) and `included` array with list items.

List item attributes:
- `label`: Item text
- `status`: `pending` or `completed`
- `section`: Section name (optional)
- `position`: Sort order

## Task Box

### Create task box item
```bash
curl -s -X POST "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/task_box/items" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "task_box_item",
      "attributes": {
        "summary": "Pack lunches"
      }
    }
  }'
```

Task box attributes:
- `summary`: Task title
- `emoji_icon`: Emoji (optional)
- `routine`: Boolean (optional)
- `reward_points`: Integer (optional)

## Categories

### List categories
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/categories" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

Categories are used to assign chores to family members. Attributes include:
- `label`: Category name (e.g., "Mom", "Dad", "Kids")
- `color`: Hex color `#RRGGBB`
- `profile_pic_url`: Avatar URL

## Rewards

### List rewards
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/rewards" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

Optional query: `redeemed_at_min` (datetime) to filter by redemption date.

### List reward points
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/reward_points" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

## Frame Info

### Get frame details
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

### List devices
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/devices" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

## Notes

- API is **unofficial** and reverse-engineered; endpoints may change
- Tokens expire on logout; recapture as needed
- Responses return 304 Not Modified when data unchanged
- Use `jq` to parse JSON:API responses
- Frame ID is your household identifier; all resources are scoped to it
