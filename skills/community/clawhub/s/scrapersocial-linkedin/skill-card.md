## Description:

Retrieves public LinkedIn profiles, company information, jobs, posts, engagement, and search results through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, researchers, and developers use this skill to look up public LinkedIn profiles, research companies and jobs, and examine post engagement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profile and contact data can include personal information.

Mitigation: Use a lawful basis for processing and avoid bulk collection where privacy laws or platform terms restrict it.

Risk: Using the skill requires a ScraperSocial API key.

Mitigation: Provide the key only if you intend to use ScraperSocial; keep it out of shared responses and logs.

Risk: Data requests consume ScraperSocial credits, with contact lookups costing more.

Mitigation: Request only the needed profile section and review credit costs before making queries.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nikhonit/skills/scrapersocial-linkedin)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text or JSON with public LinkedIn data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated results may include a next cursor and request ID.]

## Skill Version(s):

1.0.4 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
