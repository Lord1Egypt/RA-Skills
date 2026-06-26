# google-ai-mode Recipes

Uses `apis/realtime-web-search/scrape.js` with `--endpoint /ai-mode`.

## 1. Ask Google AI Mode a step-by-step question

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --endpoint /ai-mode --query "How do I set up a Node.js project from scratch?" --dry-run
```

Returns a structured AI response with headings, paragraphs, and lists — similar to what Google AI Mode shows in search.

## 2. Save an AI Mode response to JSON

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --endpoint /ai-mode --query "Explain the pros and cons of microservices architecture" \
  --format json --output output/ai-mode-microservices.json
```

Saves the full structured AI response including reply_parts and reference_links for content analysis.

## 3. Ask a localized question in a specific language

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --endpoint /ai-mode --query "Quelles sont les meilleures pratiques pour apprendre le français?" \
  --country fr --language fr --dry-run
```

Sends a French-language prompt and retrieves a localized AI Mode response from Google's French index.

## 4. Multi-turn conversation using session_token

```bash
# First turn — save the response to extract session_token
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --endpoint /ai-mode --query "What is quantum computing?" \
  --format json --output output/ai-mode-turn1.json

# Second turn — pass session_token from the first response to continue the conversation
SESSION=$(jq -r '.[0].session_token // empty' output/ai-mode-turn1.json)
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --endpoint /ai-mode --query "How is it used in cryptography?" \
  --session-token "$SESSION" --dry-run
```

Demonstrates a two-turn conversation where the second prompt builds on the context of the first.

## 5. Cross-API: AI Mode answer + supporting news articles

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --endpoint /ai-mode --query "What is happening with AI regulation in 2025?" --dry-run

node --env-file=.env openwebninja_universal_scraper/apis/realtime-news-data/scrape.js \
  --query "AI regulation 2025" --count 10 --format json \
  --output output/ai-regulation-news.json
```

Gets Google AI Mode's synthesized answer to a policy question, then pulls the latest news articles on the same topic for verification and citation.
