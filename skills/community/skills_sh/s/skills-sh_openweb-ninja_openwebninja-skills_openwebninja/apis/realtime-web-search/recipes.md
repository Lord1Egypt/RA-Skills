# realtime-web-search Recipes

## 1. Search and export top 50 results as CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --query "best project management tools 2025" --count 50 --format csv
```

Fetches 50 Google search results with title, URL, snippet, and position, exported to CSV.

## 2. Time-filtered search (past week only)

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --query "AI regulation news" --tbs qdr:w --count 30 --format json
```

Returns only results published in the past week, useful for tracking recent developments.

## 3. Quick lightweight search with /search-light

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --endpoint /search-light --query "openwebninja API" --count 10 --dry-run
```

Uses the cheaper light endpoint for a quick 10-result lookup, printed to console without saving.

## 4. Location-specific mobile search

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --query "restaurants near me" --location "New York, NY" --device mobile --count 20 --format json
```

Simulates a mobile Google search from New York, capturing local-intent results.

## 5. Cross-API: web search then fetch matching news articles

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --query "SpaceX Starship launch" --count 5 --dry-run | \
  jq -r '.[0].snippet' | xargs -I{} \
  node --env-file=.env openwebninja_universal_scraper/apis/realtime-news-data/scrape.js \
    --query "{}" --count 10 --dry-run
```

Takes the top web search snippet and uses it as a news search query to find related news coverage.
