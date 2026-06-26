# realtime-walmart-data Recipes

## 1. Search Walmart products and export to CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-walmart-data/scrape.js \
  --query "air fryer" --count 100 --format csv --sort-by best_seller
```

Exports up to 100 best-selling air fryers with price, rating, and availability to a CSV file.

## 2. Get product details for a specific item

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-walmart-data/scrape.js \
  --endpoint /product-details --product-id 609040889 --format json
```

Fetches full product details including variants, pricing, and seller info for a single Walmart product.

## 3. Fetch reviews for a product

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-walmart-data/scrape.js \
  --endpoint /product-reviews --product-id 609040889 --count 50 --sort recent --format csv
```

Retrieves up to 50 recent reviews for a product and exports to CSV for sentiment analysis.

## 4. Browse products by category with price filter

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-walmart-data/scrape.js \
  --endpoint /products-by-category --category-id 3944 --min-price 10 --max-price 100 --count 80 --format json
```

Fetches up to 80 products from Walmart category 3944, filtered to the $10-$100 price range.

## 5. Compare Walmart and Amazon prices for the same product

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-walmart-data/scrape.js \
  --query "sony wh-1000xm5" --count 5 --dry-run

node --env-file=.env openwebninja_universal_scraper/apis/realtime-amazon-data/scrape.js \
  --query "sony wh-1000xm5" --count 5 --dry-run
```

Searches both Walmart and Amazon for the same product to compare prices and availability side by side.
