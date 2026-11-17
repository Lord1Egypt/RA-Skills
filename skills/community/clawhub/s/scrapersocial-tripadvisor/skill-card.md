## Description:

Retrieves public Tripadvisor place listings and reviews through ScraperSocial for travel research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Travel researchers and agents use the skill to search hotels, restaurants, and attractions and summarize public reviews. It does not provide booking prices or availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ScraperSocial is an independent, unofficial provider of Tripadvisor data.

Mitigation: Confirm the provider is appropriate before using its data for decisions.

Risk: Searches and review requests may consume API credits per returned item.

Mitigation: Set a small review limit and page only when more results are needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nikhonit/skills/scrapersocial-tripadvisor)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON listings and reviews; optional natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated results support a cursor and a maximum of 50 items per request.]

## Skill Version(s):

1.0.4 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
