# play-store-apps Recipes

## 1. Search for apps and export results

```bash
node --env-file=.env openwebninja_universal_scraper/apis/play-store-apps/scrape.js \
  --query "fitness tracker" --count 100 --format csv
```

Searches the Play Store for fitness tracker apps with cursor-based pagination, exporting up to 100 results.

## 2. Export all reviews for a specific app

```bash
node --env-file=.env openwebninja_universal_scraper/apis/play-store-apps/scrape.js \
  --endpoint /app-reviews --app-id com.snapchat.android --count 200 --sort-by NEWEST --format csv
```

Fetches the 200 newest reviews for Snapchat, auto-paginating through cursor pages. Great for sentiment analysis.

## 3. Get full details for multiple apps at once

```bash
node --env-file=.env openwebninja_universal_scraper/apis/play-store-apps/scrape.js \
  --endpoint /app-details --app-id "com.whatsapp,com.instagram.android,com.snapchat.android" --format json
```

Batch-fetches details for up to 100 apps in a single call, including ratings, downloads, and developer info.

## 4. Export the top free apps chart for a category

```bash
node --env-file=.env openwebninja_universal_scraper/apis/play-store-apps/scrape.js \
  --endpoint /top-free-apps --category SOCIAL --count 50 --format csv
```

Gets the top 50 free social apps, useful for competitive landscape analysis.

## 5. Cross-API: find an app then search for web reviews

```bash
node --env-file=.env openwebninja_universal_scraper/apis/play-store-apps/scrape.js \
  --endpoint /app-details --app-id com.spotify.music --dry-run | \
  jq -r '.[0].app_name' | xargs -I{} \
  node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
    --query "{} app review 2025" --count 20 --format csv
```

Gets an app name from Play Store details, then searches the web for third-party reviews of that app.
