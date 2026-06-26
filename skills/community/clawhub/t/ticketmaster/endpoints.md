# Ticketmaster Discovery Endpoints

Use the open Discovery API as the default surface.

## Core resources

| Resource | Path | Typical use |
|----------|------|-------------|
| Event search | `/events.json` | Search listings by keyword, city, country, venue, attraction, or date window |
| Event details | `/events/{id}.json` | Fetch one event by ID and inspect venues, attractions, sales windows, and links |
| Venue search | `/venues.json` | Find venues by name, city, market, or keyword |
| Venue details | `/venues/{id}.json` | Fetch venue metadata, location, address, and market links |
| Attraction search | `/attractions.json` | Find artists, teams, tours, or other attractions by keyword |
| Attraction details | `/attractions/{id}.json` | Fetch one attraction by ID |
| Classifications | `/classifications.json` | Inspect segment, genre, sub-genre, and type taxonomy |

Base URL:

```text
https://app.ticketmaster.com/discovery/v2
```

## Fields worth checking

- `name` and `type`
- `url`
- `locale`
- `dates.start`
- `sales.public.startDateTime`
- `sales.presales`
- `priceRanges`
- `_embedded.venues`
- `_embedded.attractions`
- `classifications`

## Open vs restricted surface

- Safe default: Discovery API search and lookup only
- Partner boundary: offer selection, checkout, inventory holds, and other transaction flows are not part of the open Discovery API workflow used by this skill
