## Description:

Search public Google News headlines, sources, and links through ScraperSocial and return structured results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find recent public news about a topic, person, or company and monitor headline coverage without fetching full articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News queries and the ScraperSocial API key are sent to ScraperSocial.

Mitigation: Use only an intended API key and avoid sensitive search terms.

Risk: News searches may consume API credits per returned article.

Mitigation: Set --limit to control result volume and cost.

## Reference(s):

- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON news search results with headlines, sources, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated results may include a next cursor and request ID; full article text is not provided.]

## Skill Version(s):

1.0.4 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
