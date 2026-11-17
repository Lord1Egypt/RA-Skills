---
name: upwork-research
description: Researches Upwork job postings and freelancer profiles via the Crawlora API — search Upwork's public job listings by keyword, pull full detail on a specific job posting, or look up a freelancer's profile (rate, Job Success Score, ratings, feedback) — returning clean JSON. Use when the user wants to search Upwork jobs, read a specific Upwork job posting, or research an Upwork freelancer.
---

# Upwork research

Search Upwork job postings and pull freelancer profiles — all as
normalized JSON from the Crawlora API, no scraping Upwork's pages by hand.

## When to use this skill

- "Search Upwork for <skill/role> jobs." — free-text keyword search over
  public job listings.
- "Show me this Upwork job posting." — full detail (budget, description,
  client history) for one posting by id.
- "Look up this Upwork freelancer." — profile, hourly rate, Job Success
  Score, ratings, and recent client feedback by freelancer id.
- "What's the going rate for <skill> on Upwork?" — collect budgets across
  search results to estimate a market rate.
- "Vet this freelancer before hiring." — pull their profile and feedback
  history in one call.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Search** — `/upwork/search` takes a free-text keyword (`q`) and returns
   normalized job summaries (title, budget, experience level, duration,
   posted date, description snippet, skill tags), paginated via `page`.
2. **Job detail** — take an `id` from a search result and call
   `/upwork/job/{id}` for the full posting: description, employment type,
   budget (hourly range or fixed amount), location/remote type, experience
   level, duration, project type, proposal count, allowed applicant
   countries, and a summary of the posting client (member since, location,
   spend, hires, hours, industry, company size).
3. **Freelancer profile** — `/upwork/freelancer/{id}` returns a normalized
   profile: name, title, verification badge, overview, hourly rate, rating
   and review count, Job Success Score, location and local time, total
   jobs/hours worked, and recent client feedback (title, comment, date,
   client name, rating).

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search jobs by keyword:
scripts/crawlora.sh /upwork/search q="react developer" | jq '.'

# Job detail (id from a search result):
scripts/crawlora.sh /upwork/job/<job_id> | jq '.'

# Freelancer profile (id from a search result or a known profile):
scripts/crawlora.sh /upwork/freelancer/<freelancer_id> | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for all Upwork endpoints this skill uses.

## Examples

- **Freelance rate-check:** `/upwork/search` for a skill (e.g. `q="react developer"`),
  collect the `budget` field across results to estimate a market rate for
  that skill.
- **Freelancer due diligence:** `/upwork/search` or a known id to find a
  candidate, then `/upwork/freelancer/{id}` to check their Job Success
  Score, hourly rate, hours worked, and recent client feedback before
  reaching out.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public postings/profiles; respect Upwork's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Job and freelancer ids come from search results** — grab the `id` field
  from `/upwork/search` output rather than guessing one.
- Data is sourced from Upwork's own server-rendered pages via a real
  browser-rendering backend, so fields reflect exactly what's publicly
  visible on the page (no data behind Upwork's login wall).
- `/upwork/search` is paginated — pass `page` to walk past the first page
  of results.
