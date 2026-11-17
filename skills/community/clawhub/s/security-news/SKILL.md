---
name: security-news
description: Get the latest cybersecurity news, vulnerability disclosures, and threat intelligence. Aggregates CVEs from NIST NVD, CISA KEV catalog, and security advisories via a unified feed API. No API key needed.
homepage: https://cve.mitre.org
metadata:
  {
    "openclaw":
      {
        "emoji": "📰",
        "requires": { "bins": ["curl"] },
      },
  }
---

# Security News

Stay up to date with cybersecurity news, vulnerability disclosures, and threat intelligence.

## When to Use

- "What are the latest CVEs?"
- "Any new security advisories?"
- "Cybersecurity news today"
- "Check CVE-2026-XXXXX"
- "What did CISA publish this week?"

## Sources

Aggregates from public feeds via a unified API:

1. **NIST NVD** — Latest CVEs and severity scores
2. **CISA KEV** — Known exploited vulnerabilities catalog
3. **CISA Advisories** — ICS and cybersecurity advisories

## Commands

### Latest CVEs

```bash
curl -s "https://feed-monitor.security-feeds.workers.dev/api/nvd/latest"
```

### Check Specific CVE

```bash
curl -s "https://feed-monitor.security-feeds.workers.dev/api/nvd/cve?cveId=CVE-2026-XXXXX"
```

### CISA Known Exploited Vulnerabilities

```bash
curl -s "https://feed-monitor.security-feeds.workers.dev/api/cisa/kev" | head -c 4000
```

## Configuration

Read `references/feeds.md` for query parameters, rate limits, and output formatting rules.

## Output Format

- **Date/Time**
- **Top CVEs** (ID, severity, affected product, patch status)
- **CISA Advisories** (title, sector, action required)
- **Trending** (notable incidents, campaigns, disclosures)

## Notes

- All sources are public and free (no API key required)
- Feeds are rate-limited; space requests at least 5 seconds apart
- Verify critical findings against primary vendor advisories
