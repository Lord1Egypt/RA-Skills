## Description:

Decode why a specific LinkedIn post performed unusually well and turn the analysis into a reusable template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porenes](https://clawhub.ai/user/porenes)

### License/Terms of Use:

MIT-0

## Use Case:

External LinkedIn creators and professionals use this skill to understand the writing choices behind a post's performance and adapt those patterns into original posts. It requires the Taplio MCP to retrieve relevant posts and, when applicable, the user's profile and analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected Taplio account may expose permissions beyond those needed for post analysis.

Mitigation: Review Taplio connector permissions before connecting and use only an account and access scope approved for this workflow.

Risk: Topic searches sent to Taplio may disclose confidential information.

Mitigation: Keep confidential details out of search queries.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/porenes/skills/taplio-linkedin-viral-post-analyzer)
- [Taplio Claude connector](https://claude.ai/customize/connectors/id/taplio)
- [Taplio MCP endpoint](https://mcp.taplio.com)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Structured post analysis with a reusable writing template and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Taplio MCP may not provide the original author's follower count or per-post baseline, so some performance comparisons cannot be confirmed.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
