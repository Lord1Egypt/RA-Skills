# copilot recipes

## 1. Simple question

```bash
node --env-file=.env openwebninja_universal_scraper/apis/copilot/scrape.js \
  --message "What are the latest developments in renewable energy?"
```

Sends a question to Microsoft Copilot and saves the response to a JSON file.

## 2. Continue a conversation

```bash
# First message
node --env-file=.env openwebninja_universal_scraper/apis/copilot/scrape.js \
  --message "Explain the difference between REST and GraphQL" --output output/copilot_rest.json

# Follow-up (use conversation_id from the first response)
node --env-file=.env openwebninja_universal_scraper/apis/copilot/scrape.js \
  --message "Which one would you recommend for a mobile app?" \
  --conversation-id "<conversation_id_from_previous_response>"
```

Uses conversation_id for multi-turn context so Copilot remembers the prior exchange.

## 3. Analyze scraped data with Copilot

```bash
# Step 1: Scrape news articles
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --endpoint /search --query "AI regulation 2026" --count 10 --output output/ai_news.json

# Step 2: Ask Copilot to summarize
node --env-file=.env openwebninja_universal_scraper/apis/copilot/scrape.js \
  --message "Summarize the key themes from these search results" \
  --context output/ai_news.json --output output/ai_news_summary.json
```

Scrapes web search results, then feeds them to Copilot for analysis.

## 4. Quick dry-run preview

```bash
node --env-file=.env openwebninja_universal_scraper/apis/copilot/scrape.js \
  --message "Give me 5 startup ideas in the health tech space" --dry-run
```

Prints Copilot's response to the console without writing a file.

## 5. Generate structured output

```bash
node --env-file=.env openwebninja_universal_scraper/apis/copilot/scrape.js \
  --message "List the top 10 countries by GDP as a JSON array with fields: country, gdp_usd_trillions, growth_rate" \
  --format json --output output/gdp_data.json
```

Asks Copilot to generate structured JSON data.
