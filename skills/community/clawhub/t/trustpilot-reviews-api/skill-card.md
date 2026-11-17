## Description:

Search Trustpilot businesses, inspect ratings and profiles, browse categories, and retrieve filtered reviews as structured JSON through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business analysts use this skill to find businesses, assess TrustScores and review trends, and retrieve public Trustpilot reviews and category rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and the API key are sent to Scavio.

Mitigation: Obtain user approval for external queries and keep the API key in a protected environment variable.

Risk: API requests consume free or paid credits, including paginated searches.

Mitigation: State the credit cost before bulk requests and limit pages to what the user needs.

Risk: Business contact details and review data may be used in ways that conflict with privacy obligations or platform terms.

Mitigation: Use returned data only for the user's stated purpose, respecting applicable privacy laws and platform terms.

## Reference(s):

- [Scavio Trustpilot search documentation](https://scavio.dev/docs/trustpilot-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api)
- [Scavio Trustpilot reviews documentation](https://scavio.dev/docs/trustpilot-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api)
- [Scavio API rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=trustpilot-reviews-api)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [Structured JSON responses and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Six API endpoints; each request consumes two credits; review pages are limited to 200 reviews per filter combination.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
