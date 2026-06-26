# Tencent Meeting API Quick Reference

Base URL: `https://api.meeting.qq.com`

## Authentication (AK/SK)

All requests use HMAC-SHA256 signing. Required headers:
- `X-TC-Key` (SecretId), `X-TC-Timestamp`, `X-TC-Nonce`, `X-TC-Signature`
- `AppId`, `SdkId`, `X-TC-Registered: 1`
- `Content-Type: application/json`

Handled by `scripts/sign.js`.

## Endpoints

### Create Meeting
`POST /v1/meetings`

Required fields: userid, instanceid, subject, type (0=scheduled, 1=instant), start_time, end_time (unix seconds).

Optional: password, invitees, hosts, settings, meeting_type (0=normal, 1=recurring, 5=PMI), recurring_rule, enable_live, time_zone, location.

Settings sub-fields: mute_enable_type_join, allow_in_before_host, auto_in_waiting_room, auto_record_type (none/local/cloud), auto_asr (enable transcript).

### Query Meeting
`GET /v1/meetings/{meeting_id}?userid=X&instanceid=1`

### List Records
`GET /v1/meetings/{meeting_id}/records?userid=X`

Returns: meeting_record_id, record files with download URLs.

### Get Record Detail
`GET /v1/records/{meeting_record_id}?userid=X`

Returns: record_file_id, view/download URLs, meeting_summary, ai_meeting_transcripts, ai_minutes, ai_topic_minutes.

Requires STS-Token in header since 2026-02-10.

### Get Transcript Detail
`GET /v1/records/transcripts/details?record_file_id=X&operator_id=Y&operator_id_type=1`

Optional: meeting_id, pid, limit, transcripts_type (0=original, 1=AI-optimized).

Returns: paragraphs with speaker_info, sentences, words (with timestamps).

Requires STS-Token in header since 2026-02-10.

## Device Types (instanceid)
0=PSTN, 1=PC, 2=Mac, 3=Android, 4=iOS, 5=Web, 6=iPad, 8=Mini Program

## Rate Limits (Create Meeting)
- ≥50 premium accounts: 10 times/month/account
- <50 premium accounts: 2 times/month/account
