# Trustpilot Company & Reviews — Recipes

## 1. Search for companies by keyword

```bash
node --env-file=.env openwebninja_universal_scraper/apis/trustpilot-company-and-reviews/scrape.js \
  --query "web hosting" --count 40 --format csv
```

Exports up to 40 companies matching "web hosting" as CSV with ratings and review counts.

## 2. Get full details for a single company

```bash
node --env-file=.env openwebninja_universal_scraper/apis/trustpilot-company-and-reviews/scrape.js \
  --endpoint /company-details --domain bestbuy.com --format json
```

Returns the full Trustpilot profile for bestbuy.com including trust score, rating breakdown, and categories.

## 3. Scrape all reviews for a company

```bash
node --env-file=.env openwebninja_universal_scraper/apis/trustpilot-company-and-reviews/scrape.js \
  --endpoint /company-reviews --domain gossby.com --count 200 --format csv
```

Fetches up to 200 reviews (the max without auth cookie) for gossby.com and exports as CSV.

## 4. Filter reviews by rating and recency

```bash
node --env-file=.env openwebninja_universal_scraper/apis/trustpilot-company-and-reviews/scrape.js \
  --endpoint /company-reviews --domain amazon.com --rating 1 --sort recency \
  --date-posted last_3_months --count 100 --format json
```

Fetches recent 1-star Amazon reviews from the last 3 months, sorted newest first.

## 5. Multi-API chain: Trustpilot + Yelp side-by-side

```bash
# Get Trustpilot reviews for a business
node --env-file=.env openwebninja_universal_scraper/apis/trustpilot-company-and-reviews/scrape.js \
  --endpoint /company-reviews --domain dominos.com --count 100 \
  --output output/dominos_trustpilot.json

# Get Yelp reviews for the same business
node --env-file=.env openwebninja_universal_scraper/apis/yelp-business-data/scrape.js \
  --endpoint /business-reviews --business-id dominos-pizza-new-york --count 100 \
  --output output/dominos_yelp.json
```

Collects reviews from both platforms for cross-platform sentiment comparison.
