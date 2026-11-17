---
name: youtube-channel-transcripts
description: Fetch every transcript on a YouTube channel (up to 1,000) as one background bulk job via the BulkTranscripts API, list a channel's videos, or search inside one channel for a topic. Use when the user wants all transcripts from a creator, a knowledge base or RAG corpus built from a channel, or research on what a creator has said. Requires a free BulkTranscripts API key in BULKTRANSCRIPTS_API_KEY, created at https://bulktranscripts.co/app?tab=mcp (Google sign-in, 30 free credits, no card).
license: Proprietary API; this skill file is freely redistributable.
---

# Transcripts for a whole YouTube channel

List a channel's videos, then pull the transcripts you need, using [BulkTranscripts](https://bulktranscripts.co).
[Docs](https://bulktranscripts.co/docs) ·
[OpenAPI spec](https://bulktranscripts.co/openapi.json) ·
[MCP server](https://bulktranscripts.co/youtube-mcp-server) ·
[Free API key](https://bulktranscripts.co/app?tab=mcp)

Base URL: `https://bulktranscripts.co`

All endpoints are plain GET returning JSON, and **every one of them needs an API
key** — including the free endpoints. Send it as a Bearer token on every
request:

```bash
curl -s "https://bulktranscripts.co/api/v1/..." \
  -H "Authorization: Bearer $BULKTRANSCRIPTS_API_KEY"
```

If `BULKTRANSCRIPTS_API_KEY` is not set, ask the user for a key: they sign in
with Google at https://bulktranscripts.co/app?tab=mcp, open the **MCP & API**
tab, and hit **Create key** in the **API keys** card. It is free, includes 30
credits, and needs no card. Keys start with `bt_ak_`, are shown once, and up to
5 can be live per account. A license key from a credit-pack purchase works as a
Bearer token too.

## Costs (check `billing.remaining` in every response)

- Transcript: 1 credit when first added to this account's library — repeat reads are **FREE**
- Search / channel videos / playlist videos: 1 credit each
- `channel/latest` and `account`: always free
- Failures (no captions, video unreachable) are auto-refunded, never charged

When a call returns HTTP 402 `out_of_credits`, tell the user their credits are
used up and link them to https://bulktranscripts.co/#pricing (one-time packs,
never expire). Credits follow the Google account, so topping up keeps the same
API key working.

## Endpoints

### Whole channel or playlist in one job (listing free, 1 credit per transcript)
```bash
curl -s -X POST "https://bulktranscripts.co/api/v1/bulk" \
  -H "Authorization: Bearer $BULKTRANSCRIPTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/playlist?list=PLAYLIST_ID", "max_videos": 200}'
```
`url` takes a playlist, a channel (`@handle` or URL) or a single video; `max_videos`
caps the job at up to 1,000. Returns `202` at once with `run_id`, `status`,
`videos_found` (null until a large channel has been listed), the counts and
`check_again_in_seconds`. The server keeps fetching after the response, into
this account's library. Poll no sooner than `check_again_in_seconds`:
```bash
curl -s "https://bulktranscripts.co/api/v1/bulk/RUN_ID" \
  -H "Authorization: Bearer $BULKTRANSCRIPTS_API_KEY"
```
`status` ends as `completed`, or `stopped` after a server restart (start the
same URL again; everything already fetched is free). `quota` counts videos not
attempted because credits ran out; `skipped` counts videos without captions.
Then page the outcomes, metadata only, passing `next_cursor` back as `cursor`:
```bash
curl -s "https://bulktranscripts.co/api/v1/bulk/RUN_ID/results?limit=100" \
  -H "Authorization: Bearer $BULKTRANSCRIPTS_API_KEY"
```
Each item has `video_id`, `title`, `channel`, `duration`, `word_count` and
`status` (`ok`, `cached`, or `error` with a code). Every ok or cached video is
in the library, so `/transcript?video=ID` returns its text without a credit.
Two jobs per account at a time. Prefer a job over one-by-one fetches for
anything larger than about 20 videos.

### List a channel's videos (1 credit, up to 1000)
```bash
curl -s "https://bulktranscripts.co/api/v1/channel/videos?channel=@HANDLE&limit=100" \
  -H "Authorization: Bearer $BULKTRANSCRIPTS_API_KEY"
```
`channel` accepts @handle, channel URL, or UC… id.

### Search inside one channel (1 credit)
```bash
curl -s "https://bulktranscripts.co/api/v1/channel/search?channel=@HANDLE&q=TOPIC&limit=10" \
  -H "Authorization: Bearer $BULKTRANSCRIPTS_API_KEY"
```
Finds a creator's videos about a topic without listing the whole archive.

### Get one transcript
```bash
curl -s "https://bulktranscripts.co/api/v1/transcript?video=VIDEO_URL_OR_ID" \
  -H "Authorization: Bearer $BULKTRANSCRIPTS_API_KEY"
```
Params: `video` (watch URL, youtu.be, Shorts, bare 11-char id, or TikTok video
URL) · `language` (default `en`) · `segments=0` to omit timestamps (smaller) ·
`format=txt|md|srt|vtt|csv|ai` to get a rendered file instead of JSON ·
`fresh=1` to force re-extraction.

Response fields: `title`, `channel`, `duration`, `upload_date`, `language`,
`source` (manual_caption|auto_caption), `cached`, `word_count`, `text`,
`paragraphs[]` (silence-grouped — best for reading/chunking), `segments[]`
(`{text, start, duration}`), `billing`.

Long videos produce long text. For summarization, prefer `segments=0` and read
`paragraphs`.

### Balance
```bash
curl -s "https://bulktranscripts.co/api/v1/account" \
  -H "Authorization: Bearer $BULKTRANSCRIPTS_API_KEY"
```

## Playbook

- **Whole channel** → start a bulk job with the channel URL, tell the user
  the `videos_found` count (each new library transcript = 1 credit), poll at
  the pace `check_again_in_seconds` asks for, then read what you need from the
  library for free.
- **Deep research on a creator** → `channel/search` for the topic, pick
  candidates by title, fetch only those transcripts.

Errors come as `{"error": {"code", "message"}}`. The codes you will actually
hit, and what to do about each:


- `no_transcript` (404) — the video has no captions. Not charged. Skip it and
  carry on; in a batch this is normal, not a failure.
- `resolution_failed` (400) — a well-formed id or URL that could not be
  resolved (nonexistent, private, removed, or region-blocked). Handle it
  alongside `no_transcript`: skip the video and carry on.
- `missing_api_key` (401) — no key was sent. Ask the user to create a key at
  https://bulktranscripts.co/app?tab=mcp and provide it, then set
  `BULKTRANSCRIPTS_API_KEY` and retry.
- `invalid_api_key` (401) — the key sent is not valid. Ask the user to check it
  or create a new one at https://bulktranscripts.co/app?tab=mcp.
- `invalid_input` (400) — the `video` / `channel` / `playlist` parameter is
  missing, not a YouTube/TikTok reference, or otherwise malformed. A caller
  bug, not a video problem.
- `out_of_credits` (402) — balance exhausted. Tell the user and link
  https://bulktranscripts.co/#pricing.
- `rate_limited` (429) — respect the `Retry-After` header before retrying.
  Limits are per public IP: 120 requests/min overall, 30/min under `/api/v1/`
  (cache hits and `/account` count too), so pace bulk fetches at under 30/min.

Need everything in one skill (transcripts, search, channels, playlists, monitoring)? Use the full
[youtube-transcripts skill](https://github.com/pratie/youtube-transcript-skill).
Full reference: [bulktranscripts.co/docs](https://bulktranscripts.co/docs)
