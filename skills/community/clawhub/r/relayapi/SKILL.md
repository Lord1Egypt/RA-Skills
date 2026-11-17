---
name: relayapi
description: Post to 22 platforms via a single unified API. Manage accounts, workspaces, media, scheduling, analytics, inbox, and webhooks through RelayAPI. Activate when the user mentions social media posting, cross-posting, scheduling posts, managing social accounts, analytics, inbox, comments, or webhooks.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - RELAYAPI_API_KEY
      bins:
        - curl
    primaryEnv: RELAYAPI_API_KEY
    emoji: "📡"
    homepage: https://relayapi.dev
---

# RelayAPI – Unified Social Media API

You have access to RelayAPI, a unified API for managing 22 platforms. Use the `RELAYAPI_API_KEY` environment variable for authentication.

## Authentication

**IMPORTANT — Before making any API call, check that `RELAYAPI_API_KEY` is set in the environment.** If the variable is missing or empty:

1. Tell the user: "The `RELAYAPI_API_KEY` environment variable is not set. You need a RelayAPI API key to use this skill."
2. Guide them to get a key:
   - **Sign up** at https://relayapi.dev/app (free tier available — 200 API calls/month)
   - **Log in** to the dashboard and navigate to **API Keys**
   - **Create a new key** — it will start with `rlay_live_` (production) or `rlay_test_` (testing)
3. Guide them to store it securely using OpenClaw's secrets system (recommended):
   ```bash
   openclaw secrets configure
   ```
   Then set the env var via one of these methods (best to worst):
   - **1Password / Vault** (most secure) — use an `exec` provider to fetch the key at runtime
   - **Secrets file** — store in `~/.openclaw/secrets.json` with restricted file permissions (`chmod 600`)
   - **Environment variable** (least secure) — `export RELAYAPI_API_KEY="rlay_live_..."` in shell profile
4. **Do NOT proceed with any API calls until the key is configured.**
5. **Do NOT ask the user to paste the key directly in chat.**

All requests require:

```
Authorization: Bearer $RELAYAPI_API_KEY
```

Base URL: `https://api.relayapi.dev`

## Supported Platforms (22)

`twitter`, `instagram`, `facebook`, `linkedin`, `tiktok`, `youtube`, `pinterest`, `reddit`, `bluesky`, `threads`, `telegram`, `snapchat`, `googlebusiness`, `whatsapp`, `mastodon`, `discord`, `slack`, `sms`, `beehiiv`, `convertkit`, `mailchimp`, `listmonk`

---

## Posting

### Create a Post

```bash
curl -X POST https://api.relayapi.dev/v1/posts \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello from RelayAPI!",
    "targets": ["twitter", "linkedin"],
    "scheduled_at": "now"
  }'
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content` | string | No* | Post text. Optional if every target has content in `target_options`. |
| `targets` | string[] | Yes (min 1) | Where to publish. See "Target Resolution" below. |
| `scheduled_at` | string | Yes | `"now"` = publish immediately, `"draft"` = save as draft, or ISO 8601 datetime (e.g. `"2026-06-01T12:00:00Z"`) to schedule. |
| `media` | array | No | Media attachments: `[{ "url": "https://...", "type": "image" }]`. Type can be `"image"`, `"video"`, `"gif"`, `"document"`, or `"audio"`. If omitted, type is inferred from the file extension. |
| `target_options` | object | No | Per-target content overrides. Keys are target values (platform name, account ID, or workspace ID). |
| `timezone` | string | No | IANA timezone for scheduling (default: `"UTC"`). Example: `"America/New_York"`. |
| `workspace_id` | string | No | Scope the post to a specific workspace. If omitted, operates across all workspaces. |

### Target Resolution (3 ways to specify targets)

Targets tell RelayAPI where to publish. You can mix all three types in the same request:

**1. Platform name** — publishes to ALL connected accounts on that platform:
```json
{ "targets": ["twitter"] }
```
If the user has 2 Twitter accounts connected, the post goes to both.

**2. Account ID** — publishes to one specific account:
```json
{ "targets": ["acc_abc123"] }
```
Use `GET /v1/accounts` to find account IDs.

**3. Workspace ID** — publishes to ALL accounts in a workspace:
```json
{ "targets": ["ws_xyz789"] }
```
Use `GET /v1/workspaces` to find workspace IDs. A workspace named "Marketing" with a Twitter and Instagram account will publish to both.

**Mixed example:**
```json
{ "targets": ["ws_marketing", "acc_ceo_linkedin", "youtube"] }
```
This publishes to all accounts in the "Marketing" workspace + the CEO's specific LinkedIn account + all YouTube accounts.

**Error codes for failed targets:**
- `NO_ACCOUNT` — no accounts exist for the platform name
- `ACCOUNT_NOT_FOUND` — the `acc_*` ID doesn't exist in this workspace
- `WORKSPACE_NOT_FOUND` — the `ws_*` ID doesn't exist in this organization
- `EMPTY_WORKSPACE` — the workspace exists but has no accounts assigned
- `INVALID_TARGET` — not a valid platform name, account ID, or workspace ID

### Per-Platform Customization

Use `target_options` to override content per target. Keys match target values:

```json
{
  "content": "Default text for all platforms",
  "targets": ["twitter", "linkedin", "instagram"],
  "scheduled_at": "now",
  "target_options": {
    "twitter": { "content": "Short tweet with #hashtags (280 char limit)" },
    "instagram": { "content": "Instagram caption ✨", "first_comment": "#tags #here" },
    "linkedin": { "content": "Professional long-form version..." }
  }
}
```

You can also key by account ID or workspace ID:
```json
{
  "target_options": {
    "acc_abc123": { "content": "Custom for this specific account" },
    "ws_xyz": { "content": "Custom for all accounts in this workspace" }
  }
}
```

Audio is a first-class media type. WhatsApp audio messages require a digits-only
recipient under `target_options.whatsapp.to` and cannot include caption content:

```json
{
  "targets": ["whatsapp"],
  "scheduled_at": "now",
  "media": [{ "url": "https://example.com/voice.mp3", "type": "audio" }],
  "target_options": { "whatsapp": { "to": "15551234567" } }
}
```

### Media Attachments

**Option 1 — External URL** (simplest):
```json
{
  "content": "Check this out!",
  "targets": ["instagram", "twitter"],
  "scheduled_at": "now",
  "media": [
    { "url": "https://example.com/photo.jpg", "type": "image" }
  ]
}
```

**Option 2 — Upload first, then reference** (more reliable):
```bash
# Create a pending upload intent
presign="$(curl --fail-with-body -sS -X POST https://api.relayapi.dev/v1/media/presign \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filename":"photo.jpg","content_type":"image/jpeg"}')"

upload_url="$(printf '%s' "$presign" | jq -r '.upload_url')"
upload_content_type="$(printf '%s' "$presign" | jq -r '.upload_headers["Content-Type"]')"
upload_precondition="$(printf '%s' "$presign" | jq -r '.upload_headers["If-None-Match"]')"
media_url="$(printf '%s' "$presign" | jq -r '.url')"
storage_key="${media_url#https://media.relayapi.dev/}"

# PUT once using every exact header returned above
curl --fail-with-body -sS -X PUT "$upload_url" \
  -H "Content-Type: $upload_content_type" \
  -H "If-None-Match: $upload_precondition" \
  --data-binary @photo.jpg

# Confirm the object before attaching it (mandatory)
jq -n --arg storage_key "$storage_key" '{storage_key: $storage_key}' | \
  curl --fail-with-body -sS -X POST https://api.relayapi.dev/v1/media/confirm \
    -H "Authorization: Bearer $RELAYAPI_API_KEY" \
    -H "Content-Type: application/json" \
    --data-binary @-

# Use media: [{"url": media_url, "type": "image"}] in the post body.
# The presign response also contains the pending intent id and expires_in.
```

**Option 3 — Direct upload:**
```bash
curl -X POST "https://api.relayapi.dev/v1/media/upload?filename=photo.jpg" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: image/jpeg" \
  --data-binary @photo.jpg
```

### Post Statuses

After creation, a post can be in one of these states:

| Status | Meaning |
|--------|---------|
| `draft` | Saved but not scheduled or published |
| `scheduled` | Queued to publish at a future time |
| `publishing` | Currently being sent to platforms (async) |
| `published` | Successfully published to ALL targets |
| `partial` | Published to SOME targets, failed on others |
| `failed` | Failed on ALL targets |

**Important:** When `scheduled_at` is `"now"`, the API returns immediately with status `"publishing"`. The actual publishing happens asynchronously. Always check the post status afterwards or use webhooks to be notified.

### List Posts

```bash
curl "https://api.relayapi.dev/v1/posts?limit=20" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

**Query parameters:** `limit` (1-100, default 20), `cursor`, `workspace_id` (optional — scope to a specific workspace), `account_id`, `status` (draft/scheduled/publishing/published/failed/partial), `from` (ISO datetime), `to` (ISO datetime).

### Get Post Details

```bash
curl https://api.relayapi.dev/v1/posts/{post_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

Response includes per-target status with platform URLs for published targets.

### Update a Post

Only `draft`, `scheduled`, or `failed` posts can be updated.

```bash
curl -X PATCH https://api.relayapi.dev/v1/posts/{post_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "content": "Updated content", "targets": ["twitter", "linkedin"] }'
```

### Delete a Post

```bash
curl -X DELETE https://api.relayapi.dev/v1/posts/{post_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

### Retry Failed Targets

Re-attempts publishing for targets that failed:

```bash
curl -X POST https://api.relayapi.dev/v1/posts/{post_id}/retry \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

### Unpublish a Post

Deletes the post from platforms and marks it as cancelled:

```bash
curl -X POST https://api.relayapi.dev/v1/posts/{post_id}/unpublish \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "platforms": ["twitter"] }'
```

Omit `platforms` to unpublish from all. Only works on `published` or `partial` posts.

### Bulk Create Posts

Create up to 50 posts in one request:

```bash
curl -X POST https://api.relayapi.dev/v1/posts/bulk \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [
      { "content": "Post 1", "targets": ["twitter"], "scheduled_at": "now" },
      { "content": "Post 2", "targets": ["linkedin"], "scheduled_at": "2026-06-01T12:00:00Z" },
      { "content": "Post 3", "targets": ["ws_marketing"], "scheduled_at": "draft" }
    ]
  }'
```

Response includes `summary: { total, succeeded, failed }`.

### Publishing Logs

View per-target publish history:

```bash
curl "https://api.relayapi.dev/v1/posts/logs?limit=50" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

---

## Account Management

### List Connected Accounts

```bash
# All accounts
curl https://api.relayapi.dev/v1/accounts \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Filter by workspace
curl "https://api.relayapi.dev/v1/accounts?workspace_id=ws_abc123" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Accounts not assigned to a workspace
curl "https://api.relayapi.dev/v1/accounts?ungrouped=true" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Search by username
curl "https://api.relayapi.dev/v1/accounts?search=john" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

Response per account:
```json
{
  "id": "acc_abc123",
  "platform": "twitter",
  "platform_account_id": "12345",
  "username": "@johndoe",
  "display_name": "John Doe",
  "avatar_url": "https://...",
  "metadata": {},
  "workspace": { "id": "ws_xyz", "name": "Marketing" },
  "connected_at": "2026-01-15T10:00:00Z",
  "updated_at": "2026-03-30T14:00:00Z"
}
```

### Get Single Account

```bash
curl https://api.relayapi.dev/v1/accounts/{account_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

### Update Account

```bash
curl -X PATCH https://api.relayapi.dev/v1/accounts/{account_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "New Display Name",
    "workspace_id": "ws_abc123",
    "metadata": { "custom_field": "value" }
  }'
```

Set `"workspace_id": null` to remove the account from its workspace.

### Disconnect (Delete) Account

```bash
curl -X DELETE https://api.relayapi.dev/v1/accounts/{account_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

### Account Health

Check if tokens are valid and not expired:

```bash
# All accounts
curl https://api.relayapi.dev/v1/accounts/health \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Single account
curl https://api.relayapi.dev/v1/accounts/{account_id}/health \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

Response: `{ "id", "platform", "username", "healthy": true/false, "token_expires_at", "error"? }`

### Workspaces

Workspaces let you organize accounts and publish to all of them at once using `ws_*` IDs as targets.

```bash
# List workspaces
curl https://api.relayapi.dev/v1/workspaces \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Create workspace
curl -X POST https://api.relayapi.dev/v1/workspaces \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Marketing Team", "description": "All brand accounts" }'

# Update workspace
curl -X PATCH https://api.relayapi.dev/v1/workspaces/{workspace_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Rebranded Team" }'

# Delete workspace (accounts are unassigned, not deleted)
curl -X DELETE https://api.relayapi.dev/v1/workspaces/{workspace_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Assign account to a workspace
curl -X PATCH https://api.relayapi.dev/v1/accounts/{account_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "workspace_id": "ws_abc123" }'
```

**Workflow example — "publish to Marketing Team":**
1. `GET /v1/workspaces` → find `ws_abc123` named "Marketing Team"
2. `POST /v1/posts` with `"targets": ["ws_abc123"]` → publishes to all accounts in that workspace

### Platform Sub-Resources

Some platforms require selecting a specific page, org, board, or location after connecting:

```bash
# Facebook Pages
curl https://api.relayapi.dev/v1/accounts/{id}/facebook-pages \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
curl -X PUT https://api.relayapi.dev/v1/accounts/{id}/facebook-pages \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -d '{ "page_id": "123" }'

# LinkedIn Organizations
curl https://api.relayapi.dev/v1/accounts/{id}/linkedin-organizations \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Pinterest Boards
curl https://api.relayapi.dev/v1/accounts/{id}/pinterest-boards \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Reddit Subreddits & Flairs
curl https://api.relayapi.dev/v1/accounts/{id}/reddit-subreddits \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
curl https://api.relayapi.dev/v1/accounts/{id}/reddit-flairs \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Google Business Locations
curl https://api.relayapi.dev/v1/accounts/{id}/gmb-locations \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

---

## Connecting Accounts

### OAuth Flow (most platforms)

This is a 2-step process:

```bash
# Step 1: Get the authorization URL
curl "https://api.relayapi.dev/v1/connect/twitter" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
# Returns: { "auth_url": "https://twitter.com/i/oauth2/authorize?..." }

# Step 2: After user authorizes, exchange the code
curl -X POST https://api.relayapi.dev/v1/connect/twitter \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "code": "the_auth_code_from_callback" }'
# Returns: { "account": { "id": "acc_...", "platform": "twitter", ... } }
```

**Supported OAuth platforms:** twitter, instagram, facebook, linkedin, tiktok, youtube, pinterest, reddit, threads, snapchat, googlebusiness, mastodon

**For platforms with sub-resources (Facebook, LinkedIn, Pinterest, Google Business, Snapchat):**
After OAuth, you need to select which page/org/board/location:
```bash
# List available pages
curl https://api.relayapi.dev/v1/connect/facebook/pages \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Select a page
curl -X POST https://api.relayapi.dev/v1/connect/facebook/pages \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -d '{ "page_id": "123456" }'
```

**Headless OAuth** (for server-side flows):
```bash
curl "https://api.relayapi.dev/v1/connect/twitter?headless=true" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
# Returns auth_url — after callback, retrieve data via (token comes from the callback):
curl "https://api.relayapi.dev/v1/connect/pending-data?token=TEMP_TOKEN" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

### Bluesky (app password, no OAuth)

```bash
curl -X POST https://api.relayapi.dev/v1/connect/bluesky \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "handle": "user.bsky.social", "app_password": "xxxx-xxxx-xxxx-xxxx" }'
```

### Telegram (bot code)

```bash
# Initiate — returns an organization-bound challenge code and bot username
curl -X POST https://api.relayapi.dev/v1/connect/telegram \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
# Returns: { "code": "RLAY-A1B2C3D4E5F6", "bot_username": "@relayapi_bot", "expires_in": 900 }

# Tell the user to message the bot with: /start RLAY-A1B2C3D4E5F6

# Poll for connection status
curl "https://api.relayapi.dev/v1/connect/telegram?code=RLAY-A1B2C3D4E5F6" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
# Returns: { "status": "pending" | "connected" | "expired" }
```

### Connection Logs

```bash
curl https://api.relayapi.dev/v1/connections/logs \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

Returns history of connect, disconnect, token refresh, and error events.

---

## Analytics

### Post Analytics (aggregated)

```bash
curl "https://api.relayapi.dev/v1/analytics?account_id=acc_abc123&from_date=2026-01-01&to_date=2026-03-31" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

**Query parameters:** `platform`, `account_id`, `post_id`, `from_date`, `to_date`, `limit` (1-100), `offset`

Returns: impressions, reach, likes, comments, shares, saves, clicks, views per post.

### Daily Metrics

```bash
curl "https://api.relayapi.dev/v1/analytics/daily-metrics?account_id=acc_abc123" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

Returns daily time series with post count, impressions, likes, comments, shares, clicks, views.

### Best Posting Time

```bash
curl "https://api.relayapi.dev/v1/analytics/best-time?platform=twitter" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

Returns `{ day_of_week (0=Sun), hour_utc (0-23), avg_engagement, post_count }` for each time slot.

### Content Decay

```bash
curl "https://api.relayapi.dev/v1/analytics/content-decay?post_id=post_abc123&days=30" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

Returns daily engagement curve and `half_life_days`.

### Post Timeline

```bash
curl "https://api.relayapi.dev/v1/analytics/post-timeline?post_id=post_abc123" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

### Posting Frequency Analysis

```bash
curl "https://api.relayapi.dev/v1/analytics/posting-frequency?platform=twitter" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

Returns posts-per-week vs engagement correlation and `optimal_frequency`.

### YouTube Daily Views

```bash
curl "https://api.relayapi.dev/v1/analytics/youtube/daily-views?account_id=acc_abc123" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

### Platform-Native Live Analytics

These fetch real-time data directly from the platform's API:

```bash
# Channel overview (followers, impressions, engagement rate)
curl "https://api.relayapi.dev/v1/analytics/channels" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Platform overview for a specific account
curl "https://api.relayapi.dev/v1/analytics/platform/overview?account_id=acc_abc123" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Post-level metrics from the platform
curl "https://api.relayapi.dev/v1/analytics/platform/posts?account_id=acc_abc123" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Audience demographics
curl "https://api.relayapi.dev/v1/analytics/platform/audience?account_id=acc_abc123" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Daily time series from platform
curl "https://api.relayapi.dev/v1/analytics/platform/daily?account_id=acc_abc123" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

Supported for: Twitter, Instagram, Facebook, LinkedIn, TikTok, YouTube, Pinterest, Threads, Google Business.

---

## Inbox

### Comments

```bash
# List comments across platforms
curl https://api.relayapi.dev/v1/inbox/comments \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# List posts with comment counts
curl https://api.relayapi.dev/v1/inbox/comments/by-post \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Comments for a specific post
curl https://api.relayapi.dev/v1/inbox/comments/{post_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Reply to a comment (account_id is REQUIRED — the account replying)
curl -X POST https://api.relayapi.dev/v1/inbox/comments/{post_id}/reply \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "account_id": "acc_abc", "comment_id": "comment_123", "text": "Thanks for your feedback!" }'

# Delete a comment
curl -X DELETE https://api.relayapi.dev/v1/inbox/comments/{comment_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Hide/unhide a comment
curl -X POST https://api.relayapi.dev/v1/inbox/comments/{comment_id}/hide \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
curl -X DELETE https://api.relayapi.dev/v1/inbox/comments/{comment_id}/hide \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Like/unlike a comment
curl -X POST https://api.relayapi.dev/v1/inbox/comments/{comment_id}/like \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
curl -X DELETE https://api.relayapi.dev/v1/inbox/comments/{comment_id}/like \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Send private reply (DM to commenter) — account_id is REQUIRED
curl -X POST https://api.relayapi.dev/v1/inbox/comments/{comment_id}/private-reply \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "account_id": "acc_abc", "text": "Hey, can we discuss this privately?" }'
```

Supported for: Facebook, Instagram, YouTube.

### Conversations (DMs)

```bash
# List conversations (add ?workspace_id=ws_abc to scope to a workspace)
curl https://api.relayapi.dev/v1/inbox/conversations \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Get a single conversation (includes its messages)
curl https://api.relayapi.dev/v1/inbox/conversations/{conversation_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Send a message (account_id is REQUIRED — the account sending)
curl -X POST https://api.relayapi.dev/v1/inbox/conversations/{conversation_id}/messages \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "account_id": "acc_abc", "text": "Hello!" }'

# Delete a message (editing a sent message is not supported by the API)
curl -X DELETE https://api.relayapi.dev/v1/inbox/conversations/{conversation_id}/messages/{message_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Archive a conversation (set status via PATCH)
curl -X PATCH https://api.relayapi.dev/v1/inbox/conversations/{conversation_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "status": "archived" }'
```

### Reviews

```bash
# List reviews (Google Business, etc.)
curl https://api.relayapi.dev/v1/inbox/reviews \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Reply to a review (account_id is REQUIRED)
curl -X POST https://api.relayapi.dev/v1/inbox/reviews/{review_id}/reply \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "account_id": "acc_abc", "text": "Thank you for your review!" }'

# Delete a review reply
curl -X DELETE https://api.relayapi.dev/v1/inbox/reviews/{review_id}/reply \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

---

## Webhooks

### Create Webhook

```bash
curl -X POST https://api.relayapi.dev/v1/webhooks \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/webhook",
    "events": ["post.published", "post.failed", "account.disconnected"],
    "workspace_id": "ws_abc"
  }'
```

**Response includes a `secret` field (shown only once) for verifying webhook signatures.**

**Available events:**

| Event | Trigger |
|-------|---------|
| `post.published` | Post successfully published to all targets |
| `post.partial` | Post published to some targets but failed on others |
| `post.failed` | Post failed on all targets |
| `post.scheduled` | Post was scheduled for later |
| `account.connected` | New social account connected |
| `account.disconnected` | Social account disconnected |
| `comment.received` | New comment on a post |
| `message.received` | New direct message received |

### Manage Webhooks

```bash
# List webhooks (add ?workspace_id=ws_abc to scope to a workspace)
curl https://api.relayapi.dev/v1/webhooks \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Update a webhook
curl -X PATCH https://api.relayapi.dev/v1/webhooks/{webhook_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "events": ["post.published"], "enabled": false }'

# Delete a webhook
curl -X DELETE https://api.relayapi.dev/v1/webhooks/{webhook_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Test a webhook (sends a test event)
curl -X POST https://api.relayapi.dev/v1/webhooks/test \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -d '{ "webhook_id": "wh_abc123" }'

# View delivery logs (global across all webhooks — no per-webhook filter)
curl https://api.relayapi.dev/v1/webhooks/logs \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

Webhook payloads are signed with HMAC-SHA256 via the `X-Relay-Signature` header.

---

## Queue & Scheduling

Set up recurring publishing slots (e.g., "every Monday at 9am"):

```bash
# Create a queue schedule
curl -X POST https://api.relayapi.dev/v1/queue/slots \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Weekday Mornings",
    "slots": [
      { "day_of_week": 1, "time": "09:00" },
      { "day_of_week": 2, "time": "09:00" },
      { "day_of_week": 3, "time": "09:00" },
      { "day_of_week": 4, "time": "09:00" },
      { "day_of_week": 5, "time": "09:00" }
    ],
    "timezone": "America/New_York"
  }'
```

`day_of_week`: 0 = Sunday, 1 = Monday, ..., 6 = Saturday.

```bash
# List queue schedules
curl https://api.relayapi.dev/v1/queue/slots \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Update a queue
curl -X PUT https://api.relayapi.dev/v1/queue/slots \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -d '{ "name": "Updated Schedule", "slots": [...] }'

# Delete a queue
curl -X DELETE https://api.relayapi.dev/v1/queue/slots \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Get next available slot
curl https://api.relayapi.dev/v1/queue/next-slot \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Preview upcoming 10 slots
curl "https://api.relayapi.dev/v1/queue/preview?count=10" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

---

## Twitter Engagement

```bash
# Retweet / Undo retweet
curl -X POST https://api.relayapi.dev/v1/twitter/retweet \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -d '{ "tweet_id": "123456", "account_id": "acc_abc123" }'
curl -X DELETE https://api.relayapi.dev/v1/twitter/retweet \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -d '{ "tweet_id": "123456", "account_id": "acc_abc123" }'

# Bookmark / Remove bookmark
curl -X POST https://api.relayapi.dev/v1/twitter/bookmark \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -d '{ "tweet_id": "123456", "account_id": "acc_abc123" }'

# Follow / Unfollow
curl -X POST https://api.relayapi.dev/v1/twitter/follow \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -d '{ "target_user_id": "789", "account_id": "acc_abc123" }'
```

---

## Reddit

```bash
# Search posts
curl "https://api.relayapi.dev/v1/reddit/search?q=relayapi&subreddit=programming&sort=relevance" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Get subreddit feed
curl "https://api.relayapi.dev/v1/reddit/feed?subreddit=programming&sort=hot" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

---

## Validation Tools

```bash
# Dry-run post validation (checks targets, character limits, media)
curl -X POST https://api.relayapi.dev/v1/tools/validate/post \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "content": "My post", "targets": ["twitter", "instagram"], "scheduled_at": "now" }'
# Returns: { "valid": true/false, "errors": [...], "warnings": [...] }

# Check character count per platform
curl -X POST https://api.relayapi.dev/v1/tools/validate/post-length \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -d '{ "content": "My post text" }'
# Returns per-platform: { "twitter": { "count": 12, "limit": 280, "within_limit": true }, ... }

# Validate media URL for platform compatibility
curl -X POST https://api.relayapi.dev/v1/tools/validate/media \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -d '{ "url": "https://example.com/video.mp4" }'

# Check subreddit exists
curl "https://api.relayapi.dev/v1/tools/validate/subreddit?name=gaming" \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Check Instagram hashtag safety
curl -X POST https://api.relayapi.dev/v1/tools/instagram/hashtag-checker \
  -H "Authorization: Bearer $RELAYAPI_API_KEY" \
  -d '{ "hashtags": ["photography", "instagood"] }'
# Returns per hashtag: "safe", "restricted", or "banned"
```

---

## Media Management

```bash
# List uploaded media
curl https://api.relayapi.dev/v1/media \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Get media details
curl https://api.relayapi.dev/v1/media/{media_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"

# Delete media
curl -X DELETE https://api.relayapi.dev/v1/media/{media_id} \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

---

## Usage & Billing

```bash
curl https://api.relayapi.dev/v1/usage \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

Returns: `plan` (free/pro), `calls_used`, `calls_included`, `current_period_start`, `current_period_end`, overage info.

```bash
# API request history
curl https://api.relayapi.dev/v1/usage/logs \
  -H "Authorization: Bearer $RELAYAPI_API_KEY"
```

---

## Platform Character Limits

| Platform | Limit |
|----------|-------|
| Twitter | 280 |
| LinkedIn | 3,000 |
| Instagram | 2,200 |
| Facebook | 63,206 |
| TikTok | 2,200 |
| YouTube | 5,000 (description) |
| Pinterest | 800 |
| Reddit | 40,000 |
| Bluesky | 300 |
| Threads | 500 |
| Mastodon | 500 |
| Google Business | 1,500 |
| Snapchat | 250 |

---

## Response Format

**All list endpoints return:**
```json
{
  "data": [...],
  "next_cursor": "string or null",
  "has_more": true
}
```

Paginate by passing `?cursor=<next_cursor>` on the next request. Default limit is 20, max is 100.

**Errors return:**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

Common error codes: `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`, `VALIDATION_ERROR`, `RATE_LIMITED`, `INTERNAL_ERROR`.

## Rate Limits

- **Free:** 100 requests/minute, 200 calls/month
- **Pro:** 1,000 requests/minute, 10,000 calls/month

Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

## Tips for AI Agents

- Always check post status after creation — `"now"` publishes asynchronously and the post can end up as `partial` or `failed`.
- Use `target_options` to customize content per platform — different character limits and conventions require different text.
- Use workspace IDs (`ws_*`) when the user refers to a collection of accounts by name.
- Use validation tools before publishing to catch issues early.
- Complete the presign -> PUT with every exact returned header -> confirm flow before attaching the canonical media URL.
- Set up webhooks for real-time notifications instead of polling.
- When the user says "post to X", first check `GET /v1/accounts` or `GET /v1/workspaces` to resolve what "X" means.
- When the user wants stats, use `/v1/analytics/platform/overview` for live data or `/v1/analytics` for historical data.

## References

- API Docs: https://api.relayapi.dev/docs
- OpenAPI Spec: https://api.relayapi.dev/openapi.json
- SDK: `npm install @relayapi/sdk`
