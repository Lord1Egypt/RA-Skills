# ev-charge-finder — Recipes

## 1. Find EV chargers near a city

```bash
node --env-file=.env openwebninja_universal_scraper/apis/ev-charge-finder/scrape.js \
  --location "San Francisco, CA, USA" --count 50 --format json
```

Exports up to 50 EV charging stations near San Francisco as JSON.

## 2. Filter by connector type (CHAdeMO)

```bash
node --env-file=.env openwebninja_universal_scraper/apis/ev-charge-finder/scrape.js \
  --location "Los Angeles, CA, USA" --connector-type CHAdeMO --count 30 --format csv
```

Finds CHAdeMO-compatible chargers near LA and exports as CSV.

## 3. Search by exact coordinates

```bash
node --env-file=.env openwebninja_universal_scraper/apis/ev-charge-finder/scrape.js \
  --lat 37.359428 --lng -121.925337 --count 20 --format json
```

Finds the 20 nearest stations to exact GPS coordinates (e.g. Sunnyvale).

## 4. High-power chargers only

```bash
node --env-file=.env openwebninja_universal_scraper/apis/ev-charge-finder/scrape.js \
  --location "Seattle, WA, USA" --min-kw 50 --available --count 20 --format json
```

Finds available chargers with at least 50 kW power near Seattle.

## 5. Chain: find EV chargers along a driving route

```bash
# Step 1 — get the route
node --env-file=.env openwebninja_universal_scraper/apis/driving-directions/scrape.js \
  --origin "San Francisco, CA, USA" --destination "Los Angeles, CA, USA" --format json --output output/route_sf_la.json

# Step 2 — find chargers near the midpoint (Paso Robles)
node --env-file=.env openwebninja_universal_scraper/apis/ev-charge-finder/scrape.js \
  --location "Paso Robles, CA, USA" --min-kw 50 --count 10 --format json --output output/chargers_midpoint.json
```

Gets driving directions SF to LA, then finds fast chargers near the midpoint for a road-trip charging stop.
