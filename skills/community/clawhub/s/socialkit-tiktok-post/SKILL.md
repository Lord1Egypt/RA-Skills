---
name: socialkit-tiktok-post
description: Sends a video to the user's TikTok as a draft (default) or posts it directly through the official Content Posting API, following TikTok's content sharing rules and the user's explicit choices. Use when the user wants to upload or post a video to TikTok.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: tiktok
  requires: socialkit-social-core
---

# TikTok post

Apply socialkit-social-core. Official API only. Setup: [setup](references/setup.md).

## Rules

- Default draft mode: the video goes to the TikTok inbox and the user publishes it in the app.
- Direct mode: run `node scripts/auth.mjs --platform tiktok --creator-info`, show the creator nickname and privacy options, and let the user choose privacy and comment/duet/stitch settings. Never pick defaults for them.
- Apps owned by one user stay unaudited, so direct posts are private (SELF_ONLY).

## Steps

1. Sign in once (browser, local redirect): `node scripts/auth.mjs --platform tiktok`
2. Create the post folder with the socialkit-social-core post script:
   `node <socialkit-social-core>/scripts/post.mjs --init --dir tt-<slug> --platform tiktok --kind <video>`
3. Write `post.json` (text, media with alt text, options). See `node scripts/publish.mjs --help`.
4. Validate: `node scripts/publish.mjs --check --dir tt-<slug>`
5. Stop. Show the post. Ask the user to approve in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir tt-<slug>`
6. Publish: `node scripts/publish.mjs --publish --dir tt-<slug>` and report the result.

## Failure handling

- `unaudited_client_can_only_post_to_private_accounts`: use draft mode.
- `spam_risk_too_many_posts`: daily cap reached; try tomorrow.
- Status FAILED: show fail_reason; do not retry spam-related failures.
- `APPROVAL_REQUIRED`: the post changed after approval; ask again.
- `ALREADY_PUBLISHED`: this folder was posted; use `--allow-repost` only if the user asks.
