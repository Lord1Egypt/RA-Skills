# web-search-autocomplete Recipes

## 1. Get autocomplete suggestions for a query

```bash
node --env-file=.env openwebninja_universal_scraper/apis/web-search-autocomplete/scrape.js \
  --query "how to" --format json --dry-run
```

Fetches Google autocomplete suggestions for "how to" and prints them to the console.

## 2. Batch keyword research with multiple seed queries

```bash
node --env-file=.env openwebninja_universal_scraper/apis/web-search-autocomplete/scrape.js \
  --queries "best crm,best crm for,crm software,crm tools" --format csv
```

Fetches suggestions for 4 seed queries in one run and exports all results to CSV for keyword research.

## 3. Compare suggestions across languages/regions

```bash
node --env-file=.env openwebninja_universal_scraper/apis/web-search-autocomplete/scrape.js \
  --query "pizza" --language en --region us --format json --output output/pizza-us.json

node --env-file=.env openwebninja_universal_scraper/apis/web-search-autocomplete/scrape.js \
  --query "pizza" --language es --region es --format json --output output/pizza-es.json
```

Compares autocomplete suggestions for the same query in different locales.

## 4. Generate long-tail keywords from web search results

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --query "email marketing" --count 5 --dry-run | \
  jq -r '.[].title' | head -3 | while read title; do
    node --env-file=.env openwebninja_universal_scraper/apis/web-search-autocomplete/scrape.js \
      --query "$title" --dry-run
  done
```

Uses top web search result titles as seeds to discover long-tail keyword variations via autocomplete.

## 5. Mobile vs desktop suggestion comparison

```bash
node --env-file=.env openwebninja_universal_scraper/apis/web-search-autocomplete/scrape.js \
  --query "near me" --user-agent desktop --format json --output output/nearme-desktop.json

node --env-file=.env openwebninja_universal_scraper/apis/web-search-autocomplete/scrape.js \
  --query "near me" --user-agent mobile --format json --output output/nearme-mobile.json
```

Compares how autocomplete suggestions differ between desktop and mobile user agents.
