# realtime-homedepot-data Recipes

## 1. Search Home Depot products and export to CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-homedepot-data/scrape.js \
  --query "cordless drill" --count 96 --format csv --sort-by top_sellers
```

Exports up to 96 top-selling cordless drills with price, rating, brand, and availability to a CSV file.

## 2. Filter by brand, price, and in-stock with store localization

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-homedepot-data/scrape.js \
  --query "impact driver" --brand DEWALT --min-price 50 --max-price 200 --in-stock --store-id 121 --count 48 --format json
```

Finds in-stock DEWALT impact drivers between $50-$200, with pricing and fulfillment localized to store 121.

## 3. Get full product details for a specific item

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-homedepot-data/scrape.js \
  --endpoint /product-details --item-id 326680222 --format json
```

Fetches full product details (specs, dimensions, images, pricing, fulfillment) for a single Home Depot item.

## 4. Fetch reviews for a product

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-homedepot-data/scrape.js \
  --endpoint /product-reviews --item-id 300569432 --count 100 --sort-by newest --verified-only --format csv
```

Retrieves up to 100 newest verified-purchaser reviews for an item and exports to CSV for sentiment analysis.

## 5. Look up a product by model number

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-homedepot-data/scrape.js \
  --endpoint /item-lookup --search DCD800B --dry-run
```

Resolves a manufacturer model number (or Home Depot internet number) to matching products and prints the top results to the console.
