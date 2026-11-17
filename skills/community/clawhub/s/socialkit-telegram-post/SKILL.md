---
name: socialkit-telegram-post
description: Posts a message, photo, video or album to a Telegram channel or group through the official Bot API, as the user's own bot, after the user approves it. Use when the user wants to post to their Telegram channel.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: telegram
  requires: socialkit-social-core
---

# Telegram post

Apply socialkit-social-core. Official API only. Setup: [setup](references/setup.md).

## Rules

- The bot must be an administrator of the channel with permission to post.
- Captions are limited to 1,024 characters; text messages to 4,096.
- Plain text by default; set options.parseMode to HTML only when formatting is needed.

## Steps

1. Check the credentials in [setup](references/setup.md) are set (environment variables only).
2. Create the post folder with the socialkit-social-core post script:
   `node <socialkit-social-core>/scripts/post.mjs --init --dir tg-<slug> --platform telegram --kind <text|photo|video|album>`
3. Write `post.json` (text, media with alt text, options). See `node scripts/publish.mjs --help`.
4. Validate: `node scripts/publish.mjs --check --dir tg-<slug>`
5. Stop. Show the post. Ask the user to approve in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir tg-<slug>`
6. Publish: `node scripts/publish.mjs --publish --dir tg-<slug>` and report the result.

## Failure handling

- `TELEGRAM_403`: add the bot as an admin of the channel.
- `TELEGRAM_400` chat not found: check TELEGRAM_CHAT_ID.
- `APPROVAL_REQUIRED`: the post changed after approval; ask again.
- `ALREADY_PUBLISHED`: this folder was posted; use `--allow-repost` only if the user asks.
