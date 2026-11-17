# Publishing reference

Full tool reference for the Socialync MCP server, plus the failure modes that
matter when an agent is posting with the user's approval.

## Connecting

The server is a remote streamable-HTTP MCP endpoint at `https://mcp.socialync.io/mcp`,
authenticated with OAuth 2.1 using dynamic client registration.

```bash
openclaw mcp add socialync \
  --url https://mcp.socialync.io/mcp \
  --transport streamable-http \
  --auth oauth
openclaw mcp login socialync
openclaw mcp probe socialync
```

If the browser cannot reach the address OpenClaw prints, copy the code from the
address bar of the page that failed to load and run
`openclaw mcp login socialync --code YOUR_CODE`.

The user signs in with their Socialync account in a browser window. No API key
is pasted into the client. The same endpoint works in Claude, Claude Code,
Cursor, ChatGPT, Gemini CLI, Codex or any MCP client, and the connection can be
revoked from Socialync account settings at any time. A client that cannot open a
browser can send `Authorization: Bearer <key>` with a key from
https://www.socialync.io/api-keys.

Do this once, at the point of publishing. Nothing in Stage 1 of the skill needs
it. Planning, drafting, per-platform formatting and calendar building all work
with no account and no connection.

Posts publish only through social accounts the user already authorized inside
Socialync. If the sign in has not happened or has been revoked, say so plainly
and point the user at the connect step. Never fall back to drafting and imply
the post was scheduled.

MCP access is included on the free plan. A user can sign up for $0 with no
credit card and start publishing, 5 posts per calendar month on every platform
except X (X needs a paid plan), reset on the 1st. One publish counts as one post however many
platforms it targets, so a five-platform cross-post costs one of the five. Paid
plans start at $20 a month at https://www.socialync.io/pricing and remove the
monthly cap. Scheduling goes up to 2 months ahead on free, 12 on paid. Read the
live numbers from `check_quota` instead of assuming them.

## Tools

**Discovery and preflight**

- `list_profiles`: every profile this connection can manage, with id, name,
  default flag and connected platform count. Call first. Pass the chosen id as
  `profileId` on every write.
- `list_connections`: connected platforms for a profile with connection health.
  Check before drafting against a platform. `requiresReconnect: true` means
  leave it out and tell the user.
- `check_quota`: plan, remaining posts, `maxPostsPerProfilePerDay`,
  `maxScheduleMonths`, `aiContentGeneration` and supported platforms. Call
  before every batch.
- `validate_post`: the same checks Socialync's own scheduler enforces, per
  platform, without submitting anything: caption length, link count, media type
  and count, image aspect ratio, video duration and account health. Call it
  before every publish with the exact arguments you will send.

**Writing**

- `publish_now`: text or images, live now, after a yes in chat.
- `publish_scheduled`: any media including video, at a future time, after a yes.
- `create_post_draft` and `schedule_post_draft`: hold a post as a draft
  until the user says yes in chat; `approve_draft` then sends it. The user
  never opens the Socialync app for this. Unapproved drafts expire after 24 hours.
- `get_draft_status`: poll a draft that is still processing.
- `approve_draft`: publish a pending draft the user just approved in chat.
- `create_x_article_draft` and `publish_x_article_now`: long-form X Articles
  with a headline. The connected X account needs X Premium.
- `generate_content`: Socialync's AI captions, paid plans only. On free, write
  the text yourself.

**Changing the calendar**

- `get_scheduled_posts`: the calendar. Always read back after writing.
- `update_scheduled_post`: change a scheduled post in place before it fires:
  the time, the caption for every platform or one, the YouTube title, the first
  comment, or drop platforms. Pass a `groupId` to change every platform
  together. Prefer it over delete and recreate; it keeps the media and settings.
- `delete_scheduled_post`: cancel one platform by `postId` or the whole post by
  `groupId`.

**Media**

- `create_media_upload` then `finalize_media_upload`: two steps. Media has to be
  finalized before it can attach to a post. An image batch becomes one carousel
  in upload order.
- `list_media`: assets the user already uploaded in Socialync. The normal path
  for video: the agent cannot receive a video file in chat, so the user uploads
  it in Socialync (start a post, add the video, leave the page) and the agent
  finds it here. Uploads not attached to a post are removed about 12 hours
  later, so schedule them in the same session.

**Reading back**

- `get_post_history`: what already shipped, with per-platform success and
  failure. Also the correct way to check for duplicates before a retry.
- `get_analytics`: reach and engagement per platform. Socialync collects
  analytics for TikTok, YouTube, Instagram, Facebook, Threads and Bluesky on paid
  plans. X and LinkedIn analytics are not available.
- `get_top_posts`: best performers, for pattern-matching the next batch.
- `get_post_insights`: one post in depth, including the retention curve.
- `get_best_times`: the days and times the user's own posts got the most
  engagement, per platform, in their time zone.
- `get_comments`: comments on one published post, with replies, on Instagram,
  YouTube, Threads, LinkedIn Company Pages and Bluesky.
- `reply_to_comment`: reply as the user's account on Instagram, Threads,
  LinkedIn Company Pages or Bluesky. Public and immediate, one at a time, after
  the user has seen the comment and the exact reply. 30 replies a day. YouTube
  and X replies are sent by the user in the Socialync app.
- `list_audiences`: audience segments where configured.

## Platform rules at draft time

- TikTok and YouTube go only through the scheduled tools. YouTube takes video
  only and needs `title`. TikTok takes one video or a photo post of images.
- Instagram needs an image or a video. A video publishes as a Reel.
- Images: up to 10 per post. X and Bluesky publish at most 4, LinkedIn 9.
- Different text per platform: shared text in `caption`, a platform's own
  version in `platformSpecificSettings`, for example
  `{ "twitter": { "customCaption": "..." } }`. Platform keys: `facebook`,
  `instagram`, `tiktok`, `youtube`, `linkedin`, `twitter`, `threads`, `bluesky`.
- `firstComment` posts a comment under the post right after it publishes, a
  good home for links and hashtags. Instagram, Threads, X, YouTube, LinkedIn and
  Bluesky support it. Keep it under 280 characters when X is in the post.
- TikTok needs the user's own choice of audience, passed as
  `tiktokPrivacyLevel` (`PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`,
  `FOLLOWER_OF_CREATOR` or `SELF_ONLY`). Sounds cannot be chosen through the
  API, so a video's audio has to be in the file.
- X needs a paid Socialync plan. Pinterest is not available through MCP.
- `scheduledFor` is ISO 8601 in UTC, for example `2026-11-04T22:00:00Z`. Ask
  for the user's timezone once, show times in it, convert when you call.

## Failure handling

**Duplicate posts are the number one agent failure.** A network timeout on
`publish_now` does not mean the post failed. The response was often lost after
the post succeeded. Socialync blocks duplicate publishes, and failed posts are
retried automatically. Even so, call `get_post_history` or
`get_scheduled_posts` first and confirm the post is absent before trying again,
so you report the truth to the user.

**A failed post carries `error.action`.** `reconnect`: tell the user which
account to reconnect in Socialync Settings. `edit_post`: fix the content and
show it again. `retry` or `wait_and_retry`: offer to schedule it again later.

**Quota exhaustion mid-batch** leaves a half-published week. Read
`maxPostsPerProfilePerDay` and `postsRemaining` from `check_quota` and plan the
whole batch against them before the first write. The daily cap keeps automated
posting under the spam thresholds Meta, X and LinkedIn use. Offer another day.

**Monthly allowance used up on the free plan:** say in one sentence that it
resets on the 1st and that paid plans start at $20 a month. Say it once.

**A disconnected platform fails at publish time.** Check `list_connections`
during planning so the user reconnects before a scheduled post fails days later.

**Schedule horizon is bounded.** `check_quota` returns `maxScheduleMonths`.
Clamp the calendar to it and tell the user rather than letting writes fail.

## Confirmation policy

Draft, show, ask, then send. Show the user what will go out, on which platform,
at what time, and wait for a clear yes: "yes", "post it", "schedule all 5",
"approve 1, 2 and 4". A question, a "looks good so far" or silence means wait.
Any edit resets the yes. Publishing to a real audience cannot be undone in any
meaningful sense; a deleted post has already been seen.

There is no auto-approve mode and no exception for recurring schedules. If the
user asks to post without checking each time, say that Socialync needs a yes
for each post, and offer to prepare the whole week in one numbered message so a
single reply approves it. Socialync records who approved each post and when,
and it publishes the exact content that was approved.
