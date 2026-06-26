# job-salary-data Recipes

## 1. Look up salary range for a job title in a city

```bash
node --env-file=.env openwebninja_universal_scraper/apis/job-salary-data/scrape.js \
  --job-title "software engineer" --location "San Francisco, CA" \
  --location-type CITY --format json --dry-run
```

Returns min, median, and max salary estimates for a software engineer role in San Francisco.

## 2. Compare salaries across experience levels

```bash
node --env-file=.env openwebninja_universal_scraper/apis/job-salary-data/scrape.js \
  --job-title "data scientist" --location "United States" \
  --location-type COUNTRY --years-of-experience 3-5 --format csv \
  --output output/data-scientist-salary-3-5yrs.csv
```

Fetches salary data for a mid-level data scientist nationally and exports to CSV for comparison.

## 3. Fetch company-specific compensation for a role

```bash
node --env-file=.env openwebninja_universal_scraper/apis/job-salary-data/scrape.js \
  --endpoint /company-job-salary --job-title "product manager" \
  --company "Meta" --location "Seattle, WA" --location-type CITY --dry-run
```

Returns base salary plus additional pay (bonuses, etc.) for a PM role at Meta in Seattle.

## 4. Export state-wide salary survey to CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/job-salary-data/scrape.js \
  --job-title "registered nurse" --location "Texas" \
  --location-type STATE --format csv --output output/rn-salary-texas.csv
```

Pulls salary estimates for registered nurses across the state of Texas and saves as CSV.

## 5. Entry-level vs senior salary comparison for the same role

```bash
node --env-file=.env openwebninja_universal_scraper/apis/job-salary-data/scrape.js \
  --job-title "marketing manager" --location "New York" \
  --location-type STATE --years-of-experience 0-1 --dry-run

node --env-file=.env openwebninja_universal_scraper/apis/job-salary-data/scrape.js \
  --job-title "marketing manager" --location "New York" \
  --location-type STATE --years-of-experience 10-15 --dry-run
```

Run both commands to compare entry-level vs senior marketing manager salaries in New York state.
