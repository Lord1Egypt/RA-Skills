---
name: redreplier
description: Monitor Reddit, Hacker News, X, and Bluesky for keyword mentions of a product or website using the RedReplier API. Use when the user wants to track mentions of their brand across Reddit, Hacker News, X (Twitter), or Bluesky, find leads from social discussions, manage monitored websites and keywords, triage AI-scored mention relevance, approve/reject leads, or configure mention email alerts. RedReplier is a SaaS tool — no self-hosting required.
homepage: https://redreplier.com
metadata: { 'openclaw': { 'emoji': '🛰️', 'primaryEnv': 'REDREPLIER_API_KEY', 'requires': { 'env': ['REDREPLIER_API_KEY'] } } }
---

# RedReplier

Monitor Reddit, Hacker News, X, and Bluesky for keyword mentions of your product, AI-scored 0-100 for relevance so you act on real leads instead of noise. SaaS — no self-hosting needed.

## Setup

1. Sign up at https://redreplier.com/signup
2. Go to Settings → API Tokens → generate a **dedicated, revocable** API token for this agent — do not reuse a token also used by other tools or humans.
3. Set the environment variable:
   ```bash
   export REDREPLIER_API_KEY="redreplier_your-token-here"
   ```

Base URL: `https://ai.redreplier.com/ai-app/api/v1`
Auth header: `Authorization: Bearer $REDREPLIER_API_KEY`

The account is determined by the token — you never pass an account or group ID.

## Safety rules — read before any write call

Most RedReplier operations are safe and reversible (listing mentions, approving/rejecting). Two classes of action are **not** and need explicit confirmation:

1. **Billing — `POST /keywords/activate-pending`.** Activating pending keywords promotes everything that fits the plan for free, then **charges a real plan upgrade** to cover the rest. Always call `GET /keywords/activate-pending/preview` first, show the user the `immediateCharge` / `targetPlanName`, and get an explicit "yes" before activating. Never activate in a loop.
2. **Deletion — `DELETE /websites/{id}`.** This stops all monitoring for the website. Confirm with the user first; name the website (domain), not just the ID.

Other guidance:

- **Keyword edits are metered.** `PATCH /keywords/{id}` counts against a monthly edit allowance (`GET /keywords/change-usage`). Adding and disabling are unlimited — prefer those. Don't spend edits on cosmetic changes.
- **Don't fight the grader.** A `SUSPENDED` keyword was auto-judged too noisy. Fix the wording with an edit; don't try to force it back to ACTIVE.
- **Triage, don't fabricate.** When approving/rejecting mentions, act on the AI `relevanceScore`/`relevanceReason` and the actual content — don't invent leads.

## Core Workflow

### 1. List monitored websites (and their keywords)

```bash
curl -s -H "Authorization: Bearer $REDREPLIER_API_KEY" \
  https://ai.redreplier.com/ai-app/api/v1/websites
```

Returns `{ "websites": [{ "id", "domain", "url", "name", "description", "keywords": [{ "id", "value", "status" }] }] }`. Keyword `status` is one of `PENDING`, `ACTIVE`, `DISABLED`, `SUSPENDED`. Save website IDs and keyword IDs — you need them everywhere else.

### 2. Add a website to monitor

Omit `description` to let RedReplier scrape the site and AI-generate one (used as context for relevance scoring). Initial `keywords` are added as `PENDING`.

```bash
curl -X POST https://ai.redreplier.com/ai-app/api/v1/websites \
  -H "Authorization: Bearer $REDREPLIER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "name": "Example",
    "keywords": ["example tool", "competitor name"]
  }'
```

To preview an AI description without creating anything:

```bash
curl -X POST https://ai.redreplier.com/ai-app/api/v1/websites/analyze-description \
  -H "Authorization: Bearer $REDREPLIER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "url": "https://example.com" }'
```

### 3. Add keywords (and activate within plan)

Adding keywords auto-activates as many as fit the plan for free; the rest stay `PENDING`.

```bash
curl -X POST https://ai.redreplier.com/ai-app/api/v1/websites/WEBSITE_ID/keywords \
  -H "Authorization: Bearer $REDREPLIER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "keywords": ["my product", "use case phrase"] }'
```

Preview what activating the remaining pending keywords would cost, **then** activate (paid upgrade possible — confirm first):

```bash
curl -s -H "Authorization: Bearer $REDREPLIER_API_KEY" \
  https://ai.redreplier.com/ai-app/api/v1/keywords/activate-pending/preview

curl -X POST https://ai.redreplier.com/ai-app/api/v1/keywords/activate-pending \
  -H "Authorization: Bearer $REDREPLIER_API_KEY"
```

Other keyword actions: `PATCH /keywords/{id}` `{ "value": "new" }` (edit, metered), `POST /keywords/{id}/disable`, `POST /keywords/{id}/enable`, `DELETE /keywords/{id}` (PENDING only).

### 4. List mentions (the leads)

```bash
curl -s -H "Authorization: Bearer $REDREPLIER_API_KEY" \
  "https://ai.redreplier.com/ai-app/api/v1/mentions?sort=RELEVANCE&limit=20"
```

Returns `{ "mentions": [...], "total", "limit", "offset" }`. Each mention has `relevanceScore` (0-100), `relevanceReason`, `tags`, `keyword`, `title`, `contentText`, `url`, `author`, `subreddit`, `source`, `status`. `source` is one of `REDDIT_POST`, `REDDIT_COMMENT`, `TWITTER` (X), `BLUESKY`, `HACKERNEWS`; `subreddit` is populated only for Reddit sources (null for X, Bluesky, and Hacker News).

**Defaults**: `REJECTED` mentions are excluded and anything scoring below 30 is hidden. Add `&includeLowRelevance=true` to see everything.

Useful filters (combine freely): `websiteId`, `statuses` (NEW/APPROVED/REJECTED), `scoreBuckets` (VERY_LOW/LOW/MEDIUM/HIGH/VERY_HIGH), `keywords`, `sources` (REDDIT_POST/REDDIT_COMMENT/TWITTER/BLUESKY/HACKERNEWS), `sort` (RELEVANCE/RECENT), `from`/`to` (ISO 8601 ingestion window), `limit` (1-500), `offset`. Repeat a key for arrays: `?statuses=NEW&statuses=APPROVED`. See [references/mention-filtering.md](references/mention-filtering.md).

```bash
# This week's high-relevance, unreviewed leads for one site
curl -s -H "Authorization: Bearer $REDREPLIER_API_KEY" \
  "https://ai.redreplier.com/ai-app/api/v1/mentions?websiteId=WEBSITE_ID&statuses=NEW&scoreBuckets=HIGH&scoreBuckets=VERY_HIGH&sort=RECENT"
```

Count only:

```bash
curl -s -H "Authorization: Bearer $REDREPLIER_API_KEY" \
  "https://ai.redreplier.com/ai-app/api/v1/mentions/count?statuses=NEW"
```

### 5. Understand why a mention scored the way it did

```bash
curl -X POST https://ai.redreplier.com/ai-app/api/v1/mentions/MENTION_ID/explain \
  -H "Authorization: Bearer $REDREPLIER_API_KEY"
```

Returns the mention with `relevanceReason` and `tags` (lazily generated if missing).

### 6. Triage a mention (approve / reject / reset)

```bash
curl -X PATCH https://ai.redreplier.com/ai-app/api/v1/mentions/MENTION_ID/status \
  -H "Authorization: Bearer $REDREPLIER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "status": "APPROVED" }'
```

`APPROVED` = real lead, `REJECTED` = noise (hidden from default lists), `NEW` = back to inbox. Reversible.

### 7. Email alerts

```bash
# Read current settings (includes plan's fastest allowed cadence)
curl -s -H "Authorization: Bearer $REDREPLIER_API_KEY" \
  https://ai.redreplier.com/ai-app/api/v1/alert-settings

# Enable a 4-hour digest
curl -X PUT https://ai.redreplier.com/ai-app/api/v1/alert-settings \
  -H "Authorization: Bearer $REDREPLIER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "enabled": true, "cadenceMinutes": 240 }'
```

`cadenceMinutes` must be one of `60`, `240`, `720`, `1440`, and is clamped up to the plan's `minIntervalMinutes`. Returns the resolved settings (so you can confirm the cadence actually applied).

## Keyword Lifecycle Cheat Sheet

| Status | Meaning | What you can do |
| --- | --- | --- |
| `PENDING` | Proposed, not yet live/paid | Activate (may upgrade), delete |
| `ACTIVE` | Live, monitoring all channels | Disable, edit |
| `DISABLED` | Stopped | Enable (may need upgrade), edit |
| `SUSPENDED` | Auto-rejected as too noisy | Edit to fix (free re-grade) |

## Relevance Buckets

| Bucket | Score | Typical meaning |
| --- | --- | --- |
| `VERY_HIGH` | 75-100 | Strong buying intent / direct fit — review first |
| `HIGH` | 50-74 | Relevant discussion worth engaging |
| `MEDIUM` | 30-49 | Loosely related |
| `LOW` | 10-29 | Tangential (hidden by default) |
| `VERY_LOW` | 0-9 | Noise (hidden by default) |

## Tips for the Agent

- **Always list `/websites` first** to get website + keyword IDs; nothing else takes an account parameter.
- **Lead-first triage**: pull `scoreBuckets=HIGH&scoreBuckets=VERY_HIGH&statuses=NEW`, summarize each with its `source` (and `subreddit` for Reddit), `relevanceScore`, and a one-line `relevanceReason`, then ask the user which to approve.
- **Confirm before money or deletion** (activate-pending upgrades, website deletion). Everything else is safe.
- **Prefer disabling over deleting** keywords — only `PENDING` keywords can be deleted anyway.
- **Use `RECENT` sort** for "what's new since yesterday", default `RELEVANCE` for "best leads".
- **Watch `includeLowRelevance`** — leave it off unless the user explicitly wants the long tail; it floods results with noise.
- For full request/response shapes, see [references/api-reference.md](references/api-reference.md).
