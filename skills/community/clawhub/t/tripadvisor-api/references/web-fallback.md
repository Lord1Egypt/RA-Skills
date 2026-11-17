# Web fallback: location detail via fpx (no API key)

Covers `ta_web_get_location` (`tripadvisor-mcp`'s `src/tools/web.ts` +
`src/web/parse.ts`) — the one solid endpoint on the consumer site, reached
with **no Terra key** by routing through your own signed-in browser tab.
Shapes captured live 2026-07-04; re-verify if parsing drifts (see
`docs/TRIPADVISOR-WEB-API.md` in the repo for the full recon).

Setup (once): see `../SKILL.md`'s "Fallback tier" section
(`fpx profile add tripadvisor --domain tripadvisor.com` + `fpx pair -p tripadvisor`).

## Canonical URL — works for every category

TripAdvisor canonicalizes on the `d<id>` segment; the `g<geo>` and the
`_Review` type prefix are corrected by a same-origin redirect that the
in-tab fetch follows. **One fixed URL form works whether the id is an
attraction, hotel, or restaurant** — no need to know the category up front:

```
https://www.tripadvisor.com/Attraction_Review-g1-d<locationId>-Reviews-a-a.html
```

## Fetch + parse

```sh
LOCATION_ID=104675
fpx get "https://www.tripadvisor.com/Attraction_Review-g1-d${LOCATION_ID}-Reviews-a-a.html" \
  -p tripadvisor > /tmp/ta-location.html

# The page embeds 3 application/ld+json blocks; the business node is the
# one with BOTH `name` and `aggregateRating` (its @type varies by category:
# LocalBusiness=attraction, LodgingBusiness=hotel, FoodEstablishment=restaurant).
python3 - /tmp/ta-location.html <<'PY'
import re, json, sys
html = open(sys.argv[1]).read()
for m in re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S | re.I):
    try:
        obj = json.loads(m.strip())
    except Exception:
        continue
    if isinstance(obj, dict) and 'name' in obj and 'aggregateRating' in obj:
        print(json.dumps(obj))
        break
PY
```

Pipe that single-line JSON into `jq` for a slim projection matching what
`ta_web_get_location` returns:

```sh
... | jq '{
  name, type: .["@type"], url,
  rating: (.aggregateRating.ratingValue | tonumber),
  review_count: .aggregateRating.reviewCount,
  best_rating: .aggregateRating.bestRating,
  telephone, image,
  latitude: .geo.latitude, longitude: .geo.longitude,
  same_as: .sameAs, address
}'
```

Example fields (attraction, `d104675`):

```jsonc
{
  "@type": "LocalBusiness",
  "name": "Golden Gate Bridge",
  "url": "https://www.tripadvisor.com/Attraction_Review-g60713-d104675-...html",
  "address": {"addressLocality": "San Francisco", "addressRegion": "California", "addressCountry": "US", "postalCode": "94129"},
  "aggregateRating": {"ratingValue": "4.7", "reviewCount": 49969, "bestRating": 5},
  "image": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/.../golden-gate-bridge.jpg?...",
  "telephone": "+1 415-921-5858",
  "geo": {"latitude": 37.820026, "longitude": -122.47859},
  "sameAs": "https://www.goldengate.org/"
}
```

## Limits

- No key-free search/typeahead endpoint exists — every plausible one
  (`/TypeAheadJson`, `/data/1.0/typeahead`, `/api/internal/1.14/typeahead`,
  `/Search?q=`) is a dead end (empty body, 404, needs auth, or a hydrated
  SPA shell with no SSR data). **Resolve a `locationId` via the Terra
  `GET /locations/search` endpoint** (`references/terra-endpoints.md` §1),
  or take it from a TripAdvisor URL, then use this fallback for detail.
- Individual review **text** is not in the ld+json (no `Review` schema
  block, no Apollo/redux store) — only the aggregate rating/count. Use the
  Terra `GET /locations/{id}/reviews` endpoint for review text.
- If the fetched body isn't valid HTML with an ld+json block (a
  bot-challenge interstitial slipped through), re-open/refresh the
  `www.tripadvisor.com` tab and retry.
