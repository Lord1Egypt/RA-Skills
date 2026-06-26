---
name: theshort-news
description: Real-time news intelligence from theshort.ai. Search topic- and tag-scoped news feeds, fetch article details with summaries, list available topics and tags. Use this skill whenever you need to ground a response in fresh, vetted news rather than the model's training data.
version: 0.1.0
author: TQDM Inc. <contact@tqdm.org>
tags: [news, search, current-events, grounding, rag, real-time, summaries]
license: MIT-0
---

# theshort-news (OpenClaw skill)

Read access to **theshort.ai**'s curated news index for any agent running on
OpenClaw. Authenticated by API key (`X-API-Key` header), billed in credits
against the developer account that owns the key. The skill exposes
topic-scoped search, tag-scoped search, full article details, and the topic /
tag catalogs the key has access to.

## When to use this skill

- The user is asking about something that happened recently and the model's
  built-in knowledge is likely stale.
- The user wants a one-line or one-paragraph summary of a news event.
- The agent needs to ground a longer answer in real, attributable sources
  with `canonicalUrl` links.
- The user is asking about trending stories in a given topic (politics,
  finance, tech, etc.) or geography (country / region).

Do **not** use this skill for opinion pieces, social media posts, or
fact-checking arbitrary user-supplied claims — the index is curated news
only.

## Authentication

Every request requires an `X-API-Key` header. Keys are issued from the
[OpenClaw dashboard](https://openclaw.theshort.ai/dashboard/keys). Each key
has its own topic + tag access scope, set when the key was created.

```http
X-API-Key: tsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Base URL

```
https://theshort.ai/api/external
```

## Credit costs

Every successful call deducts credits from the developer account's wallet.
Credits drain in this order: `PLAN_INCLUDED` → `PROMO` → `TOPUP`. If a call
fails server-side, credits are refunded automatically.

| Operation       | Endpoint              | Cost (credits) |
|-----------------|-----------------------|----------------|
| `topics_list`   | `GET /topics`         | 0              |
| `tags_list`     | `GET /tags`           | 0              |
| `news_search`   | `GET /news`           | 1              |
| `news_detail`   | `GET /news/{id}`      | 1              |
| `brief_generate`| (future)              | 3              |

If the wallet balance is insufficient the call returns HTTP `402 Payment
Required` with `{"error":"insufficient_credits", ...}`. Direct the user to
the [credits panel](https://openclaw.theshort.ai/dashboard/credits) to
top up or upgrade their plan.

## Endpoints

### `GET /health`

Liveness probe. Returns `{"status":"ok"}`. Free, unauthenticated, useful as
a connectivity check before issuing billable calls.

```bash
curl https://theshort.ai/api/external/health
```

### `GET /topics`

List the topic taxonomy this API key is allowed to query. Topics are
hierarchical (`tech`, `tech.ai`, `tech.cybersecurity`, …). Use the returned
keys verbatim in `GET /news?topic=...`.

```bash
curl -H "X-API-Key: $TSK" https://theshort.ai/api/external/topics
```

Response shape:

```json
[
  { "topicId": 12, "topicKey": "tech", "topicName": "Technology" },
  { "topicId": 18, "topicKey": "tech.ai", "topicName": "Artificial Intelligence" }
]
```

### `GET /tags`

List the tags this key has access to. Tags are flat labels (no hierarchy)
attached to news items by the editorial team. Use these for very narrow
filters that topics can't express.

```bash
curl -H "X-API-Key: $TSK" https://theshort.ai/api/external/tags
```

Response shape:

```json
[
  { "tagId": 7,  "tagName": "openai"        },
  { "tagId": 19, "tagName": "central-banks" }
]
```

### `GET /news`

The primary search endpoint. Returns the most recent news items the key has
access to, optionally filtered by topic and/or tag. Multiple filters of the
same kind are OR-ed; topic and tag filters are AND-ed.

Query params:

| Param   | Type            | Notes                                                                                                |
|---------|-----------------|------------------------------------------------------------------------------------------------------|
| `topic` | repeated string | Topic key from `/topics`. Repeat to OR.                                                              |
| `tag`   | repeated string | Tag name from `/tags`. Repeat to OR.                                                                 |
| `limit` | int (1–200)     | Max items to return. Default 50.                                                                     |
| `lang`  | `en` / `ru` / `az` | Language for the `summary` field. **Defaults to `en`** (English). When `ru` or `az` is requested, the `summary` field is populated with the Russian / Azerbaijani translation; if a translation is missing for a particular row the API transparently falls back to English so `summary` is never empty. |

```bash
curl -H "X-API-Key: $TSK" \
  "https://theshort.ai/api/external/news?topic=tech.ai&tag=openai&limit=10"

# Russian summaries
curl -H "X-API-Key: $TSK" \
  "https://theshort.ai/api/external/news?topic=tech.ai&lang=ru&limit=10"

# Azerbaijani summaries
curl -H "X-API-Key: $TSK" \
  "https://theshort.ai/api/external/news?topic=tech.ai&lang=az&limit=10"
```

Response shape:

```json
{
  "consumer": "acme-corp",
  "appliedTopics": ["tech.ai"],
  "appliedTags": ["openai"],
  "limit": 10,
  "items": [
    {
      "id": 12345,
      "summary": "OpenAI announced ...",
      "contentType": "news",
      "countryCode": "US",
      "sourceName": "Reuters",
      "canonicalUrl": "https://reuters.com/...",
      "publishedAt": "2026-04-11T08:30:00Z",
      "topics": ["tech", "tech.ai"],
      "tags": ["openai"]
    }
  ]
}
```

The response **only** contains a single `summary` field — there is **no
separate `title`**. The first sentence of `summary` is the headline; treat
the whole field as the article text. If you need both English and Russian
text for the same article, make two requests: one with `lang=en` (or no
`lang` at all) and another with `lang=ru`.

When grounding an answer for the user, **always** cite `canonicalUrl` so
they can verify the source.

### `GET /news/{id}`

Fetch a single news item by id. Useful when the user clicks through from a
search result. Returns the same `ExternalNewsItemDTO` shape as items in
`GET /news` — the same `lang` parameter applies.

Returns `404` if the item is outside the key's topic/tag scope, even if it
exists in the underlying database — this is a billable call regardless (the
key paid for the lookup).

```bash
curl -H "X-API-Key: $TSK" https://theshort.ai/api/external/news/12345
curl -H "X-API-Key: $TSK" "https://theshort.ai/api/external/news/12345?lang=ru"
```

## Error handling

All errors come back as JSON with an `error` field and a human-readable
`message`. The HTTP status indicates the category:

| Status | Meaning                                      | Action                                  |
|--------|----------------------------------------------|-----------------------------------------|
| `401`  | Missing or invalid `X-API-Key`               | Stop. Ask the user to provide a key.    |
| `402`  | Insufficient credits in the developer wallet | Direct to credits panel.                |
| `403`  | Topic/tag is outside this key's scope        | Pick a different filter.                |
| `404`  | News item not found                          | Try `GET /news` to discover valid ids.  |
| `429`  | Rate-limited (per-key quota)                 | Back off and retry.                     |
| `5xx`  | Server error — credits are auto-refunded     | Retry with exponential backoff.         |

## Recommended workflow

1. **Discover scope** — call `GET /topics` and `GET /tags` once at agent
   startup (these are free) and cache the results for the session.
2. **Search** — call `GET /news` with the user's topic of interest. Apply
   `limit=10` for chat replies, larger for batch jobs.
3. **Drill down** — when the user asks "tell me more about story X", call
   `GET /news/{id}` for the full payload.
4. **Cite** — when summarizing, always include the `canonicalUrl` and
   `sourceName` so the user can verify.
5. **Watch the wallet** — surface the response from `GET
   /api/v1/me/billing` (admin / dashboard) when the user asks "how many
   credits do I have left".

## Example conversation

> **User:** "What's happening with OpenAI today?"
>
> **Agent (internal):**
> 1. `GET /news?topic=tech.ai&tag=openai&limit=5`
> 2. Pick the top 3 by `publishedAt`.
> 3. For the most relevant: `GET /news/{id}` to grab the full summary.
>
> **Agent (reply):** "Three things in the past 24 hours: …. _Sources:
> Reuters, TechCrunch, The Verge_."

## Plans and pricing

| Plan     | Monthly credits | Price       |
|----------|-----------------|-------------|
| FREE     | 100 (one-time)  | $0          |
| PRO      | 10,000          | $29 / month |
| SCALE    | 50,000          | $119 / month|

Top-up packs (one-time): `TOPUP_1K` (1000 credits, $10), `TOPUP_5K` (5000,
$45), `TOPUP_20K` (20,000, $160). All purchases and plan changes happen
through the [credits panel](https://openclaw.theshort.ai/dashboard/credits).

## Support

- **Dashboard:** https://openclaw.theshort.ai
- **Issues:** contact@tqdm.org
