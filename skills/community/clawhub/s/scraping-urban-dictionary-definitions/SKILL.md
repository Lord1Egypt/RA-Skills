---
name: scraping-urban-dictionary-definitions
description: >
  Extracts definitions, examples, and community votes from Urban Dictionary using apidojo's
  Urban Dictionary Scraper on Apify. Triggers when the user asks to: get Urban Dictionary definitions
  for a word or phrase, look up slang terms on Urban Dictionary, scrape definitions for internet
  slang or memes, export Urban Dictionary entries for a keyword, find how a term is defined by the
  internet community, collect crowd-sourced definitions for multiple words, or analyze slang usage
  and voting patterns. Returns word, definition, example, author, upvotes, downvotes, and timestamp.
  Ideal for linguists, brand researchers, content teams, and cultural trend analysts.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/urbandictionary-scraper
---

# Scraping Urban Dictionary Definitions

Raw data collection. No assumed use case — returns the full dataset for downstream analysis.

---

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Urban Dictionary search URLs |
| `keywords` | array | Optional | `[]` | Keywords/slang terms to search |
| `maxItems` | number | Optional | Unlimited | Maximum definitions to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## How to Run

### Using run_actor.js (recommended)

```bash
# Quick answer (table)
node scripts/run_actor.js --actor "apidojo~urbandictionary-scraper" --input '{"keywords": ["slay", "lowkey"], "maxItems": 10}'

# Save as CSV
node scripts/run_actor.js --actor "apidojo~urbandictionary-scraper" --input '{"keywords": ["slay", "lowkey"], "maxItems": 10}' --output results.csv --format csv

# Save as JSON
node scripts/run_actor.js --actor "apidojo~urbandictionary-scraper" --input '{"keywords": ["slay", "lowkey"], "maxItems": 10}' --output results.json --format json
```

### REST API fallback

```bash
curl -X POST "https://api.apify.com/v2/acts/apidojo~urbandictionary-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["slay", "lowkey"], "maxItems": 10}'
```

If Apify MCP is available:
Use the Apify MCP `call_actor` tool with actor `apidojo~urbandictionary-scraper` and the input above.

---

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `word` | string | The term being defined |
| `definition` | string | User-submitted definition |
| `example` | string | Example sentence |
| `author` | string | Definition author username |
| `id` | number | Definition ID |
| `createdAt` | string | Submission timestamp (ISO 8601) |
| `numberOfThumbsUp` | number | Upvotes |
| `numberOfThumbsDown` | number | Downvotes |
| `url` | string | Definition URL |

## Edge Cases

- **No results**: Term may not be in Urban Dictionary or spelled differently.
- **NSFW content**: Urban Dictionary contains explicit content by design — filter downstream if needed.
- **Multiple definitions**: A word may have 50+ entries. Use maxItems to cap.
- **Community vote gap**: High thumbs-up vs thumbs-down indicates consensus vs controversy.
