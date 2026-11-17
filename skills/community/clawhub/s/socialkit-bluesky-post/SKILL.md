---
name: socialkit-bluesky-post
description: Publishes a Bluesky post with optional images or a link card through the AT Protocol, using the user's app password, after the user approves it. Use when the user wants to post on Bluesky.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: bluesky
  requires: socialkit-social-core
---

# Bluesky post

Apply socialkit-social-core. Official API only. Setup: [setup](references/setup.md).

## Rules

- 300 characters; links and #hashtags become clickable automatically.
- Alt text is required on every image; images up to 2 MB.
- Use an app password, never the account password.

## Steps

1. Check the credentials in [setup](references/setup.md) are set (environment variables only).
2. Create the post folder with the socialkit-social-core post script:
   `node <socialkit-social-core>/scripts/post.mjs --init --dir bsky-<slug> --platform bluesky --kind <text|images|link>`
3. Write `post.json` (text, media with alt text, options). See `node scripts/publish.mjs --help`.
4. Validate: `node scripts/publish.mjs --check --dir bsky-<slug>`
5. Stop. Show the post. Ask the user to approve in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir bsky-<slug>`
6. Publish: `node scripts/publish.mjs --publish --dir bsky-<slug>` and report the result.

## Failure handling

- `BLUESKY_AuthenticationRequired`: check BLUESKY_HANDLE and BLUESKY_APP_PASSWORD.
- `BLUESKY_IMAGE_SIZE`: resize the image below 2 MB.
- `APPROVAL_REQUIRED`: the post changed after approval; ask again.
- `ALREADY_PUBLISHED`: this folder was posted; use `--allow-repost` only if the user asks.
