# realtime-news-search Recipes

## 1. Search news articles and export to CSV

```bash
node --env-file=.env apis/realtime-news-search/scrape.js \
  --query "artificial intelligence startups" --count 50 --format csv
```

Fetches up to 50 news articles matching the query (paginated 10/page) with title, link, snippet, source, thumbnail, and publish date.

## 2. Latest news only, sorted by date

```bash
node --env-file=.env apis/realtime-news-search/scrape.js \
  --query "bitcoin price" --time-period last_day --sort-by date --count 30 --format json
```

Returns the most recent stories from the last 24 hours, newest first — useful for breaking-news and alerting workflows.

## 3. Brand monitoring over a custom date range

```bash
node --env-file=.env apis/realtime-news-search/scrape.js \
  --query "Tesla recall" --date-from 01/01/2026 --date-to 04/10/2026 \
  --country us --language en --count 100 --format csv
```

Pulls coverage of a topic within a specific date window (MM/DD/YYYY). Do not combine `--date-from`/`--date-to` with `--time-period`.

## 4. Quick answer: top headlines for a query

```bash
node --env-file=.env apis/realtime-news-search/scrape.js \
  --query "climate change" --country gb --language en --dry-run
```

Fetches the first page and prints the top results to the console without saving a file — handy for a fast "what's the latest on X?" lookup.

## 5. Cross-API: news search → forum sentiment

```bash
node --env-file=.env apis/realtime-news-search/scrape.js \
  --query "new iphone 2026" --count 10 --dry-run | \
  jq -r '.[0].title' | xargs -I{} \
  node --env-file=.env apis/realtime-forums-search/scrape.js \
    --query "{}" --count 10 --dry-run
```

Finds a trending news headline, then searches Reddit/Quora/Stack Overflow discussions about it to gauge public sentiment.
