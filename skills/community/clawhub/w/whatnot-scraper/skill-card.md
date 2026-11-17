## Description:

Collects public Whatnot listings, shows, seller profiles, reviews, shops and category rankings, with optional price summaries and change tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxouf](https://clawhub.ai/user/maxouf)

### License/Terms of Use:

MIT-0

## Use Case:

People researching Whatnot listings, sellers and live shows can use this skill to collect public marketplace data, compare asking prices and track changes over time. It supports one-off lookups as well as scheduled monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, seller lists and tracking settings are sent to Apify; the security evidence says results and tracking state are stored there.

Mitigation: Review Apify's data handling and send only information you are comfortable sharing with that service.

Risk: Security analysis was partial because some local references could not be resolved.

Mitigation: Review the external Actor integrations and unresolved references before use.

## Reference(s):

- [Skill homepage](https://github.com/maxouf/sherwood-skills/tree/main/skills/whatnot-scraper)
- [Sherwood Actor MCP endpoint](https://mcp.apify.com/?tools=sherwood/whatnot-scraper)

## Skill Output:

**Output Type(s):** [CSV files, Structured data, Text, Guidance]

**Output Format:** [CSV datasets and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Listing prices are asking prices; the skill does not provide sold prices or buyer identities.]

## Skill Version(s):

1.0.0 (source: frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
