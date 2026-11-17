## Description:

Scrapes public Instagram posts tagged at a specific location using apidojo's Instagram Location scraper on Apify and returns post URLs, captions, author handles, engagement counts, and timestamps for UGC and creator discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External hospitality teams, event marketers, and UGC curation teams use this skill to collect public location-tagged Instagram posts, rank engagement, identify creators, and prepare location content reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports location-based discovery of people and creators from public Instagram content.

Mitigation: Use it only for lawful, platform-compliant analysis of public content and avoid sensitive profiling or unsupported conclusions about individuals.

Risk: Collected UGC may be reused or creators may be contacted for outreach.

Mitigation: Get permission before republishing content or contacting creators, and keep outreach aligned with applicable platform and privacy expectations.

Risk: The artifact documents an Apify token-in-query curl fallback.

Mitigation: Prefer an Authorization header, MCP server, or helper flow, and avoid placing API tokens in URLs or logs.

Risk: Instagram location tags can match the wrong or nearby place.

Mitigation: Manually review top posts and location IDs before using results for reporting, reuse, or creator outreach.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-instagram-location-content)
- [Apify actor run API endpoint](https://api.apify.com/v2/acts/apidojo~instagram-location-scraper/runs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, plus optional CSV or JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include post URLs, captions, author handles, likes, comments, timestamps, creator rankings, and caption themes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
