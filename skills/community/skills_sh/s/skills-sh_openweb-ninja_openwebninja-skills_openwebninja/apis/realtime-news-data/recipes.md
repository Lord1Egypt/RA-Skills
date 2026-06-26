# realtime-news-data Recipes

## 1. Search news articles and export to CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-news-data/scrape.js \
  --query "artificial intelligence startups" --count 50 --format csv
```

Fetches up to 50 news articles matching the query with title, link, source, and publish date.

## 2. Get today's top headlines for a country

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-news-data/scrape.js \
  --endpoint /top-headlines --country US --count 100 --format json
```

Retrieves the top 100 headlines for the US, including source logos and thumbnails.

## 3. Fetch technology topic headlines

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-news-data/scrape.js \
  --endpoint /topic-headlines --topic TECHNOLOGY --country US --count 50 --format csv
```

Gets the latest 50 technology news headlines, useful for daily tech news monitoring.

## 4. Local news for a specific city

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-news-data/scrape.js \
  --endpoint /local-headlines --query "San Francisco" --count 30 --format json
```

Fetches geo-targeted local news headlines for San Francisco.

## 5. Cross-API: news monitoring with Amazon product research

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-news-data/scrape.js \
  --query "best laptops 2025" --count 10 --dry-run | \
  jq -r '.[0].title' | xargs -I{} \
  node --env-file=.env openwebninja_universal_scraper/apis/realtime-amazon-data/scrape.js \
    --query "{}" --count 10 --dry-run
```

Finds trending laptop news articles, then searches Amazon for matching products mentioned in headlines.
