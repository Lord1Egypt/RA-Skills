---
name: publer-api
description: >
  Use this skill whenever the user wants to interact with the Publer API — including
  managing social media posts (create, schedule, update, delete, approve), browsing or
  uploading media, viewing workspaces and connected social accounts, or retrieving
  analytics. Trigger this skill any time the user mentions Publer, wants to schedule
  or manage posts across social platforms via Publer, asks about Publer analytics or
  insights, needs to work with the Publer media library, or wants to analyze competitors
  or hashtag performance via Publer. Also trigger when the user asks to automate social
  media workflows that involve Publer, even if they don't explicitly say "Publer API".
---

# Publer API Skill

This skill enables you to interact with all Publer API endpoints.

**Business plan required.** The Publer API is only available to Business plan users.

## Setup

**Base URL:** `https://app.publer.com/api/v1`

**Required headers on almost every request:**
```
Authorization: Bearer-API YOUR_API_KEY
Publer-Workspace-Id: YOUR_WORKSPACE_ID
Content-Type: application/json
```

Note: `Bearer-API` (not `Bearer`) is the correct format.

If the user hasn't provided their API key, ask for it before making any calls. Never hardcode or expose API keys.

**API key scopes:** `workspaces`, `accounts`, `posts`, `media`, `analytics`

---

## Quick Reference: All Endpoints

| Area | Method | Endpoint |
|---|---|---|
| Users | GET | `/users/me` |
| Workspaces | GET | `/workspaces` |
| Accounts | GET | `/accounts` |
| Posts | GET | `/posts` |
| Posts — Schedule/Draft | POST | `/posts/schedule` |
| Posts — Publish Now | POST | `/posts/schedule/publish` |
| Posts — Update | PUT | `/posts/{id}` |
| Posts — Delete | DELETE | `/posts` |
| Job Status | GET | `/job_status/{job_id}` |
| Media — List | GET | `/media` |
| Media — Direct Upload | POST | `/media` |
| Media — URL Upload | POST | `/media/from-url` |
| Media Options | GET | `/workspaces/{workspace_id}/media_options` |
| Analytics — Charts List | GET | `/analytics/charts` |
| Analytics — Chart Data | GET | `/analytics/:account_id/chart_data` |
| Analytics — Post Insights | GET | `/analytics/:account_id/post_insights` |
| Analytics — Hashtag Insights | GET | `/analytics/:account_id/hashtag_insights` |
| Analytics — Hashtag Posts | GET | `/analytics/:account_id/hashtag_performing_posts` |
| Analytics — Best Times | GET | `/analytics/:account_id/best_times` |
| Analytics — Members | GET | `/analytics/members` |
| Competitors — List | GET | `/competitors/:account_id` |
| Competitors — Analytics | GET | `/competitors/:account_id/analytics` |

For full request/response shapes, read `references/api-reference.md`.

---

## Workflow

### 1. Identify the intent
Map the user's request to one or more API calls from the table above.

### 2. Gather required parameters
- **Workspace ID:** Needed for most calls. If unknown, call `GET /workspaces` first.
- **Account IDs:** Needed for post creation. If unknown, call `GET /accounts`.
- **Scheduled posts:** `scheduled_at` must be ISO 8601 with timezone, at least 1 minute in the future.
- **Analytics:** Most endpoints need `from`/`to` date range (YYYY-MM-DD). They are co-required.
- **Media:** Must be uploaded first via `/media` or `/media/from-url`, then referenced by ID in posts.

### 3. Make the API call
Use the correct HTTP method and headers. POST/PUT use `Content-Type: application/json`. Media direct upload uses `multipart/form-data`.

### 4. Handle async operations
Post creation and URL media uploads are **asynchronous**:
- Response returns `{ "success": true, "data": { "job_id": "..." } }`
- Poll `GET /job_status/{job_id}` until `status` is `"complete"` or `"failed"`
- Check `payload.failures` even on `"complete"` — partial failures are possible

### 5. Interpret the response
- **2xx** — success. Parse and present relevant fields clearly.
- **401** — ask user to verify API key and confirm `Bearer-API` format.
- **403** — check required scope is enabled, and `Publer-Workspace-Id` header is present.
- **404** — resource ID is wrong; confirm with user.
- **422** — surface the `errors[]` array to user and ask them to correct input.
- **429** — rate limited (100 req/2 min); wait for `X-RateLimit-Reset`, use exponential backoff.
- **5xx** — Publer server error; suggest retry.

---

## Common Workflows

### Schedule a post
1. If workspace/account IDs unknown: `GET /workspaces` then `GET /accounts`
2. `POST /posts/schedule` with `state: "scheduled"`, network content, and `scheduled_at` per account
3. Poll `GET /job_status/{job_id}` until complete
4. Confirm back: platform(s), scheduled time, text preview

### Publish immediately
Same as above but use `POST /posts/schedule/publish` and omit `scheduled_at`.

### Cross-post with platform-specific content
Use multiple keys under `networks` with per-platform text/type:
```json
"networks": {
  "facebook": { "type": "status", "text": "Longer Facebook copy..." },
  "twitter": { "type": "status", "text": "Short tweet #hashtag" },
  "linkedin": { "type": "status", "text": "Professional LinkedIn copy..." }
}
```

### Upload and attach media
1. `POST /media` (multipart) for direct upload, or `POST /media/from-url` for URL import
2. Check `validity` object in response for network compatibility
3. Reference `media.id` in the `media[]` array inside the network object when creating post

### List and review scheduled posts
1. `GET /posts?state=scheduled`
2. Display as readable list: date, network, text preview
3. Offer to edit (`PUT /posts/{id}`) or delete (`DELETE /posts?post_ids[]=...`) on request

### Fetch analytics
1. For account-level charts: `GET /analytics/charts` to get available IDs, then `GET /analytics/:account_id/chart_data?chart_ids[]=...&from=...&to=...`
2. For per-post performance: `GET /analytics/:account_id/post_insights?from=...&to=...`
3. For hashtag performance: `GET /analytics/:account_id/hashtag_insights`
4. For best posting times: `GET /analytics/:account_id/best_times?from=...&to=...`

### Competitor analysis
1. `GET /competitors/:account_id` to list competitors
2. `GET /competitors/:account_id/analytics` for aggregate metrics
3. Use `competitors=true&competitor_id=...` on post insights and best times endpoints for deeper comparison

---

## Key Notes & Edge Cases

- **Auth header format:** `Bearer-API YOUR_KEY` — not `Bearer`
- **Workspace in header vs path:** Most endpoints use `Publer-Workspace-Id` header. Exception: `GET /workspaces/{workspace_id}/media_options` uses workspace ID in the path.
- **`/users/me` and `/workspaces`** do not require the workspace header.
- **Pagination:** 0-based `page` param throughout. Post insights and hashtag insights return 10 per page.
- **Date format:** ISO 8601 with timezone for timestamps; YYYY-MM-DD for analytics date ranges.
- **`default` network key:** Use `"default"` as the network to apply same content to all accounts.
- **Threads:** Cannot schedule for specific times via API.
- **Analytics data freshness:** Metrics auto-sync ~every 24h. Not real-time.
- **Competitor `sort_type`:** Lowercase `asc`/`desc` — unlike post/hashtag insights which use `ASC`/`DESC`.
- **`reach` field:** May be omitted in members analytics and competitor analytics for unsupported networks — handle gracefully.

---

## Reference Files

- `references/api-reference.md` — Full endpoint docs with all request/response shapes, field enums, media specs, daily post limits, and error handling. Read this when you need exact field names, response shapes, or need to handle a case not covered above.
