# Wayback Machine & Internet Archive — Full Reference

## CDX API — Snapshot Search

Base URL: `https://web.archive.org/cdx/search/cdx`

### Parameters

| Param | Description |
|-------|-------------|
| `url` | Target URL (supports `*` wildcards: `example.com/*`) |
| `output` | `json` or `text` |
| `fl` | Fields: `timestamp`, `original`, `mimetype`, `statuscode`, `digest`, `length` |
| `filter` | e.g. `statuscode:200`, `mimetype:text/html` |
| `from` / `to` | Date range `YYYYMMDD` |
| `limit` | Max results |
| `collapse` | Deduplicate: `timestamp:4` = one/year, `timestamp:6` = one/month |
| `showNumPages=true` | Return total snapshot count |

### Common Queries

```bash
# All 200-OK snapshots of a URL
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&filter=statuscode:200&fl=timestamp,original"

# One snapshot per year (change tracking)
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&collapse=timestamp:4&fl=timestamp,statuscode&filter=statuscode:200"

# One snapshot per month in a date range
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&from=20230101&to=20231231&collapse=timestamp:6&fl=timestamp"

# All pages under a domain
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com/*&output=json&filter=statuscode:200&fl=timestamp,original&limit=100"

# Count total snapshots
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&showNumPages=true"

# Check if a URL has ever been archived
curl -s "https://archive.org/wayback/available?url=example.com" | python3 -m json.tool
```

## Fetching Archived Content

Wayback URL format: `https://web.archive.org/web/{TIMESTAMP}/{ORIGINAL_URL}`

```bash
# Read via web_fetch (clean text)
# web_fetch: https://web.archive.org/web/20230601/https://example.com/

# Scrape archived version with Scrapling
scrapling extract get "https://web.archive.org/web/20230601000000/https://example.com/" archive.md

# Most recent snapshot
curl -s "https://archive.org/wayback/available?url=example.com" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['archived_snapshots']['closest']['url'])"
```

## `ia` CLI — Internet Archive Items

Works on archive.org **items** (books, video, audio, software). Different from Wayback snapshots.

```bash
# Search
ia search 'subject:"bitcoin" mediatype:texts' --itemlist

# Get metadata
ia metadata <identifier>
ia metadata <identifier> | jq '.metadata | {title, date, description}'

# List files
ia list <identifier>

# Download
ia download <identifier>                          # entire item
ia download <identifier> <filename>              # specific file
ia download <identifier> --glob="*.pdf"          # by pattern
ia download <identifier> --format='Text PDF'     # by format

# Dry run
ia download <identifier> --dry-run
```

Authenticate (needed for upload/modify):
```bash
ia configure   # prompts for archive.org email + password
```

## Timestamps

CDX timestamps are UTC in format `YYYYMMDDHHMMSS`.

```python
# Parse timestamp
from datetime import datetime
ts = "20230601120000"
dt = datetime.strptime(ts, "%Y%m%d%H%M%S")
```
