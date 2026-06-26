# realtime-amazon-data Recipes

## 1. Search for products and export to CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-amazon-data/scrape.js \
  --query "wireless earbuds" --count 100 --format csv --sort-by BEST_SELLERS
```

Exports up to 100 best-selling wireless earbuds with price, rating, and URL to a CSV file.

## 2. Batch product details for multiple ASINs

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-amazon-data/scrape.js \
  --endpoint /product-details --asins "B0BSHF7WHW,B09V3KXJPB,B0D1XD1ZV3" --format json
```

Fetches full product details for three ASINs in one run and saves them as a single JSON file.

## 3. Fetch top reviews for a product

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-amazon-data/scrape.js \
  --endpoint /top-product-reviews --asin B0BSHF7WHW --format csv
```

Retrieves the top reviews shown on the product page (no cookie required) and exports to CSV.

## 4. Get current Amazon deals

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-amazon-data/scrape.js \
  --endpoint /deals-v2 --count 60 --country US --format json
```

Fetches the latest 60 Amazon deals with savings percentages, deal types, and end times.

## 5. Search Amazon then enrich with web search context

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-amazon-data/scrape.js \
  --query "standing desk" --count 5 --dry-run | \
  jq -r '.[].product_title' | head -3 | while read title; do
    node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
      --query "$title review" --count 5 --dry-run
  done
```

Searches Amazon for standing desks, then pipes the top 3 product titles into the web search API to find independent reviews.
