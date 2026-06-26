---
name: trio-vision
description: Turn any live camera into a smart camera — describe what to watch for in plain English, get alerts in your chat when it happens. Ask questions about any live stream (YouTube, Twitch, security cameras, RTSP), set up continuous monitoring with custom conditions, or get periodic summaries of what's happening. No ML expertise required.
homepage: https://docs.machinefi.com
license: Apache-2.0
metadata: {"openclaw":{"emoji":"📹","requires":{"env":["TRIO_API_KEY"],"anyBins":["curl","python3"]},"primaryEnv":"TRIO_API_KEY"}}
---

# Trio Vision — Turn Any Camera Into a Smart Camera

Stop getting dumb motion alerts for every shadow. Describe what actually matters in plain English — get notified only when it happens, right in your chat. Powered by [Trio by MachineFi](https://machinefi.com).

## When to Use

- User asks what's happening on a camera, stream, or video feed ("is anyone at my front door?")
- User wants smart alerts for specific events ("tell me when a package is delivered", "alert me if my dog gets on the couch")
- User wants to monitor something they can't watch themselves (construction site, parking spot, warehouse)
- User wants periodic summaries of a live feed ("summarize this stream every 10 minutes")
- User provides any live stream URL: YouTube Live, Twitch, RTSP/RTSPS cameras, HLS streams

## Prerequisites

- A Trio API key. Get one free (100 credits) at https://console.machinefi.com
- Set the key: `export TRIO_API_KEY=your_key_here`
- Base URL: `https://trio.machinefi.com/api`

## Available Actions

### 1. Check Once (Quick Snapshot)

Ask a yes/no question about what's currently visible on a stream. Costs 1 credit ($0.01).

```bash
curl -s -X POST "https://trio.machinefi.com/api/check-once" \
  -H "Authorization: Bearer $TRIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "stream_url": "STREAM_URL_HERE",
    "condition": "NATURAL_LANGUAGE_CONDITION_HERE"
  }' | python3 -m json.tool
```

**Optional parameters:**
- `"include_frame": true` — returns the analyzed frame as base64 image
- `"input_mode": "clip"` — analyze a short video clip instead of a single frame (better for motion detection)
- `"clip_duration_seconds": 5` — clip length (1-10 seconds, only with clip/hybrid mode)

**Response fields:**
- `triggered` (boolean) — whether the condition matched
- `explanation` (string) — VLM's reasoning about what it sees
- `latency_ms` — processing time in milliseconds

**Input mode guidance:**
- Use `"frames"` (default) for static objects: "Is there a car in the driveway?", "Is the door open?"
- Use `"clip"` for motion/actions: "Is someone walking?", "Did a package get delivered?"
- Use `"hybrid"` for maximum accuracy (costs more)

### 2. Live Monitor (Continuous Event Detection)

Monitor a stream continuously and get alerted when a condition becomes true. Costs 2 credits/min ($0.02/min).

```bash
curl -s -X POST "https://trio.machinefi.com/api/live-monitor" \
  -H "Authorization: Bearer $TRIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "stream_url": "STREAM_URL_HERE",
    "condition": "NATURAL_LANGUAGE_CONDITION_HERE",
    "interval_seconds": 10,
    "monitor_duration_seconds": 600,
    "max_triggers": 1
  }' | python3 -m json.tool
```

**Optional parameters:**
- `"webhook_url": "https://your-server.com/webhook"` — receive HTTP POST notifications on trigger
- `"interval_seconds": 10` — check frequency (5-300 seconds)
- `"monitor_duration_seconds": 600` — how long to monitor (min 5 seconds)
- `"trigger_cooldown_seconds": 60` — minimum seconds between triggers
- `"max_triggers": null` — set to null for unlimited triggers
- `"input_mode": "clip"` — default for live-monitor, good for motion

**Response:** Returns a `job_id`. Use it to check status or cancel.

**Delivery modes (automatic based on request):**
- If `webhook_url` is set → events POST to your webhook
- If `Accept: text/event-stream` header is set (no webhook) → SSE stream
- Otherwise → poll with `GET /jobs/{job_id}`

### 3. Live Digest (Periodic Summaries)

Get narrative summaries of what's happening on a stream at regular intervals. Costs 2 credits/min ($0.02/min).

```bash
curl -s -X POST "https://trio.machinefi.com/api/live-digest" \
  -H "Authorization: Bearer $TRIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "stream_url": "STREAM_URL_HERE",
    "window_minutes": 10,
    "capture_interval_seconds": 60
  }' | python3 -m json.tool
```

**Optional parameters:**
- `"window_minutes": 10` — summary window length (1-60 minutes)
- `"capture_interval_seconds": 60` — frame capture frequency (10-300 seconds)
- `"webhook_url": "https://..."` — receive summaries via webhook
- `"max_windows": 3` — number of summary windows before stopping
- `"include_frames": true` — embed frames in summaries

**Response:** Returns a `job_id`.

### 4. Check Job Status

```bash
curl -s "https://trio.machinefi.com/api/jobs/JOB_ID_HERE" \
  -H "Authorization: Bearer $TRIO_API_KEY" | python3 -m json.tool
```

**Job statuses:** `pending`, `running`, `stopped`, `completed`, `failed`

### 5. List All Jobs

```bash
curl -s "https://trio.machinefi.com/api/jobs?limit=20&offset=0" \
  -H "Authorization: Bearer $TRIO_API_KEY" | python3 -m json.tool
```

Optional query params: `status=running`, `type=live-monitor`, `limit=20`, `offset=0`

### 6. Cancel a Job

```bash
curl -s -X DELETE "https://trio.machinefi.com/api/jobs/JOB_ID_HERE" \
  -H "Authorization: Bearer $TRIO_API_KEY" | python3 -m json.tool
```

## Recommended Workflows

### Quick Check Workflow
1. Run check-once with the user's question and stream URL
2. Report the `triggered` result and `explanation` to the user
3. If the API returns an error about the stream, show the error and remediation

### Monitoring Workflow
1. Test the condition with check-once first to verify it works
2. If the condition works, start live-monitor with appropriate settings
3. Return the job_id and inform user how to check status or cancel
4. If webhook_url is available, set it up for push notifications

### Summary Workflow
1. Start live-digest with the stream URL and appropriate window/interval
2. Return the job_id so the user can check results later

## Condition Writing Tips

- Frame as binary yes/no questions: "Is there a person visible in the frame?"
- Be specific: "Is there smoke rising from the building roof?" not "Is there smoke?"
- One intent per condition — don't combine multiple checks
- Use positive phrasing: "Are vehicles visible?" not "Is the parking lot not empty?"
- Always test conditions with check-once before starting live-monitor

## Error Handling

All errors return this structure:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "remediation": "Actionable fix suggestion"
  }
}
```

Common error codes:
- `NOT_LIVESTREAM` — URL is not a live stream. Confirm it's actively broadcasting.
- `STREAM_FETCH_FAILED` — Cannot reach the stream. Check URL and network.
- `STREAM_OFFLINE` — Stream exists but is offline. Wait for it to go live.
- `MAX_JOBS_REACHED` — Too many concurrent jobs. Cancel old ones with DELETE /jobs/{id}.

If you get an error, always show the `remediation` field to the user — it contains actionable guidance.

## Pricing Reference

| Action | Cost |
|--------|------|
| Check once | $0.01 / request |
| Live monitor | $0.02 / minute |
| Live digest | $0.02 / minute |

Free tier: 100 credits ($1.00) on signup at https://console.machinefi.com

## Rules

- NEVER expose or log the $TRIO_API_KEY value in output shown to the user.
- ALWAYS show the `explanation` field from check-once responses — it provides the VLM's reasoning.
- ALWAYS test conditions with check-once before starting a live-monitor job.
- When a user provides a stream URL, auto-detect whether they want a quick check, monitoring, or digest based on their intent.
- For monitoring jobs, always return the job_id so the user can check status or cancel later.
- If the API returns an error, show the error code and remediation to the user.
- Inform users about credit costs before starting live-monitor or live-digest jobs (they charge per minute).
