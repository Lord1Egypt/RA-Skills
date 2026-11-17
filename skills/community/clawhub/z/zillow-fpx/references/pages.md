# Zillow pages for fpx

All paths below are fetched with `fpx get 'https://www.zillow.com<path>' -p zillow`.
Every page is server-rendered Next.js — the data lives in
`__NEXT_DATA__.props.pageProps`, never in a separate JSON API. Field
paths below are transcribed from the MCP's parsers
(`src/next-data.ts`, `src/tools/*.ts`) — live-verified there, not
re-captured here.

## 0. The extractor (reuse for every page below)

```sh
extract_page_props() {
  python3 -c '
import re, sys, json
html = sys.stdin.read()
m = re.search(r"<script[^>]*id=[\"\x27]__NEXT_DATA__[\"\x27][^>]*>(.*?)</script>", html, re.S | re.I)
if not m:
    sys.exit("no __NEXT_DATA__ script tag found — likely a bot-wall or redirect page")
print(json.dumps(json.loads(m.group(1))["props"]["pageProps"]))
'
}

fpx get 'https://www.zillow.com/robots.txt' -p zillow  # smoke test, no parsing needed
```

Pipe any fetched HTML through `extract_page_props` to get the page's
`pageProps` as one JSON line, then `jq` into it per the recipes below.

## 1. Search listings

Two-step dance — **always resolve before filtering**:

**Step 1 — resolve** (bare slug, no query string):

```sh
fpx get 'https://www.zillow.com/homes/Brooklyn%2C%20NY_rb/' -p zillow \
  | extract_page_props > /tmp/pp.json
jq '.searchPageState.queryState.regionSelection, .searchPageState.queryState.mapBounds' /tmp/pp.json
```

- If `searchPageState` is present with a non-empty `regionSelection` +
  `mapBounds` → you have a **region**; proceed to step 2.
- If `searchPageState` is **absent** but `pageProps.gdpClientCache` (or
  `pageProps.componentProps.gdpClientCache`) is present, Zillow resolved
  the query straight to ONE property (a homedetails page) — see §2, no
  step 2 needed.
- If `searchPageState.queryState.regionSelection` is empty AND
  `cat1.searchResults.listResults` is non-empty, Zillow returned
  address/street-level listings directly with no region to pin — use
  those listings as-is (issue #31 in the MCP).

**Step 2 — filtered search** (region pinned + your filters), only when
step 1 gave you a region:

```sh
SQS='{"usersSearchTerm":"Brooklyn, NY","filterState":{"price":{"max":900000},"beds":{"min":2}},"isListVisible":true,"isMapVisible":false,"regionSelection":[{"regionId":37607,"regionType":17}],"mapBounds":{"north":40.74,"south":40.57,"east":-73.83,"west":-74.05}}'
ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$SQS")
fpx get "https://www.zillow.com/homes/Brooklyn%2C%20NY_rb/?searchQueryState=${ENC}" -p zillow \
  | extract_page_props | jq '.searchPageState.cat1.searchResults.listResults[] | {zpid: .hdpData.homeInfo.zpid, price: .hdpData.homeInfo.price, address: .hdpData.homeInfo.streetAddress, beds: .hdpData.homeInfo.bedrooms, url: .detailUrl}'
```

`filterState` keys the MCP sets (mirror these in the JSON above):
`isForRent`/`isForSaleByAgent`/etc `{value: true|false}` (status
switches), `price {min,max}`, `beds {min}`, `baths {min}`, one
`{value:true}` flag per home type (`isSingleFamily`, `isCondo`,
`isTownhouse`, `isMultiFamily`, `isManufactured`, `isLotLand`,
`isApartment`), and `pagination: {currentPage: N}` for page > 1. Zillow
returns ~40 listings per page; increment `pagination.currentPage` and
re-fetch to walk further pages (stop on an empty `listResults`).

Pagination example (page 2):

```sh
SQS='{...same as above..., "pagination":{"currentPage":2}}'
```

## 2. Property detail by zpid

```sh
fpx get 'https://www.zillow.com/homedetails/12345_zpid/' -p zillow \
  | extract_page_props > /tmp/pp.json
# gdpClientCache is a JSON-encoded STRING inside pageProps — parse twice.
jq -r '.gdpClientCache // .componentProps.gdpClientCache' /tmp/pp.json \
  | jq '[to_entries[] | select(.key | startswith("Property:")) | select(.value.property) | .value.property][0]
        // [to_entries[] | select(.value.property) | .value.property][0]'
```

That gives the raw `property` object. Useful top-level fields: `zpid`,
`hdpUrl`, `address {streetAddress,city,state,zipcode,neighborhood}`,
`mlsStreetAddress` (canonical MLS address — may disagree with `address`,
prefer it when present), `price`, `zestimate`, `rentZestimate`,
`bedrooms`, `bathrooms`, `livingArea`, `lotSize` (sqft), `yearBuilt`,
`homeType`, `homeStatus`, `description`, `latitude`/`longitude`,
`daysOnZillow`, `taxAssessedValue`/`taxAssessedYear`,
`taxAnnualAmount` (values < 10 are a not-yet-assessed sentinel, not a
real bill), `schools[]`, `resoFacts {yearBuilt, associationFee,
associationFeeFrequency, taxAnnualAmount}` (MLS fallback source),
`priceHistory[]`, `taxHistory[]`.

Only a URL with a trailing `<zpid>_zpid/` resolves — a slug-only URL
redirects to the generic search page (no `gdpClientCache`). If you only
have an address, resolve to a zpid via §1 or the autocomplete call in §7
first.

## 3. Price / tax history (same property object as §2)

```sh
jq '.priceHistory' /tmp/property.json    # [{date, price, event, source, ...}]
jq '.taxHistory' /tmp/property.json      # [{time or year, value, taxIncreaseRate, ...}]
```

Both arrays live inline on the property object fetched in §2 — no
separate request. Absent on some (commonly non-Showcase) listings —
Zillow renders the trend client-side for those.

## 4. Zestimate history (same property object as §2)

```sh
jq '(first(.homeValueChartData[] | select(.name=="This home")) // .homeValueChartData[0]) | .points' /tmp/property.json
```

Each point is `{x: <unix ms>, y: <value>}` or `{date, value}` depending
on deploy. Fall back to deriving a series from `priceHistory[].{date,price}`
when `homeValueChartData` is absent. `rentValueChartData` is the parallel
series for `rent` when present.

## 5. Photos (same property object as §2)

```sh
jq '[.photos, .responsivePhotos, .originalPhotos] | map(select(type=="array" and length>0)) | first // []' /tmp/property.json
```

Each entry: `{caption, subjectType, url, mixedSources: {jpeg: [{url,width}], webp: [{url,width}]}}`.
Pick the widest `mixedSources.jpeg`/`webp` entry for the largest image;
`url` alone is the hero/thumbnail. `streetViewImageUrl` and
`hiResImageLink` sit at the top level of the property object too.

## 6. Saved searches / saved homes (requires a signed-in tab)

```sh
# Saved searches — path is case-sensitive (capital S)
fpx get 'https://www.zillow.com/myzillow/SavedSearches' -p zillow \
  | extract_page_props | jq '.savedSearches // .userSavedSearches'

# Saved (favorited) homes — flattened across collections
fpx get 'https://www.zillow.com/myzillow/favorites' -p zillow \
  | extract_page_props | jq '[.collectionsResponse[] | (.homes // .properties // .items // [])[]]'
```

A signed-out tab redirects to `/user/login` instead of rendering these —
check the fetched HTML's final URL / body before trusting an empty
result as "no saves."

## 7. Market report for a region

```sh
fpx get 'https://www.zillow.com/home-values/6181/brooklyn-ny/' -p zillow \
  | extract_page_props > /tmp/pp.json
jq '{region: .zhviRegion, analytics: .odpMarketAnalytics}' /tmp/pp.json
```

`zhviRegion {name, regionTypeName, parentCounty.name, parentState.name}`;
`odpMarketAnalytics.mrktListingLatest {newListings, forSaleInventory,
medianListPrice, medianDaysOnMarket}`; `.mrktSaleLatest
{medianSalePrice, daysToPending}`; `.zhviLatest {zhvi, zhviYoY,
asOfDate}` (`zhviYoY` is a fraction — multiply by 100 for a percent).
The region id/slug (e.g. `6181/brooklyn-ny`) comes from a Zillow
home-values URL; there's no separate region-lookup endpoint documented
in the MCP.

## 8. Address autocomplete (bonus — resolving a free-text address to a zpid)

Zillow's own address typeahead, used internally by the MCP's
`zillow_get_by_address` resolver ladder before it falls back to §1's
search. Inline GraphQL (no persisted-query hash), POST:

```sh
cat > /tmp/ac.json <<'JSON'
{
  "operationName": "GetAutocompleteResults",
  "query": "query GetAutocompleteResults($query: String!, $queryOptions: SearchAssistanceQueryOptions, $resultType: [SearchAssistanceResultType], $shouldRequestSpellCorrectedMetadata: Boolean = false) { searchAssistanceResult: zgsAutocompleteRequest(query: $query, queryOptions: $queryOptions, resultType: $resultType, shouldRequestSpellCorrectedMetadata: $shouldRequestSpellCorrectedMetadata) { requestId results { __typename ... on SearchAssistanceAddressResult { id } } } }",
  "variables": { "query": "3538 Trent St Charlotte NC", "resultType": ["REGIONS","FORSALE","RENTALS","SOLD","COMMUNITIES","SCHOOLS","SCHOOL_DISTRICTS","SEMANTIC_REGIONS","BUILDER_COMMUNITIES"], "shouldRequestSpellCorrectedMetadata": false },
  "resultType": ["REGIONS","FORSALE","RENTALS","SOLD","COMMUNITIES","SCHOOLS","SCHOOL_DISTRICTS","SEMANTIC_REGIONS","BUILDER_COMMUNITIES"],
  "shouldRequestSpellCorrectedMetadata": false
}
JSON
QS='query=3538%20Trent%20St%20Charlotte%20NC&resultType=REGIONS&resultType=FORSALE&resultType=RENTALS&resultType=SOLD&resultType=COMMUNITIES&resultType=SCHOOLS&resultType=SCHOOL_DISTRICTS&resultType=SEMANTIC_REGIONS&resultType=BUILDER_COMMUNITIES&shouldRequestSpellCorrectedMetadata=false&operationName=GetAutocompleteResults'
fpx post-json "https://www.zillow.com/zg-graph?${QS}" @/tmp/ac.json -p zillow \
  -H 'origin: https://www.zillow.com' \
  -H 'referer: https://www.zillow.com/homes/for_sale/' \
  -H 'x-caller-id: static-search-page-graphql' \
  | jq -r '.data.searchAssistanceResult.results[] | select(.__typename=="SearchAssistanceAddressResult") | .id'
```

Each result `.id` is a full canonical address string (e.g.
`"3538 Trent St Charlotte, NC 28209"`) — feed that string into §1's
resolve step (`/homes/<that-string>_rb/`) to get the zpid. These three
headers are cookie-free by design — the bridge supplies the session
ambiently; don't add a `Cookie` header yourself.

## 9. Healthcheck

```sh
fpx get 'https://www.zillow.com/robots.txt' -p zillow
```

A 200 with plain-text `robots.txt` content confirms the bridge, the
extension, and a responsive zillow.com tab — the same probe
`zillow_healthcheck` runs.
