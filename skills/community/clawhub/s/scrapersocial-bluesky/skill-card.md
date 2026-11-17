## Description:

Retrieves public Bluesky profiles, user posts, and keyword search results through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to look up public Bluesky accounts, follow their posts, and search public conversations by keyword.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill grants it access to a ScraperSocial API key.

Mitigation: Provide a dedicated key only if you trust the service, and keep it out of shared outputs.

Risk: Public Bluesky lookups can consume ScraperSocial credits.

Mitigation: Limit requests and paginated results to what the task requires; monitor credit usage.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nikhonit/skills/scrapersocial-bluesky)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public profile or post data; paginated results may include a next cursor and responses include a request ID.]

## Skill Version(s):

1.0.4 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
