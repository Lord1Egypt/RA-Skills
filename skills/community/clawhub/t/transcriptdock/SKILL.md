---
name: transcriptdock
description: Fetch timed transcripts and captions from YouTube, TikTok and Instagram Reel links with the Transcript Dock API or hosted MCP server.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TRANSCRIPTDOCK_API_KEY
      bins:
        - curl
    primaryEnv: TRANSCRIPTDOCK_API_KEY
    envVars:
      - name: TRANSCRIPTDOCK_API_KEY
        required: true
        description: Transcript Dock API key starting with td_live_.
      - name: TRANSCRIPTDOCK_BASE_URL
        required: false
        description: Optional API origin. Defaults to https://www.transcriptdock.com.
    emoji: "📝"
    homepage: https://www.transcriptdock.com/docs/mcp
---

# Transcript Dock

Use this skill when the user wants a transcript, captions, subtitles or timed
text from a YouTube, TikTok or Instagram Reel link, or from a media file they
own.

Transcript Dock returns the text plus segment timing. It exports JSON, SRT, VTT
and TXT. YouTube and TikTok use native captions first. Instagram Reels use AI
transcription on paid plans (beta) and have no native captions.

## Preferred path: hosted MCP

If the client supports Streamable HTTP MCP, connect to:

```text
https://www.transcriptdock.com/mcp
```

Authenticate with OAuth 2.1, or send the API key as a bearer token.

Useful tools:

- `get_video_transcript` submits one URL, waits and returns the transcript text.
  This is the simplest path for a single video.
- `transcribe` creates a job when you need the job id early or want a specific
  mode.
- `wait_for_job` polls a job until it reaches a terminal state.
- `get_transcript` returns the stored result and can request SRT or VTT.
- `get_job` and `list_jobs` inspect job state and history.
- YouTube and TikTok discovery tools are available when the user wants search
  results or channel inventory.

## REST fallback

Base URL: `TRANSCRIPTDOCK_BASE_URL`, default `https://www.transcriptdock.com`.

Every request needs:

```text
Authorization: Bearer $TRANSCRIPTDOCK_API_KEY
```

The key is workspace scoped and starts with `td_live_`. Never print it, commit
it, paste it into a public issue or send it to any host other than the configured
Transcript Dock origin.

### 1. Submit a job

```bash
curl --fail-with-body --max-time 30 \
  --request POST "https://www.transcriptdock.com/v1/jobs" \
  --header "Authorization: Bearer $TRANSCRIPTDOCK_API_KEY" \
  --header "Content-Type: application/json" \
  --header "Idempotency-Key: $USER_SUPPLIED_REPLAY_KEY" \
  --data '{
    "source": { "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw" },
    "mode": "captions_only"
  }'
```

`source.url` also accepts TikTok video links and Reel links. For a file the user
owns, upload it first with `POST /v1/uploads`, then submit
`{"source":{"upload_id":"..."},"mode":"transcribe"}`.

Modes:

- `captions_only` uses existing captions. It costs 1 credit and works for
  YouTube and TikTok. Always try this first.
- `auto` and `transcribe` use AI transcription and cost credits per started
  minute. Use them only when the user asks for AI transcription and is willing
  to pay. Set `max_credits` to a deliberate ceiling.

Use a stable idempotency key per logical submission. Reusing the same key with a
different body returns HTTP 409. Reusing it with the same body replays the job
instead of charging twice.

Response: HTTP 202 with a job object. Keep `id`. Respect the `Retry-After`
header before the first poll.

### 2. Poll the job

```bash
curl --fail-with-body --max-time 30 \
  --header "Authorization: Bearer $TRANSCRIPTDOCK_API_KEY" \
  "https://www.transcriptdock.com/v1/jobs/$JOB_ID"
```

Poll until `status` is `succeeded`, `failed` or `cancelled`. Use a deadline and
a bounded sleep. Do not poll in a tight loop. When the job succeeds, read
`result_id`.

Job statuses: `queued`, `processing`, `awaiting_provider`, `succeeded`,
`failed`, `cancelled`.

### 3. Read the transcript

```bash
curl --fail-with-body --max-time 30 \
  --header "Authorization: Bearer $TRANSCRIPTDOCK_API_KEY" \
  "https://www.transcriptdock.com/v1/transcripts/$RESULT_ID"
```

The result contains the text, language and segments with timings. Export without
paying again:

```text
GET /v1/transcripts/{id}/export?format=txt
GET /v1/transcripts/{id}/export?format=json
GET /v1/transcripts/{id}/export?format=srt
GET /v1/transcripts/{id}/export?format=vtt
```

A timed format returns HTTP 422 when the stored result has no usable timing.
Plain TXT remains available.

## Costs

- Free plan: 50 caption credits every 30 days.
- Caption transcript: 1 credit.
- AI transcription: billed per started minute. The current rate is published by
  `GET /v1/capabilities`; do not hardcode a rate that contradicts it.
- A retained result reused inside the same workspace is free.
- Paid plans start at 19 USD per month.

Check `GET /v1/capabilities` before using AI transcription for a new source type.
Never promise unlimited free transcription.

## Error handling

- 401: missing or invalid API key.
- 402: plan or credit limit reached. Do not retry blindly.
- 404: the job, transcript or video is inaccessible or gone.
- 409: the idempotency key was reused with a different body.
- 422: invalid input, or the capability is unavailable for that source.
- 429: rate limited. Back off and respect `Retry-After`.

A failed job is not a successful transcript. Report the typed error to the user
instead of returning empty text.

## Notes

- Do not scrape YouTube, TikTok or Instagram directly for this task. Use the
  API or MCP server.
- Do not send cookies, session tokens or unrelated credentials.
- Keep exports and transcript text inside the user's workspace unless the user
  asks to share them.
