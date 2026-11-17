# Tock requests for fpx

All paths are relative to `https://www.exploretock.com` (subdomain `www`).
Field names, slice keys, and the GraphQL document below are transcribed
verbatim from the tock-mcp repo (`docs/TOCK-API.md`, `src/parse.ts`,
`src/graphql-ops.ts`) — not guessed.

Every SSR-page recipe follows the same shape:

```sh
fpx get '<url>' -p tock | node extract-redux-slice.mjs <sliceKey> | jq '<filter>'
```

(`extract-redux-slice.mjs` lives alongside this file — see `SKILL.md` for why
it's needed instead of piping straight to `jq`.)

---

## 1. List metros — `GET /city`

Slice: `app`. The metro directory is the largest array whose items carry
`slug` + `name` + numeric `businessCount`. Many entries have
`businessCount: 0` (inactive) — filter those out for real venues.

```sh
fpx get 'https://www.exploretock.com/city' -p tock \
  | node extract-redux-slice.mjs app \
  | jq -r '
      [.. | arrays | select(length > 0 and (.[0] | type == "object") and (.[0] | has("slug") and has("businessCount")))]
      | max_by(length)[]
      | select(.businessCount > 0)
      | "\(.slug)\t\(.businessCount)\t\(.name)"
    '
```

Fields per metro: `name`, `slug`, `state`, `country`, `businessCount`,
`isActive`, `isFeatured`, `timezone`, `currencyCode`, `lat`, `lng`, `id`.

## 2. Search a metro's restaurants — `GET /city/{slug}[?query=]`

Slice: `consumerPage`. Business listings are nested widget-tree arrays whose
items carry `domainName` + `name`; `?query=` filters server-side.

```sh
fpx get 'https://www.exploretock.com/city/chicago?query=tasting' -p tock \
  | node extract-redux-slice.mjs consumerPage \
  | jq -r '
      [.. | arrays | select(length > 0 and (.[0] | type == "object") and (.[0] | has("domainName") and has("name")))]
      | add
      | unique_by(.domainName)[]
      | "\(.domainName)\t\(.priceRange // "")\t\(.name) — \(.neighborhood // .city // "")"
    '
```

Fields per business: `domainName` (→ the venue's own page slug),
`name`, `description`, `cuisines`, `priceRange` (e.g. `"$$$$"`),
`businessType`, `city`, `state`, `country`, `neighborhood`, `webUrl`,
`timeZone`, `currencyCode`, `locale`,
`location {address city state country zipCode lat lng id}`,
`profileImageUrl`, `heroImageUrl`, `isTockUnlisted`.

A bare `/search?query=X` redirects to a detected metro — always call with an
explicit metro slug instead.

## 3. Venue detail — `GET /{slug}`

Two slices in one fetch: `app` (the venue's own business record — the item
whose `domainName === slug`) and `calendar` (its bookable offerings).

```sh
fpx get 'https://www.exploretock.com/alinea' -p tock > /tmp/tock-venue.html

node extract-redux-slice.mjs app     < /tmp/tock-venue.html > /tmp/tock-app.json
node extract-redux-slice.mjs calendar < /tmp/tock-venue.html > /tmp/tock-cal.json

jq -r '.. | objects | select(.domainName == "alinea") | "\(.name) — \(.cuisines) \(.priceRange)"' /tmp/tock-app.json

jq -r '.offerings.experience[] | "\(.id)\t\(.name)\t\(.pricePerPerson.minCents/100)-\(.pricePerPerson.maxCents/100)\t\(.partySize | join(","))"' /tmp/tock-cal.json
```

`calendar.offerings` shape (§ TOCK-API.md "Pages we fetch"):

```
offerings: {
  experience: [ { id, name, slug, shortCode, description, type,
    currencyCode, partySize:[…], pricePerPerson:{minCents,maxCents},
    ticketPriceInformation:{amountCents,priceType}, state,
    communicationPolicy:{canTransfer,cancellationPolicyText},
    eventDetails:{location:{address,city,state,zipCode,lat,lng,name}} } ],
  openDate: ["2026-07-03", …],
  openTime: ["17:00","17:15", …]
}
```

`priceType` of `PREPAID`/`DEPOSIT` means the experience needs a card at
checkout on exploretock.com — this skill cannot book it (see SKILL.md).

## 4. Date-centered availability — `GET /{slug}/search?date=YYYY-MM-DD&size=N`

Same `calendar` slice as §3, centered on `date`/`size` (party size). Tock
returns the *whole* open-date/open-time union regardless — the UI filters
client-side, so there's no per-date-only payload.

```sh
fpx get 'https://www.exploretock.com/alinea/search?date=2026-08-01&size=2' -p tock \
  | node extract-redux-slice.mjs calendar \
  | jq '{openDates: .offerings.openDate, openTimes: .offerings.openTime, experiences: [.offerings.experience[] | select(.partySize == null or (.partySize | index(2)))]}'
```

## 5. Signed-in patron's reservations — `POST /api/graphql/PatronReservationHistory`

Requires a **signed-in** tab. `selection` is a string enum:
`UPCOMING` | `PAST` | `CANCELED`.

```sh
cat > /tmp/tock-reservations.json <<'JSON'
{
  "operationName": "PatronReservationHistory",
  "variables": { "offset": 0, "limit": 30, "selection": "UPCOMING" },
  "query": "\n    query PatronReservationHistory($offset: Int!, $limit: Int!, $selection: String!) {\n  purchases(offset: $offset, limit: $limit, selection: $selection) {\n    id\n    ...ConsumerPurchaseSummary\n  }\n}\n\n    fragment ConsumerPurchaseSummary on ConsumerPurchaseSummary {\n  business {\n    domainName\n    id\n    profileImages {\n      altText\n      backingUrl\n      dominantColor\n      id\n      imageUrl\n    }\n    name\n  }\n  cancelledOrRefunded\n  city\n  country\n  dinerPatron {\n    email\n    firstName\n    lastName\n    id\n  }\n  eligibleForFeedback\n  visitFiveStarRating\n  firstTransferredTo {\n    id\n  }\n  id\n  ownerPatron {\n    email\n    firstName\n    lastName\n    id\n  }\n  ticketCount\n  ticketDateTime\n  ticketType {\n    deliveryServiceProvider\n    descriptiveVariety\n    id\n    name\n    reserveShippingTime\n    singleUnitQuantity\n    variety\n  }\n}\n"
}
JSON

fpx post-json 'https://www.exploretock.com/api/graphql/PatronReservationHistory?opname=PatronReservationHistory' \
  @/tmp/tock-reservations.json -p tock > /tmp/tock-reservations-response.json

jq -r '.data.purchases[] | "\(.ticketDateTime)\t\(.business.name)\t\(.ticketCount)ppl\t\(.ticketType.name)\(if .cancelledOrRefunded then " [CANCELLED]" else "" end)"' /tmp/tock-reservations-response.json
```

Check GraphQL-level errors first: `jq '.errors // empty' /tmp/tock-reservations-response.json` — an
auth-flavored message (matches `/auth|sign|login|unauthorized|permission/i`) means the tab
isn't signed in; re-open exploretock.com and log in, then retry.

## 6. Account identity (no standalone query)

Tock has no profile GraphQL query — the account holder's identity rides on
each purchase as `ownerPatron` (fall back to `dinerPatron`). Reuse §5's call
with `"selection": "UPCOMING"` (or `"PAST"` if there are no upcoming
reservations) and project the first entry:

```sh
jq -r '.data.purchases[0] | (.ownerPatron // .dinerPatron) | "\(.firstName) \(.lastName) <\(.email)>"' /tmp/tock-reservations-response.json
```

If there are zero purchases in both selections, Tock exposes no identity at
all for that account (this mirrors `tock_get_profile`'s behavior in the MCP).

---

## Booking / cancel — not supported

See `SKILL.md` § "Why no booking/cancel". The full reverse-engineered
protobuf protocol (lock → price → confirm → cancel) and the exact
`X-Tock-*` header gate that blocks it are documented in the tock-mcp repo's
`docs/TOCK-API.md` for the record — nothing here implements it.
