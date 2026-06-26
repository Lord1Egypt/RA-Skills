# gemini recipes

## 1. Simple question

```bash
node --env-file=.env openwebninja_universal_scraper/apis/gemini/scrape.js \
  --message "What are the pros and cons of microservices architecture?"
```

Sends a question to Google Gemini and saves the response to a JSON file.

## 2. Continue a conversation

```bash
# First message
node --env-file=.env openwebninja_universal_scraper/apis/gemini/scrape.js \
  --message "Explain how neural networks work" --output output/gemini_nn.json

# Follow-up (use conversation_id from the first response)
node --env-file=.env openwebninja_universal_scraper/apis/gemini/scrape.js \
  --message "Now explain backpropagation in more detail" \
  --conversation-id "<conversation_id_from_previous_response>"
```

Uses conversation_id for multi-turn context so Gemini remembers the prior exchange.

## 3. Analyze scraped data with Gemini

```bash
# Step 1: Scrape job listings
node --env-file=.env openwebninja_universal_scraper/apis/jsearch/scrape.js \
  --endpoint /search --query "data engineer remote" --count 20 --output output/jobs.json

# Step 2: Ask Gemini to analyze
node --env-file=.env openwebninja_universal_scraper/apis/gemini/scrape.js \
  --message "Analyze these job listings. What are the most common skills required and salary ranges?" \
  --context output/jobs.json --output output/jobs_analysis.json
```

Scrapes job listings, then feeds them to Gemini for skills and salary analysis.

## 4. Quick dry-run preview

```bash
node --env-file=.env openwebninja_universal_scraper/apis/gemini/scrape.js \
  --message "Compare Python and Rust for backend development" --dry-run
```

Prints Gemini's response to the console without writing a file.

## 5. Multi-AI comparison: Gemini vs ChatGPT

```bash
PROMPT="Explain the impact of quantum computing on cryptography in 3 paragraphs"

node --env-file=.env openwebninja_universal_scraper/apis/gemini/scrape.js \
  --message "$PROMPT" --output output/gemini_quantum.json

node --env-file=.env openwebninja_universal_scraper/apis/chatgpt/scrape.js \
  --message "$PROMPT" --output output/chatgpt_quantum.json
```

Sends the same prompt to both Gemini and ChatGPT for side-by-side comparison.
