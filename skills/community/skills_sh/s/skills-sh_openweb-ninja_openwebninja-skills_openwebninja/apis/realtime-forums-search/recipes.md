# realtime-forums-search Recipes

## 1. Search forums for product discussions

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-forums-search/scrape.js \
  --query "best mechanical keyboard 2026" --count 30 --format json
```

Returns up to 30 forum threads discussing mechanical keyboards, with titles, snippets, URLs, and sources.

## 2. Find recent forum mentions (last week)

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-forums-search/scrape.js \
  --query "openai api pricing" --time week --count 50 --format csv
```

Searches forums for threads from the past week about OpenAI API pricing and exports as CSV.

## 3. Search forums in a specific country and language

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-forums-search/scrape.js \
  --query "mejores frameworks javascript" --country es --language es --count 20
```

Searches Spanish-language forums in Spain for JavaScript framework discussions.

## 4. Chain: find forum buzz then scrape mentioned sites for contacts

```bash
# Step 1 — find forum threads mentioning a product category
node --env-file=.env openwebninja_universal_scraper/apis/realtime-forums-search/scrape.js \
  --query "best CRM for startups" --time month --count 30 \
  --format json --output output/crm_forums.json

# Step 2 — extract unique domains mentioned in forum results
DOMAINS=$(node -e "
  const d = require('./output/crm_forums.json');
  const urls = d.map(r => { try { return new URL(r.url).hostname; } catch { return null; } }).filter(Boolean);
  console.log([...new Set(urls)].slice(0, 20).join(','));
")

# Step 3 — scrape contacts from those domains
node --env-file=.env openwebninja_universal_scraper/apis/website-contacts-scraper/scrape.js \
  --domains "$DOMAINS" --match-email --format csv --output output/crm_contacts.csv
```

Discovers which CRM tools people recommend in forums, then scrapes contact info from the source sites.

## 5. Dry-run preview

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-forums-search/scrape.js \
  --query "cursor vs copilot" --dry-run
```

Fetches only the first batch of results and prints to console without writing a file.
