---
name: socialkit-google-business-post
description: Publishes an update, event or offer to the user's Google Business Profile through the official Business Profile APIs after the user approves it. Use when the user wants to post to their Google Business Profile or Google Maps listing.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: google-business
  requires: socialkit-social-core
---

# Google Business Profile post

Apply socialkit-social-core. Official API only. Setup: [setup](references/setup.md).

## Rules

- The user's Google Cloud project must be approved for the Business Profile APIs first (see setup).
- Find options.location with `node scripts/auth.mjs --platform google-business --locations`.
- Photos must be at public https URLs.

## Steps

1. Sign in once (browser, local redirect): `node scripts/auth.mjs --platform google-business`
2. Create the post folder with the socialkit-social-core post script:
   `node <socialkit-social-core>/scripts/post.mjs --init --dir gbp-<slug> --platform google-business --kind <standard|event|offer>`
3. Write `post.json` (text, media with alt text, options). See `node scripts/publish.mjs --help`.
4. Validate: `node scripts/publish.mjs --check --dir gbp-<slug>`
5. Stop. Show the post. Ask the user to approve in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir gbp-<slug>`
6. Publish: `node scripts/publish.mjs --publish --dir gbp-<slug>` and report the result.

## Failure handling

- Quota or 429 errors: the project is not approved yet; see setup.
- `GBP_403`: the account cannot manage this location.
- `APPROVAL_REQUIRED`: the post changed after approval; ask again.
- `ALREADY_PUBLISHED`: this folder was posted; use `--allow-repost` only if the user asks.
