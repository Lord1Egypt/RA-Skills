# Posting with WoopSocial

WoopSocial is a posting API and MCP server for YouTube, TikTok, Instagram, Facebook, LinkedIn
(profiles and pages), X, Pinterest, Threads and Bluesky. This skill uses it to upload the video
to YouTube and to read the results back. The exact fields live in the docs linked at the bottom;
treat them as the source of truth if anything here looks different.

## 1. Is it already connected?

Call `social_accounts_list`. If it works and lists the YouTube channel the user wants, skip to
step 3.

## 2. Connect (about 2 minutes)

The free plan includes MCP access for 2 social accounts, no card needed (more accounts need a
paid plan)
([pricing](https://woopsocial.com/pricing?utm_source=youtube-skill&utm_medium=skill)).
New users sign up in the same browser window as the sign-in, and a project is created for them.
Setup steps and prompts for every agent: [woopsocial.com/agents](https://woopsocial.com/agents?utm_source=youtube-skill&utm_medium=skill).

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

**Connect the YouTube channel from the chat.** Once WoopSocial is connected, call
`oauth_create_authorization` with the project ID and the platform `YOUTUBE`. It returns a link;
the user opens it, picks the channel, approves, and tells you when they're done. Confirm with
`social_accounts_list`.

Find IDs yourself with `projects_list` and `social_accounts_list`; never ask the user to paste
IDs.

## 3. Upload the video

The video is uploaded through an upload session:

1. `media_uploads_create_session` with `projectId` and `fileSizeInBytes` (the exact size, listed
   in `pack/manifest.json` as `bytes`). Files up to 5 GB; the session splits them into parts.
2. Save the response as `session.json` and run
   `python3 scripts/upload_parts.py session.json final.mp4`.
   It PUTs every part to its presigned URL.
3. `media_uploads_complete_session`. When the status is `READY` it includes the `mediaId`. If
   not, poll `media_uploads_get_session` until it is `READY`; on `FAILED` or `ABORTED`, report it.

Clients with a network allowlist must allow `*.r2.cloudflarestorage.com` for step 2. If the client
can't make HTTP requests at all, hand over the pack instead.

## 4. Validate, confirm, post

`pack/post.json` is the body, built from upload.json. Fill in the two IDs:

```json
{
  "content": [{"text": "<description.txt>",
               "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<media id>"}]}],
  "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-11-03T16:00:00Z"},
  "socialAccounts": [{
    "platform": "YOUTUBE", "socialAccountId": "<youtube account id>",
    "title": "<title>", "privacy": "unlisted",
    "tags": ["<tags>"], "category": "28", "madeForKids": false
  }]
}
```

- `title` and `privacy` are required. `privacy` is `public`, `unlisted` or `private`.
- `category` is optional; the pack writes YouTube's category ID as text ("28" is Science &
  Technology). If `posts_validate` rejects it, try the category name, or leave it out and set it
  in Studio.
- `madeForKids` is a legal declaration. Never guess it: ask.
- Schedule types: `PUBLISH_NOW`, `SCHEDULE_FOR_LATER` (UTC, ISO 8601, in the future), or `DRAFT`
  (saved in WoopSocial only).
- WoopSocial doesn't set the thumbnail, captions, playlist, end screen or the altered-content
  label. `upload-pack.md` lists them for YouTube Studio.

Always:

1. Run `posts_validate` with the exact body. Fix anything it rejects.
2. Show the user the title, the first lines of the description, the thumbnail preview, the
   account, privacy, made for kids and the time with timezone. Wait for a clear yes.
3. `posts_create`, then `posts_get` for the status and the video's URL (`externalPostUrl`).

**A safe first upload** is `unlisted`: the user checks it in Studio, adds the thumbnail and
captions, then makes it public. A video that goes public without its thumbnail loses its first
impressions to a random frame.

## 5. Read results

`social_account_posts_list` returns each post with its latest stored lifetime metrics: views,
likes and comments where YouTube reports them. Collection is asynchronous: report the collection
date with each number, and treat a missing field as "not reported", never as zero. Impressions,
click-through rate, average view duration and retention are only in YouTube Studio (Analytics);
ask the user for them.

## Changing a scheduled post

There's no edit. Delete it with `posts_delete` and create it again, after confirming with the
user. Once it's on YouTube, change the title, description or tags in Studio.

## Links

- Docs: https://docs.woopsocial.com/llms.txt
- MCP tools: https://docs.woopsocial.com/mcp/tools-reference
- WoopSocial: https://woopsocial.com/?utm_source=youtube-skill&utm_medium=skill
- Agent setup: https://woopsocial.com/agents?utm_source=youtube-skill&utm_medium=skill
