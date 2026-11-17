# Thumbtack discovery — verified recipes

Every recipe below was run live on **2026-08-10** and its output checked.
Set these first:

```sh
TT=~/.claude/skills/thumbtack/tt-extract.mjs
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
```

## Resolve a service slug

Thumbtack canonicalises loose slugs by redirect. Ask it rather than guessing:

```sh
curl -sSL -o /dev/null -A "$UA" -w '%{url_effective}\n' \
  "https://www.thumbtack.com/k/plumbing/near-me?zip_code=28203"
# https://www.thumbtack.com/k/plumbers/near-me?zip_code=28203   <- canonical slug is "plumbers"
```

Slugs are hyphenated trade names: `house-cleaning`, `plumbers`,
`electrical-work`, `interior-painting`, `lawn-mowing-and-trimming`.

## Search pros — compact list

```sh
curl -sSL -A "$UA" "https://www.thumbtack.com/k/house-cleaning/near-me?zip_code=28203" \
 | node "$TT" next \
 | jq -c '.props.pageProps.frontDoorPage.proListSection.proListResults[] | {
     name:    .businessSummaryPrefab.businessSummary.businessName,
     pk:      .servicePk,
     rating:  .businessSummaryPrefab.businessSummary.reviewSummaryPrefab.reviewSummary.averageRating.rating,
     reviews: .businessSummaryPrefab.businessSummary.reviewSummaryPrefab.reviewSummary.numReviews,
     hires:   .numHires,
     respHrs: (.rankingAverageResponseTimeInHours | if . == null then null else (.*100|round/100) end),
     online:  .businessSummaryPrefab.businessSummary.isOnline,
     url:     ("https://www.thumbtack.com" + (.url|split("?")[0]))
   }'
```

Verified output (first row):

```json
{"name":"Andreia’s Cleaning LLC","pk":"491089546672373766","rating":4.7,
 "reviews":1023,"hires":1619,"respHrs":0.08,"online":true,
 "url":"https://www.thumbtack.com/nc/charlotte/house-cleaning/andreias-cleaning-llc/service/491089546672373766"}
```

Ten results per page, no cursor. Other useful keys on the same node:
`businessFacts[].description` (e.g. `"994 similar jobs done near you"`),
`urgencySignalPills[].text` (e.g. `"In high demand"`), `priceInfo`.

### The category's filter schema

```sh
… | jq '.props.pageProps.frontDoorPage.proListSection.filterQuestions[]
        | {id, label, question, singleSelect}'
```

## Pro profile — summary (`ld+json`, simplest)

```sh
curl -sSL -A "$UA" "$PROFILE_URL" | node "$TT" ldjson | jq -c '.["@graph"][0] | {
   name, description,
   rating: (.aggregateRating.ratingValue*100|round/100),
   reviews: .aggregateRating.reviewCount,
   city: .address.addressLocality, state: .address.addressRegion,
   zip: .address.postalCode, url }'
```

`@graph[0]` is taken **positionally on purpose**: the node's `@type` is the
trade-specific schema.org subtype (`Plumber`, `Electrician`, `HousePainter`,
…), and is only literally `LocalBusiness` for some trades — a
`select(.["@type"]=="LocalBusiness")` filter silently returns nothing for most
pros.

Note `aggregateRating.ratingValue` here is the **unrounded** mean
(`4.68467583497053`) and its `reviewCount` may differ by a few from the search
page's `numReviews` — they are computed at different times.

## Pro profile — reviews

`review` is an **array of arrays**, so `flatten` first:

```sh
curl -sSL -A "$UA" "$PROFILE_URL" | node "$TT" ldjson \
 | jq -c '[.["@graph"][0].review | flatten[] | {
     stars: .reviewRating.ratingValue, by: .author.name,
     date:  .datePublished, text: .description }] | .[0:10][]'
```

## Pro profile — credentials, hours, payments (Apollo only)

These are absent from `ld+json`. Pull the section list once:

```sh
curl -sSL -A "$UA" "$PROFILE_URL" | node "$TT" apollo > apollo.json

SP='.ROOT_QUERY | to_entries | map(select(.key|startswith("servicePage")))[0].value'

# section inventory
jq -r "$SP"' .sections[].__typename' apollo.json

# background check / licenses
jq -c "$SP"' .sections[] | select(.__typename=="ServicePageCredentialsSection")
             | .inlineCredentials[] | {title, details: [.details[].segments[].text]}' apollo.json

# business hours, payment methods, "Top Pro" badge
jq -r "$SP"' .sections[] | select(.__typename=="ServicePageBusinessInfoSection")
             | .subsections[].__typename' apollo.json
# -> ServicePageBusinessFactsSubsection
#    ServicePageAvailabilityBusinessHoursSubsection
#    ServicePagePaymentMethodsSubsection
#    ServicePageTopProSubsection

# headline price
jq -c "$SP"' .actionFooterV2.priceSubsectionPrefab.servicePagePriceSubsection' apollo.json
# -> {"__typename":"ServicePagePriceSubsectionNoPrice","icon":"CONTACT","text":"Contact for price", …}
```

`priceSubsection` is a **union**. `…NoPrice` is common — always branch on
`__typename` before reading a number.

## GraphQL (advanced — only when SSR is not enough)

Useful for paging past the SSR page's 10 results / fixed review window.

```sh
curl -sS -X POST https://app.thumbtack.com/graphql -A "$UA" \
  -H 'content-type: application/json' -H 'origin: https://www.thumbtack.com' \
  -d '{"query":"query{__typename}"}'
# {"data":{"__typename":"Query"}}
```

Introspection is disabled, so recover field names from an Apollo dump.
`servicePage` needs its **whole** input object — lift it from the page:

```sh
node "$TT" apollo < profile.html \
 | jq '.ROOT_QUERY | to_entries | map(select(.key|startswith("servicePage")))[0].key' -r \
 | sed -E 's/^servicePage\((.*)\)$/\1/' > vars.json     # {"input":{…26 fields…}}

jq -c '{query:"query SP($input: ServicePageInput!){ servicePage(input:$input){ __typename shareableURL hasVerifiedPhoneNumber sections{ __typename } } }", variables: .}' vars.json > q.json

curl -sS -X POST https://app.thumbtack.com/graphql -A "$UA" \
  -H 'content-type: application/json' -H 'origin: https://www.thumbtack.com' -d @q.json
```

Verified 200. **Errors come back as HTTP 200 with an `errors[]` body** —
check `.errors` before `.data`.

## Failure modes

| Symptom | Cause |
| --- | --- |
| extractor exits `3` | wrong mode for the page — search pages have no Apollo state, profile pages have no `__NEXT_DATA__` |
| `jq` returns `null` for `servicePage` | you used a literal key; address it by `startswith` prefix |
| GraphQL `{"errors":[{"message":"badRequest"}]}` with HTTP 200 | partial input object — `servicePage` needs all 26 input fields |
| search returns a different trade than asked | your slug was redirected; read `%{url_effective}` to see the canonical one |
