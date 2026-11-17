---
name: socialkit-threads-post
description: Publishes a Threads post (text with optional link, image, video or carousel) through the official Threads API after validating the 500-character and link limits and getting the user's approval. Use when the user wants to post on Threads.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: meta
  requires: socialkit-social-core socialkit-meta-auth
---

# Threads post

Apply socialkit-social-core. Setup: [setup](references/setup.md). Sign in with socialkit-meta-auth
(`--platform threads`).

## Rules

- Text up to 500 characters (emoji count as several), at most 5 links.
- Images and videos must be at public `https://` URLs; Threads has no direct upload.
- One optional topic tag (`options.topicTag`, 1-50 characters, no "." or "&").
- No scheduling through the API.

## Steps

1. `node <socialkit-social-core>/scripts/post.mjs --init --dir th-<slug> --platform threads --kind <text|image|video|carousel>`
2. Write `post.json`; for text posts an optional `link` becomes a link preview.
3. `node scripts/publish.mjs --check --dir th-<slug>`
4. Stop. Ask the user to approve in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir th-<slug>`
5. `node scripts/publish.mjs --publish --dir th-<slug>`. Report the permalink.

## Failure handling

- `THREADS_NOT_AUTHORISED` or `THREADS_TOKEN_EXPIRED`: run socialkit-meta-auth for threads.
- `THREADS_API__LINK_LIMIT_EXCEEDED`: reduce links to 5.
- `META_MEDIA_FAILED`: show the error_message (format, duration, bitrate) and fix the media.
