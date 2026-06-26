# reverse-image-search Recipes

## 1. Find all web pages using a specific image

```bash
node --env-file=.env openwebninja_universal_scraper/apis/reverse-image-search/scrape.js \
  --url "https://example.com/product-photo.jpg" --limit 100 --format json --dry-run
```

Returns the top 100 web pages that contain or match the given image, with titles, domains, and links.

## 2. Detect unauthorized use of your brand images

```bash
node --env-file=.env openwebninja_universal_scraper/apis/reverse-image-search/scrape.js \
  --url "https://yourbrand.com/logo.png" --limit 500 \
  --format csv --output output/logo-usage-audit.csv
```

Exports up to 500 pages using your logo image to CSV — useful for brand protection audits.

## 3. Safe-search filtered reverse lookup

```bash
node --env-file=.env openwebninja_universal_scraper/apis/reverse-image-search/scrape.js \
  --url "https://example.com/person-photo.jpg" --limit 50 \
  --safe-search blur --format json --dry-run
```

Searches for image sources with safe search enabled (explicit content blurred), suitable for public-facing tools.

## 4. Quick domain list from a reverse image search

```bash
node --env-file=.env openwebninja_universal_scraper/apis/reverse-image-search/scrape.js \
  --url "https://cdn.example.com/hero-image.jpg" --limit 200 \
  --format json --output output/image-sources.json
```

Saves the full list of source pages as JSON for downstream deduplication or domain analysis.

## 5. Cross-API: find image sources then check business info

```bash
node --env-file=.env openwebninja_universal_scraper/apis/reverse-image-search/scrape.js \
  --url "https://example.com/storefront.jpg" --limit 10 --dry-run | \
  jq -r '.[0].domain' | xargs -I{} \
  node --env-file=.env openwebninja_universal_scraper/apis/local-business-data/scrape.js \
    --query "{}" --count 5 --dry-run
```

Takes the top domain from a reverse image search and looks it up in the local business data API.
