# chatgpt recipes

## 1. Simple question

```bash
node --env-file=.env openwebninja_universal_scraper/apis/chatgpt/scrape.js \
  --message "What are the top 5 programming languages in 2025?"
```

Saves ChatGPT's response about top programming languages to a JSON file.

## 2. Summarize a document

```bash
node --env-file=.env openwebninja_universal_scraper/apis/chatgpt/scrape.js \
  --message "Summarize the key points from this document" \
  --context ./my-report.txt --output output/summary.json
```

Reads my-report.txt as context and asks ChatGPT to summarize it.

## 3. Quick dry-run to preview response

```bash
node --env-file=.env openwebninja_universal_scraper/apis/chatgpt/scrape.js \
  --message "Explain quantum computing in 3 sentences" --dry-run
```

Prints ChatGPT's response to the console without writing a file.

## 4. Multi-API: analyze scraped product data with ChatGPT

```bash
# Step 1: Scrape product deals
node --env-file=.env openwebninja_universal_scraper/apis/realtime-product-search/scrape.js \
  --endpoint /deals-v2 --query "mechanical keyboard" --count 20 --output output/keyboards.json

# Step 2: Ask ChatGPT to analyze the results
node --env-file=.env openwebninja_universal_scraper/apis/chatgpt/scrape.js \
  --message "Analyze these product deals and recommend the best value for money" \
  --context output/keyboards.json --output output/keyboard_analysis.json
```

Scrapes keyboard deals, then feeds the JSON to ChatGPT for a best-value recommendation.

## 5. Generate structured data from a prompt

```bash
node --env-file=.env openwebninja_universal_scraper/apis/chatgpt/scrape.js \
  --message "List 10 popular tourist attractions in Tokyo as a JSON array with fields: name, category, typical_visit_hours" \
  --format json --output output/tokyo_attractions.json
```

Asks ChatGPT to generate structured JSON data about Tokyo attractions.
