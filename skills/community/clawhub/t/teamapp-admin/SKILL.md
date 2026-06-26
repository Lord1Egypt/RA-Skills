---
name: teamapp-admin-api
description: Use when interacting with TeamApp club admin JSON endpoints on teamapp.com to create/read/update News articles and Schedule events, and to resolve Team and Access Group IDs needed for visibility, roster, and targeting fields.
---

# TeamApp Admin API

Use this skill for TeamApp admin operations against JSON endpoints discovered from the web app.

## Quick Workflow

1. Resolve IDs first.
- Load [references/api-map.md](references/api-map.md) and fetch `club_id`, `team_id`, and `access_level_id` values from list endpoints.

2. Read form schemas before writing.
- Open `new.json` or `edit.json` endpoint for the target resource.
- Use the embedded `onSubmit` controller and URL as source of truth for method and endpoint.

3. Create or update content.
- Submit payload fields exactly as named in the schema.
- For visibility-scoped content, set `...access_level_ids_csv` only when visibility is `access_groups`.

4. Verify by reloading list endpoints.
- Re-read list JSON and confirm returned object IDs, titles, and action URLs.

## Auth and Session Requirements

**MANDATORY:** All interactions with the TeamApp API via this skill **must** use the provided wrapper script `bin/api-wrapper.sh`.

This wrapper automatically handles:
-   Session bootstrapping (fetching the dashboard to establish a session).
-   CSRF token extraction and caching.
-   Cookie management (`ta_auth_token` and `_teamapp_session`).
-   Session refreshing on expiration (401/422 errors).

### Required Environment Variables

The wrapper requires the following variables to be set in your shell environment:

-   `TA_AUTH_TOKEN`: The `ta_auth_token` cookie value (extracted from a browser session).

### Usage

Call the wrapper with the HTTP method, the full URL, and any `curl` options (like data payloads).

```bash
# General Syntax
./bin/api-wrapper.sh [METHOD] [URL] [CURL_OPTIONS...]
```

**Example: Read Articles**
```bash
./bin/api-wrapper.sh GET "https://examplesite.teamapp.com/clubs/$TA_CLUB_ID/articles.json?_detail=v1"
```

**Example: Create Article**
```bash
./bin/api-wrapper.sh POST "https://examplesite.teamapp.com/clubs/$TA_CLUB_ID/articles.json?_post_response=v1" \
  --data-urlencode "article[subject]=My Title" \
  --data-urlencode "article[body]=My Body" \
  --data-urlencode "article[visibility]=public" \
  --data-urlencode "article[comments_enabled]=1" \
  --data-urlencode "article[feature]=0" \
  --data-urlencode "article[html_body]=0" \
  --data-urlencode "article[release_pending]=0" \
  --data-urlencode "send_notifications=0"
```

## Scheduling and Notifications

All News and Events support scheduling and configurable notification delivery.

### Scheduling (Release Control)

- `...[release_pending]`: Set to `0` for immediate release, or `1` to schedule for later.
- `...[release_at]`: When `release_pending` is `1`, provide an ISO 8601 timestamp (e.g., `2026-03-25 10:00`).

### Notification Delivery

The `send_notifications` parameter controls how users are alerted:
- `0`: **None** (Silent release)
- `1`: **Push OR Email** (Default: sends push if enabled on device, falls back to email if notifications are disabled)
- `2`: **Push AND Email** (Sends both regardless of app notification status)

### Event Reminders

Events include an additional `event[reminder]` field for automated alerts:
- `-1`: None
- `0`: At starting time
- `1800`: 30 minutes before
- `3600`: 1 hour before
- `86400`: 1 day before (and other standard intervals in seconds)
- `-2`: Custom (requires `event[reminder_datetime]`)

## Operations

### News Articles (create/read/update)
- Endpoint map and payload fields: see [references/api-map.md](references/api-map.md).

Required baseline fields for create:
- `article[subject]`
- `article[body]`
- `article[visibility]` (`public|approved_members|access_groups`)
- `article[comments_enabled]` (`0|1`)
- `article[feature]` (`0|1`)
- `article[html_body]` (`0|1`)
- `article[release_pending]` (`0|1`)
- `send_notifications` (`0|1|2`)

### Schedule Events (create/read/update)
- Endpoint map and payload fields: see [references/api-map.md](references/api-map.md).

Key fields:
- `event[team_id]`, `event[title]`
- `event[datetime]`, `event[datetime_end]` or all-day fields
- `event[details]` / html variant fields
- `event[visibility]`, `event[access_level_ids_csv]`
- `event[release_pending]`, `event[release_at]`
- `send_notifications`, `event[reminder]`, `event[reminder_datetime]`

### Teams and Access Groups (ID resolution + targeting)

Use list endpoints to resolve IDs before posting news/events:
- Teams: see [references/api-map.md](references/api-map.md).
- Access groups: see [references/api-map.md](references/api-map.md).

Use team/access-group IDs in:
- `event[team_id]`
- `article[access_level_ids_csv]`
- `event[access_level_ids_csv]`
- `team[access_level_ids_csv]`
- `roster_access_level_id`

## References

- Endpoint and payload map: [references/api-map.md](references/api-map.md)
