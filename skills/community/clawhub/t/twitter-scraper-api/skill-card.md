## Description:

Helps agents search public X content and retrieve tweets, conversations, profiles, social connections, Communities, and trending topics through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can guide agents to find and summarize public X posts, profiles, followers, Communities, and trends for research or monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: X search terms, handles, tweet and Community IDs, and the API key are sent to Scavio.

Mitigation: Inform users before use and keep the API key in an environment variable or secret store.

Risk: Collecting profiles and social connections at scale can expose personal data or enable targeted surveillance.

Mitigation: Use only for lawful, policy-compliant purposes; avoid harassment and seek confirmation before broad collection or retention.

Risk: Broad pagination consumes API credits and may collect more personal data than needed.

Mitigation: Confirm the intended scope before paginating through many pages and stop when enough data has been retrieved.

## Reference(s):

- [Scavio X API documentation](https://scavio.dev/docs/x-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=twitter-scraper-api)
- [Scavio API rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=twitter-scraper-api)
- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/twitter-scraper-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands]

**Output Format:** [Markdown responses with structured X data and optional JSON or code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports retrieved content and engagement metrics as returned; paginated requests can consume additional credits.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
