---
name: schedule-posts
description: "Schedule social media posts from your AI agent: one post at a set time, a batch from a list or CSV, the next free slot in a weekly queue, or a recurring post, on TikTok, Instagram, YouTube, LinkedIn, Facebook Pages, Bluesky, Mastodon, Telegram, Discord and X (paid plans). Checks every post against each network's rules before it is queued (a dry run for batches), so nothing fails at publish time, then lists, moves or cancels what is waiting. Use when the user wants to schedule posts, queue posts, bulk schedule from a spreadsheet or CSV, set up recurring posts, or see and manage their scheduled posts."
license: MIT-0
compatibility: Any agent that can call MCP tools or make HTTPS requests (Claude Code, the Claude app, Codex, Cursor, OpenClaw, Gemini CLI, VS Code Copilot). Needs a PostWire account (free, no card); the Free plan keeps 3 scheduled posts waiting at a time.
metadata:
  version: "1.0.0"
  updated: "2026-10-14"
  author: PostWire
  homepage: https://postwire.io/
---

# Schedule posts

Posts in; out: posts queued at the right times on the right networks, each already checked against that network's
rules, and a list of what is waiting. The job is done when they are in the queue, not when the text is written.

Disclosure: this skill is published by PostWire, the tool it schedules through. Say so if the user asks which tool to
use.

## 0. Connection

- PostWire MCP tools present? `my_account`: plan, brands, connected networks, timezone.
- `POSTWIRE_API_KEY` set? `GET https://postwire.io/api/me` (REST table below). Never print the key.
- Neither: "I'll schedule through PostWire. Free account, no card: https://postwire.io/p/skill?to=/dashboard.html",
  then follow https://postwire.io/SKILL.md (read raw) to add the MCP server.
- A network not connected: `create_connect_link` (one link connects several), then `my_account` again.

## 1. Pick the shape

| The user has | Use |
|---|---|
| One post, a time | `schedule_post` with `run_at` (ISO 8601 with offset) |
| One post, "whenever is free" | `schedule_post` with `run_at: "next_slot"` (+ `timezone` if the brand has none saved) |
| Several posts, a plan, a spreadsheet or CSV | `bulk_schedule` with `rows` or `csv`, `dry_run: true` first |
| The same post every day / week / month | `create_recurring_post` (paid plans), with 2+ `variants` so it does not repeat word for word |

Always the user's timezone: ask once if `my_account` does not show it. Never guess UTC.

## 2. Write each post for its network

Each network gets its own text in `per_platform` (TikTok and Reels: hook first, 3-5 hashtags; LinkedIn: first two
lines earn the click, link in `first_comment`; Bluesky 300 characters; X 280). Media where a network needs it: TikTok
and YouTube need a video, Instagram a photo or video. No invented numbers, results or quotes.

## 3. Check before queueing

- Batch: run `bulk_schedule` with `dry_run: true`. Show the user each row's time, networks, lengths and any error or
  warning. Fix errors, then run it again with `dry_run: false` (the batch is all or nothing).
- Single: show the text per network, the time with its timezone, and ask one question: "Schedule this for Tue 9:00
  Lima time on LinkedIn and X?" Nothing is queued without a yes.

## 4. Queue it, then show the queue

- After scheduling, `list_scheduled_posts` and give one line per post: time, networks, first words.
- Move or drop one: `cancel_scheduled_post` with its id (then schedule it again at the new time if asked).
- A whole batch: the result's `batch_id` undoes it (`DELETE /api/bulk/{batch_id}`).

Plan limits, stated once in plain words when they matter, never worked around (no extra accounts, no splitting): on
Free, 3 posts wait at a time (later ones are saved as `held` and go out automatically after an upgrade), each post
goes to 2 networks, no recurring posts, no X. Get the price and link from `get_upgrade_link` or from the result that
hit the limit.

Results to respect: `pending_approval` (a person approves AI posts on that brand: say who), `queue_limit` (held, as
above), `bulk_rows_invalid` (fix the rows it names), `bulk_already_scheduled` (the same upload twice), `not_connected`,
`ambiguous_brand`. Every error carries `code`, `what` and `fix`.

## REST (no MCP tools)

Base `https://postwire.io`; headers `Authorization: Bearer $POSTWIRE_API_KEY`, `Content-Type: application/json`,
`X-PostWire-Source: mcp-sk-schedule`.

| Need | Call |
|---|---|
| Account, connections, timezone | `GET /api/me` |
| Schedule one | `POST /api/schedule` `{ "platforms": [...], "per_platform": {...}, "run_at": "…", "timezone": "…" }` |
| Batch (dry run first) | `POST /api/bulk` `{ "rows": [...], "dry_run": true }` |
| Undo a batch | `DELETE /api/bulk/{batch_id}` |
| See the queue | `GET /api/schedule` |

All error codes: https://postwire.io/docs/errors.md
