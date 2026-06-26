# email-search recipes

## 1. Find Gmail addresses for a niche

```bash
node --env-file=.env openwebninja_universal_scraper/apis/email-search/scrape.js \
  --query "Car Dealer California USA" --domain gmail.com --limit 100
```

Searches the web for Gmail addresses related to car dealers in California.

## 2. Find company emails

```bash
node --env-file=.env openwebninja_universal_scraper/apis/email-search/scrape.js \
  --query "marketing manager" --domain hubspot.com --format csv --output output/hubspot_emails.csv
```

Finds email addresses at hubspot.com for marketing managers and exports as CSV.

## 3. Bulk lead generation with limit

```bash
node --env-file=.env openwebninja_universal_scraper/apis/email-search/scrape.js \
  --query "real estate agent New York" --domain gmail.com --limit 500 \
  --output output/realestate_leads.json
```

Collects up to 500 Gmail addresses for real estate agents in New York.

## 4. Dry-run to preview results

```bash
node --env-file=.env openwebninja_universal_scraper/apis/email-search/scrape.js \
  --query "software engineer" --domain outlook.com --limit 50 --dry-run
```

Previews the first 20 results in the console without saving a file.

## 5. Cross-API: find emails then find social profiles

```bash
# Step 1: Find emails for tech recruiters
node --env-file=.env openwebninja_universal_scraper/apis/email-search/scrape.js \
  --query "tech recruiter San Francisco" --domain gmail.com --limit 20 \
  --output output/recruiter_emails.json

# Step 2: Search social profiles for the same people
node --env-file=.env openwebninja_universal_scraper/apis/social-links-search/scrape.js \
  --query "tech recruiter San Francisco" --output output/recruiter_socials.json
```

Finds recruiter emails, then searches for their social media profiles.
