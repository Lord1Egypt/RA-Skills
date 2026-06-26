# RedReplier API Reference

Base URL: `https://ai.redreplier.com/ai-app/api/v1`
Auth: `Authorization: Bearer <api-token>` header. Tokens start with the `redreplier_` prefix.

The authenticated account (account group) is derived from the token. No endpoint takes an account or group ID — you only ever pass resource IDs (website, keyword, mention).

All resource IDs are UUIDs. Timestamps are ISO 8601 (UTC). Errors use the shape `{ "message": string | string[], "error": string, "statusCode": number }`.

---

## Websites

### GET /websites

List all monitored websites for the account, each with its keywords.

**Response:**

```json
{
  "websites": [
    {
      "id": "11111111-1111-4111-8111-111111111111",
      "accountGroupId": "grp_...",
      "domain": "example.com",
      "url": "https://example.com",
      "name": "Example",
      "description": "Example is a developer tool for monitoring",
      "createdAt": "2026-05-27T21:31:47.189Z",
      "updatedAt": "2026-05-29T21:31:47.189Z",
      "keywords": [
        { "id": "33333331-...", "websiteId": "1111...", "value": "example tool", "status": "ACTIVE", "createdAt": "...", "updatedAt": "..." }
      ]
    }
  ]
}
```

### GET /websites/{id}

Get a single website (with keywords). `404` if not found / not owned, `400` if `id` is not a valid UUID.

### POST /websites

Create a monitored website.

```json
{
  "url": "https://example.com",      // required
  "name": "Example",                  // optional
  "keywords": ["example tool"],       // optional — added as PENDING
  "description": "..."                // optional — omit to scrape + AI-generate
}
```

Returns the created website (same shape as GET). The first website for an account also seeds keywords from the shared feed. Errors: `400` duplicate domain, `400` plan website limit reached (requires an active subscription).

### PATCH /websites/{id}

```json
{ "name": "New name", "description": "New description" }
```

Both fields optional. Returns the updated website.

### DELETE /websites/{id}

Soft-deletes the website (stops monitoring). Returns `{ "deleted": true }`.

### POST /websites/analyze-description

```json
{ "url": "https://example.com" }
```

Scrapes the URL and AI-generates a description. Returns `{ "description": "..." }`. Consumes AI quota.

---

## Keywords

Keyword `status`: `PENDING` | `ACTIVE` | `DISABLED` | `SUSPENDED`.

### POST /websites/{id}/keywords

```json
{ "keywords": ["my product", "competitor"] }   // required, non-empty
```

Adds keywords as PENDING, then auto-activates as many as fit the current plan. Returns the website with its updated keyword list.

### PATCH /keywords/{id}

```json
{ "value": "new keyword text" }
```

Renames a keyword; it is re-graded. Counts against the monthly edit allowance unless the keyword was `SUSPENDED` (free fix). Returns the keyword.

### POST /keywords/{id}/disable

Sets the keyword `DISABLED`. Unlimited. Returns the keyword.

### POST /keywords/{id}/enable

Re-activates a keyword. Goes `ACTIVE` if it fits the plan, otherwise `PENDING` and an upgrade is required (`400` "active subscription required" on free plan). Returns the keyword.

### DELETE /keywords/{id}

Deletes a keyword. **Only `PENDING` keywords can be deleted** — otherwise `400` "Only pending keywords can be removed". Returns `{ "deleted": true }`.

### POST /keywords/activate-pending

Activates pending keywords: promotes everything that fits the plan for free, then **charges a plan upgrade** to cover the remainder. Returns `{ "websites": [...] }`. May return `400` if the user has no payment customer / cannot be charged. Call the preview first.

### GET /keywords/activate-pending/preview

Returns the billing preview for activating all currently pending keywords (no change made).

### GET /keywords/billing-preview?desiredKeywordCount=N

Billing preview for a target number of active keywords. `desiredKeywordCount` is required.

**Preview response shape (both billing-preview endpoints):**

```json
{
  "currentPlanName": null,
  "currentMonthlyPrice": 0,
  "targetPlanName": "10 Keywords",
  "targetMonthlyPrice": 10,
  "targetKeywords": 10,
  "immediateCharge": 0,
  "isUpgrade": true,
  "isDowngrade": false,
  "requiresImmediatePayment": true
}
```

### GET /keywords/change-usage

```json
{ "limit": 6, "used": 0, "remaining": 6, "unlimited": false }
```

Monthly keyword-EDIT allowance (`limit` -1 = unlimited). Adding and disabling keywords are unlimited.

---

## Mentions

### GET /mentions

Query parameters (all optional):

| Param | Values | Notes |
| --- | --- | --- |
| `websiteId` | UUID | Filter to one website |
| `statuses` | `NEW`,`APPROVED`,`REJECTED` | Repeat key for multiple |
| `scoreBuckets` | `VERY_LOW`,`LOW`,`MEDIUM`,`HIGH`,`VERY_HIGH` | Repeat key for multiple |
| `includeLowRelevance` | `true`/`false` | Default false — hides score < 30 |
| `keywords` | string | Repeat key for multiple |
| `sources` | `REDDIT_POST`,`REDDIT_COMMENT`,`TWITTER`,`BLUESKY`,`HACKERNEWS` | Repeat key for multiple. `TWITTER` = X |
| `sort` | `RELEVANCE` (default), `RECENT` | |
| `from` / `to` | ISO 8601 | Ingestion-time window |
| `limit` | 1-500 (default 50) | |
| `offset` | ≥ 0 (default 0) | |

Defaults exclude `REJECTED` and hide mentions scoring below 30 unless `includeLowRelevance=true`.

**Response:**

```json
{
  "mentions": [
    {
      "id": "44444441-...",
      "websiteId": "11111111-...",
      "source": "REDDIT_POST",
      "keyword": "example tool",
      "title": "Looking for an example tool",
      "contentText": "Anyone know a good example tool for monitoring?",
      "url": "https://reddit.com/r/webdev/1",
      "author": "alice",
      "subreddit": "webdev",
      "status": "NEW",
      "relevanceScore": 85,
      "relevanceReason": "Strong match: asks for exactly this kind of tool",
      "tags": ["lead", "question"],
      "publishedAt": "2026-05-29T18:33:31.954Z",
      "ingestedAt": "2026-05-29T19:33:31.955Z",
      "reviewedAt": null,
      "createdAt": "2026-05-29T21:33:31.955Z"
    }
  ],
  "total": 3,
  "limit": 50,
  "offset": 0
}
```

`source` is one of `REDDIT_POST`, `REDDIT_COMMENT`, `TWITTER` (X), `BLUESKY`, `HACKERNEWS`. `subreddit` is populated only for Reddit sources; for X, Bluesky, and Hacker News mentions it is `null` (the `author` and `url` point to the originating platform — e.g. `https://news.ycombinator.com/item?id=...` for Hacker News).

Internal fields (raw payload, external ID, soft-delete marker) are never returned.

### GET /mentions/count

Same filters as `/mentions` (minus pagination/sort). Returns `{ "total": 3 }`.

### PATCH /mentions/{id}/status

```json
{ "status": "APPROVED" }   // NEW | APPROVED | REJECTED
```

Sets `reviewedAt` when moving out of `NEW`. Returns the updated mention.

### POST /mentions/{id}/explain

Lazily generates (if missing) and returns the mention's `relevanceReason` and `tags`. Returns the mention object, or `null` if it can't be resolved.

---

## Alert Settings

### GET /alert-settings

```json
{
  "enabled": false,
  "cadenceMinutes": 720,
  "minIntervalMinutes": 720,
  "availableCadences": [720, 1440]
}
```

`minIntervalMinutes` is the fastest cadence the current plan allows; `availableCadences` is the subset of `[60, 240, 720, 1440]` at/above that floor.

### PUT /alert-settings

```json
{ "enabled": true, "cadenceMinutes": 240 }
```

`cadenceMinutes` (optional) must be one of `60, 240, 720, 1440` and is clamped UP to `minIntervalMinutes`. Returns the resolved settings (so the applied cadence may differ from the requested one on lower plans).
