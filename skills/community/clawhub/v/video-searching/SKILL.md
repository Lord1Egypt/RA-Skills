---
name: video-searching
description: Search and analyze videos across YouTube, TikTok, Instagram, and X/Twitter via the Memories.ai Video Searching API.
user-invocable: true
metadata: {"openclaw":{"os":["darwin","linux"],"homepage":"https://api-tools.memories.ai/agents/video-searching-api","requires":{"bins":["curl","jq"],"env":["MEMORIES_API_KEY"]}}}
---

# Video Searching Skill

Use this skill when the user asks to find, compare, or analyze social videos (YouTube, TikTok, Instagram, Twitter/X), or explicitly invokes `/video_search`.

This skill calls the Memories.ai Video Searching API — a managed, token-authenticated endpoint that searches across platforms and returns structured results via SSE.

## Triggering

Run this workflow when either condition is true:

1. Message starts with `/video_search`.
2. The user asks for video sourcing/trend/creator/brand analysis and wants concrete video links.

If `/video_search` is used with no query body, ask for the missing query.

## Execution contract

1. Resolve query text:
   - `/video_search ...` → strip `/video_search` and use remaining text.
   - Free-form → use user message as query.

2. Build the API request JSON body:
   - `query` (required): the user's search query
   - `platforms` (optional): array of `youtube`, `tiktok`, `instagram`, `twitter` — only set if user specifies platforms
   - `max_results` (optional, default 10): number of video results
   - `time_frame` (optional): `past_24h`, `past_week`, `past_month`, `past_year` — only set if user specifies recency
   - `max_steps` (optional, default 10): max agent iterations
   - `enable_clarification` (optional, default false): set to true if user query is vague

3. Call the runner script:
   ```
   <skill_dir>/scripts/run_video_query.sh \
     --query "<query>" \
     [--platforms "youtube,tiktok"] \
     [--max-results 10] \
     [--time-frame past_week] \
     [--enable-clarification]
   ```

4. Start with `exec` using `background: true`.
5. Poll with `process` using `action: "poll"` every 2–4 seconds until process exits.
6. Parse NDJSON output and render only these events:
   - `started` → send: `🔍 Starting video search...`
   - `progress` → send concise progress update from `message` field (throttle: skip if last update was < 3s ago)
   - `complete` → send final formatted response (see below)
   - `clarification` → ask the clarification question directly; treat as final response
   - `error` → send concise failure reason with one actionable next step
7. Do not forward raw `tool_call` or `tool_result` events to the user.

## Final response format

When terminal event is `complete`:

1. One short paragraph conclusion (from `answer` field).
2. Top video references (up to 5 by default):
   - `title`
   - `url`
   - `platform` badge (e.g. 🎬 YouTube, 🎵 TikTok, 📸 Instagram, 🐦 X)
   - one-line `relevance_note`
   - key metrics: views, likes, engagement rate (if available)
3. Footer: `⏱ {execution_time_seconds}s · {steps_taken} steps · {tools_used}`

If fewer videos exist, show all available references.

When terminal event is `clarification`:

1. Ask the clarification question directly.
2. Present options if provided.
3. Treat as final response for the current run.

When terminal event is `error`:

1. Send concise failure reason.
2. Include one actionable next step.

## Safety and fallback

1. If `MEMORIES_API_KEY` is not set, tell the user:
   > ⚠️ Missing `MEMORIES_API_KEY`. Set it in your OpenClaw environment variables to use this skill.
   > Get your API key at https://api-tools.memories.ai
2. If the API returns a non-SSE error (HTTP 4xx/5xx), display the error message.
3. Never fabricate video URLs or metrics.
4. If the API is unreachable, suggest checking network connectivity and API status.
