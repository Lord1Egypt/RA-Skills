# Redfin stingray endpoints for fpx

Ready-to-run requests for `fpx get '<url>' -p redfin`. All paths and
params are transcribed from the live-verified request builders in
`src/tools/*.ts` / `src/autocomplete.ts` in this repo — see the header
comment of each source file for verification dates and any known quirks.

Base origin: `https://www.redfin.com`. Every `/stingray/...` response
carries a literal `{}&&` anti-CSRF prefix — strip it before parsing:

```sh
STRIP='sed -E s/^\{\}\&\&//'
fpx get 'https://www.redfin.com/stingray/api/gis?...' -p redfin | $STRIP | jq '.payload'
```

The stripped body is `{ version, errorMessage, resultCode, payload }`;
`resultCode !== 0` means Redfin rejected the request (`errorMessage` has
why).

---

## 1. Autocomplete — resolve a location or address (do this first)

`GET /stingray/do/location-autocomplete`

Params: `location` (free text), `start=0`, `count=1` (only the first row
of each section is ever needed), `v=2`, `iss=false`, `ooa=true`,
`mrs=false`.

```sh
fpx get 'https://www.redfin.com/stingray/do/location-autocomplete?location=Brooklyn%2C%20NY&start=0&count=1&v=2&iss=false&ooa=true&mrs=false' \
  -p redfin | $STRIP \
  | jq '.payload.sections[] | {name, rows: [.rows[0]]}'
```

Response: `payload.sections[]`, each `{ name: "Places"|"Addresses"|"Schools"|"Agents"|…, rows: [...] }`.

- **Places** rows: `id` formatted `"<region_type>_<region_id>"` (e.g.
  `"6_30749"` → region_type 6, region_id 30749), `name`, `subName`, `url`.
- **Addresses** rows: no `id` — `url` is the canonical home path, e.g.
  `/NC/Lake-Lure/158-Raven-Blvd-28746/home/112653221`. Parse
  `/<STATE>/<City>/<Street>-<ZIP>(/unit-<U>)?/home/<home_id>`. A full
  street address typically returns an Addresses row instead of/alongside
  Places — that's Redfin telling you it resolved a specific home, not a
  searchable region.

```sh
# Region id for a search:
jq -r '.payload.sections[] | select(.name=="Places") | .rows[0].id'
# Home id + canonical url for an address:
jq -r '.payload.sections[] | select(.name=="Addresses") | .rows[0].url'
```

## 2. Search for-sale listings — `/stingray/api/gis`

Requires a resolved `region_id` + `region_type` from §1. Query params
(all strings/CSVs):

| param | meaning |
|---|---|
| `al=1` | always 1 |
| `num_homes` | result limit (Redfin web app default 40) |
| `region_id`, `region_type` | from autocomplete |
| `sf=1,2,3,5,6,7` | static — result fields to include |
| `start=0` | pagination offset |
| `status` | `1` = active for sale; `9` = active+coming-soon+contingent+pending (broader — what redfin-mcp uses as its default "everything for sale" view) |
| `uipt` | CSV of property-type bitmap: house=1, condo=2, townhouse=3, multi_family=4, land=5, other=6, manufactured=7, co-op=8 (omit/`1,2,3,4,5,6,7,8` for all) |
| `v=8` | static |
| `min_price`, `max_price` | optional, USD |
| `num_beds`, `num_baths` | optional, minimums |

```sh
fpx get 'https://www.redfin.com/stingray/api/gis?al=1&num_homes=40&region_id=30749&region_type=6&sf=1,2,3,5,6,7&start=0&status=9&uipt=1,2,3,4,5,6,7,8&v=8&max_price=1500000' \
  -p redfin | $STRIP \
  | jq '.payload.homes[] | {propertyId, price, streetLine, city, state, zip, beds, baths, sqFt, url}'
```

Notes:
- Redfin's gis API has an undocumented **~350-result hard cap** per call
  — if `payload.homes | length` hits ~350, more listings likely exist
  server-side (narrow with price/bed filters; there's no server-side
  pagination here).
- Redfin's gis API can silently substitute a region it *does* index for
  one it doesn't. Check `payload.serviceRegionName` against the region
  you asked for; if it names a different place (or `homes[].city/state`
  don't match the requested region), don't trust the results for
  small/rural markets — try a nearby larger city/county instead.
- `sqFt`/`price`/`lotSize`/etc. may ride as either a bare number or
  `{value: number}` — unwrap defensively.

## 3. Property detail (two round trips)

### 3a. Resolve propertyId + listingId — `/stingray/api/home/details/initialInfo`

Only needed when you have a URL, not IDs. `path` is the URL-encoded
`/<STATE>/<City>/<Street>-<ZIP>/home/<id>` path (no origin).

```sh
fpx get 'https://www.redfin.com/stingray/api/home/details/initialInfo?path=%2FNY%2FBrooklyn%2F42-Monroe-St-11238%2Fhome%2F40732555' \
  -p redfin | $STRIP | jq '.payload | {propertyId, listingId, marketId, marketName}'
```

A bare `/home/<id>` URL (no full slug) will NOT resolve here — Redfin's
own site 301s `/home/<id>` to the full slug first. If you only have a
numeric property_id, `GET /home/<id>` (no `/stingray` prefix) and read
the bridge's followed redirect target/final URL, then feed that path to
`initialInfo`.

### 3b. Detail — `/stingray/api/home/details/aboveTheFold`

Params: `propertyId`, `listingId`, `accessLevel=1`.

```sh
fpx get 'https://www.redfin.com/stingray/api/home/details/aboveTheFold?propertyId=40732555&listingId=123456789&accessLevel=1' \
  -p redfin | $STRIP \
  | jq '.payload | {
      addr: .addressSectionInfo.streetAddress,
      price: (.addressSectionInfo.latestPriceInfo.amount // .addressSectionInfo.priceInfo.amount),
      beds: .addressSectionInfo.beds, baths: .addressSectionInfo.baths,
      sqft: .addressSectionInfo.sqFt,
      remarks: .mainHouseInfo.publicRemarksParagraph,
      photo: .mediaBrowserInfo.photos[0].photoUrls.fullScreenPhotoUrl
    }'
```

`addressSectionInfo` carries price/beds/baths/sqft/status/dates;
`mainHouseInfo` carries the marketing description + HOA dues;
`mediaBrowserInfo.photos[]` carries the gallery (see §8).

### 3c. Price + tax history — `/stingray/api/home/details/belowTheFold`

Same `propertyId`/`listingId`/`accessLevel=1` params, different path:

```sh
fpx get 'https://www.redfin.com/stingray/api/home/details/belowTheFold?propertyId=40732555&listingId=123456789&accessLevel=1' \
  -p redfin | $STRIP \
  | jq '{
      price_events: [.payload.propertyHistoryInfo.events[] | {date: .eventDate, event: .eventDescription, price}],
      tax_events: [.payload.publicRecordsInfo.allTaxInfo[] | {year: .rollYear, taxesDue}],
      lot_sqft: .payload.publicRecordsInfo.basicInfo.lotSqFt
    }'
```

Field gotchas: `event.price` is a bare number (not `{amount}`); the
tax-history array is `allTaxInfo` (current-year-only is `taxInfo`); tax
records use `taxesDue`, not `taxesPaid`.

## 4. Market trends — `/stingray/api/region/<region_type>/<region_id>/<property_type>/market-trends`

`property_type`: `1`=all (default), `2`=house, `3`=condo, `4`=townhouse,
`5`=multi-family, `6`=land.

```sh
fpx get 'https://www.redfin.com/stingray/api/region/2/16163/1/market-trends' \
  -p redfin | $STRIP \
  | jq '.payload.tableData | {for_sale: .homesForSaleCurMonth, sold: .homesSoldCurMonth, homesForSale, homesSold}'
```

Each row: `label`, `currentHouseAndCondoValue` (scale depends on
`valueType`: `LONG`=count, `CURRENCY`=USD, `CURRENCY_THOUSANDS`=USD/1000,
`PERCENT`=fraction), plus `houseAndCondoYoy{Up,ValueProportionalChange}`
and the `Mom` equivalents. Neighborhood-typed regions (type 6) often
return empty tables — prefer city-level regions for this endpoint.

## 5. Comparable rentals — `/stingray/api/home/comparable-rentals`

Params: `rentEstimateLow`, `rentEstimateHigh`, `latitude`, `longitude`,
`propertyId` — the rent-estimate range and lat/lng come from the
property's own page (not derivable independently; read them off
`aboveTheFold`/the live homedetails page first).

```sh
fpx get 'https://www.redfin.com/stingray/api/home/comparable-rentals?rentEstimateLow=2200&rentEstimateHigh=2600&latitude=40.679&longitude=-73.958&propertyId=40732555' \
  -p redfin | $STRIP \
  | jq '.payload.comparableRentals[] | {streetAddress, monthlyRent: .monthlyRent.amount, beds, baths, distance: .distance.value}'
```

## 6. Address resolution notes

`/stingray/do/location-autocomplete` (§1) is also the address resolver —
there's no separate endpoint. For a fuzzy street address, retry with
common suffix swaps (Rd↔Road, Ln↔Lane, St↔Street, Ave↔Avenue, …) if the
first call's Addresses row doesn't come back, and verify the returned
street genuinely matches what you asked for (Redfin's autocomplete is
fuzzy and can return a neighboring house number).

## 7. Climate risk — HTML extraction (no JSON endpoint)

Redfin server-renders First Street Foundation climate data directly into
the homedetails page HTML — there is no stingray path for it (probed
URLs 404). `fpx get` the page itself and grep/parse the embedded blocks:

```sh
fpx get 'https://www.redfin.com/NY/Brooklyn/42-Monroe-St-11238/home/40732555' -p redfin > /tmp/page.html
grep -o '\\"floodData\\":{[^}]*}' /tmp/page.html   # also try unescaped "floodData":{...}
grep -o '\\"fireData\\":{[^}]*}'  /tmp/page.html
grep -o '\\"heatData\\":{[^}]*}'  /tmp/page.html
```

Each block is a JSON object (possibly double-escaped — un-escape `\"`→`"`
and `\\`→`\` if the naive extraction above doesn't parse). Key fields:
`floodFactor`/`fireFactor`/`heatFactor` (1–10), `femaZones[]`,
`chance[]` (30-yr flood-chance series), `lowInsurancePrice`/
`highInsurancePrice`, `cumulativeRiskYear{0,5,10,15,20}`. First Street
does **not** cover landslide risk. A shared `fsid`/census-tract value
across nearby properties usually means identical scores — cheap to
group instead of re-fetching every address in a cluster.

## 8. Photos

Already embedded in `aboveTheFold.mediaBrowserInfo.photos[]` (§3b) — no
separate endpoint. Each photo: `photoUrls.{fullScreenPhotoUrl,
nonFullScreenPhotoUrl, nonFullScreenPhotoUrlCompressed, lightboxListUrl}`,
`thumbnailData.thumbnailUrl`, `photoText` (caption).

```sh
jq '.payload.mediaBrowserInfo.photos[] | .photoUrls.fullScreenPhotoUrl'
```

For saved-home cards (§9), the homecards endpoint omits `photoUrls`
entirely — construct the CDN URL yourself from `mlsId` + `dataSourceId`:

```
https://ssl.cdn-redfin.com/photo/<dataSourceId>/bigphoto/<last3-of-mlsId-zero-padded>/<mlsId>_0.jpg
```

(index 0 → `_0.jpg`; index N>0 → `_<N>_0.jpg`; `mbphotov3/` + `genMid.`
prefix instead of `bigphoto/` for the mid-size variant.)

## 9. Saved homes / saved searches — requires a SIGNED-IN tab

These need the bridged `www.redfin.com` tab to be logged in (not just
bot-wall-cleared).

```sh
# 1. Favorited property IDs are embedded as /home/<id> links in the page HTML:
fpx get 'https://www.redfin.com/myredfin/favorites' -p redfin > /tmp/favs.html
grep -oE '/home/[0-9]+' /tmp/favs.html | grep -oE '[0-9]+' | sort -u

# 2. Fetch the home-card details for those IDs (comma-separated):
fpx get 'https://www.redfin.com/stingray/do/api/v3/favorites/homecards?b=40732555,18659204&r=' \
  -p redfin | $STRIP \
  | jq '.payload.homecards[] | {propertyId, isFavorite, addr: .commonHomeData.entireAddressString, price: .commonHomeData.priceInfo.amount}'

# Saved searches: no JSON endpoint — region URLs are regex-extracted from the page HTML.
fpx get 'https://www.redfin.com/myredfin/saved-searches' -p redfin \
  | grep -oE '"(/(city|zipcode|neighborhood|county|state)/[^"<>?#]+)"'
```

## 10. Bridge healthcheck

```sh
fpx get 'https://www.redfin.com/robots.txt' -p redfin >/dev/null && echo ok
fpx health -p redfin
```
