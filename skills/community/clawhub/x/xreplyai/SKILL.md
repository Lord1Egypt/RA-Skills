---
name: xreply
description: Generate, schedule, and publish posts to X, LinkedIn, and Threads in your voice using AI. Manage preferences and track billing.
slug: xreply
version: 0.4.0
license: MIT-0
homepage: https://xreplyai.com
metadata: {"openclaw":{"emoji":"✨","requires":{"anyBins":["mcporter","npx"],"env":["XREPLY_TOKEN"]},"primaryEnv":"XREPLY_TOKEN","install":[{"id":"mcporter","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter (node)"}]}}
---

# XreplyAI — AI Post Generator

Generate, schedule, and publish posts to X, LinkedIn, and Threads in your voice using AI. Manage your post queue, preferences, and track billing and quota.

## Authentication

All tools require an `XREPLY_TOKEN` environment variable — a JWT token from XreplyAI Settings. This is automatically injected by OpenClaw when set in your skill config.

## MCP Server

The XreplyAI MCP server is published as `@xreplyai/mcp` on npm. You invoke tools via `mcporter`:

```
mcporter call 'npx @xreplyai/mcp@0.4.0' <tool_name> [param:value ...]
```

To discover all available tools and their parameters:

```
mcporter list 'npx @xreplyai/mcp@0.4.0' --all-parameters
```

## Tools

### Generation

#### xreply_posts_generate

Generate AI post(s) in the user's voice and auto-save as draft(s). Use `platform` for a single platform or `platforms` (array) to generate platform-native variants for multiple platforms at once. Each platform variant counts as 1 against the daily quota (5/day free, 100/day pro).

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate topic:"my SaaS hit 1000 users"
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate topic:"lessons from year 1" angle:story_arc
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate platform:linkedin topic:"leadership lessons"
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate angle:one_liner
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate topic:"entrepreneurship hardships" 'platforms:["twitter","linkedin","threads"]'
```

Parameters:
- `topic` (optional): topic or prompt for the post (max 280 chars)
- `angle` (optional): `one_liner` | `list` | `question` | `story_arc` | `paragraph` | `my_voice`
- `platform` (optional): `twitter` (default) | `linkedin` | `threads` | `instagram` | `youtube` — single platform, controls output length and style
- `platforms` (optional): array of 2–5 platforms — generates platform-native variants for each. Returns `variants` array + single combined post draft. Each variant counts as 1 quota.

#### xreply_posts_generate_batch

Generate multiple AI posts at once. Each post counts as 1 against the daily quota — check billing first if quota is a concern. A batch of 9 will exhaust a free account.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate_batch category:personalized count:5
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate_batch category:trending count:3
```

Parameters:
- `category` (required): `personalized` | `trending`
- `count` (required): number of posts to generate (1–9, must not exceed remaining daily quota)

---

### Post Management

#### xreply_posts_list

List all posts in the queue — drafts, scheduled, and recent posts. Returns post IDs, body text, status, scheduled times, and per-platform content.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_list
```

No parameters.

#### xreply_posts_create

Save a post draft. Use `body` for a simple X-only post. Use `post_contents` for LinkedIn, Threads, or when posting different content to multiple platforms. The post is not published until you call `xreply_posts_publish`.

**X-only post (simple):**
```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create body:"Your tweet text here"
```

**X post with auto-retweet:**
```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"twitter","body":"Tweet text","metadata":{"auto_rt_hours":24}}]'
```

**LinkedIn post:**
```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"linkedin","body":"Your long LinkedIn post here..."}]'
```

**Cross-post to X and LinkedIn with different text:**
```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"twitter","body":"Short tweet"},{"platform":"linkedin","body":"Expanded LinkedIn version..."}]'
```

**X post with image (upload first with xreply_media_upload):**
```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"twitter","body":"Check this out","content_type":"single_image","metadata":{"media_id":"1234567890"}}]'
```

**LinkedIn post with image (upload first with xreply_media_upload):**
```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"linkedin","body":"Caption here","content_type":"single_image","metadata":{"asset_urn":"urn:li:digitalmediaAsset:..."}}]'
```

Parameters:
- `body` (optional): X post body text (max 280 chars). Use `post_contents` for LinkedIn, Threads, or cross-posting.
- `post_contents` (optional): array of per-platform content objects. Takes precedence over `body`.
  - `platform` (required): `twitter` | `linkedin` | `threads`
  - `body` (required, except for LinkedIn video): post body (max 280 for X, max 3000 for LinkedIn, max 500 for Threads). Optional when `content_type` is `video`.
  - `content_type` (optional): `text` (default) | `single_image` | `multi_image` | `video`
  - `metadata` (optional): For X images: `{ media_id: "..." }` or `{ media_ids: ["..."] }`. For LinkedIn images: `{ asset_urn: "..." }` or `{ asset_urns: ["..."] }`. For LinkedIn video: `{ asset_urn: "..." }` (from `xreply_video_upload`). For Threads image: `{ image_url: "https://..." }` (public HTTPS URL — no upload step needed). For auto-retweet: `{ auto_rt_hours: 24 }`. For X communities: `{ community_id: "12345" }` (use `xreply_list_twitter_communities` to get IDs).
- `account_id` / `account_ids` (optional): social account(s) to post from

#### xreply_posts_edit

Edit a post's content, scheduled time, or auto-retweet setting. Use `body` to update X-only text, or `post_contents` to update per-platform content. Cannot edit posts that are processing or already published.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_edit id:123 body:"Updated tweet text"
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_edit id:123 'scheduled_at:2026-03-15T09:00:00Z'
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_edit id:123 post_contents:'[{"platform":"linkedin","body":"Updated LinkedIn text"}]'
```

Parameters:
- `id` (required): post ID (integer)
- `body` (optional): new X body text (max 280 chars)
- `post_contents` (optional): per-platform content to update — replaces content for submitted platforms only. `platform` can be `twitter` | `linkedin` | `threads`. `metadata.auto_rt_hours` sets X auto-retweet hours; pass `null` to disable. `metadata.community_id` sets the X community to post into (use `xreply_list_twitter_communities` to get IDs). For Threads image: `metadata.image_url`.
- `scheduled_at` (optional): ISO 8601 datetime string — omit to leave unchanged; pass `null` to unschedule

#### xreply_posts_delete

Delete a post. Cannot delete posts that are processing or already published.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_delete id:123
```

Parameters:
- `id` (required): post ID (integer)

---

### Media Upload

#### xreply_media_upload

Upload an image file from disk and get back a media identifier to attach to a post. Call this before `xreply_posts_create` or `xreply_posts_edit` to attach images. Supports JPEG, PNG, GIF, and WebP up to 5 MB.

**Note:** Requires filesystem access — works in Claude Code, Cursor, and mcporter CLI. Not available in Claude.ai (no filesystem); in that case use the Posts dashboard at app.xreplyai.com/dashboard/posts to attach images directly.

**Upload an image for X:**
```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_media_upload image_path:/path/to/photo.jpg platform:twitter
→ returns { platform: "twitter", media_id: "1234567890" }
```

**Upload an image for LinkedIn:**
```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_media_upload image_path:/path/to/photo.png platform:linkedin
→ returns { platform: "linkedin", asset_urn: "urn:li:digitalmediaAsset:..." }
```

Parameters:
- `image_path` (required): absolute or relative path to the image file on disk
- `platform` (required): `twitter` | `linkedin`
- `content_type` (optional): `image/jpeg` | `image/png` | `image/gif` | `image/webp` — inferred from extension if omitted

Use the returned identifier in `post_contents[].metadata`:
- X single image: `metadata: { media_id: "..." }`
- X multiple images: `metadata: { media_ids: ["...", "..."] }`
- LinkedIn single image: `metadata: { asset_urn: "urn:li:..." }`
- LinkedIn multiple images: `metadata: { asset_urns: ["urn:li:...", "urn:li:..."] }`

#### xreply_video_upload

Upload an MP4 video file from disk to LinkedIn and get back an asset URN to attach to a post. Uses your primary connected LinkedIn account. Call this before `xreply_posts_create` or `xreply_posts_edit` to attach a video. Supports MP4 only, up to 100 MB.

**Note:** Only LinkedIn is supported — X video upload requires OAuth 1.0a which is not currently supported. Requires filesystem access — works in Claude Code, Cursor, and mcporter CLI. Not available in Claude.ai; use the Posts dashboard at app.xreplyai.com/dashboard/posts to attach videos directly.

**Upload a video for LinkedIn:**
```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_video_upload video_path:/path/to/video.mp4
→ returns { platform: "linkedin", asset_urn: "urn:li:video:ABC123" }
```

Parameters:
- `video_path` (required): absolute or relative path to the MP4 file on disk (max 100 MB)

Use the returned `asset_urn` in `post_contents[].metadata` with `content_type: "video"`:
- LinkedIn video: `content_type: "video", metadata: { asset_urn: "urn:li:video:..." }` (body is optional)

---

### Publishing

#### xreply_posts_publish

Publish or schedule a post. Requires `account_id` or `account_ids` — if neither is provided and no accounts were attached when the post was created, returns `NO_ACCOUNT_SPECIFIED`. If `scheduled_at` is provided (ISO 8601), the post will be queued for that time (scheduling horizon depends on your plan). If `use_next_slot: true`, the post is queued into the next open slot in the account owner's posting schedule (same as the dashboard's "Add to Queue") — mutually exclusive with `scheduled_at`. If both are omitted, the post is published immediately. Each platform (X, LinkedIn) requires the corresponding social account to be connected.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:123 account_id:1
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:123 account_id:1 'scheduled_at:2026-03-15T09:00:00Z'
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:123 account_id:1 use_next_slot:true
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:123 'account_ids:[1,2]'
```

Parameters:
- `id` (required): post ID (integer)
- `account_id` (required if no accounts attached): social account ID to publish from
- `account_ids` (optional): array of social account IDs — takes precedence over `account_id`
- `scheduled_at` (optional): ISO 8601 datetime to schedule; omit to publish immediately
- `use_next_slot` (optional): `true` to queue into the next open posting-schedule slot. Mutually exclusive with `scheduled_at`. Returns `NO_SLOT_AVAILABLE` if the account owner has no posting schedule with an open slot.

#### xreply_posts_next_slot

Preview when a post would go out if queued — returns `{ scheduled_at }` without scheduling anything. Resolves the same slot that `xreply_posts_publish` with `use_next_slot: true` would use.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_next_slot id:123
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_next_slot id:123 account_id:1
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_next_slot id:123 'account_ids:[1,2]'
```

Parameters:
- `id` (required): post ID (integer)
- `account_id` (optional): social account ID to resolve the posting schedule from
- `account_ids` (optional): array of social account IDs — takes precedence over `account_id`; when neither is provided, falls back to the post's attached accounts

Returns `NO_SLOT_AVAILABLE` if the account owner has no posting schedule with an open slot.

---

### Context

#### xreply_billing_status

Get subscription tier (free/starter/pro/team), quota usage, daily limits, and subscription details.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_billing_status
```

No parameters.

#### xreply_voice_status

Get voice profile status — whether it has been analyzed, tweet count, AI provider configured, and writing style summary.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_voice_status
```

No parameters.

#### xreply_preferences_get

Get current post generation preferences — tone, emoji usage, and default structure.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_preferences_get
```

No parameters.

#### xreply_preferences_set

Update post generation preferences. Provide only the fields you want to change.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_preferences_set tone:witty
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_preferences_set tone:professional include_emoji:false
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_preferences_set structure:story_arc
```

Parameters:
- `tone` (optional): `auto` | `casual` | `professional` | `witty` | `empathetic`
- `include_emoji` (optional): `true` | `false`
- `structure` (optional): `one_liner` | `paragraph` | `question` | `list` | `story_arc`

#### xreply_list_social_accounts

List all connected social accounts (X/Twitter, LinkedIn, YouTube, Threads) with their IDs, platform, username, and primary status. Use this to find `account_id` values needed for `xreply_posts_create` and `xreply_posts_publish` — especially for newly connected accounts that have no posts yet.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_list_social_accounts
```

Returns: `social_accounts[]` — each with `id`, `platform`, `uid` (platform-native user ID), `username`, `email`, `primary`, `connected_at`.

#### xreply_platform_styles_get

Get the effective platform style profiles — system defaults merged with your per-platform overrides. Shows tone, structure, target length, hashtag rules, CTA rules, and whether defaults are active.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_platform_styles_get
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_platform_styles_get platform:linkedin
```

Parameters:
- `platform` (optional): `twitter` | `linkedin` | `threads` | `instagram` | `youtube` — omit to get all platforms

#### xreply_platform_styles_set

Override style settings for a specific platform. Only the fields you provide are updated — other fields keep their system defaults. Changes apply to all future generation for that platform.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_platform_styles_set platform:linkedin tone:witty
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_platform_styles_set platform:threads hashtag_rules:none cta_rules:soft_question
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_platform_styles_set platform:linkedin custom_instructions:"always reference my bootstrapping journey"
```

Parameters:
- `platform` (required): `twitter` | `linkedin` | `threads` | `instagram` | `youtube`
- `tone` (optional): `auto` | `casual` | `professional` | `witty` | `empathetic`
- `target_length` (optional): integer — target character count for generated posts
- `hashtag_rules` (optional): `none` | `few` | `moderate` | `match_voice`
- `cta_rules` (optional): `never` | `soft_question` | `link_in_comments` | `direct`
- `banned_phrases` (optional): array of strings — phrases to never use for this platform
- `custom_instructions` (optional): free-text instructions, max 500 chars

---

#### xreply_rules_list

List custom writing rules applied during generation — e.g. "never use hashtags", "always end with a question". Requires a Pro subscription.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_rules_list
```

No parameters.

#### xreply_rules_create

Add a new custom writing rule. Requires a Pro subscription.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_rules_create title:"No hashtags" content:"Never use hashtags in any post"
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_rules_create title:"End with question" content:"Always end posts with a question to drive engagement" active:true
```

Parameters:
- `title` (required): short label for the rule (e.g. "No hashtags")
- `content` (required): the rule instruction applied during generation
- `active` (optional): `true` (default) | `false`

#### xreply_rules_update

Edit an existing custom writing rule. Only the fields you provide are changed. Use `xreply_rules_list` to get rule IDs. Requires a Pro subscription.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_rules_update id:1 content:"Never use hashtags or emoji"
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_rules_update id:2 active:false
```

Parameters:
- `id` (required): rule ID (integer, from `xreply_rules_list`)
- `title` (optional): new label
- `content` (optional): new rule instruction
- `active` (optional): `true` | `false`

#### xreply_rules_delete

Delete a custom writing rule permanently. Use `xreply_rules_list` to get rule IDs. Requires a Pro subscription.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_rules_delete id:1
```

Parameters:
- `id` (required): rule ID (integer, from `xreply_rules_list`)

#### xreply_content_plan_list

List your automated weekly content plans. Returns each plan's name, active status, platform configs, content strategy/topics, schedule day and time, and when it last ran and is next due. Use this before generating posts manually to see what content is already scheduled to auto-generate.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_content_plan_list
```

No parameters.

#### xreply_list_twitter_communities

List the X communities the user has previously posted to, ordered by most recently used. Returns community IDs and names to use as `community_id` in post_contents metadata.

```
mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_list_twitter_communities
```

No parameters.

---

## Workflow Examples

### Generate and schedule an X post

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate topic:"ship fast, learn faster" angle:story_arc
   → returns { body: "...", post: { id: 42, ... } }
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:42 account_id:1 'scheduled_at:2026-03-12T09:00:00Z'
```

### Generate and schedule a LinkedIn post

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate platform:linkedin topic:"leadership lessons from year 1" angle:story_arc
   → returns { body: "...", post: { id: 43, ... } }
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:43 account_id:2 'scheduled_at:2026-03-12T09:00:00Z'
```

### Cross-post to X and LinkedIn with different text

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate topic:"motivation" platform:twitter
   → { body: "Short tweet...", post: { id: 44 } }
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate topic:"motivation" platform:linkedin
   → { body: "Long LinkedIn article...", post: { id: 45 } }

   Or create as a single post with both platforms:
3. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"x","body":"Short tweet..."},{"platform":"linkedin","body":"Long LinkedIn article..."}]'
4. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:46 'account_ids:[1,2]' 'scheduled_at:2026-03-13T09:00:00Z'
```

### Plan posts for the week

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_billing_status
   → check remaining quota before a large batch
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_generate_batch category:personalized count:7
   → generates 7 drafts
3. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_list
   → review the queue
4. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_edit id:101 'scheduled_at:2026-03-11T09:00:00Z'
   mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_edit id:102 'scheduled_at:2026-03-12T09:00:00Z'
   → schedule each post
```

### Queue a draft to the next open slot

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create body:"Your tweet text here"
   → { post: { id: 60, ... } }
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_next_slot id:60
   → { scheduled_at: "2026-03-12T09:00:00Z" } — optional preview
3. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:60 account_id:1 use_next_slot:true
```

### Edit and publish an existing draft

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_list
   → find the draft ID
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_edit id:55 body:"Revised tweet text"
3. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:55 account_id:1
```

### Post an X image

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_media_upload image_path:/Users/me/photo.jpg platform:twitter
   → { media_id: "1234567890" }
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"twitter","body":"Check this out!","content_type":"single_image","metadata":{"media_id":"1234567890"}}]'
   → { post: { id: 77, ... } }
3. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:77 account_id:1
```

### Post to an X community

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_list_twitter_communities
   → returns [{ community_id: "12345", name: "AI Builders", last_used_at: "..." }, ...]
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"twitter","body":"Exciting update for the community!","metadata":{"community_id":"12345"}}]'
   → { post: { id: 88, ... } }
3. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:88 account_id:1
```

---

### Post to Threads

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_list_social_accounts
   → find your Threads account id (platform: "threads")
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"threads","body":"Your Threads post here (max 500 chars)"}]'
   → { post: { id: 90, ... } }
3. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:90 account_id:3
```

### Post a Threads image

Threads takes a public image URL directly — no upload step needed (unlike X and LinkedIn).

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"threads","body":"Check this out!","content_type":"single_image","metadata":{"image_url":"https://example.com/image.jpg"}}]'
   → { post: { id: 91, ... } }
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:91 account_id:3
```

---

### Post a LinkedIn image

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_media_upload image_path:/Users/me/banner.png platform:linkedin
   → { asset_urn: "urn:li:digitalmediaAsset:ABC123" }
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"linkedin","body":"Excited to share this!","content_type":"single_image","metadata":{"asset_urn":"urn:li:digitalmediaAsset:ABC123"}}]'
   → { post: { id: 78, ... } }
3. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:78 account_id:2
```

### Post a LinkedIn video

```
1. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_video_upload video_path:/Users/me/demo.mp4
   → { platform: "linkedin", asset_urn: "urn:li:video:ABC123" }
2. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_create post_contents:'[{"platform":"linkedin","body":"Watch this demo!","content_type":"video","metadata":{"asset_urn":"urn:li:video:ABC123"}}]'
   → { post: { id: 79, ... } }
3. mcporter call 'npx @xreplyai/mcp@0.4.0' xreply_posts_publish id:79 account_id:2
```

---

## Error Handling

**Token expired:** If tools return a 401 error, the `XREPLY_TOKEN` has expired (tokens last 30 days). Ask the user to get a fresh token from XreplyAI Settings and update it in their OpenClaw config.

**Quota exhausted:** If generation returns a quota error (e.g. "Daily generation quota exhausted"), call `xreply_billing_status` to check limits and inform the user. Quota resets at midnight.

**Quota insufficient for batch:** If `xreply_posts_generate_batch` returns `quota_insufficient: true`, reduce `count` to the `available` value shown in the response, or ask the user to confirm.

**Schedule out of range:** If scheduling returns a validation error, the requested time exceeds the plan's scheduling horizon. Call `xreply_billing_status` to check `max_schedule_days` and suggest an earlier time.

**Cannot edit/delete:** Posts with status `processing` or `posted` cannot be edited or deleted. Call `xreply_posts_list` to check the current status.

**Rules list requires Pro:** If `xreply_rules_list` returns a 403, inform the user this feature requires a Pro subscription.

**No account specified:** If publish returns `NO_ACCOUNT_SPECIFIED`, you must pass `account_id` or `account_ids`. Call `xreply_list_social_accounts` to discover available account IDs (works even for newly connected accounts with no posts yet), then retry with the correct ID.

**No slot available:** If `use_next_slot` or `xreply_posts_next_slot` returns `NO_SLOT_AVAILABLE`, the account owner has no posting schedule with an open slot. Schedule explicitly with `scheduled_at` instead, or ask the user to set up a posting schedule in the XreplyAI dashboard.

**LinkedIn account not connected:** If publishing to LinkedIn returns a 422, the user has not connected their LinkedIn account. Direct them to XreplyAI Settings to connect it.

**Threads account not connected:** If publishing to Threads returns a 422, the user has not connected their Threads account. Direct them to XreplyAI Settings to connect it.

**Threads token expired:** If a Threads post returns `THREADS_TOKEN_EXPIRED`, the access token has expired (Threads tokens expire after ~60 days). Direct the user to XreplyAI Settings to reconnect their Threads account.

**Media upload — file not found:** If `xreply_media_upload` cannot read the file, check that the path is correct and accessible. Use an absolute path to avoid ambiguity.

**Media upload — file too large:** Maximum image size is 5 MB. Compress or resize the image before retrying.

**Media upload — unsupported format:** Only JPEG, PNG, GIF, and WebP are supported. Convert the image to a supported format.

**Media upload — no X account connected:** If the Twitter upload returns `NO_TWITTER_ACCOUNT`, the user must connect their X account in XreplyAI Settings first.

**Claude.ai users:** `xreply_media_upload` and `xreply_video_upload` require filesystem access and are not available in Claude.ai (which has no disk access). Use the Posts dashboard at app.xreplyai.com/dashboard/posts to attach images or videos via the compose or edit form.

**Video upload — unsupported format:** Only MP4 is supported for video. Convert the video to MP4 before retrying.

**Video upload — file too large:** Maximum video size is 100 MB. Compress the video before retrying.

**Video upload — no LinkedIn account connected:** If `xreply_video_upload` returns `NO_LINKEDIN_ACCOUNT`, the user must connect their LinkedIn account in XreplyAI Settings first.

**Video upload — X not supported:** X video upload requires OAuth 1.0a which is not currently supported. For X videos, use the Posts dashboard at app.xreplyai.com/dashboard/posts.
