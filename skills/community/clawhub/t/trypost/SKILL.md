---
name: trypost
description: Schedules and publishes social media posts through TryPost's hosted MCP server. Use when the user wants to draft, schedule, publish, preview, or analyze posts across Instagram, Facebook, LinkedIn, LinkedIn Page, X, TikTok, YouTube, Threads, Pinterest, Bluesky, Mastodon, Telegram, or Discord, or when they mention TryPost, social accounts, signatures, labels, webhooks, or repurpose.
homepage: https://trypost.it
metadata: {"openclaw":{"emoji":"📅","requires":{"bins":[],"env":[]}}}
---

# TryPost

TryPost schedules and publishes to 12 networks from one workspace. This plugin registers the hosted MCP server `https://app.trypost.it/mcp/trypost`. On first tool call the client opens a browser for OAuth (`mcp:use`). Do **not** put a Personal Access Token on the MCP URL — API keys are REST-only and return `403`. Cloud MCP requires an active plan (`402` if missing).

Docs: https://docs.trypost.it/ai/tools-reference
App: https://app.trypost.it
Site: https://trypost.it

## Hard rules

**1 — Use MCP tools, never invent IDs.** Discover `social_account_id`, `content_type`, Pinterest `board_id`, and Discord `channel_id` from tools.

**2 — `create-post-tool` always creates a draft.** `scheduled_at` on create is stored on the draft and does **not** queue publishing. Call `publish-post-tool` to publish now or schedule.

**3 — No `media[]` on create/update.** Attach after create with `attach-media-from-url-tool`, `attach-existing-asset-tool`, or `request-media-upload-tool` + `attach-media-from-upload-tool`. There is no detach/remove-media tool.

**4 — Required meta before publish** (validated by `publish-post-tool`; missing values fail):

| Platform | Required `platforms[].meta` | How to resolve |
|---|---|---|
| TikTok | `privacy_level` | `"PUBLIC_TO_EVERYONE"`, `"MUTUAL_FOLLOW_FRIENDS"`, `"FOLLOWER_OF_CREATOR"`, `"SELF_ONLY"` |
| Pinterest | `board_id` | `list-pinterest-boards-tool` |
| Discord | `channel_id` | `list-discord-channels-tool` |

**5 — Call `list-content-types-tool` before choosing `content_type`.** Honor `requires_media`, `min_media_count`, `max_media_count`, `accept_*`, `accepts_gif` / `accepts_mov`, `forbids_mixed_media`, and duration/size caps. There are **20** content types. There is no `instagram_carousel` / `linkedin_carousel` — carousels are `instagram_feed` / `linkedin_post` with multiple images or a LinkedIn PDF.

**6 — Confirm destructive tools** (`publish-post-tool`, `delete-*`, `rotate-webhook-secret-tool`) with the user before calling.

## Core workflow

```
1. get-workspace-tool
2. list-social-accounts-tool
3. list-content-types-tool
4. list-pinterest-boards-tool / list-discord-channels-tool if needed
5. create-post-tool                   # draft + platforms + meta
6. attach media (URL / library / signed upload)
7. preview-post-tool
8. publish-post-tool                  # omit scheduled_at = now; ISO 8601 future = queue
9. get-post-metrics-tool              # after published
```

Prefer public URLs or the Asset Library. Use signed upload only for a local file with no public URL.

## Authentication and roles

OAuth 2.1 + Dynamic Client Registration. First tool call opens the browser. Re-auth on `401`. `403` with "MCP OAuth authorization required" means an API key was sent — remove it. `402` means the Cloud account has no active plan.

Workspace is bound to the OAuth grant. Switch workspace in the TryPost UI (Settings → MCP) and reconnect.

| Role | Can |
|---|---|
| Viewer | Read posts/accounts/workspace. Cannot create/update/publish, list assets, list boards/channels, or manage repurpose/webhooks/keys. |
| Member | Posts, media, labels, signatures, repurpose. Cannot toggle accounts, webhooks, or API keys. |
| Owner / Admin | Everything, including `toggle-social-account-tool`, webhooks, and API keys. |

Connect or disconnect networks in the TryPost app (Accounts). MCP can only list and toggle active/inactive.

## Not in MCP

Do not invent tools for: connecting accounts, detaching media, duplicating a post, post templates, brand profile, Unsplash/Giphy, team invites, billing, in-app AI generation, or account-level analytics. Metrics are per published post via `get-post-metrics-tool` only. Signatures have no `signature_id` on create/update — append the text to `content` yourself.

## Networks

`list-social-accounts-tool` returns connected accounts (`id`, `platform`, `display_name`, `username`, `is_active`, `status`). `status` is `connected` \| `disconnected` \| `token_expired`. Skip expired/disconnected accounts and tell the user to reconnect in the app (Accounts). Platform slugs:

| Slug | Network |
|---|---|
| `instagram` | Instagram personal |
| `instagram-facebook` | Instagram Business via Facebook Page (same content types as Instagram) |
| `facebook` | Facebook **Page** (not a personal profile) |
| `linkedin` | LinkedIn profile → `linkedin_post` |
| `linkedin-page` | LinkedIn Page → `linkedin_page_post` |
| `x` | X |
| `threads` | Threads |
| `tiktok` | TikTok |
| `youtube` | YouTube Shorts only |
| `pinterest` | Pinterest |
| `bluesky` | Bluesky |
| `mastodon` | Mastodon |
| `telegram` | Telegram channel or group |
| `discord` | Discord server |

| Network | Content types | Media required | Notes |
|---|---|---|---|
| Instagram | `instagram_feed`, `instagram_reel`, `instagram_story` | yes | Stories have no viewer-facing caption. Reels are video-only. Feed carousel = multiple images on `instagram_feed`. |
| Facebook | `facebook_post`, `facebook_reel`, `facebook_story` | reel/story yes; post no | Reels/stories are video-only. |
| LinkedIn | `linkedin_post` | no | Images XOR one video XOR one PDF. `document_title` for PDFs. |
| LinkedIn Page | `linkedin_page_post` | no | Same media rules as LinkedIn. |
| X | `x_post` | no | Max 4 media. Links are defused at publish/preview. |
| Threads | `threads_post` | no | |
| TikTok | `tiktok_video`, `tiktok_photo` | yes | `privacy_level` required to publish. Video is video-only; photo is images (min 1). |
| YouTube | `youtube_short` | yes | Video-only, max ~3 min. `content` is required. Title = first line of `content` (hard cap ~100). |
| Pinterest | `pinterest_pin`, `pinterest_video_pin`, `pinterest_carousel` | yes | `board_id` required. Pin description = post `content`. Carousel needs ≥2 images. |
| Bluesky | `bluesky_post` | no | No mixed image+video. Max 4 media. |
| Mastodon | `mastodon_post` | no | Max 4 media. |
| Telegram | `telegram_post` | no | HTML sanitization at preview/publish. |
| Discord | `discord_message` | no | `channel_id` required. Channels are text/announcement the bot can post to. |

Always confirm live limits with `list-content-types-tool`. Hard caps vary a lot (X 280, Bluesky 300, Threads/Mastodon 500, YouTube ~100, LinkedIn 3000) — `preview-post-tool` is the check. GIFs stay GIFs only on X, Bluesky, Mastodon, Discord, and Telegram.

## Posts

| Tool | Notes |
|---|---|
| `list-posts-tool` | Newest `scheduled_at` first. Filters: `status` (`draft` \| `scheduled` \| `published` \| `failed`), `search` (content substring), `limit` (1–100, default 50). `published` includes `partially_published`. No filter for `publishing`. No `page`. |
| `get-post-tool` | Full post: platforms (with `meta` and `post_platform.id`), media, labels. Status may be `draft`, `scheduled`, `publishing`, `published`, `partially_published`, or `failed`. |
| `create-post-tool` | Optional `content` (max 10 000), optional `scheduled_at`, `label_ids[]`, `platforms[]` (`social_account_id` + `content_type` + optional `meta`). Platforms may be omitted (empty draft). Inactive accounts and mismatched types are rejected. |
| `update-post-tool` | `post_id` plus fields to change. Platform entries use `id` (the `post_platform` UUID). Platforms not listed are **disabled**. `meta` is merged; send `null` to clear a key. `label_ids[]` **replaces** all labels. `status` may be `draft` (unschedule) or `scheduled` only. Setting `scheduled` validates media vs every enabled type. Cannot edit a finalized / publishing post. |
| `publish-post-tool` | Needs ≥1 enabled platform. Validates required meta and media vs each content type. |
| `preview-post-tool` | Same sanitization as publish (LinkedIn Unicode bold, Telegram HTML, X link defusing). Nothing is truncated — compare `sanitized_length` vs `max_content_length`. |
| `delete-post-tool` | Permanent. |
| `get-post-metrics-tool` | Engagement on a published post. Platforms without post-level metrics return `unsupported`. |

### Media

Attach only to `draft` or `scheduled` posts. Published / partially published / failed / publishing are rejected.

| Tool | When |
|---|---|
| `attach-media-from-url-tool` | Public HTTP(S) URLs. `urls`: `[{url, alt?}]`, max 10. JPEG/PNG/GIF/WebP, MP4/MOV, PDF. Returns `attached_count` and `failed_urls`. |
| `list-assets-tool` | Workspace library (not logos/avatars). Filters: `search` (filename), `type` (`image` \| `video` \| `document`), `limit` (1–100, default 50). Returns `has_more`. No `page`. |
| `get-asset-tool` | One library item by `asset_id`. |
| `attach-existing-asset-tool` | Reuse a library item (`post_id`, `asset_id`, optional `alt`). Does not copy bytes. Same pair again does not duplicate. |
| `request-media-upload-tool` | Signed one-shot POST URL (~15 min). Returns `upload_token`, `upload_url`, `field_name` (`media`), `max_bytes`, `max_bytes_by_type`. |
| `attach-media-from-upload-tool` | After the file is POSTed: `post_id` + `upload_token` + optional `alt`. |

Image alt lives on `media[].meta.alt_text`, set via the attach tools' `alt` field (ignored for video/PDF). There is no MCP tool to remove an attached file.

Local upload: `curl -F media=@./clip.mp4 "$UPLOAD_URL"` then `attach-media-from-upload-tool`.

## Per-platform `meta`

Unknown keys are dropped. Enums are exact JSON strings.

| Platform | Optional | Required on publish |
|---|---|---|
| Instagram / Facebook | `aspect_ratio`: `"1:1"` \| `"4:5"` \| `"16:9"` \| `"original"` | — |
| LinkedIn / LinkedIn Page | `document_title` (PDF, max 300) | — |
| TikTok | `allow_comments`, `allow_duet`, `allow_stitch`, `auto_add_music`, `is_aigc`, `disclose`, `brand_content_toggle`, `brand_organic_toggle` | `privacy_level` |
| Pinterest | `title` (max 100), `link` (http/https). Description = post `content`. | `board_id` |
| Discord | `channel_name`, `mentions` (`[{token,label}]`), `embeds` (max 10: `{title,description,url,image,color}`) | `channel_id` |

X, Threads, YouTube, Bluesky, Mastodon, and Telegram have no `meta` keys.

## Accounts, workspace, labels, signatures

| Tool | Notes |
|---|---|
| `list-social-accounts-tool` | Connected accounts for this workspace. |
| `toggle-social-account-tool` | Active/inactive. Owner/Admin. Inactive accounts are skipped at publish and rejected on create/update. |
| `list-pinterest-boards-tool` | `account_id` → `{ boards: [{ id, name }], truncated }`. Use `id` as `meta.board_id`. Member+. |
| `list-discord-channels-tool` | `account_id` → `{ channels: [{ id, name }] }`. Use `id` as `meta.channel_id`. Member+. |
| `list-content-types-tool` | Live catalog: 20 types, lengths, default type, media caps per platform. |
| `get-workspace-tool` | Current workspace (`id`, `name`, timestamps). |
| `list-labels-tool` | Color tags. |
| `create-label-tool` | `name`, `color` (`#RRGGBB`). |
| `update-label-tool` | `label_id`, `name`, `color`. |
| `delete-label-tool` | Detaches the label from posts. |
| `list-signatures-tool` | Reusable hashtag/CTA blocks. |
| `create-signature-tool` | `name`, `content`. |
| `update-signature-tool` | `signature_id`, `name`, `content`. |
| `delete-signature-tool` | Permanent. |

To apply a signature: `list-signatures-tool`, then put that `content` at the end of the post `content` on create or update.

## Repurpose

Watches Instagram or Facebook videos posted *outside* TryPost and replicates them. Create as draft → destinations (video `content_type` + required destination meta) → `activate-repurpose-tool`. Only videos published after activate are copied. Videos already published through TryPost are skipped. Owner/Admin/Member.

| Tool | Notes |
|---|---|
| `list-repurpose-source-formats-tool` | Watchable formats: `reel`, `video`, `story`. |
| `list-repurposes-tool` | Newest first. Optional `page`. 25 per page. |
| `get-repurpose-tool` | One row: source, destinations, status, last poll error. |
| `create-repurpose-tool` | `source_social_account_id` (Instagram/Facebook), optional `source_format` (default `reel`), `publish_mode` (`publish` \| `draft`), `destinations[]`. One source+format per workspace. |
| `update-repurpose-tool` | Changing source or format resets the watermark. |
| `list-repurpose-items-tool` | Activity for one row. Look here when a video was not replicated. |
| `activate-repurpose-tool` | Draft or disabled only. Needs a usable source, one destination, and required dest meta. Stamps watermark to now. |
| `pause-repurpose-tool` | Keeps watermark. |
| `resume-repurpose-tool` | User pause keeps watermark; system pause (`paused_reason` set) starts from now. |
| `disable-repurpose-tool` | Clears watermark. |
| `delete-repurpose-tool` | Stops polling. Calendar posts it already created stay. |

## Webhooks

Outgoing workspace webhooks. Owner/Admin. Events: `post.created`, `post.scheduled`, `post.unscheduled`, `post.published`, `post.partially_published`, `post.failed`, `post.deleted`. No wildcard, no `publishing` event. HMAC-SHA256 of the raw body in `X-Webhook-Signature`. Pauses after 5 consecutive failures. Status is `enabled` \| `disabled` \| `paused` (`paused` is set by TryPost, not by update).

| Tool | Notes |
|---|---|
| `list-webhooks-tool` | No signing secrets. |
| `get-webhook-tool` | Includes `signing_secret`. |
| `create-webhook-tool` | `endpoint` (public http/https) + `events[]`. Created `enabled`. Secret returned once. Does not ping. |
| `update-webhook-tool` | `endpoint`, `events`, and/or `status` (`enabled` \| `disabled` — not `paused`). Re-enabling a paused webhook resets failure count. |
| `send-webhook-test-tool` | Signed `webhook.test` ping. No delivery log. Works even if paused/disabled. |
| `rotate-webhook-secret-tool` | Previous secret stops immediately. |
| `list-webhook-logs-tool` | Newest first. Optional `limit` (1–100, default 50). |
| `replay-webhook-log-tool` | Queues a new signed delivery (`replayed: true` = queued, not delivered). Does not re-enable a paused webhook. |
| `delete-webhook-tool` | Deletes the webhook and its logs. |

## API keys

These MCP tools manage Personal Access Tokens for the **REST API**. Never send that token to `/mcp/trypost`. Owner/Admin.

| Tool | Notes |
|---|---|
| `list-api-keys-tool` | Metadata only. OAuth session tokens are excluded. |
| `create-api-key-tool` | `name`, optional `expires_at`. Returns `token` once (REST calls this `plain_token`). |
| `delete-api-key-tool` | Immediate. Cannot revoke the current MCP OAuth session. |

## Patterns

### Draft for LinkedIn + X

1. `list-social-accounts-tool` → LinkedIn and X ids
2. `create-post-tool` with `content` and both platforms
3. Optional media attach
4. `preview-post-tool` — if X is over `max_content_length`, shorten via `update-post-tool`
5. `publish-post-tool` with `scheduled_at`, or omit for now

### TikTok video

1. Account + `tiktok_video`
2. Create with `meta.privacy_level: "PUBLIC_TO_EVERYONE"` unless the user asked otherwise
3. Attach video → preview → publish

### Pinterest / Discord

Resolve `board_id` or `channel_id` first, set it on create, then attach required media (Pinterest) and publish.

### Signature

`list-signatures-tool` → append the chosen block to post `content` → preview (length may overflow X / Threads / YouTube).

### Unschedule

`update-post-tool` with `status: "draft"`.

### Local file

1. Create draft
2. `request-media-upload-tool` → user runs `curl -F media=@file "$upload_url"`
3. `attach-media-from-upload-tool` → preview → publish

## Gotchas

1. API key on MCP → `403`. OAuth only.
2. Create does not publish. Always `publish-post-tool`.
3. `scheduled_at` on create ≠ scheduled. Still a draft until publish.
4. Update platforms: omit an entry and it is disabled. Resend every platform you want enabled.
5. `update-post-tool` uses `post_platform.id`, not `social_account_id`.
6. TikTok / Pinterest / Discord fail publish without required meta.
7. Type must match the account (no `x_post` on LinkedIn; LinkedIn Page is `linkedin_page_post`).
8. Inactive (`is_active=false`) or `token_expired` / `disconnected` accounts fail publish — reconnect in the app.
9. Media type must be accepted by **every** enabled platform.
10. Bluesky and LinkedIn forbid mixed image+video (or PDF) on one post.
11. Stories have no viewer-facing caption.
12. Preview does not truncate — you must shorten over-limit text.
13. Cloud MCP needs an active plan (`402`).
14. YouTube in TryPost is Shorts only (`youtube_short`). Title is the first line of `content`.
15. Facebook is a Page. Instagram Business is `instagram-facebook`, not a separate content-type family.
16. No MCP tool removes media or connects a new account.
17. Members cannot manage webhooks, API keys, or toggle accounts.
