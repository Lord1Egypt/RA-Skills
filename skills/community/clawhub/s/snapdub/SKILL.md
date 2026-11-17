---
name: snapdub
description: >-
  Turn a long video (stream, podcast, interview, gameplay VOD) into short vertical clips with captions
  using SnapDub, then pick the best ones, schedule them to TikTok, YouTube or Instagram, and find live
  paid clipping campaigns to submit them to. Use when someone wants clips from a YouTube, Twitch, Kick,
  Rumble or Zoom link, wants to run a clipping page or clip for Whop/Content Rewards campaigns, or asks
  which of their SnapDub clips to post first.
version: 1.0.0
author: SnapDub
license: MIT
homepage: https://snapdub.ai/mcp-server
platforms: [macos, linux, windows]
required_environment_variables:
  - name: SNAPDUB_API_KEY
    prompt: "SnapDub API key (sd_live_...), only for the REST route. Skip it if you connect the MCP server."
    help: "Create one at https://snapdub.ai/developers/api (paid plans). The MCP server works on the free plan without a key."
    required_for: "REST API route only"
metadata:
  {
    "openclaw": { "emoji": "🎬", "homepage": "https://snapdub.ai/mcp-server", "primaryEnv": "SNAPDUB_API_KEY" },
    "hermes": { "tags": ["video", "clipping", "shorts", "tiktok", "content", "creator"] }
  }
---

# SnapDub: long video to ready-to-post clips

SnapDub does the heavy part on its own servers: it watches the whole video (what is said, what is on screen
and the sound, so it also works on gameplay with little talking), picks the moments worth posting, crops each
one to 9:16 following whoever is speaking (streams with a facecam get the camera on top and the game below),
burns in captions and writes a title, description and hashtags. Your job as the agent is to start the job,
wait politely, then help the person choose and post.

## When to Use

- "Make clips from this link", "turn this podcast/stream into shorts", "clip this VOD".
- Running a clipping page or clipping for paid campaigns (Whop Content Rewards and similar).
- "Which of my clips should I post first?", "schedule these to TikTok".
- "Find clipping campaigns I could make money on."

Not for: editing a single existing short by hand, music videos, or anything the person does not have the
right to repost.

## Quick Reference

Two ways to connect. Prefer the first.

1. **MCP server (recommended, free plan works):** add the remote MCP server `https://snapdub.ai/mcp`
   (streamable HTTP, OAuth sign-in). Tools: `whoami`, `estimate_cost`, `create_video`, `get_video`,
   `list_videos`, `list_clips`, `get_clip`, `edit_clip`, `list_templates`, `list_campaigns`, `get_campaign`,
   `list_social_accounts`, `schedule_post`, `list_scheduled_posts`.
2. **REST API (paid plans):** `https://snapdub.ai/api/v1`, header `Authorization: Bearer $SNAPDUB_API_KEY`.
   Same tools as endpoints, same JSON. See `{baseDir}/references/rest-api.md`.

Limits: 1 to 20 clips per video, 15 to 180 seconds each. Processing takes minutes, not seconds.

## Procedure

1. **Check the account.** Call `whoami` (REST: `GET /me`). It shows the plan and credits left. If credits look
   short for the request, call `estimate_cost` with the same settings and tell the person the number before
   starting.
2. **Start the job.** `create_video` with `url` and optional `clips`, `clip_length_seconds`, `captions`
   (default true), `translate_to` (e.g. "es") and `template` (a name from `list_templates`). REST:
   `POST /videos` with a JSON body. Keep the returned video id.
3. **Wait without hammering.** Tell the person it takes a few minutes. Check `get_video` (REST:
   `GET /videos/{id}`) about once a minute, never in a tight loop. `status: "done"` means the clips are ready;
   `failed` comes with a reason to pass on as is.
4. **Present the clips best first.** `list_clips` (REST: `GET /videos/{id}/clips`) returns each clip's title,
   virality score, description, hashtags and a download link valid for about an hour. Show the top 3 to 5 with
   one line each on why it may work. The score is a ranking aid, not a promise of views: say so if asked.
5. **Post or schedule, only when asked.** `list_social_accounts` shows which networks are connected, then
   `schedule_post` with `clip_id`, `platforms` (e.g. ["tiktok", "youtube"]) and an optional `post_at`.
   Never post or schedule without the person's explicit go-ahead for that clip.
6. **Campaigns (optional).** `list_campaigns` shows live paid clipping campaigns with rate, budget left and
   rules. Match clips to a campaign's rules before suggesting it, and remind the person that each campaign
   decides what it approves.

## Pitfalls

- Private, members-only or DRM videos cannot be fetched: ask for a public link or an upload in the SnapDub app.
- Download links expire after about an hour: call `list_clips` again instead of reusing an old link.
- Do not loop `get_video` every few seconds; once a minute is plenty and keeps the rate limit happy
  (120 requests a minute on REST).
- Campaigns differ on rules (watermarks, length, captions, which platforms). Read `get_campaign` before
  promising a clip fits.
- Only clip content the person may repost. Many campaigns provide their own source footage for exactly this.

## Verification

- `get_video` shows `status: "done"` and `list_clips` returns at least one clip with a working download link.
- Anything scheduled shows up in `list_scheduled_posts` with the time the person agreed to.
