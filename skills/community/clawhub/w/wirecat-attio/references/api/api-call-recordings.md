<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Call recordings

## `attio api meetings-call-recordings-create [options]`

- What: Create call recording
- Call: `POST /v2/meetings/{meeting_id}/call_recordings`, effect: write
- Sign-in: oauth2 (meeting:read, call\_recording:read-write)
- Body: `PostV2MeetingsByMeetingIdCallRecordingsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meeting\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api meetings-call-recordings-delete [options]`

- What: Delete call recording
- Call: `DELETE /v2/meetings/{meeting_id}/call_recordings/{call_recording_id}`, effect: destructive
- Sign-in: oauth2 (meeting:read, call\_recording:read-write)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meeting\_id |
| `--call-recording-id <value>` | yes | call\_recording\_id |

## `attio api meetings-call-recordings-get [options]`

- What: Get call recording
- Call: `GET /v2/meetings/{meeting_id}/call_recordings/{call_recording_id}`, effect: read
- Sign-in: oauth2 (meeting:read, call\_recording:read)

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meeting\_id |
| `--call-recording-id <value>` | yes | call\_recording\_id |

## `attio api meetings-call-recordings-list [options]`

- What: List call recordings
- Call: `GET /v2/meetings/{meeting_id}/call_recordings`, effect: read
- Sign-in: oauth2 (meeting:read, call\_recording:read)
- Pages: cursor: send `cursor` (query), read the next one from `pagination.next_cursor`; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meeting\_id |
| `--limit <value>` | no | limit |
| `--cursor <value>` | no | cursor |
| `--all` | no | read every page, as the API pages it |
