# realtime-events-search Recipes

## 1. Search for upcoming concerts in a city

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-events-search/scrape.js \
  --query "Concerts in San Francisco" --count 50 --format csv
```

Fetches up to 50 concert events with name, date, venue, and description, exported as CSV.

## 2. This week's events (dry run)

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-events-search/scrape.js \
  --query "tech meetups New York" --date week --dry-run
```

Quickly previews tech meetups happening this week in New York without saving to disk.

## 3. Virtual events only

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-events-search/scrape.js \
  --query "AI conference" --is-virtual true --count 20 --format json
```

Finds online-only AI conferences, useful for building a remote events calendar.

## 4. Get full details for a specific event

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-events-search/scrape.js \
  --endpoint /event-details \
  --event-id "L2F1dGhvcml0eS9ob3Jpem9uL2NsdXN0ZXJlZF9ldmVudC8yMDI0LTExLTIyfDE2OTA0Nzc5MjUwNzQwODY5OTc4" \
  --dry-run
```

Fetches complete details (description, tickets, venue info) for a single event by its ID.

## 5. Cross-API: find events then search the web for reviews

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-events-search/scrape.js \
  --query "food festival Los Angeles" --date month --count 3 --dry-run | \
  jq -r '.[0].name' | xargs -I{} \
  node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
    --query "{} reviews" --count 10 --dry-run
```

Finds upcoming food festivals, then searches the web for reviews of the top result.
