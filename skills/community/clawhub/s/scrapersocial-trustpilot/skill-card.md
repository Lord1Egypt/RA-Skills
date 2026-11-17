## Description:

Retrieves public company reviews from Trustpilot as JSON through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can look up company reviews to assess reputation or monitor review activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send the requested company URL or handle and the API key to ScraperSocial.

Mitigation: Use this skill only if sharing those details with ScraperSocial is acceptable.

Risk: Each returned review consumes a credit.

Mitigation: Set a review limit and paginate only when needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nikhonit/skills/scrapersocial-trustpilot)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review listings may include pagination metadata and a request ID; requests are limited to 50 reviews at a time.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
