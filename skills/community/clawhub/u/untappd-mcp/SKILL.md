---
name: untappd-mcp
description: Search Untappd beers, breweries, and venues; read user profiles, check-ins, wishlists, distinct beers, badges, friends, and your friend activity feed; and post check-ins, toasts, and comments to your own Untappd account. Use when the user asks about beer ratings, what a beer or brewery is like on Untappd, someone's Untappd check-ins or wishlist, or wants to log/toast/comment on a beer.
---

# Untappd MCP

Talks to Untappd's mobile (v4) API using your own account, calling the same
endpoints the iPad app uses. Authenticates with an access token you already
hold, or mints one via the app's `xauth` endpoint (username + password).

## Setup

Environment variables (the README has the full table and how to capture the
client credentials):

| Variable | Needed | Purpose |
|---|---|---|
| `UNTAPPD_ACCESS_TOKEN` | no | A token you already hold. With it, **no password is needed** — xauth is skipped. When it expires, the server says so; supply a fresh one. |
| `UNTAPPD_USERNAME`, `UNTAPPD_PASSWORD` | if no token | Your Untappd login, used only to mint a token. Accounts with 2FA can't log in this way. |
| `UNTAPPD_CLIENT_ID`, `UNTAPPD_CLIENT_SECRET` | for login & writes | The Untappd mobile app's client credentials. A pre-seeded token can read without them. |
| `UNTAPPD_TIMEZONE` | no | IANA zone check-ins are stamped with when a call omits `timezone`. Defaults to the server's zone. |
| `UNTAPPD_PHOTO_DIR` | no | Directory (or `:`-separated list) a check-in's `photo_path` must be inside. Default `~/Downloads/untappd-mcp`. |
| `UNTAPPD_CACHE_DB` | no | Local check-in cache file (default `~/.untappd-mcp/checkins.db`). Local/stdio only. |

Two things the server enforces that you should plan around:

- **Photos:** pass exactly one of `photo_path`, `photo_inline` or
  `photo_blob_key` (JPEG/PNG, max 15 MB). Locally, `photo_path` must be a file
  inside `UNTAPPD_PHOTO_DIR` (default `~/Downloads/untappd-mcp`); anything else
  (e.g. `~/Pictures/beer.jpg`) is refused — ask the user to move the photo there
  first. On the **hosted connector** a path cannot work: call
  `untappd_upload_slots`, PUT the photo with the returned `curl`, then pass its
  `blobKey` as `photo_blob_key` (or, for a small photo, `photo_inline` base64).
- **Time zone:** on a hosted connector the server usually runs in UTC, so pass
  `timezone` (the drinker's IANA zone, e.g. `America/New_York`) on
  `untappd_checkin` unless `UNTAPPD_TIMEZONE` is set — otherwise the check-in is
  stamped in the server's zone.

Run `untappd_healthcheck` to confirm auth works.

## Read tools

- `untappd_search_beer` / `untappd_beer_info` — find beers, then get full detail by bid.
- `untappd_search_brewery` / `untappd_brewery_info` — breweries.
- `untappd_search_venue` / `untappd_venue_info` — bars, breweries, restaurants.
- `untappd_venue_menu` — a venue's verified beer menu, flattened. Use instead of
  `venue_info` for "what's on tap" — `venue_info` returns only the first section
  of each menu and under-reports large boards. This pages sections under a
  per-call `max_pages` budget (like the sync tools) and is resumable: it returns
  `another_run_needed` + `next_section_offset` when the budget runs out, or
  `truncated` if the upstream stops returning sections short of coverage.
- `untappd_user_info` — a user's profile (omit `username` for your own).
- `untappd_user_checkins` — recent check-ins (page with `max_id`).
- `untappd_user_wishlist` — wishlist beers.
- `untappd_user_beers` — distinct beers ever checked in.
- `untappd_user_badges` / `untappd_user_friends`.
- `untappd_activity_feed` — your friend feed (page with `max_id`).
- `untappd_checkin_info` — full detail of one check-in.

Most user tools default `username` to your configured account when omitted.

## Response shape (`view`)

Thirteen of this server's 46 tools take `view: "compact" | "full"`, and
**`compact` is the DEFAULT** — the slim rung is what you get without asking
for it.

**If you were told to pass `compact: true`, that advice is stale.** It used to
be true: the projection shipped as an opt-in boolean defaulting to `false`,
and the tool descriptions asked the caller to please turn it on. An efficiency
you have to request is one that mostly is not requested — and the caller
paying for the fat record was the one least able to know a slim rung existed.
So it flipped. The old parameter is gone; it is not declared anywhere, so zod
drops the unknown key and the call succeeds. You get the compact rung — right
answer, wrong reason. **The same silence bites the other way**: `compact:
false` no longer buys you the full record either. It is dropped identically
and you still get compact. `view: "full"` is the only way back.

`untappd_activity_feed` also takes a third rung, `view: "brief"`: one line per
check-in, `<user>: <beer> (<brewery>) at <venue> — <ISO date | no date> —
<rated N | not rated>`, each at most 120 characters, answered inside the
untrusted-data envelope as `data: string[]` (the names are other Untappd
users'). A line starting `-- ` is a note, not a check-in: `-- none` for an
empty feed, `-- more` when an older page exists; a name that itself starts
with `-- ` or `\` is escaped with one leading `\`. It is the shape a
context-group host reads aloud (below); use it when you only need to say what
friends have been drinking.

Compact comes in two tiers here, and they are not the same thing:

**A hand-written field projection — 9 tools.**

- Check-ins (`untappd_activity_feed`, `untappd_user_checkins`,
  `untappd_beer_activity`, `untappd_venue_activity`,
  `untappd_local_checkins`): each ~5 KB record becomes `{checkin_id,
  created_at, user, rating, comment, beer{bid, name, style, abv}, brewery,
  venue, toasts, comments, has_photo}`. A default page of 25 was upwards of
  100 KB to learn what someone drank.
- `untappd_search_beer`: each ~1.2 KB match becomes `{bid, name, style, abv,
  ibu, brewery, checkin_count, have_had}` — the long `beer_description` and
  the nested brewery record go.
- `untappd_user_wishlist`: the same beer core plus `added_at`.
- `untappd_user_beers`: the same beer core plus `your_count`, `your_rating`,
  `global_rating`, `last_had`.
- `untappd_brewery_beers`: the same beer core plus `rating`, `rating_count`,
  `checkin_count`, `have_had`, `your_count`. It has its **own** projector
  rather than sharing `untappd_search_beer`'s, and the reason is a trap worth
  knowing: the item shape is identically `{beer:{…}}`-wrapped, but this
  endpoint spells the two surrounding fields `total_count` / `has_had` where
  `/search/beer` says `checkin_count` / `have_had`. Sharing the projector
  would return beers with no check-ins that you had never had, and the
  drift guard would not fire — the container was where it was expected. Per
  page it also drops `sorting_options` and the copy of the same brewery
  object repeated on every row.

**An upstream request for less — 4 tools.** `untappd_user_info`,
`untappd_beer_info`, `untappd_brewery_info` and `untappd_venue_info` forward
`compact=true` to Untappd's own endpoint, which drops the embedded
activity/list blocks server side. **There is no local projection on these**:
the entity's own fields are byte-identical on both rungs. What compact saves
is Untappd's embedded blocks — and the bandwidth, not just the context. Do not
expect a shorter beer record from `untappd_beer_info`; expect the recent-
activity block to be absent.

The projectors are **drift-safe**. Each keys off a documented container
(`checkins.items`, `beers.items`); if that array is not where it is expected —
this is a reverse-engineered API — the projector warns on stderr and returns
the RAW response rather than an empty or wrong one. A short answer is never
silently manufactured.

`view: "full"` returns Untappd's response untouched. There is deliberately
**no `raw` rung**: nothing here re-serialises or normalises a payload, so
`full` already IS the upstream response and a third value would silently alias
one that exists.

### The 33 tools without `view`

Each for its own reason — and none of them will tell you it ignored the
parameter, because an undeclared key is dropped by zod without a warning:

- **The 12 confirmation-gated writes** (`untappd_checkin`, `untappd_toast`,
  `untappd_add_comment`, the two deletes, the wishlist pair, the four friend
  actions, and the local `untappd_cache_forget`) answer with a confirmation preview or a receipt. Nothing in a receipt is
  decoration.
- **`untappd_sync_checkins` / `untappd_sync_user_beers`** answer with sync
  PROGRESS — pages walked, `another_run_needed`, `backfill_complete`. Slimming
  a progress report is how you lose the field that says it is not finished.
- **The five cache tools** (`untappd_cache_has_had`, `…_has_had_many`,
  `…_not_had`, `untappd_cache_query`, `untappd_top_not_had`) answer from the
  local SQLite mirror in a shape this repo already wrote — a verdict plus the
  `freshness` block that says whether a "not found" might be a false negative.
  There is no upstream payload behind them to project away from.
- **`untappd_checkin_info`** exists to return the FULL record for one check-in
  — photos, badges earned, toasts, comments. The ~5 KB the check-in projection
  removes is exactly what you called this tool to get.
- **`untappd_venue_menu`** is already its own hand-written projection, with a
  per-call page budget and a resumable `next_section_offset` contract. A
  second projection on top of it would fight the first.
- **`untappd_resolve`, `untappd_open_url`, `untappd_healthcheck`** return a
  verdict or a diagnostic.
- **The remaining nine reads** — `untappd_trending`, `untappd_notifications`,
  `untappd_search_brewery`, `untappd_search_venue`, `untappd_user_badges`,
  `untappd_user_friends`, `untappd_user_venues`, `untappd_pending_friends`,
  `untappd_venue_by_foursquare` — hand back Untappd's payload as it arrived.
  No projector has been written for their shapes, so there is no rung to ask
  for and **no slim option exists**.

  `untappd_brewery_beers` **used to be tenth on this list and no longer is**
  (#161) — it takes a `view` now, and its field shape is documented with the
  other projections above.

## Write tools (confirmation-gated — these post to your public account)

Each asks the user to confirm first. Where the client can show a confirmation
prompt, it does (unless the server sets `MCP_CONFIRM_ELICITATION=off`). Otherwise the first call makes NO network call and returns
`status: "confirmation-required"` with a `preview` of the exact request and a
`confirmToken`; show the preview to the user, and only after they approve call
the tool again with the same arguments plus `confirmToken`. A token works once
and only for those arguments (a change returns `DRAFT_CHANGED` with a fresh
preview). `MCP_CONFIRM_MODE` on the server can make this `auto` or `refuse`.

- `untappd_toast` — toast/like a check-in (this endpoint is a toggle).
- `untappd_add_comment` — comment on a check-in.
- `untappd_checkin` — post a new beer check-in to your feed (needs a `bid` from
  `untappd_search_beer`; optional `rating` 0–5 in 0.25 steps, `shout`, venue,
  one photo — see **Photos** above).

## Check-in cache

The API can't answer "has this user ever had beer X?" without paging their whole
history (50/page, rate-limited). These tools keep a SQLite mirror so that
question is answered instantly with **no** API calls. On the stdio server the
mirror is a local file (`UNTAPPD_CACHE_DB`, default `~/.untappd-mcp/checkins.db`);
the store is injectable, so another deployment can back it differently. Same tools either way.

**Sync first, then query.** Two sources; both resumable (`max_pages`/call,
progress saved per page, `another_run_needed` until done). Omit `username` for
your own account; another user must be public or your friend.

- `untappd_sync_user_beers` — **start here for has-had questions.** Pages the
  user's COMPLETE distinct-beers list (cheap, and pages fully for anyone).
- `untappd_sync_checkins` — detailed check-ins (venue/date). Only your OWN
  account pages fully; for anyone else Untappd returns just the recent ~50 and
  the result reports `history_truncated` (it won't falsely claim
  `backfill_complete`). `force_backfill: true` resets a cache wrongly marked
  complete and re-pages (rows kept).

Query tools (has-had ones consult BOTH sources — a hit in either = had):

- `untappd_cache_has_had` — has the user had a beer? By exact `bid` or a
  case-insensitive `beer_name` substring.
- `untappd_cache_has_had_many` — batch had/not-had for a list of `bids`.
- `untappd_cache_not_had` — from a list of `bids`, the ones NOT had.
- `untappd_top_not_had` — from a list of `bids`, the top N NOT-had beers by
  Untappd rating, with an optional `style` filter ("what should I order off this
  tap list?"). Uses a `beer_meta` cache; calls `beer/info` only on miss/stale,
  capped at `api_budget` per run (partial/another_run_needed when exceeded).
- `untappd_cache_query` — filter cached check-ins by brewery, style, `min_rating`,
  venue, and date range.
- **Groups:** `untappd_cache_has_had_many` and `untappd_top_not_had` take
  `usernames` (instead of `username`) plus `mode`: `none_had` (default — new to
  everyone) or `any_not_had` (at least one of them still needs it). Each beer
  lists `had_by` / `not_had_by`; freshness is reported per user.
- `untappd_sync_venue_drinks` — opt-in, costs one call per check-in: fetches the
  beer from each cached venue's first/recent visit (`checkin/view`), budgeted by
  `max_calls`; `untappd_cache_has_visited` then shows them as `drinks`. Partial
  by design (two check-ins per venue at most).
- **Favorites** (local, no API): `untappd_favorites_list` (filter `kind`
  beer|brewery|venue, `source` derived|manual|untappd, override `thresholds`),
  `untappd_favorite_add` / `untappd_favorite_remove` (manual, with a note —
  never written to Untappd). Derived defaults: venue ≥5 check-ins or ≥3 distinct
  months; brewery ≥5 beers with avg ≥3.75, or ≥15 beers; beer rated ≥4.25 or
  had ≥3 times. has_had / has_had_many / has_visited / brewery_beers / venue_menu /
  top_not_had results carry `favorite` {is_favorite, sources, reason};
  `untappd_top_not_had` boosts wishlisted (+0.5) and favorite-brewery (+0.25)
  beers unless `prefer_favorites: false`. `untappd_sync_brewery_likes` mirrors
  the breweries a user likes/follows on Untappd (resumable, rate-guarded); they
  carry the source `untappd` (merged with derived/manual) and count for the boost.
  Untappd has no followed-venue list, so venue favorites are derived + manual.
  `brewery_info`'s `follow_status` is the signed-in account's, never another user's.
- `untappd_trip_check` — a whole trip in one call: per stop (`venue_id`, `name`
  + `city`/`state`, `lat`/`lng`, and/or `brewery_id`) → visited with dates,
  beers had from that brewery, and the top N (default 4) not-had beers by global
  rating (`style` filter). Cache only, except `brewery/beer_list` for a missing or
  >7-day-old list (`api_budget`, default 5; 0 = cache only). Flags favorite
  venues/breweries, boosts wishlist/favorite-brewery beers (`prefer_favorites`),
  and hints when a favorite venue is within `near_favorite_radius_m` (2 km).
  Sync first: `untappd_sync_user_venues`, `untappd_sync_user_beers`,
  `untappd_sync_wishlist`, `untappd_sync_brewery_likes`.

**Retention.** The cache keeps what you sync until you remove it — including
friends' dated check-ins, comments and venues. `untappd_cache_forget` (confirmation-gated)
deletes one user's check-ins, distinct beers and sync state from the LOCAL cache
only; Untappd is untouched and a later sync can re-fetch. The file is created
owner-only (dir `0700`, file `0600`).

Every cache read returns a `freshness` block reporting each source's completeness
separately (plus `coverage_complete` and a `caveat` when incomplete), so you can
flag a "not found" as possibly a false negative until the relevant sync finishes.

## In context groups

On an mcp-host connector this server is a member of the **food** group (every
tool but `untappd_healthcheck` carries a `_meta.mint` hint with
`domain: "food"`). Its one canonical read is **`untappd_activity_feed`** for
**what's new** — the friend feed, answered with `view: "brief"`. It takes no
subject and no date range: Untappd has no listable set of the person's own
subjects (no children, properties or accounts to fan out over), so the group
asks it once, not once per person. Nothing here answers what's due or what's
on; every other read is a `lookup` (`untappd_notifications` is a non-canonical
what's-new), and the writes are `send` (toast, comment, friend request),
`change` (check-in, deletes, wishlist, favourites, friend accept/reject/remove)
or `other` (the cache syncs and the pickers, which refresh the local cache as
they read).

A compound ask looks like *"what's new with food — any new reservations, and
what have my friends been drinking?"*: the host answers the Untappd half from
the feed's brief lines beside the group's other members. This server calls the
Untappd API directly, so it never answers "needs your browser open"; if it is
not configured, the group reports it as unable to answer and
`untappd_healthcheck` says which credential is missing.
