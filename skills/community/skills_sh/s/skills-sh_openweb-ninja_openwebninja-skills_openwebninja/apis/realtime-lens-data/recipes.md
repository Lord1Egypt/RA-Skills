# realtime-lens-data Recipes

## 1. Reverse image search with a URL

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-lens-data/scrape.js \
  --url "https://i.imgur.com/HBrB8p0.png" --format json
```

Performs a Google Lens reverse image search and exports matching web pages with titles, URLs, and snippets.

## 2. Find visual matches for a product image

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-lens-data/scrape.js \
  --endpoint /visual-matches --url "https://example.com/product.jpg" --query "buy online" --format csv
```

Finds visually similar images across the web, refined by a purchase-intent query. Great for competitive product research.

## 3. Find all sites using a specific image (exact matches)

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-lens-data/scrape.js \
  --endpoint /exact-matches --url "https://example.com/logo.png" --count 100 --format csv
```

Finds up to 100 web pages hosting the exact same image. Useful for brand monitoring and copyright tracking.

## 4. Extract text from an image (OCR)

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-lens-data/scrape.js \
  --endpoint /ocr --url "https://example.com/screenshot.png" --dry-run
```

Extracts text from an image using Google Lens OCR, printed to console for quick review.

## 5. Cross-API: search images then reverse-search the top result

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-image-search/scrape.js \
  --query "vintage poster art" --count 1 --dry-run | \
  jq -r '.[0].url' | xargs -I{} \
  node --env-file=.env openwebninja_universal_scraper/apis/realtime-lens-data/scrape.js \
    --endpoint /visual-matches --url "{}" --format json
```

Finds an image via search, then discovers visually similar images across the web using Google Lens.
