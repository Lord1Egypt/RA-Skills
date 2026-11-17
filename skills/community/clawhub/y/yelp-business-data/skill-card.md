## Description:

Guides agents in searching Yelp businesses through Scavio, retrieving business details, and paging through reviews and owner responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use this skill to find local businesses, examine business details, and gather reviews for local research, reputation monitoring, or competitor comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, locations, business IDs, and review filters are sent to Scavio using an API key.

Mitigation: Avoid sensitive private locations or queries unless comfortable with Scavio handling them; keep the API key in a secret store or environment variable.

Risk: API requests consume paid credits, including empty results or duplicate review pages.

Mitigation: Budget requests before paging, use the first review page included with business details, and stop when no next page is available.

## Reference(s):

- [Scavio Yelp search documentation](https://scavio.dev/docs/yelp-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=yelp-business-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=yelp-business-data)
- [ClawHub skill listing](https://clawhub.ai/scavio-ai/skills/yelp-business-data)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with code examples or structured JSON business and review data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API calls require SCAVIO_API_KEY and consume credits.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
