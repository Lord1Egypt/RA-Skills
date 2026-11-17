# Resy API — ready-to-run requests

Base URL: `https://api.resy.com`. All requests below assume you've already
exported:

```sh
RESY_API_KEY='VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5'   # public web-app key, see SKILL.md
RESY_TOKEN='...'                                   # from Step 1 in SKILL.md
```

and define this helper so every call below is one line:

```sh
resy() {
  local method=$1 path=$2; shift 2
  curl -s -X "$method" "https://api.resy.com${path}" \
    -H "Authorization: ResyAPI api_key=\"$RESY_API_KEY\"" \
    -H "x-resy-auth-token: $RESY_TOKEN" \
    -H "x-resy-universal-auth: $RESY_TOKEN" \
    -H 'Origin: https://resy.com' \
    -H 'Referer: https://resy.com/' \
    -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
    -H 'Accept: application/json, text/plain, */*' \
    "$@"
}
```

Any remaining args are forwarded straight to curl — use one `--data-urlencode "key=value"`
per form field for POST bodies (curl sets `Content-Type: application/x-www-form-urlencoded`
automatically once any `--data*` flag is present). `--data-urlencode` percent-encodes each
value the same way `src/client.ts`'s `URLSearchParams` does on the wire, so tokens like
`book_token`/`resy_token` (which can contain `rr://`, `:`, `&`, `=`) survive intact instead of
corrupting the body when interpolated raw into a single `--data` string.

Endpoints match the tool set in `src/tools/*.ts` of the resy-mcp repo
1:1 (14 tools total). Source line references are to that repo.

## Auth (Step 1 — see SKILL.md, not covered by the `resy()` helper)

- `POST /3/auth/password` — form body `email`, `password` → `{ token }`
  (or `{ id: { token } }` / `{ auth_token }` on some responses).
  `src/client.ts` `loginWithPassword()`.
- `POST /3/auth/refresh` (via `fpx post-json`, not curl — HttpOnly cookies
  authenticate it) → `{ token }`. `src/auth-fetchproxy.ts`.

## User / profile — `resy_get_profile`, `resy_list_payment_methods`

```sh
resy GET /2/user | jq '{
  first_name, last_name, email: .em_address, phone: .mobile_number,
  num_bookings, member_since: .date_created, is_resy_select: .resy_select
}'

resy GET /2/user | jq '.payment_methods[] | {
  id, brand, last_four: (.last_four // .last4 // .display_number),
  exp_month, exp_year, is_default
}'
```

`payment_methods[].id` is the `payment_method_id` accepted by the book
call below.

## Venue search — `resy_search_venues`

```sh
STRUCT=$(jq -nc --arg q "ramen" --arg day "2026-08-01" \
  '{availability:true, page:1, per_page:20, slot_filter:{day:$day, party_size:2},
    types:["venue"], order_by:"availability",
    geo:{latitude:40.7128, longitude:-73.9876, radius:16100}, query:$q}')
resy POST /3/venuesearch/search --data-urlencode "struct_data=$STRUCT" \
  | jq '.search.hits[] | {venue_id: .id.resy, name, cuisine, price_range, rating, url_slug}'
```

`src/tools/venues.ts` `registerVenueTools` / `resy_search_venues`. NYC geo
(`40.7128,-73.9876`) is the tool's default when lat/lng are omitted.

## Find slots at a venue — `resy_find_slots`

```sh
resy GET "/4/find?lat=40.7128&long=-73.9876&day=2026-08-01&party_size=2&venue_id=123" \
  | jq '.results.venues[0].slots[] | {config_token: .config.token, type: .config.type, start: .date.start}'
```

`src/tools/venues.ts` `findSlotsAtVenue`. `config.token` is the slot
token — exchange it for a `book_token` (below) before booking; it expires
quickly.

## Venue detail — `resy_get_venue`

```sh
resy GET "/3/venue?id=123" | jq '.venue | {
  venue_id: .id.resy, name, cuisine, price_range, rating, url_slug,
  city: .location.locality, state: .location.region
}'
```

`src/tools/venues.ts` `resy_get_venue`.

## Reservations — `resy_list_reservations`, `resy_cancel`, `resy_book`

```sh
# list (client-side filter by day; Resy's own `scope` param is a no-op)
resy GET /3/user/reservations | jq '.reservations[] | {
  resy_token, reservation_id, venue_id: .venue.id, day, time_slot,
  num_seats, cancellable: .cancellation.allowed
}'

# get a book_token for a chosen slot (config_token from find-slots above)
resy GET "/3/details?config_id=<CONFIG_TOKEN>&day=2026-08-01&party_size=2" \
  | jq '{book_token: .book_token.value, venue: .venue.name, type: .config.type}'

# book (mutates — real reservation)
resy POST /3/book \
  --data-urlencode "book_token=<BOOK_TOKEN>" \
  --data-urlencode "struct_payment_method=$(jq -nc --argjson id 456 '{id:$id}')" \
  --data-urlencode "source_id=resy.com-venue-details" \
  | jq '{resy_token, reservation_id, time_slot, num_seats}'

# cancel (mutates — real cancellation)
resy POST /3/cancel --data-urlencode "resy_token=<RESY_TOKEN_ID>" | jq .
```

`src/tools/reservations.ts`. The `resy_token` looks like `rr://...` and
is what `resy_list_reservations`/`resy_book` return; it's what `/3/cancel`
takes. `/3/details`' `config_id` param is confusingly named — it's the
`config_token` from find-slots, not a venue config id.

## Favorites — `resy_list_favorites`, `resy_add_favorite`, `resy_remove_favorite`

```sh
resy GET /3/user/favorites | jq '.results.venues[] | .venue | {
  venue_id: .id.resy, name, cuisine: .type, url_slug, price_range,
  city: .location.locality, neighborhood: .location.neighborhood
}'

# add (favorite=1) / remove (favorite=0) — same endpoint, no DELETE verb
resy POST /3/user/favorites --data-urlencode "venue_id=123" --data-urlencode "favorite=1"
resy POST /3/user/favorites --data-urlencode "venue_id=123" --data-urlencode "favorite=0"
```

`src/tools/favorites.ts`. Resy has no DELETE for favorites — toggling
`favorite=0` on the same POST removes it.

## Priority Notify — `resy_list_notify`, `resy_add_notify`, `resy_remove_notify`

```sh
# list — MUST be /3/notify (not /3/user/notify, which returns HTML)
resy GET /3/notify | jq '.notify[].specs | select(.notify_request_id) | {
  notify_id: .notify_request_id, venue_id, date: .day, party_size,
  time_start: .time_preferred_start, time_end: .time_preferred_end, service_type_id
}'

# add — MUST be /2/notify (POST /3/notify returns 502); field is num_seats, not party_size
resy POST /2/notify \
  --data-urlencode "venue_id=123" \
  --data-urlencode "day=2026-08-01" \
  --data-urlencode "num_seats=2" \
  --data-urlencode "time_preferred_start=18:00:00" \
  --data-urlencode "time_preferred_end=21:00:00" \
  --data-urlencode "service_type_id=2"

# remove — DELETE /2/notify needs the FULL spec as query params, not just the id.
# Look up the spec from the list call above first, then:
curl -s -X DELETE "https://api.resy.com/2/notify?notify_request_id=<ID>&venue_id=123&day=2026-08-01&num_seats=2&service_type_id=2" \
  -H "Authorization: ResyAPI api_key=\"$RESY_API_KEY\"" \
  -H "x-resy-auth-token: $RESY_TOKEN" \
  -H "x-resy-universal-auth: $RESY_TOKEN" \
  -H 'Origin: https://resy.com' -H 'Referer: https://resy.com/'
```

`src/tools/notify.ts`. Notify's date window is ~30 days out; Resy rejects
dates outside it. `time_preferred_start`/`end` are `HH:MM:SS` on the wire
(pad `HH:MM` with `:00`); `resy_list_notify`'s output trims the seconds
back off.

## Known quirks (from `CLAUDE.md` "Resy API quirks (from live smoke)")

- `/3/notify` is list-only; POST there 502s — adds go to `/2/notify`.
- `/3/user/notify` returns HTML, not JSON — always use `/3/notify` for list.
- `/2/notify`'s party-size field is `num_seats`; the `/3` reservation
  endpoints use `party_size`.
- Favorites toggle via `favorite=1|0` on the same `POST /3/user/favorites`
  — there's no DELETE.
- `/3/user/reservations`'s `scope` query param is currently a no-op; the
  MCP's "upcoming"/"past" filtering happens client-side on `day`.
- Slot times in `/4/find` come back with no timezone offset
  (restaurant-local) — don't run them through `new Date()` / a TZ-aware
  parser, read `HH:MM` off the string directly.
