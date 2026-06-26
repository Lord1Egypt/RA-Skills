# realtime-product-search recipes

## 1. Search for cheap laptops under $500

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-product-search/scrape.js \
  --query "laptop" --max-price 500 --sort-by LOWEST_PRICE --count 50 --format csv
```

Exports up to 50 laptops priced under $500 sorted by lowest price to CSV.

## 2. Find deals on refurbished headphones

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-product-search/scrape.js \
  --endpoint /deals-v2 --query "wireless headphones" --condition REFURBISHED --count 30
```

Fetches up to 30 current deals on refurbished wireless headphones as JSON.

## 3. Get reviews for a specific product

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-product-search/scrape.js \
  --endpoint /product-reviews-v2 --product-id "YOUR_PRODUCT_ID" --sort-by MOST_RECENT --count 50
```

Fetches the 50 most recent reviews for a product (replace YOUR_PRODUCT_ID with an actual ID from a search result).

## 4. Amazon store reviews

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-product-search/scrape.js \
  --endpoint /store-reviews --store-domain amazon.com --sort-by MOST_RECENT --count 40 --format csv
```

Exports the 40 most recent Amazon store reviews as CSV.

## 5. Multi-API: find products then enrich with local business data

```bash
# Step 1: Find top-rated camera stores
node --env-file=.env openwebninja_universal_scraper/apis/realtime-product-search/scrape.js \
  --query "DSLR camera" --sort-by TOP_RATED --count 20 --format json --output output/cameras.json

# Step 2: Search for camera shops near you with local-business-data
node --env-file=.env openwebninja_universal_scraper/apis/local-business-data/scrape.js \
  --query "camera store" --count 20 --format json --output output/camera_shops.json
```

Compares online product listings against local camera shops for price research.
