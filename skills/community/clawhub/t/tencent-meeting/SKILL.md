---
name: tencent-meeting
description: Manage Tencent Meeting (腾讯会议) via REST API. Schedule/create meetings, query meeting details, list cloud recordings, and extract meeting transcripts. Use when user mentions "tencent meeting", "腾讯会议", "schedule a meeting", "meeting transcript", "会议转写", "meeting recording", or needs to interact with the Tencent Meeting platform.
---

# Tencent Meeting

Manage Tencent Meeting via the open REST API (AK/SK auth).

## Setup

Required env vars (set in shell or `.env`):

| Var | Description |
|-----|-------------|
| `TM_SECRET_ID` | API SecretId from Tencent Meeting open platform |
| `TM_SECRET_KEY` | API SecretKey |
| `TM_APP_ID` | Enterprise AppId |
| `TM_SDK_ID` | Application SdkId |
| `TM_STS_TOKEN` | (Optional) STS ticket for transcript/record APIs |

Get credentials at: https://meeting.tencent.com/open-api.html

## Commands

### Create a Meeting

```bash
node {baseDir}/scripts/create_meeting.js '<JSON>'
```

JSON fields:

| Field | Required | Description |
|-------|----------|-------------|
| `userid` | yes | Creator's user ID |
| `subject` | yes | Meeting subject |
| `start_time` | yes | ISO 8601 datetime or unix timestamp (seconds) |
| `end_time` | yes | ISO 8601 datetime or unix timestamp (seconds) |
| `type` | no | 0=scheduled (default), 1=instant |
| `password` | no | 4-6 digit meeting password |
| `instanceid` | no | Device type, default 1 (PC) |
| `invitees` | no | Array of `{userid}` objects |
| `settings` | no | Meeting settings (mute, waiting room, auto-record, etc.) |
| `time_zone` | no | Timezone string |
| `location` | no | Meeting location (max 18 Chinese chars) |

Example — schedule a meeting tomorrow at 2pm:
```bash
node {baseDir}/scripts/create_meeting.js '{"userid":"user123","subject":"Weekly Sync","start_time":"2026-03-11T14:00:00+08:00","end_time":"2026-03-11T15:00:00+08:00","settings":{"auto_asr":true}}'
```

### Query a Meeting

```bash
node {baseDir}/scripts/query_meetings.js --meeting-id <ID> --userid <UID>
node {baseDir}/scripts/query_meetings.js --meeting-code <CODE> --userid <UID>
```

### List Cloud Recordings

```bash
node {baseDir}/scripts/list_records.js --meeting-id <MID> --userid <UID>
```

### Get Record Detail (download URLs, AI summary)

```bash
node {baseDir}/scripts/list_records.js --meeting-record-id <MRID> --userid <UID>
```

### Extract Meeting Transcript

```bash
# Text format (readable)
node {baseDir}/scripts/get_transcript.js --record-file-id <RFID> --operator-id <UID> [--meeting-id <MID>] [--format text]

# JSON format (full detail with timestamps)
node {baseDir}/scripts/get_transcript.js --record-file-id <RFID> --operator-id <UID> --format json

# AI-optimized transcript
node {baseDir}/scripts/get_transcript.js --record-file-id <RFID> --operator-id <UID> --type 1
```

Output (text format):
```
[00:04] Speaker1: 看一下那个哪能看。
[00:12] Speaker1: 可以。
[00:43] Speaker2: 没有类型还有...
```

## Workflow: Get Transcript from a Meeting

1. Query the meeting to get `meeting_id`
2. List recordings: `list_records.js --meeting-id <MID> --userid <UID>`
3. From the response, get `record_file_id`
4. Extract transcript: `get_transcript.js --record-file-id <RFID> --operator-id <UID>`

## Natural Language Mapping

| User says | Action |
|-----------|--------|
| "Schedule a meeting at 3pm tomorrow" | `create_meeting.js` with computed start/end times |
| "Create a meeting with password" | `create_meeting.js` with password field |
| "Get the transcript for meeting X" | Workflow: query → list records → get transcript |
| "Show meeting details" | `query_meetings.js` |
| "Download meeting recording" | `list_records.js` → use download URLs |

## API Reference

For detailed API fields and parameters, see [references/api-guide.md](references/api-guide.md).
