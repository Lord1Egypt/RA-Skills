# Zyte API Notes for Product Extraction

Reference notes and known gotchas discovered during development and testing.
Consult this when you hit unexpected errors or need to understand a parsing
edge case.

---

## Product extraction payload

The correct payload for product extraction is minimal:

```json
{"url": "https://example.com/products/some-item", "product": true}
```

That's it. Do not add other extraction fields. The `product: true` flag
triggers Zyte's browser-based AI extraction pipeline, which renders the
page in a headless browser and uses machine learning to identify and
extract structured product data.

The product extraction pipeline manages browser rendering internally — you don't need to request it separately.

---

## Control characters in responses

Zyte API responses frequently contain control characters (form feeds `\x0c`,
vertical tabs, etc.) inside JSON string values — typically in product
descriptions scraped from pages with unusual formatting.

**Impact:** `jq` crashes with:
```
jq: parse error: Invalid string: control characters from U+0000 through
U+001F must be escaped
```

**Solution:** The `scripts/parse_product.py` script uses Python's
`json.loads(strict=False)` which handles these gracefully. This is why
we use Python for parsing instead of jq.

---

## Gzip-compressed responses

When requesting gzip compression via `Accept-Encoding: gzip`, the Zyte API
sends compressed responses. Python's `urllib.request` does NOT auto-decompress
when the header is set manually (unlike curl's `--compressed` flag).

**Solution:** The `scripts/fetch_products.py` script detects gzip responses
by checking for the magic number `\x1f\x8b` in the first two bytes, then
decompresses with `gzip.decompress()` before saving.

---

## Brand field format varies

The `.product.brand` field can appear as:
- A plain string: `"SomeBrand"`
- An object: `{"name": "SomeBrand"}`
- A category label: `"casual footwear"` (when the site doesn't properly tag brands)

The parse script handles all three cases via an `isinstance` check.

---

## mainImage field format varies

The `.product.mainImage` field can be:
- A URL string: `"https://example.com/image.jpg"`
- An object: `{"url": "https://example.com/image.jpg"}`

The parse script handles both via an `isinstance` check.

---

## additionalProperties can contain junk

Some sites have seller addresses, warehouse locations, or irrelevant metadata
extracted as `additionalProperties`. For example:

```json
{"name": "169", "value": "170, Some Street, Some City, Some State, 302019"}
```

When building the comparison table, filter out entries where:
- The `name` is purely numeric
- The `value` looks like a physical address (contains words like "Road",
  "Colony", "Street", or postal code patterns)
- The `name` is generic metadata (e.g. "net quantity", "item count",
  "asin", "upc", "global trade identification number")

Focus on entries with meaningful spec data like "material", "weight",
"sole material", "dimensions", "color", etc.

---

## Pricing quirks

- Prices are returned as strings: `"2999.0"`, `"16.99"` — parse to float.
- `regularPrice` is the pre-discount price. If it differs from `price`,
  the product is on sale.
- Some sites embed pricing info in `additionalProperties` too (e.g.
  `"mrp": "₹5999 40% Off"`). Cross-reference with the top-level `price`
  and `regularPrice` fields for accuracy.
- Currency is usually consistent within a country, but always verify —
  don't assume all products share the same currency.

---

## Localized content

Amazon and other sites may return product data in the local language of
their regional domain. For example, Amazon India (amazon.in) often returns
features and specs in Hindi. The brand name, model number, and numeric
fields (price, rating, weight) are usually still readable, but descriptive
text may need translation context.

---

## Rate limits and parallelism

Zyte API rate limits are **RPM-based** (requests per minute), **not
concurrency-based**. The default limit is 1,400 RPM for all API keys.
There is no hard cap on concurrent requests.

**What this means for product comparison:**

For a typical comparison of 2–20 URLs, firing them all in parallel is
safe. Even 20 concurrent product extractions is a tiny fraction of
1,400 RPM. The `fetch_products.py` script caps concurrency at 5 workers
by default — not because Zyte requires it, but to be conservative with
target domain load.

**Optimal parallelism formula (from Zyte docs):**

```
parallel_requests = ceil(RPM_limit / 60 × avg_response_time_seconds)
```

For 1,400 RPM with ~20s product extraction: `ceil(1400/60 × 20) = 467`.
Product comparisons will never come close to this.

**HTTP 429 behavior:**

- `/limits/over-domain-limit` — too many requests to the same target site.
- `/limits/over-org-domain-limit` — org-wide limit for a domain.
- You are NOT charged for 429 responses.
- The fetch script auto-retries with exponential backoff (2s, 4s, 8s).
