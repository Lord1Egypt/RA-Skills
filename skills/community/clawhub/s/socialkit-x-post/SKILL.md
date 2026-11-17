---
name: socialkit-x-post
description: Publishes a post, image or video post, or poll on X (Twitter) through the official X API v2 after showing the pay-per-use cost and getting the user's approval. Use when the user wants to post or tweet on X.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: x
  requires: socialkit-social-core
---

# X post

Apply socialkit-social-core. Official API only. Setup: [setup](references/setup.md).

## Rules

- X charges per post: about $0.015, or $0.20 when the post contains a link. The cost is shown at approval.
- No identical cross-posting and no unsolicited @mentions (X developer guidelines).
- Media must be local files: up to 4 images or 1 video.

## Steps

1. Sign in once (browser, local redirect): `node scripts/auth.mjs --platform x`
2. Create the post folder with the socialkit-social-core post script:
   `node <socialkit-social-core>/scripts/post.mjs --init --dir x-<slug> --platform x --kind <text|media|poll>`
3. Write `post.json` (text, media with alt text, options). See `node scripts/publish.mjs --help`.
4. Validate: `node scripts/publish.mjs --check --dir x-<slug>`
5. Stop. Show the post. Ask the user to approve in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir x-<slug>`
6. Publish: `node scripts/publish.mjs --publish --dir x-<slug>` and report the result.

## Failure handling

- `X_402` or usage-capped: X API credits are used up; add credits in the X Developer Console.
- `X_403`: write access, credits or duplicate content; show the detail to the user.
- `AUTH_EXPIRED`: sign in again with the auth script.
- `APPROVAL_REQUIRED`: the post changed after approval; ask again.
- `ALREADY_PUBLISHED`: this folder was posted; use `--allow-repost` only if the user asks.
