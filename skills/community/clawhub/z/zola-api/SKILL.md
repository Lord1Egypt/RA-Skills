---
name: zola-api
description: >-
  Query or update Zola wedding-planning data (vendors, budget, guests, seating,
  events/RSVPs, registry, gift tracker, inquiries, wedding website) straight
  from a shell with curl against mobile-api.zola.com, instead of running the
  zola-mcp server. Use when you want Zola data without the MCP, in a script,
  or on a machine where the MCP isn't installed. Triggers on "check Zola",
  "Zola vendors/budget/guests/RSVP/seating/registry", or any Zola wedding
  data request that should hit the API directly.
---

# Zola mobile API via curl (no MCP)

Zola's mobile API (`mobile-api.zola.com` — the same surface the iOS/iPad app
and `zola-mcp` use) is a plain Bearer-JWT REST API reachable directly from a
server or shell — no browser bridge needed. This skill shells out to `curl`
with the JWT in an `Authorization: Bearer` header, exactly as
`zola-mcp`'s `src/client.ts` does.

## One-time setup: get the refresh token

You need Zola's long-lived (~1 year) refresh JWT — the `usr` cookie from a
signed-in `zola.com` session. Same credential `zola-mcp` uses:

```sh
# Prefer the env var zola-mcp itself reads (check its .env first):
grep -h ZOLA_REFRESH_TOKEN ~/git/zola-mcp/.env 2>/dev/null
export ZOLA_REFRESH_TOKEN='eyJhbGciOi...'   # or export directly if you have it
```

If you don't have it yet: sign into zola.com, open DevTools → Application →
Cookies → `https://www.zola.com`, copy the `usr` value. (`zola-mcp` also has a
fetchproxy fallback that reads this cookie from a signed-in browser tab — see
its README — but that's the MCP's path, not this skill's; this skill assumes
you already have the token in hand.)

## Core call pattern

Every mobile-api call needs a short-lived (30 min) **session token**, minted
from the refresh token, plus a fixed set of headers (CloudFront WAF requires
`x-zola-session-id` on every request — omit it and you get a 403).

```sh
BASE=https://mobile-api.zola.com
DEVICE_SESSION_ID=$(uuidgen | tr 'a-z' 'A-Z')   # one per "session"; reuse across calls
UA='Zola/42.5.0 (iPad; iOS 26.4; Scale/2.0)'

# 1. Mint a 30-min session token from the refresh token
SESSION_TOKEN=$(curl -sS -X POST "$BASE/v3/sessions/refresh" \
  -H 'content-type: application/json' -H 'accept: application/json' \
  -H "x-zola-platform-type: iphone_app" -H "x-zola-session-id: $DEVICE_SESSION_ID" \
  -H "user-agent: $UA" \
  -d "{\"token\":\"$ZOLA_REFRESH_TOKEN\"}" | jq -r '.data.session_token')

# 2. Every subsequent call reuses $SESSION_TOKEN until it expires (~30 min),
#    then re-run step 1. All calls carry the same 4 headers:
curl -sS -X GET "$BASE/v3/users/me/context" \
  -H "authorization: Bearer $SESSION_TOKEN" \
  -H "x-zola-platform-type: iphone_app" -H "x-zola-session-id: $DEVICE_SESSION_ID" \
  -H "user-agent: $UA" | jq '.data'
```

Wrap this in a shell function or export the 4 headers once — every recipe in
`references/mobile-api-endpoints.md` reuses `$BASE`, `$SESSION_TOKEN`,
`$DEVICE_SESSION_ID`, `$UA`. POST/PUT bodies additionally need
`-H 'content-type: application/json'`.

(The app also sends a fifth header, `x-zola-user-session-id`, derived from a
claim inside the session JWT — `zola-mcp` only attaches it when the decode
succeeds, so it's not load-bearing; every endpoint below works without it.)

## The one rule: resolve context first

Most write/list endpoints are scoped by numeric IDs, never inferred — call
`GET /v3/users/me/context` once per session and keep the three IDs around:

```sh
CTX=$(curl -sS "$BASE/v3/users/me/context" -H "authorization: Bearer $SESSION_TOKEN" \
  -H "x-zola-platform-type: iphone_app" -H "x-zola-session-id: $DEVICE_SESSION_ID" -H "user-agent: $UA")
ACCT=$(jq -r '.data.wedding_account.wedding_account_id' <<<"$CTX")
REG=$(jq -r '.data.registry.id' <<<"$CTX")
WEDDING_ID=$(jq -r '.data.wedding.wedding_id' <<<"$CTX")
```

`ACCT` (`wedding_account_id`) feeds guest/event/website-content paths; `REG`
(`registry_id`) feeds registry/gift-tracker paths.

## Ready-to-run endpoints

`references/mobile-api-endpoints.md` has real, ready-to-run `curl` + `jq`
recipes for every one of the 30 `zola-mcp` tools' underlying calls
(vendors, budget, guests, seating, inquiries, events/RSVPs/gifts/registry,
discover/storefronts, registry items, invitations/card-projects, website
pages, website theme/customization, website content). Transcribed straight
from `src/tools/*.ts` — same paths, same request bodies.

## Mutation gotcha: most writes are read-modify-write

Zola's write endpoints replace whole objects, not deltas — the same tools
that build a request first re-GET the current record and only patch the
requested fields, or a full-state write can wipe unrelated fields.
`docs/zola-api-quirks.md` in this repo documents the worst offenders (a
`header_font` write nulling every other website color; guest writes needing
to preserve `event_invitations` verbatim or lose them). Follow the
read-modify-write shape shown per-endpoint in the references file — don't
send a bare partial body to `PUT`/`POST` write endpoints.

## Output / error contract

- A 2xx body is `{"data": ...}` for nearly every endpoint — pipe to
  `jq '.data'`.
- `401` — session token expired; re-mint via `POST /v3/sessions/refresh`
  (step 1 above) and retry once.
- `429` — rate limited; back off ~2s and retry once.
- Any other non-2xx — the body is a JSON error envelope; read it directly,
  it is not redacted here (unlike the MCP, which redacts secrets from error
  text — don't paste raw error bodies containing the session token anywhere
  public).
- This project (`zola-mcp`) is developed and maintained by AI (Claude).
