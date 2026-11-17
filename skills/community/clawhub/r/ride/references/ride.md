# Ride Reference

> All agent-facing operations use `amb <subcommand> [args…]` (PATH-resident). Two scripts that cannot live on PATH (`ride-relay.js`, `install.js`) are invoked via `node ${SKILL_DIR}/scripts/<name>.js` — see `../SKILL.md` for the path convention.

## Place Search

`place-search` and `place-detail` have mode-specific signatures. Run
`amb whoami --json` before the first place command and use exactly one branch:

| Mode | Search | Detail |
|---|---|---|
| `wallet` | `amb place-search <wallet_address> <city> <query> [latitude longitude] --json` | `amb place-detail <wallet_address> <city> <place_id> --json` |
| `tada` | `amb place-search <query> <region> [originLat originLng] [--city CODE] [--session-token UUID] [--lang TAG] --json` | `amb place-detail <place_id> <region> [city] [--lang TAG] --json` |
| `null` | Stop and complete onboarding before resolving a ride place. | — |

Do not infer the mode from a response shape. Wallet responses expose coordinates
under `locationPoint`; member responses expose them under `lat_lng`. Extract the
latitude/longitude pair, then project it differently for each command:

- `ride-search` takes origin and destination coordinates as positional arguments:
  - member: `amb ride-search <oLat> <oLng> <dLat> <dLng> [card_uuid] --json`
  - wallet: `amb ride-search <wallet_address> <region> <oLat> <oLng> <dLat> <dLng> --json`
- `ride-request` takes one JSON argument. Put each pair inside the corresponding
  `locations[]` object as `latitude` and `longitude`; they are not top-level
  request fields in either mode:

  ```json
  {"locations":[{"latitude":1.3001,"longitude":103.8001},{"latitude":1.3202,"longitude":103.8202}]}
  ```

Add the other mode-specific `ride-request` fields described below; this example
shows only the coordinate projection.

### Wallet place search — autocomplete suggestions

Before running `place_search` to resolve a ride origin or destination, you may ask the user for their current location (latitude/longitude) to improve search accuracy. **Say what it is for and that it is optional** — something like "if you tell me roughly where you are I can rank the results better, but I can search without it". Precise coordinates are sensitive, and asking for them flatly reads as a requirement. They are sent to TADA/Throo as the search's bias point. If the user does not know, does not want to say, or does not answer, proceed without it — the search falls back to the city center.

```bash
amb place-search <wallet_address> <city> <query> [latitude] [longitude] --json
```

- `city`: **City code** (e.g. `SIN`, `PNH`, `HKG`) or English city name. Do NOT use region codes (`SG`, `KH`, `HK`) here — those are for `ride_search` only.

| City code | English name | Region code | Country |
|-----------|--------------|-------------|---------|
| `SIN` | Singapore | `SG` | Singapore |
| `BKK` | Bangkok | `TH` | Thailand |
| `DEN` | Denver | `CO` | USA |
| `HCM` | Ho Chi Minh / Saigon | `VN` | Vietnam |
| `HAN` | Hanoi | `VN` | Vietnam |
| `PNH` | Phnom Penh | `KH` | Cambodia |
| `REP` | Siem Reap | `KH` | Cambodia |
| `SHV` | Sihanoukville | `KH` | Cambodia |
| `KPK` | Kampot | `KH` | Cambodia |
| `SEL` | Seoul | `KR` | Korea |
| `ADD` | Addis Ababa | `ET` | Ethiopia |
| `JKT` | Jakarta | `ID` | Indonesia |
| `HKG` | Hong Kong | `HK` | Hong Kong |
| `NYC` | New York | `NY` | USA |

`place_search` uses **city code**, `ride_search` uses **region code**. Use this table to convert between them.

The table lists every city the TADA app itself serves. **Ambient Ride currently enables only `NYC`, `SIN`, `PNH`, `REP`, `SHV`, `KPK`, and `HKG`** (regions `NY`, `SG`, `KH`, `HK`). Any other city or region is rejected by the service; the CLI does not fall back to a nearby city or to a default region. A city code from the table that Ambient Ride has not enabled is still forwarded to the service, which then refuses it — so use only the enabled codes above.

- `query`: Search term (place name, address, etc.)
- `latitude` / `longitude`: Optional. User's current location for bias. Omit if unknown.

Response shape:

```json
{
  "results": [ /* PlaceResult[] */ ],
  "next_action": "ASK_USER_TO_PICK_ONE_RESULT" | "REPORT_NO_MATCHES_TO_USER",
  "must": "..."  // present only when results is non-empty
}
```

Each item in `results`:
- `placeId`: Place ID — opaque token. Treat as a black box.
- `name`: Place name
- `address`: Place address
- `locationPoint`: `{ latitude, longitude }` coordinates — present for TADA POI / OneMap results, `null` for Google Places results
- `subPlaces`: Array of sub-locations (e.g. gates, lobbies, entrances) — may be empty

Show results to the user using `name` and `address`. Ask them to select one.

If `next_action` is `REPORT_NO_MATCHES_TO_USER` (empty `results`): inform the user and ask them to try a different search term.

> **⚠️ placeId provenance rule (strictly enforced)**
> Any `placeId` / `place_id` argument passed to a subsequent command (`amb place-detail`, `amb map-session-create`, `amb ride-request` `locations[].placeId`) MUST be a value taken verbatim from `results[].placeId` of a `place_search` response — or, transitively, from a `place_detail` / `map-session-verify` response that itself originated from one.
> NEVER fabricate or substitute a place ID from any external system or from your own model knowledge.
> If `results` does not contain the place the user wants, run `place_search` again with a different query.

### After user selects a place_search result

Check the selected result's `locationPoint`:

**If `locationPoint` is present (TADA POI / OneMap):** skip `place_detail` — coordinates and subPlaces are already available from the autocomplete result. Proceed directly to Map Location Confirmation.

**If `locationPoint` is null (Google Places):** run `place_detail` to fetch coordinates.

### place_detail - Fetch coordinates (only when locationPoint is null)

```bash
amb place-detail <wallet_address> <city> <place_id> --json
```

- `place_id`: `placeId` from the chosen `place_search` result

Response fields:
- `placeId`: Place ID
- `name` / `address`: Place name and address
- `locationPoint`: `{ latitude, longitude }` coordinates (may be `null`)
- `subPlaces`: Array of sub-locations (may be empty)

If `locationPoint` is `null`: inform the user and ask them to select a different result from the already-displayed `place_search` list. Do not re-run `place_search`.

### How to build the locations array

**A-1. User provided a place name → autocomplete result has `locationPoint`** → Build from autocomplete result directly (no place_detail)
```json
{
  "name": "<name from autocomplete result>",
  "address": "<address from autocomplete result>",
  "latitude": "<locationPoint.latitude from autocomplete result>",
  "longitude": "<locationPoint.longitude from autocomplete result>",
  "placeId": "<placeId from autocomplete result>"
}
```

**A-2. User provided a place name → autocomplete result has `locationPoint: null`** → Run place_detail, build from its result
```json
{
  "name": "<name from place_detail result>",
  "address": "<address from place_detail result>",
  "latitude": "<locationPoint.latitude from place_detail result>",
  "longitude": "<locationPoint.longitude from place_detail result>",
  "placeId": "<placeId from place_detail result>"
}
```

**B. User provided coordinates/address/name directly** → Build without scripts, no map session needed
```json
{
  "name": "<user-provided name, or use address if no name>",
  "address": "<user-provided address>",
  "latitude": "<user-provided latitude>",
  "longitude": "<user-provided longitude>"
}
```

Required: `latitude`, `longitude`, `address`, `name` (all required)
Optional: `placeId`, `googlePlaceId`, `subPlaceId`

### Map Location Confirmation

**⚠️ MANDATORY for Case A (both A-1 and A-2).** You MUST run map confirmation after obtaining coordinates. Do NOT skip this step. Do NOT proceed to `ride_search` without completing map confirmation for both origin and destination. If `subPlaces` exist, do NOT list them as text — they must go to the map.

After obtaining coordinates (from autocomplete result in Case A-1, or from place_detail in Case A-2), check whether subPlaces exist:

**If subPlaces exist:** map session is **mandatory** — the user must select a specific subPlace. The place itself is just a group. Do NOT allow the user to skip.

**If subPlaces do not exist:** map session is still created — present the link alongside the result for the user to verify/adjust if they want.

**Step 1: Create map session**

If `subPlaces` exist, transform and pipe them via stdin. The `subPlaces` array from autocomplete/place_detail uses `locationPoint: { latitude, longitude }`, but `map-session-create` expects flat `{ id, name, lat, lng, address }`. Transform each subPlace: `locationPoint.latitude → lat`, `locationPoint.longitude → lng`.

```bash
echo '{"subPlaces": [{"id":"...","name":"...","lat":<locationPoint.latitude>,"lng":<locationPoint.longitude>,"address":"..."},...]}'  | amb map-session-create <wallet_address> <city> <lat> <lng> [name]
```

If no subPlaces, call without stdin:
```bash
amb map-session-create <wallet_address> <city> <lat> <lng> [name]
```

Returns `{ sessionId, mapUrl, expiresAt }`.

**Step 2: Present result + link, start polling**

Show the place result together with the map link, e.g.:
> "Marina Bay Sands (1 Bayfront Avenue, Singapore 018971)
> You can verify or adjust the location on the map: [View on map](mapUrl)
> If this looks correct, just let me know to proceed."

Poll for the user's selection using `amb map-session-verify <session_id> --json` in a polling loop.

**Step 3: React to whichever signal comes first**

| Signal | Action |
|--------|--------|
| User says "proceed" / "looks good" | Use the place result as-is. Ignore the poll (session expires naturally). Only allowed when subPlaces do not exist. |
| Poll result: `completed` | Use the map result (`lat`, `lng`, `address`, `name`, `placeId`, `subPlaceId`) for the locations array. If `subPlaceId` is present, include it. |
| Poll result: `cancelled` | Ask the user: use the original place result, or search again? |
| Poll result: `expired` | Proceed with the place result (session timed out). |
| Poll result: `jwt_expired` | Re-authenticate (SIWE login), then run `map-session-create` again with fresh JWT. |

`amb map-session-verify <session_id> --json` output events:
- `{ "type": "waiting" }` — user has not selected yet
- `{ "type": "completed", "result": { "lat", "lng", "address", "name", "placeId?", "subPlaceId?" } }` — use this for the locations array
- `{ "type": "cancelled" }` — user closed the map without confirming
- `{ "type": "jwt_expired" }` — requires re-authentication
- `{ "type": "expired" }` — session timed out (5-minute TTL)

Do NOT create a map session when the user provided coordinates directly (Case B).

## Saved places (local catalog)

Frequent destinations and origins can be persisted locally so the agent can skip TADA autocomplete on subsequent rides.

> Auth asymmetry: `place-save` requires a valid JWT (it calls the gateway `/v1/places/resolve-google` endpoint). `place-list`, `place-remove`, `place-favorite`, and `place-unfavorite` are purely local (SQLite) and need no JWT — do not run a preflight auth check for them.

When re-favoriting or relabeling an existing local or history row, use `place-favorite` with its `id` or `dedup_key`.
Do not call `place-save` or send its Google Maps URL again.

### Save a place

```
amb place-save <wallet_address> <google_maps_url> [--label LABEL] [--force]
```

- `<google_maps_url>`: a `google.com/maps/place/…` URL or a `maps.app.goo.gl/…` short link. The gateway resolves it to a canonical `ChIJ…` placeId and formatted address.
- `--label LABEL`: optional. Labels are case-insensitive (lowercased on write). Re-saving an existing label silently overwrites.
- `--force`: confirm an approximate match (see below).

**Exact match** — the URL resolves to a precise place. The CLI saves it immediately and exits 0.

**Approximate match** — when the URL cannot be resolved to an exact place, the CLI exits non-zero with:

```json
{ "error": "APPROXIMATE_MATCH_NEEDS_FORCE", "candidate": { "name": "…", "formatted_address": "…" } }
```

The agent MUST show the candidate `name` and `formatted_address` to the user and ask whether it is the correct place. Only after the user explicitly confirms should the agent re-run the same command with `--force` appended. Never pass `--force` without explicit user confirmation — and never in the same turn you first receive `APPROXIMATE_MATCH_NEEDS_FORCE`: stop, present the candidate, and wait for the user's reply first. This holds even if the user already named or labeled the place in their original request: an approximate match means the *resolved* candidate is uncertain, so it is the resolved candidate that must be confirmed, not the user's wording.

The persisted row includes more fields than agents typically need; for downstream ride construction use `name`, `formatted_address`, `latitude`, `longitude`, and `google_place_id`.

### List / look up saved places

```
amb place-list <wallet_address> [--match QUERY [--match QUERY ...]]
```

`--match` is repeatable. The agent should generate 2–5 candidate phrasings from the user's utterance (original wording, English transliteration, common aliases, plausible typos) and pass them all in one invocation.

Matching is **tier-per-pass union**:
1. Label exact (NOCASE) — first tier to hit wins.
2. Else name `LIKE %candidate%` (NOCASE union across all candidates).
3. Else formatted_address `LIKE %candidate%` (NOCASE union).
4. Else empty matches with `matched_tier: null`.

Output shape:

```json
{
  "matches": [ /* rows */ ],
  "matched_tier": "label" | "name" | "address" | null,
  "queries":      ["jacx", "잭스"],
  "next_action":  "USE_FOR_RIDE_OR_FALLBACK_TO_PLACE_SEARCH"
}
```

Empty matches return exit code `0` — this is the signal to fall through to `amb place-search`.

### Remove a saved place

```
amb place-remove <wallet_address> <id_or_label>
```

If the argument is an integer it's treated as the row `id`; otherwise as a `label`. Returns `{ removed: 1, id, label }` on success or `{ removed: 0, error: "NOT_FOUND" }` (still exit 0).

### Crypto saved-place shortcut (`mode: "wallet"` only)

Run `amb whoami` before considering this shortcut. It applies only to `mode: "wallet"`, because saved-place commands require a registered wallet address. For `mode: "tada"`, skip `place-list` and resolve named locations with the member flow's wallet-free `place-search` / `place-detail` commands below. Before either flow, apply the **"Acknowledge before a long booking turn"** guardrail in `SKILL.md`: unless this turn's response is a question (not signed in / no destination / already-known-ambiguous), send a short acknowledgement first, then proceed. See that guardrail for the OpenClaw `message send` mechanics.

Places stored locally include both favorites (explicit, with labels) and history (auto-tracked from every successful ride-request, no label). `amb place-list --match QUERY` returns both, but `is_favorite=1` rows are sorted ahead of history, then by `hit_count` and `last_used_at`. When mixed results appear:
- If an `is_favorite=1` row matches, use it directly.
- If only history rows match, confirm with the user before booking ("Want to go back to <X>?").

Promote a history row to favorite with `amb place-favorite <wallet> <id_or_dedup_key> --label LABEL`. Demote with `amb place-unfavorite <wallet> <id_or_label>` (preserves hit_count). Auto-history fields on each row: `is_favorite`, `hit_count`, `last_used_at`. `hit_count` counts requests, not completions — cancelled rides still count.

In `mode: "wallet"`, when the user names an origin or destination, start with:

1. Generate 2–5 candidate phrasings (original / English / alias / typo correction).
2. `amb place-list <wallet> --match "<c1>" --match "<c2>" …`
3. If `matches.length > 0`, construct the ride-request location directly from the row:

```json
{
  "name":      "<row.name>",
  "address":   "<row.formatted_address>",
  "latitude":  <row.latitude>,
  "longitude": <row.longitude>,
  "placeType": "GOOGLE",
  "placeId":   "<row.google_place_id>"
}
```

Skip `place-search` / `place-detail` / `map-session-create` for that endpoint. If `row.google_place_id` is null, omit both `placeType` and `placeId` — the ride still works on `name + address + lat/lng`.

If `matches` is empty (or the matched tier feels ambiguous and the candidates are off), fall through to the existing `place-search` flow.

## Ride

> **Two modes — run `amb whoami` first and read `mode`.** The ride commands have different argument forms per mode:
> - **`mode: "tada"` (TADA/Throo member)** — card-paid and wallet-free. Use the **Member mode** flow immediately below. **Do NOT call `setup-check`, `wallet-*`, collateral, SIWE, `ride-pay-prepare`, or `ride-pay-confirm`** — those belong to the crypto path, and wallet-only commands return `MODE_MISMATCH` for members.
> - **`mode: "wallet"` (crypto)** — collateral/USDC-paid. Use the `<wallet_address>`-prefixed forms and the payment flow (`ride-pay-prepare → wallet-sign → ride-pay-confirm`) documented in the subsections after this one.

### Member mode (`mode: "tada"`) — card-paid ride flow

A logged-in TADA/Throo member pays with a registered card. There is **no separate payment step**: `ride-request` creates a `PENDING` ride and the card is charged directly. Do not run any `ride-pay-*` command.

The card (`payment_item_uuid` in `ride-request`, `card_uuid` in `ride-search`) is **optional**. When omitted, the CLI resolves it automatically via the gateway `GET /v1/cards` (see **Card resolution** below) — so the normal flow is to leave it out entirely. Pass it explicitly only when re-running after a `needs_card_selection` prompt.

**1. Search** — positional args (no `wallet_address`, no `region`; region is resolved automatically from coordinates). The trailing `card_uuid` is optional:
```bash
amb ride-search <origin_lat> <origin_lng> <dest_lat> <dest_lng> [card_uuid] [--coupon-code CODE] --json
```

The normal result is `{ options[], routes, journey_id, search_id }`. In member mode `routes` is an **object keyed by car type** (e.g. `routes.CAR`), not an array — the crypto-mode `routes[]` array is a different shape. Each entry carries `distance_display` and `duration_display` already localized to the rider's region (US regions in miles, elsewhere in km), alongside the raw `distance_meter` / `duration_seconds`. Present the `*_display` strings verbatim — do **not** convert distance units yourself.

Preserve the CLI-generated `journey_id` and `search_id`; always pass `search_id` to the following `ride-request`. If local correlation storage is unavailable, the command preserves search behavior and may omit both handles. Each entry in `options[]` carries `product_name` — the rider-facing display name, already region-localized (e.g. `Save Throo` in NY). Present `product_name` to the user; do **not** surface the raw `car_type` / `product_type` enum values (`SEDAN`, `ANYTADA`) — the projection does not return them.

| Field | Meaning |
|---|---|
| `product_id` | Pass as `product_id` in `ride-request` |
| `product_name` | Rider-facing display name (already region-localized) |
| `price` | **The quoted total the rider is charged**, including an applicable coupon or promotion. A numeric string (e.g. `"31.35"`); the currency is in `price_currency`, never embedded here. Show exactly one price per option. |
| `price_currency` | ISO currency code for `price` (e.g. `USD`) |
| `na` | `true` when the option cannot be booked right now. This is the single availability signal — it already accounts for every reason booking would reject the option. |

When `discount` is present, inspect `discount.applicable`; HTTP 200 alone is not proof that a coupon applied. `discount.coupon_code` is the user coupon to copy into `ride-request`. `discount.campaign_promotion_code` is a server campaign and must never be used as `coupon_code`.

A campaign promotion may be applicable even when no coupon code was sent. Keep its discounted `price` in the normal quote, but leave `coupon_code` out of `ride-request`; the server re-evaluates the campaign during creation. Do not gate campaign pricing on explicit coupon intent.

For an applicable coupon, `price` already includes fees that are outside the coupon calculation basis. Do not replace it with `discount.discounted_price`, recalculate it, or show that nested field as the final charge.

An option with `na: true` always has `price: null`, and an option with `na: false` always has a `price`. Offer only `na: false` options to the rider.

**2. Request** — a single JSON argument. `locations` is `[origin, destination]`; `payment_item_uuid` (the card) is optional. `product_id` is optional without a coupon and required when `coupon_code` is present:
```bash
amb ride-request '{"search_id":"<search_id from ride-search>","locations":[{"latitude":<oLat>,"longitude":<oLng>,"name":"<origin name>","address":"<origin address>"},{"latitude":<dLat>,"longitude":<dLng>,"name":"<dest name>","address":"<dest address>"}],"product_id":<required with coupon_code; otherwise optional int>,"coupon_code":"<optional exact code>","confirmed_price":"<required with coupon_code: exact quoted price>"}'
```
Agent-required fields are `search_id` from the selected search result and `locations`. The CLI still accepts a missing `search_id` for backward compatibility, but that request cannot join the correlated telemetry funnel. On success the ride is created in `PENDING` and the card is charged — **immediately start `ride-relay.js`** (see the ride-relay section). Do **not** call `ride-pay-prepare`/`ride-pay-confirm`.

#### Member coupons

Coupon commands are member-only and should be called with `--json` when their output feeds the booking flow:

```bash
amb coupon-current [--page N] [--page-size N] [--sort createdAt|validUntil[,asc|desc]] --json
amb coupon-past [--status used|expired] [--page N] [--page-size N] [--sort createdAt|validUntil[,asc|desc]] --json
amb coupon-detail <code> --json
amb coupon-register <case-sensitive-code> --json
amb coupon-available '{"locations":[...],"product_id":<id>,"payment_item_uuid":"<optional card>"}' [--lang TAG] --json
```

Use this sequence for a member booking unless the user supplies a code or explicitly declines coupons:

1. Run the normal member `ride-search` and select a bookable product. Keep its locations, product id, card, and currency as the comparison context. `discount.available_coupon_count` is not proof that those coupons apply to this route/product; do not announce an applicable-coupon count before the next step.
2. Run `coupon-available` with the same locations and `product_id`. Its JSON result is the gateway coupon array. Keep only entries whose `available` is `true`; unavailable entries may be explained using `unavailable_reason`. Treat an unknown numeric `status` or `discount_type` as unavailable even though its raw value is preserved.
3. Preserve the gateway order and evaluate exactly the first three remaining codes, or all remaining codes when fewer than three exist. Re-run `ride-search --coupon-code <exact code> --json` for each evaluated code. In each response, select the comparison product by the original `product_id`; keep only `na: false`, `discount.applicable: true`, and an exact `discount.coupon_code` match. Do not fan out across every product and every coupon.
4. Rank the valid quotes by lowest rider-facing `price` in the same currency among the evaluated candidates. For equal prices, preserve the original gateway order. Present the winner first, then show every successfully evaluated candidate's exact rider-facing price with its code/title and available discount metadata so the rider can compare and choose. Do not invent or display a price for an unavailable or unsuccessfully evaluated candidate. The winner is applied to the quote only — do not create the ride yet. This bounded evaluation is not a guarantee of the best coupon across all held coupons or all products.
5. Ask for booking confirmation with the winner's exact `price`. If the user chooses an alternative, re-quote that code and show its exact price before asking again.
6. Run `ride-request` with the `search_id` from the final re-quote for the coupon the user selected, the selected `product_id`, the confirmed exact `coupon_code`, and the quoted `price` string in `confirmed_price`. The CLI requires the three coupon confirmation fields (`product_id`, `coupon_code`, and `confirmed_price`), performs the mandatory fresh server quote, accepts only an equivalent canonical decimal amount, and refuses to create the ride if that rider-facing total changed after confirmation.

If the user directly supplies a known code, skip discovery and comparison, honor that code, and re-quote it; the three-candidate cap does not apply, and booking must use that re-quote's `search_id`. If no evaluated candidate applies, show the normal quote and say that no usable coupon was found. Requests to apply a coupon automatically, choose the best coupon, or choose the cheapest coupon all use the bounded explicit-code comparison above; there is no separate server-side auto-apply path. A campaign-only `campaign_promotion_code` is never a booking code. Never infer application from HTTP 200, and never switch payment away from card. `COUPON_PRICE_CHANGED` requires showing a new quote, obtaining confirmation again, and booking with that new quote's `search_id`. Any coupon failure during booking requires a new quote or explicit user approval to continue without it; the CLI never retries couponless automatically.

> **Coordinates must be flattened out of the place response.** `place-search` / `place-detail` nest coordinates under `lat_lng`, and each location you send must carry them **top-level** as `latitude` / `longitude`:
>
> ```
> place-detail  →  { "place_id": …, "name": …, "lat_lng": { "latitude": 40.762048, "longitude": -73.938523 } }
> ride-request  →  { "place_id": …, "name": …, "latitude": 40.762048, "longitude": -73.938523 }
> ```
>
> The command tolerates the nested `lat_lng` container and the short `lat` / `lng` spelling, but emit the canonical flat form — it is the only shape the gateway itself accepts. Never omit the coordinates and expect them to be inferred: a location whose coordinates cannot be read fails with `INVALID_COORDINATES` rather than being routed to a guessed region. A `place-list` row already uses `latitude` / `longitude` and needs no conversion.

**3. Status / cancel** — the ride id is the `request_id` returned by `ride-request`:
```bash
amb ride-status <request_id>
amb ride-cancel <request_id> [reason] [--reason-type <id>]   # member form: no wallet_address argument
amb ride-cancel-penalty <request_id> [--reason-type <id>]    # member-only: preview cancellation fee before cancelling
```

After the driver is assigned, member-mode cancellation is a **two-step protocol** — the first call returns the reason list instead of cancelling. See `ride_cancel` below.

The status values and cancel-confirmation etiquette are identical to crypto mode — see `ride_status` and `ride_cancel` below. **Share links differ by mode:** member mode has no inline `rideShareUrl` on `ride-status` — use the `ride-share` command below (it calls the gateway). Monitor events are the exception: after a driver is assigned, the monitor fetches the link in the background, and from then on `ride_event` payloads carry `rideShareUrl` in both modes. The member-mode fetch is best-effort — if the gateway is slow or failing, the first events after assignment carry no link (and a ride where every attempt fails carries none at all). Crypto mode surfaces `rideShareUrl` inline on `ride-status` as well.

#### Card resolution

When the active mode is `tada` (TADA/Throo member), `payment_item_uuid` in `ride-request` and `card_uuid` in `ride-search` are **optional**. The CLI calls the gateway `GET /v1/cards` internally and selects the card automatically — the agent does not call this endpoint directly.

**Fields in the `needs_card_selection` payload.** When the CLI cannot resolve a single card, each entry in the emitted `cards[]` array carries only these fields:

| Field | Notes |
|-------|-------|
| `id` | Use this value as `payment_item_uuid` (ride-request) or `card_uuid` (ride-search) |
| `card_brand` | Card brand, e.g. `"American Express"` (may be `null`) |
| `card_last4` | Last 4 digits, for display |
| `is_expired` | Authoritative expiry flag — trust this; do **not** recompute from expiry dates |
| `is_default` | Per-card flag set by the user in the TADA/Throo app; NOT the account-level default payment method |

**Additional fields of the underlying card record** (present on the full card object the CLI uses internally, but NOT in the `needs_card_selection` payload above): `exp_month` / `exp_year` (may be `0` = unknown — treat `0` as "not available", not "January year 0"), `country`, `issuer`.

**Resolution outcomes:**

| Condition | Result |
|-----------|--------|
| 0 cards or all `is_expired` | `NO_CARD` error — tell user to add a card in the TADA/Throo app |
| 1 non-expired card | That card is auto-selected; ride proceeds without agent action |
| 2+ non-expired cards, exactly one with `is_default: true` | The default is auto-selected; ride proceeds without agent action |
| 2+ non-expired cards, no single default | Returns `{ needs_card_selection: true, cards: [...], next_action: "ASK_USER_TO_PICK_CARD_THEN_RERUN_WITH_payment_item_uuid" }` — present the list, ask the user to pick, re-run with the chosen card's `id` |
| Card lookup fails (gateway error or expired session) | `CARD_LOOKUP_FAILED` error |

Cards are **scoped to the pickup's region**: the lookup runs against the regional gateway derived from the origin coordinates. Correct coordinates are therefore a precondition for finding the rider's cards — this is why a location with unreadable coordinates is rejected outright (`INVALID_COORDINATES`) instead of being routed to a default region. If a user insists a card exists in the app but you get `NO_CARD`, re-check the coordinates you passed before telling them to add another card.

Card register, delete, and set-default operations are not exposed by the CLI — they live in the TADA/Throo rider app.

### Crypto mode (`mode: "wallet"`) — collateral/USDC ride flow

> **JWT expired / `JWT_NOT_FOUND` mid-ride → re-authenticate with the registered wallet, then retry the failed command.**
> For MetaMask, follow the typed-login and exact-resume contract in [Wallet reference](wallet.md). For Built-in Privy, run these three legacy SIWE commands **in order**. They are **positional — do NOT invent `--siwe` / `--file` / any flag**, and the argument order is exact:
> ```bash
> amb siwe-request-message <wallet_address> <chain_id>   # → returns siwe_file path
> amb wallet-sign <wallet_address> personal_sign <siwe_file>   # 3rd arg is the FILE PATH, not the message text → returns signature
> amb siwe-submit <siwe_file> <signature>                # order: siwe_file FIRST, then signature
> ```
> `chain_id`: `84532` (BASE_SEPOLIA) or `11155111` (ETH_SEPOLIA). Full reference: `references/wallet.md` → SIWE Authentication.

### ride_search - Search for a ride

```bash
amb ride-search <wallet_address> <region> <origin_lat> <origin_lng> <dest_lat> <dest_lng>
```

- `region`: Service region code (`SG`, `NY`, `KH`, or `HK`)

Searches available ride products for the given origin/destination coordinates.
The `search_id` (checkSum) from the result is cached in DB for 3 minutes.

Each entry in the result's `routes[]` carries `distance_display` and `duration_display` already localized to the ride's region (US regions in miles, elsewhere in km). Present these strings verbatim — do **not** convert distance units yourself.

Each entry in `options[]` also carries `price` and `price_currency`. In crypto mode `price_currency` is the **pay currency** (e.g. `USDC_base_sepolia`) because the projection selects the price entry matching it — so `price` is directly comparable to the `usdc` figure from `amb wallet-balance`, with no conversion. (Member mode's identically-named fields are fiat; see "Member mode" above.)

### ride_request - Request a ride

```bash
amb ride-request <json_params>
```

`json_params` example:
```json
{
  "wallet_address": "0x...",
  "search_id": "checkSum from ride_search",
  "product_code": "STANDARD",
  "region": "SG",
  "pay_currency": "USDC_base_sepolia",
  "locations": [
    {
      "name": "Marina Bay Sands",
      "address": "1 Bayfront Avenue, Singapore 018971",
      "latitude": 1.2834,
      "longitude": 103.8607,
      "placeId": "ChIJ..."
    },
    {
      "name": "40 Sin Ming Lane",
      "address": "40 Sin Ming Lane, Midview City, Singapore 573958",
      "latitude": 1.3491,
      "longitude": 103.8321,
      "placeId": "ChIJ..."
    }
  ],
  "rider": { "name": "John Doe", "phone": "+821012345678" }
}
```

**Before calling `ride-request`, you must have both the rider's name and phone number confirmed by the user. If not already provided in the conversation, ask the user for their name explicitly. Never invent or guess a name.**

The `locations` array is [origin, destination] in order.

- `pay_currency`: Always use `USDC_base_sepolia` (Base Sepolia environment)
- `wallet_provider_id` is determined automatically from `pay_currency` — do not specify it

**⚠️ After ride_request succeeds, you MUST complete payment before starting ride-relay:**
```bash
amb ride-pay-prepare <request_id> <wallet_address>   # → returns typed_data JSON to sign
amb wallet-sign <wallet_address> eth_signTypedData_v4 '<typed_data_json>'   # payment uses eth_signTypedData_v4 + JSON (NOT personal_sign/siwe_file — that form is SIWE re-auth only)
amb ride-pay-confirm <request_id> <signature>
```
Then start `ride-relay.js` in the background. Do NOT start ride-relay while status is `WAITPAY`.

## Member place search

When the active mode is `tada` (TADA/Throo member), use the five gateway-backed place commands below to resolve a place name or coordinates into a bookable `place_id` + coordinates before calling `ride-search` / `ride-request`.

> **placeId provenance rule (strictly enforced)**
> Any `place_id` passed to a subsequent command (`place-detail`, `ride-search`, `ride-request` `locations[].place_id`) MUST be copied verbatim from the response of one of these commands. Never fabricate or substitute a place_id from model knowledge.

### Command signatures

```bash
amb place-search <query> <region> [originLat originLng] [--city CODE] [--session-token UUID] [--lang TAG] --json
amb place-detail <place_id> <region> [city] [--lang TAG] --json
amb place-nearby <lat> <lng> [limit] [--lang TAG] --json
amb place-airports <city> [--lang TAG] --json
amb place-reverse-geocode <lat> <lng> <region> [--lang TAG] --json
```

- `region`: Two-letter region code. Currently supported: **`NY`**, **`SG`**, **`KH`**, **`HK`**. Any other value returns an error — there is no fallback.
- `city`: TADA city code (e.g. `NYC`), not free text. Used by `place-airports` (required) and `place-detail` (optional hint).
- `originLat` / `originLng`: Optional bias point for `place-search` — pass the user's current coordinates when known.
- `limit` (place-nearby): Optional integer cap on results.
- `--lang TAG`: Optional BCP 47 language tag for localised names (e.g. `en`, `ko`).
- `--session-token UUID`: Optional session continuity token for `place-search`.

### Response shapes

**place-search / place-nearby / place-airports** — list response:
```json
{
  "places": [ /* PlaceResult[] — may be empty */ ],
  "next_action": "...",
  "must": "..."
}
```

`places` can be an empty array (`[]`) — this is a **normal 200 response**, not an error. Never treat an empty list as a failure; ask the user to try a different query or pick-up point.

**place-detail / place-reverse-geocode** — single-record response. These are the only commands that can return `404 place_not_found` (no result for the given id or coordinates).

### PlaceResult fields

| Field | Type | Notes |
|-------|------|-------|
| `place_id` | string | Opaque. TADA UUID or Google `ChIJ…` id. Copy verbatim. |
| `name` | string | Display name |
| `address` | string | Formatted address |
| `lat_lng` | `{latitude, longitude}` or `null` | Present for TADA POIs (`place_type 0`); **may be `null` for Google candidates (`place_type 10`)** — resolve with `place-detail` before booking |
| `place_type` | integer | `0` = TADA POI (ranked first), `10` = Google, `20` = OneMap |
| `allowance_type` | integer | `0` = Both, `1` = Pickup only, `2` = Dropoff only |
| `sub_places` | array | Bookable sub-points of a terminal (see below) |
| `nearest_place_id` | string \| null | Present on any place record; non-null mainly on reverse-geocode when a TADA POI is near the point, null otherwise |
| `pickup_disclaimer_type` | string \| null | Open string set — pass through as-is; do not fabricate |
| `dropoff_disclaimer_type` | string \| null | Open string set — pass through as-is; do not fabricate |

`place_type` and `allowance_type` are integer enums — pass through verbatim; do not fabricate values.

### Resolve → ride flow

1. **place-search**: search by query string and present the `places` list to the user.
2. **User picks a result.** Check `lat_lng`:
   - `lat_lng` present (TADA POI / OneMap): use coordinates directly — skip `place-detail`.
   - `lat_lng` is `null` (Google candidate): run `place-detail` with the same `region` to resolve coordinates. If `place-detail` also returns `null` coords, ask the user to pick a different result.
3. **Terminal sub_places**: If the place is an airport or major terminal, `sub_places` may contain bookable points. Each sub_place has its own `allowance_type`:
   - `1` (Pickup): use for origin → book as `sub_place_id` + the sub_place's `lat_lng` + `name_with_main_place`
   - `2` (Dropoff): use for destination → same pattern
   - `0` (Both): can be used for either leg
   Present the relevant sub_places to the user if they exist; ask which one to use.
4. **Build LocationRequest** — copy values verbatim into the **flat** shape below. `latitude` / `longitude` are top-level (NOT nested under a `lat_lng` object); read them out of the response's `lat_lng` and place them at the top level. Sending a nested `lat_lng` object is rejected with `gateway 400 invalid_parameter`.
   ```json
   {
     "latitude":  <lat_lng.latitude from response>,
     "longitude": <lat_lng.longitude from response>,
     "name":      "<name or name_with_main_place from response>",
     "address":   "<address from response>",
     "place_id":  "<place_id from response — verbatim>"
   }
   ```
   When booking a sub_place, also include `"sub_place_id": "<sub_place.id>"`.
5. **Ride**: pass the resolved locations into `amb ride-search` / `amb ride-request` (member).

### Alternative place-lookup commands

| User intent | Command to use |
|-------------|----------------|
| "Near me" / nearby TADA pickup points | `place-nearby <lat> <lng>` — returns TADA POIs only |
| Airport / terminal by city | `place-airports <city>` — e.g. `amb place-airports NYC` |
| Coordinates → address / place | `place-reverse-geocode <lat> <lng> <region>` — returns the nearest place; `nearest_place_id` if a TADA POI is close |

Use `place-nearby` or `place-airports` instead of `place-search` when the user's intent clearly matches those cases; it reduces round trips and returns better-typed results.

### ride_status - Check ride status

```bash
amb ride-status <request_id> [wallet_address]
```

Returns the current status and driver info of a ride request.

Status values (in lifecycle order):

| Status | Phase | Meaning |
|--------|-------|---------|
| `WAITPAY` | Pre-ride | Ride requested, waiting for payment |
| `PAYCONFIRMED` | Pre-ride | Payment confirmed, entering driver matching |
| `PENDING` | Matching | Searching for available drivers |
| `NOT_MATCHED` | Terminal | No driver found within matching window |
| `MATCHED` | Matching | Driver candidate found (not yet accepted) |
| `CONFIRMED` | Matching | System confirmed the match |
| `ASSIGNED` | Active | Driver accepted and assigned to the ride |
| `PICKUP` | Active | Driver is **driving toward** the pickup point (NOT "picked up") |
| `PICKUP_ARRIVED` | Active | Driver **arrived at** the pickup point, waiting for passenger |
| `INUSE` | Active | Passenger is in the car, ride **in progress** |
| `FINISHED` | Terminal | Ride completed successfully |
| `USER_CANCELED` | Terminal | Cancelled by the rider |
| `USER_CANCELED_BEFORE_CALL` | Terminal | Cancelled by the rider before driver matching started |
| `USER_CANCELED_NO_FREE` | Terminal | Cancelled by the rider (cancellation fee charged) |
| `DRIVER_CANCELED` | Terminal | Cancelled by the driver |
| `DRIVER_CANCELED_RECALLABLE` | Terminal | Cancelled by the driver (can re-request with same search) |
| `COMPANY_CANCELED` | Terminal | Cancelled by the operator |
| `COMPANY_CANCELED_RECALLABLE` | Terminal | Cancelled by the operator (can re-request with same search) |
| `EXPIRED` | Terminal | No driver found, request expired |
| `EXPIRED_RECALLABLE` | Terminal | Expired but can be re-requested with the same search |
| `EXPIRED_BEFORE_PAY` | Terminal | Payment window expired before payment was made |
| `ERROR_PAYMENT` | Terminal | Payment processing error |
| `ERROR` | Terminal | Unexpected system error |

If the `driverInfo` field is present, a driver has been assigned (status is `ASSIGNED` or later). When `driverInfo` is present and the response also includes `rideShareUrl`, surface it to the user as a markdown link (e.g. `[ride share](url)`) — this is a public live-tracking URL the user can share externally. Ignore `rideShareUrl` before driver assignment.

### ride_share - Get a shareable trip-tracking link

```bash
amb ride-share <request_id> [--lang TAG]
```

Returns a public link others can open to follow the trip's live location and status. Works in both modes from the local `request_id`:
- **Member**: calls the gateway share endpoint. `--lang` localizes the optional share `message` (en, ko, ja, th, vi, km, es, zh-CN, zh-TW; default `en`).
- **Crypto**: returns the inline `rideShareUrl` (available only after a driver is assigned).

Output (member): `url`, `urlId`, optional `message`, optional `chatUrl`. Crypto returns just `url`. Surface `url` to the user as a markdown link.

Errors: `SHARE_NOT_AVAILABLE` (crypto, before driver assignment) · `SHARE_LINK_FAILED` (gateway error) · `RIDE_NOT_FOUND` (no local ride record).

### ride_cancel - Cancel a ride request

```bash
# member: amb ride-cancel <request_id> [reason] [--reason-type <id>]
# crypto: amb ride-cancel <request_id> [wallet_address] [reason]
```

- `request_id`: `requestId` returned after running `ride_request`
- `wallet_address`: crypto mode only. Auto-looked up from local DB if omitted; required if not in DB.
- `reason`: free-text cancellation note (optional)
- `--reason-type <id>`: the id of a reason the **rider** picked from the `cancel_pending` list (see below)

**⚠️ Always follow this order:**

1. Run `amb ride-status <request_id>` to check the current ride status
2. If `driverInfo` exists or status is `ASSIGNED` or later → clearly inform the user that **a cancellation fee may apply** and ask them to confirm
3. Run `amb ride-cancel <request_id>` only after the user confirms

#### Two-step cancellation after driver assignment (member mode)

Once the ride reaches `ASSIGNED` / `PICKUP` / `PICKUP_ARRIVED`, the server requires a
cancellation reason. Calling `ride-cancel` without `--reason-type` therefore **does not
cancel the ride**. It exits 0 with:

```json
{
  "cancel_pending": true,
  "ride_status": "PICKUP",
  "reasons": [ { "id": 17, "title": "Found another travel option" }, { "id": 999, "title": "Others" } ],
  "cancellation_fee": 5,
  "cancellation_fee_currency": "USD",
  "fee_varies_by_reason": true,
  "message": "Ride is NOT cancelled yet. ..."
}
```

`cancel_pending: true` means **the ride is still active**. Do not tell the user it was
cancelled, and do not report an error — this is step 1 of 2.

1. Show the `reasons` list and the fee to the rider.
2. **The rider picks the reason. You must never choose one on their behalf — not even
   `999` / "Others".** Picking for them files a false reason against the driver and can
   change the fee. If the rider will not pick, the ride stays active; say so.
3. Re-run with their choice: `amb ride-cancel <request_id> --reason-type <id>`.

`cancellation_fee` is the **default** fee (`fee_varies_by_reason: true`); the actual fee
depends on the reason. For an exact figure before committing, run
`amb ride-cancel-penalty <request_id> --reason-type <id>`.

The reason list **narrows as the ride advances** (e.g. once the driver arrives). If the
rider deliberates and the chosen id has gone stale, the CLI re-issues a fresh
`cancel_pending` with the current list — present it again rather than retrying the old id.

No reason is required — and `ride-cancel` cancels immediately, as before — for member rides
before assignment (`PENDING`/`CONFIRMED`), and for crypto rides in **any cancelable status**
(`PAYCONFIRMED`, `PENDING`, `ASSIGNED`, `PICKUP`, `PICKUP_ARRIVED`). Crypto has no reason
list yet, so it cancels in one step even after assignment; outside those statuses it is
refused locally (see `RIDE_NOT_CANCELABLE` below).

Response (on an actual cancellation):
- `isFreeCancel`: Whether this is a free cancellation (crypto; for recording purposes)
- `pickupStartTime`: Time the driver departed (null if not yet departed)
- `cancelRequestedAt`: Time the cancellation was requested

Errors:
- `RIDE_NOT_CANCELABLE` — the ride cannot be cancelled at all. Do not ask for a reason and
  do not retry; the envelope carries the `status`. Raised when the ride is **in progress**
  (`INUSE`) or already ended (finished/expired/cancelled) — for a ride already underway the
  rider must ask the driver to end the trip. **In crypto mode it is also raised for
  `WAITPAY`, `MATCHED`, and `CONFIRMED`** — pre-payment and matching-transition states that
  the crypto backend refuses. `WAITPAY` is the status a crypto ride sits in right after
  `ride-request`, before payment confirms: nothing to retry away, so either complete the
  payment flow (`ride-pay-prepare` → `ride-pay-confirm`) or wait for the ride to reach
  `PAYCONFIRMED` before cancelling. This check is local — no server call is made.
- `RIDE_CANCEL_FAILED` with a "payment is being held" message — a transient pre-payment
  hold (~30s). Retry shortly.
- `INVALID_ARGUMENT` — `--reason-type` was missing or not an integer id from the list.

### Payment flow (ride_pay_prepare → wallet_sign → ride_pay_confirm)

Complete these three steps in sequence immediately after `ride_request`:

**Step 1. Prepare payment:**
```bash
amb ride-pay-prepare <request_id> <wallet_address> --json
```
Returns `{ typed_data }` — EIP-712 typed data for signing.

**Step 2. Sign the typed data:**
```bash
amb wallet-sign <wallet_address> eth_signTypedData_v4 '<typed_data_json>'
```
Pass the `typed_data` JSON from step 1 as the message argument. Returns `{ wallet_signature }`.

**Step 3. Confirm payment:**
```bash
amb ride-pay-confirm <request_id> <signature>
```
Pass the `wallet_signature` from step 2. Returns `{ success, tx_hash }`.

If `ride-request` returns `POLICY_EXCEEDED` before creation, follow the
[spend-policy approval flow](spend-policy.md#basic-ride-flow): choose once/raise, issue a link
with the original ride JSON, poll, and retry creation with `approval_id`. Keep the same trip
when refreshing an expired search. Once created, preserve that request ID for payment.
If payment preparation or confirmation later reports a limit blocker, explain it and stop.
Do not issue a new creation-time approval or create a replacement ride automatically.

## ride-relay (event streaming)

Streams ride status and driver chat events from the mode-specific commit point:

- **Member (`mode: "tada"`)** — start immediately after `amb ride-request`
  succeeds. Member rides have no separate `ride-pay-*` step.
- **Crypto (`mode: "wallet"`)** — start only after `amb ride-pay-confirm`
  returns `success: true`; never start while status is `WAITPAY`.

### How to start

At the applicable commit point above, start ride-relay using the platform's background primitive:

```bash
node ${SKILL_DIR}/scripts/ride-relay.js <request_id> [--agent <agent-id>] [--session-key <session-key>] [--session-id <sid>] [--once]
```

This is the invocation form for the stdout-passthrough platforms (Claude Code
Monitor, Hermes, codex/other) that run ride-relay.js directly. **On OpenClaw, do
not background this `node …/ride-relay.js` form directly** — background the
`ride-relay.sh` launcher (see the OpenClaw bullet below); a direct background
launch is exposed to the process-group startup race the launcher's `setsid` closes.

Refer to SKILL.md → "Event streaming: ride-relay" for the correct primitive per platform:

- **Claude Code:** the `Monitor` tool, with ride-relay as its `command` (e.g. `node ${SKILL_DIR}/scripts/ride-relay.js <request_id>`). Monitor runs the command itself and turns each stdout line into a live notification, so every `ride_event` reaches the user as it arrives; the relay self-exits on the terminal `ride_event`, which ends the watch. Do **not** run the relay under a backgrounded `Bash` and try to attach `Monitor` to that shell — `Monitor` streams the stdout of its *own* command, it cannot watch a separate background process.
- **Hermes:** `terminal(background=true, notify_on_complete=true)` with `--once`; on each `[IMPORTANT: Background process … completed]` notification, parse the status line, report it to the user verbatim, and spawn the next relay (agentic loop) until terminal status. See SKILL.md → "Hermes extra" for the loop and the manual-drain fallback.
- **OpenClaw:** background the **`ride-relay.sh`** launcher — `sh ${SKILL_DIR}/scripts/ride-relay.sh <request_id> &` (or `nohup … &`). The launcher `exec`s the relay under `setsid`, so it lives in its own session from exec time — *before* Node boots — and OpenClaw's process-group kill on tool-call return cannot reap it during startup. It prints a `RELAY_DETACHED` note with the child pid and its log path (`~/.amb/run/relay-<request_id>.log`), and the command you ran exits immediately. Do not wait on it. **Do not** launch `node ${SKILL_DIR}/scripts/ride-relay.js <request_id> &` directly on OpenClaw: ride-relay.js still self-detaches, but only after Node has booted, leaving a startup window where the group-kill can land first and the ride goes silent after booking. Pass only `<request_id>`: ride-relay self-resolves its agent from the configured agents/workspace and its session from the unique active transcript containing that ride id. It never guesses the freshest session. `--agent`, `--session-key`, and `--session-id` remain optional compatibility/debug hints and must not be invented. `--once` under OpenClaw is ignored (no-op) — the relay stays long-running. See SKILL.md → "OpenClaw extra" for deterministic resolution + hybrid (channel-aware) delivery behavior.
- **Other:** platform's own background primitive; ride-relay runs in stdout passthrough mode.

After starting, tell the user the ride was requested and monitoring is active, then continue handling arriving events.

### Stdout event schema

Each line ride-relay emits on its stdout is a single JSON event.
**Key fields** the LLM cares about:

| Field | Meaning | Handling |
|---|---|---|
| `type` | `ride_event`, `chat_event`, `monitor_event`, ... | branch on it |
| `terminal` | `true` when the ride has reached a terminal status (`FINISHED`, `USER_CANCELED*`, `DRIVER_CANCELED*`, ...) | on `true`, notify the user and end the loop |
| `prompt` | instruction text for the agent (already formatted for human reading) | surface to user / take action verbatim |

Other fields (`requestId`, `ts`, `seq`, `eventId`, `payload`) are metadata — the LLM doesn't need to handle them.

| `type` | When | Agent action |
|--------|------|--------------|
| `ride_event` (terminal=false) | ride status changed | notify user of the new status |
| `ride_event` (terminal=true) | ride reached terminal status | tell user the outcome; exit loop; do NOT restart |
| `chat_event` | driver sent a chat message | relay sender + content to user |
| `monitor_event` phase=started | monitor process came up | no user-facing action |
| `monitor_event` phase=error | transient error in monitor | no action; monitor handles retry |
| `monitor_event` phase=exiting | monitor about to terminate | see Reconnect below |

No heartbeats are emitted; absence of output is normal. stderr is diagnostic only.

### Reconnect after termination

ride-relay is cursor-resumable — re-running the same command picks up automatically from where it left off (at-least-once). Termination handling:

1. **exit code 0 + last stdout line has `terminal=true`** → ride is done. Tell the user the outcome; do NOT restart.
2. **exit code 1** → fatal initialization error (auth expired, missing request, ...). Restarting will fail the same way; surface to user.
3. **anything else (exit 2, SIGKILL, runtime timeout)** → transient termination. Restart with the same command.
   - However, if the same command exits 1 three times in a row, stop and surface to user.

Before restarting, it's good practice to call `amb ride-status <request_id>` to check the ride is still active (if it's already terminal, no restart needed).

### Exit codes

| code | Meaning |
|---|---|
| 0 | reached a terminal `ride_event`; normal exit. |
| 1 | fatal initialization error (auth, missing request, ...). |
| 2 | received `SIGTERM` / `SIGINT`. |

### Driver info presentation

When a `ride_event` carries a `driverInfo` object (driver assigned), the payload looks like:

```json
{
  "driverInfo": {
    "carPlate": "1231A",
    "carModel": "Model",
    "profilePhotoUrl": "https://...",
    "name": "HAYDEN WOO"
  }
}
```

Present driver info to the user in this order of priority: **license plate (carPlate) → car model (carModel) → photo (profilePhotoUrl) → name (name)**.
If `profilePhotoUrl` is present, send it as an image using the `message` tool with `media=<profilePhotoUrl>`.

If the `ride_event` payload contains `rideShareUrl` (both modes carry it once a driver is matched and the link has been retrieved — treat its absence as "not yet", not as an error), surface it to the user as a markdown link (e.g. `[ride share](url)`) so they can share the live ride status externally.

### Sending chat messages

To send a message to the driver while ride-relay is running, use `amb chat-send-message` (see `references/chat.md`).

### Ride status classification

Used by the reconnect procedure to decide whether to restart ride-relay after an unexpected process termination.

**Active** (ride-relay should be running; restart on abnormal exit):
- `PAYCONFIRMED`, `PENDING`, `MATCHED`, `CONFIRMED`, `ASSIGNED`, `PICKUP`, `PICKUP_ARRIVED`, `INUSE`

**Terminal** (do not restart):
- `FINISHED`, `USER_CANCELED`, `USER_CANCELED_BEFORE_CALL`, `USER_CANCELED_NO_FREE`, `DRIVER_CANCELED`, `DRIVER_CANCELED_RECALLABLE`, `COMPANY_CANCELED`, `COMPANY_CANCELED_RECALLABLE`, `EXPIRED`, `EXPIRED_RECALLABLE`, `EXPIRED_BEFORE_PAY`, `NOT_MATCHED`, `ERROR_PAYMENT`, `ERROR`

### Event handling

1. When a `ride_event` with `driverInfo` present is received (driver assigned) → chat WebSocket connects automatically within the monitor process; no extra setup needed.
2. When a `ride_event` with `terminal: true` is received → ride-relay exits on its own. Handle by status:

**Terminal status handling:**

| Status | Action |
|--------|--------|
| `FINISHED` | Inform the user the ride is complete. Check tip availability with `amb tip-config` for the ride's region and offer a tip when enabled. Also offer an on-demand receipt, but do not query it until the user explicitly asks. On request, run `amb ride-receipt <request_id>` and surface stdout verbatim. |
| `USER_CANCELED` | Inform user the ride was cancelled. No tip. |
| `USER_CANCELED_BEFORE_CALL` | Inform user the ride was cancelled (before driver matching). No tip. |
| `USER_CANCELED_NO_FREE` | Inform user the ride was cancelled and a cancellation fee was charged. No tip. |
| `DRIVER_CANCELED` | Inform user the driver cancelled. Offer to search for a new ride. |
| `DRIVER_CANCELED_RECALLABLE` | Inform user the driver cancelled. Offer to re-request immediately (same search parameters). |
| `COMPANY_CANCELED` | Inform user the ride was cancelled by the operator. Offer to search for a new ride. |
| `COMPANY_CANCELED_RECALLABLE` | Inform user the ride was cancelled by the operator. Offer to re-request immediately (same search parameters). |
| `EXPIRED` | Inform user that no driver was found and the request has expired. Offer to search again. |
| `EXPIRED_RECALLABLE` | Inform user that no driver was found but the ride can be re-requested with the same search. Offer to re-request immediately. |
| `EXPIRED_BEFORE_PAY` | Inform user the payment window expired. Offer to search for a new ride. |
| `NOT_MATCHED` | Inform user that no driver was matched. Offer to search for a new ride. |
| `ERROR_PAYMENT` | Inform user of a payment processing error. In wallet mode, run `amb wallet-balance` and `amb deposit-status`; in member mode, diagnose the card/member error without wallet commands. |
| `ERROR` | Inform user of a system error. In wallet mode during a crypto ride, run `amb setup-check <wallet_address>`; in member mode, inspect member authentication and the failing command instead. |

**Do not tell the user to wait** — report each event as it arrives. **Never say "let me know if you'd like to check the status" — do not hand the trigger to the user.**

> On any expiry / no-match, follow the SKILL.md **Guardrails**: offer a TADA re-search **once** (never a competitor or any other ride app), and do not speculate about why it expired beyond "no driver matched in time." See SKILL.md → Guardrails.

## Ride History

### ride_history - List completed rides

```bash
amb ride-history <wallet_address> [limit]
```

- Returns completed rides with `tipInfo.tipPaymentAvailable` per ride.
- Display per ride: `rideTimeStamp`, `pickup → destination`.

### ride_history_detail / ride_receipt

```bash
# Raw wallet detail:
amb ride-history-detail <wallet_address> <request_id>
# Raw member detail, when member mode is active:
amb ride-history-detail <request_id>
# Canonical user-facing receipt:
amb ride-receipt <request_id>
```

`ride-history-detail` is raw diagnostic output. Wallet detail comes from
`GET /v2/ride-histories/detail/{rideRequestId}`; member detail comes from
`GET /v1/rides/{rideId}`. `--account=tada|wallet` may override its diagnostic mode.

`ride-receipt` is canonical Markdown; surface it verbatim. Its local ride record
selects wallet or member mode, and a conflicting `--account` override is rejected.
It preserves nested fare items for both modes. Wallet receipts also show currency
conversion context and payment, refund, and paid-tip transaction links.

Canceled or unsettled rides do not produce a canonical receipt;
`RECEIPT_NOT_READY` asks the caller to retry later.

## Full Crypto Ride Booking Flow

0. Initial setup (first time only)
```bash
# Built-in Privy wallet (agent: always pass --no-wait — see references/wallet.md)
amb wallet-setup --no-wait
```

1. Check wallet status
```bash
amb wallet-status
```

2. Login (required to obtain JWT)
```bash
# MetaMask: follow the typed-login contract in references/wallet.md
# Built-in Privy:
amb siwe-request-message 0x1234... <chain_id>
amb wallet-sign 0x1234... personal_sign <siwe_file>
amb siwe-submit <siwe_file> <signature>
```

3. Phone verification (first time only)
```bash
# Always check server status first
amb phone-verify-check 0x1234... +821012345678
# Only if verified: false → send OTP and confirm
amb phone-verify-start 0x1234... +821012345678
amb phone-verify-confirm 0x1234... +821012345678 123456
```

4. Readiness check — must pass before booking
```bash
amb setup-check 0x1234...
# Proceed only if ready_for_ride: true
```

5. Resolve places (for each of origin and destination):
```bash
# 5a. Search
amb place-search 0x1234... SIN "Marina Bay" --json
# 5b. Get detail for selected place (only if locationPoint is null)
amb place-detail 0x1234... SIN <place_id> --json
# 5c. ⚠️ MANDATORY: Create map session (pipe subPlaces if present)
amb map-session-create 0x1234... SIN <lat> <lng> [name]
# 5d. Poll map-session-verify until completed/cancelled/expired
amb map-session-verify <session_id> --json
```

6. Search for a ride
```bash
amb ride-search 0x1234... SG 37.5665 126.9780 37.4979 127.0276
```

7. Request a ride
- Confirm rider name and phone with the user before proceeding. Ask if not already provided.
```bash
amb ride-request '{"wallet_address":"0x1234...","search_id":"...","product_code":"STANDARD","region":"SG","pay_currency":"USDC_base_sepolia","locations":[...],"rider":{"name":"John Doe","phone":"+821012345678"}}'
```

7-1. (Optional) Cancel — always check status first
```bash
# 1. Check current ride status
amb ride-status 550e8400-e29b-41d4-a716-446655440000 0x1234...
# If driverInfo exists or status is ASSIGNED or later → warn about possible fee and confirm with user
# 2. After user confirms, execute cancellation
amb ride-cancel 550e8400-e29b-41d4-a716-446655440000 0x1234...
```

8. Payment signing
```bash
amb ride-pay-prepare 550e8400-e29b-41d4-a716-446655440000 0x1234... --json
amb wallet-sign 0x1234... eth_signTypedData_v4 '<typed_data_json>'
amb ride-pay-confirm 550e8400-e29b-41d4-a716-446655440000 0xsignature...
```

9. Start ride-relay (background)
```bash
node ${SKILL_DIR}/scripts/ride-relay.js 550e8400-e29b-41d4-a716-446655440000
```
Launch with the platform's background primitive (see SKILL.md → "Event streaming: ride-relay" for the platform spawn primitives). Stdout JSONL events: see "Stdout event schema" above. Reconnect: see "Reconnect after termination" above. Exit codes: see "Exit codes" above.

10. Cleanup — ride-relay exits on its own when a terminal `ride_event` is reached. If you need to stop it early (e.g. user cancelled and you already handled the terminal event), use the platform's kill primitive (Claude Code `TaskStop` to stop the Monitor, OpenClaw `process kill`).

11. On `FINISHED`, ride-relay prints the completion prompt with an on-demand receipt offer and, only where the region supports tipping, a tip offer. Offer a tip only if the prompt carries one — never invent the offer. It does not fetch the receipt. On an explicit request, run `amb ride-receipt <request_id>` and surface the live result verbatim. If settlement is pending, ask the user to try again shortly. Only after the user has requested and seen a canonical receipt should you check whether the wallet can still afford the next ride — see SKILL.md → "USDC bridge".

## Error Handling

When a command fails, take the following action based on the error code:

| Error code | Action |
|------------|--------|
| `WALLET_NOT_FOUND` | Run `amb wallet-setup --no-wait` |
| `JWT_NOT_FOUND` | MetaMask: follow the typed-login and exact-resume contract in [Wallet reference](wallet.md). Built-in Privy: run legacy `amb siwe-request-message` → `amb wallet-sign ... personal_sign` → `amb siwe-submit`. |
| `PHONE_NOT_VERIFIED` | Run `amb phone-verify-start` + `amb phone-verify-confirm` |
| `INSUFFICIENT_DEPOSIT` | Run `amb deposit-status` for the shortfall, then `amb deposit-add <wallet> <network> <token> <amount>`. **`deposit-add` spends Base USDC too** — if `amb wallet-balance` shows too little USDC on the payment chain and a positive USDC row on the bridge source chain, bridge first (SKILL.md → "USDC bridge"), then deposit, then request the ride. `requiredToActivate[].tokenWei` is **raw** (USDC has 6 decimals: `"4000000"` is 4.00 USDC) — convert before passing it anywhere that takes decimal, such as `bridge-usdc`. It is the amount `deposit-add` will **spend**, so the amount to *bridge* is that minus what the wallet already holds on the payment chain: `max(0, amount - payment-chain USDC)`. Note the MVL entry is a different currency — do not bridge against it. When `requiredToActivate` is `null`, do not guess an amount: report `requiredToActivateReason` instead. |
| `INSUFFICIENT_BALANCE` | Run `amb wallet-balance`. If the bridge source chain's USDC row has funds, the wallet can be topped up from Ethereum — see SKILL.md → "USDC bridge". If that chain has no rows at all, this build has no bridge and that is not the problem. Once the bridge lands, retry the payment or tip that failed. |
| `POLICY_EXCEEDED` | Stop, read `amb policy`, and name the blocking per-ride / rolling 24-hour / 7-day / 30-day limit with current cap and attempted amount (plus spent/remaining for periods). Offer one-time ride approval, a link-approved policy raise, or stop; see the [spend policy flow](spend-policy.md#basic-ride-flow). Before creation, choose before issuing the link, poll, and retry the same trip with approval_id. For a payment-stage failure on an existing request, report the remaining blocker and stop. This flow also applies when the code is nested inside a generic booking/payment error; never automatically raise limits or switch payment paths. |
| `POLICY_UNAVAILABLE` | The server could not check the spend policy. Payment is blocked; follow existing payment recovery rules. |
| `RIDE_REQUEST_FAILED` | Run both `amb deposit-status` and `amb wallet-balance` to identify the cause |
| `RIDE_CREATE_OUTCOME_UNKNOWN` | Member mode `ride-request` (v1 card flow or v2 `payment_method` flow): the create was sent but its result is unknown, so a ride may exist. Do not rebook; run the returned `inspect_command` (`amb ride-current <region>`) and track any ride it shows |
| `NETWORK_ERROR` | The gateway in `host` was unreachable or did not answer (`cause`, e.g. `ECONNREFUSED` or `TIMEOUT`). Not an expired session; do not ask the user to log in again. For read/lookup commands (search, status, place, coupon, tip-config), retry when the network recovers. On a payment (`ride-pay`), tip (`tip`) or cancel (`ride-cancel`) the server may already have processed the request — always possible when `cause` is `TIMEOUT`: re-check the ride with `amb ride-current <region>` / `amb ride-status <request_id>` before any retry, and never blind-retry |

For unknown errors in wallet mode during a crypto ride, run `amb setup-check <wallet_address>` to check crypto readiness. Never use it as general recovery for member mode or `mode: null`; inspect member authentication and the failing command instead.
