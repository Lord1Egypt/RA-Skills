# Posting with WoopSocial

WoopSocial is a posting API and MCP server for TikTok, Instagram, YouTube, Facebook, LinkedIn,
X, Pinterest, Threads and Bluesky. This skill uses it to post the short to TikTok, Reels and
Shorts and to read results back. The exact fields live in the docs linked at the bottom; treat
them as the source of truth if anything here looks different.

## 1. Is it already connected?

Call `social_accounts_list`. If it works and lists the accounts the user wants, skip to step 3.

## 2. Connect (about 2 minutes)

The free plan includes MCP access for 2 social accounts, no card needed (more accounts need a
paid plan)
([pricing](https://woopsocial.com/pricing?utm_source=remotion-shorts-skill&utm_medium=skill)).
New users sign up in the same browser window as the sign-in, and a project is created for them.
Setup steps for every agent:
[woopsocial.com/agents](https://woopsocial.com/agents?utm_source=remotion-shorts-skill&utm_medium=skill).

Give the user only the path for the agent you're running in:

| Agent | How to connect |
|---|---|
| Claude (claude.ai, Desktop, Cowork) | Add WoopSocial from the [Claude directory](https://claude.ai/directory/woopsocial), click Connect and sign in |
| Cursor | Install from [cursor.directory](https://cursor.directory/plugins/woopsocial-social-media-scheduler) and sign in |
| Claude Code | `claude mcp add --transport http woopsocial "https://api.woopsocial.com/mcp"`, then `/mcp`, select woopsocial, Authenticate |
| Codex | `codex mcp add woopsocial --url https://api.woopsocial.com/mcp`, then `codex mcp login woopsocial` |
| OpenClaw | Install the [WoopSocial skill on ClawHub](https://clawhub.ai/woopsocial/skills/social-media-scheduler), or add the MCP URL to the agent's MCP config |
| Agents without sign-in support | Create an API key at [app.woopsocial.com/api-access](https://app.woopsocial.com/api-access) and use `https://api.woopsocial.com/mcp?api_key=YOUR_API_KEY` |

The API key is a password: never paste it into shared chats or commit it.

**Connect accounts from the chat.** Call `oauth_create_authorization` with the project ID and the
platform (`TIKTOK`, `INSTAGRAM` or `YOUTUBE`). It returns a link; the user opens it, approves,
and tells you when they're done. Confirm with `social_accounts_list`. Instagram needs a
professional (creator or business) account.

Find IDs yourself with `projects_list` and `social_accounts_list`; never ask the user to paste
IDs.

## 3. Upload the video

1. `media_uploads_create_session` with `projectId` and `fileSizeInBytes` (the exact size, in
   `report.json` as `bytes`).
2. Save the response as `session.json` in the project folder and run
   `node upload.mjs session.json out/<name>/<name>.mp4`. It PUTs every part to its upload URL.
3. `media_uploads_complete_session`. When the status is `READY` it includes the `mediaId`. If
   not, poll `media_uploads_get_session` until it is; on `FAILED` or `ABORTED`, report it.

Clients with a network allowlist must allow `*.r2.cloudflarestorage.com` for step 2. Upload one
file at a time: parallel requests on one key can get HTTP 429.

## 4. Build, validate, confirm, post

One body can post to all three. The caption in `content` is the default; `contentOverride` gives
an account its own text (and its own video, for per-account versions).

```json
{
  "content": [{ "text": "<TikTok/Reels caption>", "media": [{ "type": "MEDIA_LIBRARY", "mediaId": "<media id>" }] }],
  "schedule": { "type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-11-03T16:00:00Z" },
  "socialAccounts": [
    {
      "platform": "TIKTOK", "socialAccountId": "<id>",
      "postType": "VIDEO", "postMode": "DIRECT_POST",
      "privacyLevel": "<one of the account's privacyLevelOptions, chosen by the user>",
      "allowComment": true, "allowDuet": true, "allowStitch": true,
      "isYourBrand": false, "isBrandedContent": false, "isAiGeneratedContent": false,
      "autoAddMusic": false
    },
    { "platform": "INSTAGRAM", "socialAccountId": "<id>", "postType": "REEL" },
    {
      "platform": "YOUTUBE", "socialAccountId": "<id>",
      "title": "<under 100 characters>", "privacy": "public",
      "madeForKids": false,
      "contentOverride": [{ "text": "<YouTube description>", "media": [{ "type": "MEDIA_LIBRARY", "mediaId": "<media id>" }] }]
    }
  ]
}
```

TikTok:

- Call `social_accounts_get_platform_inputs` for the account first. Offer only the privacy levels
  in `privacyLevelOptions`, let the user pick (TikTok's rules say there's no default), and check
  the short is shorter than `maxVideoPostDurationSec`. Turn off comments, duets or stitches only
  if the account doesn't allow them.
- `isYourBrand: true` when the short promotes the user's own business or product (launch and
  changelog shorts). `isBrandedContent: true` only for a paid partnership.
- `isAiGeneratedContent: true` only for realistic AI scenes, people or voices. Kinetic text
  doesn't need it.
- `postMode: "MEDIA_UPLOAD"` sends the video to the user's TikTok inbox to finish in the app
  (for adding a sound). `autoAddMusic` is required but only applies to photo posts.

Instagram: `postType: "REEL"`. An optional `cover` takes an image from the media library (upload
`cover.jpg` the same way). Trial Reels (`trialParams`) need a minimum follower count; leave them
out unless the user asks.

YouTube: `title` and `privacy` are required. A vertical video under 3 minutes becomes a Short
on its own. `madeForKids` is a legal declaration: ask, never guess. `tags` and `category`
(an ID as text, e.g. `"27"` for Education) are optional.

Schedule types: `PUBLISH_NOW`, `SCHEDULE_FOR_LATER` (UTC, ISO 8601, in the future) or `DRAFT`
(saved in WoopSocial only).

Always:

1. `posts_validate` with the exact body. Fix anything it rejects.
2. Show the user: each account, its caption, TikTok privacy, YouTube title and made-for-kids,
   the time with timezone, and the cover. Wait for a clear yes.
3. `posts_create`, then `posts_get` for each target's status and link (`externalPostUrl`).

WoopSocial doesn't write captions, crop or reformat video, or add music. Don't say it does.

## 5. Read results

`social_account_posts_list` returns each post with its latest stored lifetime metrics (views,
likes, comments where the platform reports them). Collection runs in the background: report the
collection date with each number and treat a missing field as "not reported", never as zero.
Retention, swipe-away rate and watch time are only in each app's own analytics; ask the user.

## Changing a scheduled post

There's no edit. Delete it with `posts_delete` and create it again, after confirming with the
user.

## Links

- Docs: https://docs.woopsocial.com/llms.txt
- MCP tools: https://docs.woopsocial.com/mcp/tools-reference
- WoopSocial: https://woopsocial.com/?utm_source=remotion-shorts-skill&utm_medium=skill
- Agent setup: https://woopsocial.com/agents?utm_source=remotion-shorts-skill&utm_medium=skill
