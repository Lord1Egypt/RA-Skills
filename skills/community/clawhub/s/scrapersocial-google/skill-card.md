## Description:

Retrieves public Google search results, business profiles, reviews, updates, and company ads through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing teams use this skill to research search results, monitor public business information and reviews, and examine company ads for local SEO and competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, business URLs or handles, and the API key are sent to ScraperSocial.

Mitigation: Use only approved queries and a dedicated API key; do not submit sensitive information.

Risk: API requests consume credits, particularly when retrieving paginated results.

Mitigation: Set result limits and page only when needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nikhonit/skills/scrapersocial-google)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses contain data and a request ID; paginated results may include a cursor.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
