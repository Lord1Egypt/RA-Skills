---
name: threads-publisher
description: "Publish posts and threads to Threads (by Meta). Use when the user says 'post to Threads', 'create a thread', 'publish thread', 'write a Threads post', 'reply on Threads', or wants to create text posts, photo/video posts, carousels, or multi-post threads on Threads."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🧵"
    homepage: https://boring-doc.aiagent-me.com/getting-started/mcp.html
    requires:
      config:
        - MCP Connector link from boring.aiagent-me.com (contains embedded auth token)
---

# Boring Threads Publisher

Publish posts, multi-post threads, and replies on Threads. Powered by [Boring](https://boring-doc.aiagent-me.com).

## Security & Data Handling

- **MCP link is a credential**: Your MCP Server URL (`https://boring.aiagent-me.com/mcp/t/xxxxx...`) contains an embedded authentication token. Treat it like a password — do not share it publicly.
- **Token scope**: The embedded token grants **publish access** to your connected social media accounts. It can create posts, upload media, and manage scheduled posts on the platforms you have connected. It cannot access your social media passwords or modify account settings.
- **Token storage**: The token is stored server-side in Boring's database (MongoDB on DigitalOcean). It is never written to your local filesystem. You can regenerate or revoke it anytime at [boring.aiagent-me.com/settings](https://boring.aiagent-me.com/settings).
- **Data flow**: Analytics queries are sent from Boring's server (Google Cloud, us-central1) to the platform's API on your behalf. Only performance metrics are retrieved — no content is uploaded or modified.
- **No local credentials**: No local API keys, environment variables, or secrets are needed. All auth is embedded in the MCP link.
- **Third-party service**: This skill relies on [Boring](https://boring.aiagent-me.com), an open-source social media management tool. Source code: [github.com/snoopyrain](https://github.com/snoopyrain).

## Prerequisites

1. **Sign up** at [boring.aiagent-me.com](https://boring.aiagent-me.com) with Google
2. **Connect Threads** account via OAuth
3. **Get your MCP link**: Go to **Settings** → copy your MCP Server URL (contains your auth token — treat it like a password)
4. **Add to Claude**: Paste the MCP link as a Connector — no install, no API key needed

## Workflow

### Step 1: List Accounts

Call `boring_list_accounts` and filter for `threads` platform. Show connected accounts.

### Step 2: Determine Post Type

Threads supports multiple content types:

| Type | Description | Limit |
|------|-------------|-------|
| Text | Text-only post | 500 characters |
| Photo | Single image | JPG/PNG/WEBP, max 8MB |
| Carousel | Multi-image | 2-20 images (more than other platforms!) |
| Video | Single video | MP4/MOV, max 512MB, 5 min |
| Thread | Multi-post thread | Array of text posts, each up to 500 chars |

### Step 3: Choose the Right Tool

**Single post** (text, photo, carousel, video) → use `boring_publish_post`:
```
boring_publish_post(
  account_id="<threads_account_id>",
  platform="threads",
  text="Your post content",
  media_urls=["https://..."]  (optional)
)
```

**Multi-post thread** (long-form content split into connected posts) → use `boring_publish_thread`:
```
boring_publish_thread(
  account_id="<threads_account_id>",
  platform="threads",
  texts=["First post in thread", "Second post continues...", "Third post wraps up"],
  media_urls=["https://..."]  (optional, added to first post only)
)
```

**Reply to existing post** → use `boring_reply_to_post_threads`:
```
boring_reply_to_post_threads(
  account_id="<threads_account_id>",
  reply_to_id="<original_post_id>",
  text="Your reply here",
  media_urls=["https://..."]  (optional, first URL only)
)
```

### Step 4: Handle Long Content

If the user provides content longer than 500 characters:
1. **Automatically split** into multiple posts for a thread
2. Split at sentence boundaries when possible
3. Use `boring_publish_thread` with the array of texts
4. Inform the user: "Your content was split into X connected posts"

### Step 5: Prepare Media

- **Local files**: `boring_upload_file` with `file_path`
- **URLs**: `boring_upload_from_url` to re-host
- **Google Drive**: Pass directly

### Step 6: Publish and Report

Show results:
- Post ID(s) for each published post
- Thread URL if it was a multi-post thread
- Any errors encountered

## Scheduling

Add `scheduled_at` in ISO 8601 format to schedule:
```
boring_publish_post(..., scheduled_at="2025-12-25T10:00:00Z")
boring_publish_thread(..., scheduled_at="2025-12-25T10:00:00Z")
```

## Threads-Specific Notes

- **Text-only posts**: Threads is one of the few platforms that supports pure text posts
- **Carousel limit**: Up to 20 images (vs 10 on Instagram/Facebook)
- **Token**: 60-day expiration with auto-refresh 5 days before expiry
- **Rate Limit**: 250 calls/hour per user
- **Permissions**: `threads_basic`, `threads_content_publish`, `threads_manage_replies`

## Error Handling

| Error | Solution |
|-------|----------|
| `TextTooLong` | Split into thread using `boring_publish_thread` |
| `InvalidCarouselSize` | Carousel needs 2-20 images |
| `TokenExpired` | Reconnect at boring.aiagent-me.com (rare due to auto-refresh) |
| `MediaTooLarge` | Images max 8MB, videos max 512MB |

## Documentation

Full API docs: [boring-doc.aiagent-me.com](https://boring-doc.aiagent-me.com)
