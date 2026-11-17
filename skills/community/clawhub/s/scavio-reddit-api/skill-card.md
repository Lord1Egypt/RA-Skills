## Description:

Search Reddit, read posts and threaded comments, and pull subreddit, user, popular, and trending data as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to research Reddit discussions, monitor public sentiment and brand mentions, collect subreddit or redditor activity, and retrieve structured data for RAG workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reddit research queries, post IDs, subreddit names, usernames, cursors, and the Scavio API key are sent to a third-party API.

Mitigation: Install and use the skill only when this third-party data sharing is acceptable; avoid sending sensitive or private data in API requests.

Risk: The optional LangChain package adds dependency supply-chain exposure.

Mitigation: Prefer the direct API workflow for minimal dependencies, or install the optional package in a virtual environment with a pinned and audited version.

Risk: The skill retrieves public Reddit content that may include NSFW material or user-generated claims.

Mitigation: Surface returned flags such as is_nsfw and verify user-generated content before relying on it for decisions or summaries.

## Reference(s):

- [Scavio Reddit API documentation](https://scavio.dev/docs/reddit-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits)
- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/scavio-reddit-api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, json]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; Reddit endpoints return structured JSON and cost 1 credit per call.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
