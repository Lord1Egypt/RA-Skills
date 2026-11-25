<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Meetings

## `attio api meetings-create [options]`

- What: Create a meeting
- Call: `POST /v2/meetings`, effect: write
- Sign-in: oauth2 (meeting:read-write, record\_permission:read)
- Body: `PostV2MeetingsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api meetings-delete [options]`

- What: Delete a meeting
- Call: `DELETE /v2/meetings/{meeting_id}`, effect: destructive
- Sign-in: oauth2 (meeting:read-write)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meeting\_id |

## `attio api meetings-get [options]`

- What: Get a meeting
- Call: `GET /v2/meetings/{meeting_id}`, effect: read
- Sign-in: oauth2 (meeting:read, record\_permission:read)

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meeting\_id |

## `attio api meetings-list [options]`

- What: List meetings
- Call: `GET /v2/meetings`, effect: read
- Sign-in: oauth2 (meeting:read, record\_permission:read)
- Pages: cursor: send `cursor` (query), read the next one from `pagination.next_cursor`; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | limit |
| `--cursor <value>` | no | cursor |
| `--linked-object <value>` | no | linked\_object |
| `--linked-record-id <value>` | no | linked\_record\_id |
| `--participants <value>` | no | participants |
| `--sort <value>` | no | sort |
| `--ends-from <value>` | no | ends\_from |
| `--starts-before <value>` | no | starts\_before |
| `--timezone <value>` | no | timezone |
| `--all` | no | read every page, as the API pages it |

## `attio api meetings-replace [options]`

- What: Update a meeting (overwrite linked records)
- Call: `PUT /v2/meetings/{meeting_id}`, effect: write
- Sign-in: oauth2 (meeting:read-write, record\_permission:read)
- Body: `PutV2MeetingsByMeetingIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meeting\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api meetings-update [options]`

- What: Update a meeting (append linked records)
- Call: `PATCH /v2/meetings/{meeting_id}`, effect: write
- Sign-in: oauth2 (meeting:read-write, record\_permission:read)
- Body: `PatchV2MeetingsByMeetingIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meeting\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
