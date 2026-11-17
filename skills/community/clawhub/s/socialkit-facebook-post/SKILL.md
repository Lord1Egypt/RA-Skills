---
name: socialkit-facebook-post
description: Drafts and publishes or schedules a post on a Facebook Page (text, link, one or several photos, or a video) through the official Graph API after the user approves the exact post. Use when the user wants to post to their Facebook Page. Facebook Pages only; personal profiles are not supported by the API.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: meta
  requires: socialkit-social-core socialkit-meta-auth
---

# Facebook post

Apply socialkit-social-core. Setup: [setup](references/setup.md). Sign in first with socialkit-meta-auth.

## Steps

1. Create the post folder with the socialkit-social-core post script:
   `node <socialkit-social-core>/scripts/post.mjs --init --dir fb-<slug> --platform facebook --kind <text|link|photo|photos|video>`
2. Write `post.json`: `text`, optional `link`, `media` entries (`{"source": "photo.jpg", "type": "image", "altText": "..."}`;
   local files are uploaded directly), optional `scheduledAt` (10 minutes to 30 days
   ahead) and `options.pageId` when several Pages are connected.
3. Validate: `node scripts/publish.mjs --check --dir fb-<slug>`
4. Stop. Show the post. Ask the user to run in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir fb-<slug>`
5. Publish: `node scripts/publish.mjs --publish --dir fb-<slug>`. Report the post id,
   URL, Page and schedule.

## Failure handling

- `APPROVAL_REQUIRED`: the post changed after approval; ask again.
- `META_PAGE_AMBIGUOUS`: set `options.pageId` to one of the listed Pages.
- Code 190: run socialkit-meta-auth again. Code 368: Meta blocked the action; do not retry.
- `ALREADY_PUBLISHED`: this folder was posted; only use `--allow-repost` if asked.
