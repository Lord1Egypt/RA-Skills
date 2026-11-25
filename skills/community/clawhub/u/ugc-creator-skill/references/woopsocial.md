# Posting with WoopSocial

WoopSocial is a posting API and MCP server for TikTok, Instagram, YouTube and other networks. This
skill uses it to post a campaign batch to several accounts in one request, one video and caption per
account, and to read back each post's link and numbers. It posts through each platform's own API
with WoopSocial's approved apps, so the user needs no developer app or app review of their own;
their accounts authorize WoopSocial to post for them. TikTok makes posts from unaudited developer
apps private, which is why creators who build their own posting end up with posts nobody sees. The
exact fields live in WoopSocial's API docs and MCP schema (`schema_describe`); treat them as the
source of truth if anything here looks different.

WoopSocial posts what the agent sends. It doesn't write captions, edit videos or change files.

## 1. Is it already connected?

Call `social_accounts_list`. If it lists the accounts the user named with status `CONNECTED`, skip
to step 3. `DISCONNECTED` needs connecting again.

## 2. Connect

The free plan covers 2 social accounts, no card:
[app.woopsocial.com/signup](https://app.woopsocial.com/signup?utm_source=ugc-creator-skill&utm_medium=connect).
Give this link at the start, so the user signs in while they film.

**Count the accounts first.** A UGC creator with TikTok, Reels and Shorts has 3 accounts, and a brief that wants a dedicated account adds more. Say it before
connecting: 2 through WoopSocial and the rest by hand from their `by-hand/` pages, all of them on a
paid plan ([pricing](https://woopsocial.com/pricing?utm_source=ugc-creator-skill&utm_medium=skill)),
or all by hand. Never drop an account silently, and never suggest upgrading for anything but
posting to more accounts.

Setup for every agent: [woopsocial.com/agents](https://woopsocial.com/agents?utm_source=ugc-creator-skill&utm_medium=skill).
Give only the path for the agent you're running in:

| Agent | How to connect |
|---|---|
| Claude (claude.ai, Desktop, Cowork) | Add WoopSocial from the [Claude directory](https://claude.ai/directory/woopsocial), click Connect and sign in |
| Cursor | Install from [cursor.directory](https://cursor.directory/plugins/woopsocial-social-media-scheduler) and sign in |
| Claude Code | `claude mcp add --transport http woopsocial "https://api.woopsocial.com/mcp"`, then restart with `claude --continue` (keeps the conversation), `/mcp`, select woopsocial, Authenticate |
| Codex | `codex mcp add woopsocial --url https://api.woopsocial.com/mcp`, then `codex mcp login woopsocial`, then start a new session (`codex resume --last` keeps this one) |
| OpenClaw | Install the [WoopSocial skill on ClawHub](https://clawhub.ai/woopsocial/skills/social-media-scheduler), or add the MCP URL to the agent's MCP config |
| Agents without sign-in support | Create an API key at [app.woopsocial.com/api-access](https://app.woopsocial.com/api-access) and use `https://api.woopsocial.com/mcp?api_key=YOUR_API_KEY` |

The API key is a password: never paste it into shared chats or commit it. Claude Code and Codex
load new tools only in a new session, and a restart stops a running script: never add the
connection or restart while `make_video.py` runs. Everything is saved in the project folder, so
after signing in the user says "continue".

Account rules to say before connecting: Instagram posting needs a Business or Creator account
(free to switch in the Instagram app). All accounts in one request must be in the same WoopSocial
project.

**Connect every account in one pass.** `projects_list`, then `oauth_create_authorization` for each
missing platform, all links in one message. When they're done, `social_accounts_list` once and put
each `socialAccountId` in `job.json`. Never ask the user to paste ids.

## 3. Read each TikTok account's limits

`social_accounts_get_platform_inputs` returns the audiences the account offers
(`privacyLevelOptions`), whether comments, duets and stitches are available, and its maximum video
length. Copy them into the account as `privacyOptions` and `max_video_s`. The choices themselves
are the user's.

## 4. Upload each video once

Only after the user said yes to the plan and `plan.py job.json --yes <plan id>` recorded it. The yes
holds for 3 hours; after that, show the plan again. For every file under "Files to upload" in
`plan.md`, one at a time:

1. `media_uploads_create_session` with `projectId` and `fileSizeInBytes` (the exact byte size).
2. Save the response as `session.json`, as it came back, and run
   `python3 <skill>/scripts/upload_parts.py session.json <video>`. It refuses a file that no fresh
   yes covers, tries each part three times, prints the file's sha256 when done, records the upload
   in `uploaded.json` next to the video, and says in one line what to do when it can't go on.
   `plan.py --media` accepts only files recorded there.
3. `media_uploads_complete_session`. When the status is `READY` it includes the `mediaId`; if not,
   poll `media_uploads_get_session`; on `FAILED` or `ABORTED`, report it. Save the READY reply as
   `reply.json` and run `python3 <skill>/scripts/upload_parts.py --complete reply.json <video>`: it
   records the mediaId against that file and its upload session. `plan.py --media` refuses a
   mediaId that isn't recorded for its file, and `--check` rebuilds each request's media ids from
   these records, so a mediaId can't be moved to another video.

Save `{"<video as plan.md lists it>": {"mediaId": "<mediaId>", "sha256": "<the sha256 upload_parts.py printed>"}}`
as `media.json` and run
`python3 <skill>/scripts/plan.py job.json --media media.json`. It writes requests only while the
yes holds for exactly these files and captions. A video that changed after its upload (edited
again under the same name) is refused: upload the new file, update media.json, and show
the plan for a new yes. Upload one file at a time:
parallel uploads on one key can get HTTP 429. Clients with a network allowlist must allow
`*.r2.cloudflarestorage.com`.

## 5. One request, a child per account

`plan.py` writes one body per round to `requests/`: one post, one child per connected account, each
with its own video and caption in `contentOverride`, and `requests/index.json` with the plan id
and each body's fingerprint. With `"stagger": true` in job.json it writes one body per account
instead, so each post goes out, gets its in-app step and is submitted before the next. Older
requests move to `requests-old/<plan id>/`.

```json
{
  "content": [{"text": "<first caption>", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<video 1>"}]}],
  "schedule": {"type": "PUBLISH_NOW"},
  "socialAccounts": [
    {"platform": "TIKTOK", "socialAccountId": "<id>", "postType": "VIDEO", "postMode": "DIRECT_POST",
     "privacyLevel": "PUBLIC_TO_EVERYONE", "allowComment": true, "allowDuet": false, "allowStitch": false,
     "isYourBrand": false, "isBrandedContent": true, "autoAddMusic": false, "isAiGeneratedContent": false,
     "contentOverride": [{"text": "#ad ...", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<video 1>"}]}]},
    {"platform": "INSTAGRAM", "socialAccountId": "<id>", "postType": "REEL", "isAiGeneratedContent": false,
     "contentOverride": [{"text": "#ad ...", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<video 2>"}]}]},
    {"platform": "YOUTUBE", "socialAccountId": "<id>", "title": "<title>", "privacy": "public",
     "madeForKids": false, "tags": ["<tag>"],
     "contentOverride": [{"text": "#ad ...", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<video 3>"}]}]}
  ]
}
```

- `PUBLISH_NOW` always: the 30-minute submission window starts when each post is live.
- The request is validated as a whole: if one account's part is invalid, nothing is created.
- TikTok: WoopSocial requires `platform`, `socialAccountId`, `postType`, `allowComment`,
  `allowDuet`, `allowStitch`, `isYourBrand`, `isBrandedContent` and `autoAddMusic` on every TikTok
  child. `privacyLevel` is the user's choice from the account's options. `isBrandedContent` is
  TikTok's "Paid partnership" label: always `true` on a campaign post (and it can't be
  `SELF_ONLY`), with `isYourBrand: false` ("Your brand" is for promoting your own business, not a
  paid campaign). `autoAddMusic` is always `false`: music is the creator's declared choice, never added.
  `isAiGeneratedContent` is `true` only when realistic AI-made scenes or voices are in the video (the
  skill never makes a person; an AI voiceover would need it).
- YouTube: `title` and `privacy` are required; `madeForKids` is the owner's declaration. `category`
  is optional; the skill leaves it out so YouTube picks it.
- WoopSocial can't set these, so the plan and `submit.md` list them as steps in the app:
  Instagram's paid partnership label and YouTube's paid promotion box (inside the 30 minutes),
  YouTube's "altered or synthetic content" answer (only when it applies). A brief that requires a
  sound from an app's library can't be posted through any API: that post goes out by hand.
- Send each request as `plan.py` wrote it. It rewrites `requests/` on every run; change
  `job.json` instead. An edited request, or one written for a plan that has changed since, is refused
  by `--check` and `--posted`.

Always, in this order:

1. The user has said yes to the plan id on `plan.html` or `plan.md`, and
   `plan.py job.json --yes <plan id>` recorded it. Nothing is uploaded before that.
2. Upload (section 4), then `plan.py job.json --media media.json`.
3. Right before sending: `plan.py job.json --check requests/<name>.json`. It refuses a request that
   was edited, or whose files, captions or settings changed after the yes.
4. `posts_validate` with each exact body. If it forces a change, fix `job.json`, plan again,
   show the new plan and wait for a new yes.
5. `posts_create`, then at once `plan.py job.json --posted requests/<name>.json <postId>`. A post
   that went out is always recorded, also when something changed after the check (it says what).
   A checked request that was never sent: `plan.py job.json --not-sent requests/<name>.json
   --checked` after looking at `social_account_posts_list`.
6. `posts_get` with the post id: `socialAccountPosts` has one entry per account with its
   `deliveryStatus` and, once live, its `externalPostUrl`. Save the reply as `status.json` and run
   `plan.py job.json --status status.json <postId>` (the post id is read from the reply when it
   holds one; a reply for another post or account is refused). Report each account in plain words (live with its
   link, still processing, or failed and why) and read the submission sheet out: the deadline per
   post and the steps to do before it. Ask the user to open each link once and check it looks
   right (public, sound on, the label showing).

## 6. Numbers for the proof log

`social_account_posts_list_analytics` (filter by account, platform or project, and a publish-date
range of up to 366 days) returns per post its `externalPostUrl`, `deliveryCompletedAt`, lifetime
`metrics` and `metricsCollectedAt`. Save the reply and run `ledger.py --proof <file>`.

- Collected about once a day; reading doesn't refresh.
- `views`: plays on TikTok and YouTube; times shown (repeats included) on Instagram.
- Not verified yet: TikTok per-post views through this call, whether posts made outside WoopSocial
  show up, and how soon after posting the first numbers appear. If a post has no numbers yet, try
  again the next day.

The skill reads views per post from this call and nothing else; the campaign's own count decides
what is paid.

## Nothing goes out twice

- `plan.py` leaves every post recorded in the ledger (`~/.ugc-creator/ledger.json`) out of new
  requests.
- **Not sure a post went through:** read the ledger, call `posts_get` for the recorded post id.
  If the session ended between `posts_create` and `--posted`, call `social_account_posts_list` for
  each account in that request and look for it before anything else. Never create it again to find
  out: a second post of the same video is a duplicate the campaign can reject.
- **One account failed** (`deliveryStatus` says so, and the post has no link): say why in plain
  words and fix the cause with the user. A failed delivery can still have published on the
  platform: call `social_account_posts_list` for that account and look at the last hour. Only when
  the video isn't there, `plan.py job.json --failed <job post id> --checked` takes that one
  post out of the ledger, and the next plan puts it in a new request. Show the plan, wait
  for a new yes. Only a post whose saved status says it failed is released: a post still processing
  can go live minutes later, and one that is live, has a link or was submitted is never released.

## Links

- Docs: https://docs.woopsocial.com/llms.txt
- MCP tools: https://docs.woopsocial.com/mcp/tools-reference
- WoopSocial: https://woopsocial.com/?utm_source=ugc-creator-skill&utm_medium=skill
