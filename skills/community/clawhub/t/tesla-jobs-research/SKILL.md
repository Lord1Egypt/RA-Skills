---
name: tesla-jobs-research
description: Researches Tesla job postings via the Crawlora API — search Tesla's careers site (tesla.com/careers) by title, department, or location, and pull a single posting's full description by id — returning clean JSON. Use when the user wants to search Tesla job openings, see what Tesla is hiring for in a location, or pull the full detail of a specific Tesla posting.
---

# Tesla Jobs search

Search Tesla's public careers site and pull full posting detail — all as
normalized JSON from the Crawlora API, no scraping tesla.com/careers by hand.

## When to use this skill

- "Search for <role> jobs at Tesla." / "What is Tesla hiring for in <location>?"
- "Show me all Tesla openings in the <department> department."
- "Get the full description/requirements for Tesla job id <id>."
- "Is Tesla scaling up hiring in <location>?" — page through the listing.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **List postings** — `/tesla-jobs/list` searches Tesla's careers-state JSON
   snapshot. Filter with `query` (title/department substring) and/or
   `location` (substring), and page through results with `page` and
   `page_size`. Tesla's own upstream endpoint always returns its entire
   global job dataset regardless of query — this endpoint filters and
   paginates that snapshot server-side, so listings carry identity/
   department/location metadata only (no full description yet).
2. **Job detail** — take the numeric `id` field from a list result and pass
   it to `/tesla-jobs/job` to get the full posting: description,
   responsibilities, and requirements.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search Tesla openings by title/department and location:
scripts/crawlora.sh /tesla-jobs/list query="software engineer" location="Austin" | jq '.'

# Pull the full detail for one posting (id from the list response):
scripts/crawlora.sh /tesla-jobs/job id=204536 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for both Tesla Jobs
endpoints this skill uses.

## Examples

- **"What is Tesla hiring for in Berlin?"** — `/tesla-jobs/list`
  `location="Berlin"`, then `/tesla-jobs/job` on the ids of interest for
  full requirements.
- **"Show me every Tesla data engineering role."** — `/tesla-jobs/list`
  `query="data engineer"`, walking `page`/`page_size` until the response is
  short of a full page.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public postings; respect Tesla's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **`query`/`location` are substring filters, not full-text/geo search** — a
  narrow term (e.g. a city abbreviation) may miss postings; try broader
  substrings if a search returns nothing.
- **List results are metadata-only** — always follow up with `/tesla-jobs/job`
  for the full description, responsibilities, and requirements.
- Results are paginated — pass `page` (and optionally `page_size`, up to 100)
  to walk the full list.
