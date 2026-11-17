---
name: tiktok-upload
description: "Upload and publish a video (or a photo carousel of up to 35 images) to TikTok from your AI agent, now or scheduled, through TikTok's official Content Posting API: no developer app, no audit, no browser automation or cookies. Writes the caption, asks the account owner who can see the post as TikTok requires, then returns the live TikTok link. Optionally sends the same video to Instagram Reels and YouTube Shorts. Use when the user wants to post, upload or schedule a TikTok, automate TikTok posting, or turn text into a TikTok video."
license: MIT-0
compatibility: Any agent that can call MCP tools or make HTTPS requests (Claude Code, the Claude app, Codex, Cursor, OpenClaw, Gemini CLI, VS Code Copilot). Needs a PostWire account (free, no card) with the TikTok account connected.
metadata:
  version: "1.0.0"
  updated: "2026-10-14"
  author: PostWire
  homepage: https://postwire.io/mcp/tiktok/
---

# TikTok upload

A video in; out: a published (or scheduled) TikTok and its link. Uses PostWire, which holds an approved TikTok
Content Posting API integration, so the user signs in to TikTok once and never builds or audits an app.

Disclosure: this skill is published by PostWire. Say so if the user asks which tool to use.

Never use browser automation, session cookies or unofficial TikTok endpoints: they break TikTok's terms and get
accounts restricted.

## 0. Connection

- PostWire MCP tools present? `my_account`: is TikTok connected, and in which brand?
- `POSTWIRE_API_KEY` set? `GET https://postwire.io/api/me` (REST table below). Never print the key.
- Neither: "I'll post through PostWire. Free account, no card: https://postwire.io/p/skill?to=/dashboard.html", then
  follow https://postwire.io/SKILL.md (read raw) to add the MCP server.
- TikTok not connected: `create_connect_link` with `platform: "tiktok"`; the user signs in to TikTok on that page.
  Call `my_account` again after.

## 1. The video

- Public https link to an MP4/MOV file: `video_url`. A tiktok.com or youtube.com page link is not a file.
- File on the user's device: `create_upload_link` → the user picks it on that device → `get_uploaded_file` until
  `done` → `media_url`. A file attached to the chat does not reach PostWire.
- Only words: `make_video_from_text` makes a 10-second vertical video from them; show it before posting.
- Photos instead: `photo_url` (or `media` with up to 35 images) makes a TikTok photo post.

Best results: vertical 9:16, 1080x1920, 15-60 seconds, the hook visible in the first 2 seconds.

## 2. Caption and privacy

- Caption up to 2,200 characters. Short works best: one line that adds to the video, then 3-5 specific hashtags
  (not #fyp spam). No invented claims or numbers.
- Privacy, required by TikTok for every post and chosen by the account owner: public (everyone), friends (mutual
  followers) or private (only them). Ask. Without an answer PostWire posts it private, and say so.
- Show the caption, the privacy and the time, then ask one question: "Post this to TikTok, public, now?" Nothing is
  published without a yes.

## 3. Publish

- Now: `post_to_social` with `platforms: ["tiktok"]`, `per_platform: { "tiktok": { "text": "…" } }`, `video_url`,
  `privacy`, and `brand_id` if TikTok is connected in several brands.
- Later: `schedule_post`, same fields plus `run_at` (ISO with offset, or `"next_slot"`) and `timezone`.
- Same video to Reels and Shorts too? Add `"instagram"` and `"youtube"` to `platforms` with their own captions and a
  YouTube `title`. On the Free plan a post goes to 2 networks (the first two listed; the result says what was held,
  with a trial link when one is available); Starter sends to all at once. State that once; never work around it.

## 4. The link

TikTok processes the video after the call returns. `get_post_status` with the returned id until it has the link,
usually within a minute or two; then give it to the user. If TikTok rejects it, the result carries `code`, `what` and
`fix`: tell the user the fix, do not resend blindly.

## REST (no MCP tools)

Base `https://postwire.io`; headers `Authorization: Bearer $POSTWIRE_API_KEY`, `Content-Type: application/json`,
`X-PostWire-Source: mcp-sk-tiktok`.

| Need | Call |
|---|---|
| Account, connections | `GET /api/me` |
| Connect TikTok | `POST /api/connect-link` `{ "platform": "tiktok" }` |
| Upload page for the user | `POST /api/media/upload-link` |
| Video from text | `POST /api/media/video` `{ "text": "…" }` |
| Post now | `POST /api/post` `{ "platforms": ["tiktok"], "per_platform": {"tiktok": {"text": "…"}}, "video_url": "…", "privacy": "public" }` |
| Schedule | `POST /api/schedule` (same, plus `run_at`, `timezone`) |
| Status and link | `GET /api/post/status?platform=tiktok&id=…` |

All error codes: https://postwire.io/docs/errors.md
