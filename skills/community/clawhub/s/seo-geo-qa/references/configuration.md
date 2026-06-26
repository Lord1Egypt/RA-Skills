# Configuration

Use an optional JSON config file to set project defaults.

## Example

```json
{
  "siteName": "Example Site",
  "siteDomain": "example.com",
  "reportDir": "qa-reports",
  "minFaqCount": 2,
  "minExternalLinks": 5,
  "maxTierD": 1,
  "tierADomains": ["mycompany.com", "docs.mycompany.com"],
  "tierBDomains": ["partner-site.com"],
  "brandDomains": ["mycompany.com"]
}
```

## Fields

- `siteName` — optional metadata for your own reporting
- `siteDomain` — used to distinguish internal vs external links
- `reportDir` — report output root, relative to workspace root
- `minFaqCount` — warning threshold for FAQ count (default: 2)
- `minExternalLinks` — warning threshold for thin citation profiles (default: 5)
- `maxTierD` — maximum allowed TIER-D sources before FAIL (default: 1)
- `tierADomains` — additional domains to treat as TIER-A (first-party / official)
- `tierBDomains` — additional domains to treat as TIER-B (reputable secondary)
- `brandDomains` — domain roots for same-brand redirect detection (e.g., subdomains that should not count as "moved")

## Notes

- The runner works without config.
- Keep config small. If your config becomes huge, your process is probably overfitted.
- Prefer stable project defaults over article-by-article micromanagement.
