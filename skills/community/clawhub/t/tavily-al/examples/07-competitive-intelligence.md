# Example 07 — Competitive Intelligence

Research competitors using domain filters, extract their pricing/feature pages, and produce a structured comparison with sources.

## User request

> "Compare the pricing and key features of three project-management tools: Acme PM, Globex Tasks, and Initech Plan. Use their official sites."

## Agent reasoning summary

- The user named three competitors and wants official-site data, so I will scope searches to each vendor's domain.
- Pricing and feature details live on specific pages; I will find those pages via domain-filtered search, then extract them for accuracy.
- I will present a side-by-side comparison with a source per cell/vendor.

## Tavily operation to use

Use **search** with `include_domains` (one vendor domain at a time, or a combined list) to locate each vendor's pricing/features page, then **extract** those pages for precise, current details.
Why: domain filtering keeps results on official sources (avoiding third-party reviews), and extract reads the actual pricing tables rather than relying on snippets that often omit numbers.

## Request shape

Locate pages (repeat per vendor, or combine domains):

```json
{
  "query": "pricing plans features",
  "include_domains": ["acmepm.com"],
  "search_depth": "advanced",
  "max_results": 5
}
```
```json
{
  "query": "pricing plans features",
  "include_domains": ["globextasks.com"],
  "search_depth": "advanced",
  "max_results": 5
}
```
```json
{
  "query": "pricing plans features",
  "include_domains": ["initechplan.com"],
  "search_depth": "advanced",
  "max_results": 5
}
```

Extract the identified pricing/feature pages:

```json
{
  "urls": [
    "https://acmepm.com/pricing",
    "https://globextasks.com/pricing",
    "https://initechplan.com/pricing"
  ],
  "extract_depth": "advanced"
}
```

> Verification needed: confirm `include_domains` (and `exclude_domains`) parameter names and behavior at https://docs.tavily.com

## Response handling

1. For each vendor search, sort by `score`, filter `score >= 0.5`, and pick the most likely pricing/features URL on that vendor's own domain.
2. Confirm each chosen URL's host matches the intended vendor domain (guards against off-domain leakage).
3. Extract the three pricing pages; read `raw_content`; note any `failed_results`.
4. Pull comparable fields per vendor: starting price, billing unit (per user/month), notable tier limits, and 3-5 headline features — only what appears in the extracted text.
5. Normalize into a comparison table; leave a cell blank or "not stated" if the page does not list it (do not guess).

## Citation behavior

- Each vendor's row cites that vendor's extracted page URL.
- Pricing figures are cited to the exact pricing page they came from, with an "as of" date because prices change.
- If a field was unavailable, the cell says "not stated on page" rather than borrowing a number from memory or a third-party site.

## Final answer pattern

```
Comparison of project-management tools (from official sites, as of 2026-05-31):

| Tool          | Starting price        | Billing       | Headline features                        | Source |
|---------------|-----------------------|---------------|-------------------------------------------|--------|
| Acme PM       | $9 / user / month     | per user/mo   | Kanban, Gantt, time tracking              | [1]    |
| Globex Tasks  | $7 / user / month     | per user/mo   | Lists, automations, calendar              | [2]    |
| Initech Plan  | Free tier; $12 Pro    | per user/mo   | Roadmaps, dependencies, dashboards        | [3]    |

Notes: Initech's enterprise price is not stated on the public page.

Sources:
[1] Acme PM Pricing — https://acmepm.com/pricing
[2] Globex Tasks Pricing — https://globextasks.com/pricing
[3] Initech Plan Pricing — https://initechplan.com/pricing
```

## Common failure mode

Searching without `include_domains`, so the comparison gets built from third-party blog posts and outdated review sites — leading to stale or wrong prices. Or filling in missing cells from memory, presenting guesses as fact.

## Improved version

- Scope discovery with `include_domains` per vendor; verify the chosen URL's host.
- Extract official pricing pages and read figures from `raw_content`.
- Use "not stated on page" for missing data; add an "as of" date for all prices.
- Cite each vendor's own page per row.

```json
{
  "query": "pricing plans features",
  "include_domains": ["acmepm.com"],
  "search_depth": "advanced",
  "max_results": 5
}
```
