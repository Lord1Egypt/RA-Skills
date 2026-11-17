---
name: socialkit-mastodon-post
description: Publishes or schedules a Mastodon post with optional media or a poll on the user's instance after the user approves it. Use when the user wants to toot or post on Mastodon or the fediverse.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: mastodon
  requires: socialkit-social-core
---

# Mastodon post

Apply socialkit-social-core. Official API only. Setup: [setup](references/setup.md).

## Rules

- The character limit comes from the user's instance; the publish step re-checks it.
- Add alt text (descriptions) to every attachment.
- options.visibility defaults to public.

## Steps

1. Check the credentials in [setup](references/setup.md) are set (environment variables only).
2. Create the post folder with the socialkit-social-core post script:
   `node <socialkit-social-core>/scripts/post.mjs --init --dir masto-<slug> --platform mastodon --kind <text|media|poll>`
3. Write `post.json` (text, media with alt text, options). See `node scripts/publish.mjs --help`.
4. Validate: `node scripts/publish.mjs --check --dir masto-<slug>`
5. Stop. Show the post. Ask the user to approve in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir masto-<slug>`
6. Publish: `node scripts/publish.mjs --publish --dir masto-<slug>` and report the result.

## Failure handling

- `MASTODON_401`/`403`: the token is invalid or lacks write:statuses or write:media.
- `APPROVAL_REQUIRED`: the post changed after approval; ask again.
- `ALREADY_PUBLISHED`: this folder was posted; use `--allow-repost` only if the user asks.
