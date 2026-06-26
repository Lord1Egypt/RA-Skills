# social-links-search recipes

## 1. Find social profiles for a person

```bash
node --env-file=.env openwebninja_universal_scraper/apis/social-links-search/scrape.js \
  --query "John Smith"
```

Searches for social media profiles matching "John Smith" across all default networks.

## 2. Search specific networks only

```bash
node --env-file=.env openwebninja_universal_scraper/apis/social-links-search/scrape.js \
  --query "OpenAI" --social-networks "linkedin,twitter,github" \
  --output output/openai_socials.json
```

Searches only LinkedIn, Twitter, and GitHub for profiles related to OpenAI.

## 3. Export social links as CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/social-links-search/scrape.js \
  --query "Elon Musk" --format csv --output output/elon_socials.csv
```

Finds all social profiles and exports as a flat CSV with network and URL columns.

## 4. Dry-run preview

```bash
node --env-file=.env openwebninja_universal_scraper/apis/social-links-search/scrape.js \
  --query "Netflix" --dry-run
```

Prints all found social links to the console without writing a file.

## 5. Cross-API: combine email search with social links

```bash
# Step 1: Find emails for a company
node --env-file=.env openwebninja_universal_scraper/apis/email-search/scrape.js \
  --query "product manager" --domain stripe.com --limit 50 \
  --output output/stripe_emails.json

# Step 2: Find social profiles for the same company
node --env-file=.env openwebninja_universal_scraper/apis/social-links-search/scrape.js \
  --query "Stripe product manager" --social-networks "linkedin,twitter" \
  --output output/stripe_socials.json
```

Builds a contact profile by combining email addresses with social media links.
