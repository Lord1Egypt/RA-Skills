# Query Patterns

## Planning first

Do not treat this skill as direct keyword passthrough.

Before querying, decide:

- which source is most likely correct
- which filters are actually supported
- whether the user gave enough information to justify one paid query

Language rule:

- first query with the user's original wording
- if the first query returns no result, allow one fallback retry using a closer language match for the chosen source
- do not default to immediate English translation
- do not keep retrying across many language variants

If the user intent is ambiguous and the first query would likely be low precision, ask one short clarifying question first.

## Importers

Use `importers` when the user asks for buyers, importers, or company-level lead lookup.

Helpful filters:

- `company_name`
- `country_code`
- `hs_code`
- `hs_codes`
- `date_period`
- `is_verified`

Do not use:

- `keyword`

If the user only has a product phrase such as `LED light`, do not send it directly to `importers` as `keyword`. Prefer one of:

1. convert the product phrase to HS code and search `importers`
2. search `requirements` with `keyword`
3. ask one short question if buyer intent is clear but HS code is missing and the product phrase is broad

## Exhibition

Use `exhibition` when the user asks for fair leads, exhibitors, or trade show contacts.

Helpful filters:

- `fair_name`
- `state`
- `company_name`
- `procurement_category`
- `contact_person`

## Requirements

Use `requirements` when the user asks for procurement demand or sourcing notices.

Helpful filters:

- `country`
- `purchase_title`
- `purchasing_unit`
- `keyword`
- `min_amount`
- `max_amount`
- `currency`

For `requirements`, prefer the user's original country and product wording on the first attempt when the dataset is likely to store those fields in the same language. If the first attempt returns zero results, allow one fallback retry with a closer storage-language synonym.

## Fallback pattern

If the first search returns no result:

1. remove one restrictive filter
2. keep the same source
3. retry once

If language mismatch is the most likely cause, use that one retry for a closer language match instead of random filter changes.

If still empty, switch source only if the user's goal clearly supports it.

If the initial plan itself is weak, do not spend the query immediately. Ask one short question instead.

Do not solve large result sets by paging deeply. Runtime search only exposes a shallow page window. If results are broad, narrow the filters instead of trying to enumerate the dataset.

When presenting search results back to the user:

1. say how many rows were returned in the current window
2. say whether more results may exist when `has_more = true`
3. give one concrete narrowing suggestion before suggesting another page

Preferred phrasing:

- `This query returned 10 results`
- `More matching results may be available`
- `Try adding country, HS code, or a more specific company name to narrow the next step`
