# Yelp Business Data — Recipes

## 1. Search for businesses by keyword and location

```bash
node --env-file=.env openwebninja_universal_scraper/apis/yelp-business-data/scrape.js \
  --query "sushi" --location "San Francisco, CA, USA" --count 50 --format csv
```

Exports up to 50 sushi restaurants in San Francisco as CSV with ratings, review counts, and addresses.

## 2. Get full details for a business

```bash
node --env-file=.env openwebninja_universal_scraper/apis/yelp-business-data/scrape.js \
  --endpoint /business-details --business-id "gary-danko-san-francisco" --format json
```

Returns the full Yelp profile for Gary Danko including hours, categories, photos, and owner info.

## 3. Scrape reviews for a business

```bash
node --env-file=.env openwebninja_universal_scraper/apis/yelp-business-data/scrape.js \
  --endpoint /business-reviews --business-id "gary-danko-san-francisco" \
  --count 60 --sort NEWEST --format csv
```

Fetches up to 60 recent reviews sorted by newest first and exports as CSV.

## 4. Search highest-rated businesses in a city

```bash
node --env-file=.env openwebninja_universal_scraper/apis/yelp-business-data/scrape.js \
  --query "coffee" --location "Portland, OR, USA" --sort-by HIGHEST_RATED \
  --count 30 --format json
```

Returns the top 30 highest-rated coffee shops in Portland.

## 5. Multi-API chain: Yelp search + Trustpilot cross-reference

```bash
# Find top pizza places on Yelp
node --env-file=.env openwebninja_universal_scraper/apis/yelp-business-data/scrape.js \
  --query "pizza" --location "New York, NY, USA" --sort-by HIGHEST_RATED \
  --count 20 --output output/nyc_pizza_yelp.json

# Cross-reference a chain on Trustpilot
node --env-file=.env openwebninja_universal_scraper/apis/trustpilot-company-and-reviews/scrape.js \
  --endpoint /company-reviews --domain dominos.com --count 100 \
  --output output/dominos_trustpilot.json
```

Finds top-rated pizza places on Yelp, then pulls Trustpilot reviews for a chain to compare local vs. national reputation.
