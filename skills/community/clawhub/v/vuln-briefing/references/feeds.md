# Feed API Reference

## Endpoints

| Endpoint | Description | Upstream Source |
|----------|-------------|----------------|
| `/api/nvd/latest` | Latest 5 CVEs | NIST NVD |
| `/api/nvd/cve?cveId=CVE-XXXX-XXXXX` | Look up specific CVE | NIST NVD |
| `/api/cisa/kev` | Known exploited vulnerabilities | CISA KEV Catalog |

Base URL: `https://feed-monitor.security-feeds.workers.dev`

## Query Parameters (NVD)

- `cveId` — look up a specific CVE (e.g., CVE-2026-12345)

## Rate Limits

- NVD upstream: 5 requests per 30 seconds
- CISA upstream: no hard limit, but space requests 5 seconds apart

## Formatting Rules

- Always include the current date at the top of the briefing
- Group CVEs by severity: Critical first, then High, Medium, Low
- Include CVSS v3 base score where available
- Note whether a patch or workaround exists
- For CISA KEV entries, include the due date for remediation
- Keep summaries concise — under 500 words unless the user requests detail
- Use markdown tables for multi-CVE summaries

## Error Handling

- HTTP 502: upstream feed temporarily unavailable, retry in 30 seconds
- HTTP 404: unknown endpoint, check the path
- If NVD returns 403 via upstream, rate limit exceeded — wait 30 seconds
