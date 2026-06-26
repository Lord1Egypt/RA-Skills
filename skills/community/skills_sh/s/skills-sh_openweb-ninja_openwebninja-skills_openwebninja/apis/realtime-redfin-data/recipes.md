# realtime-redfin-data Recipes

> **Location note:** `/search` and `/market-trends` take a 5-digit US zip code, a Canadian postal-code area, or a Redfin region URL — NOT a "City, State" string.

## 1. Search homes for sale in a zip code

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-redfin-data/scrape.js \
  --location "78701" --count 200 --format csv --sort newest
```

Exports up to 200 newest for-sale listings in Austin zip 78701 with price, beds, baths, and sqft to CSV.

## 2. Search condos under a price with bed/bath filters

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-redfin-data/scrape.js \
  --location "90210" --property-types "CONDO,TOWNHOUSE" --max-price 2000000 --min-beds 2 --min-baths 2 --count 100 --format csv
```

Finds up to 100 condos/townhouses in Beverly Hills (90210) under $2M with 2+ beds and 2+ baths.

## 3. Get full property details for a specific home

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-redfin-data/scrape.js \
  --endpoint /property-details --property-id 6824074 --format json
```

Fetches the full Redfin payload (price history, tax history, schools, photos, Redfin Estimate) for a property by its `property_id` (taken from a `/search` result).

## 4. Pull market trends for a region

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-redfin-data/scrape.js \
  --endpoint /market-trends --location "94103" --format json
```

Returns the latest market snapshot (median list/sale price, days on market, YoY change) plus home-price and demand time series for San Francisco zip 94103.

## 5. Map-based search by bounding box, then overlay commute data

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-redfin-data/scrape.js \
  --endpoint /search-coordinates --ne-lat 37.79 --ne-lng -122.40 --sw-lat 37.77 --sw-lng -122.43 --status for_sale --count 50 --dry-run

node --env-file=.env openwebninja_universal_scraper/apis/driving-directions/scrape.js \
  --origin "San Francisco, CA" --destination "Palo Alto, CA" --dry-run
```

Searches for-sale homes inside a San Francisco bounding box, then checks the commute from the area using the Driving Directions API.
