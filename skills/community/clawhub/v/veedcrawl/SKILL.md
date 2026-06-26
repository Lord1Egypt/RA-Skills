---
name: veedcrawl
description: Give OpenClaw the ability to access social media content. It can search across TikTok, Instagram, and YouTube for videos, watch TikTok/Reels/YouTube, retrieve metadata, get creator profiles, and extract insights from video content across platforms.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - VEEDCRAWL_API_KEY
      bins:
        - curl
    primaryEnv: VEEDCRAWL_API_KEY
    envVars:
      - name: VEEDCRAWL_API_KEY
        required: true
        description: API key for authenticated Veedcrawl requests.
      - name: VEEDCRAWL_BASE_URL
        required: false
        description: Optional API base URL override. Defaults to https://api.veedcrawl.com.
    homepage: https://docs.veedcrawl.com
---

# Veedcrawl API

Use Veedcrawl for public social video discovery and analysis across supported video platforms.

## Runtime

- Require `VEEDCRAWL_API_KEY` before making protected requests.
- Use `VEEDCRAWL_BASE_URL` when set. Otherwise use `https://api.veedcrawl.com`.
- Use `curl` for direct API calls.
- Consult `https://docs.veedcrawl.com` or `https://veedcrawl.com/openapi.json` when an endpoint shape is unclear.

Prepare shell examples with:

```bash
API_BASE="${VEEDCRAWL_BASE_URL:-https://api.veedcrawl.com}"
AUTH_HEADER="x-api-key: ${VEEDCRAWL_API_KEY}"
```

## Choose The Workflow

1. Start with `POST /v1/search` when the user gives a topic, keyword, creator idea, competitor, product, or trend instead of video URLs.
2. Start with `GET /v1/tiktok/profile` or `GET /v1/instagram/profile` when the user gives a creator username or public profile URL.
3. Call `GET /v1/metadata?url=...` for normalized per-video metadata, stats, author, tags, media details, and timestamps.
4. Call `POST /v1/transcript` when spoken content matters.
5. Call `POST /v1/extract` when the task needs structured conclusions such as hooks, claims, products, CTAs, format analysis, sponsorship signals, or summaries.
6. Shortlist before running bulk transcript or extraction jobs. Search and profile data can narrow the video set first.

## Async Jobs

`search`, `transcript`, and `extract` return a `jobId`.

1. Save the returned `jobId`.
2. Poll `GET /v1/search/{jobId}`, `GET /v1/transcript/{jobId}`, or `GET /v1/extract/{jobId}` until `status` is `completed` or `failed`.
3. Use `result` only after completion.
4. Surface a failed job clearly instead of guessing at missing output.
5. Preserve timestamps and source URLs when producing research notes, citations, evidence tables, or creator briefs.

## Request Examples

Search videos:

```bash
curl -X POST "$API_BASE/v1/search" \
  -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "skincare morning routine",
    "platforms": ["tiktok", "instagram", "youtube"],
    "limit": 25,
    "sort": "relevant",
    "timePeriod": "past_month",
    "filters": { "language": "en", "duration": "short", "minLikes": 1000 }
  }'
```

Poll a search job:

```bash
curl "$API_BASE/v1/search/JOB_ID" \
  -H "$AUTH_HEADER"
```

Inspect one video:

```bash
curl "$API_BASE/v1/metadata?url=VIDEO_URL" \
  -H "$AUTH_HEADER"
```

Get a creator profile:

```bash
curl "$API_BASE/v1/tiktok/profile?username=CREATOR_USERNAME&limit=12" \
  -H "$AUTH_HEADER"
```

Queue a transcript:

```bash
curl -X POST "$API_BASE/v1/transcript" \
  -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -d '{"url":"VIDEO_URL","mode":"auto"}'
```

Extract structured findings:

```bash
curl -X POST "$API_BASE/v1/extract" \
  -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -d '{"url":"VIDEO_URL","prompt":"Extract the hook, main claim, and call to action"}'
```

## Output Defaults

- Prefer structured tables or JSON when comparing videos or creators.
- Keep video URL, platform, creator identity, and timestamps with extracted findings.
- Do not infer engagement stats, transcript text, or extraction output that the API did not return.
- State when a result is based on metadata only versus transcript or extraction evidence.
