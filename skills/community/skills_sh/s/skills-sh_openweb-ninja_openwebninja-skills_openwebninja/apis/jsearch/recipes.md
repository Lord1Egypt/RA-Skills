# jsearch Recipes

## 1. Search remote React developer jobs

```bash
node --env-file=.env openwebninja_universal_scraper/apis/jsearch/scrape.js \
  --query "react developer" --remote --count 50 --format csv
```

Exports up to 50 remote React developer job listings as CSV with titles, companies, salary ranges, and apply links.

## 2. Get salary estimates for a role in a city

```bash
node --env-file=.env openwebninja_universal_scraper/apis/jsearch/scrape.js \
  --endpoint /estimated-salary --query "data engineer" --location "san francisco" --format json
```

Returns min/median/max salary data for "data engineer" positions in San Francisco.

## 3. Search full-time jobs posted this week

```bash
node --env-file=.env openwebninja_universal_scraper/apis/jsearch/scrape.js \
  --query "product manager jobs in NYC" --employment-type FULLTIME --date-posted week --count 30
```

Finds up to 30 full-time product manager jobs in NYC posted in the last 7 days.

## 4. Dry-run to preview results before a large pull

```bash
node --env-file=.env openwebninja_universal_scraper/apis/jsearch/scrape.js \
  --query "machine learning engineer" --count 100 --dry-run
```

Fetches only the first page (10 results) and prints them to console without writing a file.

## 5. Chain: find jobs then get salary benchmarks

```bash
# Step 1 — search for jobs and save JSON
node --env-file=.env openwebninja_universal_scraper/apis/jsearch/scrape.js \
  --query "backend engineer" --count 20 --format json --output output/backend_jobs.json

# Step 2 — get salary estimate for the same role
node --env-file=.env openwebninja_universal_scraper/apis/jsearch/scrape.js \
  --endpoint /estimated-salary --query "backend engineer" --location "austin, tx" \
  --format json --output output/backend_salary.json
```

First pulls job listings, then fetches salary benchmarks for the same role/location so you can compare offers against market rates.
