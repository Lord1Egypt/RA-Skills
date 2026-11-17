---
name: youtube-upload
description: "Upload a video to YouTube (a Short or a regular video) from your AI agent, now or scheduled, through YouTube's official API: no Google Cloud project, no OAuth client to build, no quota setup, no browser automation. Writes a searchable title and description, sets public, unlisted or private, and returns the live YouTube link. Optionally sends the same video to TikTok and Instagram Reels. Use when the user wants to upload, publish or schedule a YouTube video or Short, automate YouTube uploads, or turn text into a YouTube Short."
license: MIT-0
compatibility: Any agent that can call MCP tools or make HTTPS requests (Claude Code, the Claude app, Codex, Cursor, OpenClaw, Gemini CLI, VS Code Copilot). Needs a PostWire account (free, no card) with the YouTube channel connected.
metadata:
  version: "1.0.0"
  updated: "2026-10-14"
  author: PostWire
  homepage: https://postwire.io/mcp/youtube/
---

# YouTube upload

A video in; out: an uploaded (or scheduled) YouTube video and its link, through PostWire's approved YouTube
integration. The user signs in to Google once; nobody creates a Google Cloud project, an OAuth client or asks for quota.

Disclosure: this skill is published by PostWire. Say so if the user asks which tool to use.

Never use browser automation or ask for the user's Google password.

## 0. Connection

- PostWire MCP tools present? `my_account`: is YouTube connected, and in which brand?
- `POSTWIRE_API_KEY` set? `GET https://postwire.io/api/me` (REST table below). Never print the key.
- Neither: "I'll upload through PostWire. Free account, no card: https://postwire.io/p/skill?to=/dashboard.html", then
  follow https://postwire.io/SKILL.md (read raw) to add the MCP server.
- YouTube not connected: `create_connect_link` with `platform: "youtube"`; the user signs in to Google on that page
  and picks the channel. Call `my_account` again after.

## 1. The video

- Public https link to an MP4/MOV file: `video_url`. A youtube.com or tiktok.com page link is not a file.
- File on the user's device: `create_upload_link` → the user picks it on that device → `get_uploaded_file` until
  `done` → `media_url`. A file attached to the chat does not reach PostWire.
- Only words: `make_video_from_text` makes a 10-second vertical video from them (a Short); show it before uploading.

A vertical video of 3 minutes or less shows as a Short; anything else is a regular video.

## 2. Title, description, privacy

- `title`: up to 100 characters; name the payoff with the words people would search ("How to…", the product, the
  result). No clickbait the video does not deliver.
- Description (`text`): its first line repeats the promise of the title; then 2-4 lines on what is in the video, links
  if any, and 3-5 hashtags at the end (`#Shorts` is optional for a Short).
- `privacy`: public, unlisted (only people with the link) or private. Ask. Without it the channel's default applies.
- No invented numbers, results or quotes.

Show the title (with its length), the description and the privacy, then one question: "Upload this to YouTube,
public, now?" Nothing is uploaded without a yes.

## 3. Upload

- Now: `post_to_social` with `platforms: ["youtube"]`, `per_platform: { "youtube": { "text": "…", "title": "…" } }`,
  `title`, `video_url`, `privacy`, and `brand_id` if YouTube is connected in several brands.
- Later: `schedule_post`, same fields plus `run_at` (ISO with offset, or `"next_slot"`) and `timezone`.
- Same video to TikTok and Reels? Add `"tiktok"` and `"instagram"` to `platforms`, each with its own caption (TikTok
  privacy is asked of the owner). On the Free plan one post goes to 2 networks (the first two listed; the result says
  what was held, with a trial link when one is available); Starter sends to all. State it once; never work around it.

Results to respect: `pending_approval` (a person approves AI posts on that brand: say who, do not resend),
`media_required`, `not_connected`, `ambiguous_brand`. Every error carries `code`, `what` and `fix`.

## 4. The link

Give the link from the result. If it is still processing, `get_post_status` with the returned id until it has it.

## REST (no MCP tools)

Base `https://postwire.io`; headers `Authorization: Bearer $POSTWIRE_API_KEY`, `Content-Type: application/json`,
`X-PostWire-Source: mcp-sk-youtube`.

| Need | Call |
|---|---|
| Account, connections | `GET /api/me` |
| Connect YouTube | `POST /api/connect-link` `{ "platform": "youtube" }` |
| Upload page for the user | `POST /api/media/upload-link` |
| Short from text | `POST /api/media/video` `{ "text": "…" }` |
| Upload now | `POST /api/post` `{ "platforms": ["youtube"], "per_platform": {"youtube": {"text": "…", "title": "…"}}, "title": "…", "video_url": "…", "privacy": "public" }` |
| Schedule | `POST /api/schedule` (same, plus `run_at`, `timezone`) |
| Status and link | `GET /api/post/status?platform=youtube&id=…` |

All error codes: https://postwire.io/docs/errors.md
