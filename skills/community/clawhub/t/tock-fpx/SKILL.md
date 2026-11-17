---
name: tock-fpx
description: >-
  Query Tock (exploretock.com — restaurant discovery, availability, and the
  signed-in user's reservations) from a shell with the fpx CLI
  (@fetchproxy/cli) instead of running the tock-mcp server — list metros,
  search a metro's restaurants, get a venue's bookable calendar, and list
  reservations, all through a signed-in browser tab. Use when you want Tock
  data without the MCP, in a script, or on a machine where the MCP isn't
  installed.
---

# Tock via fpx (no MCP)

`www.exploretock.com` sits behind a Cloudflare managed challenge — a plain
`curl`/Node request 403s every path (`cf-mitigated: challenge`, a "Just a
moment..." interstitial), including `/city` and `/{slug}`. There is no
server-side login form and no consumer token exchange. `fpx` routes the
request through the user's own signed-in browser tab (the ContextMint Bridge
extension), which has already cleared the challenge, so the same fetch
succeeds. Browsing (metros, search, venue detail, availability) needs no Tock
login at all — just an open, challenge-cleared tab; only the reservations
list needs the tab **signed in**.

This is the same data the `tock_*` MCP tools return, reached with one-shot CLI
calls instead of a running server. It is **read-only** — see "Why no
booking/cancel" below.

## One-time setup

```sh
npm install -g @fetchproxy/cli              # provides `fpx`
fpx profile add tock --domain exploretock.com
fpx pair -p tock                             # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed (from
https://github.com/nullnet-app/contextmint-bridge/releases — Chrome: load the chrome zip
unpacked; Safari isn't available yet, so use Chrome for now), with an open
`www.exploretock.com` tab (signed in, for the reservations tool only), and its
Chrome **Site access** allowing `exploretock.com`. Pairing persists — after the
first approval every later `fpx` call reuses it. ContextMint Bridge is the fetchproxy extension under its new name, same maintainer; its source is public at https://github.com/nullnet-app/contextmint-bridge — build it yourself or check a release zip against its published `.sha256` file.

## Two call shapes

Tock has two different backends behind the same bridge:

1. **SSR pages** (`/city`, `/city/{slug}`, `/{slug}`, `/{slug}/search`) — an
   ordinary GET returns full HTML with the entire dataset embedded as a JS
   object-literal assignment: `window.$REDUX_STATE = {"app":{...},
   "consumerPage":{...}, "calendar":{...}, ...}`. It is **not** JSON — absent
   fields are the bare identifier `undefined`, so `jq` can't parse the raw
   response. Use the bundled `references/extract-redux-slice.mjs` (a faithful
   port of the MCP's own `src/redux-state.ts`) to pull one named slice out as
   real JSON, then pipe that to `jq`:

   ```sh
   fpx get 'https://www.exploretock.com/city' -p tock \
     | node references/extract-redux-slice.mjs app \
     | jq '.metros // . | length'
   ```

2. **Authenticated GraphQL** (`/api/graphql/<OperationName>`) — used only for
   the signed-in patron's reservations, which are lazy-loaded client-side and
   never appear in the SSR store. Clean JSON in and out — pipe straight to
   `jq`:

   ```sh
   fpx post-json 'https://www.exploretock.com/api/graphql/PatronReservationHistory?opname=PatronReservationHistory' \
     @body.json -p tock | jq '.data.purchases'
   ```

Ready-to-run paths/bodies for both shapes, plus the exact GraphQL document and
jq recipes, are in `references/requests.md`.

## The one rule: resolve the metro before searching

Tock's `/city/{slug}` search takes a **metro slug** (from `/city`'s `app`
slice, e.g. `"chicago"`), never a free-text city name. A venue's own page path
is its `domainName` slug (from a search result, or the
`exploretock.com/{slug}` URL directly) — no numeric-id resolution needed
beyond that.

## Exit codes (fetch verbs)

- `0` — success. For GraphQL, a `0` HTTP status can still carry an `errors`
  array in the body — check `jq '.errors // empty'`.
- `2` — bridge unavailable: extension not connected or pairing pending → run
  `fpx pair -p tock`, confirm an exploretock.com tab is open.
- `3` — bot wall: the tab hasn't cleared the Cloudflare challenge → open/
  refresh a `www.exploretock.com` tab and retry.
- `4` — upstream non-2xx from Tock (e.g. a bad slug → 404).

A non-JSON 2xx body on the GraphQL path is almost always a bot-challenge or
sign-in interstitial slipping through, not real data — don't blindly
`JSON.parse` it.

## Why no booking/cancel

Tock's booking/checkout/cancel flow is a stateful **protobuf** transaction
(`/api/ticket/*`) authenticated by app-injected `X-Tock-Authorization` /
`X-Tock-Session` / `X-Tock-Fingerprint` request headers set by Tock's own JS
interceptor — not cookies. A bridge fetch (fpx included) only carries the
tab's cookies, so replaying the protobuf calls 404s
(`"Unknown business identifier"`). Reconstructing those headers would mean
harvesting the user's live session secrets or forging an anti-bot device
fingerprint — both out of scope. This skill (like the MCP) stays read-only;
book/cancel on exploretock.com itself. Full detail: `docs/TOCK-API.md` in the
tock-mcp repo.

If a booking was made outside this skill (on the site, by hand or by UI
automation), treat it as **confirmed** only when a confirmation ID/URL/email
was captured **and** it shows up in a `PatronReservationHistory` re-query
afterward; otherwise report it as "attempted, unverified." The post-booking
modal is not proof (a stale-cart confirm is a silent no-op that still renders
it), and the reservations backend lags the Reservations tab by minutes — an
immediate empty re-read proves nothing.

## Notes

- `fpx health -p tock` shows bridge connection state when a call fails.
- Reservations/profile calls need a **signed-in** tab; browsing does not.
- This project is developed and maintained by AI (Claude).
