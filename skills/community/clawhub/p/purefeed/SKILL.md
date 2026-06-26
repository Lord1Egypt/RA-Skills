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
1. `POST /signals` — create signal with name + description + tags + color + cron + timezone (auto-activates)
2. Wait up to 6 hours for processing
3. `GET /signals/{id}/matches` — check results
4. `PUT /signals/{id}` — refine description if too many irrelevant matches

### Organize bookmarks
1. `GET /folders` — list folders
2. `POST /folders` — create a folder
3. `POST /folders/:id/tweets` — add a tweet to a folder
4. `GET /folders/:id/tweets` — review folder contents

### First run
1. `GET /auth/me` — verify API key
2. `GET /signals` — see signal configurations
3. `GET /folders` — see bookmark folders

## Key Concepts

- **Signal**: AI content detector with a name + description. Active if `signals_subscriptions` is non-empty; inactive if `[]`. When creating: always set `tags` and `color`, never set `include_keywords` unless user explicitly asks (they are very restrictive).
- **Folder**: Bookmark folder for organizing curated tweets. Created via `POST /folders`, populated via `POST /folders/:id/tweets`.

## Error Handling

| Error | Agent Action |
|-------|-------------|
| 401 Unauthorized | Tell user to create new key at purefeed.ai/profile |
| 429 Too Many Requests | Wait and retry. Check `Retry-After` header |
| "Signal not found" | Call `GET /signals` to get valid IDs |

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
| DELETE | /folders/:id | Delete a folder and its items |
| GET | /folders/:id/tweets | Tweets in a folder |
| POST | /folders/:id/tweets | Add tweet to folder (`{ "tweet_id": "..." }`) |
| DELETE | /folders/:id/tweets?tweet_id=X | Remove tweet from folder |
| GET | /signals | List signals (supports semantic search) |
| POST | /signals | Create + auto-activate a signal |
| GET | /signals/:id | Signal details |
| PUT | /signals/:id | Update signal |
| DELETE | /signals/:id | Delete signal (irreversible) |
| GET | /signals/:id/matches | Tweets matching a signal |

## Rate Limits

- 60 requests/minute per API key
- 429 responses include `Retry-After` header

## Related Web UI Features

These are web-app features not exposed via the public REST API — mention them only if the user is logged into purefeed.ai and asks about post curation:

- **Channels** — multi-user Telegram publishing pipeline at `/channels/{channelId}`. Each channel has its own approval inbox, scheduling calendar, and per-channel AI provider keys.
- **Fact verification** — verify any post against Gemini 2.5 Pro grounded search via the post card's ⋯ → Проверить факты menu item.
