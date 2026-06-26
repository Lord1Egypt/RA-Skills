# OpenWeb Ninja Universal Scraper

A Claude Code skill that lets you extract data from 35+ public web APIs using natural language. Just describe what you want — Claude selects the right API, runs the script, and returns results as JSON or CSV.

## What it can do

- **Lead generation** — Find businesses, emails, phones, and social profiles by location or industry
- **Market research** — Search news, forums, reviews, and product listings
- **Competitor analysis** — Scrape websites, compare pricing, monitor reviews
- **Job & talent research** — Search job listings, salaries, and company profiles
- **Finance & real estate** — Stock quotes, property listings, Zillow estimates
- **GEO tracking** — Monitor how AI search engines (ChatGPT, Gemini, Copilot) reference your brand or topic

## Covered APIs (36)

| Category | APIs |
|----------|------|
| Local & Maps | local-business-data, local-rank-tracker, waze, ev-charge-finder, driving-directions |
| E-commerce | realtime-amazon-data, realtime-product-search, realtime-walmart-data, realtime-costco-data |
| Jobs & Salaries | jsearch, job-salary-data, realtime-glassdoor-data |
| Reviews | trustpilot-company-and-reviews, yelp-business-data |
| News & Forums | realtime-news-data, realtime-forums-search |
| Search | realtime-web-search, realtime-image-search, realtime-lens-data, realtime-shorts-search, web-search-autocomplete, reverse-image-search |
| Social & Contacts | website-contacts-scraper, social-links-search, email-search |
| Real Estate | realtime-zillow-data |
| Finance | realtime-finance-data |
| Events & Books | realtime-events-search, realtime-books-data |
| Apps | play-store-apps |
| AI Search / GEO | chatgpt, gemini, copilot, ai-overviews, google-ai-mode |
| Web | web-unblocker |

## Requirements

- Node.js 20.6+
- A [RapidAPI](https://rapidapi.com) key with subscriptions to the APIs you want to use, **or** an [OpenWeb Ninja](https://openwebninja.com) API key

## Setup

1. Copy this skill into your Claude Code skills directory:
   ```
   ~/.claude/skills/openwebninja-universal-scraper/
   ```
   Or add it at the project level under `.claude/skills/`.

2. Install dependencies (required for S3, FTP, and Google Sheets output):
   ```bash
   cd ~/.claude/skills/openwebninja-universal-scraper
   npm install
   ```

3. Add your API key to a `.env` file in your project root:
   ```
   RAPIDAPI_KEY=your_key_here
   # or
   OPENWEBNINJA_API_KEY=your_key_here
   ```

4. In Claude Code, the skill is available automatically. Just ask:
   > "Find all Italian restaurants in Chicago with emails"
   > "Get the latest news about OpenAI"
   > "Search Amazon for standing desks under $500 and export to CSV"

## Running scripts directly

Each API has its own `scrape.js` with full CLI support:

```bash
# Search Google Maps businesses with email extraction
node --env-file=.env apis/local-business-data/scrape.js \
  --query "plumbers" --contacts --format csv --output results.csv

# Broad geographic coverage with grid mode (auto-subdivides dense areas)
node --env-file=.env apis/local-business-data/scrape.js \
  --query "plumbers" --grid --bbox "32.5,-124.5,42.0,-114.0" \
  --contacts --max-calls 300 --format csv

# Quick answer (no file saved)
node --env-file=.env apis/realtime-news-data/scrape.js \
  --query "AI startups 2025" --dry-run
```

Run `node apis/{api_id}/scrape.js --help` to see all flags for any API.

## Output destinations

| Destination | Env vars required |
|-------------|------------------|
| Local file (JSON/CSV) | — |
| Chat (quick answer) | — |

## Structure

```
openwebninja-universal-scraper/
├── SKILL.md              # Claude's instructions
├── package.json          # npm dependencies
├── lib/
│   └── utils.js          # Shared HTTP, pagination, CSV, output utilities
└── apis/
    └── {api_id}/
        ├── scrape.js     # CLI scraper script
        ├── README.md     # Endpoint docs and parameters
        ├── meta.json     # Host, pricing, subscription URLs
        └── recipes.md    # Example use cases with exact commands
```
