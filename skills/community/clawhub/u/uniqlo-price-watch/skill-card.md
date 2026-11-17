## Description:

Tracks product prices on UNIQLO China, stores watched items in a local CSV file, and compares current official product-page prices with saved baseline prices before responding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjy233](https://clawhub.ai/user/yjy233)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to monitor one or more UNIQLO China products, keep a local record of tracked items, and ask whether watched products have dropped in price.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product URLs may be sent to FireCrawl when API-based scraping is used.

Mitigation: Use the skill only when sharing those product URLs with FireCrawl is acceptable, or rely on the browser-based fallback instead.

Risk: The skill can read a FireCrawl API key from the environment and can use an override endpoint.

Mitigation: Keep FireCrawl credentials scoped and avoid setting FIRECRAWL_API_URL unless the endpoint is trusted.

Risk: Local shopping history is retained in uniqlo/uniqlo-price-watch.csv.

Mitigation: Review or delete the CSV file when tracked-item history is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yjy233/skills/uniqlo-price-watch)
- [Publisher profile](https://clawhub.ai/user/yjy233)
- [UNIQLO China search](https://www.uniqlo.cn/search.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration]

**Output Format:** [Markdown responses with inline shell commands and local CSV updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update uniqlo/uniqlo-price-watch.csv with product names, search URLs, prices, and timestamps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
