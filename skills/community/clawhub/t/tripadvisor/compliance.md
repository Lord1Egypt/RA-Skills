# Tripadvisor Compliance Boundaries

This skill must stay inside official access and policy-safe behavior.

## Hard rules

- No scraping of hidden or blocked content.
- No CAPTCHA bypass, bot evasion, or anti-detection tricks.
- No automated account actions without explicit user request.
- No data collection outside user-approved travel context.

## Official signals to respect

- Tripadvisor Content API exists with self-serve access and monthly call limits.
- Higher-volume API usage requires partnership approval.
- Tripadvisor terms include restrictions on robots, spiders, scraping, and unauthorized automated access.

## Allowed behavior

- Official API requests with valid key.
- Standard browser navigation of public pages.
- User-assisted extraction and summarization from visible content.

## Output policy

- Always disclose data source: API, UI, or hybrid.
- Flag uncertainty when data freshness cannot be guaranteed.
- Keep recommendation logic transparent.
