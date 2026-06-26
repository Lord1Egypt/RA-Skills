---
name: readarr
description: Interact with Readarr (ebook/audiobook manager) via its REST API. Use when searching for books, monitoring authors for new releases, checking what's missing or wanted, triggering downloads, or managing the book library. Works alongside Calibre — Readarr acquires, Calibre organises.
---

# Readarr Skill

Readarr is the *arr-suite manager for ebooks and audiobooks. It monitors authors, finds releases via indexers (Prowlarr), sends them to a download client, and drops them into the Calibre library.

## Connection

Readarr runs as `/Applications/Readarr.app` on Dozo. Already configured and running.

```bash
READARR_URL="http://localhost:8787"
READARR_KEY=$(cat /path/to/readarr_api_key)
```

See `references/api.md` for all endpoints.

## Core Workflows

### Find and add a book
```bash
# 1. Look up by title or ISBN
curl -s "$READARR_URL/api/v1/book/lookup?term=<title>" \
  -H "X-Api-Key: $READARR_KEY" | python3 -c "
import sys,json
books = json.load(sys.stdin)
for b in books[:5]:
    print(b.get('title'), '—', b.get('author',{}).get('authorName'), '| foreignBookId:', b.get('foreignBookId'))
"

# 2. Add it (need qualityProfileId + metadataProfileId from /api/v1/qualityprofile and /api/v1/metadataprofile)
curl -s -X POST "$READARR_URL/api/v1/book" \
  -H "X-Api-Key: $READARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"foreignBookId":"<id>","monitored":true,"author":{...},"qualityProfileId":1,"metadataProfileId":1,"rootFolderPath":"/path/to/books","addOptions":{"searchForNewBook":true}}'
```

### Monitor an author
```bash
# Look up author first
curl -s "$READARR_URL/api/v1/author/lookup?term=Iain+Banks" \
  -H "X-Api-Key: $READARR_KEY"

# Add author (monitors all future releases)
curl -s -X POST "$READARR_URL/api/v1/author" \
  -H "X-Api-Key: $READARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"foreignAuthorId":"<id>","monitored":true,"qualityProfileId":1,"metadataProfileId":1,"rootFolderPath":"/path/to/books","addOptions":{"monitor":"all","searchForMissingBooks":true}}'
```

### Check wanted/missing
```bash
curl -s "$READARR_URL/api/v1/wanted/missing?pageSize=20" \
  -H "X-Api-Key: $READARR_KEY" | python3 -c "
import sys,json
d = json.load(sys.stdin)
for b in d.get('records',[]):
    print(b['title'], '—', b.get('author',{}).get('authorName'))
"
```

### Trigger a search
```bash
curl -s -X POST "$READARR_URL/api/v1/command" \
  -H "X-Api-Key: $READARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"MissingBookSearch"}'
```

### Check download queue
```bash
curl -s "$READARR_URL/api/v1/queue" -H "X-Api-Key: $READARR_KEY" | python3 -c "
import sys,json
q = json.load(sys.stdin)
for item in q.get('records',[]):
    print(item.get('title'), '|', item.get('status'), '|', item.get('timeleft','?'))
"
```

## Calibre Integration
Readarr drops completed books into Calibre's watch folder. Lucien then runs:
```bash
calibredb add /path/to/new/book.epub --with-library /Volumes/Bull/calibre-library
```
Or configure Readarr's "Book Import" post-processing to point directly at the Calibre library path.

## Credentials
Store API key at `~/clawd/credentials/readarr_api_key` (single line, no newline).
Load with: `READARR_KEY=$(cat ~/clawd/credentials/readarr_api_key)`
