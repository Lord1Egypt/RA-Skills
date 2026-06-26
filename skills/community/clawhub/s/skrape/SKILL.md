---
name: Skrape
description: Ethical web data extraction with robots exclusion protocol adherence, throttled scraping requests, and privacy-compliant handling ("Scrape responsibly!").
---

## Respect Creative Work

- **Design & text copying**: Avoid copying design elements or substantial portions of text; while facts and data aren't typically protected by copyright, their presentation (website layouts, specific text, compilations) often is.
- **Source attribution**: Properly attribute sources when appropriate; this shows integrity and builds trust with both content creators and your own audience.
- **Creator impact**: Consider how your use might impact the original creator's work; respecting copyrighted material demonstrates ethical conduct.

## Pre-Extraction Verification Steps

**I. Access Authorization** — Retrieve `{domain}/robots.txt` and review `/terms` or `/tos` endpoints. Proceed only if neither prohibits extraction; halt if blocked or explicit restrictions exist.

**II. Data Classification** — Distinguish between public factual information (listings, pricing) versus personal information. The latter invokes GDPR/CCPA obligations and requires stronger justification.

**III. Preferred Channels** — Check whether the platform offers an API. If available, use it instead of direct extraction. Never access content requiring authentication without proper credentials.

## Operational Conduct & Compliance

- **Request discipline**: Throttle at 2-3 seconds minimum, honor 429 with progressive backoff, maintain connection pooling, and use authentic User-Agent with contact email.
- **Access boundaries**: robots.txt disregard carries uncertain legal standing (Meta v. Bright Data 2024); publicly accessible content is typically permissible (hiQ v. LinkedIn 2022); circumventing access controls risks CFAA exposure (Van Buren v. US 2021).
- **Data & content restrictions**: Personal information without permission triggers GDPR/CCPA breach; redistributing copyrighted material constitutes copyright violation.

## Information Stewardship

- **PII & profiling restrictions**: Remove personal information promptly and avoid correlating data to identify individuals.
- **Limit retention**: Store only necessary data, purge the rest.
- **Activity logging**: Record extraction events (what, when, source) to demonstrate responsible conduct if questioned.

Implementation patterns and robots.txt evaluation logic in `code.md`
