---
name: resy-mcp
description: Manage Resy restaurant reservations via MCP — search venues, book tables, list and cancel reservations, manage favorites, and subscribe to Priority Notify. Triggers on phrases like "book a table at", "find me a reservation", "what reservations do I have", "cancel my Resy", "add to my Resy hit list", or any request involving restaurant reservations on Resy. Requires resy-mcp installed and the resy server registered (see Setup below).
---

# resy-mcp

MCP server for Resy — natural-language restaurant reservation management. Uses Resy's private web-app API with email + password auth.

- **npm:** [npmjs.com/package/resy-mcp](https://www.npmjs.com/package/resy-mcp)
- **Source:** [github.com/chrischall/resy-mcp](https://github.com/chrischall/resy-mcp)

> ⚠️ Resy does not publish an official API. This server uses the same private endpoints the Resy web app calls, with the public web-app `api_key` and user-level auth via email + password. Use at your own discretion.

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "resy": {
      "command": "npx",
      "args": ["-y", "resy-mcp"],
      "env": {
        "RESY_EMAIL": "you@example.com",
        "RESY_PASSWORD": "yourpassword"
      }
    }
  }
}
```

### Option B — from source

```bash
git clone https://github.com/chrischall/resy-mcp
cd resy-mcp
npm install && npm run build
```

Then add to `.mcp.json`:

```json
{
  "mcpServers": {
    "resy": {
      "command": "node",
      "args": ["/path/to/resy-mcp/dist/bundle.js"],
      "env": {
        "RESY_EMAIL": "you@example.com",
        "RESY_PASSWORD": "yourpassword"
      }
    }
  }
}
```

Or place `.env` in the project directory with `RESY_EMAIL=` and `RESY_PASSWORD=`.

## Authentication

- `RESY_EMAIL` + `RESY_PASSWORD` are required. The client logs in lazily on first request via `POST /3/auth/password`, caches the returned token for the process lifetime, and re-logs automatically on 401 / 419 / auth-like 500 responses.
- `RESY_API_KEY` is optional. If unset, the client uses the public web-app key baked into resy.com's JS bundle. Override only if Resy rotates it.

## Tools

### User
| Tool | Description |
|------|-------------|
| `resy_get_profile` | Current user profile — name, email, phone, booking count, member-since. Payment method IDs are stripped. |
| `resy_list_payment_methods` | List saved payment methods (`id`, `brand`, `last_four`, `exp_month`, `exp_year`, `is_default`). The `id` feeds `resy_book`'s `payment_method_id`. |

### Venues
| Tool | Description |
|------|-------------|
| `resy_search_venues(date, party_size, query?, lat?, lng?, limit?, radius_meters?)` | Search venues with availability for a date + party size. Defaults to NYC geo. |
| `resy_find_slots(venue_id, date, party_size, lat?, lng?)` | List bookable slots at a venue — each includes a short-lived `config_token`. |
| `resy_get_venue(venue_id)` | Full venue details. |

### Reservations
| Tool | Description |
|------|-------------|
| `resy_book(venue_id, date, party_size, desired_time?, lat?, lng?, payment_method_id?)` | Composite: find fresh slot → details → book. `desired_time` is "HH:MM" (24h); closest match wins if no exact slot. Uses default payment method unless `payment_method_id` is supplied. |
| `resy_list_reservations(scope?)` | List reservations. `scope`: `upcoming` (default), `past`, or `all`. Each result includes the `resy_token` needed for cancellation. |
| `resy_cancel(resy_token)` | Cancel by `resy_token` (`rr://…`). Inspects the response body to set `cancelled: true/false` honestly. |

### Favorites
| Tool | Description |
|------|-------------|
| `resy_list_favorites` | List favorited venues ("hit list"). |
| `resy_add_favorite(venue_id)` | Add a venue to favorites. |
| `resy_remove_favorite(venue_id)` | Remove from favorites. |

### Priority Notify
| Tool | Description |
|------|-------------|
| `resy_list_notify` | List Priority Notify subscriptions. |
| `resy_add_notify(venue_id, date, party_size, time_start?, time_end?)` | Subscribe to notifications when slots open. `time_start` / `time_end` are HH:MM (24h); default window 18:00–21:00. |
| `resy_remove_notify(notify_id)` | Cancel a Priority Notify subscription. |

## Workflows

**Book a specific restaurant at a specific time:**
```
resy_search_venues(query: "carbone", date: "2026-05-01", party_size: 2)
  → find venue_id
resy_book(venue_id, date: "2026-05-01", party_size: 2, desired_time: "19:00")
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
