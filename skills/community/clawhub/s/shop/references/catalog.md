# Additional catalog inputs

Use these fields only when the request needs them. Add them inside `catalog`; keep the outer `{catalog:...}` object. All fields below are optional. The shapes are notation, not JSON.

| Field | Shape and meaning |
|---|---|
| `context.language`, `context.intent` | Language code and buyer intent text. |
| `filters.categories` | `[taxonomy_id]`; category alternatives. |
| `filters.condition` | `["new","secondhand"]`; condition alternatives. |
| `filters.ships_from` | `[{country:"CA"}]`; origin alternatives, not delivery destinations. |
| `filters.price_tier` | Search only: `["low","medium","high"]`; category-relative tiers, not money limits. |
| `filters.rating` | Search only: `{variant:{min?,min_count?}}`; score 0 to 5 and minimum review count. |
| `filters.available` | `false` includes unavailable items; it does not select only unavailable items. |

Rating thresholds require at least one matching variant, not a product-wide average. Category, condition, origin, and price-tier lists use OR. Different filters use AND. Use known taxonomy IDs and condition values. Read messages for unsupported values. Country codes use two uppercase letters. Currency codes use three uppercase letters.

## Match a known item

Use `lookup_catalog` for public product URLs, product or variant IDs, GTINs, or UPCs, including items found elsewhere. Results need not match input count or order: correlate each returned variant's `inputs[]` with the supplied identifier, never by array position. An `exact` resolution directly identifies that variant; `featured` selects a representative, not necessarily the requested size or color. Confirm product, seller, and selected options before transferring facts between sources. Use a returned product ID for `get_product`, not the original URL or a variant ID. Skip it when search or lookup already proves the requested variant's facts.

## Price and currency

`context.currency` expresses the user's preferred currency and sets the currency of specified price limits; `min` and `max` use minor units in that currency. Catalog converts limits to apply price filters across currencies of matching offers. Returned offers keep their own price and currency.

Inspect `messages[]` for applied filters, bounds, and conversion details. In `price_filter_applied`, `data.applied_usd` gives applied bounds in USD dollars; offer `price.amount` uses minor units. If conversion was unavailable, leave cross-currency compliance unverified.

## Select options

Use `get_product` with exact option names and labels from the product:

```json
{"catalog":{"id":"gid://shopify/Product/1","selected":[{"name":"Size","label":"M"},{"name":"Color","label":"Black"}],"context":{"address_country":"CA","currency":"CAD"}}}
```

- Replace the illustrative ID with the returned product ID.
- Read the effective selection even when no warning appears; an unavailable combination can lose a requested option.
- If the user permits alternatives, add `preferences:[option_name]` to `get_product`. List option names from most to least important; relaxation starts at the end.
- Never relax a hard requirement. Search has no `preferences` field.
- Use exact-product facts for care, dimensions, compatibility, and pack size.
- Keep each rating's score, scale, count, and source together, and say whether it belongs to the product or variant.
