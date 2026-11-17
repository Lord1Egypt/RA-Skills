---
name: socialkit-discord-post
description: Posts a message with optional attachments to a Discord channel through a channel webhook after the user approves it. Use when the user wants to post an announcement or update to their Discord server.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: discord
  requires: socialkit-social-core
---

# Discord post

Apply socialkit-social-core. Official API only. Setup: [setup](references/setup.md).

## Rules

- Mentions never ping unless options.allowMentions is true; only set it when the user asks.
- The webhook URL is a secret; refer to it only by its environment variable name.

## Steps

1. Check the credentials in [setup](references/setup.md) are set (environment variables only).
2. Create the post folder with the socialkit-social-core post script:
   `node <socialkit-social-core>/scripts/post.mjs --init --dir dc-<slug> --platform discord --kind <text|media>`
3. Write `post.json` (text, media with alt text, options). See `node scripts/publish.mjs --help`.
4. Validate: `node scripts/publish.mjs --check --dir dc-<slug>`
5. Stop. Show the post. Ask the user to approve in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir dc-<slug>`
6. Publish: `node scripts/publish.mjs --publish --dir dc-<slug>` and report the result.

## Failure handling

- `DISCORD_404`: the webhook was deleted; create a new one. Do not retry the old URL.
- `APPROVAL_REQUIRED`: the post changed after approval; ask again.
- `ALREADY_PUBLISHED`: this folder was posted; use `--allow-repost` only if the user asks.
