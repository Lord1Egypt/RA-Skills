---
name: tock-mcp
description: Discover restaurants on Tock (exploretock.com) via MCP — list cities, search a metro, and get a venue's details plus its bookable experiences, prices, party sizes, and open dates/times. Triggers on phrases like "search Tock for", "what's on Tock in Chicago", "find a Tock reservation at", "does Alinea have availability on Tock", "what experiences does <venue> offer on Tock", or "my Tock reservations". Requires tock-mcp installed and the ContextMint Bridge browser extension running in a signed-in exploretock.com tab.
---

# tock-mcp

MCP server for Tock (exploretock.com) — restaurant discovery and availability. Every request is relayed through the user's signed-in browser tab via the [ContextMint Bridge](https://github.com/nullnet-app/contextmint-bridge/releases) browser extension, so there's no cookie paste, no bot-wall dance, and no password handling.

- **npm:** [npmjs.com/package/tock-mcp](https://www.npmjs.com/package/tock-mcp)
- **Source:** [github.com/chrischall/tock-mcp](https://github.com/chrischall/tock-mcp)

> Tock does not publish an official consumer API, and exploretock.com sits behind a Cloudflare challenge. This server fetches the same server-rendered pages the Tock web app uses (parsing their embedded `window.$REDUX_STATE` store) through your own signed-in browser tab. It is **read-only**: Tock reservations are prepaid tickets, so booking is left to exploretock.com. Use at your own discretion.

## Setup

The MCP server is half of the picture — the other half is the [ContextMint Bridge](https://github.com/nullnet-app/contextmint-bridge/releases) browser extension that talks to Tock from your signed-in tab. Both are required.

### 1. Install the MCP server

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "tock": {
      "command": "npx",
      "args": ["-y", "tock-mcp"]
    }
  }
}
```

Or from source:

```bash
git clone https://github.com/chrischall/tock-mcp
cd tock-mcp
npm install && npm run build
# then point .mcp.json at dist/bundle.js
```

### 2. Install ContextMint Bridge

tock-mcp shares a single browser extension, ContextMint Bridge, with every other fetchproxy-based MCP. Install it once from [its releases page](https://github.com/nullnet-app/contextmint-bridge/releases) — in Chrome, unzip the chrome zip and load it unpacked (`chrome://extensions` → Developer mode → Load unpacked); Safari isn't available yet, so use Chrome for now. ContextMint Bridge is the fetchproxy extension under its new name, same maintainer; its source is public at https://github.com/nullnet-app/contextmint-bridge — build it yourself or check a release zip against its published `.sha256` file. Then open **exploretock.com** and sign in (only needed for the account tools; discovery works signed-out).

### 3. Approve the one-time pair code

The first tool call prints a pair code to approve in the ContextMint Bridge popup (trust-on-first-use, per identity). Run `tock_healthcheck` to trigger it, approve the code, and you're paired for good.

## Tools

| Tool | What it does |
| --- | --- |
| `tock_list_metros` | List Tock cities/metros (name, slug, business count). Filter by name/country. |
| `tock_search_restaurants` | List / search venues in a metro slug (cuisine, price, neighborhood, slug). |
| `tock_get_restaurant` | Venue details + its bookable experiences (prices, party sizes). |
| `tock_get_availability` | A venue's bookable calendar: experiences, prices, open dates/times. |
| `tock_list_reservations` | The signed-in user's purchases / reservations (needs a signed-in tab). |
| `tock_get_profile` | The signed-in user's profile (needs a signed-in tab). |
| `tock_verify_reservation` | After a booking attempt, re-query the account and return `confirmed` / `cancelled` / `not_found` / `ambiguous` (needs a signed-in tab). Use this instead of eyeballing a success screen. |
| `tock_healthcheck` | Round-trip the bridge; reports status + the pair code on first run. |

## Response shape (`view`)

Two tools take `view: "compact" | "full"` — `tock_get_restaurant` and
`tock_get_profile` — and **`compact` is the default**, so you get the slim
rung without asking for it. `tock_list_reservations` takes a different
`view: "full" | "brief"` (below, "In context groups"). The other five of this
server's eight tools have no `view`; each for its own reason, below.

**Compact here is media stripping, not a field projection.** `src/view.ts`
holds no hand-written field list, because this repo has no captured Tock
payload to derive one from honestly. What it does instead is subtractive: drop
keys whose value is a picture, plus **two named explicitly** —
`profileImageUrl` and `heroImageUrl`.

Naming those two is the load-bearing part, and it is worth knowing why. The
shared rule anchors its media noun at the START of the key, which is what
keeps a flag like `hasThumbnail` alive — and it is also why `profileImageUrl`
(starts `profile`) and `heroImageUrl` (starts `hero`) both slip past it. That
would leave only the fallback rule, which fires when a URL's path happens to
end in an image extension. A signed or extension-less Tock CDN URL would then
survive compact silently, with nothing in the response to say why. Naming the
keys removes the dependency on what a URL happens to look like.

Those two are the only image fields any parsed shape in this server carries —
they live on `RestaurantDetails` and nowhere else — and **nothing is kept**:
no tool here has a picture as its product, so no payload mixes decoration with
content.

Expect one specific non-effect: on **`tock_get_profile` compact provably
removes nothing.** The identity record is four fields (`firstName`,
`lastName`, `email`, `id`), none of them a picture, so both rungs serialise to
the same bytes. The rung is declared there for consistency, not for savings.

`view: "full"` returns the parsed record untouched. There is deliberately **no
`raw` rung**: `full` already IS the record this server parsed out of Tock's
page, so a third value would silently alias one that exists.

Why the others have no compact rung:

- **`tock_search_restaurants`** returns `RestaurantSummary`, which carries no
  image key at all — the two image fields exist only on the *details* shape.
  That is exactly why one of the two restaurant tools has a rung and the other
  does not; it is not an omission.
- **`tock_list_metros`** returns hand-built metro records (name, slug, state,
  country, business count, coordinates). No picture, and no fatter upstream
  shape behind them to project away from.
- **`tock_get_availability`** returns an ASSEMBLED calendar — experiences,
  `openDates`, `openTimes` — built by the parser from Tock's calendar slice,
  not a pass-through payload. There is no single upstream object to hand back
  or to slim.
- **`tock_list_reservations`** returns hand-built reservation records (venue,
  date/time, party size, experience, cancelled flag) with no media field. Its
  only `view` is `"full"` (default) or `"brief"`, the one-line-per-item answer
  a context group asks for.
- **`tock_verify_reservation`** returns a VERDICT — `verdict`, `match`,
  `searched`, `recheckAdvised`, `reportAs`, `summary`. The verdict is the
  product, and there is nothing decorative in it to remove.
- **`tock_healthcheck`** returns a bridge diagnostic, for the same reason.

Passing `view` to one of those is not an error and will not fail: the tool
does not declare it, so zod drops the unknown key and the call runs exactly as
it would have. You get no warning, so a successful call is not evidence the
rung was honoured.

## In context groups

When this server is hosted on mcp-host, every tool except `tock_healthcheck`
carries a `_meta.mint` hint in the **food** group (inert to any other
client).

- **Canonical read:** `tock_list_reservations` answers *what's on*
  ("what reservations do I have?", "where are we eating this week?"). It has no
  subject — a Tock account is one person's, so there is no list of children,
  properties or accounts to fan out over — and no date range: it lists the
  upcoming (or past / canceled) set, and the host narrows by date itself. With
  `view: "brief"` it answers one line per reservation, at most 120 characters:
  `<venue>: <experience> (party of N) — <ISO date-time | no date> — <upcoming|past|cancelled>`,
  inside the untrusted-data envelope as `data: string[]` (venue and experience
  names are the restaurants' text). An empty page answers `-- none`, a full
  page ends with `-- more`, and a venue name starting `-- ` or `\` is escaped
  with one leading `\`.
- **Nothing here answers what's new or what's due**, so no other tool is
  canonical. Discovery (`tock_list_metros`, `tock_search_restaurants`,
  `tock_get_restaurant`, `tock_get_availability`), `tock_get_profile` and
  `tock_verify_reservation` are `lookup` reads; there are no writes.
- **A compound ask** looks like "what's on this week — and any dinner
  reservations?": the food group calls `tock_list_reservations` beside the
  other food members' canonical reads and merges the brief lines.
- **Browser-bridged:** every read goes through a signed-in exploretock.com tab
  via ContextMint Bridge. When no browser is connected, the group answers that
  Tock "needs your browser open" rather than reporting no reservations.

## Typical flow

1. `tock_list_metros { query: "chicago" }` → find the metro slug.
2. `tock_search_restaurants { metro: "chicago", query: "tasting menu" }` → get venue slugs.
3. `tock_get_availability { slug: "alinea", date: "2026-07-10", party_size: 2 }` → see experiences and open dates/times.
4. To book, open `exploretock.com/<slug>` — reservations are prepaid tickets and are completed on Tock.

## Booking verification protocol

Booking happens outside these tools (on exploretock.com, by hand or by UI
automation), but **verification is this server's job**. A booking counts as
**confirmed** only when BOTH hold:

1. a confirmation ID, receipt URL, or confirmation email was captured, **and**
2. `tock_verify_reservation { venue, date, partySize, bookedMinutesAgo }` returns
   verdict `confirmed`.

Use `tock_verify_reservation` rather than reading `tock_list_reservations`
yourself: it checks the canceled and past lists too (a created-then-voided
booking appears only in `canceled`), and it applies the lag rule below for you,
returning `recheckAdvised: true` when an absence is still inconclusive. Pass
the venue's exact Tock slug when you have it: a partial name that matches more
than one restaurant on the date returns verdict `ambiguous` (with the
candidates), never `confirmed` — re-run with the slug. A venue query under 4
characters matches only a full name or slug; if it merely appears in a venue
booked that date, the result is `not_found` with `venueQueryTooShort: true`,
`nearMatches` and `recheckAdvised: true` — re-run with the full name, and never
read that `not_found` as proof the booking failed. Handle all four verdicts
(`confirmed`, `cancelled`, `not_found`, `ambiguous`); anything but `confirmed`
is reported per the rules below.

Anything less — including a screenshot of a success screen — must be reported
as **"attempted, unverified."** Two Tock-specific traps make the stricter rule
non-negotiable:

- The post-booking modal is not proof: a confirm submitted with a stale cart
  is a silent no-op that still renders the success modal.
- The reservations backend (`PatronReservationHistory`) lags the Reservations
  tab by **minutes**. A single immediate re-read proving absence proves
  nothing; re-query after a couple of minutes (and once more before giving a
  verdict).

## Notes

- **Read-only.** No booking, cancelling, or payment — Tock reservations are prepaid/Turnstile-gated checkouts left to the site.
- **Discovery needs no login.** Only `tock_list_reservations`, `tock_get_profile` and `tock_verify_reservation` require a signed-in exploretock.com tab.
- Errors are actionable: a Cloudflare challenge asks you to clear it in the signed-in tab; a signed-out account tool asks you to sign in.
