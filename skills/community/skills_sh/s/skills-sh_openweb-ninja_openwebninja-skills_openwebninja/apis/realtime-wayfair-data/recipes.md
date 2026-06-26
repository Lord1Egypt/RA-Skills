# realtime-wayfair-data Recipes

## 1. Search Wayfair products and export to CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-wayfair-data/scrape.js \
  --query "sectional sofa" --count 96 --format csv --sort-by customer_rating
```

Exports up to 96 top-rated sectional sofas with price, rating, shipping, and stock status to a CSV file.

## 2. Browse a brand's products with a price filter

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-wayfair-data/scrape.js \
  --manufacturer-id 21377 --min-price 100 --max-price 500 --color Black --in-stock --count 96 --format json
```

Browses all in-stock products from a specific Wayfair manufacturer/brand, filtered to black items between $100-$500.

## 3. Get product details for a specific SKU

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-wayfair-data/scrape.js \
  --endpoint /product-details --sku W110457689 --format json
```

Fetches full product details including name, brand, pricing, images, rating, and description for a single Wayfair product.

## 4. Fetch reviews for a product (with AI summary + aspect sentiments)

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-wayfair-data/scrape.js \
  --endpoint /product-reviews --sku MBYC1062 --count 50 --sort-by date_descending --format csv
```

Retrieves up to 50 most-recent reviews (10 per page) for a product and exports to CSV for sentiment analysis. The raw response also carries an AI-generated review summary and per-aspect sentiment breakdown.
