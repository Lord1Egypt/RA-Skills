# realtime-books-data Recipes

## 1. Search for thrillers and export as CSV

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-books-data/scrape.js \
  --query "good thriller" --count 50 --format csv
```

Fetches up to 50 thriller books with title, author, description, and publication info.

## 2. Recent books only (published since 2023)

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-books-data/scrape.js \
  --query "machine learning" --year-from 2023 --count 30 --format json
```

Finds machine learning books published from 2023 onward, useful for curating up-to-date reading lists.

## 3. Full-view books only (dry run)

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-books-data/scrape.js \
  --query "classic literature" --view-type full_view --dry-run
```

Searches for classic literature books that have full preview available, printed to console.

## 4. Search for magazines in Spanish

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-books-data/scrape.js \
  --query "cocina" --document-type magazines --language es --country es --count 20 --format json
```

Finds Spanish-language cooking magazines available on Google Books.

## 5. Cross-API: find books then search for author news

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-books-data/scrape.js \
  --query "science fiction 2025" --count 3 --dry-run | \
  jq -r '.[0].authors[0]' | xargs -I{} \
  node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
    --query "{} interview 2025" --count 10 --dry-run
```

Finds top sci-fi books, then searches the web for recent interviews with the top author.
