---
name: using-vizard-api
description: Use when needing to clip long videos into short social media clips, edit short videos with subtitles or b-roll, publish clips to social platforms, or generate AI captions using Vizard.ai API. Use when user asks to automate video content creation with Vizard.
---

# Using Vizard.ai API

## Overview

Vizard API converts long videos into AI-clipped short videos optimized for TikTok, YouTube Shorts, and Instagram Reels. It also edits short videos with subtitles, B-roll, and branding. All endpoints use REST + JSON.

**Base URL:** `https://elb-api.vizard.ai/hvizard-server-front/open-api/v1`  
**Auth header:** `VIZARDAI_API_KEY: YOUR_API_KEY`  
**Requires paid Vizard plan.**

## Core Workflow

```
Submit Video → Poll for Results → (Optional) Publish / Generate Caption
```

### Step 1: Submit a Video

**Mode A — Clip a long video** (returns multiple clips):
```python
import requests, time

headers = {
    "Content-Type": "application/json",
    "VIZARDAI_API_KEY": "YOUR_API_KEY"
}

resp = requests.post(
    "https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/create",
    headers=headers,
    json={
        "videoUrl": "https://www.youtube.com/watch?v=XXXXX",
        "videoType": 2,        # 2=YouTube, 1=direct file, 3=GDrive, 4=Vimeo
        "lang": "en",          # or "auto" for auto-detect
        "preferLength": [0]    # 0=auto, 1=<30s, 2=30-60s, 3=60-90s, 4=>90s
    }
)
project_id = resp.json()["projectId"]
```

**Mode B — Edit a short video** (≤3 min, returns 1 edited video):
```python
resp = requests.post(
    "https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/create",
    headers=headers,
    json={
        "videoUrl": "https://example.com/video.mp4",
        "videoType": 1,
        "ext": "mp4",
        "lang": "auto",
        "getClips": 0,          # 0 = editing mode
        "subtitleSwitch": 1,
        "headlineSwitch": 1,
        "autoBrollSwitch": 1,
        "removeSilenceSwitch": 1,
        "ratioOfClip": 1        # 1=9:16, 2=1:1, 3=4:5, 4=16:9
    }
)
project_id = resp.json()["projectId"]
```

### Step 2: Poll for Results (every 30 seconds)

```python
def wait_for_clips(project_id, api_key, max_wait=1200):
    headers = {"VIZARDAI_API_KEY": api_key}
    url = f"https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/query/{project_id}"
    
    for _ in range(max_wait // 30):
        time.sleep(30)
        r = requests.get(url, headers=headers).json()
        if r["code"] == 2000 and r.get("videos"):
            return r["videos"]   # list of clip objects
        if r["code"] not in (2000, 1000):
            raise RuntimeError(f"Error: {r}")
    raise TimeoutError("Processing timed out")

clips = wait_for_clips(project_id, "YOUR_API_KEY")
# Each clip: videoId, videoUrl (valid 7 days), title, transcript, viralScore
```

### Step 3 (Optional): Publish to Social Media

```python
# First get connected account IDs
accounts = requests.get(
    "https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/social-accounts",
    headers={"VIZARDAI_API_KEY": "YOUR_API_KEY"}
).json()["accounts"]

# Then publish
requests.post(
    "https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/publish-video",
    headers={**headers},
    json={
        "finalVideoId": clips[0]["videoId"],
        "socialAccountId": accounts[0]["id"],
        "post": ""   # empty = AI auto-generates caption + hashtags
    }
)
```

### Step 3 (Optional): Generate AI Social Caption

```python
resp = requests.post(
    "https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/ai-social",
    headers=headers,
    json={
        "finalVideoId": clips[0]["videoId"],
        "aiSocialPlatform": 2,  # 1=General,2=TikTok,3=Instagram,4=YouTube,5=Facebook,6=LinkedIn,7=Twitter
        "tone": 2,              # 0=Neutral,1=Interesting,2=Catchy,3=Serious,4=Question
        "voice": 0              # 0=First person, 1=Third person
    }
)
caption = resp.json()["aiSocialContent"]
```

## Quick Reference

See `api-reference.md` for full parameter tables, videoType values, status codes, and editing options.

### Supported Video Sources (`videoType`)
| Value | Source |
|-------|--------|
| 1 | Direct file URL (.mp4/.mov/.avi/.3gp) — also requires `ext` |
| 2 | YouTube |
| 3 | Google Drive |
| 4 | Vimeo |
| 5 | StreamYard |
| 6 | TikTok |
| 7 | Twitter |
| 9 | Twitch |
| 10 | Loom |
| 11 | Facebook |
| 12 | LinkedIn |

### Key Status Codes
| Code | Meaning |
|------|---------|
| 2000 | Success |
| 1000 | Still processing (keep polling) |
| 4001 | Invalid API key |
| 4003 | Rate limit exceeded |
| 4007 | Insufficient account time/credits |
| 4008 | Failed to download video |

## Common Mistakes

- **Not waiting long enough:** 4K or long videos can take 10-30 min. Poll every 30s; don't give up after a few retries.
- **Using `getClips: 0` for a long video:** Editing mode only works for videos ≤3 minutes.
- **Missing `ext` for direct files:** `videoType: 1` requires `"ext": "mp4"` (or other format).
- **`videoUrl` expires after 7 days:** Re-query the API to get a fresh download link.
- **Social caption won't work on silent videos:** `ai-social` endpoint requires spoken dialogue.
