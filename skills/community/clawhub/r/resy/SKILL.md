---
name: resy
description: Manage Resy restaurant reservations via MCP — search venues, book tables, list and cancel reservations, manage favorites, and subscribe to Priority Notify. Triggers on phrases like "book a table at", "find me a reservation", "what reservations do I have", "cancel my Resy", "add to my Resy hit list", or any request involving restaurant reservations on Resy. Requires resy-mcp installed and the resy server registered (see Setup below).
---

# resy-mcp

MCP server for Resy — natural-language restaurant reservation management. Uses Resy's private web-app API. By default it signs in through your own signed-in resy.com tab via the ContextMint Bridge browser extension, so no credentials go in env; a token or email/password are optional alternatives.

- **npm:** [npmjs.com/package/resy-mcp](https://www.npmjs.com/package/resy-mcp)
- **Source:** [github.com/chrischall/resy-mcp](https://github.com/chrischall/resy-mcp)

> ⚠️ Resy does not publish an official API. This server uses the same private endpoints the Resy web app calls, with the public web-app `api_key` and the signed-in user's auth token. Use at your own discretion.

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "resy": {
      "command": "npx",
      "args": ["-y", "resy-mcp"]
    }
  }
}
```

Then install the ContextMint Bridge extension from its [releases page](https://github.com/nullnet-app/contextmint-bridge/releases) (Chrome: unzip and load unpacked at `chrome://extensions`), sign in to resy.com in that browser, and approve the one-time pair code the first tool call prints. No env vars are needed.

### Option B — from source

```bash
git clone https://github.com/chrischall/resy-mcp
cd resy-mcp
npm install && npm run build
```

Then point `.mcp.json` at `/path/to/resy-mcp/dist/bundle.js` (`"command": "node"`). Any of the optional env vars below can go in that entry's `env` block or in a `.env` next to the repo.

## Authentication

The client picks an auth path on first request, in this priority order:

1. **`RESY_AUTH_TOKEN`** — a pre-obtained `x-resy-auth-token`, used verbatim. Overrides everything (CI / power users).
2. **`RESY_EMAIL` + `RESY_PASSWORD`** — optional password login via `POST /3/auth/password`. Only needed on a host with no browser.
3. **ContextMint Bridge (default)** — with neither of the above set, one `/3/auth/refresh` call runs through your signed-in resy.com tab and returns a token; every later call is direct. Set `RESY_DISABLE_FETCHPROXY=1` to turn this path off.

Never ask a bridge user for their Resy password — path 3 exists so they don't have to hand it over.

The minted token is cached on disk (`$MCP_DATA_DIR/.resy-mcp/token.json`; `RESY_TOKEN_CACHE=false` turns it off, `RESY_TOKEN_FILE` moves it), so a restart doesn't need a fresh sign-in. A token lifted from the browser expires after 24 hours and is then re-minted through the tab. A 401, 419 or auth-shaped 500 clears the token and re-mints it once — except an auth-shaped 500 on a write (book/cancel), which is reported as outcome-unknown and never replayed: check `resy_list_reservations` before retrying.

`RESY_API_KEY` is optional: the public web-app key is captured from your tab and cached, so set it only to pin a specific key. Other knobs: `RESY_CAPTURE_TIMEOUT` (seconds to wait for the bridge capture, default 30), `RESY_WS_PORT` (bridge port, default 37149), `RESY_API_KEY_FILE`.

`resy_book` and `resy_cancel` ask for confirmation before they act; the `MCP_CONFIRM_MODE` / `MCP_CONFIRM_ELICITATION` / `MCP_CONFIRM_TTL_SECONDS` / `MCP_CONFIRM_SECRET` knobs are documented in the README's Confirmations section.

## Tools

### User
| Tool | Description |
|------|-------------|
| `resy_get_profile(view?)` | Current user profile — name, email, phone, booking count, member-since. Payment method IDs are stripped. |
| `resy_list_payment_methods(view?)` | List saved payment methods (`id`, `brand`, `last_four`, `exp_month`, `exp_year`, `is_default`). The `id` feeds `resy_book`'s `payment_method_id`. |

### Venues
| Tool | Description |
|------|-------------|
| `resy_search_venues(date, party_size, query?, lat?, lng?, limit?, radius_meters?, view?)` | Search venues with availability for a date + party size. Defaults to NYC geo. |
| `resy_find_slots(venue_id, date, party_size, lat?, lng?)` | List bookable slots at a venue — each includes a short-lived `config_token`. |
| `resy_get_venue(venue_id)` | Full venue details. |

### Reservations
| Tool | Description |
|------|-------------|
| `resy_book(venue_id, date, party_size, desired_time?, slot_type?, terms_token?, allow_closest_time?, lat?, lng?, payment_method_id?, allow_duplicate?, confirmToken?)` | Composite: find fresh slot → details → book. It books ONLY the exact previewed slot. `desired_time` is "HH:MM" (24h); an unavailable time returns the available times unless `allow_closest_time: true` previews the nearest. `slot_type` picks a seating (Dining Room / Bar / Patio) when several share a time. On a client without prompts, the preview comes back as `confirmation-required` with a `confirmToken` bound to that slot's time, seating type and terms; after the user approves, repeat the call with the preview's time as `desired_time` and the `confirmToken` (see `MCP_CONFIRM_MODE`). On a client with prompts (unless the server sets `MCP_CONFIRM_ELICITATION=off`, which sends every client down the `confirmToken` path), call again with `desired_time` + `slot_type` + `terms_token` (a fingerprint of the seating type and cancellation/payment terms) from the preview and the user is prompted. If the slot, its type or its terms changed, nothing is booked and a fresh preview is returned. The booking refuses if you already hold a reservation at that venue that date (e.g. an earlier timed-out call that went through) unless `allow_duplicate: true` — checked before you are asked to confirm, so an approval is never wasted; with `allow_duplicate: true` the preview lists the existing reservation(s). Uses default payment method unless `payment_method_id` is supplied; either way the preview names the card (brand and last-4), and an id that is not one of your saved cards is refused. |
| `resy_list_reservations(scope?, view?)` | List reservations. `scope`: `upcoming` (default), `past`, or `all`. Each result includes the `resy_token` needed for cancellation. `view: "brief"` answers one line per reservation instead: `<venue> <HH:MM>, party of <n> — <YYYY-MM-DDTHH:MM or no date> — <booked\|past>`. |
| `resy_cancel(resy_token, confirmToken?)` | Cancel by `resy_token` (`rr://…`). Asks the user to confirm first (the Resy account, venue, date, time, party size, any fee): a prompt where the client supports one (unless `MCP_CONFIRM_ELICITATION=off`), otherwise a preview plus `confirmToken` that a repeat call passes back. Returns `cancelled` (always a boolean — `true` only when confirmed) and `outcome` (`cancelled` / `not_cancelled` / `unknown`), set from an explicit success/failure in Resy's response, and otherwise by checking whether the reservation is still listed. On `outcome: "unknown"` the reservation may still have been cancelled — check `resy_list_reservations` before retrying. |

### Favorites
| Tool | Description |
|------|-------------|
| `resy_list_favorites(view?)` | List favorited venues ("hit list"). |
| `resy_add_favorite(venue_id)` | Add a venue to favorites. |
| `resy_remove_favorite(venue_id)` | Remove from favorites. |

### Priority Notify
| Tool | Description |
|------|-------------|
| `resy_list_notify(view?)` | List Priority Notify subscriptions. |
| `resy_add_notify(venue_id, date, party_size, time_start?, time_end?)` | Subscribe to notifications when slots open. `time_start` / `time_end` are HH:MM (24h); default window 18:00–21:00. |
| `resy_remove_notify(notify_id)` | Cancel a Priority Notify subscription. |

## Response shape (`view`)

Five read tools take `view: "compact" | "full"` — `resy_get_profile`,
`resy_list_payment_methods`, `resy_list_favorites`, `resy_list_notify` and
`resy_search_venues` — and **`compact` is the default**. The slim rung arrives
without being asked for, because an efficiency a caller has to know about and
request is one that usually is not requested.

**Compact strips image and avatar URLs here, and nothing else.** There is no
field projection: this server holds no captured fixture or documented field
list for Resy's payloads, and an invented one would return a record with holes
in it that still reads like a verified answer. Media stripping is subtractive,
so it cannot lose a field nobody knew about.

**The surprise worth stating plainly: on four of those five tools, compact and
full are byte-identical today.** `resy_get_profile` is the ONE response in this
whole server that carries a media URL — `profile_image_url` off `/2/user` — so
it is the one place compact removes anything at all. The other four already
hand back records this server assembled field by field, with no picture in
them. The parameter is on them so that a field arriving later with an avatar
inside it is stripped by default rather than after somebody notices.

`profile_image_url` is named in the drop list rather than left to the built-in
rules, and that is what makes its removal deterministic. The key pattern
anchors its noun at the START of a key (it knows `profile_pic`, not
`profile_image_url`), which leaves only the value rule — and that fires just
when a URL path ends in an image extension, which Resy's avatar pipeline need
not do.

`view: "full"` returns the record untouched. There is **no `raw` rung**: `full`
already IS the un-stripped response, so a third value could only alias it.

`resy_list_reservations` takes a different `view`: `"full"` (the default, its
JSON records) or `"brief"` (one line per reservation, at most 120 characters,
for a host that reads several sources at once — see "In context groups"). It
has no compact rung because its records are built field by field with no media
URL in them.

The other nine tools take no `view`:

- **`resy_find_slots` and `resy_get_venue`** build their answers field by field
  (`formatSlot`, `formatVenue`). No upstream payload survives into the
  response, and no media URL with it — there is nothing for the rung to remove.
- **`resy_book`, `resy_cancel`, `resy_add_favorite`, `resy_remove_favorite`,
  `resy_add_notify`, `resy_remove_notify`** are writes. A write's response is a
  receipt — a `resy_token`, a confirmation, a status — with nothing to strip and
  everything to keep.
- **`resy_healthcheck`** answers reachability and auth.

## In context groups

On a host that groups connectors by context (mcp-host's context groups), every
tool here except `resy_healthcheck` is in the **food** group.

- **Canonical read:** `resy_list_reservations` answers *what's on* — the
  person's upcoming tables — and the host reads it with `view: "brief"`. The
  brief lines ride inside the untrusted-data envelope (`data: string[]`,
  because venue names are the restaurants' own text), a venue name starting
  `-- ` or `\` is escaped with one leading `\`, and an empty list answers the
  single note line `-- none`. It takes no subject (a Resy session is one
  account, with nothing to choose between) and no date range (only `scope`).
- Everything else is a `lookup` (profile, cards, venue search, slots,
  favorites, the notify list) or a `change` (book, cancel, favorite, notify).
- A compound ask reads this beside the group's other sources: *"what's on this
  week — and do we have dinner anywhere?"* answers the reservations as one line
  each.
- When this server is minting its token through the browser bridge (no
  `RESY_AUTH_TOKEN` or password set) and no signed-in resy.com tab is
  reachable, the group answers that Resy **needs your browser open** rather
  than reporting no reservations.

## Workflows

**Book a specific restaurant at a specific time:**
```
resy_search_venues(query: "carbone", date: "2026-05-01", party_size: 2)
  → find venue_id
resy_book(venue_id, date: "2026-05-01", party_size: 2, desired_time: "19:00")
  → preview: time, slot_type, terms_token, fees, payment card; show it to the user

  client WITHOUT prompts (claude.ai, Claude Desktop), or any client when the
  server sets MCP_CONFIRM_ELICITATION=off: that preview is
  `confirmation-required` and carries a confirmToken. Once the user approves in chat:
resy_book(venue_id, date: "2026-05-01", party_size: 2,
          desired_time: "<preview's time>", confirmToken: "<token>")

  client WITH prompts (Claude Code), unless MCP_CONFIRM_ELICITATION=off: name the
  slot and the user is prompted:
resy_book(venue_id, date: "2026-05-01", party_size: 2, desired_time: "<preview's time>",
          slot_type: "<preview's slot_type>", terms_token: "<preview's terms_token>")
```

**See what's available tonight near me:**
```
resy_search_venues(date: "2026-04-20", party_size: 2, lat: 37.7749, lng: -122.4194)
  → returns venues with baked-in slot availability
```

**Cancel a reservation:**
```
resy_list_reservations() → find resy_token for the one to cancel
resy_cancel(resy_token)
  → a confirmation prompt (unless MCP_CONFIRM_ELICITATION=off), or a preview plus
    confirmToken to pass back once the user approves
```

**Stalking a hard-to-get table:**
```
resy_search_venues(query: "4 charles prime rib", ...) → venue_id
resy_add_notify(venue_id, date: "2026-05-31", party_size: 2, time_start: "19:00", time_end: "21:00")
# Resy emails you when a slot opens
```

## Notes

- Slot `config_token`s expire within minutes of being fetched. `resy_book` re-fetches fresh slots internally — don't try to thread a stale token from `resy_find_slots` into a book call manually.
- `resy_book` requires a payment method on file at resy.com/account. If none exists it throws a clear error.
- Default geo is NYC (40.7128, -73.9876). Pass `lat`/`lng` for other cities.
- Favorites and Priority Notify endpoint paths are reverse-engineered. If a call fails with 404, run `npm run smoke` locally against your credentials and adjust the path.
- `RESY_API_KEY` env var overrides the baked-in public web-app key if Resy ever rotates it.
