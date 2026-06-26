# realtime-image-search Recipes

## 1. Search and export image results as CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-image-search/scrape.js \
  --query "modern office interior design" --count 50 --format csv
```

Fetches up to 50 image results with titles, URLs, dimensions, and thumbnails exported to CSV.

## 2. Filter by size, type, and file format

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-image-search/scrape.js \
  --query "product photography" --size large --type photo --file-type jpg --count 30 --format json
```

Returns only large JPG photos, useful for sourcing high-quality product imagery.

## 3. Find Creative Commons licensed images

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-image-search/scrape.js \
  --query "nature landscape" --usage-rights creative_commons --count 20 --dry-run
```

Quick lookup of freely-licensed nature images, printed to console without saving.

## 4. Recent images in a specific aspect ratio

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-image-search/scrape.js \
  --query "AI generated art" --time week --aspect-ratio wide --count 40 --format json
```

Finds wide-format images from the past week, ideal for blog headers or social media banners.

## 5. Cross-API: web search then find related images

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --query "trending fashion 2025" --count 3 --dry-run | \
  jq -r '.[0].title' | xargs -I{} \
  node --env-file=.env openwebninja_universal_scraper/apis/realtime-image-search/scrape.js \
    --query "{}" --count 20 --format csv
```

Takes the top web search result title and finds matching images for visual content research.
