---
name: youtube-apify-transcript
version: 1.4.0
description: Fetch YouTube transcripts via the Apify API. Works from cloud IPs (Hetzner, AWS, etc.) by bypassing YouTube's bot detection. Features local caching (free repeat requests) and batch mode. Requires APIFY_API_TOKEN and the Python requests library.
tags: [youtube, transcript, apify, video, subtitles, captions, cloud-ip, free-tier, web-scraping, caching, batch]
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["APIFY_API_TOKEN"]
    primaryEnv: APIFY_API_TOKEN
    envVars:
      - name: APIFY_API_TOKEN
        required: true
        description: "Apify API token from https://console.apify.com/account/integrations"
      - name: YT_TRANSCRIPT_CACHE_DIR
        required: false
        description: "Cache directory. Defaults to .cache/ in the skill directory."
    note: "Install the Python dependency once: python3 -m pip install requests"
---

# youtube-apify-transcript

Fetch YouTube transcripts via Apify API (works from cloud IPs, bypasses YouTube bot detection).

## Why Apify?

YouTube blocks transcript requests from cloud IPs (AWS, GCP, etc.). Apify runs the request through residential proxies, bypassing bot detection.

## Default actor

`topaz_sharingan/youtube-transcript-scraper-1` (YouTube Transcript Ninja). Store sheet: https://apify.com/topaz_sharingan/youtube-transcript-scraper-1

Checked against the Apify API on 2026-08-31:

- Public, not deprecated (`isDeprecated: false`, `notice: NONE`)
- Last code change: 2026-07-19
- 30-day public runs: 36,362 succeeded, 0 failed, 91 timed out, 18 aborted (36,471 total)

### Cost

Pay per event: $0.01 per result ($10.00 per 1,000 results). The actor page states platform compute is included in that event price. Older docs that said $0.007 per video were wrong.

Apify Free plan (https://apify.com/pricing, 2026-08-31): $5 prepaid usage per month, no credit card. Unused credits do not roll over.

Free-tier video count: $5 / $0.01 = **500 videos per month**, not 714. (714 was $5 / $0.007.) Repeat requests served from the local cache do not start an actor run.

Track spend at https://console.apify.com/billing

### Input

OpenAPI input schema on 2026-08-31 has two fields:

| Field | Type | Required | Default | Role |
| --- | --- | --- | --- | --- |
| `startUrls` | string[] | yes | (none) | YouTube video URLs |
| `timestamps` | boolean | no | `false` | `true`: transcript as `{timestamp, text}` array. `false`: joined text |

There is no language field. `--lang` on the CLI does not change the default actor's input. The script only forwards `--lang` for other actor IDs (`pintostudio`, `starvibe`, `karamelo`). For `topaz_sharingan~Youtube-Transcript-Scraper-1` it sends `startUrls` only.

```json
{
  "startUrls": ["https://www.youtube.com/watch?v=VIDEO_ID"],
  "timestamps": false
}
```

The schema types `startUrls` items as strings. The script currently sends `[{"url": "..."}]` Request-list objects.

### Output

Actor sheet examples:

- `timestamps: false` → `{"transcript": "plain text..."}`
- `timestamps: true` → `{"transcript": [{"timestamp": "0:01", "text": "..."}]}`

The skill script also looks for `text`, `captions`, `title` / `videoTitle`, and `channelName`. If a run returns only `transcript`, formatting depends on whether that value is a string or a list.

## Links

- [Apify Pricing](https://apify.com/pricing)
- [Get API token](https://console.apify.com/account/integrations)
- [YouTube Transcripts Actor](https://apify.com/topaz_sharingan/youtube-transcript-scraper-1)

## Setup

1. Create a free Apify account: https://apify.com/
2. Get your API token: https://console.apify.com/account/integrations
3. Set the environment variable and install `requests` yourself. OpenClaw has no `kind: pip` installer (allowed kinds: brew, node, go, uv, download), so this is a manual step.

```bash
# Add to ~/.bashrc or ~/.zshrc
export APIFY_API_TOKEN="apify_api_YOUR_TOKEN_HERE"

# Python dependency (once)
python3 -m pip install requests

# Or use .env file (never commit this!)
echo 'APIFY_API_TOKEN=apify_api_YOUR_TOKEN_HERE' >> .env
```

## Usage

### Basic Usage

```bash
# Get transcript as text (uses cache by default)
python3 scripts/fetch_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Short URL also works
python3 scripts/fetch_transcript.py "https://youtu.be/VIDEO_ID"
```

### Options

```bash
# Output to file
python3 scripts/fetch_transcript.py "URL" --output transcript.txt

# JSON format (includes timestamps when the payload has them)
python3 scripts/fetch_transcript.py "URL" --json

# Both: JSON to file
python3 scripts/fetch_transcript.py "URL" --json --output transcript.json

# --lang is accepted by the CLI but is not sent to the default actor
# (no language field on topaz_sharingan/youtube-transcript-scraper-1).
python3 scripts/fetch_transcript.py "URL" --lang de
```

### Caching

Transcripts are cached locally by default. Repeat requests for the same video do not start an actor run.

```bash
# First request: fetches from Apify ($0.01)
python3 scripts/fetch_transcript.py "URL"

# Second request: uses cache
python3 scripts/fetch_transcript.py "URL"
# Output: [cached] Transcript for: VIDEO_ID

# Bypass cache (force fresh fetch)
python3 scripts/fetch_transcript.py "URL" --no-cache

# View cache stats
python3 scripts/fetch_transcript.py --cache-stats

# Clear all cached transcripts
python3 scripts/fetch_transcript.py --clear-cache
```

Cache location: `.cache/` in skill directory (override with `YT_TRANSCRIPT_CACHE_DIR` env var)

### Batch Mode

Process multiple videos at once:

```bash
# Create a file with URLs (one per line)
cat > urls.txt << EOF
https://youtube.com/watch?v=VIDEO1
https://youtu.be/VIDEO2
https://youtube.com/watch?v=VIDEO3
EOF

# Process all URLs
python3 scripts/fetch_transcript.py --batch urls.txt

# Output:
# [1/3] Fetching VIDEO1...
# [2/3] [cached] VIDEO2
# [3/3] Fetching VIDEO3...
# Batch complete: 2 fetched, 1 cached, 0 failed
# [Cost: ~$0.020 for 2 API call(s)]

# Batch with JSON output to file
python3 scripts/fetch_transcript.py --batch urls.txt --json --output all_transcripts.json
```

The script's cost line prints $0.01 per result, so two fetched videos show about $0.02.

### Output Formats

**Text (default):**
```
Hello and welcome to this video.
Today we're going to talk about...
```

**JSON (--json):**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Video Title",
  "transcript": [
    {"start": 0.0, "duration": 2.5, "text": "Hello and welcome"},
    {"start": 2.5, "duration": 3.0, "text": "to this video"}
  ],
  "full_text": "Hello and welcome to this video..."
}
```

The actor's timestamped items use `timestamp` (string like `"0:01"`), not `start` / `duration`. The JSON example above is the skill script's shape when captions already have those keys.

## Agent Instructions

When the user asks to summarize a YouTube video, first fetch the transcript using the script, then summarize the transcript text directly using your own model capabilities. Do NOT use --summarize flag.

## Error Handling

The script handles common errors:

- Invalid YouTube URL
- Video has no transcript
- API quota exceeded
- Network errors

## Metadata

Runtime requirements live in the YAML frontmatter (`metadata.openclaw`). OpenClaw 2.0 (v2026.8.1) installer kinds are brew, node, go, uv, and download. There is no `kind: pip`. Install `requests` with `python3 -m pip install requests`.
