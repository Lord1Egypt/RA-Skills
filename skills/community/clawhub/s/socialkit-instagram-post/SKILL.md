---
name: socialkit-instagram-post
description: Publishes an Instagram image, carousel, Reel or Story to a Business or Creator account through the official Instagram Graph API, after validating caption limits and getting the user's approval. Use when the user wants to post to Instagram. Personal Instagram accounts are not supported by the API.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: meta
  requires: socialkit-social-core socialkit-meta-auth
---

# Instagram post

Apply socialkit-social-core. Setup: [setup](references/setup.md). Sign in with socialkit-meta-auth
(`--platform facebook`); the Instagram account must be linked to a connected Page.

## Media rules

- Images: JPEG at a public `https://` URL. Instagram downloads them; local image files
  cannot be uploaded. Ask the user where they host images if needed.
- Reels and story videos: a local MP4/MOV file is uploaded directly, or use an https URL.
- Carousel: 2 to 10 items, all by https URL.
- No scheduling through the API.

## Steps

1. `node <socialkit-social-core>/scripts/post.mjs --init --dir ig-<slug> --platform instagram --kind <image|carousel|reel|story>`
2. Write `post.json` caption (`text`) within 2,200 characters, 30 hashtags, 20 mentions;
   add `altText` to images.
3. `node scripts/publish.mjs --check --dir ig-<slug>`
4. Stop. Ask the user to approve in their own terminal:
   `node <socialkit-social-core>/scripts/post.mjs --approve --dir ig-<slug>`
5. `node scripts/publish.mjs --publish --dir ig-<slug>`. Report the permalink and the
   remaining daily quota.

## Failure handling

- Subcode 2207052: the media URL is not publicly reachable.
- `IG_DAILY_LIMIT` or subcode 2207042: daily publishing limit reached; try tomorrow.
- `IG_ACCOUNT_UNKNOWN`: link a Business/Creator account to the Page, then run socialkit-meta-auth again.
- `META_MEDIA_TIMEOUT`: the video is still processing; nothing was published.
