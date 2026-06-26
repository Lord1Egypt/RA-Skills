# waze recipes

## 1. Get NYC traffic alerts and jams

```bash
node --env-file=.env openwebninja_universal_scraper/apis/waze/scrape.js \
  --bbox "40.666,-74.137|40.772,-73.768" --max-alerts 50 --max-jams 50
```

Fetches up to 50 alerts and 50 jams in the NYC area, saved as JSON with alert/jam type tags.

## 2. Driving directions between two cities

```bash
node --env-file=.env openwebninja_universal_scraper/apis/waze/scrape.js \
  --endpoint /driving-directions --source "32.0852999,34.7817676" --destination "32.7940463,34.989571" \
  --return-coords --format json
```

Gets Waze driving directions with route coordinates between Tel Aviv and Haifa.

## 3. Find venues near the Eiffel Tower

```bash
node --env-file=.env openwebninja_universal_scraper/apis/waze/scrape.js \
  --endpoint /venues --bbox "48.851,2.334|48.853,2.354" --format csv
```

Exports all venues in a small bounding box around the Eiffel Tower as CSV.

## 4. Autocomplete place search

```bash
node --env-file=.env openwebninja_universal_scraper/apis/waze/scrape.js \
  --endpoint /autocomplete --query "sunn" --coordinates "37.376754,-122.023350" --dry-run
```

Previews autocomplete suggestions for "sunn" biased to Sunnyvale, CA coordinates.

## 5. Multi-API: traffic alerts near local businesses

```bash
# Step 1: Find coffee shops in Brooklyn
node --env-file=.env openwebninja_universal_scraper/apis/local-business-data/scrape.js \
  --query "coffee shop Brooklyn NY" --count 20 --output output/brooklyn_coffee.json

# Step 2: Get traffic alerts for the Brooklyn area
node --env-file=.env openwebninja_universal_scraper/apis/waze/scrape.js \
  --bbox "40.630,-74.042|40.694,-73.855" --max-alerts 30 --output output/brooklyn_traffic.json
```

Cross-references coffee shop locations with current traffic conditions in Brooklyn.
