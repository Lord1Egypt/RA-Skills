## Description:

Search public Polymarket listings and odds through ScraperSocial and return the results as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can search prediction markets and compare indicative odds with other forecast signals. This skill retrieves listings only; it does not place trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market searches and the API key are sent to ScraperSocial.

Mitigation: Use a dedicated API key and submit only queries you are comfortable sharing with ScraperSocial.

Risk: Returned odds may be cached and are not guaranteed execution prices.

Mitigation: Present odds as indicative market prices, not facts or live trade quotes; refresh and verify before consequential use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nikhonit/skills/scrapersocial-polymarket)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON market listings or a text summary of the returned odds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only results may be cached; responses include a request ID and may include pagination metadata.]

## Skill Version(s):

1.0.4 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
