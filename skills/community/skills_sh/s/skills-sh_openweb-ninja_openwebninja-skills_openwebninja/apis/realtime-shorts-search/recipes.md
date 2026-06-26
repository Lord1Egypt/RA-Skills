# realtime-shorts-search Recipes

> **WARNING:** This API currently returns empty results for all queries and may
> be non-functional. Always test with `--dry-run` first before running full scrapes.

## 1. Search for trending short videos

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-shorts-search/scrape.js \
  --query "cooking tips" --count 50 --format json --dry-run
```

Searches for cooking-related short videos. Use `--dry-run` to verify the API is returning data before a full run.

## 2. Filter shorts by time period

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-shorts-search/scrape.js \
  --query "tech review" --time week --count 30 --format csv
```

Searches for tech review shorts posted in the past week.

## 3. Search with date range and quality filter

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-shorts-search/scrape.js \
  --query "travel vlog" --date-from "1/1/2025" --date-to "3/1/2025" --high-quality true --format json
```

Finds high-quality travel vlog shorts posted between January and March 2025.

## 4. Cross-reference shorts with web search results

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-shorts-search/scrape.js \
  --query "AI tools 2025" --count 10 --dry-run

node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --query "best AI tools 2025 short video" --count 10 --dry-run
```

Searches both the Shorts API and web search for AI tools content to compare coverage across platforms.
