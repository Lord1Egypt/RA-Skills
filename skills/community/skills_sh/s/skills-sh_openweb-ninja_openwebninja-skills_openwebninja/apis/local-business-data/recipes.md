# local-business-data — Recipes

## 1. Lead list with contact info
```bash
node --env-file=.env apis/local-business-data/scrape.js \
  --query "Plumbers in Austin, TX" --count 200 --contacts --format csv
```
1 API call. Returns: name, address, phone, website, emails, social profiles.

## 2. Full city coverage by zip code
```bash
node --env-file=.env apis/local-business-data/scrape.js \
  --query "Dentists" --zips "90210,90211,90212,90213" --contacts --format csv
```
1 call per zip, deduplicates by business_id.

## 3. Filter by business category
```bash
node --env-file=.env apis/local-business-data/scrape.js \
  --query "Restaurants in Miami" --subtypes "Mexican restaurant" --format json
```
See `gmb_categories.json` for 4,039 available subtypes.

## 4. Business reviews
```bash
node --env-file=.env apis/local-business-data/scrape.js \
  --endpoint /business-reviews --business-id "0x89c259b5a9bd152b:0x31453e62a3be9f76" \
  --count 100 --sort-by newest --format json
```
Cursor-paginated, 20 reviews per call.

## 5. State-wide lead gen with grid search (Adam's use case)
```bash
node --env-file=.env apis/local-business-data/scrape.js \
  --query "plumbers" --grid --bbox "32.5,-124.5,42.0,-114.0" \
  --contacts --max-calls 300 --format csv --output output/ca_plumbers.csv
```
Tiles California into a grid of /search-in-area cells at zoom 10. Auto-subdivides dense areas (LA, SF) where results hit the 500 cap. Deduplicates by business_id. ~100-200 calls for full state coverage.

Common bounding boxes:
- California: `32.5,-124.5,42.0,-114.0`
- Texas: `25.8,-106.7,36.5,-93.5`
- New York state: `40.5,-79.8,45.0,-71.9`
- Florida: `24.5,-87.6,31.0,-80.0`

## 6. Multi-API: Lead gen + SEO rankings
```bash
# Step 1: Get local SEO rankings
node --env-file=.env apis/local-rank-tracker/scrape.js --query "car accident lawyer Houston" ...
# Step 2: Get competitor contact info
node --env-file=.env apis/local-business-data/scrape.js --query "car accident lawyer Houston" --contacts --format csv
```
