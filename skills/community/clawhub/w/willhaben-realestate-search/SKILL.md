---
name: willhaben-realestate-search
description: Search willhaben.at real estate listings (apartments, houses) via their public webapi. No browser needed. Search any Austrian state and district with price/room filters. Get full listing details including heating type, building condition, energy class (HWB/fGEE), parking, and floor. Use for Austrian property searches, willhaben real estate queries, or building property reports. Triggers on "willhaben", "Austrian real estate", "Eigentumswohnung", "Haus kaufen Österreich", property search Austria.
metadata: {"openclaw":{"emoji":"🏠","requires":{"bins":["python3"]}}}
---

# Willhaben Real Estate Search

Search and retrieve property listings from willhaben.at using their public webapi. No browser automation needed.

## Prerequisites

Requires `python3` with the `requests` library (pre-installed in most environments).

## Quick Start

### Search listings

```bash
# Apartments for sale in Schärding, max €300k
python3 scripts/willhaben-search.py --district schaerding --type apartment --max-price 300000

# Houses in Wels, max €350k
python3 scripts/willhaben-search.py --district wels --type house --max-price 350000

# With room filter and JSON output
python3 scripts/willhaben-search.py --district linz --type apartment --max-price 300000 --min-rooms 2 --format json

# With full details (heating, energy, condition) for each listing
python3 scripts/willhaben-search.py --district schaerding --type apartment --max-price 300000 --with-details
```

### Get detail for a specific listing

```bash
python3 scripts/willhaben-search.py --detail 1148259428
python3 scripts/willhaben-search.py --detail 1148259428 --format json
```

Detail fields include:
- **HEATING** (heating type): Fernwärme, Fußbodenheizung, Zentralheizung, Gasheizung, etc.
- **BUILDING_CONDITION**: Erstbezug, Sehr gut/gut, Renoviert, Renovierungsbedürftig
- **YEAR_OF_BUILDING**: Construction year
- **ENERGY_HWB** + **ENERGY_HWB_CLASS**: Energy rating (kWh/m²a) + class (A-G)
- **ENERGY_FGEE** + **ENERGY_FGEE_CLASS**: Overall energy efficiency factor
- **Parking**: Extracted from listing body text (garage, stellplatz, carport, tiefgarage)

## Property Types

| CLI Type | Willhaben Category |
|----------|-------------------|
| `apartment` | Eigentumswohnung (buy) |
| `house` | Haus kaufen |

## District Slugs

Districts use willhaben's URL slug format — the slug is taken directly from the willhaben URL path. Browse `willhaben.at/iad/immobilien/` to discover slugs for any district.

Examples:

| District | Slug |
|----------|------|
| Schärding | `schaerding` |
| Ried im Innkreis | `ried-im-innkreis` |
| Wels (Stadt) | `wels` |
| Linz (Stadt) | `linz` |
| Linz-Land | `linz-land` |
| Braunau am Inn | `braunau-am-inn` |
| Wien | `wien` |
| Graz | `graz` |
| Salzburg | `salzburg-stadt` |
| Innsbruck | `innsbruck` |
| Klagenfurt | `klagenfurt` |

Any valid willhaben district slug works — these are just examples.

## States

Default state is `oberoesterreich`. Override with `--state`:

```bash
python3 scripts/willhaben-search.py --state salzburg --district salzburg-stadt --type apartment
```

Available: `oberoesterreich`, `niederoesterreich`, `wien`, `salzburg`, `steiermark`, `kaernten`, `tirol`, `vorarlberg`, `burgenland`

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--district` | District URL slug (required for search) |
| `--state` | Austrian state (default: `oberoesterreich`) |
| `--type` | Property type: `apartment` or `house` |
| `--max-price` | Maximum price in EUR |
| `--min-rooms` | Minimum number of rooms |
| `--max-pages` | Max result pages (default: 5) |
| `--with-details` | Fetch heating/energy/condition for each listing |
| `--detail` | Get full details for a specific listing ID |
| `--format` | `text` or `json` |

## API Details

Uses willhaben's public webapi:
- Search: `GET https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/{type}/{state}/{district}`
- Detail: `GET https://www.willhaben.at/webapi/iad/atverz/{ad_id}`

No authentication needed. Be respectful with request rates — add delays between detail requests (~200-300ms).

## Notes

- Listing URLs follow pattern: `https://www.willhaben.at/iad/{SEO_URL}`
- Search returns: id, title, price, rooms, area, location, district, postcode, published date
- Detail adds: heating, building condition, year built, HWB/fGEE energy ratings, parking
- Parking is extracted from the listing body text when not in structured fields
