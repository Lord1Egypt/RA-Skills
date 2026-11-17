# Per-platform settings reference

Everything here goes in `create_post`'s `platformSettings` object, keyed by
platform name, e.g.:

```json
{
  "platformSettings": {
    "tiktok": { "privacy": "PUBLIC_TO_EVERYONE", "postMode": "direct" },
    "youtube": { "title": "My video", "description": "…" }
  }
}
```

`validate_post` checks all of this without posting — use it when unsure.
Full REST docs per platform: https://schedulala.com/developers/docs/platforms

## Character limits (main content)

| Platform | Limit |
|---|---|
| twitter | 280 |
| bluesky | 300 |
| threads | 500 |
| mastodon | 500 |
| google-business | 1500 |
| instagram | 2200 |
| tiktok | 2200 |
| linkedin | 3000 |
| telegram | 4096 |
| facebook | 63206 |

YouTube and Pinterest don't use the main content limit the same way: YouTube
takes a title (≤100 chars) + description (≤5000 chars) via platformSettings;
Pinterest takes a title (≤100) + description (≤500).

## First comments (auto-plug)

Top-level `firstComments` (or the `firstComment` string shorthand) on
`create_post` / `bulk_create_posts` / `create_thread` / `update_post` — NOT
inside platformSettings. Auto-posted ~15 seconds after the post publishes:
the "link in the first comment" workflow. Text and links only, no media.
A failed comment never fails the post — read `platforms[].firstComments` on
`get_post` for delivery status (posted with the comment url, failed, skipped).

| Platform | First comment | Comment limit |
|---|---|---|
| linkedin | ✅ | 1500 chars |
| facebook | ✅ | no fixed limit |
| instagram | ✅ | 1000 UTF-8 bytes (skipped on Stories) |
| youtube | ✅ | 10000 chars |
| twitter | ✅ | 280 chars (Premium limits apply per account) |
| threads | ✅ | 500 chars |
| bluesky | ✅ | 300 chars |
| mastodon | ✅ | instance-defined |
| tiktok | ❌ no comment API | — |
| pinterest | ❌ no comment API | — |
| telegram | ❌ no comment API | — |
| google-business | ❌ no comment API | — |

- Targeting ONLY unsupported platforms with a first comment is a validation
  error; mixed selections publish where supported and warn about the rest.
- `firstComments` entries are `{ "target": 0, "text": "…" }`. target 0 = the
  main post; on `create_thread`, target i = entry i+1 (max target =
  entries − 1), and thread-targeted comments deliver on twitter / threads /
  bluesky only (mastodon takes just the target-0 comment).
- An empty `firstComments` array on `update_post` clears pending comments.

## tiktok — BOTH fields required, no defaults

```json
{ "tiktok": { "privacy": "PUBLIC_TO_EVERYONE", "postMode": "direct" } }
```

- `privacy`: e.g. `PUBLIC_TO_EVERYONE`, `SELF_ONLY`.
- `postMode`: `direct` (publish straight to the profile) or `inbox` (send to
  the user's TikTok app inbox to finish manually).
- There is **no default for postMode — ASK the user** which they want if they
  haven't said. Applies to `create_post` and every entry of
  `bulk_create_posts`.
- Carousels (multiple images) supported.

## instagram

- **At least one media item is required** (image or video).
- Reels: `{ "instagram": { "postType": "reel" } }` — set this for any 9:16
  video meant for the Reels surface (including files that arrive via
  `attach_media`).
- Carousels: multiple `mediaItems`.

## youtube

- **A video is required.**
- `{ "youtube": { "title": "≤100 chars", "description": "≤5000 chars", "privacyStatus": "public|unlisted|private" } }`

## pinterest

- `{ "pinterest": { "boardName": "My Board", "link": "https://…" } }`
- Title ≤100 chars, description ≤500 chars.

## linkedin

- Regular posts: content ≤3000 chars.
- **Document posts (PDF)**: mediaItem `{ "type": "pdf", "url": "…" }` plus
  `{ "linkedin": { "documentTitle": "My Deck" } }`. PDFs are LinkedIn-only —
  a pdf mediaItem on any other platform is rejected at validation.

## google-business

- **Exactly one image, no video.** Content ≤1500 chars.
- `postType`: `STANDARD`, `EVENT`, or `OFFER`, with CTA buttons, via
  platformSettings.
- Engagement note: google-business "comments" are customer reviews
  (`platformData.starRating` carries the 1–5 rating); one owner reply per
  review, ≤4096 chars, replying again overwrites the previous reply.

## mastodon

- `{ "mastodon": { "visibility": "public|unlisted|private|direct" } }`
- Up to 4 images per post.
- Connecting a Mastodon account is dashboard-only (per-instance OAuth: the
  user enters their instance domain, e.g. mastodon.social, on schedulala.com).

## telegram

- Content ≤4096 chars.
- Polls: `{ "telegram": { "pollData": { … } } }` (see the preview widget or
  REST docs for the poll shape).

## twitter

- 280 chars. Threads (chains) via `create_thread`.
- Community posts: `{ "twitter": { "communityName": "…" } }` (rendered by
  `show_post_preview`).

## bluesky

- 300 chars. Connects with handle + app password (created at bsky.app under
  Settings → App Passwords, entered on schedulala.com only).
- Replies need all four AT-Protocol refs — see the engagement section of the
  skill.

## threads

- 500 chars. Chains via `create_thread`. Location tag:
  `{ "threads": { "locationName": "…" } }` (rendered by `show_post_preview`).

## facebook

- 63206 chars. Carousels supported. One Facebook account per workspace.

## Thread (chain) rules — `create_thread`

- Platforms: twitter, threads, bluesky, mastodon ONLY. Others are rejected.
- 2–25 ordered entries; each entry: own `content`, optional single media item
  (max 1 per entry), optional `platformContent` per-platform text override.
- Scheduling: `scheduledFor` or `publishNow: true`; omitting both schedules
  for now.
- `config.postDelay` is accepted for compatibility but NOT honored (the chain
  delay is fixed per platform).
- **Consumes one post of quota per entry.**
- The response has ONE postId for the whole chain — `get_post` it for status.

## Scheduling window

`scheduledFor` must be an ISO 8601 datetime **5 minutes to 90 days in the
future**. Use `timezone` (IANA, e.g. `America/New_York`) with local times.
