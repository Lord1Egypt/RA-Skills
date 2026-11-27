---
name: schedule-social-posts
description: Draft, schedule or publish social media posts through Auto Poster AI to Instagram, TikTok, LinkedIn, X, Threads, Bluesky, YouTube, Pinterest, Facebook and Telegram. Use when the user asks to post, schedule, queue or draft something on social media, or to cross-post to several platforms.
---

# Schedule social posts with Auto Poster AI

Uses the Auto Poster AI MCP tools (`autoposter_*`). If they are missing, tell the user to connect the Auto Poster AI MCP server (see the repo README) and stop.

## Workflow

1. **Find accounts.** Call `autoposter_list_accounts`. Match the platforms the user named to account IDs. If a platform has several accounts, or none match, ask which one. Never guess an ID.
2. **Check platform limits.** Call `autoposter_get_rules` once per task. Respect character limits and media requirements. Shorten or split the text yourself; do not rely on the platform to truncate.
3. **Write per-platform copy** when the platforms differ (X is short, LinkedIn is longer, Instagram needs a hook plus hashtags). Put the shared text in `content` and the differences in `platformContent` (keys like `twitter`, `linkedin`).
4. **Attach media** if any (see below).
5. **Confirm, then act.** Show the user: accounts, final text per platform, media, and send time with timezone. Then:
   - User said "draft" or gave no time: `autoposter_draft_post`.
   - User gave a time and said schedule/queue: `autoposter_schedule_post`.
   - User said "post now": `autoposter_draft_post`, then `autoposter_publish_draft` only after the user confirms the text.
   If the user already gave exact text, accounts and time in their request, that counts as confirmation. Do not ask again.
6. **Report back** with the post ID, state and scheduled time in the user's timezone.

## Times

- Pass `scheduledAt` as an ISO local datetime (`2026-10-05T14:00:00`) and set `timezone` (IANA, e.g. `America/New_York`). If the user gave no timezone and you do not know it, ask once. The time must be in the future.
- Convert relative phrases ("tomorrow 10am") using today's date. Say the resolved date back to the user.

## Media

- Public image or video URL: pass it in `mediaUrls`, or call `autoposter_upload_media` first to store it in the library.
- File only on the user's device: call `autoposter_create_upload_link`, give the user the link, wait for them to say it is done, then `autoposter_list_media` (newest first) and pass the IDs in `mediaIds`.
- Large video (over 100 MB), if you can make HTTP PUT requests: `autoposter_get_media_upload_url`. Otherwise ask for a public URL.
- Existing library file: `autoposter_list_media`, then `mediaIds`.

## Formats and extras

- `postType`: `post` (default), `reel` (needs video), `story` (needs image or video), `shorts` (vertical video under 60 s). Only set it when the user asks for that format.
- `threadComments`: follow-up texts posted in order (a tweet thread on X).
- `firstComment`: posted right after publishing. Good place for links and hashtags.
- `title`: used by YouTube, Pinterest and WordPress only.
- `visibility`: TikTok only. Default is public; do not change it unless asked.

## Rules

- Draft is the safe default. Publishing or scheduling needs the user's clear go-ahead for that exact text.
- If the API key cannot publish directly, the post lands in `pending_approval` and approvers are notified. Tell the user that, do not retry.
- Never invent links, stats or claims in the post text.
- Do not post the same text verbatim to every platform when limits or norms differ.
