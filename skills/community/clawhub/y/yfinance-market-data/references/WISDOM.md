# Cross-Project Wisdom

Total: **8**

## `CW-DATA-SOURCING-001` — Exponential backoff retry with rate limit detection
**From**: finance-bp-079--akshare, finance-bp-114--edgar-crawler · **Applicable to**: data-sourcing

Implement retry logic with exponential backoff specifically for HTTP 429 rate limit responses. Retrying immediately on rate limit errors worsens the block situation. Separate retry logic for transient network errors (TimeoutError, ConnectionError) from permanent errors (ValueError, KeyError) prevents resource waste and masks underlying bugs.

## `CW-DATA-SOURCING-002` — Strict date format validation and standardization
**From**: finance-bp-070--edgartools, finance-bp-079--akshare, finance-bp-084--eastmoney · **Applicable to**: data-sourcing

Validate date formats strictly (YYYY-MM-DD pattern with leap year and month-end checks) before processing XBRL or API data. Convert date strings between formats (YYYYMMDD to YYYY-MM-DD) when storing to databases. Invalid dates corrupt downstream financial calculations.

## `CW-DATA-SOURCING-003` — XBRL fact attribute completeness enforcement
**From**: finance-bp-070--edgartools, finance-bp-114--edgar-crawler · **Applicable to**: data-sourcing

Extract and validate all essential XBRL fact attributes (concept, value, period, unit) from every fact. Missing attributes cause financial analysis queries to return incomplete or misleading results. Period type (instant vs duration) must be correctly distinguished for accurate balance sheet rendering.

## `CW-DATA-SOURCING-004` — Streaming parser threshold for large documents
**From**: finance-bp-070--edgartools, finance-bp-128--yfinance · **Applicable to**: data-sourcing

Implement streaming parser activation when documents exceed configurable thresholds (10MB default). This prevents OOM errors on large NPORT-P filings or bulk document downloads. Also require timezone information for time-series data to prevent DST offset corruption.

## `CW-DATA-SOURCING-005` — Data accuracy disclaimer requirements
**From**: finance-bp-079--akshare, finance-bp-128--yfinance, finance-bp-097--OpenBB · **Applicable to**: data-sourcing

Always present scraped or third-party financial data with proper caveats about accuracy limitations and delays. Claims of guaranteed accuracy, real-time capabilities, or Yahoo/provider affiliation violate terms of service and can lead to user financial losses from reliance on delayed or incorrect data.

## `CW-DATA-SOURCING-006` — Atomic write ordering for versioned storage
**From**: finance-bp-103--ArcticDB · **Applicable to**: data-sourcing

Write atom keys (TABLE_DATA, TABLE_INDEX, VERSION) before updating mutable reference keys (VERSION_REF, SNAPSHOT_REF). Never modify atom keys after writing to preserve content-addressed storage invariants. This prevents readers from accessing incomplete data in multi-writer scenarios.

## `CW-DATA-SOURCING-007` — HTTP status code validation before data processing
**From**: finance-bp-079--akshare, finance-bp-097--OpenBB · **Applicable to**: data-sourcing

Always validate HTTP response status codes before processing response data. Error responses (404, 500) may contain HTML error pages that corrupt downstream JSON parsing. Explicitly check for HTTP 429 and raise RateLimitError for proper handling by callers.

## `CW-DATA-SOURCING-008` — Quality gates for financial recommendations
**From**: finance-bp-084--eastmoney · **Applicable to**: data-sourcing

Apply fundamental quality filters (ROE thresholds, OCF/Profit ratios, debt ratios) before generating financial recommendations. Without quality gates, low-quality stocks may be recommended for positions, leading to investment losses. Separate on-demand computation from scheduled pre-computation to handle API rate limits.
