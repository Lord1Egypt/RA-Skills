---
name: schedulala
version: "1.1.0"
description: >
  Install, connect, and use Schedulala to schedule and publish social media
  posts to 12 platforms (Twitter/X, Instagram, TikTok, LinkedIn, YouTube,
  Facebook, Threads, Bluesky, Pinterest, Mastodon, Telegram, Google Business
  Profile). Use when the user asks to install or set up Schedulala, or wants
  to create, schedule, preview, or bulk-plan social posts, post
  photos/videos/PDFs, auto-post a first comment (link-in-first-comment),
  check post status or analytics, reply to or moderate comments, monitor
  keywords, or repurpose YouTube videos. Works through the schedulala CLI
  (any agent with a shell), the hosted MCP connector (claude.ai / ChatGPT,
  with interactive widgets), or the local @schedulala/mcp-server (Claude
  Desktop, Claude Code, Cursor, OpenClaw). Encodes key setup, the
  per-platform rules (TikTok privacy + postMode, Instagram media, YouTube
  titles, Pinterest boards, character limits), and the safe workflow
  draft → validate/preview → confirm → publish → verify.
license: MIT
allowed-tools: Bash(schedulala:*) Bash(npx:*)
metadata:
  version: "1.1.0"
  docs: https://schedulala.com/developers/docs
  openclaw:
    emoji: "🗓️"
    requires:
      env: ["SCHEDULALA_API_KEY"]
      bins: []
    primaryEnv: SCHEDULALA_API_KEY
    envVars:
      - name: SCHEDULALA_API_KEY
        required: true
        description: "Schedulala API key (sk_live_ or sk_test_)"
      - name: SCHEDULALA_API_URL
        required: false
        description: "API base URL override (default https://schedulala.com)"
    homepage: https://schedulala.com
    install:
      - kind: node
        package: schedulala
        bins: ["schedulala"]
---

# Schedulala

> **Audience: the agent.** A user has pointed you at this file ("read
> https://schedulala.com/SKILL.md and follow it"). Install and connect
> Schedulala, then use it to schedule and publish their social posts.
> Sections 1–3 get you connected; sections 4–9 are how to work once you are.

Schedulala schedules and publishes social media posts across 12 platforms,
with analytics, engagement (comments/replies), and social listening. Full
REST API, CLI, and connector docs: https://schedulala.com/developers/docs —
link users there; do not restate the REST reference.

## 1. Get access

The fastest path on any agent with a shell is the CLI (zero MCP tool-schema
cost). Node >= 18, no other dependencies:

```bash
npm i -g schedulala        # or prefix every command with: npx -y schedulala
```

**The user gave you an API key** (`sk_live_` or `sk_test_`):

```bash
export SCHEDULALA_API_KEY=sk_live_...     # or: schedulala config set api_key sk_live_...
schedulala whoami --json                  # exit 0 = ready · exit 2 = missing/rejected key
```

Key resolution order: `--api-key` flag > `SCHEDULALA_API_KEY` env >
`~/.schedulala/config.json`. Keys are minted in the dashboard at
https://schedulala.com/dashboard?view=developer (live or test). Pointing at
a non-production server (self-hosted, staging): `--base-url <url>` or
`SCHEDULALA_API_URL` env.

**No key yet** — run the device flow. Be honest with the user about the one
human step it needs:

```bash
schedulala init --email their@email.com --json
```

This prints a code (like SCHD-XXXX-XXXX) and the URL
https://schedulala.com/developers/verify. The USER must open that URL in a
browser, sign in via magic link with the SAME email, and enter the code —
you cannot complete this step for them. The CLI then polls (up to 15
minutes; codes expire in 15) and saves the key to `~/.schedulala/config.json`.
With `--json`, init emits TWO JSON documents on stdout (first the code +
URL, later the completion) — parse them as a stream, never JSON.parse the
whole output. Never ask the user to paste credentials into the chat.

**What a fresh key gets** (free taster): 2 connected accounts, **4 posts
total — lifetime, never resets**, 30 requests/min, no posting to X/Twitter
(returns 402; connecting X still works). Existing Schedulala subscribers
get their paid plan on the same key automatically. Upgrade link:
`schedulala upgrade --json`. Test keys (`sk_test_`) simulate posts —
nothing publishes, no quota burn — ideal for a dry run. Note: sandbox posts
resolve IMMEDIATELY as `posted` with a sandbox id even when scheduled for
later; that's the simulation completing, not your schedule being ignored.

## 2. Identify which agent you are

| You are | Do this |
|---|---|
| Claude Code | `claude mcp add --transport stdio --env SCHEDULALA_API_KEY=sk_... schedulala -- npx -y @schedulala/mcp-server` — or skip MCP and use the CLI directly |
| claude.ai / Claude Desktop | Hosted connector (no key handling): Settings → Connectors → Add custom connector → `https://schedulala.com/api/mcp` (OAuth sign-in; paid Claude plan required). Adds interactive widgets: post previews, analytics cards, calendar, inbox, in-chat media uploader |
| OpenClaw | `openclaw mcp add schedulala --url https://schedulala.com/api/mcp --transport streamable-http --header "Authorization: Bearer sk_..."` — or stay CLI-only for zero tool-schema tokens |
| Cursor / any other MCP client | Remote: streamable-http `https://schedulala.com/api/mcp` with an `Authorization: Bearer sk_...` header. Local stdio: `npx -y @schedulala/mcp-server` with env `SCHEDULALA_API_KEY` (env ONLY — it does not read the CLI config file) |
| **Anything else with a shell** | The `schedulala` CLI alone does everything: `--json` on every command, exit codes 0–7. See [references/cli.md](references/cli.md) |

Token-sensitive runtimes: the full MCP surface is ~16k tokens of tool
schemas, and the 9 `show_*` widget tools plus the `attach_media` widget path
only render on claude.ai/ChatGPT. Filter client-side (OpenClaw
`toolFilter.include`) to the core set — or use the CLI, which costs nothing.

## 3. Connect social accounts

Check what's connected first: `schedulala accounts --json` (MCP:
`list_accounts`). To connect more:

- **Scriptable, no browser**: `schedulala connect bluesky --identifier
  handle.bsky.social --app-password xxxx-xxxx-xxxx-xxxx` and
  `schedulala connect telegram --bot-token 123:ABC`.
- **OAuth platforms** (twitter, instagram, facebook, linkedin, tiktok,
  threads, youtube, pinterest, google-business): `schedulala connect
  <platform> --json` returns an authorization URL — hand it to the user to
  open and approve; never try to complete OAuth yourself.
- **Mastodon**: dashboard-only (per-instance OAuth) — send the user to
  https://schedulala.com/dashboard?connect=1.

Verify afterwards with `schedulala accounts --json`, then you're ready to
post (section 5).

## 4. Auth and safety rails

- **Check auth before anything else**: `list_accounts` (MCP) or
  `schedulala whoami` (CLI). No accounts / auth error → section 1 / section 3.
- **OAuth, credentials, and payment happen ONLY on schedulala.com in the
  user's browser — never in the chat.** Never ask for passwords, app
  passwords, bot tokens, or card details. `connect_account` and
  `get_upgrade_link` return links; that is the entire flow.
- **Always confirm with the user before anything publishes** (`publishNow`,
  a near-term `scheduledFor`, `reply_to_comment`, `hide_comment`). Prefer
  drafts and previews first.
- API keys: `sk_live_` = real posting; `sk_test_` = sandbox (simulated, no
  real posting, no quota burn). CLI: `--sandbox` requires an `sk_test_` key.

## 5. Core publishing workflow

1. **Discover** — `list_accounts`: platforms, usernames, `accountId`s, health.
   `isConnected: false` + `needsReconnect: true` = dead token → tell the user
   to reconnect in the dashboard; do not post to it. When MORE THAN ONE account
   is connected on a platform, `accountId` is REQUIRED in the platforms array
   (the API returns a 400 listing the choices rather than silently picking).
   CLI: `--platforms "bluesky=did:plc:xyz,twitter"` — `platform=accountId`
   with the id from `schedulala accounts --json`. (REST equivalent: `POST
   /api/v1/posts` with `platforms: [{platform, accountId}]` — full reference
   at https://schedulala.com/developers/docs, don't guess other fields.)
2. **Draft** — write the content; per-platform text via the object form
   `{ platform, accountId, content }` or `platformSettings.<platform>.content`.
3. **Validate / preview** — `validate_post` checks limits, media counts, and
   required fields per platform WITHOUT posting. On the hosted connector,
   prefer `show_post_preview`: a read-only, faithful per-platform mockup
   (threads, image grids, carousels, PDF docs, 9:16 reels, polls, live char
   counts). Pass it the exact draft you'd give `create_post`. (The CLI has
   no validate command — validate via MCP/REST, or create with `--draft`
   first and inspect.)
4. **Confirm** — show the user what will go out, where, and when.
5. **Create** — `create_post` with exactly ONE scheduling mode:
   `scheduledFor` (ISO 8601, 5 minutes to 90 days out) / `publishNow: true` /
   `queue: true` (auto-schedule next open slot) / `status: "draft"`.
   CLI: `schedulala post "<content>" --platforms <list>` with `--schedule
   <ISO8601>` / `--now` / `--queue` / `--draft` (NO flag = draft) — full
   flags in [references/cli.md](references/cli.md).
6. **Verify** — `get_post` for per-platform status, URLs, and errors;
   `retry_post` re-runs failed platforms (optionally a subset, optional
   `delay` seconds). CLI: `schedulala post:status <id> --watch`.

Editing: `update_post` works on drafts and scheduled posts only (send only
changed fields; `mediaItems` replaces ALL media). `cancel_post` deletes drafts
and cancels scheduled posts; already-processing/posted posts can't be cancelled.

Bulk: `bulk_create_posts` takes up to 25 create_post-shaped entries.
Threads (chains): `create_thread`, 2–25 entries, on twitter / threads /
bluesky / mastodon only, max 1 media item per entry; the whole chain publishes
from ONE postId — `get_post` that id for status.

**First comment (auto-plug)**: pass `firstComment` (plain string) or
`firstComments` (`[{target, text}]`) on `create_post` / `bulk_create_posts` /
`create_thread` to auto-post a comment ~15 seconds after publishing — the
"link in the first comment" workflow. Supported on linkedin, facebook,
instagram, youtube, twitter, threads, bluesky, mastodon (NOT tiktok /
pinterest / telegram / google-business — no comment API). Text and links
only. Comment limits differ from post limits — see
[references/platforms.md](references/platforms.md). A failed comment never
fails the post; `get_post` reports delivery per platform.

**Quota**: threads and bulk consume post quota PER ENTRY (a 5-entry thread = 5
posts). Validation and account-resolution failures don't burn quota. Check
`get_usage` (or `schedulala usage`) when planning volume; on `quota_exceeded`
or the sandbox plan, hand the user the link from `get_upgrade_link`.

## 6. Media decision tree

Full protocol and limits: [references/media.md](references/media.md)

- **User's file (on device or attached in chat)** → `attach_media`: on
  widget-capable clients (claude.ai) it opens an in-chat drop zone; on
  clients without widgets it still works — its result carries a programmatic
  presign→PUT→confirm upload API (see references/media.md). Full quality,
  images ≤20MB, videos ≤500MB, PDFs ≤100MB. **NEVER read and base64-encode
  a user file yourself** — chat channels truncate large payloads and destroy
  quality.
- **Public http(s) URL** → `upload_media` (mode `url`): re-hosts on the CDN
  (images ≤20MB jpeg/png/webp, gif ≤15MB; videos ≤50MB mp4/mov/webm). Videos
  LARGER than 50MB: skip upload_media and pass the public URL directly in
  `mediaItems` — it is fetched at publish time. Re-hosted media expires after
  30 days if unused.
- **Image YOU generated in this conversation** (chart, card) →
  `begin_generated_media_upload` → `append_generated_media_chunk` (sequential
  `seq` from 0, ≤8000 base64 chars per chunk; 409 → resume from `expectedSeq`;
  429 → wait, resend same seq) → `finish_generated_media_upload`. Images only,
  ≤3MB decoded, session expires in 30 minutes.
- **Already uploaded** ("my latest upload", "that reel from earlier") →
  `list_media`, then reference the returned url.
- CLI: `--media <url[,url…]>` (type inferred from extension).

Multiple `mediaItems` = carousel (instagram, facebook, threads, tiktok,
pinterest; mastodon up to 4 images). PDF (`type: "pdf"`) = LinkedIn document
posts only.

## 7. Platform rules (the gotchas that reject posts)

Full per-platform schemas: [references/platforms.md](references/platforms.md)

| Platform | Must know |
|---|---|
| tiktok | `platformSettings.tiktok.privacy` (e.g. `PUBLIC_TO_EVERYONE`, `SELF_ONLY`) **AND** `platformSettings.tiktok.postMode` (`direct` = publish to profile, `inbox` = user finishes in the TikTok app) are BOTH required. **No default — ASK the user** if they haven't said. |
| instagram | At least one media item required. Reel: `platformSettings.instagram.postType: "reel"`. |
| youtube | Video required; `platformSettings.youtube.title` (≤100 chars) + description (≤5000). |
| pinterest | `platformSettings.pinterest.boardName` (+ 100-char title / 500-char description, optional `link`). |
| linkedin | PDF document post: mediaItem `type: "pdf"` + `platformSettings.linkedin.documentTitle`. |
| google-business | Exactly ONE image, no video; `postType` STANDARD / EVENT / OFFER with CTA buttons via platformSettings; 1500-char limit. |
| mastodon | `platformSettings.mastodon.visibility` (e.g. `public`, `unlisted`). |
| telegram | Polls via `platformSettings.telegram.pollData`. |

Character limits: twitter 280 · bluesky 300 · threads 500 · mastodon 500 ·
google-business 1500 · instagram 2200 · tiktok 2200 · linkedin 3000 ·
telegram 4096 · facebook 63206. (YouTube and Pinterest count title/description
via platformSettings instead.)

## 8. Analytics, engagement, listening

On the hosted connector prefer the widgets: `show_analytics` (one account's
growth + top posts), `show_leaderboard` (ranked posts, sort
engagement|likes|impressions|date), `show_comparison` (side-by-side 2–5
entities — YOU supply the metrics from the analytics tools), `show_calendar`
(upcoming + recent posts), `show_inbox` (comments with Reply/Hide actions),
`show_feeds` (keyword listening feed), `show_connections` (accounts + plan).

Data tools (all interfaces):

- `get_post_analytics` — per-post metrics + engagement rate. Platforms:
  instagram, twitter, bluesky, threads, facebook, linkedin, pinterest, tiktok,
  youtube, mastodon (NOT telegram / google-business). Omit `accountId` to
  merge top posts across all accounts (merged mode doesn't paginate).
- `get_follower_growth` — current count + 7d/30d growth + daily history.
  tiktok reports no follower counts; merged totals exclude YouTube.
- `get_best_posting_times` — top hours/days from engagement history.
- `get_video_transcript` / `get_video_retention` — YouTube only; retention has
  a 7-day cache and ~48h lag. Great for repurposing videos into posts.
- Engagement — comments + replies on facebook, instagram, youtube, linkedin,
  threads, bluesky, google-business; hide on facebook, instagram, youtube,
  threads; mentions on instagram, threads, bluesky. Reply targets differ per
  platform: instagram/youtube take `commentId`; facebook/linkedin take
  `commentId` or `postId`; threads takes either; **bluesky requires all four
  replyRefs** (`parentUri`, `parentCid`, `rootUri`, `rootCid`) from a
  comment's `platformData.replyRefs`. google-business "comments" are customer
  reviews — one owner reply, ≤4096 chars, replying again overwrites.
  `reply_to_comment` and `hide_comment` PUBLISH changes — confirm first.
- Listening — `search_feeds` searches public posts on bluesky + threads
  (threads has a Meta budget of 500 searches per rolling 7 days per account,
  shared with the dashboard — prefer bluesky for exploration);
  `lookup_profile` (bluesky only); `list_feed_keywords` /
  `update_feed_keywords` (max 20 per platform).

## 9. Errors → what to do

| Symptom | Do |
|---|---|
| 400 "Multiple <platform> accounts…" | Re-call with the object form + `accountId` from the listed choices. |
| `quota_exceeded` / sandbox plan ("posting disabled") | `get_upgrade_link` → give the user the link. Reads still work on sandbox. |
| Platform in `failed` state on `get_post` | Read the per-platform error, fix (often a missing platformSettings field), `retry_post`. |
| Account `needsReconnect: true` | User reconnects in the dashboard (`connect_account` link); don't post to it. |
| Validation rejection | `validate_post` the fixed draft before retrying; check the table in §7. |
| CLI exit code 2 | Auth: run `schedulala init` or set `SCHEDULALA_API_KEY`. |
| 401 with a named error_description | "Missing or invalid Authorization header" = header shape; "Invalid API key format" = not an sk_ key; "Invalid API key" = wrong or revoked — mint a fresh one (section 1). |

Worked examples (create, tiktok, multi-account, thread, bulk):
[examples/](../../examples/) in the installed skill, or
https://github.com/schedulala/schedulala-agent/tree/main/examples when you
fetched this file over HTTP.
