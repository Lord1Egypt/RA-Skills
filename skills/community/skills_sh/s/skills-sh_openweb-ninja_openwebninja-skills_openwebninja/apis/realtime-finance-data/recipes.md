# realtime-finance-data Recipes

## 1. Get a stock quote and export to JSON

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-finance-data/scrape.js \
  --endpoint /stock-quote --symbol AAPL --format json
```

Fetches the current quote for Apple (AAPL) including price, change, volume, and market cap.

## 2. Export stock news as CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-finance-data/scrape.js \
  --endpoint /stock-news --symbol TSLA --format csv
```

Gets all recent news articles for Tesla and exports them as a CSV with title, source, date, and URL.

## 3. Currency exchange rate lookup (dry run)

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-finance-data/scrape.js \
  --endpoint /currency-exchange-rate --from-symbol USD --to-symbol EUR --dry-run
```

Quickly checks the current USD to EUR exchange rate, printed to console without saving.

## 4. Company financials: income statement

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-finance-data/scrape.js \
  --endpoint /company-income-statement --symbol MSFT --period ANNUAL --format csv
```

Exports Microsoft's annual income statement data to CSV for spreadsheet analysis.

## 5. Cross-API: search stocks then fetch news for top result

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-finance-data/scrape.js \
  --endpoint /search --query "electric vehicles" --dry-run | \
  jq -r '.[0].symbol' | xargs -I{} \
  node --env-file=.env openwebninja_universal_scraper/apis/realtime-finance-data/scrape.js \
    --endpoint /stock-news --symbol {} --format json
```

Searches for EV-related stocks, picks the top symbol, then fetches its latest news articles.
