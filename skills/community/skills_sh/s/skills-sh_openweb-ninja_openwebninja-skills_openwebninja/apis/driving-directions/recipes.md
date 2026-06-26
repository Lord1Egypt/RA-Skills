# driving-directions — Recipes

## 1. Basic driving directions

```bash
node --env-file=.env openwebninja_universal_scraper/apis/driving-directions/scrape.js \
  --origin "Church St & 29th St, San Francisco, CA, USA" \
  --destination "Sunnyvale, CA, USA" --format json
```

Gets driving directions from SF to Sunnyvale with distance, duration, and turn-by-turn steps.

## 2. Directions in miles with toll avoidance

```bash
node --env-file=.env openwebninja_universal_scraper/apis/driving-directions/scrape.js \
  --origin "New York, NY, USA" --destination "Boston, MA, USA" \
  --distance-units mi --avoid tolls --format json
```

Gets NY-to-Boston directions in miles while avoiding toll roads.

## 3. Export route as CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/driving-directions/scrape.js \
  --origin "Los Angeles, CA, USA" --destination "Las Vegas, NV, USA" \
  --format csv --output output/la_vegas_route.csv
```

Exports the LA-to-Vegas route data as a flat CSV file.

## 4. Dry-run to preview response

```bash
node --env-file=.env openwebninja_universal_scraper/apis/driving-directions/scrape.js \
  --origin "Seattle, WA, USA" --destination "Portland, OR, USA" --dry-run
```

Prints the raw route JSON to the console without writing a file.

## 5. Chain: get directions then find businesses along the route

```bash
# Step 1 — get the route
node --env-file=.env openwebninja_universal_scraper/apis/driving-directions/scrape.js \
  --origin "San Francisco, CA, USA" --destination "Los Angeles, CA, USA" \
  --format json --output output/route_sf_la.json

# Step 2 — find hotels near a waypoint along the route
node --env-file=.env openwebninja_universal_scraper/apis/local-business-data/scrape.js \
  --query "Hotels in Paso Robles, CA" --count 20 --format json --output output/hotels_paso_robles.json
```

Gets the SF-to-LA route, then searches for hotels near a midpoint stop using the Local Business Data API.
