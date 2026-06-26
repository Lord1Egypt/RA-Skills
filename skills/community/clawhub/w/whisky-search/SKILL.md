---
name: whisky-search
description: >-
  Search and retrieve whisky information from WhiskySpace. Use this skill when
  users ask about whisky bottles, brands, distilleries, prices, ratings,
  regions, cask types, filters, recommendations, or WhiskySpace page
  links/URLs/addresses for whisky or brand pages. Trigger for requests like
  "find a whisky", "tell me about Macallan", "show me Islay whiskies", "what's
  the price of", "compare these whiskies", "give me the details page URL",
  "give me the brand page URL", or "where did this link come from". Supports 8
  languages: English, Chinese (zh), Japanese (ja), Spanish, French, German,
  Korean, Portuguese.
---

# Whisky Search

Use WhiskySpace API responses as the source of truth. Prefer short, factual answers built from returned fields.

## Non-negotiable rules

- Use only API-returned data plus the canonical website URL rules in this skill.
- Do not infer site routes, official websites, histories, tasting notes, prices, or descriptions from naming patterns.
- If a required field is missing, say it is unavailable or not provided. Do not guess.
- Distinguish clearly between a WhiskySpace page URL and a brand's official website.
- If the user asks for a WhiskySpace link, return the page URL. If the user asks for the official website, use only the API `website` field.
- If the user asks where a URL came from, explain that it uses the canonical route in this skill plus the identifier returned by the API.
- Never describe a canonical URL as guessed, inferred, predicted, or assumed.

## Canonical website URL rules

- Whisky detail page: `https://www.whiskyspace.com/whiskies/{slug_or_id}`
- Brand page: `https://www.whiskyspace.com/brand/{id}`
- If the API response includes a full website URL field for the requested WhiskySpace page, use that exact value.
- Otherwise, whisky pages use the returned `slug`; if `slug` is missing, use the numeric ID.
- Brand pages use the numeric `id` only. Never use `slug` to build a brand page URL.
- Never output `/brand/{slug}`, `/brands/{slug}`, or any undeclared route.
- If the user asks for a brand page URL and the current payload has only `slug`, call `GET https://www.whiskyspace.com/api/brands/{slug}` first and then use the returned numeric `id`.
- If the required identifier is still missing after the relevant lookup, say the WhiskySpace page URL is unavailable.

## Request routing

1. Search, compare, recommend, or filter whiskies:
   Use `GET https://www.whiskyspace.com/api/search`.
2. Show one whisky's details:
   Use `GET https://www.whiskyspace.com/api/whiskies/{slug_or_id}`.
3. List brands:
   Use `GET https://www.whiskyspace.com/api/brands`.
4. Show one brand's details:
   Use `GET https://www.whiskyspace.com/api/brands/{identifier}`.
5. Show filter choices:
   Use `GET https://www.whiskyspace.com/api/search/filters`.
6. User asks only for a page address, link, or URL:
   Fetch only what is needed to obtain the canonical identifier, then return the URL directly.
7. User asks where a URL came from:
   Answer with the canonical route plus the API identifier used. Keep it to one or two sentences.

## API endpoints

### Search whiskies

```text
GET https://www.whiskyspace.com/api/search
```

Common parameters:
- `q`
- `region`, `country`, `type`, `cask_type`
- `min_age`, `max_age`
- `min_abv`, `max_abv`
- `min_rating`, `max_rating`
- `sort=rating|name|age|price|newest`
- `per_page` (max 50)

### Get whisky details

```text
GET https://www.whiskyspace.com/api/whiskies/{slug_or_id}
```

### List brands

```text
GET https://www.whiskyspace.com/api/brands
```

Common parameters:
- `country`
- `region`
- `sort=name|founded_year|whisky_count`
- `per_page`

### Get brand details

```text
GET https://www.whiskyspace.com/api/brands/{identifier}
```

`identifier` can be a slug or numeric ID for the API request. Use the returned numeric `id` for the website brand page URL.

### Get filter options

```text
GET https://www.whiskyspace.com/api/search/filters
```

## Output templates

### Search results

Show the top 5 to 10 matches unless the user asks for more.

For each whisky include:
- Name
- Age if present
- Volume and ABV if present
- Rating and review count if present
- Brand, region, country if present
- Price with recorded date if present
- Cask types if present
- WhiskySpace link: `https://www.whiskyspace.com/whiskies/{slug_or_id}`

When there are many matches, say: `Found N results, showing top M`.

### Whisky details

Include:
- Name, brand, category
- Age, ABV, volume
- Rating and review count
- Description if present
- Cask types
- Prices with currency, market, and recorded date
- WhiskySpace page URL

### Brand list

For each brand include:
- Name
- Founded year if present
- Region and country if present
- Whisky count if present
- WhiskySpace brand page URL: `https://www.whiskyspace.com/brand/{id}`

### Brand details

Include:
- Name
- Description or history if present
- Region and country
- Founded year if present
- Official website only if the API returns `website`
- WhiskySpace brand page URL: `https://www.whiskyspace.com/brand/{id}`

### Link-only response

When the user asks only for an address, link, or URL, keep the answer minimal.

Example:

```text
White Horse brand page:
https://www.whiskyspace.com/brand/492
```

Do not add extra tasting notes, history, or route speculation.

### URL provenance response

When the user asks where the URL came from, use this pattern:

```text
It uses the canonical WhiskySpace brand route `/brand/{id}` defined in this skill and the API-returned brand id `492`. I did not use the slug to build the page URL.
```

Adapt the route and identifier to the actual case.

## Anti-patterns

Never do any of the following:

- `The brand page should be /brand/{slug}.`
- `I inferred that URL from the site's naming pattern.`
- `The official website is https://www.whiskyspace.com/brand/492.`
- `The brand URL is unavailable, but it is probably https://www.whiskyspace.com/brand/white-horse.`

## Edge cases

### No results

- Say no matching results were found.
- Suggest a broader search term or a different filter.

### Missing fields

- Use `Not available` or `Not provided`.
- Do not omit an important field if the user explicitly asked for it.

### URL request with incomplete brand data

- If you have `brand.slug` but not `brand.id`, call the brand details endpoint first.
- If you still do not get a numeric `id`, say the WhiskySpace brand page URL is unavailable.

### API error or timeout

- Explain the failure plainly.
- Suggest retrying or simplifying the query.
- Do not dump raw error output unless the user asks for it.

### Large result sets

- Show the top 10 by default.
- Mention the total count when available.
- Suggest filters such as region, age, price, or rating.

## Minimal examples

Search:

```bash
curl -s "https://www.whiskyspace.com/api/search?q=Macallan&per_page=5" -H "Accept: application/json"
```

Whisky details:

```bash
curl -s "https://www.whiskyspace.com/api/whiskies/macallan-12-year-old" -H "Accept: application/json"
```

Brand details by slug to retrieve numeric ID:

```bash
curl -s "https://www.whiskyspace.com/api/brands/white-horse" -H "Accept: application/json"
```

## Notes

- Prices may be stale. Show the recorded date when available.
- Ratings based on few reviews may be less reliable.
- No API key is required for the documented endpoints.
