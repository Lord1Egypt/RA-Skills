---
name: setlist-fpx
description: >-
  Query and update setlist.fm from a shell without running the setlist-mcp
  server — search/read concert setlists, artists, venues, cities, and users
  via plain curl against the public REST API (an x-api-key header), and
  toggle "I was there" attendance on a setlist via the authenticated website,
  using an fpx-captured session cookie. Use when you want setlist.fm data or
  want to mark/unmark attendance without the MCP, in a script, or on a
  machine where the MCP isn't installed.
---

# setlist.fm via curl + fpx (no MCP)

setlist.fm is **hybrid**: reads and writes use two different surfaces.

- **Reads** — a documented public REST API (`api.setlist.fm/rest`) keyed by
  an **`x-api-key` header**. Plain `curl`, no browser, no fpx.
- **Writes** — the only mutation setlist.fm offers is the site's "I was
  there" attendance toggle, and it exists **only on the logged-in website**
  (`www.setlist.fm`, server-rendered Apache Wicket), not the REST API. There's
  no login form to script — the credential is your browser's session cookie.
  `fpx` lifts that cookie out of your signed-in tab **once**; every actual
  request afterward is plain `curl` carrying it. No bridge round-trip per call.

This is the same data/actions the `setlist_*` MCP tools expose, reached with
`curl` instead of a running server.

## Part 1 — reads (curl + API key)

### One-time setup

Apply for a free key at <https://www.setlist.fm/settings/api>, non-commercial
use only (see API terms below), then:

```sh
export SETLIST_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Core call

```sh
curl -s 'https://api.setlist.fm/rest/1.0/search/artists?artistName=Radiohead' \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' \
  | jq '.artist[] | {name, mbid, url}'
```

`Accept: application/json` is required — the API serves XML otherwise.
Optional `Accept-Language: en|es|fr|de|pt|tr|it|pl` localizes city/country
names. Standard tier is **~2 req/sec, 1440/day** — a 429 means slow down.

**Dates are `dd-MM-yyyy` on the wire** (NOT ISO) for `date` search params and
`lastUpdated` (`yyyyMMddHHmmss`); `eventDate` comes back the same way in
responses — convert both directions yourself (the MCP does this for you via
`dmyToIso`/`isoToDmy`; a shell one-liner: `date -j -f '%Y-%m-%d' '+%d-%m-%Y'`
on macOS).

The full request catalog (all 15 read endpoints, params, and `jq` projections)
is in `references/rest-api.md`.

### The one rule: chain ids, don't guess them

Every entity is keyed by an id you get from a search: artists by **`mbid`**
(MusicBrainz id), setlists by **`setlistId`**, venues by **`venueId`**,
cities by **`geoId`**. Search first, then feed the id into the matching
`get`/`setlists` endpoint. Got a setlist.fm URL instead of an id? The id is
the trailing hex token before `.html`, e.g.
`.../setlist/.../...-4ba8a766.html` → `4ba8a766` — no fetch needed.

### Attribution (compliance, not optional)

The API terms require a **followable link** to setlist.fm wherever this data
is shown. Every artist/setlist/venue object has a `url` — surface it as a
clickable link (no `nofollow`) when you present the data. Also: **no
persistent caching** (fetch live each time, don't build a local store) and
**non-commercial use only** on the free key.

## Part 2 — the attendance write (fpx-captured cookie + curl)

There is no API for this — it's the logged-in **website's** Wicket AJAX
control, so you need your own `www.setlist.fm` session cookie.

### One-time setup

```sh
npm install -g @fetchproxy/cli                      # provides `fpx`
fpx profile add setlist --domain setlist.fm          # apex scope
fpx pair -p setlist                                  # prints a pair code → approve in ContextMint Bridge
```

Requirements: **ContextMint Bridge** installed ([releases](https://github.com/nullnet-app/contextmint-bridge/releases) — Chrome: load the chrome zip unpacked; Safari isn't available yet, so use Chrome for now), an open, **signed-in**
`www.setlist.fm` tab, and Chrome **Site access** allowing `setlist.fm`.
Pairing persists after the first approval.
ContextMint Bridge is the renamed fetchproxy extension (same maintainer; [fetchproxy README](https://github.com/chrischall/fetchproxy#extension)); source at [nullnet-app/contextmint-bridge](https://github.com/nullnet-app/contextmint-bridge) — build it, or verify a release zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`.

### Capture the session cookie (once per shell session)

The session cookie (`JSESSIONID`) is **HttpOnly** — only `fpx cookies`
(which uses `chrome.cookies.get`, not page JS) can read it:

```sh
COOKIE=$(fpx cookies -p setlist --domain www.setlist.fm \
  | jq -r '[.JSESSIONID, .RememberMeCookie, .["aws-waf-token"]]
           | map(select(. != null)) | join("; ")')
```

`JSESSIONID` (Wicket session) or `RememberMeCookie` (remembered login) must
be present — if both are empty you're not signed in on that tab. `COOKIE` is
now a ready-to-send `Cookie:` header value; every `curl` below reuses it. A
browser-like `User-Agent` is required too — the bare curl default trips the
site's bot heuristics:

```sh
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
```

### Toggle attendance

Full walkthrough (resolve the setlist URL, fetch the page, parse the toggle
control, replay it, verify) is in `references/attendance-write.md` — it's
several steps, not a one-liner, because the control is a per-render Wicket
AJAX anchor you must parse out of the page HTML first.

**Always dry-run first**: read the page, check the control's current state,
and only send the AJAX toggle if it doesn't already match what you want.
**Never trust the toggle's response status as proof** — always re-fetch the
page afterward and re-check the control's state.

## Exit codes / failure modes

- **Read path (curl)**: a non-2xx from `api.setlist.fm` is a normal HTTP
  error — `403` on a valid-looking key usually means a bad/revoked key, not
  "no key" (that's a `401`).
- **Write path (fpx)**: `fpx cookies` exit codes — `2` bridge unavailable
  (extension not connected / not paired → `fpx pair -p setlist`), `3` bot
  wall, `4` upstream non-2xx. Once you have `COOKIE`, subsequent `curl`
  failures are yours to diagnose (see "session expired" below) — `fpx` is
  out of the loop.
- **Session expired mid-session**: a page fetched with your cookie renders
  **logged out** (a `href="/signin"` or `/login` link instead of the
  attendance control) — re-run the cookie capture (re-approve in ContextMint Bridge
  if needed) and retry.

## Notes

- Reads need no session at all — keep `SETLIST_API_KEY` and the fpx cookie
  capture on completely separate paths, same as the MCP does.
- `fpx health -p setlist` shows bridge connection state if the cookie
  capture fails outright.
- This project is developed and maintained by AI (Claude).
