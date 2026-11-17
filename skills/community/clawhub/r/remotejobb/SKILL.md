---
name: remotejobb
description: Search open jobs in Sweden with the Remotejobb connector. Use when the user is looking for a job, wants to see open positions, asks about jobs in a Swedish city, category or company, asks which companies are hiring, wants remote or hybrid work, or writes in Swedish about "lediga jobb", "söka jobb" or "jobba hemifrån".
version: 1.1.0
metadata:
  openclaw:
    homepage: https://remotejobb.se/en/ai
---

# Search jobs on Remotejobb

Use the Remotejobb connector's tools: `search_jobs`, `get_job`, `list_companies` and `list_search_filters`.

## Setup

This skill uses the Remotejobb MCP server at `https://remotejobb.se/mcp` (Streamable HTTP, read-only, no account or API key). If its tools are not available, add the server once:

```bash
openclaw mcp add remotejobb --url https://remotejobb.se/mcp --transport streamable-http
```

More about the server: https://remotejobb.se/en/ai

## 1. Understand the request

- Pick out role or keywords, city, category, company, employment type, remote or hybrid, where the user lives, salary, the language of the ad and how recent the jobs should be.
- Search right away when the request has enough to go on. Ask one short question only when it is too vague to search at all.
- Answer in the user's language. Use `language: "sv"` for Swedish-speaking users so labels come back in Swedish.

## 2. Map the request to filters

- Most filters take one value or a list. Values in one list mean "any of these" (`city: ["Stockholm", "Uppsala"]`), and different filters must all match.
- `city` and `company` take plain names; the server matches them loosely, so "Göteborg", "goteborg" and "Gothenburg" all work, and "spotify" finds "Spotify AB". `category` takes a name or a slug. Call `list_search_filters` when you need the valid categories or the cities that have jobs.
- `work_mode`: `remote` for fully remote, `hybrid` for partly on site. Leave it out when the user doesn't care.
- `remote_scope` is where the applicant may live. It also matches more open scopes, so `sweden` includes jobs open to all of Europe or worldwide.
- `ad_language`: `sv` or `en` for the language the ad is written in, for example when the user only wants jobs in English.
- `salary_only: true` keeps jobs that state a salary. `min_monthly_salary_sek` only matches jobs that state a salary in SEK; tell the user that jobs without a stated salary are excluded.
- `posted_within_days` for "this week" (7) or "today" (1).
- Put the role in `query` with short keywords (for example `utvecklare`, `kundtjänst`, `python`). Every word must match, so keep it to one or two words.
- `order`: `relevance` (the default with keywords), `published_at` (newest first, the default otherwise), `apply_by` (closest application deadline first) or `salary` (highest first).

## 3. Show results

- List the jobs compactly: title, company, location or work mode, employment type, salary if stated, deadline if relevant, and the link to the listing.
- Say how many jobs matched in total, and offer the next page when `has_more` is true.
- The response's `facets` show how the results split by city, category, company, employment type and more. Use them to suggest how to narrow a large result, or to answer "where are most of these jobs?".
- If `matched_companies` lists several companies, ask which one the user means when it matters.
- If nothing matches, loosen one filter at a time (salary, date, city, then keywords), say which one you loosened, and search again.

## 4. Open jobs

- Use `get_job` with `ids` when the user wants details, requirements or the apply link. Pass up to five ids to compare jobs side by side.
- Set `with_similar: true` when the user asks for similar or related jobs.
- Summarize the description in the user's language and give `apply_url` as the way to apply.
- If `is_excerpt_only` is true, say that only an excerpt is available and link to the original listing.
- If `apply_method` is `email`, the apply link leads to the job page on Remotejobb.se, where the application details are.

## 5. Companies

- Use `list_companies` for questions about employers: "which companies are hiring?", "is Klarna hiring?". It lists hiring companies by default with their number of open jobs; pass `name` to look one up.
- To see a company's jobs, pass its name or slug as `company` to `search_jobs`.

## Limits

- The connector is read-only. You cannot apply, save jobs or contact employers on the user's behalf. Give the apply link instead.
- Listings change daily. Don't present a job as still open without checking it with `get_job` when the user asks again later.
