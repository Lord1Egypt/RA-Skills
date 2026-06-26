---
name: slack-thread-export
description: Export Slack thread messages from a logged-in Slack web tab into CSV using an attached Chrome Browser Relay tab. Use when the user wants to collect Slack conversations by person, channel, or time range; exclude DMs/comments; archive thread activity; or turn Slack search results into reusable CSV/JSONL datasets. Especially useful for requests like "export this user's work-related thread messages", "collect Slack thread history into CSV", or "crawl Slack from my logged-in browser session".
---

# Slack thread export

Use this skill when Slack data must be exported from a **real logged-in browser tab** instead of a bot token or admin API.

## Scope and non-goals

This skill is intentionally optimized for **logged-in Slack Web exports through an attached Chrome Browser Relay tab**.

It is meant to be good at:
- exporting thread replies for one user across selected channels
- building CSV/JSONL archives from Slack search
- narrowing results by channel/date and optionally reducing non-work noise
- surviving partial failures with resumable raw output and failed-channel retries

It is **not** meant to be:
- a generic Slack admin/export replacement
- a bot-token or SCIM-based export tool
- a guaranteed complete legal/compliance archive
- a universal classifier for "work-related" messages

## Workflow

1. Ensure the user has attached the Slack tab with **Browser Relay** and use `profile="chrome"`.
2. Use the browser tool or `openclaw browser --browser-profile chrome` to confirm the attached tab is the correct Slack workspace.
3. Read `localStorage.localConfig_v2` from the Slack tab to get the active team metadata and xoxc token used by the web client.
4. Query Slack's internal `search.messages` endpoint **from inside the page context** using `fetch('/api/search.messages', ...)` so the logged-in browser session supplies the right cookies/session context.
5. Export in small batches:
   - Prefer channel-by-channel queries over one huge query.
   - Prefer page-by-page loops (`count=100`, increment `page`).
   - Back off on `ratelimited` with sleep/retry.
   - Stop when `count == 0` or `< 100` for a page.
6. Exclude unwanted records before writing files:
   - Drop IM/MPIM results.
   - Keep only records whose permalink includes `thread_ts=` when the user wants thread replies.
   - Apply user-requested business filters (channel whitelist, keyword filter, date range, etc.).
7. Save both:
   - raw JSONL for audit/debugging
   - cleaned CSV for the user's actual deliverable

## How it works

This skill does **not** scrape visible Slack DOM rows as the primary path. Instead it piggybacks on the same internal search flow used by Slack Web:

1. Attach to the user's already logged-in Slack browser tab.
2. Read the active workspace metadata from `localStorage.localConfig_v2`.
3. Reuse the web client's xoxc token **inside the page context only**.
4. Call `fetch('/api/search.messages', ...)` from the attached Slack page so the request inherits the browser session cookies and client context.
5. Page through Slack search results and transform them into exportable rows.

This is more reliable than host-side requests because Slack search often expects both the token **and** the live logged-in browser session.

## Operational numbers and limits

Use these defaults unless there is a clear reason not to:

- `count=100` per `search.messages` request
  - This is the practical max batch size used by the web client path here.
- `sleep-seconds=0.5` between normal page requests
- On `ratelimited`, sleep **at least 3-5 seconds** before retrying the same page
- Start with `max-pages=60` per channel as a practical ceiling
- Prefer **1 channel at a time** or a short whitelist over a whole-workspace sweep

Practical guidance:

- **Usually safe:** 1 user + 1 channel + 1-20 pages
- **Still reasonable:** 1 user + 3-10 channels + paging with 0.5s delay
- **Risky:** one giant all-history query across the whole workspace
- **Very risky:** one huge page-context evaluate that loops many channels and many pages in one call

Why this matters:

- Slack will return `ratelimited` if requests come too quickly or the query is too broad.
- Browser evaluation can time out if too much work is packed into one evaluate call.
- The safest shape is **many short calls**, not one giant call.

## What was actually validated

These are not theoretical claims only; the workflow was exercised against a real logged-in Slack tab.

### Small-range validation

Test shape:
- channels: `tech-team`, `moonlight`, `dev-part`
- range: `after=2026-03-01`, `before=2026-03-15`
- mode: `strict`

Observed result:
- `tech-team`: 9 rows
- `moonlight`: 29 rows
- `dev-part`: 0 rows
- total raw: 38
- unique raw: 38
- failed channels: 0
- total requests: 3
- duration: ~5.05s

This validated:
- `--before`
- `--after`
- `--channel-file`
- `--summary-json`
- `--failed-channels-out`
- `--resume-from-jsonl`
- `--preflight`
- `strict` mode

### Heuristic filtering validation

To prove that `heuristic` mode does more than `strict`, a second test included edge channels:
- `tech-team`
- `moonlight`
- `random`
- `music`
- `ai서비스활용-lounge`

Observed result:
- `strict`: 50 rows kept
- `heuristic`: 40 rows kept
- removed by heuristic: 10 rows
  - `random`: 9
  - `music`: 1

The removed examples were casual/non-work items such as chatty thread replies, celebration posts, and a YouTube link. This confirmed that heuristic mode can reduce obvious non-work noise when mixed channels are included.

### Stress validation

A broader run used these channels:
- `moonlight`
- `dev-part`
- `tech-team`
- `bob`
- `cms`

Stress settings:
- `max-pages=20`
- `sleep-seconds=0.05`
- mode: `heuristic`

Observed result:
- total raw: 4580
- filtered keep: 2763
- total requests: 48
- duration: ~85.52s
- ratelimit retries: 0
- failed channels: 0

Interpretation:
- The channel-by-channel/page-by-page design was stable under a moderately aggressive run.
- This does **not** guarantee immunity from rate limiting in all workspaces.
- It does show that the design is more robust than one giant search/evaluate call.

## Important constraints

- Do **not** assume the Slack API is callable directly from host Python with only the xoxc token. In practice the browser session context matters; call from the page context first.
- Do **not** try one giant all-history query first; Slack rate-limits and long browser evaluations will time out.
- Do **not** claim the export is complete if channel-level calls failed. Report partial coverage clearly.
- Treat the xoxc token and any cookies as sensitive. Do not echo them back to the user or store them in exported files.
- Do **not** silently widen "work-related" to mean everything. If the user wants "all work-related threads," state clearly that this is a heuristic unless they also provide a channel whitelist, date range, or keyword rule.
- Do **not** present heuristic filtering as moderation-, compliance-, HR-, or legal-grade classification.

## Publish-ready status

At this stage, the skill is suitable for **beta/publication-candidate** use when these caveats are respected:

- Requires an attached, logged-in Slack web tab via Browser Relay
- Relies on Slack web client behavior that may change over time
- Uses heuristic filtering for "work-like" exports unless `strict` or `raw` mode is chosen
- Is strongest for operator-led exports, not unattended compliance archiving

If publishing publicly, describe it as an advanced/browser-relay Slack export skill rather than a universal Slack export solution.

## Failure semantics

Handle failures explicitly:

- `invalid_auth`
  - Meaning: wrong tab, logged-out tab, or a host-side request that lacks the browser session context.
  - Fix: confirm the attached Slack tab is logged in and re-run from page context.
- `ratelimited`
  - Meaning: too many requests too quickly or query scope too broad.
  - Fix: sleep and retry the same page; reduce channel count; add `after:` date filters.
- browser evaluate timeout
  - Meaning: too much work packed into one evaluate call.
  - Fix: split by channel and page; keep each evaluate short.
- partial export
  - Meaning: some channels completed and some failed.
  - Fix: save raw progress, report completed channels, and retry only failed channels.

## Recommended query patterns

Use these building blocks:

- User filter: `from:<@USER_ID>`
- Thread-only: `is:thread`
- Channel filter: `in:#channel-name`
- Time filter if needed: `after:YYYY-MM-DD`

Typical query:

```text
from:<@UXXXX> is:thread in:#tech-team after:2026-01-01
```

## Preferred output columns

Use these columns unless the user asks otherwise:

- `datetime_utc`
- `channel_name`
- `channel_id`
- `thread_ts`
- `username`
- `text`
- `permalink`
- `source_query_channel`

## Scripts

- `scripts/export_slack_threads.py` — channel-by-channel Slack thread exporter driven through the attached Chrome relay tab.
- `scripts/retry_failed_channels.py` — rerun export using the `failed-channels-out` file from a previous run.

Run scripts with explicit parameters instead of editing code in place.

Example:

```bash
python3 skills/slack-thread-export/scripts/export_slack_threads.py \
  --target-id <attached-tab-id> \
  --user-id U04SFF458BC \
  --team-id T01AY79ELUC \
  --channels tech-team moonlight dev-part \
  --after 2026-01-01 \
  --before 2026-03-15 \
  --mode heuristic \
  --failed-channels-out exports/slack/failed.txt \
  --summary-json exports/slack/summary.json \
  --out-csv exports/slack/out.csv \
  --out-jsonl exports/slack/out.jsonl
```

## If coverage is too broad

Narrow the export before retrying:

- Use a shorter date range.
- Use channel whitelist first.
- Export raw first, then run a second-pass filter for “work-like” heuristics.
- Sample channel distribution first, then choose high-signal channels before doing the full export.

## Retry workflow

When a run is partial:

1. Keep the raw JSONL from the first run.
2. Save failed channels with `--failed-channels-out`.
3. Retry only those channels using `scripts/retry_failed_channels.py`.
4. If needed, pass `--resume-from-jsonl` so the retry output starts from the previous raw capture instead of rebuilding from zero.

Retry example:

```bash
python3 skills/slack-thread-export/scripts/retry_failed_channels.py \
  --target-id <attached-tab-id> \
  --user-id U04SFF458BC \
  --team-id T01AY79ELUC \
  --failed-channels-file exports/slack/failed.txt \
  --resume-from-jsonl exports/slack/out.jsonl \
  --out-csv exports/slack/retry.csv \
  --out-jsonl exports/slack/retry.jsonl \
  --summary-json exports/slack/retry-summary.json \
  --failed-channels-out exports/slack/retry-failed.txt
```

## Supported options

The script now supports these operational controls:

- `--channel-file` — read channel names from a file
- `--after` / `--before` — date windowing
- `--resume-from-jsonl` — continue from a previous raw export
- `--failed-channels-out` — save failed channels for targeted retry
- `--summary-json` — save structured run summary
- `--preflight` — sample page-1 volume per channel before full export
- `--mode strict|raw|heuristic`
  - `strict`: export only the requested channel/date slice, no work-like heuristic filtering
  - `raw`: keep everything collected after the query constraints; useful for audit/review datasets
  - `heuristic`: apply work-related channel/text filtering after collection
- `--keyword` / `--channel-hint` — extend heuristic filtering for a specific workspace

## Filtering guidance

For “work-related” exports, prefer this order:

1. Channel whitelist / channel-name hints
2. Explicit date range
3. Keyword heuristic on message text
4. Manual review for edge channels

If the user says "all work-related threads", explain that this is heuristic unless they provide a strict channel whitelist or date range.

## Mode selection guide

Use `strict` when:
- the user already knows which channels matter
- the goal is faithful export within explicit channel/date constraints
- the user does not want extra classifier behavior

Use `raw` when:
- the user wants a review dataset first
- a human or later pipeline will do the filtering
- auditability matters more than noise reduction

Use `heuristic` when:
- the user asks for "work-related" rather than a strict channel list
- there are mixed-signal channels in scope
- reducing obvious non-work chatter is valuable

If unsure, start with `strict` or `raw`, then derive a second-pass `heuristic` export for comparison.
