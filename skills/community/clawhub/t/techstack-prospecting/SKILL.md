---
name: techstack-prospecting
description: Find and qualify company websites by their detected technologies using Crawlora's tech-stack dataset and live website checks. Use for technology-based account lists, integration targeting, or qualifying an existing domain list.
---

# Tech-stack prospecting

Find websites matching a technology profile, then verify the most relevant
candidates. Detected software supports technical fit; it does not establish
budget, willingness to buy, or the identity of a decision-maker.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It uses `x-api-key` at `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for exact
filters and optional live-detection parameters.

## Workflow

1. Translate the brief into required technologies, acceptable alternatives,
   excluded technologies, company-fit criteria, and a target list size. If the
   user supplies domains, start with those rather than discovering a new list.
2. Use `/datasets/techstack/facets?facet=technology` to discover common exact
   labels, and `/datasets/techstack/search` for candidates. Facets return only
   the top 50 buckets, not a complete list of accepted technology names; observed
   `technology_names` in search/item results can supply other exact labels.
3. Use repeated query keys for Boolean filters: `technology` is AND, `any_of`
   is OR, and `not` excludes. Do not send a comma-joined string as a substitute.
   `q` is a domain substring search, not a search over company descriptions.
   Normally set `is_infrastructure=false`; add `reachable=true` when appropriate.
   `page_size` is at most 100 and `page * page_size` cannot exceed 10,000.
4. Fetch `/datasets/techstack/items/{domain}` for evidence, confidence,
   the returned freshness fields (`probed_at`, `run_date`, or `crawled_at` when
   present), and `run_id`. Keep a consistent run when comparing dataset
   counts. A 404 means the domain is absent from the index, not that it lacks
   the technology; a live check can still answer the user's question.
5. Refresh selected candidates using `POST /web/techstack` with flat
   `{"url":"https://..."}`. Inspect `/web/scrape` output for business fit when
   needed, and `/brand/retrieve` for domain identity. Label discrepancies between
   stored and live observations. A live homepage-only scan may miss technology
   previously observed on a cart, docs, or other secondary page.
6. Deduplicate by normalized domain, preserving genuinely distinct storefronts.
   Merge different domains into one company only when public evidence supports
   that relationship. Apply the user's criteria and explain each qualification.

```sh
scripts/crawlora.sh /datasets/techstack/facets facet=technology ecommerce=Shopify
scripts/crawlora.sh /datasets/techstack/search \
  technology=Shopify technology=Klaviyo is_infrastructure=false page_size=10
```

## Output and limits

Return a table or CSV with domain, company identity when verified, matching
technologies, detection confidence/evidence, dataset refresh time, live-check
time/status, fit rationale, and source URLs. Preserve unknowns.

- `not=Klaviyo` means the dataset did not detect Klaviyo, not proof the site
  does not use it. Private/backend-only tools may leave no public evidence.
- `reachable=true` alone does not prove a usable page was fetched. Inspect
  `failure_reason` and related status fields when present before trusting absence.
- Technology counts are counts within this corpus/run, not internet-wide market
  share. Do not infer company geography from a TLD alone.
- Bound live checks to the shortlist. Back off on `429`, retry a transient
  `5xx` once, and stop on `401`/`403`. Check application `code`. A failed refresh
  leaves a dataset-only observation, not a confirmed current installation.
- Exporting a research list does not authorize outreach or a CRM write.
