---
name: setlist
description: Look up concert setlists and live-music history via setlist.fm. Use when the user asks what songs an artist played at a show, their tour setlists, what was performed at a venue or on a date, or wants to find concerts by artist, venue, city, or year. Triggers on phrases like "what did Radiohead play at...", "Phish setlist for...", "shows at Red Rocks", "what songs were played on this tour", or any request about concert setlists, gigs, tours, or live performances. Requires setlist-mcp installed and the setlist server registered (see Setup below).
---

# setlist-mcp

MCP server for setlist.fm — search concert setlists, artists, venues, and tours via natural language. Read-only (setlist.fm has no write API).

- **npm:** [npmjs.com/package/setlist-mcp](https://www.npmjs.com/package/setlist-mcp)
- **Source:** [github.com/chrischall/setlist-mcp](https://github.com/chrischall/setlist-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "setlist": {
      "command": "npx",
      "args": ["-y", "setlist-mcp"],
      "env": {
        "SETLIST_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Option B — from source

```bash
git clone https://github.com/chrischall/setlist-mcp
cd setlist-mcp
npm install && npm run build
```

Then add to `.mcp.json`:

```json
{
  "mcpServers": {
    "setlist": {
      "command": "node",
      "args": ["/path/to/setlist-mcp/dist/index.js"],
      "env": {
        "SETLIST_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Or use a `.env` file in the project directory with `SETLIST_API_KEY=<value>`.

### Getting your API key

Apply for a free API key (non-commercial use) at [setlist.fm/settings/api](https://www.setlist.fm/settings/api) — you'll need a setlist.fm account. The key is sent as the `x-api-key` header on every request.

Optional: set `SETLIST_ACCEPT_LANGUAGE` (one of `en, es, fr, de, pt, tr, it, pl`) to localize city/country names.

## Tools

All tools are prefixed `setlist_`. Everything below is read-only; the two
attendance tools (`setlist_mark_attended` / `setlist_unmark_attended`) write to
your setlist.fm account. Each undoes the other, so neither asks for a
confirmation step.

### Artists
- **`setlist_search_artists`** — find artists by `artistName` or `artistMbid`; returns each artist's MusicBrainz ID (`mbid`).
- **`setlist_get_artist`** — get an artist by `mbid`.
- **`setlist_get_artist_setlists`** — an artist's setlists (most recent first), by `mbid`, paginated via `p`.

### Setlists
- **`setlist_search_setlists`** — search by any mix of artist, venue, city, country, tour, `date` (ISO yyyy-MM-dd), or `year`.
- **`setlist_get_setlist`** — a setlist (with full song list) by `setlistId`.
- **`setlist_get_setlist_version`** — a specific historical version by `versionId`.

### Batch
- **`setlist_resolve_concerts`** — resolve up to **24** `{artist, date, city?, venue?}` to their best-match setlists in one call (with `songCount`/`hasSongs` + a `{matched, stubs, tourReferenced, unmatched, pending, errored}` summary). When a show is an empty stub but the act toured a repeating set, the result also includes a **`tourReference`** — a populated, representative setlist from the *same tour* on a nearby date (with `songs` + its own `url`), clearly labeled as a reference, **not** the exact show (pass `tourFallback: false` to skip). Calls are paced to setlist.fm's rate limit; if a batch can't finish in time the rest come back `pending: true` — re-call with just those. A concert whose lookup fails upstream comes back with `match: null` and an `error` (counted in `errored`) without sinking the batch. For more than 24 shows, chunk into batches of ≤24.

### Venues
- **`setlist_search_venues`** — find venues by `name` and/or location.
- **`setlist_get_venue`** — get a venue by `venueId`.
- **`setlist_get_venue_setlists`** — setlists performed at a venue, paginated via `p`.

### Cities & countries
- **`setlist_search_cities`** — find cities by `name`/location; returns each city's `geoId`.
- **`setlist_get_city`** — get a city by `geoId`.
- **`setlist_search_countries`** — list all supported countries and their codes.

### Users
- **`setlist_get_user`** — a user's public profile by `userId`.
- **`setlist_get_user_attended`** — concerts a user marked as attended.
- **`setlist_get_user_edited`** — setlists a user has created or edited.

### Utility
- **`setlist_healthcheck`** — verify the API key works and the API is reachable.

## Response shape (`view`)

Fifteen tools take `view: "compact" | "full"` — every search and every getter
above, from `setlist_search_artists` through `setlist_get_user_edited` — and
**`compact` is the default**. The slim rung arrives without being asked for,
because an efficiency a caller has to know about and request is one that
usually is not requested.

**Compact strips image and avatar URLs, and claims no field projection.** These
tools hand setlist.fm's payload back close to verbatim, and this repo holds no
captured fixture or documented field list for those endpoints — so nothing here
can honestly say which of setlist.fm's fields matter and which are noise.
Stripping media needs no such knowledge and is subtractive, so it cannot lose a
field nobody knew about; an invented field list would risk returning a record
with holes in it that still reads like a verified answer. Expect the same
record minus the picture URLs, not a named field set.

Note what this does **not** touch: a setlist's `url` is not a media URL, and it
is the link setlist.fm's API terms require you to show — it survives BOTH rungs,
and `tests/view.test.ts` pins that. Compact is not a reason to drop attribution.

In practice that leaves compact with little to remove: none of the setlist.fm
payloads captured in this repo carry a media key at all, so today the two rungs
are usually the same bytes. The rung is there so that a field arriving later
with a picture in it is stripped by default, rather than after somebody notices.

`view: "full"` returns setlist.fm's payload untouched. There is **no `raw`
rung**: `full` already IS the untouched payload, so a third value could only
alias it.

The other five tools take no `view`, each for its own reason:

- **`setlist_resolve_concerts`** already answers in its own shape. It builds
  the `{matched, stubs, tourReferenced, unmatched, pending, errored}` summary and the
  per-show rows itself, unconditionally — that projection IS the tool's output,
  not a slimmed copy of an upstream payload, so there is no fatter version to
  offer. A `view` here would be a parameter that decides nothing.
- **`setlist_id_from_url`** parses an id out of a URL string. No network call,
  no payload, nothing to project.
- **`setlist_mark_attended` and `setlist_unmark_attended`** are writes. A
  write's response is a receipt — a status, an id — with nothing to strip and
  everything to keep.
- **`setlist_healthcheck`** answers whether the API key works and the API is
  reachable.

## Typical flows

- **"What did Radiohead play at their last show?"** → `setlist_search_artists` (Radiohead → mbid) → `setlist_get_artist_setlists` (latest) → `setlist_get_setlist` for the song list.
- **"Setlists at Red Rocks in 2023"** → `setlist_search_venues` (Red Rocks → venueId) → `setlist_search_setlists` with `venueId` + `year: 2023`.
- **"Phish on 2023-08-07"** → `setlist_search_setlists` with `artistName: "Phish"`, `date: "2023-08-07"`.

## In context groups

On a host that groups MCPs by context (mcp-host's context groups), this server
sits in the **family** group. It carries `lookup` hints on its reads (setlists,
artists, venues, cities, users, the batch resolver), an `other` hint on the
local `setlist_id_from_url` parser, and `change` hints on the two "I was there"
attendance writes, with the words people say ("concert", "setlist", "gig",
"venue", "my concerts", "i was there") as aliases.

It has **no canonical read and no subject**: setlist.fm records shows that
already happened, so nothing in it answers "what's new", "what's due" or
"what's on" for a person, and it has no listable set of people or accounts to
fan out over. A compound family ask ("what's on this weekend, and what did that
band play last night?") reaches it only for the second half, as an ordinary
lookup. The reads need only the API key and never a browser; the attendance
writes may use the fetchproxy browser bridge, so on a host where that bridge
signs them in, they answer "needs your browser open" when no signed-in
setlist.fm tab is connected.

## Attribution & API terms

setlist.fm's [API terms](https://www.setlist.fm/help/api-terms) bind anyone using this data. When you present setlist.fm results to a user:

- **Always cite the source.** Each setlist/artist/venue result includes a `url` — show it as a real, clickable link to setlist.fm (e.g. "Source: [The Beatles setlist on setlist.fm](https://www.setlist.fm/...)"). The terms require a *followable* link — never a `nofollow`. If a particular result has no `url`, link to https://www.setlist.fm instead.
- **Non-commercial use only.** A free API key covers non-commercial use; commercial use needs setlist.fm's permission.
- **Live data, not a datastore.** The terms forbid persistent caching — this server fetches fresh on every call and you should treat results as point-in-time, not build a local copy.
- **Don't expose or share the API key.** It's read from `SETLIST_API_KEY` and never appears in results.

## Interpreting setlist data

- Songs live in `sets.set[]`; each set may have an `encore` number (1 = first encore) and a `name` (e.g. an acoustic set or a full album).
- Each `song` may carry: `tape: true` (a pre-recorded intro/outro — not actually performed live), `cover` (the original artist when it's a cover), `with` (a guest performer), and `info` (a note like "acoustic" or "first time live"). Surface these when relevant rather than dropping them.

## Notes

- **Stub setlists:** every setlist result carries `songCount` / `setCount` / `hasSongs`. A page can exist with no songs logged (`hasSongs: false`) — skip those without a second `get_setlist` call.
- **Disambiguate by location:** `artistName` + `date` can return shows in multiple cities. Add `cityName`/`cityId` or `venueName`/`venueId` to pin the right one (e.g. TSO on a date plays both Charlotte and Orlando).
- **All performers at a venue/festival on a day:** call `setlist_search_setlists` with `venueName` (or `venueId`) + `date` and **no** artist.
- IDs chain: `search_*` tools return the `mbid` / `setlistId` / `venueId` / `geoId` you feed into the `get_*` tools.
- **All dates are ISO `yyyy-MM-dd`** — both the `date`/`lastUpdated` inputs and every `eventDate` in the output. (The server translates to/from setlist.fm's native `dd-MM-yyyy` internally.)
- Results are paginated; pass `p` (1-based) to page through large result sets.
- setlist.fm rate-limits the standard tier (~2 req/sec); a 429 is retried once.
