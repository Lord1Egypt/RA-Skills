# Setup — Ticketmaster Discovery API

## Get an API key

1. Create or sign in to a Ticketmaster Developer account.
2. Generate an API key for the Discovery API product.
3. Keep the key in an environment variable instead of hardcoding it in commands or files.

```bash
export TM_API_KEY="your-ticketmaster-key"
```

## Create local working memory

```bash
mkdir -p ~/ticketmaster/logs
cp /path/to/installed/ticketmaster/memory-template.md ~/ticketmaster/memory.md
touch ~/ticketmaster/queries.md
```

If the skill is already installed locally, copy the structure from `memory-template.md` into `~/ticketmaster/memory.md`.

## Smoke test the API

```bash
curl --get "https://app.ticketmaster.com/discovery/v2/events.json" \
  --data-urlencode "apikey=$TM_API_KEY" \
  --data-urlencode "keyword=metallica" \
  --data-urlencode "size=1"
```

Expected result: JSON with `_embedded.events` or an empty but valid search result.

## Smoke test the helper

```bash
chmod +x /path/to/installed/ticketmaster/ticketmaster.sh
/path/to/installed/ticketmaster/ticketmaster.sh events "metallica" --size 1
```

If `jq` is installed, output is pretty-printed. Otherwise the helper prints raw JSON.

## Suggested first defaults

Add these to `~/ticketmaster/memory.md` after the first successful request:
- default locale
- default country or market
- common city filters
- common sort order
- event IDs or venue IDs you revisit often

## Troubleshooting

### 401 or auth-style failures
- Re-export `TM_API_KEY`
- Confirm the key belongs to the same Ticketmaster developer account you expect

### Empty result set
- Remove one filter at a time
- Try `locale=*`
- Test the same keyword with only `countryCode` and `size=1`

### Too many results
- Add `city`, `dmaId`, `marketId`, `venueId`, or `classificationName`
- Keep paging shallow and narrow the query instead
