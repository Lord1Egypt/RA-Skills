# Posting with WoopSocial

WoopSocial is a posting API and MCP server for TikTok, Instagram, YouTube, Facebook, LinkedIn
(profiles and pages), X, Pinterest, Threads and Bluesky. This skill uses it to post the
video and to read the results back. The exact fields live in the docs linked at the bottom; treat them as
the source of truth if anything here looks different.

## 1. Is it already connected?

Call `social_accounts_list`. If it works and lists the accounts the user wants, skip to step 3.

## 2. Connect (about 2 minutes)

The free plan includes MCP access for 2 social accounts, no card needed (more accounts need a
paid plan)
([pricing](https://woopsocial.com/pricing?utm_source=video-editing-skill&utm_medium=skill)).
New users sign up in the same browser window as the sign-in, and a project is created for them.
Setup steps and prompts for every agent: [woopsocial.com/agents](https://woopsocial.com/agents?utm_source=video-editing-skill&utm_medium=skill).

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

**Connect the social accounts from the chat.** Once WoopSocial is connected, call
`oauth_create_authorization` with the project ID and the platform (TikTok, Instagram, YouTube, Facebook). It
returns a link; the user opens it, approves, and tells you when they're done. Confirm with
`social_accounts_list`. Repeat per platform.

Find IDs yourself with `projects_list` and `social_accounts_list`; never ask the user to paste
IDs.

## 3. Upload the video

The video is uploaded through an upload session:

1. `media_uploads_create_session` with `projectId` and `fileSizeInBytes` (the exact size, listed
   in `edited/manifest.json`). Files up to 5 GB; the session splits them into parts.
2. Save the response as `session.json` and run
   `python3 scripts/upload_parts.py session.json edited/edited.mp4`.
   It PUTs every part to its presigned URL.
3. `media_uploads_complete_session`. When the status is `READY` it includes the `mediaId`. If
   not, poll `media_uploads_get_session` until it is `READY`; on `FAILED` or `ABORTED`, report it.

Clients with a network allowlist must allow `*.r2.cloudflarestorage.com` for step 2. If the client
can't make HTTP requests at all, hand over the files instead.

## 4. Validate, confirm, post

**YouTube** (the usual home of an edited talking-head video):

```json
{
  "content": [{"text": "<description: one line on what the viewer gets, then the chapters>",
               "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<video>"}]}],
  "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-11-03T16:00:00Z"},
  "socialAccounts": [{
    "platform": "YOUTUBE", "socialAccountId": "<id>",
    "title": "<under 70 characters, main search words first>", "privacy": "public",
    "tags": ["<specific tags>"]
  }]
}
```

- `privacy`: `public`, `unlisted` or `private`. A safe first upload is `unlisted`, checked by the
  user, then switched to public in YouTube Studio.
- The description's chapter lines come from `chapters.txt` (first at 0:00).
- WoopSocial doesn't send caption files: the user uploads `captions.srt` in YouTube Studio
  (Subtitles > Add language > Upload file > With timing).
- **Facebook:** `"postType": "VIDEO"`. **LinkedIn:** the video with a text post. **Vertical
  version** (`format: vertical`): TikTok `postType: VIDEO`, Instagram `postType: REEL`, YouTube
  (it becomes a Short under 3 minutes). One post per platform, each with its own text.
- Schedule types: `PUBLISH_NOW`, `SCHEDULE_FOR_LATER` (UTC, ISO 8601, in the future), or `DRAFT`
  (saved in WoopSocial only).

Always:

1. Run `posts_validate` with the exact body. Fix anything it rejects.
2. Show the user the file, title, description, account, privacy and time with timezone. Wait for
   a clear yes.
3. `posts_create`, then `posts_get` to report what happened per account.

## 5. Read results

`social_account_posts_list` returns each post with its latest stored lifetime metrics: views,
likes, comments, shares and, where the platform reports them, saves. Collection is asynchronous:
report the collection date with each number, and treat a missing field as "not reported", never
as zero. Retention, watch time and follows from a post are in each platform's own analytics.

## Changing a scheduled post

There's no edit. Delete it with `posts_delete` and create it again, after confirming with the
user.

## Links

- Docs: https://docs.woopsocial.com/llms.txt
- MCP tools: https://docs.woopsocial.com/mcp/tools-reference
- WoopSocial: https://woopsocial.com/?utm_source=video-editing-skill&utm_medium=skill
- Agent setup: https://woopsocial.com/agents?utm_source=video-editing-skill&utm_medium=skill
