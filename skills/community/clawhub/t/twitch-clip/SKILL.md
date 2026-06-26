---
name: twitch-clip
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["curl"],"env":["TWITCH_CLIENT_ID","TWITCH_ACCESS_TOKEN","TWITCH_BROADCASTER_ID"]},"os":["linux","darwin"]}}
description: Create Twitch clips of the current live stream via the Twitch API. Use when a streamer says "clip that", "clip the last X seconds", "make a clip", "clip it", or any variation requesting a clip of the current broadcast. Requires Twitch API credentials configured in environment variables. Has a 30-second cooldown between clips to prevent spam.
---

# Twitch Clip Skill

Creates a clip of the last 30–60 seconds of a live Twitch stream via the Twitch Clips API. Includes a 30-second cooldown to prevent accidental spam clipping.

## Setup

### 1. Create a Twitch app
1. Go to https://dev.twitch.tv/console/apps
2. Register a new app (OAuth Redirect URL: `http://localhost`, Category: Other)
3. Copy your **Client ID** and generate a **Client Secret**

### 2. Get an OAuth token
Visit this URL in your browser (replace `YOUR_CLIENT_ID`):
```text
https://id.twitch.tv/oauth2/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost&response_type=token&scope=clips:edit
```
Copy the `access_token` from the redirect URL.

### 3. Set environment variables
```bash
export TWITCH_CLIENT_ID="your_client_id"
export TWITCH_ACCESS_TOKEN="your_access_token"
export TWITCH_BROADCASTER_ID="your_broadcaster_id"  # numeric user ID
```

To find your broadcaster ID:
```bash
curl -s -H "Authorization: Bearer $TWITCH_ACCESS_TOKEN" \
  -H "Client-Id: $TWITCH_CLIENT_ID" \
  https://api.twitch.tv/helix/users | python3 -c "import json,sys; print(json.load(sys.stdin)['data'][0]['id'])"
```

## Usage

Run the clip script:
```bash
bash scripts/create_clip.sh [duration_seconds]
```
- Duration defaults to 30, max 60
- Stream must be live or the API returns a 404

## Cooldown

A 30-second cooldown is enforced between clips. If a clip request comes in during cooldown:
- Script exits with code 2 and prints remaining wait time
- Reply: `⏳ Cooldown active — try again in Xs`
- Do NOT retry automatically — wait for the next explicit clip request

## Trigger phrases
- "clip that"
- "clip the last X seconds"
- "make a clip"
- "clip it"

## Response format

**Success:**
`Clipped! 🎬 https://clips.twitch.tv/<clip_id>`

**Cooldown active:**
`⏳ Cooldown active — try again in Xs`

**Not live:**
`Stream is offline — can't clip right now`

## Token refresh
Tokens expire. If you get a 401 error, re-authorize using the URL in Setup step 2.
