# Web Unblocker — Recipes

## 1. Basic page fetch (no JS rendering)

Fetch a static page through the unblocker proxy and save the response.

```bash
node --env-file=.env apis/web-unblocker/scrape.js \
  --url "https://example.com/pricing" \
  --dry-run
```

## 2. Fetch a JavaScript-heavy SPA page

Render JS and wait for a specific element before capturing content.

```bash
node --env-file=.env apis/web-unblocker/scrape.js \
  --url "https://example.com/dashboard" \
  --render-js \
  --wait-until networkidle \
  --wait-for-selector ".main-content" \
  --format json
```

## 3. Scrape a page with anti-bot protection

Use extra retries and a minimum response length to ensure you get real content.

```bash
node --env-file=.env apis/web-unblocker/scrape.js \
  --url "https://protected-site.com/products" \
  --render-js \
  --extra-retries \
  --min-response-len 5000 \
  --failure-selectors ".captcha-challenge" \
  --format json
```

## 4. POST a form payload through the unblocker

Submit a form via POST and capture the response.

```bash
node --env-file=.env apis/web-unblocker/scrape.js \
  --url "https://example.com/api/search" \
  --method POST \
  --body '{"query":"openwebninja","page":1}' \
  --format json
```

## 5. Cross-API: Unblock a page then extract contacts

First fetch a company's "About" page through the unblocker, then pipe the
saved HTML into the Contacts Scraper for email/phone extraction.

```bash
# Step 1 — Fetch the blocked page
node --env-file=.env apis/web-unblocker/scrape.js \
  --url "https://hard-to-reach-site.com/about" \
  --render-js \
  --wait-until networkidle \
  --output output/about-page.json

# Step 2 — Extract the URL and feed it to contacts-scraper
node --env-file=.env apis/contacts-scraper/scrape.js \
  --url "https://hard-to-reach-site.com/about" \
  --format csv \
  --output output/contacts.csv
```
