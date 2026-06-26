# realtime-ebay-data Recipes

## 1. Search eBay products and export to CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-ebay-data/scrape.js \
  --query "nintendo switch oled" --count 120 --format csv --sort-by PRICE_LOWEST
```

Exports up to 120 listings (cheapest first) with price, condition, seller feedback, and shipping to a CSV file.

## 2. Find used/refurbished iPhones under a price cap on the UK marketplace

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-ebay-data/scrape.js \
  --query "iphone 15 pro max" --domain co.uk --condition "used,refurbished" \
  --max-price 600 --count 60 --format json
```

Searches eBay UK for used/refurbished iPhone 15 Pro Max listings priced under £600.

## 3. Get full details for a specific listing

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-ebay-data/scrape.js \
  --endpoint /product-details --product-id 287062440001 --format json
```

Fetches title, images, condition, item specifics, seller ratings, and return policy for a single eBay item.

## 4. Pull a seller's recent feedback for reputation analysis

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-ebay-data/scrape.js \
  --endpoint /seller-feedback --seller-id musicmagpie --count 100 --format csv
```

Retrieves up to 100 feedback reviews (25 per page) for the seller, with rating, comment, and verified-purchase status — useful for sentiment analysis.

## 5. Browse a category with an aspect filter

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-ebay-data/scrape.js \
  --endpoint /products-by-category --category-id 9355 --query "samsung galaxy" \
  --aspects '[{"name":"Brand","value":"Samsung"}]' --count 60 --dry-run
```

Browses Cell Phones & Smartphones (category 9355) for Samsung Galaxy listings filtered to the Samsung brand aspect.
