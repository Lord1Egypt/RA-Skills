---
name: tiktok-creator-tracker
description: Track TikTok creators and get alerted when a watched account posts a new video, with follower movement since the last check. Use when the user wants TikTok creator monitoring, competitor or influencer tracking, new-video alerts for specific accounts, or an ad-hoc look at a creator's recent videos and stats. Runs the magnova/tiktok-scraper Actor through the Apify plugin for OpenClaw; each record costs $0.001 on the user's own Apify account.
version: 1.0.0
homepage: https://apify.com/magnova/tiktok-scraper
metadata:
  openclaw:
    requires:
      env:
        - APIFY_API_TOKEN
---

# TikTok Creator Tracker

Creators post, trends move, and follower counts shift daily —
but nobody wants to open TikTok and check ten profiles by
hand. This skill keeps a watchlist of TikTok accounts and, on
each check, alerts the user to new videos from watched
creators and reports how their follower counts moved.

## Prerequisites

1. The Apify plugin for OpenClaw is installed and allowlisted:
   `openclaw plugins install @apify/apify-openclaw-plugin`
2. `APIFY_API_TOKEN` holds the user's own Apify API token. All
   runs bill to that account.
3. You call Actors through the plugin's `apify` tool: `start`
   (returns a runId), then `collect` (returns the results).

If the plugin or token is missing, stop and tell the user
exactly what to install or set. Do not scrape TikTok yourself
and do not substitute another source.

**Cost, stated plainly:** the Actor charges $0.001 per record
returned (one profile record plus one record per video), no
start fee. A daily check of 10 creators at 20 videos each is
about $0.21 per check. The Actor needs no TikTok login or
cookies — it reads public data only.

## Setup (first run only)

Ask the user for the watchlist: TikTok usernames (with or
without the @). Also ask one question:

- **Backfill or start fresh?** Default: start fresh — the
  baseline is the creator's current recent videos, and only
  videos posted afterwards alert. If they ask for backfill,
  present the first fetch (up to 30 recent videos per creator)
  as a one-time report; those videos then count as seen.

Save the answers in the state file.

## State

Keep one JSON file at `state/tiktok-creator-tracker.json` in
the workspace:

```json
{
  "watchlist": ["natgeo", "nasa"],
  "lastCheckDate": "2026-11-18",
  "seenVideoIds": ["7708408003065580831"],
  "followers": {"natgeo": 1234567}
}
```

Keep at most the last 5,000 video IDs; the per-check fetch
window is the primary dedupe, the list is the backstop.

## Check procedure

1. Read the state file. If none exists, do Setup.
2. For each username on the watchlist, start the Actor with
   the `apify` tool:
   - actorId: `magnova~tiktok-scraper`
   - input: `profiles`: [the username],
     `maxResultsPerProfile`: 20, `includeProfileRecords`: true.
3. Collect each run's results. Rows with `recordType` PROFILE
   carry the account's current counts; VIDEO rows are videos;
   SUMMARY and ERROR rows are not content.
4. From the PROFILE row, compare `followerCount` with the
   stored value for that creator and note the change.
5. Drop any VIDEO whose `videoId` is already in
   `seenVideoIds`. What remains is genuinely new.
6. Alert on what remains (format below) — alerts are sent
   before the state file is updated, so a crash can never
   lose an alert silently.
7. Only after all alerts are delivered, append the new video
   IDs, store the latest follower counts, and set
   `lastCheckDate` to today. If a creator's run failed (an
   ERROR row and nothing else), do not advance that creator —
   note the failure in your summary and let the next check
   retry it.

## Alert format

One block per creator who posted something new:

```
🎵 <@username> — <followerCount> followers (<+ or -><change> since last check)
New video: <videoDescription, trimmed to one line>
<createdAt> · <viewCount> views · <likeCount> likes · <commentCount> comments
<videoUrl>
```

- If several videos are new, list each on its own two lines
  under the same creator header.
- If a whole check finds nothing new across the watchlist,
  send one line: "No new videos from your TikTok watchlist."
  Add follower movement only if a watched account moved by
  1% or more.
- Report counts exactly as returned. Do not predict virality
  or present guesses about why a video performed as findings.

## Ad-hoc checks

The same Actor answers one-off questions without touching
the watchlist or the schedule:

- "How is @creator doing?" — run one profile with
  `includeProfileRecords: true` and report the PROFILE row
  plus the latest few videos.
- "Get @creator's latest 50 videos" — run with
  `maxResultsPerProfile: 50`.
- "Look up this video: <url>" — run with `videoUrls` set to
  the link and report the VIDEO row.

Present results in the same field order as the alert format.

## Scheduling

Offer a recurring daily check (for example 09:00 in the
user's timezone) using OpenClaw's scheduler — TikTok moves
fast enough that daily is the useful cadence; weekly is
available on request. The user can add or remove watchlist
names in chat at any time; re-read the state file at the
start of every check.
