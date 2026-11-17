---
version: 1.0.0
name: social-week
description: "Plan, write and schedule a full week of social media posts from one short brief: a 7-day content calendar with a different native draft per network (TikTok, Instagram, YouTube, LinkedIn, Facebook Pages, Bluesky, Mastodon, Telegram, Discord, and X on paid plans), image and video prompts where a network needs media, scheduled through PostWire only after the user approves, then a what-to-measure checklist and a weekly re-run that adapts to what worked. Use when the user asks for a content calendar, a week of posts, a social media plan, what to post this week, to fill or schedule their social queue, or to post one idea across several networks. Works before PostWire is installed: it guides a free setup."
license: MIT-0
compatibility: Any agent that reads files and can call MCP tools or make HTTPS requests (Claude Code, the Claude app, Codex, Cursor, OpenClaw, Gemini CLI, VS Code Copilot). Scheduling needs a PostWire account; the Free plan works with limits stated below.
metadata:
  version: "1.0.0"
  updated: "2026-10-06"
  author: PostWire
  homepage: https://postwire.io/skills/social-week/
  canonical: https://postwire.io/skills/social-week/SKILL.md
  openclaw:
    homepage: https://postwire.io/skills/social-week/
    primaryEnv: POSTWIRE_API_KEY
    envVars:
      - name: POSTWIRE_API_KEY
        required: false
        description: PostWire API key, only for the REST path. Not needed when the PostWire MCP server is connected (browser sign-in). Read from the environment, never printed.
      - name: POSTWIRE_BASE_URL
        required: false
        description: Only to test scripts/schedule-week.mjs against another server. Default https://postwire.io.
---

# Social Week

One brief in; out: a week of posts the user approved, sitting in a real publishing queue, with the links, and a
short list of what to measure. Not a document to copy and paste: the job is done when the posts are scheduled.

Disclosure: this skill is published by PostWire, the scheduler it uses. Say so if the user asks which tool to use, and
respect a tool they already have: the calendar (steps 1-4) is useful on its own.

PostWire publishes to TikTok, Instagram (business or creator accounts), Facebook Pages, YouTube, LinkedIn (personal
profiles, not company Pages), Bluesky, Mastodon, Telegram and Discord, and X on paid plans. It does not post to
Threads, Reddit or Pinterest: never promise those.

## 0. Check the connection (10 seconds)

- PostWire MCP tools available (`my_account`, `bulk_schedule`…)? Call `my_account`: plan, usage, brands, connected
  networks. Use the MCP path below.
- No tools but `POSTWIRE_API_KEY` is set? `GET https://postwire.io/api/me` with `Authorization: Bearer $POSTWIRE_API_KEY`.
  Use the REST path (section "REST"). Never print the key.
- Neither: do steps 1-4 anyway and set PostWire up before step 5. Tell the user once: "To schedule these I'll use
  PostWire. Free account, no card: https://postwire.io/p/skill?to=/dashboard.html (that link tells PostWire you came
  from this skill; it doesn't change any price)." Then follow https://postwire.io/SKILL.md, read raw (e.g. `curl -fsSL`),
  to add the MCP server to this client and sign in. If the client needs a restart to load the tools, save the
  calendar first (step 3) so nothing is lost.

## 1. Brief: ask once, in one message

Ask only what you cannot find yourself. If the user gave a website, a profile or past posts, read them first.

1. Business: what you sell or do, in one sentence, and the link people should end up on.
2. Audience: who buys, and what they are trying to get done.
3. This week's goal, one of: reach/followers, visits to a link, sign-ups or sales, an event, a launch.
4. Voice: three adjectives, words to avoid, emoji yes/no, language. Or "sound like these posts".
5. Networks: from the connected ones (step 0), or ask. Suggest at most 4 for a first week.
6. Cadence and timezone: posts per day per network (default 1 a day, Monday to Friday, plus 1 weekend post),
   preferred hours, IANA timezone (e.g. America/Lima).
7. Fixed things: dates, offers, prices, links, photos or videos already available.

"Just do it" means: defaults above, 5 weekdays + Saturday, the networks connected, their site for facts. Write the
brief back in 5 lines and continue.

## 2. Research angles (no paid APIs)

Use the tools you already have: web search and fetch, the user's site, their public profiles and recent posts,
competitors' pages, forum and Reddit threads where their audience asks questions, and this week's dates (holidays,
events, launches in their niche). If PostWire is connected and the account has published before, read what worked:
`get_post_performance` (MCP, with `timezone`) or `GET /api/insights?tz=<tz>` (REST).

Produce 8-10 angles. Each: one line, the source (a link, the user's words, or "general knowledge"), and which goal it
serves. Keep only what you can stand behind:

- No invented numbers, customers, quotes, reviews or results. A figure needs a source the user gave or a link.
- No web tools? Say so and work from the brief and the user's own material.

Pick 6-7 for the week, mixed roughly: 2 teach (a how-to or tip), 1 proof (a real result or case), 1 story or
behind the scenes, 1 opinion, 1 conversation starter (a question), 1 offer (a direct ask). Shift the mix toward the
goal: launches and sales get 2 offers; reach gets 2 opinions and no offer.

## 3. Write the calendar

One table first, then every draft:

| Day | Local date and time | Angle | Networks | Format | Status |
|---|---|---|---|---|---|
| Mon | 2026-10-12 09:00 | How we cut prep time in half | LinkedIn, Bluesky, Instagram | text; IG carousel 5 slides | needs 5 images |

Write each network's version from scratch for that network. Not the same text trimmed:

| Network | Limit PostWire checks | What works natively |
|---|---|---|
| LinkedIn | 3,000 | First 2 lines decide the click on "see more". Short paragraphs, first person. Link in `first_comment`, not the body. 0-3 hashtags at the end. |
| X (paid plans) | 280 per post (a link counts 23, an emoji 2) | One idea per post. Threads: up to 25 posts after the first. Put the link in the reply under the last post. Costs X credits: 1 per post, 10 with a link. |
| Bluesky | 300 | Plain and direct; a link card is fine; 0-2 hashtags. |
| Mastodon | 500 on most servers | Conversational; 2-4 CamelCase hashtags (they are how people find posts there). |
| Instagram | 2,200; needs a photo or video | Hook in the first 125 characters; carousel up to 10 (4:5); Reels for video (9:16); 3-5 specific hashtags; links are not clickable, say "link in bio". |
| TikTok | 2,200; needs a video or photos (up to 35) | The hook is the first 2 seconds of the video, not the caption. Short caption, 3-5 hashtags. The account owner picks who can see it, every time. |
| YouTube Shorts | title 100, description 5,000; needs a video | Title that names the payoff; first line of the description repeats it; tags. |
| Facebook Pages | 2,000 | Conversational, a question at the end; links work. |
| Telegram | 4,000 | A channel update: the news first, then details, then the link. |
| Discord | 2,000 | Community tone; say why it matters to the people in that server. |

Every post: one call to action tied to the goal. Tag the user's own links so they can measure them in their own
analytics: `?utm_source=<network>&utm_medium=social&utm_campaign=social-week-<YYYY-MM-DD of Monday>`.

Media: where a network needs a photo or video, write the prompt, do not pretend it exists.
- Image prompt: subject, composition, aspect ratio (4:5 Instagram feed, 9:16 Reels/TikTok/Shorts, 1:1), at most 7
  words of on-image text, style.
- Video script (15-30 s): the hook on screen in the first 2 seconds, 3 beats, the on-screen text, the call to action.
- The user makes them (or you, if you have an image or video tool). Without footage, `make_video_from_text` makes an
  8-12 s vertical MP4 from the post's words for TikTok or YouTube; show it before using it.
- A media network with no media by approval time stays in the calendar as "needs media" and is not scheduled.

Before showing it, check every draft: within its limit; different from the other networks' versions; no filler
("in today's fast-paced world", "game-changer", "unlock", "it's not X, it's Y", "here's the thing", chains of em
dashes); no claim without a source; hashtags only where the table says they help.

Save the week where the user can find it: `social-week/<Monday's date>.md` (the table and every draft) and
`social-week/<Monday's date>.json` in the format of "Calendar file" below, if you can write files; otherwise keep it
in the chat. The re-run in step 7 reads it.

## 4. Approval

Show the table and every draft exactly as it will be published, day by day, network by network, with its length
against the limit. Then ask one question that names everything:

"Schedule these 14 posts to LinkedIn, Bluesky and Instagram, Monday 12 to Saturday 17 October, at the times shown
(America/Lima)?"

Edit what they ask and show the edited text again. Nothing is scheduled without a yes to the exact text, networks and
times. TikTok: ask who can see each post (public, friends or private). X: say the credits it will use.

## 5. Schedule it with PostWire

1. Account (`my_account`): which brand (if a network is connected in several brands, ask and pass `brand_id`), which
   networks are connected. Missing ones: `create_connect_link` (one link connects several networks); wait for the
   user, call `my_account` again.
2. Say the plan's limits before scheduling, in plain words, when they matter. Free plan: 20 posts a month (a post
   counts once per network), 2 networks per post (the others are written and held), 3 scheduled posts waiting at a
   time (the 4th onward are saved as held: never published on Free, scheduled automatically after an upgrade), 20
   rows per upload, no X. So on Free a full week does not fit: offer to schedule the 3 most important posts on 2
   networks now and post the rest day by day from this chat, or to upgrade. Starter is the smallest plan that fits a
   week (every network in each post, 1,000 posts, no queue cap); Pro adds more brands, unlimited posts and team seats.
   Get the price and link from `get_upgrade_link` (or the result that hit the limit) and pass it on once. Never work
   around a limit (no extra accounts, no splitting posts).
3. Media: a file in the chat does not reach PostWire. `create_upload_link`, the user opens it on the device with the
   file, then `get_uploaded_file` until `done`; use its `media_url`. A public https link works as is.
4. Check first, then schedule. Use `bulk_schedule` with `rows` (one row per post) and `dry_run: true`:

   ```json
   { "timezone": "America/Lima", "dry_run": true, "rows": [
     { "date": "2026-10-12 09:00", "networks": "linkedin, bluesky, x",
       "text_linkedin": "…", "first_comment": "Full guide: https://example.com/guide?utm_source=linkedin&utm_medium=social&utm_campaign=social-week-2026-10-12",
       "text_bluesky": "…", "text_x": "…", "x_thread": "second post|||third post", "x_reply": "Link: https://…",
       "label": "social-week · Mon · prep time" },
     { "date": "2026-10-13 12:00", "networks": "instagram, tiktok", "text_instagram": "…", "text_tiktok": "…",
       "media_urls": "video:https://…/clip.mp4", "privacy": "public", "label": "social-week · Tue · behind the scenes" } ] }
   ```

   Columns: `date` ("YYYY-MM-DD HH:MM" in `timezone`, an ISO time with offset, or `next_slot` for the brand's next
   free queue slot), `networks`, `text_<network>`, `title` (YouTube), `media_urls` (`video:` prefix for a video),
   `alt_text`, `first_comment` (LinkedIn), `x_thread` (posts joined with `|||`), `x_reply`, `privacy` (TikTok),
   `label`. `media_urls` goes to every network of its row, so put the networks that share one photo or video in one
   row and the text-only networks in another row at the same time (a video listed per network is read as a photo
   post, which TikTok refuses). Always set `label` to `social-week · <day> · <angle>`: it is how the user finds the
   week in their queue.

   The dry run answers per row: the time it will go out, each network's length as that network counts it, X credits,
   whether it waits for approval, whether the plan holds it, and errors. Fix the errors, show anything that changed,
   then send the same rows with `dry_run: false`. It schedules every row or none. Keep the `batch_id`: the whole week
   can be undone with `DELETE /api/bulk/{batch_id}`, or one post with `cancel_scheduled_post`.
   Without `bulk_schedule`, call `schedule_post` once per row (`run_at` with an offset or `"next_slot"`,
   `per_platform`, `label`).
5. Results to respect, never to retry around:
   - `pending_approval` (202): the brand's rules send posts from AI agents to a person. Say who was asked; only a
     person approves, from the email or the dashboard. Do not resend.
   - `held` / `queue_limit` / `networks_per_post`: the plan held it. Say so once with the upgrade link it carries.
   - `bulk_already_scheduled` (409): it is already in the queue. Do not send it again.
   - `not_connected`, `media_required`: fix the row (connect link, or media) and run the dry run again.
   - `ambiguous_brand`: ask which brand, send `brand_id`.

## 6. Hand over: links and what to measure

List the week from `list_scheduled_posts` (from Monday to Sunday): day, local time, networks, status (queued, held,
pending_approval), id. The queue is in the dashboard, https://postwire.io/dashboard.html → Queue, where any post can be
edited or canceled before it goes out. After a post goes out, `get_post_status` with its id returns the live link.

Then give this checklist, filled in for their networks:

- After 24 hours and after 7 days, per post: views or impressions, interactions, link clicks (the utm links in their
  own analytics), follows, and the goal (sign-ups, sales, replies).
- Judge each post against the same account's usual post (its median), not against other accounts.
- PostWire reads the numbers of Bluesky, Mastodon, Instagram (likes and comments) and YouTube (views); for TikTok,
  LinkedIn, Facebook, Telegram and Discord, check the network's own analytics.
- Write one line per post in the calendar file: what happened, and a guess at why (hook, format, time, topic).
- One week is a hint; three weeks is a pattern. Change one thing at a time.

## 7. Next week (the re-run)

When the user says "next week", "again" or "what worked?":

1. Read last week's calendar file and its results lines.
2. `get_post_performance` (or `GET /api/insights?tz=<tz>`): winners and losers against the median, `best_times`,
   `headline_pattern`, `next`. Posts under 24 hours old are not ranked; patterns need 10 measured posts and appear on
   paid plans. Say how much data there is (n) before drawing a conclusion.
3. Keep the 2 best angles or formats with new topics, drop the weakest, move times toward `best_times`, keep 1-2
   experiments. On paid plans `replicate_top_post` drafts new posts on the structure of a winner.
4. Steps 3 to 6 again, with the same approval.

If the user wants it every week, set a reminder with this client's own scheduler only if they ask; never schedule
posts that were not approved.

## Calendar file

```json
{ "skill": "social-week", "week_of": "2026-10-12", "timezone": "America/Lima", "brand_id": null,
  "brief": { "business": "…", "audience": "…", "goal": "sales", "voice": "…", "link": "https://…" },
  "posts": [
    { "day": "Mon", "date": "2026-10-12", "time": "09:00", "angle": "…", "source": "https://…", "status": "approved",
      "networks": {
        "linkedin": { "text": "…", "first_comment": "…" },
        "x": { "text": "…", "thread": ["…"], "reply": "…" },
        "instagram": { "text": "…", "media": ["https://…/1.jpg"], "media_prompt": "…" },
        "tiktok": { "text": "…", "video_url": "https://…", "privacy": "public", "video_script": "…" },
        "youtube": { "title": "…", "text": "…", "video_url": "https://…" } },
      "result": null } ] }
```

If this skill's folder has `scripts/schedule-week.mjs` and Node 18+ is available, it turns this file into the rows
above, checks limits and media, and runs the dry run (`--confirm` schedules; it never schedules without it;
`--report` reads what worked for step 7): `node scripts/schedule-week.mjs social-week/2026-10-12.json` with
`POSTWIRE_API_KEY` set.

## REST (no MCP tools)

Base `https://postwire.io`. Headers: `Authorization: Bearer $POSTWIRE_API_KEY` (from the environment; never written to
a file or shown), `Content-Type: application/json`, and `X-PostWire-Source: mcp-skill-social-week`, which marks the
calls as an AI agent's so the brand's approval rules for agents apply.

| Need | Call |
|---|---|
| Account, plan, connections | `GET /api/me` |
| Link to connect networks | `POST /api/connect-link` `{ "platform"? , "brand_id"? }` |
| Check, then schedule the week | `POST /api/bulk` `{ "rows": […], "timezone": "…", "dry_run": true }`, then `false` |
| Undo the week | `DELETE /api/bulk/{batch_id}` |
| One post | `POST /api/schedule` `{ "platforms", "per_platform", "run_at", "label" }` |
| Next free slot | `GET /api/schedule/next-slot?platforms=linkedin,bluesky&timezone=…` |
| The queue | `GET /api/schedule?from=…&to=…` |
| What worked | `GET /api/insights?tz=…` |
| Price an X thread | `GET /api/x/quote?text=…&thread=…&reply=…` |
| Upload a file | `POST /api/media/upload-link` (a page for the user) or `POST /api/media/upload-url` |

Every error has `code`, `what` and `fix`: read them, do not retry blindly. All codes: https://postwire.io/docs/errors.md

## Rules

- Never publish, schedule or cancel without the user's explicit yes to the exact text, networks and times with timezone.
- Never rewrite an approved draft without showing it again.
- Never invent results, testimonials, statistics or customers.
- Never print, log or commit an API key.
- Plan limits are facts to state once, not obstacles to route around.

Docs: https://postwire.io/docs/automation/ (bulk) · https://postwire.io/docs/scheduling/ ·
https://postwire.io/docs/analytics/ · https://postwire.io/docs/x/ · Latest version of this file:
https://postwire.io/skills/social-week/SKILL.md
