---
name: socialkit-linkedin-post
description: Publishes a text, link, image or video post to the user's personal LinkedIn profile through the official Posts API after the user approves it. Use when the user wants to post on LinkedIn. Company page posting needs a separately approved Community Management API app.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: linkedin
  requires: socialkit-social-core
---

# LinkedIn post

Apply socialkit-social-core. Official API only. Setup: [setup](references/setup.md).

## Rules

- Posts go to the personal profile; company pages need the Community Management API and options.organizationUrn.
- Link previews are not fetched: set options.title (and options.description) for link posts.
- The sign-in lasts 60 days and cannot be refreshed; sign in again when it expires.

## Steps

1. Sign in once: `node scripts/auth.mjs --platform linkedin --start`, give the user the `signInUrl`, then `node scripts/auth.mjs --platform linkedin --finish --url "<URL they landed on>"`.
2. Create the post folder with the socialkit-social-core post script:
   `node <socialkit-social-core>/scripts/post.mjs --init --dir li-<slug> --platform linkedin --kind <text|link|image|video>`
3. Write `post.json` (text, media with alt text, options). See `node scripts/publish.mjs --help`.
4. Validate: `node scripts/publish.mjs --check --dir li-<slug>`
5. Stop. Show the post. Ask the user to approve in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir li-<slug>`
6. Publish: `node scripts/publish.mjs --publish --dir li-<slug>` and report the result.

## Failure handling

- `LINKEDIN_401`: sign in again.
- Version errors: set LINKEDIN_VERSION to a current YYYYMM version.
- `APPROVAL_REQUIRED`: the post changed after approval; ask again.
- `ALREADY_PUBLISHED`: this folder was posted; use `--allow-repost` only if the user asks.
