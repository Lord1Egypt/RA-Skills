# RedReplier API Reference

Base URL: `https://ai.redreplier.com/ai-app/api/v1`
Auth: `Authorization: Bearer <api-token>` header. Tokens start with the `redreplier_` prefix.

The workspace is derived from the token. No endpoint takes an account or group ID in the path, query, or body; you only ever pass resource IDs (website, keyword, mention). Every endpoint accepts an optional `X-Workspace-Id` header. An API token belongs to one workspace, so send that workspace's id or leave the header out. OAuth sign-ins that reach several workspaces pick one per call with it.

All resource IDs are UUIDs. Timestamps are ISO 8601 (UTC). Errors use the shape `{ "message": string | string[], "error": string, "statusCode": number }`. Some add a machine-readable `code`:

| Status | `code` | Meaning |
| --- | --- | --- |
| `401` | `token_issuer_lost_access` | The person who created the token was removed from the workspace or deactivated. Create a new token. |
| `403` | `subscription_required` | The plan does not include API access. Upgrade in the RedReplier app. |
| `403` | `workspace_access_denied` | `X-Workspace-Id` names a workspace this token cannot reach. The body also carries `workspaceId`. |

A `401` without a `code` means the token is missing, malformed, revoked, or for another product.

---

## Workspaces

### GET /workspaces

Lists the workspaces the caller can act in. An API token reaches only its own workspace, so the list has one entry; an OAuth sign-in lists every workspace its member belongs to.

```json
{
  "workspaces": [
    {
      "id": "22222222-2222-4222-8222-222222222222",
      "name": "Marketing",
      "organization": { "id": "org_...", "name": "Example Inc" },
      "role": { "key": "editor", "name": "Editor" },
      "permissions": ["redreplier.write", "..."],
      "isDefault": true,
      "current": true
    }
  ]
}
```

`current` marks the workspace this call landed in. Send an `id` as `X-Workspace-Id` to act in that workspace.

---

## Websites

### GET /websites

List all monitored websites for the account, each with its keywords and `ignoredKeywords`. Read-only: it changes no keyword status.

**Response:**

```json
{
  "websites": [
    {
      "id": "11111111-1111-4111-8111-111111111111",
      "accountGroupId": "22222222-2222-4222-8222-222222222222",
      "domain": "example.com",
      "url": "https://example.com",
      "name": "Example",
      "description": "Example is a developer tool for monitoring",
      "ignoredKeywords": ["hiring", "job post"],
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
  "keywords": ["example tool"],       // optional, added as PENDING
  "description": "..."                // optional: omit and the URL is scraped to write one
}
```

Returns the created website (same shape as GET). `description` is what every mention is scored against. Omit it and the server scrapes the URL to write one, spending one AI generation from the plan quota. If the scrape fails or the quota is exhausted the site is still created with `description: null` and new mentions get no `relevanceScore` (`relevanceReason` = "Scoring skipped: website description missing"), so check the response and set one with `PATCH` or `POST /websites/analyze-description`. Initial keywords are stored `PENDING`; `POST /websites/{id}/keywords`, `POST /keywords/activate-pending` or a freed slot promotes those that fit the plan for free. AI keyword suggestions are queued in the background and appear on the website later. Re-creating a domain that was soft-deleted revives the old record. Errors: `400` duplicate domain, `400` plan website limit reached.

### PATCH /websites/{id}

```json
{ "name": "New name", "description": "New description", "ignoredKeywords": ["hiring", "job post"] }
```

Every field optional; omitted fields keep their value, and an empty `description` clears it. The description is the AI scoring context; mentions already scored are not rescored. `ignoredKeywords` (string array, at most 100 entries of up to 255 characters each) replaces the whole ignore list: a mention whose title or text contains any entry leaves every mention list and count, and new matches are hidden as they arrive. Matching ignores case, blanks and duplicates are dropped, and `[]` clears the list; removing a word brings its mentions back. To add or remove one entry, read the current list from `GET /websites/{id}`, edit it and send all of it. The response returns `ignoredKeywords` lowercased. URL and keywords cannot be changed here. Returns the updated website with its keywords.

### DELETE /websites/{id}

Soft-deletes the website: it leaves `GET /websites` at once and its keywords stop matching. No restore endpoint; `POST /websites` with the same URL revives the record. Use `POST /keywords/{id}/disable` instead to pause a single keyword. Returns `{ "deleted": true }`.

### POST /websites/analyze-description

```json
{ "url": "https://example.com" }
```

Scrapes the URL and AI-generates a description without creating or changing any website. Returns `{ "description": "..." }`, ready to pass to `POST /websites` or `PATCH /websites/{id}`. Consumes one AI generation from the monthly quota unless a precomputed description already exists for the domain; the generation is refunded on failure. `400` when the quota is exhausted or the URL is invalid; an error when the page has too little readable text.

---

## Keywords

Keyword `status`: `PENDING` | `ACTIVE` | `DISABLED` | `SUSPENDED`.

### POST /websites/{id}/keywords

```json
{ "keywords": ["my product", "competitor"] }   // required, non-empty
```

Adds keywords: as many as fit the plan's free headroom become `ACTIVE` at once (no charge), and only the rest are `PENDING`. Values are trimmed, lowercased, and de-duplicated; ones already `ACTIVE` on the website are skipped, and a re-added `DISABLED` one counts as new (prefer `enable`). Unlimited. Keywords beyond the plan stay `PENDING` and match nothing until a slot frees up (disabling or deleting a keyword, or deleting a website, promotes pending keywords into it, and so does `activate-pending`) or the plan is upgraded in the RedReplier app. Returns the whole website with its updated keyword list, not only the new keywords.

### PATCH /keywords/{id}

```json
{ "value": "new keyword text" }
```

Renames a keyword in place (same ID) and re-grades it. Unlimited on every plan. An `ACTIVE` keyword stays `ACTIVE`; a `PENDING`, `DISABLED`, or `SUSPENDED` one goes `ACTIVE` if the plan has a free slot, else `PENDING`. A case-only change is a no-op; `400` if the value already exists on the website. Returns the keyword.

### POST /keywords/{id}/disable

Sets the keyword `DISABLED`; it stops matching immediately and frees its slot, which a `PENDING` keyword in the workspace takes at once. Its mentions are kept. Unlimited and reversible. Already-`DISABLED` keywords are returned unchanged. Returns the keyword.

### POST /keywords/{id}/enable

Re-activates one keyword. Goes `ACTIVE` at once if the plan has a free slot, otherwise it is set `PENDING`. Never charges: the user upgrades the plan in the RedReplier app, and `GET /keywords/billing-preview` shows what that would cost. An already `ACTIVE` keyword is returned unchanged. Use `activate-pending` to promote every `PENDING` keyword that fits instead. Returns the keyword.

### DELETE /keywords/{id}

Permanently deletes a keyword in any status **and every mention it produced**. No undo. Deleting an `ACTIVE` keyword frees its slot the same way disabling does, with no refund; disable instead to keep the mentions. Returns `{ "deleted": true }`.

### POST /keywords/activate-pending

Promotes `PENDING` keywords to `ACTIVE`, oldest first, up to the free slots on the current plan. Never charges: keywords beyond the plan stay `PENDING` until the plan is upgraded in the RedReplier app. Returns `{ "websites": [...] }`.

### GET /keywords/activate-pending/preview

Read-only price of the plan upgrade that would cover every `ACTIVE` keyword plus every `PENDING` one. No input needed and nothing changes. `isUpgrade: false` means the current plan already covers them. The API cannot perform the upgrade; the user does that in the RedReplier app.

### GET /keywords/billing-preview?desiredKeywordCount=N

Read-only price for a target number of active keywords (no change made, and the API cannot perform the upgrade). `desiredKeywordCount` is required and is the **absolute** total of active keywords wanted across the workspace, not the number being added. Use it for what-if pricing; use the activate-pending preview for the cost of covering what is already `PENDING`.

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
{ "limit": -1, "used": 0, "remaining": -1, "unlimited": true }
```

Monthly keyword-EDIT allowance (`limit` -1 = unlimited). Every current plan reports unlimited, so there is no need to check it before editing; the endpoint remains for clients that budget edits. Adding, disabling, and enabling were never metered.

---

## Mentions

### GET /mentions

Query parameters (all optional):

| Param | Values | Notes |
| --- | --- | --- |
| `websiteId` | UUID | Filter to one website |
| `statuses` | `NEW`,`APPROVED`,`REJECTED` | Repeat key for multiple |
| `scoreBuckets` | `VERY_LOW`,`LOW`,`MEDIUM`,`HIGH`,`VERY_HIGH` | Repeat key for multiple |
| `includeLowRelevance` | `true`/`false` | Default false: hides scores below the website minimum (30 by default) |
| `minScore` | 0-100 | Only mentions scoring at least this; leaves out unscored ones. Stacks on the website minimum |
| `keywords` | string | Repeat key for multiple |
| `sources` | `REDDIT_POST`,`REDDIT_COMMENT`,`TWITTER`,`BLUESKY`,`HACKERNEWS`,`FACEBOOK`,`FACEBOOK_GROUP` | Repeat key for multiple. `TWITTER` = X |
| `sort` | `RELEVANCE` (default), `RECENT` | |
| `from` / `to` | ISO 8601 | Ingestion-time window |
| `limit` | 1-500 (default 50) | |
| `offset` | ≥ 0 (default 0) | |

Defaults exclude `REJECTED` (unless `statuses` names it) and hide mentions below the website's minimum score (30 by default) unless `includeLowRelevance=true`. `scoreBuckets=LOW` on its own does not lift that cutoff. Unscored mentions (`relevanceScore: null`) are shown unless `minScore` is set.

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
      "aiReplySuggestion": "We built Example for exactly this...",
      "tags": ["lead", "question"],
      "publishedAt": "2026-05-29T18:33:31.954Z",
      "ingestedAt": "2026-05-29T19:33:31.955Z",
      "reviewedAt": null,
      "createdAt": "2026-05-29T21:33:31.955Z",
      "updatedAt": "2026-05-29T21:33:31.955Z"
    }
  ],
  "total": 3,
  "limit": 50,
  "offset": 0
}
```

`source` is one of `REDDIT_POST`, `REDDIT_COMMENT`, `TWITTER` (X), `BLUESKY`, `HACKERNEWS`, `FACEBOOK`, `FACEBOOK_GROUP`. `subreddit` holds the subreddit for Reddit sources and the group for `FACEBOOK_GROUP`; for other sources it is `null` (the `author` and `url` point to the originating platform, e.g. `https://news.ycombinator.com/item?id=...` for Hacker News).

Internal fields (raw payload, external ID, soft-delete marker) are never returned.

### GET /mentions/count

Same filters and defaults as `/mentions` (minus pagination/sort). Returns `{ "total": 3 }`. `/mentions` already returns `total`, so use this only when you do not need rows.

### PATCH /mentions/{id}/status

```json
{ "status": "APPROVED" }   // NEW | APPROVED | REJECTED
```

Fully reversible: any status can move to any other. Sets `reviewedAt` when moving out of `NEW` and clears it on `NEW`. `REJECTED` mentions drop out of default `/mentions` and `/mentions/count` results. Returns the updated mention.

### POST /mentions/{id}/explain

Generates whatever is missing among `relevanceReason`, `tags`, and `aiReplySuggestion`, stores it, and returns the full mention (later calls are instant reads). The website must have a `description`; without one the mention comes back unchanged. Returns `404` if the ID is unknown to this account. Generation is slow, so use it on a score that looks wrong rather than across a list.

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

`minIntervalMinutes` is the fastest cadence the current plan allows; `availableCadences` is the subset of `[15, 30, 60, 120, 180, 240, 720, 1440]` at/above that floor. `cadenceMinutes` is never reported below the floor, even if a faster value was saved before a plan downgrade.

### PUT /alert-settings

```json
{ "enabled": true, "cadenceMinutes": 240 }
```

`cadenceMinutes` (optional) must be one of `15, 30, 60, 120, 180, 240, 720, 1440` (else `400` "Invalid alert frequency for your plan") and is clamped UP to `minIntervalMinutes`. The PUT replaces both settings: omitting `cadenceMinutes` resets it to the fastest cadence the plan allows, so pass the current value when only toggling `enabled`. Returns the resolved settings (so the applied cadence may differ from the requested one on lower plans).

## Rate limits

600 requests per minute per API token, counted on a hash of the token rather than on IP.

Every response carries the RFC 9331 headers:

```
RateLimit-Policy: "redreplier-api";q=600;w=60
RateLimit-Limit: 600
RateLimit-Remaining: 587
RateLimit-Reset: 43
```

A `429` adds `Retry-After` in seconds. Wait it out rather than retrying immediately.

Paginating through mentions with `limit=500` is the usual reason an agent hits this. Filter harder instead of walking the whole list.

## GET /openapi.json

The full OpenAPI 3 spec, and the one endpoint that needs no authentication, so automation platforms can import it without a token.
