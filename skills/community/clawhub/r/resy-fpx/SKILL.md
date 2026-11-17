---
name: resy-fpx
description: >-
  Query and act on Resy (resy.com restaurant reservations) from a shell
  without running the resy-mcp server — search venues, check slot
  availability, book/cancel reservations, and manage favorites/Priority
  Notify with curl against api.resy.com, using the fpx CLI
  (@fetchproxy/cli) only for the one-time token bootstrap when you have no
  RESY_EMAIL/RESY_PASSWORD. Use when you want Resy data or actions without
  the MCP, in a script, or on a machine where the MCP isn't installed.
---

# Resy via curl (+ one-time fpx bootstrap)

Resy has no public API — resy-mcp calls the same `api.resy.com` endpoints
the resy.com web app calls, all of which are reachable with **plain
curl**; nothing here needs a bot-wall bypass. The browser bridge (`fpx`)
is only needed to mint an auth token when you have no email/password on
hand — after that, every actual call (search, slots, book, cancel,
favorites, notify, profile) is a direct curl with the token in a header.
This mirrors resy-mcp's own "Pattern B": bridge the one auth call, then
go direct for the hot path (see `src/client.ts` / `src/auth-fetchproxy.ts`
in the resy-mcp repo).

## Step 1 — get a token (pick ONE path)

**Path A — you have Resy credentials (preferred, no browser needed):**

```sh
curl -s 'https://api.resy.com/3/auth/password' \
  -H 'Authorization: ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "email=$RESY_EMAIL" \
  --data-urlencode "password=$RESY_PASSWORD" \
| jq -r '.token // .id.token // .auth_token'
```

The api key above is Resy's public web-app key (baked into resy.com's own
JS, not a secret — see `src/client.ts`). Save the returned token as
`$RESY_TOKEN`.

**Path B — no credentials, only a signed-in resy.com browser tab:**

One-time setup:

```sh
npm install -g @fetchproxy/cli            # provides `fpx`
fpx profile add resy --domain resy.com
fpx pair -p resy                          # prints a pair code → approve in ContextMint Bridge
```

Then bootstrap the token through the tab (this replicates the one call
resy.com's own JS makes to refresh its in-memory token — the HttpOnly
session cookies authenticate it):

```sh
fpx post-json 'https://api.resy.com/3/auth/refresh' '{}' -p resy \
  | jq -r '.token'
```

Save it as `$RESY_TOKEN`. `fpx` is not used again after this — every
call below is curl.

## Step 2 — call the API directly with the token

Every authenticated request needs this header set (see `SPOOF_HEADERS` +
`buildHeaders` in `src/client.ts`):

```sh
RESY_API_KEY='VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5'   # override if Resy rotates it
curl -s '<url>' \
  -H "Authorization: ResyAPI api_key=\"$RESY_API_KEY\"" \
  -H "x-resy-auth-token: $RESY_TOKEN" \
  -H "x-resy-universal-auth: $RESY_TOKEN" \
  -H 'Origin: https://resy.com' \
  -H 'Referer: https://resy.com/' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
  -H 'Accept: application/json, text/plain, */*'
```

POST/DELETE bodies are `application/x-www-form-urlencoded`
(`--data-urlencode`), except venue search which sends a single
`struct_data` field containing JSON. All 14 request/response shapes,
copy-pasteable, are in `references/resy-api.md`.

## The one rule: resolve venue → slot → book_token before booking

Booking is a 3-hop chain, same as `resy_book`'s internal flow:

1. `POST /3/venuesearch/search` or `GET /4/find` → `config_token` for the
   slot you want.
2. `GET /3/details?config_id=<config_token>&day=&party_size=` →
   `book_token.value` (expires fast — fetch it right before booking).
3. `POST /3/book` with `book_token` + `struct_payment_method` (get a
   payment id from `GET /2/user` if you don't already have one).

## Token lifetime

Resy tokens are opaque with no published TTL and no separate refresh
token. If a call 401s (or 419s, or 500s with an auth-shaped message),
just re-run Step 1 to mint a fresh one — there's no incremental refresh.

## Exit codes (fpx, Path B only)

- `0` — success.
- `2` — bridge unavailable: extension not connected or pairing pending →
  `fpx pair -p resy`, confirm a resy.com tab is open.
- `3` — bot wall: shouldn't happen on the bootstrap call, but if it does,
  refresh the resy.com tab and retry.
- `4` — upstream non-2xx (e.g. not actually signed in — sign into
  resy.com in that tab first).

## Notes

- This is your own Resy account — write calls (book, cancel, favorite,
  notify) mutate real reservations/subscriptions. There is no dry-run at
  the curl layer (the MCP's confirmation step — prompt or preview token — is an MCP-side
  convenience); read back with a list call before/after a write if you
  want to verify it landed.
- `fpx health -p resy` shows bridge connection state if Path B's bootstrap
  call fails.
- This project is developed and maintained by AI (Claude).
