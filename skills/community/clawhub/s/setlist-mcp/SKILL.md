---
name: setlist-mcp
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

All tools are read-only and prefixed `setlist_`.

### Artists
- **`setlist_search_artists`** — find artists by `artistName` or `artistMbid`; returns each artist's MusicBrainz ID (`mbid`).
- **`setlist_get_artist`** — get an artist by `mbid`.
- **`setlist_get_artist_setlists`** — an artist's setlists (most recent first), by `mbid`, paginated via `p`.

### Setlists
- **`setlist_search_setlists`** — search by any mix of artist, venue, city, country, tour, `date` (ISO yyyy-MM-dd), or `year`.
- **`setlist_get_setlist`** — a setlist (with full song list) by `setlistId`.
- **`setlist_get_setlist_version`** — a specific historical version by `versionId`.

### Batch
- **`setlist_resolve_concerts`** — resolve up to **24** `{artist, date, city?, venue?}` to their best-match setlists in one call (with `songCount`/`hasSongs` + a `{matched, stubs, tourReferenced, unmatched, pending}` summary). When a show is an empty stub but the act toured a repeating set, the result also includes a **`tourReference`** — a populated, representative setlist from the *same tour* on a nearby date (with `songs` + its own `url`), clearly labeled as a reference, **not** the exact show (pass `tourFallback: false` to skip). Calls are paced to setlist.fm's rate limit; if a batch can't finish in time the rest come back `pending: true` — re-call with just those. For more than 24 shows, chunk into batches of ≤24.

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

## Typical flows

- **"What did Radiohead play at their last show?"** → `setlist_search_artists` (Radiohead → mbid) → `setlist_get_artist_setlists` (latest) → `setlist_get_setlist` for the song list.
- **"Setlists at Red Rocks in 2023"** → `setlist_search_venues` (Red Rocks → venueId) → `setlist_search_setlists` with `venueId` + `year: 2023`.
- **"Phish on 2023-08-07"** → `setlist_search_setlists` with `artistName: "Phish"`, `date: "2023-08-07"`.

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
