# Realtime Glassdoor Data — Recipes

## 1. Search for a company on Glassdoor

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-glassdoor-data/scrape.js \
  --query "Apple" --count 10 --format json
```

Returns up to 10 matching company results with IDs you can use for deeper lookups.

## 2. Get company overview/details

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-glassdoor-data/scrape.js \
  --endpoint /company-overview --company-id 1138 --format json
```

Fetches the full Glassdoor overview for Apple (company ID 1138) including ratings, CEO approval, and industry.

## 3. Scrape employee reviews

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-glassdoor-data/scrape.js \
  --endpoint /company-reviews --company-id 9079 --count 50 --sort MOST_RECENT --format csv
```

Exports up to 50 recent Amazon employee reviews as CSV with pros, cons, and ratings.

## 4. Export salary data by company

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-glassdoor-data/scrape.js \
  --endpoint /company-salaries-v2 --company-id 1138 --count 30 \
  --job-title "software engineer" --format csv
```

Fetches salary ranges for software engineers at Apple, including base pay and additional compensation.

## 5. Multi-API chain: Glassdoor + Trustpilot company comparison

```bash
# Get Glassdoor employee reviews
node --env-file=.env openwebninja_universal_scraper/apis/realtime-glassdoor-data/scrape.js \
  --endpoint /company-reviews --company-id 9079 --count 50 \
  --output output/amazon_glassdoor_reviews.json

# Get Trustpilot customer reviews for the same company
node --env-file=.env openwebninja_universal_scraper/apis/trustpilot-company-and-reviews/scrape.js \
  --endpoint /company-reviews --domain amazon.com --count 100 \
  --output output/amazon_trustpilot_reviews.json
```

Combines employee sentiment (Glassdoor) with customer sentiment (Trustpilot) for a full company reputation view.
