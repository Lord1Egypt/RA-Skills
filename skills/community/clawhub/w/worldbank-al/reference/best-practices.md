# Reference · Best Practices

Imperative best practices for using World Bank Open Data well. **The API is open
— no API key.**

---

## Discovery

- **Search before fetching** when the indicator concept is at all ambiguous. Use
  `worldbank_search_indicators` and pick the `{ id, name }` that truly matches.
- **Confirm units/definition** with `worldbank_indicator_metadata` before
  reporting a figure (e.g. current vs. constant US$, annual % vs. level).
- **Browse by theme** with `worldbank_topics` when exploring.

## Country & date selection

- Prefer **ISO3** codes (`USA`) for clarity.
- Use a **single multi-country call** (`USA;CHN;IND`) instead of many calls.
- Use **`mrv: N`** for "the latest" and a **`date` range** for trends.
- Distinguish **aggregates** (`WLD`, `EUU`, income groups) from countries and
  label them as groups.

## Citation

- **Always cite.** Free and open still requires attribution.
- Format: **World Bank, <indicator name> (<code>), <country>, <year>.** +
  `https://data.worldbank.org/indicator/<code>`.
- Include the **year(s)** so the figure is verifiable.

## Caching

- Cache `worldbank_indicator_data` by `country + indicator + date/mrv`.
- Cache static lookups (topics, country list, sources, income levels) hard.
- Use `lastupdated` (from pagination meta via `worldbank_request`) to refresh.
- Caching keeps you polite on the free API and avoids HTTP 429.

## Integrity

- **Never invent numbers.** `null` means missing; report it as such, never `0`.
- Pair every figure with its **unit**.
- Do not present output as financial/economic advice.

## No-key note

- The API is **open**: `"env": {}`. Do not add `WORLDBANK_API_KEY`.
- Only optional tuning vars exist (`WORLDBANK_TIMEOUT_MS`,
  `WORLDBANK_MAX_RETRIES`, `WORLDBANK_API_BASE_URL`, `LOG_LEVEL`).

## Performance

- Keep `per_page` modest; paginate rather than requesting huge pages.
- Avoid tight retry loops; let the server's backoff handle 429/5xx.

> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
