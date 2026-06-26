# Routing Guide

## Priority order

1. `supermemory` — recover prior decisions, preferences, and related work.
2. `self-improvement` — use as a light quality check when the route or answer needs internal review.
3. `brainstorming` — sharpen the question, compare approaches, and remove ambiguity.
4. `zo-research-topic` — general research and synthesis.
5. `web-scraper` — source verification, extraction, and current web evidence.
6. Domain specialist skills — only the ones that materially improve the answer.

## Minimal routing rule

Choose the smallest set of skills that can answer the question confidently.

## Clarifying question rule

If the question is vague, stop after one clarifying question instead of guessing.

## Evidence rule

Use `web-scraper` whenever the answer depends on a specific page, quote, current claim, or other web evidence that must be checked.

## Specialist mappings

### Strategy and marketing
- `marketing-psychology`
- `marketing-ideas`
- `pricing-strategy`
- `free-tool-strategy`
- `launch-strategy`
- `competitor-alternatives`

### Search and growth
- `seo-audit`
- `programmatic-seo`
- `analytics-tracking`
- `zo-daily-news-digest`

### Research and economics
- `market-research`
- `zo-research-topic`

## Script-backed helpers

- `web-scraper/scripts/scraper.py` — page scraping and extraction.
- `self-improvement/scripts/audit.py` — internal audit and capability review.
- `supermemory/scripts/memory.py` — memory search and ingestion.
- `market-research/scripts/research.py` — BLS, FRED, and Census data.

## Output template

Use this exact answer structure:

1. Question breakdown
2. Skills used
3. Evidence
4. Recommendation
5. Next steps
