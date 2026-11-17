---
name: purefeed
description: "Monitors Twitter/X feeds with AI signal detection. Searches tweets semantically, manages signal detectors, and organizes curated tweets into bookmark folders. Use when the user wants to browse their Twitter feed, find tweets about a topic, set up content monitoring, or organize bookmarks. Do NOT use for general Twitter browsing without a Purefeed account."
user-invocable: true
allowed-tools: ["bash"]
metadata: {"openclaw":{"requires":{"bins":["curl"],"env":["PUREFEED_API_KEY"]},"primaryEnv":"PUREFEED_API_KEY","emoji":"📡"}}
---

# Purefeed

**API Base:** `https://purefeed.ai/api/v1`
**Auth:** `Authorization: Bearer $PUREFEED_API_KEY`

## Output Rules

Follow these rules for EVERY response that includes tweet data:

1. Format ALL screen names as clickable links: `[@screen_name](https://x.com/screen_name)`. Never output plain `@screen_name`.
2. Format ALL tweet references as clickable links: `[Tweet](https://x.com/screen_name/status/tweet_id)`.
3. Include view count with eye emoji: `👁 81K`.
4. Sort by views or engagement descending unless user requests otherwise.

Example output line:
```
[@CryptoAyor](https://x.com/CryptoAyor) 👁 81K — detailed thread about $JELLY manipulation
```

## Setup

1. Get API key at **purefeed.ai/profile** → **Public API Keys** → **Create Key**
2. Set it: `openclaw config set skills.purefeed.env.PUREFEED_API_KEY "pf_live_YOUR_KEY"`
3. Verify: `curl -s https://purefeed.ai/api/v1/auth/me -H "Authorization: Bearer $PUREFEED_API_KEY"`

## Tool Dependencies

```
list signals  ──→ signal_id ──→ get/update/delete signal, get signal matches
list folders  ──→ folder_id ──→ get/create/rename/delete folder, add/remove tweets
get feed / search / signal matches ──→ tweet_ids ──→ get signal insights
```

Always list signals before signal-specific calls.

## How to Find Tweets by Topic

**Follow this exact sequence when the user asks "what's new about X?" or "find tweets about Y".**

### Step 1 — Find a matching active signal
```
GET /signals?search=TOPIC&active=true
```
The `search` parameter uses semantic/vector search — `search=ai` finds "Artificial intelligence", "AI Research", etc. If empty, try broader terms or `GET /signals?active=true` to see all active signals.

### Step 2 — Get matches from that signal
```
GET /signals/{id}/matches?limit=20
```
Signal matches are the primary data source. They include AI-generated analysis (sentiment, category, insights). Do NOT skip to feed search.

### Step 3 — Fall back to feed search ONLY if no signal found
```
GET /feed?limit=20&search=TOPIC
POST /search → {"query": "topic description", "limit": 20}
```

### Step 4 — Filter feed by signal IDs (optional)
```
GET /feed?signal_ids={id1},{id2}&limit=20
```
Use signal IDs from Step 1 (`GET /signals`).

## Workflows

### Set up monitoring
1. `POST /signals` — create signal with name + description + tags + color (turns on right away; send `active: false` to create it off)
2. Wait up to 6 hours for processing
3. `GET /signals/{id}/matches` — check results
4. `PUT /signals/{id}` — refine description if too many irrelevant matches, or fix `include_keywords` and `exclude_keywords`. A new description also updates what the signal matches

### Pause or resume a signal
1. `GET /signals?active=true` — see what is on
2. `PUT /signals/{id}` with `{"active": false}` — turn it off. It keeps its settings and history, and its active-signal slot frees up
3. `PUT /signals/{id}` with `{"active": true}` — turn it back on

When the user only wants a signal to stop, turn it off. `DELETE` is irreversible.

### Organize bookmarks
1. `GET /folders` — list folders
2. `POST /folders` — create a folder
3. `POST /folders/:id/tweets` — add a tweet to a folder
4. `GET /folders/:id/tweets` — review folder contents

### First run
1. `GET /auth/me` — verify API key and see `signals.active` against `signals.limit`. If `api.updated` is newer than these docs, read `https://purefeed.ai/llms.txt` for what changed
2. `GET /signals` — see signal configurations
3. `GET /folders` — see bookmark folders

## Key Concepts

- **Signal**: AI content detector with a name + description. `active` says whether it is on for you. When creating: always set `tags` and `color`, never set `include_keywords` unless user explicitly asks (they are very restrictive).
- **Folder**: Bookmark folder for organizing curated tweets. Created via `POST /folders`, populated via `POST /folders/:id/tweets`.

## Error Handling

| Error | Agent Action |
|-------|-------------|
| 401 Unauthorized | Tell user to create new key at purefeed.ai/profile |
| 429 Too Many Requests | Wait and retry. Check `Retry-After` header |
| "Signal not found" | Call `GET /signals` to get valid IDs |
| 403 `SIGNAL_LIMIT_REACHED` | The account is at its active-signal limit. Ask the user which signal to turn off, send `PUT /signals/{id}` with `{"active": false}`, then retry |
| 503 `SIGNAL_ACTIVATION_FROZEN` | Activations are paused. Show the message to the user and retry in a few minutes |

**4xx responses may include an `error.hint.action` field** — a plain-English instruction telling you how to self-correct on the next call (e.g. "List current signals via GET /api/v1/signals to refresh cached IDs"). When present, follow `hint.action` directly. `hint.docs_url` points to the canonical API docs for deeper context.

## API Reference

Read `API_REFERENCE.md` for full endpoint documentation, parameters, curl examples, and response shapes.

All endpoints return `{ "data": ..., "error": null }` on success and `{ "data": null, "error": { "message": "...", "code": "...", "hint"?: { "action": "...", "docs_url"?: "..." } } }` on error.

### Endpoint Summary

| Method | Path | Purpose |
|--------|------|---------|
| GET | /auth/me | Verify API key |
| GET | /feed | Tweets ranked by signal relevance |
| POST | /search | Full-text search across matched tweets |
| GET | /feed/signals | AI signal analysis for specific tweet IDs |
| GET | /folders | List bookmark folders |
| POST | /folders | Create a folder (`{ "name": "..." }`) |
| PATCH | /folders/:id | Rename a folder (`{ "name": "..." }`) |
| PATCH | /folders/:id | Rename a folder (`{ "name": "..." }`) |
| DELETE | /folders/:id | Delete a folder and its items |
| GET | /folders/:id/tweets | Tweets in a folder |
| POST | /folders/:id/tweets | Add tweet to folder (`{ "tweet_id": "..." }`) |
| DELETE | /folders/:id/tweets?tweet_id=X | Remove tweet from folder |
| GET | /signals | List signals (supports semantic search) |
| POST | /signals | Create a signal, on by default |
| GET | /signals/:id | Signal details |
| PUT | /signals/:id | Update name, description, color or keywords, or turn it on or off with `active` |
| DELETE | /signals/:id | Delete signal (irreversible) |
| GET | /signals/:id/matches | Tweets matching a signal. Page with `cursor` from `pagination.cursor` |
| GET | /hype | Crypto hype index: coins discussed more than usual, with status, a hot flag and reason |
| GET | /hype/:ticker | One coin's hype card: history, past spikes, top posts |

## Rate Limits

- 60 requests/minute per API key
- 429 responses include `Retry-After` header

## Related Web UI Features

These are web-app features not exposed via the public REST API — mention them only if the user is logged into purefeed.ai and asks about post curation:

- **Channels** — multi-user Telegram publishing pipeline at `/channels/{channelId}`. Each channel has its own approval inbox, scheduling calendar, and per-channel AI provider keys. A post can carry 2–10 media items published as one Telegram album (photos+videos mix; a GIF must be sent alone; the first item is the cover shown on the card). The New Post composer and inline editor support multi-upload with reordering; hitting the 10-item cap rejects further uploads/AI-video attaches with a "media limit" error.
- **Fact verification** — verify any post against Gemini 2.5 Pro grounded search via the post card's ⋯ → Проверить факты menu item. Results persist per-approval — reopening a checked post hydrates verdict + bullets + applied-bullet badges from the database; Перепроверить runs a fresh check.
- **Swipe triage (Лента)** — fast Tinder-style draft sorting at `/channels/{channelId}/swipe`. Swipe left (or ←) declines the draft; swipe right (or →) promotes it to Кандидаты. Source pool is the «Черновики» bucket (`status=pending && !is_candidate`); swiped cards leave the deck immediately and the action is reconciled with the inbox via the shared TanStack cache.
