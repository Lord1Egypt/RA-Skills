---
name: scraping-api-pricing
description: Compare web scraping API, SERP API and headless browser plans by monthly cost and conditions. Use when the user asks which scraping, crawling, search results (SERP), proxy or browser API plan fits a workload or a budget, for example "cheapest plan for 100k JavaScript pages a month", "SERP API for 20k Google searches in Germany under $100", "are failed requests billed", "compare Firecrawl and ZenRows". Covers Firecrawl, ScrapingBee, ZenRows, Bright Data, Oxylabs, Zyte, Scrapfly, ScrapingAnt, Scrapingdog, SerpApi, Serper, DataForSEO, SearchCans, Brave Search API, Tavily, Apify and Spider. Each answer carries the sentence from the official pricing page and its check date; a term the page does not state is reported as unknown, not guessed.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    homepage: https://plans.intoperson.com
---

# Scraping API pricing

This skill answers plan and price questions about web data APIs with the public
Web Data API Plan Finder service (https://plans.intoperson.com). It needs no key
and no account. Every request below is a plain HTTPS call.

## When to use

- The user needs a scraping, crawling, SERP, proxy or headless browser API and
  asks which plan fits a monthly volume, a budget or a billing rule.
- The user names plans and asks whether they meet a condition.
- The user asks how the cost changes when the workload grows.

Do not answer these from memory. Prices and terms change, and the service
records each fact with its source sentence and the date it was checked.

## Steps

1. Turn the request into conditions. Ask only for what changes the answer:
   pages per month by type (`plain_html`, `javascript`, `premium_proxy`,
   `javascript_premium_proxy`), or `monthly_pages_total` if the split is not
   known; `monthly_searches` for SERP; `max_monthly_cost_usd`; and any must-have
   rule such as `failed_requests_not_billed`, `search_engines`,
   `search_countries` (ISO alpha-2, e.g. `"DE"`) or `search_result_types`.
2. Search:

   ```bash
   curl -s -X POST https://plans.intoperson.com/api/v1/search \
     -H "Content-Type: application/json" \
     -d '{"monthly_searches":20000,"search_engines":["google"],"search_countries":["US"],"max_monthly_cost_usd":100}'
   ```

   ```bash
   curl -s -X POST https://plans.intoperson.com/api/v1/search \
     -H "Content-Type: application/json" \
     -d '{"monthly_pages":{"javascript":50000},"max_monthly_cost_usd":200}'
   ```

   On Windows PowerShell call `curl.exe`, not `curl`.
3. Read the result:
   - `full_matches` meet every required condition. `partial_matches` have
     conditions listed in `unmet_conditions` or `unknown_conditions`.
   - `monthly_cost.explanation` shows how the cost was computed. A cost can be
     a range (`low`, `high`) when the price depends on the target site.
   - Each fact has `evidence` (official page URL and quoted sentence) and
     `checked_at`.
4. If nothing fits, ask which conditions can change and call `/api/v1/relax`
   with the same body plus `"negotiable": [...]` (for example
   `"monthly_budget"`, `"billing_type"`, `"serp_engines"`). It returns the
   smallest changes that admit a plan.
5. Other calls, all with the same condition fields:
   - `POST /api/v1/check` with `"offer_ids": [...]` or
     `"plans": ["ScrapingBee Freelance"]` checks named plans.
   - `POST /api/v1/scenarios` with `"scale": 2` or a `"target"` workload
     shows plan costs as the workload grows.
   - `GET /api/v1/offers/{offer_id}` and `GET /api/v1/products/{product_id}`
     return every recorded fact of a plan or product.
   - Full schema: https://plans.intoperson.com/api/v1/openapi.json

## How to report

- Lead with the plans that meet every condition, their monthly cost and the
  cost explanation.
- For each claim you pass on, give the quoted sentence, the page URL and the
  check date from the response.
- When a condition is `UNKNOWN`, say the official page does not state it. Do
  not fill it in from general knowledge.
- For a follow-up question about one product (for example "do unused credits
  roll over?"), read its terms with `GET /api/v1/products/{product_id}` and
  answer from the matching fact. The service records prices, included units,
  overage, rollover, concurrency, rate limits, timeouts, rendering, proxies,
  geo targeting, SERP engines, countries and result types, crawl limits,
  failed-request billing, free allowances, tax and commitments. For anything
  else (refunds, SLA, terms of use, data retention), say the service does not
  record it and point to the provider's page.
- Say that prices exclude tax and that the user should confirm the final price
  and account limits with the seller before buying. Order is by monthly cost.

## MCP server (optional)

The same service is an MCP server with the tools `search`,
`check_conditions`, `cost_scenarios`, `relax_conditions` and `get_details`:

```bash
claude mcp add --transport http web-data-plan-finder https://plans.intoperson.com/mcp
```

Other clients: add the streamable HTTP URL `https://plans.intoperson.com/mcp`.
