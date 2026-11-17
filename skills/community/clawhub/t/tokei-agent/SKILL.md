---
name: tokei-agent
description: Tokei (tokei.io) is a pre-launch, waitlist and giveaway platform — launch pages, competition giveaways, sweepstakes, referral and viral-loop campaigns, Product Hunt launch drives, Gleam-style and KickoffLabs-style entry pages. This CLI controls them from the command line — list, clone, update, publish and unpublish pages, upload images and video, set prizes, reward tiers and deadlines, restyle pages, and read stats, leaderboards, top referrers, signups, survey responses, winner selections and the webhook event catalog, plus manage webhooks (all 5 events) — all via the Tokei v1 REST API.
homepage: https://tokei.io/agent
metadata: {"openclaw":{"emoji":"⏱️","requires":{"bins":[],"env":["TOKEI_API_KEY"]}}}
---

# tokei-agent

`tokei-agent` is a zero-dependency CLI for the Tokei v1 REST API (`https://tokei.io/api/v1`). Every command prints JSON to stdout, so pipe it to `jq` or parse it directly.

## Install tokei-agent if it isn't already there

```sh
npm install -g tokei-agent
# or run it without installing:
npx tokei-agent --help
```

Requires Node 22.12+. npm release: https://www.npmjs.com/package/tokei-agent — official website: https://tokei.io — agent docs: https://tokei.io/agent — API reference: https://tokei.io/docs/api

---

## ⚠️ Four hard rules (read first)

**Rule 1 — Run `tokei-agent me` before anything else.** It proves the key is live and reports the account's **plan**. API access requires an active subscription or lifetime plan — **trial accounts get `403` on every command**, so a whole workflow can fail on its first call for a reason no other command explains.

> `me` does **not** report the key's scope. There is no way to read a key's scope from the API — you discover a read-only key by getting `403 FORBIDDEN` on your first write. If the task involves changing anything, ask the human up front whether their key is read+write.

**Rule 2 — Every media URL you write to a page MUST come from `tokei-agent media:upload`.** Raw filesystem paths (`hero.png`) and third-party URLs (`https://example.com/hero.png`) are **rejected** — the seven media fields on `pages:update` are guarded by a closed host allowlist that only accepts the app's own storage (and `res.cloudinary.com`). Always:

```sh
HERO=$(tokei-agent media:upload ./hero.png | jq -r '.data.public_url')
tokei-agent pages:update "$PAGE_ID" --image-video "$HERO"
```

Every `--image-video` / `--og-image` / `--background-image` example below assumes a `public_url` obtained this way — never a local file.

**Rule 3 — List fields replace wholesale; always read before you write.** `prizes` (max 20) and `reward_thresholds` (max 50) are **not** merged — whatever array you send becomes the entire list, so sending one prize deletes the other nineteen. The pattern is always `pages:get` → modify the array → `pages:update` with the complete list.

**Rule 4 — Get explicit human approval before any action that emails people or changes anything public.** Publishing a page, creating a webhook that fires on live events, sending entries/notifications, or anything else visible to entrants or third parties needs a human sign-off first — this CLI does not gate those calls for you, so you are the gate. Read-only commands (`me`, `pages:list`, `pages:get`, `stats`, `leaderboard`, `referrals:top`, `entries:list`, `surveys:list`, `winners:list`, `webhooks:list`, `templates:list`, `actions:catalog`, `events:catalog`) need no such approval.

---

## Terminology mapping (read this first)

The API and the UI use different words for the same objects. Do not treat these as different things.

| API says               | UI / humans say    | Notes                                                            |
| ---------------------- | ------------------ | ---------------------------------------------------------------- |
| `contest`              | page, campaign     | The core object. `contestId` in paths = the page's id.           |
| `promotion`            | page, campaign     | Same object again — `POST /promotions` creates it, reads live under `/contests/{id}`. |
| `entry`                | signup, subscriber | One person joining a page.                                       |
| `entries:create`       | add a signup       |                                                                  |

CLI command names use the UI words (`pages:list`, `pages:update`); the JSON they return uses the API words (`contest`, `promotion`).

## Setup

| Env var         | Required | Meaning                                                                          |
| --------------- | -------- | -------------------------------------------------------------------------------- |
| `TOKEI_API_KEY` | Yes      | Sent as `Authorization: Bearer <key>`. Create one at tokei.io → Dashboard → Settings → API Keys. |
| `TOKEI_API_URL` | No       | Base URL override (default `https://tokei.io`).                                  |

Keys have a scope: **read-only** or **read+write**. Write commands need a read+write key; a read-only key gets `403`. Keys can also carry an expiry — an expired key gets `401`. Prefer a read-only key unless the task actually changes something.

## Core workflow

The fundamental pattern, end to end:

1. **Verify** — confirm the key and the plan (Rule 1)
2. **Discover** — list your pages, and the platform's named starting points
3. **Create** — clone a template (or one of your own pages) into a new draft
4. **Prepare** — upload media and get back allowlisted URLs (Rule 2)
5. **Shape** — PATCH copy, dates, prizes, appearance and media onto the page
6. **Publish** — flip the draft live (needs a future `end_date`)
7. **Monitor** — stats, leaderboard, top referrers, signups
8. **Automate** — subscribe a webhook instead of polling

```sh
# 1. Verify — do this first, always
tokei-agent me

# 2. Discover
tokei-agent pages:list --status active
tokei-agent templates:list

# 3. Create (returns a draft page)
PAGE=$(tokei-agent pages:clone --title "Spring Launch Waitlist" \
  --template product-hunt | jq -r '.data.id')

# 4. Prepare media (Rule 2 — never pass a raw path)
HERO=$(tokei-agent media:upload ./hero.png | jq -r '.data.public_url')

# 5. Shape
tokei-agent pages:update "$PAGE" \
  --description "Join the list for early access." \
  --template showcase --dark-mode true --primary-color "#7d78c6" \
  --image-video "$HERO"

# 6. Publish (end_date must be in the future — set it in the same call if unset)
tokei-agent pages:publish "$PAGE" --data '{"end_date":"2026-09-01T00:00:00Z"}'

# 7. Monitor
tokei-agent stats "$PAGE"
tokei-agent leaderboard "$PAGE" --per-page 10
tokei-agent referrals:top "$PAGE" --per-page 10
tokei-agent entries:list "$PAGE"

# 8. Automate — events:catalog lists all 5 subscribable events and their payloads
tokei-agent webhooks:create --url https://yourserver.com/webhooks/tokei \
  --events entry.created,winner.selected
```

Confirm every write by reading it back with `pages:get "$PAGE"` — everything writable is also readable.

## Output envelope, exit codes

- stdout: the API's JSON body, augmented with a top-level `"rate_limit"` object: `{"limit": n, "remaining": n, "reset": <unix epoch seconds>}`, or `null` when the headers were absent (e.g. network failure).
- **Agents always get this JSON.** From 0.3.1 the CLI renders a human banner and summary *only* when stdout is an interactive terminal. A subprocess, pipe, redirect, CI environment or the `mcp` transport has no TTY, so the JSON envelope below is what you will receive, byte for byte. If you ever need to force it explicitly, set `TOKEI_OUTPUT=json`.
- Exit code `0` — success (HTTP 2xx).
- Exit code `1` — API or network error. The API's JSON error body (same envelope, with `rate_limit`) is still printed on stdout; pure network failures print `{"ok": false, "error": {"type": "network_error", "message": ...}}`.
- Exit code `2` — usage error (bad flags, missing arguments, missing `TOKEI_API_KEY`). Printed as JSON on **stderr**: `{"ok": false, "error": {"type": "usage_error", "message": ...}}`. Nothing was sent to the API.

**The shape, so you can `jq` it without guessing.** Success always nests the payload under `data` — it is never a bare top-level array:

```jsonc
// single-object reads (pages:get, me, media:upload, pages:clone, …)
{ "success": true, "data": { … }, "rate_limit": { … } }

// list reads (pages:list, leaderboard, referrals:top, entries:list,
//             surveys:list, templates:list, webhooks:list)
// referrals:top adds a sibling "totals" object next to data + pagination
{ "success": true, "data": [ … ],
  "pagination": { "page": 1, "per_page": 20, "total_pages": 3, "total_count": 47 },
  "rate_limit": { … } }

// errors
{ "success": false,
  "error": { "code": "VALIDATION_ERROR", "message": "…", "status": 422,
             "details": [{ "field": "end_date", "message": "…" }] },
  "rate_limit": { … } }
```

So the idioms are:

```sh
tokei-agent pages:list | jq -r '.data[0].id'                          # first page's id
tokei-agent pages:list | jq -r '.data[] | select(.status=="active") | .id'
tokei-agent pages:list --per-page 100 | jq '.pagination.total_pages'  # more to fetch?
tokei-agent pages:get "$PAGE" | jq -r '.data.public_url'
tokei-agent media:upload ./hero.png | jq -r '.data.public_url'
tokei-agent pages:update "$PAGE" --title x | jq -r '.error.details[]?.field'
```

`templates:list`, `me` and `winners:list` are unpaginated — they return `data` with no `pagination` key (`winners:list`'s `data` is still an array, just capped rather than paged; see its entry below). `events:catalog` and `actions:catalog` return `data` as an object (or one entry, with `--type`), not an array at all.

> **Known issue — exit codes on Node 24 / Windows (fixed in 0.3.0).** On 0.2.2 and earlier the CLI could print its correct JSON output and then abort during process exit, corrupting the exit code (`$LASTEXITCODE` read `-1073740791` / `0xC0000409` on success and failure alike). On an affected version, judge a run by the JSON on stdout, not by the exit status — or upgrade. (Historical labelling slip: the 0.3.0 tarball misreported `--version` as `0.2.2`; 0.3.1+ reports correctly.)

## Commands (read — any key)

**`me`** — verify the key, see plan and API usage. Returns `user_id`, `email`, `plan`, `active_contests` and an `api_usage` block (`requests_today`, `daily_limit`, `rate_limit_per_minute`). Not the key's scope — see Rule 1.

```sh
tokei-agent me
```

**`pages:list`** — list your pages. Flags: `--status draft|active|completed|deleted`, `--mode competition|gamification|sharing_only`, `--page <n>`, `--per-page <1-100>`. The filter values are exactly the values a page's `status` field can hold, so what you read back is what you can filter on. There is no `ended` or `paused` status; those were accepted by older builds and always returned nothing.

`status` — both the field and the filter — is the **effective** status, derived from the stored value **and the dates**: a page whose `end_date` has passed reads and filters as `completed`, and one whose `start_date` is still in the future reads as `draft`. A creator can mark a page completed by hand, but nothing does so when `end_date` passes, so before 2026-07-27 an ended page nobody closed manually reported `active` indefinitely. `status: "active"` now genuinely means live — trust it.

```sh
tokei-agent pages:list --status active --per-page 20
```

**`pages:get <contestId>`** — one page, full object. `title` is the **visible page headline**, not the internal dashboard name, so what you read is what a visitor sees. The object also carries:

| Field | Meaning |
| ----- | ------- |
| `total_entries` | Count of entry **actions** (`contest_entries` rows) — not people, and not points. **Never narrate this as "signups."** |
| `total_points_awarded` | Sum of points earned across all entry actions. Not a headcount either. |
| `status` | The **effective** status (see `pages:list` above) — `completed` once `end_date` passes, whatever is stored. Safe to report as "live" / "finished" directly. |
| `days_left` | Whole days remaining, computed from `end_date` at read time; **`0` means it has ended**, and the partial final day rounds up so a page closing tonight reads `1`. Only falls back to the stored column when there is no `end_date` at all. Before 2026-07-27 this replayed a stale stored value and could say `30` on a page with a day to go. |
| `entry_methods[].points` | What each action **actually awards**, including any per-action override the owner configured. Safe to quote to a user. |
| `description`, `prizes`, `reward_thresholds` | Everything `pages:update` can write, so you can read-modify-write. |
| `public_url` | The live page URL — no second call needed. **Can be `null`** when the page has no slug yet (`contest_url` null); check before handing it to your user as a link. |
| `primary_color` | Brand colour as a CSS value (e.g. `#7d78c6`); `null` means the template default. `settings.color` is a deprecated alias of it. |
| `card_width` | `max-w-2xl` \| `max-w-3xl` \| `max-w-4xl` \| `max-w-7xl`; `null` renders as `max-w-2xl`. |
| `settings.template` | Page skin: `basic-new`, `showcase` or `future`. |
| `image_video` | Hero media — an image **or** a video URL. May carry dimension hints as query params. Writable via `pages:update --image-video` (get the URL from `media:upload`). |
| `secondary_image` … `fifth_image`, `background_image`, `og_image` | The page's other media slots; `null` when unset. Each writable via its own `pages:update` flag — see the media flags note under `pages:update` below. |
| `campaign_name`, `project_name` | **Read-only.** `project_name` is the small subheading under the headline; `campaign_name` is the internal dashboard name and never appears on the page. |

`primary_color`, `card_width`, `settings.template` and all seven media fields (`image_video`, `secondary_image`, `third_image`, `fourth_image`, `fifth_image`, `background_image`, `og_image`) are now writable via `pages:update` (see below); `dark_mode_enabled` writes through `--dark-mode` there too, though it isn't itself a field in this table. `campaign_name`/`project_name` remain read-only always. If your user wants a headcount ("how many people entered"), that's neither `total_entries` nor `total_points_awarded` — use `stats`'s `unique_participants` instead.

```sh
tokei-agent pages:get 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90
```

**`stats <contestId>`** — aggregated analytics for a page.

```sh
tokei-agent stats 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90
```

**`leaderboard <contestId>`** — participants ranked by points. Flags: `--page`, `--per-page <1-100>`.

```sh
tokei-agent leaderboard 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90 --per-page 10
```

**`referrals:top <contestId>`** — the page's top referrers, ranked by converted referrals then total referrals. Flags: `--page`, `--per-page <1-100>`.

Each row carries `referrer_id`, `referral_code`, `full_name`, `email`, `total_referrals`, `converted_referrals` and `bonus_points_earned`. Alongside `data` and `pagination` the response adds a `totals` object: `total_referrers`, `total_referrals`, `total_clicks`, `converted_clicks`, `click_conversion_rate` (a percentage, one decimal place).

Three things to know before you report these numbers:

- Only entrants who have actually referred someone appear. Every participant is issued a referral code, so an unfiltered list would be almost entirely zero rows.
- `converted_referrals` counts referred people who went on to complete at least one entry action *other than* sharing — it is the ranking key, and it is the number worth reporting as "referrals that worked".
- `bonus_points_earned` is a **count of bonus entries, not a points total**, despite the name. The name matches the underlying data and the dashboard, so it is kept for consistency; do not present it as points.

```sh
tokei-agent referrals:top 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90 --per-page 10
```

**`winners:list <contestId>`** — selection-run history for a page, newest first, each run with its persisted winners nested. Read-only, no query params, no pagination (contest-scale run/winner counts, capped at 100 runs — headroom, not a pagination story). Finalize-via-API is deliberately out of scope (human-approval policy, Rule 4) — this is how an agent looks back at what a run actually selected, not how it draws one. Each run carries `id`, `created_at`, `seed`, `algorithm_version`, `status`, `requested_by_email`, `finalized_at`, `total_candidates`, `total_winners_selected`, `winners_count` and a `winners` array; each winner carries `id`, `contest_user_id`, `email`, `full_name`, `entry_points`, `created_at`, `country_name`, `city`, `prize_tier`, `prize_description`, `prize_value`, `selected_at`, `notified_at`, `notification_method`, `verified`, `claimed_at`.

```sh
tokei-agent winners:list 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90
```

**`entries:list <contestId>`** — signups for a page. Flags: `--page`, `--per-page <1-100>`, `--email <addr>` (exact-match filter).

```sh
tokei-agent entries:list 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90 --email fan@example.com
```

**`surveys:list <contestId>`** — survey responses. Flags: `--page`, `--per-page <1-100>`.

```sh
tokei-agent surveys:list 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90 --page 2
```

**`webhooks:list`** — list webhook subscriptions. Reading them needs no write scope (only `webhooks:create`/`webhooks:delete` do). Flags: `--page`, `--per-page <1-100>`. Watch `failure_count`: a subscription is auto-disabled after 10 consecutive failed deliveries.

```sh
tokei-agent webhooks:list
```

**`templates:list`** — the platform's named starting points, for cloning with `pages:clone --template <slug>`. Same list for every key — not scoped to your account (it's platform content, not the caller's). No flags, no pagination.

```sh
tokei-agent templates:list
```

Example response — an **excerpt** of the real menu at the time of writing (15 templates live, 5 shown). It grows as the platform publishes templates, so call `templates:list` and use the slugs it returns; never hardcode one.

```json
{
  "success": true,
  "data": [
    {
      "id": "0e4de06c-8915-4e1c-ba3f-48f6c9a098f2",
      "slug": "collect-email-list",
      "name": "Collect email list — registration-first opt-in subscriber page",
      "skin": "future",
      "entry_method_count": 0
    },
    {
      "id": "06743256-2e8e-4ede-a431-f17866fae1f6",
      "slug": "competition-starter",
      "name": "Starter — Gleam-style competition giveaway (X, Instagram, TikTok, Facebook entries)",
      "skin": "basic-new",
      "entry_method_count": 6
    },
    {
      "id": "c0cc71a0-1ff5-46ab-8a23-c801aec30337",
      "slug": "instagram-engagement",
      "name": "Instagram engagement — follow & share photo giveaway",
      "skin": "showcase",
      "entry_method_count": 3
    },
    {
      "id": "6ca0bdbc-23d8-4c79-a894-857eea485fbe",
      "slug": "secret-codes",
      "name": "Secret Code — unlock entries with a code (QR codes, receipts, printed inserts, events)",
      "skin": "basic-new",
      "entry_method_count": 0
    },
    {
      "id": "88fde228-8baf-4b31-9b0e-cc243b3cc83d",
      "slug": "steam-promotion",
      "name": "A futuristic Steam template for Adding to Steam Wishlists and Playing Steam Games.",
      "skin": "future",
      "entry_method_count": 6
    }
  ],
  "rate_limit": { "limit": 60, "remaining": 59, "reset": 1753000000 }
}
```

Rows come back sorted by `slug`, unpaginated. The other ten at the time of writing: `discord-community`, `facebook-promotion`, `family-friends`, `prelaunch-vips`, `product-hunt`, `survey-system`, `tiktok-growth`, `twitch-growth`, `x-followers`, `youtube-contest`.

`skin` is the page skin (`basic-new`/`showcase`/`future`) — the same vocabulary `pages:update --template` writes. `entry_method_count` is how many entry actions the template ships with. For agents: **list templates first, then clone by slug** — don't guess a slug. A `0` there is not always a stub — three templates legitimately report `0` because their action lives on the page rather than in `entry_methods`: `secret-codes` (the single action *is* the secret code), `survey-system` (a mandatory survey plus a photo upload) and `collect-email-list` (the sign-up form is the whole page). Cloning `secret-codes` keeps its code copy but switches the code input **off** and copies **no codes** — codes are stored per page and are never copied, so the owner uploads their own in the dashboard and then switches the input on.

What the skins look like — use this to match the user's reference point:

- `basic-new` ("Basic") — the classic giveaway card: entry actions in a clean vertical list, soft pastel styling. This is the format popularized by Gleam — when a user asks for a Gleam-style (or KickoffLabs-style) campaign, this is the closest match. The platform default.
- `showcase` — a dynamic two-column layout with warm colors and platform-styled buttons. Product-forward — the natural fit for a Product Hunt-style launch page.
- `future` — a dark, immersive game-style skin for bold, high-impact pages (gaming and tech audiences).

**`actions:catalog`** — every entry-action type Tokei supports: label, description, default points, platform, whether it's trust-based/verifiable, and — for the 28 types writable as an `entry_methods` row — the exact `config` fields `pages:update` accepts for that type. This is the **authoritative** per-type reference; nothing below restates it. Same list for every key (not scoped to your account, no pagination). Flags: `--type <actionType>` (a value matching no action type is `400`).

```sh
tokei-agent actions:catalog --type twitter_follow
```

```json
{
  "success": true,
  "data": {
    "label": "Follow on X",
    "defaultPoints": 3,
    "platform": "twitter",
    "trustBased": false,
    "isEntryMethodRow": true,
    "fields": [
      { "key": "username", "type": "string", "required": true,
        "note": "X/Twitter handle. Checked for presence only — no format validation." }
    ],
    "needs": null
  }
}
```

A field's `group` marks alternatives — write the FIRST field of the group; the rest are claim-validator aliases that satisfy validation but render a dead button on their own (each carries a `note` saying so). `isEntryMethodRow: false` means the type is not writable as an `entry_methods` row at all (it's enabled via a contest setting or a dedicated route instead) — `needs` says which.

**`events:catalog`** — every webhook event Tokei's delivery engine understands: description, `payloadSchema` (the exact shape of the `data` field a subscriber receives), `emitSites` and whether it's `subscribable`. This is the **authoritative** payload reference for `webhooks:create` — read it before assuming a field exists in a delivery. Same list for every key (not scoped to your account, no pagination). Flags: `--type <eventName>` (a value matching no event type is `400`). All 5 events are `subscribable: true` this stage — every one has a real emit site (see Webhooks below).

```sh
tokei-agent events:catalog --type winner.selected
```

## Commands (write — need a read+write key)

**`pages:clone`** — create a page by cloning one you own (`--source <promotionId>`), a named platform template by slug (`--template <slug>` — get slugs from `templates:list`), or omit both to clone the platform starter template. `--template` and `--source` are **alternatives, not combinable** — sending both is `422`; a `--template` slug matching no template is `404`. Template, theme, and entry methods copy verbatim from the source — keep one polished master page per shape and clone it. Capped at **20 API-created pages per account per UTC day** (429 with `Retry-After`). Flags: `--title` (required), `--source`, `--template`, `--description`, `--prize`, `--end-date <iso>`, `--campaign-url`, `--image-url`, `--status draft|active`, `--idempotency-key`, `--data`.

```sh
tokei-agent pages:clone --title "Spring Launch Waitlist" \
  --source 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90 \
  --prize "Lifetime license" --end-date 2026-09-01T00:00:00Z \
  --idempotency-key spring-launch-2026
```

Cloning from a named template instead — list first, then clone by slug:

```sh
tokei-agent templates:list
tokei-agent pages:clone --title "Spring Launch Waitlist" --template product-hunt \
  --prize "Lifetime license" --end-date 2026-09-01T00:00:00Z
```

`--status active` makes the page live immediately at the returned `public_url`; the default is `draft`. Reuse an `--idempotency-key` and you get `409` with the existing page's id in `error.details` instead of a duplicate.

**`media:upload <file>`** — upload an image or video and get back a `public_url` to feed into `pages:update`'s media flags (below). One `multipart/form-data` POST to Tokei: the server checks the file, stores it and answers `201`. Content type is inferred from the file extension (`.jpg`/`.jpeg`/`.png`/`.gif`/`.webp`/`.mp4`/`.webm`/`.mov`); override it with `--content-type <type>` for an extensionless or misnamed file. `application/pdf` is not accepted — only image and video. Prints `{bucket, path, public_url, content_type, filename, size_bytes, backend}` under `data`; use `public_url` as-is rather than building one from `bucket` and `path`.

```sh
tokei-agent media:upload ./hero.png
tokei-agent pages:update 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90 \
  --image-video https://media.tokei.io/api-uploads/u1/<uuid>.png
```

Things that surprise agents:

- **The 4MB cap applies to video as well as images.** This is thin for video; a real clip is likely to exceed it. There is no larger-upload path through this API today.
- **A file over 4MB or under 100 bytes never leaves your machine.** The CLI refuses it before sending, with exit code `2` and a `usage_error` on stderr — see the error-semantics note below.
- **The bytes must match the declared type.** For images and `video/mp4`, the server checks the file's leading bytes, so a misnamed file is a `422` on field `file`, not a mislabelled upload.
- **The 50/day cap counts uploads that pass validation.** A rejected file does not use quota, but a server error after validation still does — so don't loop calling `media:upload` speculatively.
- **The stored object name is always a server-generated UUID.** The `filename` you send (or that the CLI infers from your local path) is validated and echoed back in the response, but never used to name anything — so reusing a filename never collides or overwrites.

**`pages:update <contestId>`** — PATCH a page. Simple fields via flags: `--title`, `--description`, `--start-date <iso>`, `--end-date <iso>`, `--template basic-new|showcase|future|simple`, `--custom-css <css>`, `--dark-mode true|false`, `--primary-color "#7d78c6"`, `--card-width narrow|medium|wide`, and the seven media flags below. Prizes, reward tiers, nulls, or a full body via `--data`. At least one field required; unknown fields are rejected (422). `prizes` (max 20) and `reward_thresholds` (max 50) each **replace the existing list wholesale** — read the current lists with `pages:get` first, modify, and send the complete list back (Rule 3). A future `start_date` pauses new entries until then; setting `end_date` recomputes `days_left` — but a page whose winners have already been drawn rejects any `end_date` write, **setting or clearing**, with `409 WINNERS_ALREADY_SELECTED`. Clearing the date via `--data '{"end_date": null}'` also requires the page to be unpublished: an **active** page must keep a deadline (otherwise it renders as live forever while every signup is rejected), so clearing one returns `422` on field `end_date` — send `{"status": "draft", "end_date": null}` together, or a replacement date. `--title` sets the visible page headline (and the dashboard name), and `--description` accepts basic rich-text HTML which is sanitized on write, so unsupported tags come back stripped.

Appearance flags: `--template` is the page skin (`basic-new`, `showcase` or `future`), stored verbatim as `settings.template` — see the skin guide under `templates:list` for what each looks like and when to pick it. `--dark-mode` is a plain creator-side toggle (column `dark_mode_enabled`) — there is no visitor `prefers-color-scheme` behavior, so this is the only thing that controls it. `--primary-color` must be a hex colour only (3, 4, 6 or 8 digits, e.g. `"#7d78c6"`) — other CSS colour formats (`rgb()`, named colours) are rejected because the value is interpolated into the page's server-rendered `<style>` tag; to reset it to the template default, send `--data '{"primary_color": null}'` (there is no flag spelling for null). `--card-width` accepts the friendly names `narrow`/`medium`/`wide`/`xl` **or** the raw stored Tailwind class directly (`max-w-2xl`/`max-w-3xl`/`max-w-4xl`/`max-w-7xl`); friendly names map `narrow`→`max-w-2xl`, `medium`→`max-w-3xl`, `wide`→`max-w-4xl`, `xl`→`max-w-7xl`, and **reads always return the stored class, never the friendly name** — PATCH `--card-width wide` and the next `pages:get` returns `"max-w-4xl"`.

**`template: "simple"` is the Custom template** (launched 2026-08-10) — bare structural markup the creator styles via `custom_css`, applied on both the hosted page and the widget embed via `--tokei-*` custom properties and `.tokei-simple-*` class hooks. `--custom-css` is a string, max 20KB, server-sanitised on write — `@import`, `<` anywhere, and URLs outside `data:`/Cloudinary/tokei.io are rejected with a `422 VALIDATION_ERROR` naming the reason, so read-back may differ from what was sent; send `--data '{"custom_css": null}'` to clear it (there is no flag spelling for null). `pages:get` returns the stored `custom_css` for any page that has one.

Media flags: `--image-video <url>` (the hero — an image **or** a video), `--secondary-image <url>`, `--third-image <url>`, `--fourth-image <url>`, `--fifth-image <url>` (the additional layout block slots), `--background-image <url>` (interpolated into the page's CSS), `--og-image <url>` (social-share preview). All seven accept only an `https` URL on `media.tokei.io` or `res.cloudinary.com` — exactly what `media:upload`'s `public_url` produces, so the normal flow is `media:upload` then `pages:update` with the URL it printed (Rule 2). There is no flag spelling for clearing a media field to `null`; use `--data '{"og_image": null}'`.

```sh
tokei-agent pages:update 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90 \
  --title "Now with 3 prize tiers" \
  --data '{"prizes":[{"name":"AirPods Pro","winners":1,"value":249,"currency":"USD"},{"name":"Sticker pack","winners":50}]}'
```

```sh
tokei-agent pages:update 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90 \
  --template showcase --dark-mode true --primary-color "#7d78c6"
```

**`entry_methods`** — reachable only via `--data` (max 30 rows, ~64KB body cap on this route only, raised from the shared 10KB to fit it). Seven things to know:

1. **Full-array replace, same as Rule 3 — always `pages:get` → modify → `pages:update`.** There is no per-row patch: `[]` clears every entry method, and omitting the field leaves the stored array untouched. Two row shapes: an **action row** `{id?, actionType, label, points?, config?, requireVerification?}` — `actionType` must be one of the 28 writable types from `actions:catalog` — or a **link row** with no `actionType`: `{id?, label, points?, link, actionsRequired?}` — a plain http(s) button to any URL, for anything the catalog has no action for; `actionsRequired` (0-20) hides the row until the entrant has completed that many other actions; action rows accept it only for `tokei_cross_promote` and drop it otherwise. Unknown keys (`icon`, `config.type`, the ten legacy `<platform>Config` duplicates) are stripped, not stored, so echoing back a row you just read is always safe. `icon`/`config.type` are always server-derived from `actionType`; whatever you send for them is ignored.
2. **`points` may not render as sent.** `0` means unset — the renderer falls back to the type's default. Any type with an `entryValueSettingKey` (see `actions:catalog`) has its displayed points overridden by `settings.<type>_entry_value` when the owner has configured one, and Product Hunt (`producthunt_follow`, `producthunt_vote`) and all three Steam types go further — their points are **hard-substituted with the platform default at render**, unconditionally. Also: **`pages:get` already returns the EFFECTIVE points** (overrides applied), not the raw stored value, so an untouched `pages:get` → `pages:update` round-trip silently persists that effective number into storage in place of whatever was originally configured.
3. **Some types need a deployment prerequisite — warn the human before adding one.** `linkedin_share`/`linkedin_post` need the `linkedin_oidc` provider enabled on this deployment, and all 3 `steam_*` types need Steam login. `actions:catalog`'s `needs` field says this per type — `null` means no prerequisite. X/Twitter, Discord, Facebook, Instagram, TikTok, Twitch, Product Hunt, `linkedin_follow`, `linkedin_company_follow` and link rows have none — safe to add without asking.
4. Draft/publish semantics are unchanged by any of this. Unknown keys are stripped on the way in, never stored.
5. **Link-row rules:** a label that doesn't start with `"Visit Our "` renders as a non-clickable generic row; the clickable, credited path also requires the page to have a `campaign_url` configured.
6. **Rows of one `actionType` are capped, and can carry a stable `id`.** At most 5 rows may share one `actionType` — but only for `twitter_follow`, `instagram_follow` and `facebook_visit_page`; every other type, including one that reads as duplicate-eligible in `actions:catalog`, is capped at 1. Exceeding it is `422 VALIDATION_ERROR`: `Too many "twitter_follow" entry methods (max 5 per promotion).` for the three types above, `Only one "tiktok_follow" entry method is allowed per promotion.` for everything else. `id` (optional, `[A-Za-z0-9_-]`, max 64 chars) gives a row stable identity across a `pages:get` → modify → `pages:update` round-trip. It is optional on input. Every stored row has one, and a row sent without one gets one when it is stored, as a new action. Two rows sharing an `id` is also `422`: `Duplicate entry method id "<id>" (already used at index <n>).`
7. **Changing a row's target keeps credit while it keeps its `id`; omit the `id` to make it a new action.** Entrants who already completed the row keep their credit and are not paid again. The server records the old target in the row's read-only `previousTargets` and `targetSuffix`, and ignores values you send for them. A row sent without its `id` is stored as a new action, so everyone can complete it again. Confirm with the human before doing that on a live page.

```sh
tokei-agent pages:get "$PAGE" | jq '.data.entry_methods'   # always read first (Rule 3)

# Two trust-based rows (no prerequisite) + a link row, sent together as the
# COMPLETE replacement array
tokei-agent pages:update "$PAGE" --data '{"entry_methods":[
  {"actionType":"tiktok_follow","label":"Follow us on TikTok","points":3,"config":{"username":"tokei"}},
  {"actionType":"twitter_follow","label":"Follow on X","points":3,"config":{"username":"tokei"}},
  {"label":"Visit Our Store","points":1,"link":"https://example.com/store"}
]}'
```

**`pages:publish <contestId>`** — sugar over `pages:update` that PATCHes `{"status": "active"}`. Requires an `end_date` in the future — either already stored on the page, or sent in the same call via `--data`. If neither is true, this returns `422 VALIDATION_ERROR` with `details: [{"field": "status", "message": "Publishing requires an end_date in the future..."}]`. Re-publishing an already-active page is a no-op and skips that check. Still accepts `--data` for any other field, merged under the fixed `status` (a `--data` `status` value would override it, but there's no reason to send one here).

```sh
tokei-agent pages:publish 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90
```

The one-call ergonomic path, when the page has no future `end_date` yet — set it and publish together:

```sh
tokei-agent pages:publish 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90 \
  --data '{"end_date":"2026-09-01T00:00:00Z"}'
```

**`pages:unpublish <contestId>`** — sugar over `pages:update` that PATCHes `{"status": "draft"}`. Safe for pages with entrants: entries and entrants are left untouched, and it only blocks new signups. **Unpublishing hides the page:** visitors to its URL see "This promotion isn't open right now" (noindex), and only the owner, signed in to tokei.io, still sees it. `pages:publish` restores it. Nothing is deleted, and there is no way to delete a page through this API (the `status` field only ever accepts `draft`/`active` — `deleted` is rejected).

```sh
tokei-agent pages:unpublish 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90
```

**`entries:create <contestId>`** — add a signup. Flags: `--email` (required), `--name`, `--action-type` (default `api_import`), `--points`, `--value`; `metadata` via `--data`.

```sh
tokei-agent entries:create 4e7a1c0e-8b2d-4f6a-9c3e-2d5b8a7f1e90 \
  --email fan@example.com --name "Ada Lovelace" --points 10 --value "Order #12345"
```

A duplicate email for the same page returns `409` — the person is already signed up; usually safe to treat as success.

**`webhooks:create`** — subscribe an HTTPS endpoint. Flags: `--url` (required), `--events <e1,e2>` (required — one or more of the 5 subscribable events: `entry.created`, `contest.ended`, `winner.selected`, `daily_bonus.claimed`, `referral.converted`; run `events:catalog` for what each payload contains and where it fires from), `--data`. Capped at **10 active subscriptions per account** — the eleventh returns `400 BAD_REQUEST` telling you to delete one first. Get explicit human approval before creating a live webhook (Rule 4) — it starts firing on real events immediately.

```sh
tokei-agent webhooks:create --url https://yourserver.com/webhooks/tokei --events entry.created,winner.selected
```

The response contains the `whsec_` signing secret **exactly once** — it cannot be retrieved again (the CLI also prints a stderr warning). Store it immediately; deliveries are HMAC-SHA256 signed in the `X-TOKEI-Signature` header, expect a 2xx within 10s, and retry with backoff (5s, 30s, 5min).

> **Creator (per-contest) webhooks are separate from this API.** A page owner can also subscribe a webhook from the Tokei dashboard, per contest — those are created via a session-auth route (`src/app/api/promotion/[contestId]/webhooks/route.ts`), not this CLI/API, and are curated to a fixed trio (`entry.created`, `winner.selected`, `contest.ended`) with no event-picker UI. `daily_bonus.claimed` and `referral.converted` stay developer-API-only, reachable only via `webhooks:create` above.

**`webhooks:delete <webhookId>`** — remove a subscription.

```sh
tokei-agent webhooks:delete 9f1b2a3c-4d5e-6f70-8192-a3b4c5d6e7f8
```

## MCP server

`tokei-agent mcp` runs a local MCP server over stdio (newline-delimited JSON-RPC) exposing every command above as an MCP tool — no extra install, zero dependencies. Tool names swap `:` for `_` (`pages:list` → `pages_list`); inputs use the API's wire field names directly (`contest_id`, `per_page`, `prizes`, …) instead of flags, so nested bodies need no `--data`. Results carry the same envelope (`rate_limit` included) as text content, with `isError` set on API failures — the error semantics table below applies unchanged. Register it with an MCP client, e.g. Claude Code:

```sh
claude mcp add tokei --env TOKEI_API_KEY=tokei_k_... -- npx -y tokei-agent mcp
```

## `--data` semantics

Write commands accept `--data '<json>'` or `--data @file.json` for the raw request body (must be a JSON object). Individual field flags are merged **on top of** `--data` — **flags win** on conflict. The merged body is sent to the API untouched: the CLI does no schema validation, so the API's `422` response with per-field `error.details` **is** the validation. Fields only reachable via `--data`: `prizes`, `reward_thresholds`, and nulls (e.g. `{"end_date": null}` clears the end date — only on a page that is not active) on `pages:update`; `metadata` and `marketing_consent` on `entries:create` (`marketing_consent: true` records the participant's consent and is what enables syncing them to the connected email provider — send it only when consent was genuinely collected).

## Error semantics — what to DO per status

| Status | `error.code`          | Meaning                                                                 | Agent action                                                                                     |
| ------ | --------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 400    | `BAD_REQUEST`         | Invalid query parameters, or the 10-active-webhooks cap.                | Fix the request. Do not retry as-is.                                                             |
| 401    | `UNAUTHORIZED`        | Missing, invalid, revoked, or **expired** key.                          | Stop and ask the human for a fresh key. Never retry.                                             |
| 403    | `FORBIDDEN`           | Key is valid but: trial plan (no API access), or the key **lacks the write scope** for a write command. | Do not retry. Ask the human for a read+write key (or a plan upgrade). Not an ownership error.    |
| 404    | `NOT_FOUND`           | Resource doesn't exist **or is not owned by this key's account** — ownership failures are masked as 404. `pages:clone --template <slug>` also 404s when the slug matches no template (`error.details` has `field: "template"`). | Verify the id via `pages:list` / `webhooks:list`, or the slug via `templates:list`. Do not retry. For `webhooks:delete`, a 404 usually means already deleted — safe to treat as success. |
| 409    | `CONFLICT`            | `entries:create`: email already entered. `pages:clone`: idempotency key already used (existing page's id is in `error.details`). | Safe to treat as success in both cases — the desired state already exists. Do not retry.          |
| 409    | `WINNERS_ALREADY_SELECTED` | `pages:update`: `end_date` was set **or cleared** on a page whose winners have already been drawn. | Do not retry. Tell the human the draw is final — they must clear the winner selection in the dashboard first. Other fields still patch fine; just omit `--end-date`. |
| 413    | `PAYLOAD_TOO_LARGE`   | Body over the 10KB limit (`pages:update` alone is raised to 64KB, to fit a full `entry_methods` array). | Shrink the body. Do not retry as-is.                                                             |
| 422    | `VALIDATION_ERROR`    | Body failed validation; `error.details` is an array of `{field, message}`. | Fix exactly the listed fields, then retry once.                                                  |
| 429    | `RATE_LIMIT_EXCEEDED` | Per-minute limit, the 20/day clone cap, or the 50/day media-upload cap. | Wait `Retry-After` seconds (in the response headers), then retry with exponential backoff. On the two daily caps, trust `Retry-After` — `rate_limit` in the envelope reports the per-minute window, which will still look healthy. |
| 5xx    | `INTERNAL_ERROR`      | Server fault.                                                           | Retry with exponential backoff, max 2–3 attempts, then report to the human.                      |
| (none) | `network_error`       | Request never reached the API (DNS, timeout, refused).                  | Retry with backoff a couple of times, then report.                                               |

`media:upload` uses the table above as normal — a rejected content type or bytes that don't match it come back as `422 VALIDATION_ERROR` on field `file`, and the 50/day cap as `429 RATE_LIMIT_EXCEEDED`. A file over 4MB or under 100 bytes is refused locally before any request: exit code `2`, `{"ok": false, "error": {"type": "usage_error", "message": "..."}}` on stderr. Shrink or replace the file; retrying as-is cannot succeed. A `410 GONE` means an old CLI (0.3.5 or earlier) that still requests the retired signed-upload ticket — upgrade `tokei-agent`.

## Self-throttling

Every successful and failed API response includes `rate_limit` in the envelope (from the `X-RateLimit-*` headers). Limits are per account: Subscriber 60 read / 30 write per minute, Lifetime 120 / 60. When `rate_limit.remaining` is low, slow down; when it's 0, sleep until `rate_limit.reset` (Unix epoch seconds) before the next call. Don't burn the budget discovering a 429 — read the envelope you already have.

## Common gotchas

1. **`TOKEI_API_KEY` not set** — exit code `2`, JSON on stderr, nothing sent to the API. Export the key first.
2. **Trial plan gets `403` on everything** — API access needs an active subscription or a lifetime plan. Run `me` first (Rule 1) so this surfaces once, not on every command.
3. **Read-only key gets `403` on writes, and nothing tells you in advance** — `me` doesn't report scope. If the task changes anything, confirm the key is read+write with the human before starting.
4. **Media must go through `media:upload` first (Rule 2)** — raw filenames and external URLs are rejected by the host allowlist on all seven media fields. No exceptions, not even for a quick test.
5. **4MB applies to video too**, and every upload that passes validation counts toward the 50/day media cap — never call `media:upload` speculatively in a loop.
6. **`prizes` and `reward_thresholds` replace the whole list (Rule 3)** — `pages:get` first or you will silently delete the other entries.
7. **`pages:unpublish` hides the page from everyone but the owner** — visitors see "This promotion isn't open right now" and cannot join. Confirm with the user before unpublishing a page that has live traffic.
8. **Publishing needs a future `end_date`** — otherwise `422` on field `status`. Set it in the same call: `pages:publish <id> --data '{"end_date":"..."}'`.
9. **Clearing `end_date` needs `status: draft` in the same body**, and is refused outright with `409 WINNERS_ALREADY_SELECTED` once winners are drawn.
10. **Appearance values don't always read back as written** — `--card-width wide` reads back as `max-w-4xl`. That's correct, not a failed write.
11. **`--primary-color` is hex only** — `rgb()` and named colours are rejected, because the value is interpolated into a server-rendered `<style>` tag.
12. **`404` can mean "not yours"** — ownership failures are masked as not-found. Confirm the id with `pages:list` before assuming the page is gone.
13. **`--status` takes `draft|active|completed|deleted`** — `ended` and `paused` are not real values; older builds accepted them and always returned an empty list.
14. **`--data` is not validated locally** — it is sent untouched and the API's `422` with `error.details` is the validation. Read `.error.details[].field`.
15. **Template slugs change** — always `templates:list` first; never hardcode a slug.

## Quick reference

```sh
# Setup — required before anything else
export TOKEI_API_KEY=tokei_k_...      # read-only unless you need to write
tokei-agent me                        # verify key + plan FIRST (Rule 1)

# Read (any key)
tokei-agent pages:list --status active --per-page 20
tokei-agent pages:get <contestId>
tokei-agent stats <contestId>
tokei-agent leaderboard <contestId> --per-page 10
tokei-agent referrals:top <contestId> --per-page 10
tokei-agent entries:list <contestId> --email fan@example.com
tokei-agent surveys:list <contestId> --page 2
tokei-agent winners:list <contestId>
tokei-agent webhooks:list
tokei-agent templates:list
tokei-agent actions:catalog
tokei-agent events:catalog

# Create (write key)
tokei-agent pages:clone --title "T" --template <slug>          # 20/day cap
tokei-agent pages:clone --title "T" --source <promotionId>     # or clone your own
tokei-agent media:upload ./hero.png                            # ≤4MB, 50 uploads/day

# Update (write key) — read back with pages:get to confirm
tokei-agent pages:update <id> --title "T" --description "<p>D</p>"
tokei-agent pages:update <id> --start-date <iso> --end-date <iso>
tokei-agent pages:update <id> --template showcase --dark-mode true \
  --primary-color "#7d78c6" --card-width wide
tokei-agent pages:update <id> --image-video <public_url> --og-image <public_url>
tokei-agent pages:update <id> --data '{"prizes":[...]}'        # replaces the list
tokei-agent pages:update <id> --data '{"og_image": null}'      # nulls need --data
tokei-agent pages:update <id> --data '{"entry_methods":[...]}' # replaces the list, max 30, 64KB cap

# Publish state (write key)
tokei-agent pages:publish <id> --data '{"end_date":"2026-09-01T00:00:00Z"}'
tokei-agent pages:unpublish <id>                               # hides the page from visitors

# Signups + webhooks (write key)
tokei-agent entries:create <id> --email a@b.com --name "Ada" --points 10
tokei-agent webhooks:create --url https://you.com/hook --events entry.created  # secret shown ONCE
tokei-agent webhooks:delete <webhookId>

# Other
tokei-agent mcp                       # MCP stdio server (all 21 commands as tools)
tokei-agent --help                    # full flag reference
tokei-agent --version
```
