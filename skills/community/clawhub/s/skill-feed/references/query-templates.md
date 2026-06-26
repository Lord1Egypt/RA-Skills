# Query Templates

Use these templates to build Q1/Q2/Q3 from failure context.

## Social posting

- Q1: `tweet automation`
- Q2: `x twitter schedule post cron`
- Q3: `twitter post failed {error_code} {error_token}`

## Auto-reply bots

- Q1: `auto reply bot`
- Q2: `telegram auto reply schedule`
- Q3: `bot reply failed timeout permission denied`

## Daily reports/content pipeline

- Q1: `daily report automation`
- Q2: `ai web3 daily report generate publish`
- Q3: `daily report publish failed api timeout`

## GitHub workflow

- Q1: `github automation`
- Q2: `gh pr issue run ci`
- Q3: `github action failed permission 403`

## Web scraping / browser automation

- Q1: `browser automation scraping`
- Q2: `headless browser crawl extract page data`
- Q3: `browser automation failed {error_code} selector timeout`

## Web search / research

- Q1: `web search`
- Q2: `ai web search fetch summarize`
- Q3: `search failed {error_code} api key quota`

## File and media processing

- Q1: `file media processing`
- Q2: `summarize transcript video pdf convert`
- Q3: `media processing failed {error_code} format unsupported`

## Scheduling / cron jobs

- Q1: `schedule cron automation`
- Q2: `proactive cron recurring task trigger`
- Q3: `cron schedule failed {error_code} missed trigger`

## Multi-API / SaaS integration

- Q1: `api integration gateway`
- Q2: `connect saas api multi-service workflow`
- Q3: `api integration failed {error_code} auth scope mismatch`

## Error token extraction hints

Extract compact error markers:

- HTTP: `400 401 403 404 409 429 500 502 503`
- Auth: `invalid token`, `unauthorized`, `forbidden`
- Limits: `rate limit`, `quota`
- Infra: `timeout`, `connection reset`, `dns`
- Payload: `invalid param`, `bad request`, `schema`
