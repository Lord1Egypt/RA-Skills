# Filters and Pagination

## High-value filters

| Parameter | Use it for | Notes |
|-----------|------------|-------|
| `keyword` | Free-text search | Best first filter for artist, team, tour, or event name |
| `city` | Local search | Reduces noisy multi-market results fast |
| `countryCode` | Country scoping | Useful baseline filter for broad keywords |
| `locale` | Localized responses | Try `*` when localized naming gets in the way |
| `marketId` | Ticketmaster market scoping | Good when a city spans multiple operational markets |
| `dmaId` | US media markets | Useful when the docs or existing queries already use DMA |
| `venueId` | Venue-specific listings | Best for recurring venue watches |
| `attractionId` | Artist/team-specific listings | Best after one attraction lookup |
| `classificationName` | Segment or genre | Useful for music, sports, arts, and theater narrowing |
| `startDateTime` | Start window lower bound | Use UTC ISO-8601 |
| `endDateTime` | Start window upper bound | Use UTC ISO-8601 |
| `onsaleStartDateTime` | Onsale window lower bound | Useful for release monitoring |
| `sort` | Result ordering | Keep the chosen sort in memory if it becomes stable |
| `size` | Page size | Prefer small sizes during exploration |
| `page` | Page index | Use only after narrowing filters |

## Paging rules

- Keep `size * page < 1000` to stay inside the documented deep-paging boundary.
- When a query is too broad, add filters instead of increasing `page`.
- Save IDs from strong matches and switch to detail endpoints as soon as possible.

## Practical sort choices

- `date,asc` when the user wants upcoming events
- `date,desc` when auditing past or recently announced results
- Keep sort explicit in repeatable scripts so the result order does not surprise you later
