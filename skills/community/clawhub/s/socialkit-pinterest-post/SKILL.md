---
name: socialkit-pinterest-post
description: Creates a Pinterest Pin (image, carousel or video) on a chosen board through the official Pinterest API v5 after the user approves it. Use when the user wants to pin or post on Pinterest.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: pinterest
  requires: socialkit-social-core
---

# Pinterest post

Apply socialkit-social-core. Official API only. Setup: [setup](references/setup.md).

## Rules

- Every Pin needs options.boardId; list boards with `node scripts/auth.mjs --platform pinterest --boards`.
- Trial-access apps create Pins visible only to the user until Standard access is granted.
- Add alt text to every image.

## Steps

1. Sign in once: `node scripts/auth.mjs --platform pinterest --start`, give the user the `signInUrl`, then `node scripts/auth.mjs --platform pinterest --finish --url "<URL they landed on>"`.
2. Create the post folder with the socialkit-social-core post script:
   `node <socialkit-social-core>/scripts/post.mjs --init --dir pin-<slug> --platform pinterest --kind <image|carousel|video>`
3. Write `post.json` (text, media with alt text, options). See `node scripts/publish.mjs --help`.
4. Validate: `node scripts/publish.mjs --check --dir pin-<slug>`
5. Stop. Show the post. Ask the user to approve in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir pin-<slug>`
6. Publish: `node scripts/publish.mjs --publish --dir pin-<slug>` and report the result.

## Failure handling

- `PINTEREST_403` PINNER_DATA_ACCESS_DENIED: use a Pinterest business account.
- `PINTEREST_401`: sign in again.
- `APPROVAL_REQUIRED`: the post changed after approval; ask again.
- `ALREADY_PUBLISHED`: this folder was posted; use `--allow-repost` only if the user asks.
