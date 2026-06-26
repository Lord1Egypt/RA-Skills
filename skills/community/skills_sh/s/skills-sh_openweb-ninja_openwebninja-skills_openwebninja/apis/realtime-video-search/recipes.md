# realtime-video-search Recipes

## 1. Search for tutorial videos (quick answer)

```bash
node --env-file=.env apis/realtime-video-search/scrape.js \
  --query "react tutorial" --count 20 --dry-run
```

Fetches the first page of Google Videos results for "react tutorial" and prints
the top results to the console. Use `--dry-run` to verify the API is returning
data before a full run.

## 2. Recent product demo videos, sorted by date

```bash
node --env-file=.env apis/realtime-video-search/scrape.js \
  --query "product demo software" --time-period last_month --sort-by date \
  --count 50 --format json --output output/demos.json
```

Pulls videos published in the last month, newest first, and saves them to a JSON
file. Note: `--time-period` cannot be combined with `--date-from`/`--date-to`.

## 3. Short highlight clips for a custom date range

```bash
node --env-file=.env apis/realtime-video-search/scrape.js \
  --query "lebron james highlights" --duration short \
  --date-from "01/01/2026" --date-to "04/29/2026" \
  --count 30 --format csv --output output/highlights.csv
```

Finds short videos (under 4 minutes) published between Jan 1 and Apr 29, 2026,
and exports them to CSV. `--date-from` and `--date-to` must be supplied together
in MM/DD/YYYY format.

## 4. Localized video search with safe search on

```bash
node --env-file=.env apis/realtime-video-search/scrape.js \
  --query "cómo invertir" --country es --language es --safe active \
  --count 40 --dry-run
```

Searches Spanish-language video results targeted to Spain with explicit content
filtered out.
