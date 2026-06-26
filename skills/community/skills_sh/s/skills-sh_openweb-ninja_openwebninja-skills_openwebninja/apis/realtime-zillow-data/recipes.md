# realtime-zillow-data Recipes

## 1. Search homes for sale in a city

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-zillow-data/scrape.js \
  --location "Austin, TX" --count 200 --format csv --sort NEWEST
```

Exports up to 200 newest listings in Austin, TX with price, beds, baths, and sqft to CSV.

## 2. Get property details and Zestimate for a specific home

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-zillow-data/scrape.js \
  --endpoint /property-details --zpid 7594920 --format json

node --env-file=.env openwebninja_universal_scraper/apis/realtime-zillow-data/scrape.js \
  --endpoint /zestimate --zpid 7594920 --format json
```

Fetches full property details and Zillow's automated valuation (Zestimate) for a property by its ZPID.

## 3. Look up a property by street address

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-zillow-data/scrape.js \
  --endpoint /property-details-address --address "1161 Natchez Dr College Station Texas 77845" --format json
```

Retrieves property details using a full street address instead of a ZPID.

## 4. Search rentals with bedroom/price filters

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-zillow-data/scrape.js \
  --location "San Francisco, CA" --home-status FOR_RENT --min-bedrooms 2 --max-price 4000 --count 100 --format csv
```

Finds up to 100 rental listings in San Francisco with 2+ bedrooms under $4,000/month.

## 5. Search by coordinates and cross-reference with local business data

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-zillow-data/scrape.js \
  --endpoint /search-coordinates --lat 34.01822 --long -118.504744 --diameter 2 --home-status FOR_SALE --count 50 --dry-run

node --env-file=.env openwebninja_universal_scraper/apis/local-business-data/scrape.js \
  --query "grocery stores near Santa Monica CA" --count 10 --dry-run
```

Searches homes for sale within 2 miles of coordinates, then finds nearby grocery stores using the Local Business Data API.
