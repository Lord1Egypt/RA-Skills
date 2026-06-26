# website-contacts-scraper Recipes

## 1. Scrape contacts from a single domain

```bash
node --env-file=.env openwebninja_universal_scraper/apis/website-contacts-scraper/scrape.js \
  --domain "openwebninja.com" --format json
```

Returns emails, phone numbers, and social media profiles found on the given website.

## 2. Batch scrape contacts for multiple domains

```bash
node --env-file=.env openwebninja_universal_scraper/apis/website-contacts-scraper/scrape.js \
  --domains "stripe.com,shopify.com,twilio.com,vercel.com" --format csv
```

Scrapes contact info from up to 20 domains in a single API call and exports as CSV.

## 3. Match emails to domain only

```bash
node --env-file=.env openwebninja_universal_scraper/apis/website-contacts-scraper/scrape.js \
  --domain "hubspot.com" --match-email --format json
```

Only returns email addresses whose domain matches the target website (filters out generic gmail/yahoo addresses).

## 4. Chain: find businesses then scrape their contacts

```bash
# Step 1 — find businesses with local-business-data
node --env-file=.env openwebninja_universal_scraper/apis/local-business-data/scrape.js \
  --query "marketing agencies in Austin, TX" --count 20 --format json --output output/agencies.json

# Step 2 — extract domains from results and scrape contacts
DOMAINS=$(node -e "
  const d = require('./output/agencies.json');
  const sites = d.map(r => r.website).filter(Boolean).map(u => new URL(u).hostname);
  console.log([...new Set(sites)].slice(0, 20).join(','));
")
node --env-file=.env openwebninja_universal_scraper/apis/website-contacts-scraper/scrape.js \
  --domains "$DOMAINS" --match-email --format csv --output output/agency_contacts.csv
```

Finds local marketing agencies, extracts their websites, then batch-scrapes emails and phone numbers for outreach.

## 5. Dry-run preview before committing to a large batch

```bash
node --env-file=.env openwebninja_universal_scraper/apis/website-contacts-scraper/scrape.js \
  --domains "example.com,test.com" --dry-run
```

Fetches the first batch and prints results to console without writing a file, so you can verify the data shape.
