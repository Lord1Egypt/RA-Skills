---
name: text-to-published-podcast-rss
description: |
  Helps an agent or app to turn text into
  audio podcast episodes. One API call creates an episode using TTS and
  auto-publish to an RSS feed subscribable in
  any podcast app.
---

# Text to Published Podcast RSS - cast0 API

Text in, podcast episode out. The `text` field is read verbatim by TTS, not interpreted as a prompt. Episodes auto-publish to an RSS feed compatible with Apple Podcasts, Spotify, Overcast, and other podcast apps.

**Base URL:** `https://api.cast0.ai`
**Auth:** `Authorization: Bearer pk_xxxxx`
**Docs:** `https://api.cast0.ai/docs`

## Setup

Ask the user to create a podcast (= show) at `https://cast0.ai`. The dashboard is where the user can:

- Get the API key and RSS feed URL
- Change podcast settings (voice, TTS model, speed, name)

Each API key is tied to one podcast. Once you have the key, save it:

```bash
echo "CAST0_API_KEY=pk_xxxxx" >> .env
```

## Create an Episode

```bash
curl -X POST https://api.cast0.ai/api/episodes \
  -H "Authorization: Bearer pk_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"title": "Daily Standup", "text": "Here is what happened today..."}'
```

Returns `201` with the episode `id` and `"status": "queued"`.

## Poll for Completion

Generation is async: `queued` → `processing` → `done` | `failed`.

```bash
curl https://api.cast0.ai/api/episodes/EPISODE_ID \
  -H "Authorization: Bearer pk_xxxxx"
```

When `"done"`, the response includes `audioUrl` with the MP3 link.

## List Episodes

```bash
curl https://api.cast0.ai/api/episodes \
  -H "Authorization: Bearer pk_xxxxx"
```

## RSS Feed

Every podcast has a public feed URL (no auth):

```
https://api.cast0.ai/rss/FEED_TOKEN
```

Subscribe in any podcast app. New episodes appear automatically after generation.

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/episodes` | API key | Create episode (`{ title, text }`) |
| `GET` | `/api/episodes` | API key | List episodes |
| `GET` | `/api/episodes/:id` | API key | Get episode status |
| `GET` | `/rss/:feedToken` | None | RSS 2.0 feed |
