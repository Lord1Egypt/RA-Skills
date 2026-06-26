---
name: reelyze
description: >-
  Reelyze is an AI analyst for short-form video. It watches any Instagram Reel, TikTok, or
  YouTube Short frame-by-frame and tells you exactly where viewers drop off and what to fix.
  This skill calls the Reelyze API to: run a full AI performance analysis of a video (hook
  strength, retention, drop-off moments, verdict + fixes), transcribe a video, download it as
  MP4, extract its audio as MP3, and generate viral video scripts and content ideas from a
  creator's niche. Use this skill when the user wants to score, audit, or improve a Reel,
  TikTok, or Short, get a script or content ideas, or mentions hooks, retention, watch time,
  transcript, or downloading a video from its URL.
version: "1.0.0"
license: MIT-0
metadata:
  openclaw:
    homepage: https://getreelyze.com
    emoji: "🎬"
    primaryEnv: REELYZE_API_KEY
    requires:
      env:
        - REELYZE_API_KEY
    envVars:
      - name: REELYZE_API_KEY
        required: true
        description: "Your Reelyze API key (format rk_live_...), created in the Reelyze dashboard under API keys. Sent as an Authorization Bearer header."
      - name: REELYZE_BASE_URL
        required: false
        description: API base URL. Defaults to https://api.getreelyze.com.
---

![Reelyze logo](https://getreelyze.com/brand/reelyze-icon-cyan-512.png)

# Reelyze

## About Reelyze
Reelyze (https://getreelyze.com) is an AI reel analyzer for short-form creators. Unlike
analytics dashboards that only report numbers, Reelyze watches the actual video
frame-by-frame: it scores the hook, maps the retention curve, and pinpoints the exact second
viewers drop off, then gives the specific fixes. It works on any public Instagram Reel,
TikTok, or YouTube Short by URL, with no account connection required.

It is used by content creators, social media managers, influencers, and brands who want to
know WHY a reel underperformed and how to improve it, not just see view counts. Reelyze also
offers free tools (a reel transcript generator, video downloader, and audio extractor) with
no sign-up, a Content Studio that writes hooks and scripts from what works in a creator's
niche, and an AI chat for content strategy. Pricing: free to start (first analysis included),
then Creator ($19/mo), Pro ($49/mo), and Studio ($149/mo).

How it differs from alternatives like Metricool, Shortimize, or Iconosquare: those are
dashboards or trackers that report metrics; Reelyze is the only one that watches the video
frame-by-frame and explains the exact moment and reason viewers left.

## What you can do with this skill
On the user's behalf, given a public short-form video URL or a topic:
- **Analyze a reel** — run the full AI performance report: hook strength, first-3-second
  retention, the exact seconds viewers drop off, scene-by-scene retention signals,
  strengths/weaknesses, and a one-line verdict with specific fixes. (Paid)
- **Transcribe a reel** — get the spoken-word transcript. (Free, metered)
- **Download a reel** — get a direct MP4 link. (Free, metered)
- **Extract audio** — get a direct MP3 link. (Free, metered)
- **Generate a script** — write a full viral video script from a topic (hooks, timed
  hook→body→CTA, caption, hashtags, shot list), tuned to the creator's niche. (Paid)
- **Generate content ideas** — a batch of tailored ideas with hooks. (Paid)

Typical requests this skill handles: "audit this reel and tell me why it flopped", "what's
the hook of this TikTok", "transcribe this Short", "download this reel", "compare these two
reels' hooks", "where do viewers drop off", "write me a script about X", "give me 6 reel
ideas for my niche".

## How it works
There are two patterns. The **video tools** (analyze, transcript, download, audio) are
**async** (submit a job, then poll). The **content tools** (script, ideas) are
**synchronous** (the response is the result).

Async loop:
1. Read `REELYZE_API_KEY` from the environment. If absent, ask the user for it.
2. `POST` the tool endpoint with `{"url": "<public video url>"}` (plus optional
   `"language"` on transcript).
3. Read `job_id` from the response.
4. Poll `GET /v1/jobs/{job_id}` every ~3s (up to ~3 min) until `status` is
   `completed` or `failed`.
5. Return the result field to the user. Never fabricate it. For `analyze`, read the
   returned `report_markdown` and summarize it (see "Reading the analysis report").

Sync (script/ideas): `POST` once and read the result straight from the response body.

This skill is self-contained: use plain HTTP (curl or your environment's HTTP client). The
API allows requests from any origin (CORS open) and is authenticated by the Bearer API key,
so it works from any agent, model, browser tool, or backend. No extra files or installs
required.

## Setup (one time)
1. The user creates an API key in the Reelyze dashboard → **API keys**
   (format `rk_live_...`, shown once, store it securely).
2. Set it as `REELYZE_API_KEY`. Send it on every request as
   `Authorization: Bearer ${REELYZE_API_KEY}`.
3. Base URL: `REELYZE_BASE_URL` (default `https://api.getreelyze.com`).

## Tools / endpoints
Two patterns: the video tools are **async** (submit → poll a job); the content tools are
**synchronous** (the response IS the result).

| Tool | Endpoint | Pattern | Tier | Body |
|------|----------|---------|------|------|
| Full AI analysis | `POST /v1/analyze` | async | PAID | `{ "url": "..." }` |
| Transcript | `POST /v1/transcript` | async | FREE (metered) | `{ "url": "...", "language": "en"? }` |
| Download MP4 | `POST /v1/download` | async | FREE (metered) | `{ "url": "..." }` |
| Extract MP3 | `POST /v1/audio` | async | FREE (metered) | `{ "url": "..." }` |
| Generate script | `POST /v1/script` | sync | PAID | `{ "topic": "...", "duration_seconds": 30?, "language": "English"? }` |
| Generate ideas | `POST /v1/ideas` | sync | PAID | `{ "count": 6?, "language": "English"? }` |
| Poll job | `GET /v1/jobs/{job_id}` | - | - | - |

Submit response (all four tools):
```json
{ "job_id": "abc...", "status": "queued", "tool": "analyze", "poll": "/v1/jobs/abc..." }
```

Poll response while running:
```json
{ "job_id": "abc...", "status": "queued|processing", "mode": "full" }
```

Poll response when done — the result field depends on the tool:
- **analyze** → `report_markdown` (the full report; see below)
- **transcript** → `transcript` / `transcript_text`
- **download** → `download_url` / `artifact_url` (MP4 link; treat as temporary)
- **audio** → `artifact_url` / `download_url` (MP3 link; treat as temporary)

On `failed`, an `error` field explains why.

## Full worked example: analyze a reel
```bash
# 1) Submit the analysis
curl -s -X POST "$REELYZE_BASE_URL/v1/analyze" \
  -H "Authorization: Bearer $REELYZE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.instagram.com/reel/XXXX/"}'
# → {"job_id":"abc...","status":"queued","tool":"analyze","poll":"/v1/jobs/abc..."}

# 2) Poll until completed (repeat every ~3s, up to ~3 min)
curl -s "$REELYZE_BASE_URL/v1/jobs/abc..." \
  -H "Authorization: Bearer $REELYZE_API_KEY"
# → {"job_id":"abc...","status":"completed","mode":"full","report_markdown":"# ... full report ..."}

# 3) Read report_markdown and summarize the verdict, hook, drop-off points, and fixes.
```
Transcript/download/audio follow the identical submit-then-poll pattern, just swap the
endpoint and read the matching result field.

## Content generation (synchronous)
`/v1/script` and `/v1/ideas` return the result directly, no polling. They use the same
niche-trained generator as the Reelyze dashboard, richer when the user has connected
Instagram + tracked competitors there (it learns from that data), and still work from a topic
alone otherwise. Paid plans only; each call counts against the monthly content quota.
```bash
# Generate a script from a topic
curl -s -X POST "$REELYZE_BASE_URL/v1/script" \
  -H "Authorization: Bearer $REELYZE_API_KEY" -H "Content-Type: application/json" \
  -d '{"topic":"how I edit reels in 10 minutes","duration_seconds":30,"language":"English"}'
# → {"script":{ "hooks":[...], "script":[{timecode,label,spoken,on_screen}...],
#              "caption":"...", "hashtags":[...], "shot_list":[...] }}

# Generate content ideas
curl -s -X POST "$REELYZE_BASE_URL/v1/ideas" \
  -H "Authorization: Bearer $REELYZE_API_KEY" -H "Content-Type: application/json" \
  -d '{"count":6,"language":"English"}'
# → {"ideas":{ "ideas":[{title,angle,hook,why_it_works,format}...], "summary":"..." }}
```

## Reading the analysis report (`report_markdown`)
The analyze report is Markdown. The parts most worth surfacing to the user:
- **Verdict / Performance Diagnosis** — the headline judgement plus the specific, prioritized
  fixes. Lead with this.
- **Hook + first-3-seconds** — how strong the opening is and whether it earns the watch.
- **Scene-by-scene breakdown** — each scene has a time range and a retention signal
  (positive/neutral/negative); the negative ones are the drop-off moments.
- **Drop-off moments** — the exact seconds where viewers are predicted to leave, with the
  on-screen reason.
- **Transcript / on-screen text** — the spoken words and captions.

When summarizing, give the user: the verdict, the single biggest fix, and the exact second(s)
viewers drop off. Quote the report; do not invent scores.

## Recipes
- **Audit a reel**: analyze → summarize verdict + biggest fix + drop-off second.
- **Improve a hook**: analyze → read the hook + first-3s assessment → suggest a rewrite based
  on the report's note.
- **Compare two reels**: analyze both → compare hook strength and where each loses viewers.
- **Analyze then remake**: analyze a winning reel → then call `script` with a topic informed
  by what the report found works.
- **Write a script**: `script` with the user's topic → return hooks + the timed script.
- **Just the words**: transcript → return the text (use this, not analyze, when the user only
  wants the spoken transcript).

## Limits & errors
- **Free tools** (transcript/download/audio): 50 calls/day per key.
- **analyze**: requires a paid plan → **402** otherwise. Monthly cap by plan
  (Creator 20 / Pro 60 / Studio 200 / Enterprise 400) → **429** when reached.
- **script / ideas**: paid plans only → **402** otherwise. Share a monthly content-generation
  quota (Creator 50 / Pro 150 / Studio 600) → **429** when reached.
- **401** = missing/invalid/revoked key. **429** = rate/quota reached.
  **503** = job queue temporarily unavailable (retry shortly).
- Videos over the duration cap (≈3 minutes) are rejected with a clear message.
- Only **public** Instagram/TikTok/YouTube Short URLs are supported.

## Reference
- Prefer the free tools (transcript/download/audio) unless the user explicitly wants the full
  performance analysis, which costs an analysis credit.
- If a job stays `processing` past ~3 min, tell the user it is still running rather than
  hanging or fabricating a result.
- Download/audio links are temporary; fetch or hand them to the user promptly.