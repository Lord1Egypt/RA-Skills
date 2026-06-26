# realtime-costco-data Recipes

## 1. Search for Nike products and export as CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-costco-data/scrape.js \
  --query "Nike" --count 50 --format csv
```

Fetches up to 50 Nike products from Costco with name, price, and product details.

## 2. Quick price check (dry run)

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-costco-data/scrape.js \
  --query "Kirkland olive oil" --dry-run
```

Quickly checks current Costco prices for Kirkland olive oil, printed to console.

## 3. Electronics comparison export

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-costco-data/scrape.js \
  --query "laptop" --count 100 --format csv --output output/costco-laptops.csv
```

Exports a large set of laptop listings for price comparison in a spreadsheet.

## 4. Cross-API: compare Costco vs Amazon prices

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-costco-data/scrape.js \
  --query "KitchenAid mixer" --count 5 --dry-run && \
node --env-file=.env openwebninja_universal_scraper/apis/realtime-amazon-data/scrape.js \
  --query "KitchenAid mixer" --count 5 --dry-run
```

Fetches KitchenAid mixer listings from both Costco and Amazon for side-by-side price comparison.

## 5. Canadian Costco products

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-costco-data/scrape.js \
  --query "patio furniture" --country CA --language en-CA --count 30 --format json
```

Searches the Canadian Costco catalog for patio furniture with local pricing.
