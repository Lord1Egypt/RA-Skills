# local-rank-tracker Recipes

## 1. Find a business location by name

```bash
node --env-file=.env openwebninja_universal_scraper/apis/local-rank-tracker/scrape.js \
  --query "Jives Media" --near "California, USA" --format json
```

Searches for Google My Business locations matching the query, returning place IDs, coordinates, and addresses.

## 2. Check local search results at a specific coordinate

```bash
node --env-file=.env openwebninja_universal_scraper/apis/local-rank-tracker/scrape.js \
  --endpoint /search --query "web design" --lat 37.341759 --lng -121.938314 --format csv
```

Gets all local search results at the given coordinate, useful for seeing who ranks for a keyword in a specific area.

## 3. Track a business ranking at a coordinate

```bash
node --env-file=.env openwebninja_universal_scraper/apis/local-rank-tracker/scrape.js \
  --endpoint /ranking-at-coordinate \
  --place-id ChIJ0zS4SOvLj4AR1obZVVeLFM0 \
  --query "web design" --lat 37.341759 --lng -121.938314 --dry-run
```

Checks the rank of a specific business for a keyword at a given location, printed to console for quick review.

## 4. Run a full grid search for local rank heatmap

```bash
node --env-file=.env openwebninja_universal_scraper/apis/local-rank-tracker/scrape.js \
  --endpoint /grid \
  --place-id ChIJoejvAr3Mj4ARtHrbKxtAHXI \
  --query "web design" --lat 37.341759 --lng -121.938314 \
  --grid-size 5 --radius 3 --radius-units km --format json
```

Performs a 5x5 grid search across a 3km radius, generating rank data at 25 coordinate points for heatmap visualization.

## 5. Cross-API: find a business then check its local rank

```bash
node --env-file=.env openwebninja_universal_scraper/apis/local-rank-tracker/scrape.js \
  --query "Starbucks" --near "San Jose, CA" --dry-run | \
  jq -r '.[0].place_id' | xargs -I{} \
  node --env-file=.env openwebninja_universal_scraper/apis/local-rank-tracker/scrape.js \
    --endpoint /grid --place-id {} \
    --query "coffee shop" --lat 37.3382 --lng -121.8863 \
    --grid-size 3 --radius 2 --format json
```

Finds a business place ID, then runs a grid search to map its local ranking across the surrounding area.
