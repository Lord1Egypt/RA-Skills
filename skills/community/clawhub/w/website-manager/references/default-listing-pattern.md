# Default Listing Pattern

Use this as the default for blog, resources, services, directories, and any Notion-backed collection.

## Layout

1. intro block with title and short description
2. featured items row if at least one item is featured
3. category chip bar
4. search input
5. result count and reset control
6. responsive card grid
7. pagination

## Interaction defaults

- items per page: `9`
- category filter: single-select by default
- tag filter: optional and hidden unless the collection is complex enough to justify it
- search fields: title, summary/excerpt, category, tags
- URL params:
  - `category`
  - `q`
  - `page`

## Required states

- loading state
- empty collection state
- no-results state
- invalid page fallback

## Card fields

Every card should have:
- title
- summary
- category
- image or visual fallback
- date when relevant
- primary CTA or link target

## Mobile rules

- chips must wrap cleanly
- search stays visible near the top
- pagination controls remain tap-friendly
- card grids collapse to one column when needed
