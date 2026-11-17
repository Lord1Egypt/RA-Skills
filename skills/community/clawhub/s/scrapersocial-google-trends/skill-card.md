## Description:

Explore relative Google Trends interest over time and rising related searches through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content researchers use this skill to check interest trends and identify rising related queries for keyword research and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill sends a ScraperSocial API key to api.scrapersocial.com.

Mitigation: Provide the key only if you trust ScraperSocial and handle it as a credential.

Risk: API requests spend ScraperSocial credits.

Mitigation: Check the credit budget before running repeated or large queries.

Risk: Relative interest can be mistaken for absolute search volume.

Mitigation: Describe results as indexed interest, not search counts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nikhonit/skills/scrapersocial-google-trends)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [JSON responses with trend data; plain-text guidance when used by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trend interest is relative, not absolute search volume; rising queries may be paginated.]

## Skill Version(s):

1.0.4 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
