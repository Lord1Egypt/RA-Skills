<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Transcripts

## `attio api meetings-call-recordings-transcript-list [options]`

- What: Deprecated: Get call transcript
- Call: `GET /v2/meetings/{meeting_id}/call_recordings/{call_recording_id}/transcript`, effect: read
- Sign-in: oauth2 (meeting:read, call\_recording:read)
- Pages: cursor: send `cursor` (query), read the next one from `pagination.next_cursor`

| Flag | Required | What |
|---|---|---|
| `--meeting-id <value>` | yes | meeting\_id |
| `--call-recording-id <value>` | yes | call\_recording\_id |
| `--cursor <value>` | no | cursor |
| `--all` | no | read every page, as the API pages it |
